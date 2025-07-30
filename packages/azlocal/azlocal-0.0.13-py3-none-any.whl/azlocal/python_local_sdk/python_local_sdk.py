import os
from pathlib import Path
from typing import Optional

from ..shared import get_proxy_endpoint, get_proxy_env_vars, get_default_proxy_certificate_location, get_custom_proxy_certificate_location


class PythonLocalSdk:

    def __init__(self):
        self._started = False
        self._existing_env_vars: dict[str, str] = {}
        self._proxy_endpoint = get_proxy_endpoint()
        self._tmp_certificate_location: Optional[str] = None

    def start_interception(self, use_temp_dir_for_ca_certificate: bool = False):
        """
        Start intercepting all Azure requests by configuring a proxy. To ensure that the proxy is trusted, it will use the CA root certificate in the default directory,
        '$HOME/.localstack/azure/ca.crt', or download if from the Emulator if it doesn't exist.

        :param use_temp_dir_for_ca_certificate: If TRUE: download the CA root certificate to a temp directory, instead of using the one in the default directory.
        :return:
        """
        if self._started:
            return

        proxy_endpoint = get_proxy_endpoint()
        if use_temp_dir_for_ca_certificate:
            certificate_location = get_custom_proxy_certificate_location(proxy_endpoint)
            self._tmp_certificate_location = certificate_location
        else:
            certificate_location = get_default_proxy_certificate_location(proxy_endpoint)

        proxy_env_vars = get_proxy_env_vars(proxy_endpoint, certificate_path=certificate_location)

        # Keep a copy of the existing env vars
        # We're about to overwrite them, but we do want to revert them to the old value when we're done
        self._existing_env_vars = {
            "HTTP_PROXY": os.environ.get("HTTP_PROXY"),
            "HTTPS_PROXY": os.environ.get("HTTPS_PROXY"),
            "MSSQL_ACCEPT_EULA": os.environ.get("MSSQL_ACCEPT_EULA"),
            "REQUESTS_CA_BUNDLE": os.environ.get("REQUESTS_CA_BUNDLE"),
        }

        os.environ.update(proxy_env_vars)

    def stop_interception(self):
        if not self._started:
            return
        os.environ.update({k:v for k,v in self._existing_env_vars.items() if v})
        self._existing_env_vars.clear()

        if self._tmp_certificate_location:
            Path(self._tmp_certificate_location).unlink()
            self._tmp_certificate_location = None

        self._started = False
