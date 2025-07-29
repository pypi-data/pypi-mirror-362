"""
Storage metadata classes allowing to easily configure various user, group and topic storages (default, and extra ones).

Inside Lynceus since version 0.7.0 (instead of LynceusCLI) to share unique key creation algorithm across all projects.

"""
from abc import ABC
from dataclasses import dataclass

from lynceus.core.config import ACCESS_PERMISSION_RO, ACCESS_PERMISSION_RW, ACCESS_PERMISSION_RWD, CREATED_OBJECT_NAME_KEYWORD
from lynceus.utils import cleansed_str_value

_MOUNT_HOME_RELPATH: str = ''

_MOUNT_ORGANIZATION_RELPATH_FORMAT: str = '/organization_{organization_id:05d}/{organization_name}_resources'
_MOUNT_EXTRA_USER_RELPATH_FORMAT: str = '/{activity_name}/user_{user_id:05d}_space'
_MOUNT_GROUP_RELPATH_FORMAT: str = '/{activity_name}/{topic_name}/group_{group_id_or_order:05d}_shared_workspace'
_MOUNT_GROUP_UNIQUE_RELPATH_FORMAT: str = '/{activity_name}/{topic_name}/group_shared_workspace'
_MOUNT_GROUP_SPECIAL_ORGANIZER_RELPATH_FORMAT: str = '/{activity_name}/organizers_shared_workspace'
_MOUNT_TOPIC_RELPATH_FORMAT: str = '/{activity_name}/{topic_name}/datasets'


@dataclass
class StorageMetadataBase(ABC):
    # TheInstance ID (allowing to have an environment discrimination)
    instance_id: str

    def cleansed_instance_id(self) -> str:
        return cleansed_str_value(self.instance_id)

    def build_unique_storage_name(self) -> str:
        raise NotImplementedError()

    def get_cache_toggle(self) -> bool:
        raise NotImplementedError()

    def get_access_permission(self) -> str:
        raise NotImplementedError()

    def build_storage_prefix(self) -> str:
        raise NotImplementedError()

    def build_mount_path_relative_to_home_dir(self) -> str:
        raise NotImplementedError()


@dataclass
class FileStorageMetadata(StorageMetadataBase):
    def build_unique_storage_name(self) -> str:
        return f'{self.cleansed_instance_id()}-core-api-file-s3-storage'

    def get_cache_toggle(self) -> bool:
        # This method should NOT be used on this kind of dynamic storage.
        raise NotImplementedError()

    def get_access_permission(self) -> str:
        # This method should NOT be used on this kind of dynamic storage.
        raise NotImplementedError()

    def build_storage_prefix(self) -> str:
        # This method should NOT be used on this kind of dynamic storage.
        raise NotImplementedError()

    def build_mount_path_relative_to_home_dir(self) -> str:
        # This method should NOT be used on this kind of dynamic storage.
        raise NotImplementedError()


@dataclass
class ResourceConsumptionStorageMetadata(StorageMetadataBase):
    def build_unique_storage_name(self) -> str:
        return f'{self.cleansed_instance_id()}-resources-stats-storage'

    def get_cache_toggle(self) -> bool:
        # This method should NOT be used on this kind of dynamic storage.
        raise NotImplementedError()

    def get_access_permission(self) -> str:
        # This method should NOT be used on this kind of dynamic storage.
        raise NotImplementedError()

    def build_storage_prefix(self) -> str:
        # This method should NOT be used on this kind of dynamic storage.
        raise NotImplementedError()

    def build_mount_path_relative_to_home_dir(self) -> str:
        # This method should NOT be used on this kind of dynamic storage.
        raise NotImplementedError()


