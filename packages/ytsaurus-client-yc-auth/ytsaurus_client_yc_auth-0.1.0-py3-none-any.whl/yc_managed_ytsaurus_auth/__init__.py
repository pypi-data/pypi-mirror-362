import abc
import logging
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta
import os
import socket
from typing import Optional

import yt.packages.requests as requests
from yt.wrapper.http_driver import TokenAuth

# delta for comparison iam token expiration time
iam_token_expiration_period_epsilon = timedelta(seconds=10)

@dataclass
class IssuedIamToken:
    value: str
    expires_after_seconds: int

class IamTokenSource:
    CLI = 'cli'
    METADATA = 'metadata'

class IamTokenAuth(TokenAuth):
    def __init__(self, config=None):
        super().__init__(None)
        
        self.logger = logging.getLogger(__name__)
        self.expires_at = None
        self.metadata_host = os.getenv('YC_METADATA_ADDR', '169.254.169.254')
        
        config = config or {}
        self.profile = config.get('profile') 
        self.source = config.get('source')
    
        if self.source and self.source not in (IamTokenSource.CLI, IamTokenSource.METADATA):
            raise RuntimeError(f'invalid iam token source: {self.source}')

        if self._is_cli_installed():
            if self.source is None:
                self.source = IamTokenSource.CLI
                return
        elif self.source == IamTokenSource.CLI:
            raise RuntimeError('`yc` is not installed, see https://yandex.cloud/cli/')
        
        if self._is_metadata_available():
            if self.source is None:
                self.source = IamTokenSource.METADATA
        elif self.source == IamTokenSource.METADATA:
            raise RuntimeError('metadata server is not available, see https://yandex.cloud/docs/compute/operations/vm-connect/auth-inside-vm')

        if self.source is None:
            raise RuntimeError(
                'none of iam token sources are available, see '
                'https://yandex.cloud/cli/ to learn how to install `yc` utility or '
                'https://yandex.cloud/docs/compute/operations/vm-connect/auth-inside-vm to learn how to bind service account to VM'
            )

    def set_token(self, request):
        if self.token is not None:
            request.headers['Authorization'] = f'Bearer {self.token}' 

    def handle_redirect(self, request, **kwargs):
        self._update_token()
        return super().handle_redirect(request, **kwargs)

    def __call__(self, request):
        self._update_token()
        return super().__call__(request)

    def _update_token(self):
        now = datetime.now()
        expired = self.expires_at is None or now > self.expires_at - iam_token_expiration_period_epsilon
        if expired:
            issued_token = {
                IamTokenSource.CLI: self._issue_token_with_cli,
                IamTokenSource.METADATA: self._request_token_from_metadata,
            }[self.source]()
            self.token = issued_token.value
            self.expires_at = now + timedelta(seconds=issued_token.expires_after_seconds)

    def _is_cli_installed(self) -> bool:
        try:
            subprocess.run(['yc', 'version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False
        
    def _issue_token_with_cli(self) -> IssuedIamToken:
        self.logger.debug('issue iam token with `yc`...')

        cmd = ['yc', 'iam', 'create-token', '--no-user-output']
        if self.profile:
            cmd += ['--profile', self.profile]
        
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        if process.returncode != 0:
            raise RuntimeError(f'`yc` failed to create token, stderr:\n{process.stderr}')

        # there may be another output before the token, for example, info about opening the browser.
        # TODO: not sure if token will be last line (update suggestion appears regardless of --no-user-output flag
        token = process.stdout.strip().split('\n')[-1]
        return IssuedIamToken(
            value=token,
             # yc somehow caches IAM token but does not provide info about its expiration time, so let's just re-issue it frequently
            expires_after_seconds=5,
        )
    
    def _is_metadata_available(self) -> bool:
        try:
            with socket.create_connection((self.metadata_host, 80), timeout=1):
                # metadata host is present, not let's check if some SA associated with it (request token handler returns 200) 
                try:
                    self._request_token_from_metadata()
                    return True
                except Exception:
                    return False
        except Exception:
            return False

    def _request_token_from_metadata(self) -> IssuedIamToken:
        self.logger.debug('request iam token from metadata server...')

        resp = requests.get(
            f'http://{self.metadata_host}/computeMetadata/v1/instance/service-accounts/default/token',
            headers={'Metadata-Flavor': 'Google'},
            timeout=1,
        )
        resp.raise_for_status()
        resp = resp.json()

        return IssuedIamToken(
            value=resp['access_token'], 
            expires_after_seconds=resp['expires_in'],
        )


def with_iam_token_auth(
        config: Optional[dict] = None, 
        profile: Optional[str] = None, 
        source: Optional[str] = None,
    ) -> dict:
    config = config or {}
    params = {}
    config['auth_class'] = {
        'module_name': 'yc_managed_ytsaurus_auth', 
        'class_name': IamTokenAuth.__name__, 
        'config': params,
    }
    if profile:
        params['profile'] = profile
    if source:
        params['source'] = source
    return config
