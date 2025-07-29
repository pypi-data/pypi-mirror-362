"""
This module encapsulates global configuration settings for the DBNL python SDK
It encodes precendece rules for getting configuration variable values.

Configuration settings order of precedence is :
explicit pass to login() > env var  > internal default

"""

import json
import logging
import os
import re
import warnings
from typing import Any, Literal, Optional
from urllib.parse import ParseResult, urlparse, urlunparse

from dbnl.errors import DBNLConfigurationError

DBNL_ENV_VARS = [
    "DBNL_API_TOKEN",
    "DBNL_API_URL",
    "DBNL_APP_URL",
    "DBNL_LOG_LEVEL",
    "DBNL_NAMESPACE_ID",
]


class _Config:
    def __init__(self) -> None:
        # mutable config are variable values passed
        # in via special functions eg login()
        self.mutable_config: dict[str, str] = {}

        # env var config are variable values passed from environment variables
        self.env_var_config: dict[str, str] = {}
        for env_var_name in DBNL_ENV_VARS:
            env_var_value = os.environ.get(env_var_name)
            if env_var_value:
                self.env_var_config[env_var_name] = env_var_value

    def get_config_with_precedence(self, var_name: str) -> Optional[str]:
        if var_name in self.mutable_config.keys():
            return self.mutable_config[var_name]

        if var_name.upper() in self.env_var_config.keys():
            return self.env_var_config[var_name.upper()]

        return None

    @property
    def dbnl_logged_in(self) -> bool:
        _var_name = "dbnl_logged_in"
        config_with_prec = self.get_config_with_precedence(_var_name)

        if config_with_prec:
            return config_with_prec == "True"

        return False

    @dbnl_logged_in.setter
    def dbnl_logged_in(self, value: bool) -> None:
        # these mutable config properties should be the exception
        # most config state should be immutable
        _var_name = "dbnl_logged_in"
        self.mutable_config[_var_name] = str(value)

    def _set_url_defaults(
        self,
        env_name: Literal["DBNL_API_URL", "DBNL_APP_URL"],
        url: str,
        scheme: str = "https",
    ) -> str:
        # NOTE: urlparse doesn't do the expected thing when the scheme is absent
        # https://bugs.python.org/issue754016
        original_url = url
        if "//" not in url:
            url = "//" + url
        parsed = urlparse(url, scheme=scheme)
        if parsed.fragment or parsed.query or parsed.params:
            raise DBNLConfigurationError(f"Invalid {env_name}: {original_url}. URL contains extra parts.")
        if not parsed.path.endswith("/"):
            parsed = parsed._replace(path=parsed.path + "/")
        return urlunparse(parsed)

    _dbnl_api_url_key = "dbnl_api_url"

    @property
    def dbnl_api_url(self) -> str:
        _var_name = self._dbnl_api_url_key

        config_with_prec = self.get_config_with_precedence(_var_name)

        if config_with_prec:
            return self._set_url_defaults("DBNL_API_URL", config_with_prec)

        raise DBNLConfigurationError(
            "The DBNL_API_URL environment variable is not set."
            " Please set the DBNL_API_URL environment variable to the base URL of the DBNL API."
        )

    @dbnl_api_url.setter
    def dbnl_api_url(self, value: str) -> None:
        # these mutable config properties should be the exception
        # most config state should be immutable
        self._set_url_defaults("DBNL_API_URL", value)  # validate the URL
        _var_name = self._dbnl_api_url_key
        self.mutable_config[_var_name] = value

    @property
    def dbnl_api_token(self) -> str:
        _var_name = "dbnl_api_token"

        config_with_prec = self.get_config_with_precedence(_var_name)

        if config_with_prec:
            return config_with_prec

        # cannot have internal default for api token
        raise DBNLConfigurationError(
            "Can't find DBNL API token, please set the DBNL_API_TOKEN env variable. "
            "This token can be retrieved from the {self.dbnl_app_url}tokens page of the DBNL app"
        )

    @dbnl_api_token.setter
    def dbnl_api_token(self, value: str) -> None:
        # these mutable config properties should be the exception
        # most config state should be immutable
        _var_name = "dbnl_api_token"
        self.mutable_config[_var_name] = value

    @property
    def dbnl_namespace_id(self) -> Optional[str]:
        _var_name = "dbnl_namespace_id"
        config_with_prec = self.get_config_with_precedence(_var_name)

        if config_with_prec:
            return config_with_prec

        # internal default
        return None

    @dbnl_namespace_id.setter
    def dbnl_namespace_id(self, value: str) -> None:
        # these mutable config properties should be the exception
        # most config state should be immutable
        _var_name = "dbnl_namespace_id"
        self.mutable_config[_var_name] = value

    def clear_mutable_config(self) -> None:
        self.mutable_config = {}

    @property
    def dbnl_app_url(self) -> str:
        _var_name = "dbnl_app_url"
        config_with_prec = self.get_config_with_precedence(_var_name)
        if config_with_prec:
            return self._set_url_defaults("DBNL_APP_URL", config_with_prec)
        api_url = self.dbnl_api_url
        parsed = urlparse(api_url)
        dbnl_domain_re = re.compile(r"^api(|-.*|\..*)\.dbnl\.com(|:.*)$")
        if dbnl_domain_re.search(parsed.netloc):
            app_netloc = "app" + parsed.netloc[len("api") :]
            path = parsed.path
        else:
            app_netloc = parsed.netloc
            # assume that the root is the app
            path = ""
        if not path.endswith("/"):
            path += "/"
        return urlunparse(
            ParseResult(
                scheme=parsed.scheme,
                netloc=app_netloc,
                path=path,
                params="",
                query="",
                fragment="",
            )
        )

    @dbnl_app_url.setter
    def dbnl_app_url(self, value: str) -> None:
        # these mutable config properties should be the exception
        # most config state should be immutable
        self._set_url_defaults("DBNL_APP_URL", value)  # validate the URL
        _var_name = "dbnl_app_url"
        self.mutable_config[_var_name] = value

    @property
    def dbnl_log_level(self) -> int:
        _var_name = "dbnl_log_level"
        config_with_prec = self.get_config_with_precedence(_var_name)
        if config_with_prec:
            if config_with_prec.isdigit():
                return int(config_with_prec)
            level_name: Any = logging.getLevelName(config_with_prec.upper())
            if isinstance(level_name, int):
                return level_name
            warnings.warn(
                f"Invalid log level: {config_with_prec}."
                f" Please set the DBNL_LOG_LEVEL environment variable to one of"
                f" {', '.join(logging._nameToLevel.keys())}.",
                UserWarning,
            )
        # internal default
        return logging.WARNING

    @property
    def json(self) -> str:
        return json.dumps(
            {
                "api_token": self.dbnl_api_token,
                "api_url": self.dbnl_api_url,
                "app_url": self.dbnl_app_url,
                "namespace_id": self.dbnl_namespace_id,
                "log_level": self.dbnl_log_level,
            },
            indent=2,
        )


CONFIG = _Config()
