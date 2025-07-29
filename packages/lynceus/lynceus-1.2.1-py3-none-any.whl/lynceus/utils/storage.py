from logging import Logger
from pathlib import Path

from lynceus.core.config import (CONFIG_PROJECT_DYNAMIC_STORAGE_MANDATORY_PARAM_MAP,
                                 CONFIG_PROJECT_KEY,
                                 CONFIG_PROJECT_ROOT_PATH_HOLDER,
                                 CONFIG_STORAGE_LOCAL)
from lynceus.core.config.lynceus_config import LynceusConfig
from lynceus.core.exchange.lynceus_exchange import LynceusExchange
from lynceus.core.lynceus import LynceusSession
from lynceus.files.file_factory import LynceusFileFactory
from lynceus.files.lynceus_file import LynceusFile
from lynceus.lynceus_exceptions import LynceusConfigError, LynceusFileError
from lynceus.utils import lookup_root_path


def create_storage_file_factory(*, name: str,
                                lynceus_session: LynceusSession,
                                lynceus_config: LynceusConfig,
                                logger: Logger,
                                log_prefix: str,
                                remote_config_section: str | None,
                                remote_mode_forced_by_cli: bool = True,
                                source_path_format: str = '{target}',
                                dest_path_format: str = '{dest_file_name}',
                                lynceus_exchange: LynceusExchange | None = None) -> LynceusFileFactory | None:
    # Safe-guard: ensure specified config_section exists in Lynceus configuration.
    if remote_config_section and not lynceus_config.has_section(remote_config_section):
        logger.warning(f'{log_prefix} unable to register storage "{name}", because configuration section "{remote_config_section}" does not exist. Fix your configuration.')
        return None

    # Creates a new Lynceus file factory corresponding to needs.
    return LynceusFileFactory(
        lynceus_session=lynceus_session,
        lynceus_config=lynceus_config,
        remote_config_section=remote_config_section,
        remote_mode_forced_by_cli=remote_mode_forced_by_cli,
        source_path_format=source_path_format,
        dest_path_format=dest_path_format,
        lynceus_exchange=lynceus_exchange,
    )


def extract_dynamic_remote_storage_params(lynceus_config: LynceusConfig) -> dict[str, str | int]:
    if not lynceus_config.has_section(CONFIG_PROJECT_KEY):
        raise LynceusConfigError(f'Unable to find [{CONFIG_PROJECT_KEY}] configuration section in specified configuration file.')

    dynamic_remote_storage_params = {}
    for param, is_mandatory in CONFIG_PROJECT_DYNAMIC_STORAGE_MANDATORY_PARAM_MAP.items():
        value = lynceus_config.get_config(CONFIG_PROJECT_KEY, param, default=None)
        if value is None:
            if is_mandatory:
                raise LynceusConfigError(f'Unable to find "{param}" option (mandatory for dynamic remote storage) inside' +
                                         f' [{CONFIG_PROJECT_KEY}] configuration section in specified configuration file.')
            continue

        # Checks the type of value, can be either:
        #  - string if coming from a static configuration file
        #  - int if coming from API, CLI or Tests
        if isinstance(value, str):
            value = value if not value.isnumeric() else int(value)

        dynamic_remote_storage_params[param] = value

    return dynamic_remote_storage_params


