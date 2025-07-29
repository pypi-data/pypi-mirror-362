from typing import Optional
from types import ModuleType

import importlib.machinery
import importlib.util

from os import getenv
from os.path import isdir
import re
import sys

import yaml
from decouple import UndefinedValueError, Config, RepositoryEnv
from cron_converter import Cron

from umnet_napalm.abstract_base import AbstractUMnetNapalm

from .mappers import credentials, save_to_db, save_to_file
from .utils import agador_cfg


class AgadorError(Exception):
    pass


class CommandMapError(Exception):
    def __init__(self, cmd: str, error_str: str):
        super().__init__(f"command map error for '{cmd}' - {error_str}")


class CredentialMapError(Exception):
    pass


def apply_config_settings(cfg_file: Optional[str]):
    """
    Get config settings from file, or if 'None' is provided, look for 'AGADOR_CFG'
    in environment. Update global variables with an 'AGADOR' attribute
    so we can reference the settings anywhere in the code.
    """

    cfg_file = cfg_file if cfg_file else getenv("AGADOR_CFG")
    if not cfg_file:
        raise AgadorError("No config file provided, and no AGADOR_CFG env set!")

    try:
        globals()["AGADOR"] = Config(RepositoryEnv(cfg_file)).repository.data

    except FileNotFoundError:
        raise AgadorError(f"Cannot locate agador config file {cfg_file}")

    load_command_map()
    load_credential_map()


def load_inventory_filters(file_name: str) -> ModuleType:
    """
    Loads inventory filters if they're not loaded already
    """

    # Prefer to only load the module once
    if "inventory_filters" not in sys.modules:
        loader = importlib.machinery.SourceFileLoader("inventory_filters", file_name)
        spec = importlib.util.spec_from_loader("inventory_filters", loader)
        inventory_filters = importlib.util.module_from_spec(spec)
        try:
            sys.modules["inventory_filters"] = inventory_filters
            loader.exec_module(inventory_filters)

        except Exception as e:
            raise AgadorError(f"Could not load inventory filters from {file_name}: {e}")

    # returning referece to modules for convenience
    return sys.modules["inventory_filters"]


def load_command_map():
    """
    Parses and validates command_map file, replacing text references
    to functions to references to the actual functions where applicable.

    Future task: pydantic-based validation
    """

    db_module = save_to_db
    file_module = save_to_file

    inventory_filters = load_inventory_filters(agador_cfg("INVENTORY_FILTERS"))

    with open(agador_cfg("CMD_MAP"), encoding="utf-8") as fh:
        cmd_map = yaml.safe_load(fh)

    output = {}

    ## agador netbox inventory filter
    globals()["AGADOR"]["NETBOX_INVENTORY_FILTER"] = cmd_map.get(
        "netbox_inventory_filter"
    )

    for cmd, data in cmd_map["commands"].items():
        output[cmd] = {}

        # validating frequency, which is required
        if "frequency" not in data:
            raise CommandMapError(cmd, "Must specify frequency")
        try:
            output[cmd]["frequency"] = Cron(data["frequency"])
        except ValueError:
            raise CommandMapError(cmd, "Invalid frequency - must be in crontab format")

        # validating umnet_napalm getter specification
        if "getter" not in data:
            raise CommandMapError(cmd, "Must specify umnet_napalm getter")
        if data["getter"] not in dir(AbstractUMnetNapalm):
            raise CommandMapError(cmd, f"Unknown umnet_napalm getter {data['getter']}")
        output[cmd]["getter"] = data["getter"]

        # validating and retrieving inventory filter fuction
        inv_filter = data.get("inventory_filter", None)
        if inv_filter:
            if inv_filter not in dir(inventory_filters):  # noqa: F821
                raise CommandMapError(cmd, f"Unknown inventory filter {inv_filter}")

            output[cmd]["inventory_filter"] = getattr(inventory_filters, inv_filter)  # noqa: F821

        # validating and retrieving save_to_file class
        file_data = data.get("save_to_file", None)
        if file_data:
            if "mapper" not in file_data:
                raise CommandMapError(cmd, "Must specify mapper for save_to_file")

            if "destination" not in file_data:
                raise CommandMapError(cmd, "Must specify destination for save_to_file")

            destination = resolve_envs(file_data["destination"])
            if not isdir(destination):
                raise CommandMapError(
                    cmd, f"Invalid desintation {destination} for save_to_file"
                )

            if file_data["mapper"] not in dir(file_module):
                raise CommandMapError(
                    cmd, f"Unknown save_to_file mapper {file_data['mapper']}"
                )

            output[cmd]["save_to_file"] = {
                "mapper": getattr(file_module, file_data["mapper"])(destination),
            }

        # validating and retrieving save_to_db class
        db_data = data.get("save_to_db", None)
        if db_data:
            if db_data not in dir(db_module):
                raise CommandMapError(cmd, f"Unknown save_to_db mapper {db_data}")

            output[cmd]["save_to_db"] = getattr(db_module, db_data)

        if not db_data and not file_data:
            raise CommandMapError(
                cmd, "Must specifiy either save_to_db or save_to_file"
            )

    globals()["AGADOR"]["CMD_MAP"] = output


