"""
Note - the Cyberark class below is adapted from one that Jeff Hagley wrote
and placed in umnet-scripts. Instead of augmenting that class, we've created
a new one here so that this package isn't dependent on the umnet-scripts
package, which has many dependencies of its own.
"""

import sys
from typing import Optional
from dataclasses import dataclass

from decouple import Config, RepositoryEnv
import requests
import urllib3

urllib3.disable_warnings()

CYBERARK_TIMEOUT = 30


class CyberarkLookupError(Exception):
    pass


class CyberarkTimeoutError(Exception):
    pass


class CyberarkAuthError(Exception):
    pass


@dataclass
class CyberarkEnvironment:
    name: str
    cert: tuple[str, str]
    appid: str
    safe: str


class Cyberark:
    """
    Class that interacts with the cyberark API.
    """

    def __init__(
        self, env_file: str = "cyberark.env", environment: Optional[str] = "UMNET"
    ):
        self.env_config = Config(RepositoryEnv(env_file))
        self.url_base = self.env_config.get("URL_BASE")
        self.url_aim_endpoint = self.env_config.get("URL_AIM_ENDPOINT")
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
        }
        self.set_environment(environment)

    def set_environment(self, environment: str):
        environment = environment.upper()

        if environment == "UMNET":
            self.env = CyberarkEnvironment(
                environment,
                (self.env_config.get("CERT"), self.env_config.get("KEY")),
                self.env_config.get("APPID"),
                self.env_config.get("SAFE"),
            )
        elif environment == "NSO":
            self.env = CyberarkEnvironment(
                environment,
                (self.env_config.get("NSO_CERT"), self.env_config.get("NSO_KEY")),
                self.env_config.get("NSO_APPID"),
                self.env_config.get("NSO_SAFE"),
            )
        elif environment == "DEARBORN":
            self.env = CyberarkEnvironment(
                environment,
                (
                    self.env_config.get("DEARBORN_CERT"),
                    self.env_config.get("DEARBORN_KEY"),
                ),
                self.env_config.get("DEARBORN_APPID"),
                self.env_config.get("DEARBORN_SAFE"),
            )

        else:
            raise ValueError(f"Unknown cyberark environment {environment}")

    def query_cyberark(
        self, password_entity: str, environment: Optional[str] = None
    ) -> str:
        """
        Queries cyberark for a specific entity
        """
        if sys.version.startswith("3.8"):
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = (  # pylint: disable=no-member
                "ALL:@SECLEVEL=1"
            )
        if environment:
            self.set_environment(environment)

        aim_url = (
            self.url_base
            + self.url_aim_endpoint
            + self.env.appid
            + self.env.safe
            + "&Object="
            + password_entity
        )
        try:
            acct = requests.get(
                aim_url,
                headers=self.headers,
                cert=self.env.cert,
                verify=True,
                timeout=CYBERARK_TIMEOUT,
            )
        except requests.exceptions.ReadTimeout:
            raise CyberarkTimeoutError(
                f"Cyberark query for {password_entity} timed out after {CYBERARK_TIMEOUT} seconds"
            )

        if acct.status_code == 404:
            raise CyberarkLookupError(
                f"No password found for {password_entity} environment {self.env.name}"
            )
        if acct.status_code == 403:
            raise CyberarkAuthError(f"Could not auth to cyberark for {self.env.name}")

        result = acct.json()

        if acct.status_code != 200 or not result or "Content" not in result:
            raise CyberarkLookupError(
                f"Invalid response from cyberark for {password_entity} environment {self.env.name}"
            )

        return result["Content"]

    def lookup_enable(self, host: str = "", environment: Optional[str] = None) -> str:
        """
        Looks up an 'enable' password for a specific host
        """
        if environment:
            self.set_environment(environment)

        return self.query_cyberark(f"{host}_enable")

    def lookup_username_password(
        self,
        username: str,
        host: Optional[str] = None,
        environment: Optional[str] = None,
    ) -> str:
        """
        Looks up the password for a specific username, optionally on a specific host.
        If there's no password found for that specific host, looks for that
        username for *all* hosts
        """
        if environment:
            self.set_environment(environment)

        # host passwords without usernames are stored in cyberark as 'name_user_name'
        if host is None:
            entity = f"{username}_user_{username}"
        else:
            entity = f"{host}_{username}"

        try:
            return self.query_cyberark(entity)
        except CyberarkLookupError:
            return self.query_cyberark(f"_{username}")
