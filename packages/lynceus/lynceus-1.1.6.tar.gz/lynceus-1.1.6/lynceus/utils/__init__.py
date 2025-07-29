import random
import re
import time
import timeit
from collections.abc import Iterable
from contextlib import contextmanager
from datetime import datetime, timezone
from logging import Logger
from pathlib import Path
from string import ascii_letters, digits

from setuptools import find_packages

# Default allowed characters when cleansing string values (e.g. activity/topic name).
from lynceus.core.config import DATETIME_FORMAT, DATETIME_FORMAT_SHORT

ALLOWED_CHARACTERS = ascii_letters + digits + 'ÀÂÄÆÇÈÉÊËÎÏÔŒÙÛÜàâäæçèéêëîïôœùûü'


def cleansed_str_value(value: str, *,
                       to_lower_case: bool = True,
                       replacement_character: str = '_',
                       allowed_characters: str = ALLOWED_CHARACTERS):
    if to_lower_case:
        value = value.lower()
    return ''.join(char if char in allowed_characters else replacement_character for char in value.strip())


def concatenate_string_with_limit(begin: str, extra: str, *, limit: int, truncate_begin: bool = True):
    if len(begin) >= limit:
        return begin[:limit]

    remaining_limit: int = limit - len(begin)
    kept_extra: str = extra
    if len(extra) > remaining_limit:
        if truncate_begin:
            kept_extra = extra[-remaining_limit:]
        else:
            kept_extra = extra[0:remaining_limit]

    return begin + kept_extra


def exec_and_return_time(func, /, *args) -> float:
    """
    Utility method allowing to measure execution time of specified function, and arguments.
    This function allows to easily change implementation at any time.

    IMPORTANT: does NOT support async function.

    :param func:
    :param args:
    :return:
    """
    return timeit.timeit(lambda: func(*args), number=1)


@contextmanager
def time_catcher() -> float:
    start = time.time()
    cpu_start = time.process_time()
    yield lambda: f'{(time.process_time() - cpu_start):0.03f} CPU seconds, {(time.time() - start):0.03f} elapsed seconds'


def parse_string_to_datetime(datetime_str: str, *,
                             datetime_format: str = DATETIME_FORMAT,
                             datetime_format_short: str = DATETIME_FORMAT_SHORT,
                             override_timezone: timezone | None = timezone.utc) -> datetime:
    try:
        final_datetime = datetime.strptime(datetime_str, datetime_format)
    except ValueError:
        final_datetime = datetime.strptime(datetime_str, datetime_format_short)

    if override_timezone:
        final_datetime = final_datetime.replace(tzinfo=override_timezone)

    return final_datetime


def format_exception_human_readable(exc: Exception, *, quote_message: bool = False) -> str:
    result_begin: str = f'{exc.__class__.__name__}: '
    exc_msg: str = str(exc)

    return result_begin + (f'"{exc_msg}"' if quote_message else exc_msg)


def create_temporary_directory(root_dir: Path, seed: str | None = None):
    seed: str = seed or str(''.join(random.choice(ascii_letters) for _ in range(16)))
    tmp_dir: Path = root_dir / Path(seed)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir


def lookup_root_path(path_to_search_string: Path | str, remaining_iteration: int = 3, root_path: Path = Path().resolve()) -> Path:
    """
    Looks for the specified path_to_search_string starting from specified path (or current path, by default); checking
     iteratively in parent directory, during specified remaining_iteration iteration (default: 3).

    :param path_to_search_string:
    :param remaining_iteration:
    :param root_path:
    :return: the root path containing specified path_to_search_string (you need to concatenate result and path_to_search_string if you want a full path for it).
    """
    full_path: Path = root_path / Path(path_to_search_string)
    if full_path.exists():
        return root_path

    if not remaining_iteration:
        raise FileNotFoundError(f'Unable to find root_path of specified "{path_to_search_string}" path, after several iteration (last check in "{root_path}" directory).')

    return lookup_root_path(path_to_search_string, remaining_iteration - 1, root_path.parent)


def lookup_files_from_pattern(root_path: Path, pattern: str, *, min_file_size: float = None, case_insensitive: bool = True, logger: Logger = None):
    if case_insensitive:
        # Enhances the pattern to be case-insentitive.
        pattern = ''.join(map(lambda c: f'[{c.lower()}{c.upper()}]' if c.isalpha() else c, pattern))

    # Uses globbing in any case, according to the way pattern may have been enhanced to manage case.
    existing_files_list = list(root_path.glob(pattern))

    # Checks file size if needed.
    if min_file_size is not None:
        # Keeps only file whose size is greater of equal to specified size.
        existing_files_list = list(filter(lambda file: file.stat().st_size >= min_file_size, existing_files_list))

        if logger:
            logger.debug(f'After "file_size>={min_file_size} Bytes" filter, this is the list of files matching pattern "{pattern}": {existing_files_list=}')

    return existing_files_list


def check_file_exist_from_pattern(root_path: Path, pattern: str, *, min_file_size: float | None = None,
                                  case_insensitive: bool = True, logger: Logger | None = None):
    return len(lookup_files_from_pattern(root_path, pattern, min_file_size=min_file_size, case_insensitive=case_insensitive, logger=logger)) > 0


def lookup_available_packages(root_dir: Path | str, *, keep_children_packages: bool = False) -> set[str]:
    packages: list[str | bytes] = find_packages(root_dir)
    packages: set[str] = set(packages)
    if keep_children_packages:
        return packages

    # Removes all packages children.
    something_change: bool = True
    filtered_packages = packages
    while something_change:
        merged_children = set()
        for element in filtered_packages:
            # Merges all package children in the same set.
            merged_children ^= {child for child in filtered_packages - {element} if child.startswith(element)}

        # Updates filtered packages set if needed.
        filtered_packages -= merged_children

        # Registers something change.
        something_change = len(merged_children) > 0

    # Returns the final filtered packages set.
    return filtered_packages


def compute_file_line_count(file_path: Path):
    # Does not count one-line comment, empty line, line with only spaces characters, and docstring begin lines.
    # But following lines of docstring will unfortunately be counted, and it is an accepted limitation.
    source_code_line_pattern = re.compile(r'^\s*[^#"\s\']\S+.*$')
    source_code_line_count: int = 0
    with open(file_path, encoding='utf8') as file:
        for line in file:
            source_code_line_count += 1 if source_code_line_pattern.match(line) and len(line) > 4 else 0
    return source_code_line_count


def extract_class_fqn(specified_class: type) -> str:
    return f'{specified_class.__module__}.{specified_class.__name__}'


def dynamically_load_class(module_path: str, class_name: str):
    mod = __import__(module_path, fromlist=[class_name])
    return getattr(mod, class_name)


def inspect_attrs(obj, logger: Logger, patterns=None):
    pattern_info: str = 'with no condition' if not patterns else f'matching any of one of these patterns: {patterns}'
    logger.debug(f'Checking all Python attributes of instance "{obj}", {pattern_info}')
    for attr, value in obj.__dict__.items():
        if not patterns or any(pattern in attr for pattern in patterns):
            logger.debug(f'\t{attr=} => {value=}')


def flatten(collection):
    for item in collection:
        if isinstance(item, Iterable):
            yield from flatten(item)
        else:
            yield item


def filter_kwargs(*, args_filter: list[str], **kwargs):
    return dict(filter(lambda kv: print(f'{kv=}') or kv[0] in args_filter, kwargs.items()))