def get_lynceus_file_from_metadata(*,
                                   file_metadata: str,
                                   lynceus_config: LynceusConfig,
                                   logger: Logger,
                                   log_prefix: str,
                                   storage_file_factory_map: dict[str, LynceusFileFactory],
                                   locally_retrieved_repository_root_path: Path | None,
                                   must_exist: bool,
                                   overriden_root_path_if_local: Path = None) -> LynceusFile:
    # Extracts storage name and file path from metadata.
    storage_name, file_path = LynceusFile.extract_storage_and_path(file_metadata)
    dest_path_format: str | None = None
    override_dest_path_kwargs: dict[str, str] | None = None

    storage_file_factory: LynceusFileFactory = storage_file_factory_map.get(storage_name)
    if not storage_file_factory:
        raise LynceusConfigError(f'{log_prefix} file option ("{file_metadata}"), is hosted on remote storage "{storage_name}"' +
                                 ', which is not configured!' +
                                 f' Available/configured remote storages: {storage_file_factory_map}.')

    # Manages dynamic remote storage if needed.
    if storage_file_factory.is_dynamic_remote:
        # TODO: limitation is that ALL remote file coming from a dynamic remote, share the same parameters linked to the parent project.
        # Thus: atm it is NOT possible to have a reference file on a dynamic remote and the solution file on another dynamic remote, for the same project.
        try:
            dynamic_remote_storage_params: dict[str, str | int] = extract_dynamic_remote_storage_params(lynceus_config)
            storage_file_factory.update_dynamic_storage_params(dynamic_remote_storage_params)

            # Checks if the path must be formatted.
            if '{' in file_path:
                dest_path_format = str(file_path)
                override_dest_path_kwargs = dynamic_remote_storage_params

        except LynceusConfigError as exc:
            # pylint: disable=raise-missing-from
            raise LynceusFileError(f'Unable to prepare system to use dynamic remote storage "{storage_name}"', exc)

    # Manages Local file if needed:
    if storage_name == CONFIG_STORAGE_LOCAL:
        if overriden_root_path_if_local:
            file_path: str = str(lookup_root_path(file_path, remaining_iteration=4, root_path=overriden_root_path_if_local) / Path(file_path))
        else:
            #  - adds special CONFIG_PROJECT_ROOT_PATH_HOLDER keyword at beginning if relative path
            if CONFIG_PROJECT_ROOT_PATH_HOLDER not in file_path and not file_path.startswith('/'):
                file_path: str = CONFIG_PROJECT_ROOT_PATH_HOLDER + file_path

        #  - replaces CONFIG_PROJECT_ROOT_PATH_HOLDER keyword by retrieved repository root path
        if CONFIG_PROJECT_ROOT_PATH_HOLDER in file_path:
            if not locally_retrieved_repository_root_path:
                raise ValueError('Repository should have been locally retrieved for this request.')

            root_dir: str = str(locally_retrieved_repository_root_path)
            file_path: str = file_path.replace(CONFIG_PROJECT_ROOT_PATH_HOLDER, root_dir + '/')

    # Creates a LynceusFile instance.
    logger.debug(f'{log_prefix} creating LynceusFile ({file_path=}; {dest_path_format=}; {override_dest_path_kwargs=}) ...')
    lynceus_file: LynceusFile = storage_file_factory.new_file(source_name=None, source_file_name=file_path,
                                                              dest_path_format=dest_path_format,
                                                              override_dest_path_kwargs=override_dest_path_kwargs,
                                                              create_sub_directories=False,
                                                              must_exist=must_exist)

    return lynceus_file


def retrieve_remote_file_locally(*, lynceus_file: LynceusFile,
                                 logger: Logger,
                                 log_prefix: str,
                                 dest_dir_path: Path,
                                 extension_if_none: str | None = None) -> Path | None:
    # This method is useful in several situations, for instance:
    #  - scoring engine is unable to work with remote file ... retrieve the remote file locally first
    #  - third-party tool configuration file can be overriden and put on remote storage, so we retrieve them locally first
    if lynceus_file is None:
        return None

    if lynceus_file.is_local():
        return lynceus_file.path

    local_file_name: str = lynceus_file.get_name()
    if not lynceus_file.get_extension() and extension_if_none:
        local_file_name += extension_if_none

    local_path: Path = dest_dir_path / Path(local_file_name)
    lynceus_file.download_to(local_path)
    logger.debug(f'{log_prefix} saved {lynceus_file=} to {local_path=} to ease usage.')
    return local_path
