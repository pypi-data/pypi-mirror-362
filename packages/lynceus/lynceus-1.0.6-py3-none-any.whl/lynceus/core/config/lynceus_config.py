import configparser
import json
from collections.abc import Iterable, MutableMapping
from configparser import ConfigParser
from copy import deepcopy
from json import JSONDecodeError, JSONEncoder
from logging import Logger
from pathlib import Path

from lynceus.core.config import CONFIG_JSON_DUMP_KEY_END_KEYWORD
from lynceus.lynceus_exceptions import LynceusConfigError
from lynceus.utils import lookup_root_path


# pylint: disable=too-many-public-methods
class LynceusConfig(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys.

       IMPORTANT: when a key does not exist, it is automatically created to ease definition like ['X']['Y']['Z'] = 'XXX'
       BUT: it means the 'in' operator should NOT be used, because it will always return True, because the checked key will be created if not existing,
        for such situation, you should use the has_section() method.
       """

    UNDEFINED_VALUE: str = '$*_UNDEFINED_*$'

    def __init__(self, *args, **kwargs):
        self.__store = {}
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        # Creates automatically sub dictionary if needed.
        if LynceusConfig._keytransform(key) not in self.__store:
            self.__store[LynceusConfig._keytransform(key)] = {}

        return self.__store[LynceusConfig._keytransform(key)]

    def __setitem__(self, key, value):
        self.__store[LynceusConfig._keytransform(key)] = LynceusConfig._valuetransform(value)

    def __delitem__(self, key):
        del self.__store[LynceusConfig._keytransform(key)]

    def __iter__(self):
        return iter(self.__store)

    def __len__(self):
        return len(self.__store)

    @staticmethod
    def _keytransform(key):
        return key

    @staticmethod
    def _valuetransform(value):
        if isinstance(value, LynceusConfig):
            # pylint: disable=protected-access
            return value.__store

        return value

    def copy(self):
        lynceus_config_copy: LynceusConfig = LynceusConfig()
        # pylint: disable=protected-access,unused-private-member
        lynceus_config_copy.__store = deepcopy(self.__store)
        return lynceus_config_copy

    def as_dict(self):
        return deepcopy(self.__store)

    @staticmethod
    def dump_config_parser(config_parser: ConfigParser):
        result: str = ''
        for config_section in config_parser.sections():
            result += f'[{config_section}]\n'
            for key, value in config_parser.items(config_section):
                result += f'\t{key}={value}\n'
        return result

    def get_config(self, section: str, key: str, *, default: object = UNDEFINED_VALUE):
        try:
            return self[section][key]
        except KeyError as error:
            # Safe-guard: raise an error if configuration not found and no default specified.
            if default == self.UNDEFINED_VALUE:
                raise LynceusConfigError(f'Configuration [\'{section}\'][\'{key}\'] does not exist in your configuration.') from error
            return default

    def check_config_exists(self, section: str, key: str, *, transform_func=None):
        """
        Returns True if the configuration option with specified Key under specified section exists, False otherwise.
        If the value exists, system executes the optional func if specified, on the value (can be a cast, or any process function);
        caller need to manage potential exception during this execution.

        :param section:
        :param key:
        :param transform_func: (optional) **value** transformation function (can be a cast, or any process function)
        :return:
        """
        value = self.get_config(section, key, default=None)
        if value is None:
            return False

        # Checks if there is a trasnformation to apply.
        if transform_func:
            # Transforms (and registers) the value for further usage.
            self[section][key] = transform_func(value)

        # Returns the config option exists.
        return True

    @staticmethod
    def to_bool(value: str | None) -> bool | None:
        if value is None:
            return None
        return value in ['1', 'True', True]

    def is_bool_config_enabled(self, section: str, key: str, *, default: bool = False):
        return LynceusConfig.to_bool(self.get_config(section=section, key=key, default=default))

    def get_config_as_dict(self, section: str, key: str):
        # TODO: enhance it to work from API version which will be a string ...
        return self.get_config(section=section, key=key)

    def has_section(self, section: str):
        # Important: we must check the specified section on a list of keys, and not on the result of keys(), otherwise tha automatic
        #  key addition will be performed in __getitem__() method, and this method will always answer True.
        return section in list(self.keys())

    @staticmethod
    def __cleanse_value(value: str):
        return value if not isinstance(value, str) else str(value).strip("'").strip('"')

    @staticmethod
    # pylint: disable=too-many-branches
    def recursive_merge(dict1: dict | MutableMapping, dict2: dict | MutableMapping, *,
                        override_section: bool = False, override_value: bool = False, key_transform_func=None):
        """
        Merges all data from specified dict2, to the specified dict1, without removing/overriding any existing value, when possible.

        :param dict1: (aka destination dictionary)
        :param dict2: (aka source dictionary)
        :param override_section: overrides existing section (section=dict/mapping), or merges all existing key, value pairs of existing section (default)
        :param override_value: overrides existing value (value=all type which is not a section) or raises an exception (default)
        :param key_transform_func: optional **key** transformation function (e.g. useful to merge project template LynceusMetadata configuration in the project to score with
                    updated key, to state they belong to the template and not the project itself).

        For instance (very simplified):
        [General]                           Top level **section**
        logger.console.enable=True              simple key=value

        
        

        [MyKey2]                            Top level **section**
            [MyInnerKey]                        Second level **section**
                MyLeafKey=MyValue                   simple key=value
        """
        for key, value in dict2.items():
            # Checks if the corresponding key already exists in destination dict.
            # Important: do NOT use the in operator if first argument is a LynceusConfig, to avoid automatic creation of section here.
            if (isinstance(dict1, LynceusConfig) and not dict1.has_section(key)) or key not in dict1:
                dict1[key] = value
                continue

            # Checks if existing destination is iterable but NOT a map/mapping.
            if isinstance(dict1[key], Iterable) and not isinstance(dict1[key], (dict, MutableMapping, str)):
                # Checks if "new" value is iterable
                # N.B.: If it is NOT the case, it will be managed as a no map-like one with further instructions.
                if isinstance(value, Iterable) and not isinstance(value, str):
                    # Adapts merge according to concrete type.
                    if isinstance(dict1[key], list):
                        dict1[key].extend(value)
                    elif isinstance(dict1[key], set):
                        dict1[key] |= set(value)
                    else:
                        raise NotImplementedError(f'Recursive merge is not implemented for config option of type {type(dict1[key])=}.')
                    continue

            # Checks if existing destination is a map-like.
            if not isinstance(dict1[key], (dict, MutableMapping)):
                # Transforms the leaf key if requested.
                if key_transform_func:
                    key = key_transform_func(key)

                # Checks if override_value is allowed.
                if override_value:
                    dict1[key] = value
                    continue

                # Checks if it is not already the same value.
                if dict1[key] != value:
                    raise LynceusConfigError(f'Merge of "({key}, {value})" pair would override existing "({key}, {dict1[key]})" pair, whose value is NOT a dictionary/mapping.')

                continue

            # Overrides section if requested.
            if override_section:
                dict1[key] = value
                continue

            # Checks if source value is a map/mapping, otherwise.
            if isinstance(value, (dict, MutableMapping)):
                # Calls recursively this method on them.
                LynceusConfig.recursive_merge(dict1[key], value, override_value=override_value, override_section=override_section, key_transform_func=key_transform_func)
                continue

            # Updates the destination with the current pair.
            dict1[key].update({key: value})

    def merge(self, config_map: dict[str, any], *,
              set_only_as_default_if_not_exist: bool = False, override_section: bool = False, override_value: bool = False, key_transform_func=None):
        """
        Merges specified dict into this LynceusConfig instance.
        If set_only_as_default_if_not_exist is False (default), all existing inner dict-like values will be merged with new
         (key; value) pair if already exists, otherwise, the new values will only be considred as
         default value, and will only be set, if corresponding key does not already exists.

        :param config_map: the config map to merge into this instance
        :param set_only_as_default_if_not_exist: False (default) if existing value must be merged, True to
         only set value(s) if the corresponding key(s) do(es) not already exist (thus NOT overriding existing (key,value) pairs).
        :param override_section: overrides existing section (section=dict/mapping), or merges all existing key, value pairs of existing section (default)
        :param override_value: overrides existing value (value=all type which is not a section) or raises an exception (default)
        :param key_transform_func: optional **key** transformation function (e.g. useful to merge project template LynceusMetadata configuration in the project to score with
                    updated key, to state they belong to the template and not the project itself).
        """

        if not isinstance(self, LynceusConfig):
            raise LynceusConfigError(f'Self should be LynceusConfig, but is {type(self)}')

        # Processes automatically specified config_map to manage optional json dump options.
        config_map = LynceusConfig.load_json_params_from_lynceus_config(config_map).as_dict()

        if set_only_as_default_if_not_exist:
            if key_transform_func:
                raise NotImplementedError('key_transform_func option can not be used with set_only_as_default_if_not_exist option while merging config map.')

            # Uses the Python 3.9 ability to update Dictionary (considering existing values as the
            #  precedence ones).
            # TODO: it may be needed to iterate on each (key, value) pairs and recursively execute the | operator on them if value is dict-like instance ...
            self.__store = config_map | self.__store
            return

        # In this version, we need to merge everything, keeping existing inner (key; value) pairs.
        LynceusConfig.recursive_merge(self, config_map, override_section=override_section, override_value=override_value, key_transform_func=key_transform_func)

    def merge_from_lynceus_config(self, lynceus_config, *, override_section: bool = False, override_value: bool = False):
        # pylint: disable=protected-access
        self.merge(lynceus_config.__store, override_section=override_section, override_value=override_value)

    def merge_from_config_parser(self, config_parser: ConfigParser, *, override_section: bool = False, key_transform_func=None):
        """
        Merges configuration coming from specified configParser.

        :param config_parser:
        :param override_section: if True, resets all inner (key; value) pairs of existing section (e.g. top level key) in both this instance, and specified configParse,
                    merge everything otherwise (Default: False)
        :param key_transform_func: optional **key** transformation function (e.g. useful to merge project template LynceusMetadata configuration in the project to score with
                    updated key, to state they belong to the template and not the project itself).
        """
        # Merges each config parser section, as a dictionary, in this instance of Lynceus config.
        config_parser_to_dict = {config_section: {key: self.__cleanse_value(value) for key, value in config_parser.items(config_section)}
                                 for config_section in config_parser.sections()}
        self.merge(config_parser_to_dict, override_section=override_section, override_value=True, key_transform_func=key_transform_func)

    def lookup_configuration_file_and_update_from_it(self, config_file_name: str, *,
                                                     must_exist: bool = True,
                                                     root_path: Path = Path().resolve(),
                                                     logger: Logger | None = None,
                                                     **kwargs):
        try:
            # Retrieves the complete path of the configuration file, if exists.
            config_file_path = lookup_root_path(config_file_name, root_path=root_path) / Path(config_file_name)

            # Merges it in this instance.
            self.update_from_configuration_file(config_file_path, **kwargs)

            if logger:
                logger.info(f'Successfully load and merge configuration options from file "{config_file_name}".')
        except FileNotFoundError:
            # Raises FileNotFoundError only if configuration file should exist.
            if must_exist:
                raise

            if logger:
                logger.info(f'Configuration file "{config_file_name}" does not exist, so it will not be loaded (nor an error because {must_exist=}).')

    def update_from_configuration_file(self, file_path: Path, *,
                                       override_section: bool = False, key_transform_func=None):
        """
        Merges configuration coming from configuration file whose path is specified.

        :param file_path: path of the configuration file.
        :param override_section: if True, resets all inner (key; value) pairs of existing section (e.g. top level key) in both this instance, and specified configParse,
                    merge everything otherwise (Default: False).
        :param key_transform_func: optional **key** transformation function (e.g. useful to merge project template LynceusMetadata configuration in the project to score with
                    updated key, to state they belong to the template and not the project itself).
        """
        if not file_path.exists():
            raise FileNotFoundError(f'Specified "{file_path}" configuration file path does not exist.')

        # Reads configuration file.
        config_parser: configparser.ConfigParser = configparser.RawConfigParser()
        config_parser.read(str(file_path), encoding='utf8')

        # Merges it into this instance.
        self.merge_from_config_parser(config_parser, override_section=override_section, key_transform_func=key_transform_func)

    @staticmethod
    def format_config(config) -> dict[str, str]:
        def obfuscator(key, value):
            return '<secret>' if ('secret' in key or 'password' in key or 'pwd' in key or 'token' in key) else value

        return {key: obfuscator(key, value) if not isinstance(value, dict) else LynceusConfig.format_config(value)
                for key, value in dict(config).items()}

    @staticmethod
    def format_dict_to_string(dict_to_convert: MutableMapping, indentation_level: int = 0) -> str:
        return '\n'.join('\t' * indentation_level + f'{key}={str(value)}'
                         if not isinstance(value, dict) and not isinstance(value, LynceusConfig)
                         else '\t' * indentation_level + f'[{key}]\n' + LynceusConfig.format_dict_to_string(value, indentation_level + 1)
                         for key, value in dict_to_convert.items())

    def dump_for_config_file(self) -> str:
        return LynceusConfig.dump_to_config_str(self.__store)

    @staticmethod
    def dump_to_config_str(value) -> str:
        return json.dumps(value, cls=LynceusConfigJSONEncoder)

    @staticmethod
    def load_from_config_str(lynceus_config_dump: str | dict[str, any]):
        # TODO: may be better to instantiate an empty LynceusConfig, and use merge method here too.
        try:
            loaded_collection = json.loads(lynceus_config_dump)
        except JSONDecodeError as exc:
            # pylint: disable=raise-missing-from
            raise LynceusConfigError(f'Unable to JSON load config from specified string: "{lynceus_config_dump}".', from_exception=exc)

        if isinstance(loaded_collection, dict):
            return LynceusConfig(loaded_collection)

        return loaded_collection

    @staticmethod
    def load_json_params_from_lynceus_config(config_map: dict[str, any]):
        # Safe-guard: ensures specified parameter is a dict.
        if not isinstance(config_map, dict):
            raise LynceusConfigError(f'Specified parameter {config_map=} should be a dict ({type(config_map)} actually.')

        # Loads the specified config (e.g. custom user Project Profile metadata, jobs overriding/configuration options):
        #  - if key ends with the special json keyword, loads it
        #  - otherwise keep the key, value metadata pair unchanged
        loaded_lynceus_config: LynceusConfig = LynceusConfig()
        for config_param_with_json_key in list(config_map):
            # Checks if it is a json dump metadata.
            config_param_with_json_key_name: str = str(config_param_with_json_key)
            if not config_param_with_json_key_name.endswith(CONFIG_JSON_DUMP_KEY_END_KEYWORD):
                # It is NOT a json dump.

                # Checks if the value is a complex one.
                if isinstance(config_map[config_param_with_json_key_name], (dict, MutableMapping)):
                    # Calls recursively this method on the complex value.
                    loaded_lynceus_config[config_param_with_json_key_name].update(LynceusConfig.load_json_params_from_lynceus_config(config_map[config_param_with_json_key_name]).as_dict())
                else:
                    # Registers this single value.
                    LynceusConfig.recursive_merge(loaded_lynceus_config, {config_param_with_json_key_name: config_map[config_param_with_json_key_name]})

                continue

            # Loads the json value, and merges it recursively.
            loaded_metadata_key = config_param_with_json_key_name.removesuffix(CONFIG_JSON_DUMP_KEY_END_KEYWORD)
            value_dump = config_map[config_param_with_json_key]
            LynceusConfig.recursive_merge(loaded_lynceus_config, {loaded_metadata_key: LynceusConfig.load_from_config_str(value_dump)})

        return loaded_lynceus_config

    def save_partial_to_config_file(self, *, section_key_map: list[tuple], file_path: Path,
                                    key_transform_func=None,
                                    logger: Logger | None = None, log_prefix: str | None = ''):
        """
        Saves a copy of specified (section, key) tuple list, to file whose path is specified.

        :param section_key_map: a list of (section, key) tuple of configuration option to save (there is no error if any does not exist).
        :param file_path:
        :param key_transform_func: optional **key** transformation function (e.g. useful to merge project template LynceusMetadata configuration in the project to score with
                                    updated key, to state they belong to the template and not the project itself).
        :param logger:
        :param log_prefix:
        """
        config_parser: ConfigParser = ConfigParser()
        not_existing_value: str = 'no/th/ing'

        # Defines the metadata lynceus file, from complete configuration file, if defined.
        for metadata_option in section_key_map:
            section: str = metadata_option[0]
            key: str = metadata_option[1]

            # Attempts to retrive the value.
            value = self.get_config(section, key, default=not_existing_value)
            if value == not_existing_value:
                continue

            # Ensures section exists.
            if not config_parser.has_section(section):
                config_parser.add_section(section)

            # Transforms key if func is specified (useful to save project template config options, while processing the project to score).
            if key_transform_func:
                key = key_transform_func(key)

            # Registers it.
            if isinstance(value, Path):
                # - Path are saved as a string (not as a json dump, which is not loadable).
                value = str(value)
            elif not isinstance(value, str):
                # - all other type, but string, are saved as Json dump.
                key += CONFIG_JSON_DUMP_KEY_END_KEYWORD
                value = self.dump_to_config_str(value)
            #     - registers it inside config_parser.
            config_parser.set(section, key, value)

        if not config_parser.sections():
            logger.info(f'{log_prefix} no configuration option found to create Lynceus metadata file content among "{section_key_map}"')
            return

        if logger:
            logger.debug(f'{log_prefix} created Lynceus metadata file content:\n{LynceusConfig.dump_config_parser(config_parser)}')

        with open(file_path, 'w', encoding='utf8') as file:
            config_parser.write(file)

        if logger:
            logger.debug(f'{log_prefix} successfully written Lynceus metadata to file "{file_path}".')

    def is_empty(self):
        return len(self.__store) == 0

    def __repr__(self):
        return str(LynceusConfig.format_config(self))

    def __str__(self):
        return LynceusConfig.format_dict_to_string(LynceusConfig.format_config(self))

    def __or__(self, other):
        # Implements Python 3.9+ dict | operator allowing mixing between LynceusConfig and dict.
        return self.__store | other


class LynceusConfigJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, LynceusConfig):
            return dict(o)

        if isinstance(o, set):
            return list(o)

        if isinstance(o, Path):
            return str(o)

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)
