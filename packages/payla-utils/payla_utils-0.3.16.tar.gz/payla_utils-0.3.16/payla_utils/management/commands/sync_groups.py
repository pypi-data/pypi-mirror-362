import json
from pathlib import Path
from typing import Any

import structlog
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction
from pydantic import BaseModel

from payla_utils.settings import payla_utils_settings

logger = structlog.get_logger(__name__)

User = get_user_model()


# region: Schema classes for parsing users configurations from JSON file
class UserBasicInfoConfig(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str


class UserEnvConfig(BaseModel):
    is_superuser: bool
    is_staff: bool
    is_active: bool


class UserConfig(BaseModel):
    basic_info: UserBasicInfoConfig
    envs: dict[str, UserEnvConfig]
    groups: list[str]

    def to_minimal_dict(self, env_str: str) -> dict:
        basic_info = self.basic_info
        env_config = self.envs[env_str]
        return {
            "first_name": basic_info.first_name,
            "last_name": basic_info.last_name,
            "email": basic_info.email,
            "is_active": env_config.is_active,
            "is_staff": env_config.is_staff,
            "is_superuser": env_config.is_superuser,
        }


#  endregion


class Command(BaseCommand):
    """
    Django management command to set up groups, permissions, and users.

    This command performs the following functions:
        1. Adding Permissions: it reads a JSON file that defines groups and their respective permissions.
           For each group, the command creates it in the database (if it doesn't already exist) and assigns
           the specified permissions to it.
        2. Removing Unspecified Permissions: the command also checks for and removes any permissions
           currently assigned to the group but not specified in the JSON configuration. This ensures that
           each group only has the permissions explicitly defined in the configuration.
        3. Adding Users (if they don't already exist): it reads ANOTHER JSON file that contains essential data for
           creating users and assigning them to appropriate groups. User hashed passwords are read from an environment
           variable that's taken from AWS secret manager.
        4. Removing users from groups they should not belong to, correcting potential mistakes made via Admin.
        5. Clearing User-Level Permissions: users should receive permissions only via their assigned groups.

    Example 1: JSON structure for group permissions(core is the app_label, bank is the model name, view_bank is the
    permission codename):

    {
        "core": {
            "bank": {
                "view_bank": [
                    {"group": "customer_service_level_1", "envs": ["playground", "prod", "stage"]},
                ],
                "change_bank": [
                    {"group": "finance", "envs": ["prod", "stage"]},
                ]
            }
        }
    }

    Example 2: JSON structure for group users:
    [
        {
            "basic_info": {
                "username": "john.doe@payla.de",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@payla.de"
            },
            "envs": {
                "stage": {
                    "is_superuser": false,
                    "is_staff": true,
                    "is_active": true,
                },
                "playground": {
                    "is_superuser": false,
                    "is_staff": true,
                    "is_active": true,
                },
                "prod": {
                    "is_superuser": false,
                    "is_staff": true,
                    "is_active": true,
                }
            },
            "groups": [
                "Backoffice",
                "engineering",
                "core"
            ]
        }
    ]

    Example 3: AWS secret manager environment variable for user passwords (per environment):

    USER_PASSWORDS = {
        "username1": "pbkdf2_sha256$870000$YPcJGsFOSJM3uEoNbSePfX$tWi4dy66J9I7BOV6De04AbaVD8g9UBGH9wzatGYSt2c=",
        "username2": "pbkdf2_sha256$870000$YPcJGsFOSJM3uEoNbSePfX$tWi4dy66J9I7BOV6De04AbaVD8g9UBGH9wzatGYSt2c=",
    }

    How to create the hash for the password:

    ```python
    from django.contrib.auth.hashers import make_password
    make_password('your_password_here')
    ```

    """

    help = 'Syncs groups permissions and users based on JSON configuration files.'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.current_env = ''
        self.groups_permissions: dict[str, list[str]] = {}

    def assign_group_permissions(self, groups_permissions_config: dict):
        for app_label, app_data in groups_permissions_config.items():
            for model_name, model_data in app_data.items():
                for permission_codename, permission_data in model_data.items():
                    self.process_group_permission(app_label, model_name, permission_codename, permission_data)

    def process_group_permission(
        self, app_label: str, model_name: str, permission_codename: str, permission_data: dict
    ):
        permission_code = f"{permission_codename}.{app_label}.{model_name}"

        try:
            permission = Permission.objects.get_by_natural_key(permission_codename, app_label, model_name)
        except Permission.DoesNotExist:
            logger.exception("Permission %s not found!", permission_code)
            return

        for permission_group in permission_data:
            envs = permission_group.get('envs', [])
            groups_names = (
                permission_group['groups']
                if isinstance(permission_group['groups'], list)
                else [permission_group['group']]
            )

            if self.current_env not in envs:
                logger.info(
                    "Skipping permission %s for group(s) %s in environment %s",
                    permission_codename,
                    groups_names,
                    self.current_env,
                )
                continue

            for group_name in groups_names:
                # Create group
                group = Group.objects.get_or_create(name=group_name)[0]

                self.groups_permissions.setdefault(group_name, [])

                # Add permission to group
                group.permissions.add(permission)
                logger.info("Added permission %s to group %s", permission_codename, group_name)
                self.groups_permissions[group_name].append(permission_codename)

    def remove_unwanted_group_permissions(self) -> None:
        # Remove unused permissions from group
        for group_name, permissions in self.groups_permissions.items():
            group = Group.objects.get(name=group_name)
            removed_permissions = 0
            for permission in group.permissions.all():
                if permission.codename not in permissions:
                    logger.info("Removing permission %s from group %s", permission.codename, group_name)
                    group.permissions.remove(permission)
                    removed_permissions += 1
            logger.info("Removed %s permissions from group %s", removed_permissions, group_name)

    def sync_group_permissions(self) -> None:
        if not payla_utils_settings.GROUPS_PERMISSIONS_FILE_PATH:
            logger.warning("Skipping groups permissions sync. Missing GROUPS_PERMISSIONS_FILE_PATH in settings.")
            return

        with Path.open(payla_utils_settings.GROUPS_PERMISSIONS_FILE_PATH, encoding='utf-8') as f:
            groups_permissions_config = json.loads(f.read())

        self.assign_group_permissions(groups_permissions_config)
        self.remove_unwanted_group_permissions()

    def update_or_create_user(self, user_config: UserConfig, password: str) -> AbstractUser:
        basic_info_config = user_config.basic_info

        user_db = User.objects.filter(username=basic_info_config.username).first()

        if user_db:
            for attr, value in user_config.to_minimal_dict(self.current_env).items():
                setattr(user_db, attr, value)
        else:
            user_db = User.objects.create_user(
                username=basic_info_config.username,
                **user_config.to_minimal_dict(self.current_env),
            )

        if password:
            user_db.password = password
        else:
            user_db.set_unusable_password()

        user_db.save()

        return user_db

    def add_user_to_groups(self, user: AbstractUser, groups: list[str]) -> None:
        for group_name in groups:
            group, __ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

    def remove_unwanted_groups(self, user: AbstractUser, desired_groups: list[str]) -> None:
        for group in user.groups.all():
            if group.name not in desired_groups:
                user.groups.remove(group)

    def clear_user_level_permissions(self, user: AbstractUser) -> None:
        user_level_permissions = user.get_user_permissions()
        if user_level_permissions:
            user.user_permissions.clear()
            logger.info(
                'User-level permissions have been cleared for: %s',
                user.username,
                user_level_permissions=user_level_permissions,
            )

    def sync_group_users(self) -> None:
        config_file = payla_utils_settings.GROUPS_USERS_FILE_PATH
        if not config_file:
            logger.warning("Skipping groups users sync. Missing GROUPS_USERS_FILE_PATH in settings.")
            return

        passwords_map = payla_utils_settings.USER_PASSWORDS
        if not passwords_map:
            logger.warning("Skipping groups users sync. Missing USER_PASSWORDS in settings.")
            return

        with Path.open(config_file, encoding='utf-8') as f:
            users_configs_data = json.loads(f.read())

        for user_config_data in users_configs_data:
            logger.info("Groups users sync: Processing user %s", user_config_data['basic_info']['username'])
            user_config = UserConfig(**user_config_data)

            if self.current_env not in user_config.envs:
                logger.info(
                    "Groups users sync: Skipping user %s in environment %s",
                    user_config.basic_info.username,
                    self.current_env,
                )
                continue

            password = passwords_map.get(user_config.basic_info.username)

            user_db = self.update_or_create_user(user_config, password)
            self.add_user_to_groups(user_db, user_config.groups)
            self.remove_unwanted_groups(user_db, user_config.groups)
            self.clear_user_level_permissions(user_db)

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.current_env = 'stage' if settings.ENVIRONMENT == 'local.dev' else settings.ENVIRONMENT

        self.sync_group_permissions()

        self.sync_group_users()

        return None
