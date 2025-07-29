from logging import Logger
from pathlib import Path

import s3fs

from lynceus.core.config import CONFIG_STORAGE_DYNAMIC_TYPE, CONFIG_STORAGE_IS_DYNAMIC, CONFIG_STORAGE_REMOTE_TYPE, LYNCEUS_S3_CONFIG_KEY
from lynceus.core.config.lynceus_config import LynceusConfig
from lynceus.core.exchange.lynceus_exchange import LynceusExchange
from lynceus.core.lynceus import LynceusSession
from lynceus.core.lynceus_client import LynceusClientClass
from lynceus.lynceus_exceptions import LynceusFileError


class S3Utils(LynceusClientClass):
    def __init__(self, *, lynceus_session: LynceusSession, lynceus_exchange: LynceusExchange | None, lynceus_s3_config: dict[str, str]):
        super().__init__(lynceus_session=lynceus_session, logger_name='s3', lynceus_exchange=lynceus_exchange)
        self.__lynceus_s3_config = lynceus_s3_config
        self.__s3filesystem = None

    def initialize(self):
        self._logger.info('Initializing s3fs according to configuration.')
        s3fs.S3FileSystem = S3FileSystemPatched

    def get_s3filesystem(self):
        if self.__s3filesystem is None:
            self.__s3filesystem = s3fs.S3FileSystem(**{LYNCEUS_S3_CONFIG_KEY: self.__lynceus_s3_config})

        return self.__s3filesystem

    def force_cache_refresh(self, path: Path = None):
        if self.__s3filesystem:
            self._logger.debug(f'Refreshing S3 fs cache ({path=}) ...')
            self.__s3filesystem.invalidate_cache(path=str(path) if path else None)

    def split_path(self, *, remote_file_path: str):
        return self.get_s3filesystem().split_path(remote_file_path)

    def list_remote_files(self, *, remote_root_path: Path,
                          recursive: bool, pattern: str | None = None,
                          maxdepth: int | None = None, withdirs: bool | None = None,
                          detail: bool = False):
        def _retrieve_remote_files():
            if recursive:
                # s3fs Globing feature does not support path with the 's3:/' prefix ...
                return self.get_s3filesystem().glob(str(Path(remote_root_path) / Path(pattern or '**/*')),
                                                    maxdepth=maxdepth, detail=detail)

            # Uses the find method, because ls one is NOT implemented in s3fs.
            # Some options are used only if pattern is NOT defined.
            find_kwargs = {
                'detail': detail
            }

            if pattern:
                find_kwargs.update({'prefix': pattern})
            else:
                find_kwargs.update(
                    {
                        'maxdepth': maxdepth or 1,
                        'withdirs': withdirs if not None else True
                    }
                )

            # s3 find feature does not support path with the 's3:/' prefix ...
            return self.get_s3filesystem().find(path=remote_root_path, **find_kwargs)

        def _extract_path(remote_file_path):
            return self.split_path(remote_file_path=remote_file_path)[1]

        try:
            self._logger.debug(f'Looking/globbing for remote files ({remote_root_path=}; {pattern=}) ...')
            all_remote_file_metadata = _retrieve_remote_files()

            # Processed result according to requested detail
            #  - only path are returned as a list
            if not detail:
                return [_extract_path(remote_file_path) for remote_file_path in all_remote_file_metadata]

            #  - path, and lots of metadata are returned as a dict
            return {_extract_path(remote_file_key): remote_file_detailed_metadata
                    for remote_file_key, remote_file_detailed_metadata in all_remote_file_metadata.items()}
        except Exception as exc:  # pylint: disable=broad-except
            # pylint: disable=raise-missing-from
            raise LynceusFileError(f'An error occured while looking/globbing for remote files ({remote_root_path=}; {pattern=}) ...', from_exception=exc)


# Patch and initialize s3fs once for all.
# pylint: disable=useless-super-delegation,abstract-method
class S3FileSystemPatched(s3fs.S3FileSystem):
    def __init__(self, *k, **kw):
        # Extracts s3 config key from parameters.
        self.lynceus_s3_config = kw.pop(LYNCEUS_S3_CONFIG_KEY, None)
        if not self.lynceus_s3_config:
            raise ValueError(f'{LYNCEUS_S3_CONFIG_KEY} is a mandatory parameter when initializing S3FileSystemPatched')

        lynceus: LynceusSession = LynceusSession.get_session(registration_key={'user': 's3filesystem'})
        logger: Logger = lynceus.get_logger('s3Init')
        logger.info(f'Using S3 config "{LynceusConfig.format_config(self.lynceus_s3_config)}".')

        # Builds client kwargs.
        client_kwargs = {
            'endpoint_url': self.lynceus_s3_config['s3_endpoint'],
        }

        # Adds any additional/extra parameters to client kwargs.
        client_kwargs.update(
            {key: value for key, value in self.lynceus_s3_config.items()
             if key not in (CONFIG_STORAGE_REMOTE_TYPE, 'endpoint_url', 'bucket_name', 'username',
                            'access_key_id', 'secret_access_key', 's3_endpoint', 'addressing_style',
                            CONFIG_STORAGE_IS_DYNAMIC, CONFIG_STORAGE_DYNAMIC_TYPE)}
        )
        logger.info(f'System will use these S3 client kwargs: "{LynceusConfig.format_config(client_kwargs)}".')

        super().__init__(*k,
                         key=self.lynceus_s3_config.get('access_key_id'),
                         secret=self.lynceus_s3_config.get('secret_access_key'),
                         client_kwargs=client_kwargs,
                         **kw)

    async def _rm(self, path, recursive=False, **kwargs):
        return await super()._rm(path, recursive, **kwargs)

    async def _rm_file(self, path, **kwargs):
        return await super()._rm_file(path, **kwargs)

    def created(self, path):
        return super().created(path)

    def cp_file(self, path1, path2, **kwargs):
        return super().cp_file(path1, path2, **kwargs)

    def sign(self, path, expiration=100, **kwargs):
        return super().sign(path, expiration, **kwargs)

    def ls(self, path, detail=True, **kwargs):
        # See: s3fs.core.S3FileSystem._find
        return self.find(path, maxdepth=1, withdirs=True, detail=detail, **kwargs)
