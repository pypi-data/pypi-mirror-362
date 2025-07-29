import inspect
from pathlib import Path

from lynceus.core.config import (CONFIG_GENERAL_KEY,
                                 CONFIG_PROJECT_DYNAMIC_STORAGE_MANDATORY_PARAM_MAP,
                                 CONFIG_STORAGE_DYNAMIC_TYPE,
                                 CONFIG_STORAGE_IS_DYNAMIC,
                                 CONFIG_STORAGE_REMOTE_TYPE)
from lynceus.core.config.lynceus_config import LynceusConfig
from lynceus.core.exchange.lynceus_exchange import LynceusExchange
from lynceus.core.lynceus import LynceusSession
from lynceus.core.lynceus_client import LynceusClientClass
from lynceus.files.lynceus_file import LynceusFile, _LocalLynceusFile, _RemoteS3LynceusFile
from lynceus.files.remote.s3 import S3Utils
from lynceus.files.storage_metadata import (ActivityStorageMetadata, GroupStorageMetadata,
                                            FileStorageMetadata,
                                            OrganizationStorageMetadata,
                                            ResourceConsumptionStorageMetadata,
                                            StorageMetadataBase, UserStorageMetadata)
from lynceus.lynceus_exceptions import LynceusFileError
from lynceus.utils import lookup_root_path