@dataclass
class OrganizationStorageMetadata(StorageMetadataBase):
    organization_id: int
    organization_name: str

    def cleansed_organization_name(self) -> str:
        return cleansed_str_value(self.organization_name)

    def build_unique_storage_name(self) -> str:
        return f'{self.cleansed_instance_id()}-{self.organization_id:05d}-org-{CREATED_OBJECT_NAME_KEYWORD}'

    def get_cache_toggle(self) -> bool:
        return True

    def get_access_permission(self) -> str:
        # Organization storages contents are only managed via client project, so here it is only RO.
        return ACCESS_PERMISSION_RO

    def build_storage_prefix(self) -> str:
        # No prefix for this type of storage.
        return ''

    def build_mount_path_relative_to_home_dir(self) -> str:
        return _MOUNT_ORGANIZATION_RELPATH_FORMAT.format(
            organization_id=self.organization_id,
            organization_name=self.cleansed_organization_name()
        )


@dataclass
class StorageMetadataWithActivity(StorageMetadataBase, ABC):
    # TheActivity ID, and name.
    activity_id: int
    activity_name: str

    def cleansed_activity_name(self) -> str:
        return cleansed_str_value(self.activity_name)


@dataclass
class UserStorageMetadata(StorageMetadataWithActivity):
    # TheUser ID.
    user_id: int

    # Defines if write permission is allowed on this storage when NOT the default one (RO by default for extra user storage).
    write_permission: bool = False

    # Defines if Cache must be forced (can be interesting when participant are using multiple instance for the same Activity, for instance cpu/gpu).
    force_cache: bool = False

    # Default toggle: if True, it corresponds to the default user/group/topic space (changes behaviour on mount point and/or permissions).
    default: bool = False

    def build_unique_storage_name(self) -> str:
        # Important: see this Gitlab Card to see before/after algorithm:
        #  

        return f'{self.cleansed_instance_id()}-{self.user_id:05d}-user-{CREATED_OBJECT_NAME_KEYWORD}'

    def get_cache_toggle(self) -> bool:
        # According to situation, if it is the default/contextual user storage or an extra mounted one:
        #  - default/contextual => no need for cache
        #  - extra => interesting to have the cache
        return self.force_cache or not self.default

    def get_access_permission(self) -> str:
        # According to situation, if it is the default/contextual user storage or an extra mounted one:
        #  - default/contextual => user has RW access on its own user storage
        #  - extra => RO by default, RW only if defined
        return ACCESS_PERMISSION_RWD if self.default or self.write_permission else ACCESS_PERMISSION_RO

    def build_storage_prefix(self) -> str:
        # No prefix for this type of storage.
        return ''

    def build_mount_path_relative_to_home_dir(self) -> str:
        # Checks if it is the default User storage, in which case it must be mounted as $HOME.
        if self.default:
            return _MOUNT_HOME_RELPATH

        return _MOUNT_EXTRA_USER_RELPATH_FORMAT.format(
            activity_name=self.cleansed_activity_name(),
            user_id=self.user_id
        )


@dataclass
class StorageMetadataWithTopicBase(StorageMetadataWithActivity, ABC):
    # TheTopic ID and name.
    topic_id: int
    topic_name: str

    def cleansed_topic_name(self) -> str:
        return cleansed_str_value(self.topic_name)


