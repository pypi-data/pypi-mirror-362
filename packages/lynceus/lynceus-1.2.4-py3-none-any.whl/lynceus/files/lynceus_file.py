import shutil
from abc import ABCMeta
from logging import Logger
from pathlib import Path
from typing import (Generic,
                    TypeVar)

import pandas as pd
import pyarrow
import pyarrow.parquet as pq
from fsspec.asyn import AsyncFileSystem
from pandas import DataFrame
from pandas.io.common import _get_filepath_or_buffer

from lynceus.core.config import (CONFIG_STORAGE_LOCAL,
                                 LYNCEUS_S3_CONFIG_KEY)
from lynceus.core.config.lynceus_config import LynceusConfig
from lynceus.files.remote.s3 import (S3FileSystemPatched,
                                     S3Utils)
from lynceus.lynceus_exceptions import LynceusFileError

# pylint: disable=invalid-name
FileSystemType = TypeVar("FileSystemType", bound=AsyncFileSystem)


class LynceusFile(Generic[FileSystemType], metaclass=ABCMeta):
    S3_PATH_BEGIN = 's3://'

    FILE_STORAGE_PATH_SEPARATOR: str = '|'

    def __init__(self,
                 path: Path,
                 logger: Logger,
                 filesystem: FileSystemType = None):
        self._path: Path = path
        self._logger: Logger = logger
        self._filesystem: FileSystemType = filesystem

    @staticmethod
    def extract_storage_and_path(file_metadata: str):
        # Checks if there is storage information in the metadata.
        if LynceusFile.FILE_STORAGE_PATH_SEPARATOR in file_metadata:
            file_metadata_parts = file_metadata.split(LynceusFile.FILE_STORAGE_PATH_SEPARATOR)
            return file_metadata_parts[0], file_metadata_parts[1]

        # There is none, so consider it as a file hosted on Local storage.
        return CONFIG_STORAGE_LOCAL, file_metadata

    @staticmethod
    def build_file_metadata(storage_name: str, file_path: str):
        return f'{storage_name}{LynceusFile.FILE_STORAGE_PATH_SEPARATOR}{file_path}'

    def read_parquet(self, **params) -> DataFrame:
        """
        Reads corresponding (local or remote) file, considering it as a parquet file, with optional parameters.
        :param params: optional parameters (usually, it can be columns, to specify which columns
                        to read from parquet file).
        :return: corresponding DataFrame.
        """
        # Cf. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_parquet.html
        # Cf. http://arrow.apache.org/docs/python/generated/pyarrow.parquet.read_table.html

        self._logger.debug(f'Reading file {self} ...')
        # pylint: disable=c-extension-no-member
        try:
            return pd.read_parquet(self.get_path(), storage_options=self.get_storage_options(), **params)
        except pyarrow.lib.ArrowInvalid as exc:
            # Special (somehow dirty) hack allowing to get a workaround about some issue with invalid datetime.
            # Initially needed for Exco project.
            if 'would result in out of bounds timestamp' not in str(exc):
                # N.B. it is not the "issue" for which the workaround has been developed.
                raise

            self._logger.warning(f'Caught "out of bounds timestamp" error while reading file {self} ... trying to read it with unsafe method as a workaround.')

            # The key of the workaround is the use the **safe=False** option on the to_pandas method,
            #  which can't be specified through Pandas.
            # But, because we are breaking down here the pd.read_parquet method, we need to work on the path
            #  using the pandas.io.common._get_filepath_or_buffer method to create a remote path if needed.
            ioargs = _get_filepath_or_buffer(self.get_path(), storage_options=self.get_storage_options())
            parquet_table = pq.read_table(ioargs.filepath_or_buffer, **params)
            return parquet_table.to_pandas(safe=False)

    def write_to_parquet(self, dataframe: DataFrame, **kwargs):
        # N.B.: **kwargs is the opportunity to provide parameters for internal implementation (e.g. PyArrow),
        #  for instances, pyarrow filters param, to better control what is load in memory.
        #
        # Cf. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_parquet.html
        # Cf. https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-parquet
        # Cf. https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html

        self._logger.debug(f'Writing specified DataFrame to file {self} ...')
        dataframe.to_parquet(self.get_path(),
                             coerce_timestamps='ms', allow_truncated_timestamps=True,
                             storage_options=self.get_storage_options(),
                             **kwargs)

    def get_storage_options(self):
        # pylint: disable=no-self-use
        return None

    def is_local(self):
        raise NotImplementedError()

    def is_remote(self):
        return not self.is_local()

    def delete(self):
        self._logger.debug(f'Deleting file {self} ...')
        return self._do_delete()

    def _do_delete(self):
        raise NotImplementedError()

    def download_to(self, destination: Path, *, create_sub_directories: bool = True):
        self._logger.debug(f'Retrieving/downloading file to "{destination}" from {self} ...')
        return self._do_download_to(destination=destination, create_sub_directories=create_sub_directories)

    def _do_download_to(self, *, destination: Path, create_sub_directories: bool):
        raise NotImplementedError()

    def exists(self, *, reason: str = None):
        check_msg: str = f'Checking existence of file {self}'
        if reason:
            check_msg += f' (reason: {reason})'
        self._logger.debug(f'{check_msg} ...')
        return self._do_exists()

    def _do_exists(self):
        raise NotImplementedError()

    def list_files(self, *, recursive: bool = False, pattern: str | None = None, **kwargs):
        self._logger.debug(f'Listing files from {self}, {pattern=} ...')
        return self._do_list_files(recursive=recursive, pattern=pattern, **kwargs)

    def _do_list_files(self, *, recursive: bool, pattern: str | None = None, **kwargs):
        raise NotImplementedError()

    def copy_to(self, destination: Path, *, create_sub_directories: bool = True):
        self._logger.debug(f'Copying {self} to local file {destination} ...')
        return self._do_copy_to(destination=destination, create_sub_directories=create_sub_directories)

    def _do_copy_to(self, *, destination: Path, create_sub_directories: bool):
        raise NotImplementedError()

    def get_name(self) -> str:
        return self._path.name

    @property
    def path(self) -> Path:
        return self._path

    def get_path(self) -> str:
        return str(self._path)

    def get_raw_path(self) -> str:
        raise NotImplementedError()

    def get_relative_path(self) -> str:
        """
        :return: for remote file: the relative path from remote storage container, for local file: same than raw_path.
        """
        raise NotImplementedError()

    def get_parent_path(self) -> Path:
        return self._path.parent

    def parent_exists(self):
        self._logger.debug(f'Checking existence of parent folder of file {self} ...')
        return self._do_parent_exists()

    def _do_parent_exists(self):
        raise NotImplementedError()

    def get_extension(self) -> str:
        return self._path.suffix

    def __str__(self):
        return f'"{self.__class__.__name__}" with path "{self._path}"'

    def __repr__(self):
        return str(self)