def load_credential_map():
    """
    Parses and validates the credential map file, replacing references
    to filters and mappers with actual functions

    Future task: pydantic-based validation
    """

    required_default_fields = ["username", "password", "mapper", "enable"]
    required_custom_fields = ["mapper", "inventory_filter"]

    inventory_filters = load_inventory_filters(agador_cfg("INVENTORY_FILTERS"))

    with open(agador_cfg("CRED_MAP"), encoding="utf-8") as fh:
        cred_map = yaml.safe_load(fh)

    output = {}

    ##### default credential validation
    if "defaults" not in cred_map:
        raise CredentialMapError("Default credentials must be specified!")

    for reqd in required_default_fields:
        if reqd not in cred_map["defaults"]:
            raise CredentialMapError(f"default {reqd} is required")

    output["defaults"] = {}
    for k, v in cred_map["defaults"].items():
        if k == "mapper":
            if v not in dir(credentials):
                raise CredentialMapError(f"Invalid credential mapper {v}")
            output["defaults"]["mapper"] = getattr(credentials, v)
        else:
            output["defaults"][k] = v

    ##### custom credentials parsing
    output["custom"] = []
    seen_filters = []
    for cred in cred_map.get("custom", []):
        for reqd in required_custom_fields:
            if reqd not in cred:
                raise CredentialMapError(
                    f"Required custom credential {reqd} is missing"
                )

        if cred["inventory_filter"] not in dir(inventory_filters):
            raise CredentialMapError(
                f"Invalid inventory filter {cred['inventory_filter']}"
            )

        if cred["inventory_filter"] in seen_filters:
            raise CredentialMapError("Inventory filter values must be unique!")

        new_cred = {
            "inventory_filter": getattr(inventory_filters, cred["inventory_filter"]),
            "username": cred.get("username", output["defaults"]["username"]),
            "password": cred.get("password", output["defaults"]["password"]),
            "mapper": getattr(credentials, cred["mapper"]),
        }

        if "enable" in cred:
            new_cred["enable"] = cred["enable"]

        output["custom"].append(new_cred)
    globals()["AGADOR"]["CRED_MAP"] = resolve_credentials(output)


def resolve_envs(input_str: str) -> str:
    """
    Takes an input string and searches for all instances of '${ENV_VAR}', replacing
    ENV_VAR with the value in the .env file. Raises an exception
    if the ENV_VAR is not found
    """
    for m in re.finditer(r"\${(\w+)}", input_str):
        var = m.group(1)
        try:
            input_str = re.sub(r"\${" + var + "}", agador_cfg(var), input_str)
        except UndefinedValueError:
            raise ValueError(f"Invalid env var {m.group(1)} in {input_str}")

    return input_str


def resolve_credentials(cred_map):
    """
    Resolving all credentials in the cred map based on their
    mapper functions
    """

    # first we need to resolve all the credentials in the map
    _resolve_cred(cred_map["defaults"])
    for custom_cred in cred_map["custom"]:
        _resolve_cred(custom_cred)

    return cred_map


def _resolve_cred(cred):
    """
    Resolves enable and password fields in the credential map using the specified mapper
    """
    if "password" in cred:
        cred["password"] = cred["mapper"](cred["password"])

    if "enable" in cred:
        cred["enable"] = cred["mapper"](cred["enable"])
