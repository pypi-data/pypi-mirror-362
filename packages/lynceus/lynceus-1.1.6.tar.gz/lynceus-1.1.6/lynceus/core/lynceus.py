import configparser
import logging.config
import logging.handlers
from logging import Logger
from pathlib import Path

from lynceus.core.config import CONFIG_GENERAL_KEY
from lynceus.core.config.lynceus_config import LynceusConfig
from lynceus.lynceus_exceptions import LynceusConfigError
from lynceus.utils import format_exception_human_readable, lookup_root_path


class LynceusSession:
    DEFAULT_SALT: str = 'lynceus'

    # Additional even more verbose than DEBUG log level.
    TRACE = 5

    __internal_key_preventing_external_usage_of_init = object()

    __REGISTERED_SESSIONS: dict = {}

    def __init__(self, *,
                 salt: str = DEFAULT_SALT,
                 root_logger_name: str = 'Lynceus',
                 load_core_default_config: bool = True,
                 overridden_root_logger_level: str | None = None,
                 _creation_key=None):
        """

        Creates a new Lynceus Session.

        Lynceus client must use :py:meth:`~lynceus.core.lynceus.LynceusSession.get_session` method only (it should NEVER call this constructor directly).

        :param salt: the salt used to identify with unicity this session.
        :param root_logger_name: the name of the root logger (will be used as prefix for all logger requested with :py:meth:`~lynceus.core.lynceus.LynceusSession.get_logger` method).
        :param load_core_default_config: toggle defining if Lynceus default configuration file must be loaded too (strongly recommended).
        :param overridden_root_logger_level: optional root logger level overridding; which can be interesting when used via a tool/script whose CLI options allow to force logging
                (i.e. --quiet, --debug ...)
        :param _creation_key: internal creation key (should NEVER be directly specified by external caller), preventing Lynceus client to call this method directly.
        """
        # Safe-guard: prevents direct call to this method.
        if _creation_key != LynceusSession.__internal_key_preventing_external_usage_of_init:
            raise RuntimeError(f'You should always use LynceusSession.get_session() method when requesting a LynceusSession ({salt=}).')

        # Initializes internal Lynceus config.
        self.__config = LynceusConfig()
        self.__root_logger_name = root_logger_name

        # Loads configuration file(s):
        #  - first the default config according to load_core_default_config toggle
        #  - then the default and user config corresponding to specify salt, if not the default one
        loaded_config_files = self.__load_configuration(salt, load_core_default_config=load_core_default_config)

        # Additional even more verbose than DEBUG log level.
        logging.TRACE = LynceusSession.TRACE
        logging.addLevelName(LynceusSession.TRACE, 'TRACE')

        # Setups default/root Lynceus logger.
        self.__logger = self.get_logger()
        root_level: int = logging.getLevelName(overridden_root_logger_level or self.get_config(CONFIG_GENERAL_KEY, 'logger.root.level', default='INFO'))
        self.__logger.setLevel(root_level)

        # Informs now that Logger is initialized.
        self.__logger.info(f'This is the loading information of looked up configuration files (Format=<Path: isLoaded?>) "{loaded_config_files}".')

    @staticmethod
    # pylint: disable=protected-access
    def get_session(*,
                    salt: str = DEFAULT_SALT,
                    registration_key: dict[str, str] | None = None,
                    root_logger_name: str = 'Lynceus',
                    load_core_default_config: bool = True,
                    overridden_root_logger_level: str | None = None):
        # Safe-guard: a registration key is highly recommended if not an internal session (which would be the case with salt == DEFAULT_SALT).
        if registration_key is None:
            if salt != LynceusSession.DEFAULT_SALT:
                raise LynceusConfigError('It is mandatory to provide your own registration_key when getting a session.' +
                                         f' System will automatically consider it as {registration_key}, but you may not be able to retrieve your session.' +
                                         ' And it may lead to memory leak.')
            registration_key = {'default': salt}

        # Turns the registration_key to an hashable version.
        if registration_key is not None:
            registration_key = frozenset(registration_key.items())

        # Creates and registers the session if needed.
        if registration_key in LynceusSession.__REGISTERED_SESSIONS:
            session: LynceusSession = LynceusSession.__REGISTERED_SESSIONS[registration_key]
            session.__logger.debug(f'Successfully retrieved cached Session for registration key "{registration_key}": {session}.')
        else:
            session: LynceusSession = LynceusSession(salt=salt, root_logger_name=root_logger_name,
                                                     load_core_default_config=load_core_default_config,
                                                     overridden_root_logger_level=overridden_root_logger_level,
                                                     _creation_key=LynceusSession.__internal_key_preventing_external_usage_of_init)

            LynceusSession.__REGISTERED_SESSIONS[registration_key] = session
            session.__logger.debug(f'Successfully registered new Session (new total count={len(LynceusSession.__REGISTERED_SESSIONS)})'
                                   f' for registration key "{registration_key}": {session}.'
                                   f' This is its loaded configuration (salt={salt}):\n' +
                                   f'{LynceusConfig.format_dict_to_string(LynceusConfig.format_config(session.__config), indentation_level=1)}')

        # TODO: implement another method allowing to free a specific registered session
        # TODO: turn LynceusSession as a Context, allowing usage with the 'with' keyword to automatic free the session once used

        # Returns the Lynceus session.
        return session

    def __load_configuration(self, salt: str, load_core_default_config: bool) -> dict[Path, bool]:
        # Defines the potential configuration file to load.
        config_file_meta_list = []
        if load_core_default_config:
            # Adds the Lynceus default configuration file as requested.
            config_file_meta_list.append({'config_path': f'misc/{self.DEFAULT_SALT}.default.conf', 'root_path': Path(__file__).parent})

        # Adds default configuration file corresponding to specified salt, if not the default one.
        if salt != self.DEFAULT_SALT:
            config_file_meta_list.append({'config_path': f'misc/{salt}.default.conf'})

        # Adds user configuration file corresponding to specified salt.
        config_file_meta_list.append({'config_path': f'{salt}.conf'})

        # Looks up for configuration file(s), starting with a "default" one, and then optional user one.
        loaded_config_files: dict[Path, bool] = {}
        for config_file_meta in config_file_meta_list:
            conf_file_name = config_file_meta['config_path']
            conf_file_root_path = config_file_meta.get('root_path', Path().resolve())

            loaded: bool = False
            relative_file: Path = Path(conf_file_name)
            try:
                full_path: Path = lookup_root_path(relative_file, root_path=conf_file_root_path) / relative_file

                # Merges it in internal Lynceus config.
                additional_config: configparser.ConfigParser = self.__config.update_from_configuration_file(full_path)

                # Updates/Configures fine-tuned logger, if any in this (first or) additional configuration file.
                # N.B.: in ideal world, could be interesting to extract logger config from all configuration file(s) merged, and
                #  create a fake fileConfig in memory, to logging.config.fileConfig once for all, after all loading.
                # Without that, handlers and formatters must be redefined each time, in each configuration file definined fine-tuned logger configuration.
                if 'loggers' in additional_config.sections():
                    self.get_logger('internal').debug(f'Requesting fine-tuned logger configuration with configuration coming from {conf_file_name}.')
                    # Cf. https://docs.python.org/3.10/library/logging.config.html#logging.config.fileConfig
                    logging.config.fileConfig(full_path, disable_existing_loggers=False, encoding='utf-8')

                loaded = True
            except FileNotFoundError as exc:
                # Since recent version, there is no more mandatory configuration file to have, and several files can be loaded.
                # N.B.: it is valid, there is no logger yet here, so using print ...
                self.get_logger('internal').debug(f'WARNING: Unable to load "{conf_file_name}" configuration file,'
                                                  f' from "{conf_file_root_path}"'
                                                  f' (it is OK, because this configuration file is NOT mandatory) =>'
                                                  f' {format_exception_human_readable(exc, quote_message=True)}')

            # Registers configuration file loading information.
            loaded_config_files[relative_file] = loaded

        # Returns configuration file loading mapping, for information.
        return loaded_config_files

    def has_config_section(self, section: str):
        return self.__config.has_section(section)

    def get_config(self, section: str, key: str, *, default: object = LynceusConfig.UNDEFINED_VALUE):
        return self.__config.get_config(section, key, default=default)

    def is_bool_config_enabled(self, section: str, key: str):
        return self.__config.is_bool_config_enabled(section=section, key=key)

    def get_config_section(self, section: str):
        return self.__config[section]

    def get_lynceus_config_copy(self) -> LynceusConfig:
        """
        Returns a copy of the internal Lynceus config, can be very interesting to get default config.
        :return: a copy of the internal Lynceus config, can be very interesting to get default config.
        """
        return self.__config.copy()

    def get_logger(self, name: str = None, *, parent_propagate: bool = True) -> Logger:
        complete_name: str = f'{self.__root_logger_name}.{name}' if name else self.__root_logger_name
        logger: Logger = logging.getLogger(complete_name)
        if logger.parent:
            logger.parent.propagate = parent_propagate

        return logger