class _LocalLynceusFile(LynceusFile[AsyncFileSystem]):
    def is_local(self):
        return True

    def _do_delete(self):
        self._path.unlink()

    def _do_download_to(self, *, destination: Path, create_sub_directories: bool):
        return self._do_copy_to(destination=destination, create_sub_directories=create_sub_directories)

    def _do_exists(self):
        return self._path.exists()

    def _do_parent_exists(self):
        return self.get_parent_path().exists()

    def _do_list_files(self, *, recursive: bool, pattern: str | None = None, **kwargs):
        if not recursive:
            return self._path.iterdir()
        return self._path.glob(pattern or '**/*')

    def _do_copy_to(self, *, destination: Path, create_sub_directories: bool):
        if not destination.parent.exists():
            if create_sub_directories:
                destination.parent.mkdir(parents=True, exist_ok=True)
            else:
                raise LynceusFileError(f'Parent directory of specified destination "{destination}" does not exist;' +
                                       ' you should either create it yourself, or use the corresponding option.')

        # Requests the copy.
        shutil.copyfile(self.get_path(), destination)

    def get_raw_path(self) -> str:
        return str(self._path)

    def get_relative_path(self) -> str:
        return self.get_raw_path()


class _RemoteS3LynceusFile(LynceusFile[S3FileSystemPatched]):
    # In addition there is a self.S3_PATH_BEGIN usage in Factory which should be adapted (in case it is NOT S3 !).
    def __init__(self, path: Path, logger: Logger, s3filesystem: S3FileSystemPatched, s3_utils: S3Utils):
        super().__init__(path, logger, filesystem=s3filesystem)
        self.__s3_utils = s3_utils

    def get_storage_options(self):
        # N.B.: in our Patched remote fs System, we added the needed lynceus_s3_config.
        storage_options = {
            'anon': False,
            LYNCEUS_S3_CONFIG_KEY: self._filesystem.lynceus_s3_config
        }

        # Checks if it is an OVH remote storage.
        if '.ovh.' in self._filesystem.lynceus_s3_config['s3_endpoint']:
            # Hacks ACL information to workaround OVH Bug, with default ACL specified by s3fs/botocore.
            # Leading to an useless "OSError: [Errno 22] Invalid Argument." ...
            storage_options.update(
                {
                    's3_additional_kwargs': {'ACL': 'private'}
                }
            )

        return storage_options

    def is_local(self):
        return False

    def _do_delete(self):
        self._filesystem.rm_file(self.get_raw_path())

    # pylint: disable=unused-argument
    def _do_download_to(self, *, destination: Path, create_sub_directories: bool):
        return self._filesystem.get(self.get_path(), str(destination))

    def _do_exists(self):
        # N.B.: in case exists check does not work properly, it is possible to use ls, forcing cache refresh.
        # bucket, key, version_id = self.__s3filesystem.split_path(self._path)
        # Checks with a forced refresh, in case the file has been generated by this Data Exporter execution.
        # return len(self.__s3filesystem.ls(key, refresh=True)) > 0

        # Checks if it exists, letting internal s3 FS to use its cache system.
        # pylint: disable=broad-except
        try:
            # TODO: understand the Bad request which happens sometimes ...
            return self._filesystem.exists(self.get_raw_path())
        except Exception as exc:
            self._logger.warning(f'An exception occured while checking existence of remote file "{self}" (it will be considered as not existing).', exc_info=exc)
            # Can happen for instance with a bad/broken specified path;
            #   caller raises an exception on none existence which is enough (so here, we just return the file does not exist).
            return False

    def _do_parent_exists(self):
        return self._filesystem.exists(self.get_raw_path_from_remote_path(self.get_parent_path()))

    # pylint: disable=arguments-differ
    def _do_list_files(self, *,
                       recursive: bool,
                       pattern: str | None = None,
                       maxdepth: int | None = None,
                       withdirs: bool | None = None,
                       detail: bool = False):
        return self.__s3_utils.list_remote_files(remote_root_path=Path(self.get_raw_path()),
                                                 recursive=recursive,
                                                 pattern=pattern,
                                                 maxdepth=maxdepth,
                                                 withdirs=withdirs,
                                                 detail=detail)

    # pylint: disable=unused-argument
    def _do_copy_to(self, *, destination: Path, create_sub_directories: bool):
        if self.is_remote() and destination.is_absolute():
            raise LynceusFileError(f'You should use only relative Path with remote file ("{self}"), which is not the case of destination "{destination}"')

        bucket_name, _, _ = self.__s3_utils.split_path(remote_file_path=self.get_path())
        return self._filesystem.copy(self.get_path(), str(Path(bucket_name) / destination))

    def get_path(self) -> str:
        # Important: to work, we must ensure the S3 PATH Begin is unaltered here (the double slash is mandatory ...).
        return LynceusFile.S3_PATH_BEGIN + self.get_raw_path()

    @staticmethod
    def get_raw_path_from_remote_path(path: Path):
        # Removes the 's3:/' prefix to get a raw path.
        raw_path_from_remote_path = str(path)[len(LynceusFile.S3_PATH_BEGIN) - 1:]

        # Safe-guard: ensures there is at least one '/' in the final raw path (which is NOT the case for remote 'root path',
        #  to avoid issue with s3fs path splitting feature, and avoid 'Could not traverse all s3' issue).
        if '/' not in raw_path_from_remote_path:
            raw_path_from_remote_path += '/'

        return raw_path_from_remote_path

    def get_raw_path(self) -> str:
        return self.get_raw_path_from_remote_path(self._path)

    def get_relative_path(self) -> str:
        _, rpath, _ = self.__s3_utils.split_path(remote_file_path=self.get_path())
        return rpath

    def __str__(self):
        return f'"{self.__class__.__name__}" with path "{self._path}" on remote "{LynceusConfig.format_config(self._filesystem.lynceus_s3_config)}"'