# pylint: disable=too-many-instance-attributes
class LynceusFileFactory(LynceusClientClass):
    """
    LynceusFileFactory is useful to create instance of Local or Remote according to various configuration provided once
    for all in Factory constructor.
    By default, it is configured to read and write parquet files, but it can be configured to manage any kind of file.
    """

    REMOTE_STORAGE_TYPE_S3: str = 's3'
    REMOTE_STORAGE_TYPE_SUPPORTED_LIST: set[str] = {REMOTE_STORAGE_TYPE_S3}

    # Defines supported dynamic remote storage.
    REMOTE_DYNAMIC_TYPE_FILE: str = 'files'
    REMOTE_DYNAMIC_TYPE_ORGANIZATION: str = 'organization'
    REMOTE_DYNAMIC_TYPE_ACTIVITY: str = 'activity'
    REMOTE_DYNAMIC_TYPE_USER: str = 'user'
    REMOTE_DYNAMIC_TYPE_GROUP: str = 'group'
    REMOTE_DYNAMIC_TYPE_RESOURCES_STATS: str = 'resources_stats'

    # Defines once for all classes, and awaited parameters for each type of supported dynamic remote storage.
    REMOTE_DYNAMIC_TYPE_CLASS_MAP: dict[str, StorageMetadataBase] = {
        REMOTE_DYNAMIC_TYPE_FILE:
            (FileStorageMetadata, set(inspect.getfullargspec(FileStorageMetadata).args) - {'self'}),
        REMOTE_DYNAMIC_TYPE_ORGANIZATION:
            (OrganizationStorageMetadata, set(inspect.getfullargspec(OrganizationStorageMetadata).args) - {'self'}),
        REMOTE_DYNAMIC_TYPE_ACTIVITY:
            (ActivityStorageMetadata, set(inspect.getfullargspec(ActivityStorageMetadata).args) - {'self'}),
        REMOTE_DYNAMIC_TYPE_USER:
            (UserStorageMetadata, set(inspect.getfullargspec(UserStorageMetadata).args) - {'self'}),
        REMOTE_DYNAMIC_TYPE_GROUP:
            (GroupStorageMetadata, set(inspect.getfullargspec(GroupStorageMetadata).args) - {'self'}),
        REMOTE_DYNAMIC_TYPE_RESOURCES_STATS:
            (ResourceConsumptionStorageMetadata, set(inspect.getfullargspec(ResourceConsumptionStorageMetadata).args) - {'self'}),
    }

    REMOTE_DYNAMIC_TYPE_SUPPORTED_LIST: set[str] = set(REMOTE_DYNAMIC_TYPE_CLASS_MAP.keys())

    # pylint: disable=too-many-branches,too-many-statements
    def __init__(self, *, lynceus_session: LynceusSession, lynceus_exchange: LynceusExchange | None,
                 lynceus_config: LynceusConfig = None,
                 env: str = None, env_suffix: str = None,
                 remote_config_section: str = None, remote_config_key: str = None,
                 remote_mode_forced_by_cli: bool = True, remote_mode_automatic_activation: bool = False,
                 source_path_format: str = '{target}/{env}/parquet', source_mode: bool = False,
                 dest_path_format: str = '{dest_file_name}/{source_name}.parquet', dest_path_kwargs: dict[str, str] = None):
        """
        Initializes Lynceus file Factory generating File allowing local or remote management,
         according to remote mode toggle (depending on specified argument and optional overriding configuration).
        :param lynceus_config: configuration to use (if not specified, configuration of specified lynceus session is used).
        :param env: name of the environment which will be used as parent directory of parquet files (for write access).
        :param remote_mode_forced_by_cli: (forced by CLI) True to read remotely, False to read locally (default).
        :param dest_path_format: the format used to generate destination path.
        :param dest_path_kwargs: the parameters used to generate destination path.
        :param remote_mode_automatic_activation: automatic activation requested.
        :param remote_config_section: config section containing remote storage configuration.
        :param remote_config_key: config key, in General section, giving config section (needed only if remote_config_section is not defined).

        remote_mode explanation:
         - by default destination files are read and write locally,
         - if Host is our Data Factory,
            or if NB_USER environment variable is defined to jovyan, indicating system is launched with Docker image,
            remote_mode automatic activation is requested
         - but the **override_to_local_mode** configuration (in configuration file), allow ignoring automatic activation request
         - in any case, the remote_mode_forced_by_cli toggle (e.g. set by a --remote-mode CLI option) can be used to force remote mode
            (it will be False here, BUT 100% of request will use the override_remote_mode method parameter).
         => this system could be lightened, but it is risky to do that while keeping backward compatibility.
        """
        super().__init__(logger_name='file', lynceus_session=lynceus_session, lynceus_exchange=lynceus_exchange)

        # Safe-guard:
        if not source_path_format:
            raise LynceusFileError('Source path format must be defined!')

        self.__env: str = env
        self.__remote_mode: bool = remote_mode_forced_by_cli
        self.__remote_mode_automatic_activation: bool = remote_mode_automatic_activation
        self.__local_mode_forced_by_config: bool = False
        self.__source_path_format: str = source_path_format
        self.__source_mode = source_mode
        self.__dest_path_format: str = dest_path_format
        self.__dest_path_kwargs: dict[str, str] = dest_path_kwargs or {}
        self.__previous_dest_path_kwargs = {}

        if not lynceus_config:
            lynceus_config = self._lynceus_session.get_lynceus_config_copy()

        # Loads remote configuration, and define some variable accordingly.
        self.__dynamic_container_name_params: dict[str, str] = {}
        if not remote_config_section and not remote_config_key:
            self._logger.warning('No remote configuration given at all, this file factory will only be able to create Local file.')
            self.__remote_config = None
            self.__with_dynamic_container_name: bool = False
        else:
            if not remote_config_section:
                remote_config_section = lynceus_config.get_config(CONFIG_GENERAL_KEY, remote_config_key)
            self.__remote_config = lynceus_config[remote_config_section]
            if not self.__remote_config:
                raise ValueError(f'There is no "{remote_config_section}" configuration in configuration file (are you sure you load the storage definition file ?).')

            self._logger.debug(f'According to "{remote_config_section}" configuration section, LynceusFileFactory will' +
                               f' consider remote configuration named "{remote_config_section}": "{LynceusConfig.format_config(self.__remote_config)}".')

            if self.__remote_config.get(CONFIG_STORAGE_REMOTE_TYPE) not in LynceusFileFactory.REMOTE_STORAGE_TYPE_SUPPORTED_LIST:
                raise NotImplementedError(f'Configured "{CONFIG_STORAGE_REMOTE_TYPE}={self.__remote_config.get(CONFIG_STORAGE_REMOTE_TYPE)}" is not supported.' +
                                          f' Supported values: {LynceusFileFactory.REMOTE_STORAGE_TYPE_SUPPORTED_LIST}')

            # Retrieves optional is_dynamic configuration option.
            self.__with_dynamic_container_name: bool = self.__remote_config.get(CONFIG_STORAGE_IS_DYNAMIC)
            self.__with_dynamic_container_type: str = self.__remote_config.get(CONFIG_STORAGE_DYNAMIC_TYPE,
                                                                               LynceusFileFactory.REMOTE_DYNAMIC_TYPE_GROUP)

            if self.__with_dynamic_container_type not in LynceusFileFactory.REMOTE_DYNAMIC_TYPE_SUPPORTED_LIST:
                raise NotImplementedError(f'Configured "{CONFIG_STORAGE_DYNAMIC_TYPE}={self.__with_dynamic_container_type}" is not supported.' +
                                          f' Supported values: {LynceusFileFactory.REMOTE_DYNAMIC_TYPE_SUPPORTED_LIST}')

            # Initializes some utilities.
            self.__s3utils = S3Utils(lynceus_session=lynceus_session, lynceus_exchange=lynceus_exchange, lynceus_s3_config=self.__remote_config)
            self.__s3utils.initialize()

            # Checks if local mode (against remote mode) is forced in configuration file.
            if 'override_to_local_mode' in self.__remote_config:
                if LynceusConfig.to_bool(self.__remote_config['override_to_local_mode']):
                    self.__local_mode_forced_by_config = True
                    # It is the case so defined the remote mode as False.
                    self.__remote_mode = False
                    self._logger.info(
                        f'According to "override_to_local_mode" configuration in "{remote_config_section}"' +
                        ' remote mode is overridden to "local" (it can only be overridden by CLI option).')
            else:
                # In any case, set the remote mode as the value of CLI **or** auto activation.
                self.__remote_mode |= remote_mode_automatic_activation
                self._logger.info(f'remote mode="{self.__remote_mode}" (forced by CLI option="{remote_mode_forced_by_cli}";' +
                                  f' automatic activation according to environment="{self.__remote_mode_automatic_activation}").')

            if 'override_environment' in self.__remote_config:
                self.__env = self.__remote_config['override_environment']
                self.__env = self.__define_complete_env(self.__env, env_suffix)
                self._logger.info(f'According to "override_environment" configuration in "{remote_config_section}"' +
                                  f' Environnment is overriden to "{self.__env}".')

            # Defines remote root path, once for all.
            self.__remote_root_path: Path | None = None
            if not self.__with_dynamic_container_name:
                self.__remote_root_path = self.__define_remote_root_path(self.__env)

        # Defines default environment if needed.
        if self.__env is None:
            self.__env = self.__define_complete_env('dev', env_suffix)
            self._logger.info(f'No environment defined in CLI or configuration, defined it to "{self.__env}".')

        # Defines local root path, once for all.
        self.__local_root_path: Path = self.__define_local_root_path(self.__env)

        # Defines string presentation of this LynceusFile Factory.
        self.__string_presentation = LynceusConfig.format_dict_to_string(LynceusConfig.format_config(
            self.get_context_info() |
            {
                'env': self.__env,
                'source_path_format': self.__source_path_format,
                'source_mode': self.__source_mode,
                'dest_path_format': self.__dest_path_format,
                'storage': self.__remote_config or 'Local only',
                'dynamic': self.__dynamic_container_name_params,
            }), indentation_level=2)

    @property
    def is_dynamic_remote(self):
        return self.__with_dynamic_container_name

    def __define_complete_env(self, env: str, env_suffix: str):
        # Checks if this factory is used as a source.
        if self.__source_mode:
            # It is the case, so suffix is NOT used here.
            return env

        # It is used as a target, so environment suffix must be taken care.
        return env if not env_suffix else f'{env}/{env_suffix}'

    def force_cache_refresh(self):
        if self.__remote_config:
            self.__s3utils.force_cache_refresh()

    def get_env(self) -> str:
        return self.__env

    def __build_relative_path_dir(self, target: str, env: str | None):
        return self.__source_path_format.format(**self.__dest_path_kwargs, target=target, env=env)

    def __define_local_root_path(self, env: str | None) -> Path:
        root_path: Path = lookup_root_path('lynceus/misc', root_path=Path(__file__).parent)
        return root_path / Path(self.__build_relative_path_dir('target', env))

    def update_dynamic_storage_params(self, params: dict[str, str | int]):
        self.__dynamic_container_name_params: dict[str, str | int] = params.copy()
        mandatory_params: set[str] = {param for param, is_mandatory in CONFIG_PROJECT_DYNAMIC_STORAGE_MANDATORY_PARAM_MAP.items() if is_mandatory}

        # Ensures there are all the mandatory params.
        if mandatory_params - set(self.__dynamic_container_name_params.keys()):
            raise LynceusFileError(f'Specified dynamic storage params ({set(self.__dynamic_container_name_params.keys())}),' +
                                   f' should contain at least all the awaited ones ({mandatory_params}).')

        # Adds mandatory option allowing to create GroupStorageMetadata instance.
        # Tricks: GroupStorageMetadata is used only for its build_unique_storage_name method,
        #  which does NOT need following parameters, but which are mandatory to create a new instance.
        self.__dynamic_container_name_params.update({
            'organization_name': 'notUsedHere',
            'activity_name': 'notUsedHere',
            'topic_id': -1,
            'topic_name': 'notUsedHere',
            'group_order': -1,
            'group_nickname': 'notUsedHere',
        })

    def __define_remote_container_name(self) -> str:
        # Checks if it is a static or dynamic storage.
        if not self.__with_dynamic_container_name:
            return self.__remote_config["bucket_name"]

        # Defines which StorageMetadata and params according to configuration.
        storage_metadata_class, awaited_params = LynceusFileFactory.REMOTE_DYNAMIC_TYPE_CLASS_MAP.get(self.__with_dynamic_container_type)

        # Creates the corresponding StorageMetadata, and requests the unique storage name building to be 100% sure
        #  it will be the exact same name used during creation, and during compute resources request.
        try:
            # Filters parameters to use to instantiate such StorageMetadata class.
            params = {key: value for key, value in self.__dynamic_container_name_params.items()
                      if key in awaited_params}

            dynamic_storage: StorageMetadataBase = storage_metadata_class(**params)
            return dynamic_storage.build_unique_storage_name()
        except TypeError as exc:
            raise LynceusFileError(f'Unable to define the name of the dynamic remote container "{self}".', exc) from exc

    def __define_remote_root_path(self, env: str | None) -> Path:
        relative_path_dir: str = self.__build_relative_path_dir(self.__define_remote_container_name(), env)

        return Path(f'{LynceusFile.S3_PATH_BEGIN}{relative_path_dir}/')

    def new_file(self, source_name: str | None, source_file_name: str, must_exist: bool = True,
                 override_env: str = None, override_remote_mode: bool = None,
                 create_sub_directories: bool = True, dest_path_format: str = None,
                 override_dest_path_kwargs: dict = None, specific_dest_file_name: str = None) -> LynceusFile:
        # Safe-guard: ensures source_file_name is defined to minimum.
        source_file_name = source_file_name or '/'

        # Defines destination file name, which is the same as the source file name by default.
        dest_file_name = specific_dest_file_name if specific_dest_file_name else source_file_name

        # Manages path kwargs overriding if needed.
        path_kwargs = override_dest_path_kwargs if override_dest_path_kwargs else self.__dest_path_kwargs

        # Special Hack (mainly needed for CustomerInfo auto merge system), using previous path kwargs if none is defined here.
        if not path_kwargs:
            path_kwargs = self.__previous_dest_path_kwargs
        else:
            # Registers path_kwargs for next potential iteration.
            self.__previous_dest_path_kwargs = path_kwargs

        # Formats the new file path.
        if not dest_path_format:
            dest_path_format = self.__dest_path_format

        try:
            new_file_path: str = dest_path_format.format(**path_kwargs, source_name=source_name, dest_file_name=dest_file_name)
        except KeyError:
            # Gives as much information as possible.
            self._logger.error(f'Unable to build the file path from format "{dest_path_format}" and arguments: "{source_name}", "{dest_file_name}", "{path_kwargs=}"')
            # Stops on error anyway.
            raise

        return self._do_new_file(new_file_path, must_exist, override_env,
                                 override_remote_mode, create_sub_directories=create_sub_directories)

    def new_env_directory(self, must_exist: bool = True, override_env: str = None,
                          override_remote_mode: bool = None) -> LynceusFile:
        return self._do_new_file('', must_exist, override_env, override_remote_mode, create_sub_directories=False)

    def _do_new_file(self, path: str, must_exist: bool = True,
                     override_env: str | None = None, override_remote_mode: bool = None,
                     create_sub_directories: bool = True) -> LynceusFile:
        if self.__remote_mode or override_remote_mode:
            root_path: Path = self.__remote_root_path if override_env is None and not self.__with_dynamic_container_name \
                else self.__define_remote_root_path(override_env)

            complete_path: Path = root_path

            # Important: concatenates path only if it exists and not '/'.
            if path and path != '/':
                complete_path /= Path(path)

            # Manages optional globbing if needed.
            if '*' in path:
                matching_files = self.__s3utils.list_remote_files(remote_root_path=_RemoteS3LynceusFile.get_raw_path_from_remote_path(root_path), recursive=True, pattern=path, detail=True)
                if not matching_files:
                    self._logger.warning(f'Unable to find any remote files while globbing with "{complete_path}". It will certainly lead to not found file.')
                else:
                    # Sorts by last modification date.
                    sorted_matching_files = sorted(matching_files.items(), key=lambda kv: kv[1]['LastModified'], reverse=True)
                    selected_file_path = sorted_matching_files[0][0]

                    complete_path = root_path / Path(selected_file_path)
        else:
            root_path: Path = self.__local_root_path if override_env is None and not self.__with_dynamic_container_name \
                else self.__define_local_root_path(override_env)

            complete_path: Path = root_path / Path(path)
            # TODO: implement globbing on local path, something like root_path.glob(pattern)

        return self.create_from_full_path(complete_path, must_exist=must_exist,
                                          override_remote_mode=override_remote_mode, create_sub_directories=create_sub_directories)

    def create_from_full_path(self, complete_path: Path, must_exist: bool = True,
                              override_remote_mode: bool = None, create_sub_directories: bool = True) -> LynceusFile:
        complete_path = Path(complete_path)
        if self.__remote_mode or override_remote_mode:
            new_lynceus_file: LynceusFile = _RemoteS3LynceusFile(complete_path, self._logger,
                                                                 self.__s3utils.get_s3filesystem(),
                                                                 self.__s3utils)

            # Forces cache refresh if corresponding file existence if False atm.
            # it can happen if the file has been created (from elsewhere) after creation of this Factory.
            if must_exist and not new_lynceus_file.exists(reason='check if S3fs cache must be refreshed'):
                self.__s3utils.force_cache_refresh(path=_RemoteS3LynceusFile.get_raw_path_from_remote_path(complete_path.parent))
        else:
            # Creates subdirectories if needed.
            if create_sub_directories:
                complete_path.parent.mkdir(parents=True, exist_ok=True)

            new_lynceus_file: LynceusFile = _LocalLynceusFile(complete_path, self._logger)

        # Safe-guard: ensures corresponding file exists.
        if must_exist and not new_lynceus_file.exists():
            raise LynceusFileError(f'Requested file "{new_lynceus_file}" does not exist.')

        return new_lynceus_file

    def get_parent_file(self, lynceus_file: LynceusFile, must_exist: bool = True,
                        override_remote_mode: bool = None, create_sub_directories: bool = True) -> LynceusFile:
        return self.create_from_full_path(lynceus_file.get_parent_path(), must_exist=must_exist,
                                          override_remote_mode=override_remote_mode,
                                          create_sub_directories=create_sub_directories)

    def get_context_info(self):
        return {
            'remote_mode (from CLI)': self.__remote_mode,
            'remote_mode (automatic)': self.__remote_mode_automatic_activation,
            'local_mode (from Config)': self.__local_mode_forced_by_config
        }

    def __str__(self):
        return self.__string_presentation