@dataclass
# pylint: disable = too-many-instance-attributes
class GroupStorageMetadata(StorageMetadataWithTopicBase):
    # TheGroup metadata.
    group_id: int
    group_order: int
    group_nickname: str

    # Defines if write permission is allowed on this storage when NOT the default one (RO by default for extra group storage).
    write_permission: bool = False

    # Defines if Delete permission is allowed (false by default since 2023 January).
    # Requires write_permission True to be considered.
    delete_permission: bool = False

    # Toggle: defines if the mount point should contain group id (it allows to have a proper mount point name, in case there is no group, or only one group).
    mount_point_with_group_id: bool = True

    # Toggle: defines to use the group order (which is known by human) in the mount point, instead of the group id (which is only internal)
    use_group_order_instead_of_group_id: bool = False

    # Toggle: defines if this is a special organizer storage.
    special_organizer_group_storage: bool = False

    # Default toggle: if True, it corresponds to the default user/group/topic space (changes behaviour on mount point and/or permissions).
    default: bool = False

    def build_unique_storage_name(self) -> str:
        # Important: see this Gitlab Card to see before/after algorithm:
        #  

        return f'{self.cleansed_instance_id()}-{self.activity_id:05d}-{self.group_id:05d}-group-{CREATED_OBJECT_NAME_KEYWORD}'

    def build_mount_path_relative_to_home_dir(self) -> str:
        if self.special_organizer_group_storage:
            return _MOUNT_GROUP_SPECIAL_ORGANIZER_RELPATH_FORMAT.format(
                activity_name=self.cleansed_activity_name()
            )

        if self.mount_point_with_group_id:
            final_id = self.group_order if self.use_group_order_instead_of_group_id else self.group_id

            return _MOUNT_GROUP_RELPATH_FORMAT.format(
                activity_name=self.cleansed_activity_name(),
                topic_name=self.cleansed_topic_name(),
                group_id_or_order=final_id
            )

        return _MOUNT_GROUP_UNIQUE_RELPATH_FORMAT.format(
            activity_name=self.cleansed_activity_name(),
            topic_name=self.cleansed_topic_name()
        )

    def get_cache_toggle(self) -> bool:
        # In any case Cache is needed on Group storage.
        return True

    def get_access_permission(self) -> str:
        # According to situation, if it is the default/contextual group storage or an extra mounted one:
        #  - default/contextual => user has RW acces on its own group storage
        #  - extra => RO by default, RW only if defined
        #  - in any case, RW becomes RWD if delete_permission is True
        if self.default or self.write_permission:
            return ACCESS_PERMISSION_RWD if self.delete_permission else ACCESS_PERMISSION_RW

        return ACCESS_PERMISSION_RO

    def build_storage_prefix(self) -> str:
        return f'{self.activity_id:05d}/'


@dataclass
class ActivityStorageMetadata(StorageMetadataWithTopicBase):
    # Defines if write permission is allowed on this storage when NOT the default one (RO by default for extra group storage).
    write_permission: bool = False

    # Defines if Delete permission is allowed (false by default since 2023 January).
    # Requires write_permission True to be considered.
    delete_permission: bool = False

    # Defines if access should be given at root of the topic/fact/datasets storage (not recommended but for Ubeeko Team member)
    force_topic_storage_root: bool = False

    def build_unique_storage_name(self) -> str:
        return f'{self.cleansed_instance_id()}-{self.activity_id:05d}-activity-{CREATED_OBJECT_NAME_KEYWORD}'

    def build_mount_path_relative_to_home_dir(self) -> str:
        return _MOUNT_TOPIC_RELPATH_FORMAT.format(
            activity_name=self.cleansed_activity_name(),
            topic_name=self.cleansed_topic_name(),
            topic_id=self.topic_id
        )

    def get_cache_toggle(self) -> bool:
        # Important: cache allows sharing (the same Ceph) all the same files for all instances mounting this share.
        # So it is very important to use cache on Topic/fact/datasets storage for OVH to mount it only once for any count of AI Training instance(s) ...
        return True

    def get_access_permission(self) -> str:
        # According to situation:
        #  - if no write permission => RO
        #  - if ONLY write permission => RW
        #  - in write AND delete permission => RWD
        if not self.write_permission:
            return ACCESS_PERMISSION_RO

        return ACCESS_PERMISSION_RWD if self.delete_permission else ACCESS_PERMISSION_RW

    def build_storage_prefix(self) -> str:
        return f'{self.cleansed_instance_id()}/' + \
               f'{self.activity_id:05d}/{self.topic_id:05d}/public/' if not self.force_topic_storage_root else ''


# Backward compatibility, ActivityStorageMetadata was formerly named TopicStorageMetadata when is was related to topic
TopicStorageMetadata = ActivityStorageMetadata
