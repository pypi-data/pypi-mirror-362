from lynceus.core.exchange.lynceus_exchange import LynceusExchange
from lynceus.core.lynceus import LynceusSession
from lynceus.core.lynceus_client import LynceusClientClass
from .github_devops_analyzer import GithubDevOpsAnalyzer
from .gitlab_devops_analyzer import GitlabDevOpsAnalyzer
from ..core.config import (CONFIG_AUTHENTICATION_KEY,
                           CONFIG_PROJECT_CRED_SECRET,
                           CONFIG_PROJECT_CRED_SECRET_GITHUB_DEFAULT,
                           CONFIG_PROJECT_CRED_SECRET_GITLAB_DEFAULT,
                           CONFIG_PROJECT_KEY,
                           CONFIG_PROJECT_URI)
from ..core.config.lynceus_config import LynceusConfig


class DevOpsFactory(LynceusClientClass):
    def __init__(self, lynceus_session: LynceusSession, lynceus_exchange: LynceusExchange | None):
        super().__init__(lynceus_session, 'devops', lynceus_exchange)

    def new_devops_analyzer(self, uri: str, token: str):
        if 'gitlab' in uri:
            self._logger.debug(f'Instantiating a Gitlab implementation, according to uri \'{uri}\'')
            return GitlabDevOpsAnalyzer(self._lynceus_session, uri, token, self._lynceus_exchange)

        self._logger.debug(f'Instantiating a Github implementation, according to uri \'{uri}\'')
        return GithubDevOpsAnalyzer(self._lynceus_session, uri, token, self._lynceus_exchange)

    def get_access_token_simulating_anonymous_access(self, *, uri: str, lynceus_config: LynceusConfig):
        if 'gitlab' in uri:
            default_credential_secret_key: str = CONFIG_PROJECT_CRED_SECRET_GITLAB_DEFAULT
        else:
            default_credential_secret_key: str = CONFIG_PROJECT_CRED_SECRET_GITHUB_DEFAULT

        default_credential_secret: str = lynceus_config.get_config(CONFIG_AUTHENTICATION_KEY, default_credential_secret_key, default=None)
        if default_credential_secret:
            self._logger.warning(f'No specific "{CONFIG_PROJECT_CRED_SECRET}" in your [{CONFIG_AUTHENTICATION_KEY}] configuration,'
                                 f' using the configured "{default_credential_secret_key}" one.')
            lynceus_config[CONFIG_AUTHENTICATION_KEY][CONFIG_PROJECT_CRED_SECRET] = default_credential_secret
            return default_credential_secret

        error_message: str = f'Unable to find "{CONFIG_PROJECT_CRED_SECRET}" in your [{CONFIG_AUTHENTICATION_KEY}] configuration,'
        error_message += f' and there is no "{default_credential_secret_key}" configured. Update your configuration and try again.'

        self._logger.warning(error_message)
        raise ValueError(error_message)

    def check_and_enhance_configuration_for_anonymous_access(self, lynceus_config: LynceusConfig):
        uri: str = lynceus_config.get_config(CONFIG_PROJECT_KEY, CONFIG_PROJECT_URI)
        configured_credential_secret: str = lynceus_config.get_config(CONFIG_PROJECT_KEY, CONFIG_PROJECT_CRED_SECRET, default=None)
        if configured_credential_secret is None:
            lynceus_config[CONFIG_PROJECT_KEY][CONFIG_PROJECT_CRED_SECRET] = self.get_access_token_simulating_anonymous_access(uri=uri, lynceus_config=lynceus_config)
