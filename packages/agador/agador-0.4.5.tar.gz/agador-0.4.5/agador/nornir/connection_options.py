import logging
import re

from nornir.core import Nornir
from nornir.core.inventory import ConnectionOptions

logger = logging.getLogger(__name__)

GLOBAL_TIMEOUT = 300

# maps firewalls to panorama instances. Note that the firewall name is assumed
# to be the name of the device in netbox
PANOS_FW_MAP = {
    "fw-dpss-1": "panorama-test.miserver.it.umich.edu",
    "fw-dpss-2": "panorama-test.miserver.it.umich.edu",
    "ngfw-1": "panorama-1.umnet.umich.edu",
    "ngfw-2": "panorama-1.umnet.umich.edu",
    "fw-umd-1": "panorama-1.umnet.umich.edu",
    "fw-umd-2": "panorama-1.umnet.umich.edu",
    "fw-umddc-1": "panorama-1.umnet.umich.edu",
    "fw-umddc-2": "panorama-1.umnet.umich.edu",
}


def configure_connection_options(nr: Nornir):
    """
    Applies custom connection options that make sense for our environment
    """

    for d in nr.inventory.hosts.values():
        if "umnet_napalm" not in d.connection_options:
            d.connection_options["umnet_napalm"] = ConnectionOptions(extras={})
        extras = d.connection_options["umnet_napalm"].extras

        # Setting our read timeouts. BIN routers and DNs take a long time so setting a very
        # large timeout for those
        if re.match(r"(bin-|d-\w+dn-)", d.name):
            extras["timeout"] = 7200
        else:
            extras["timeout"] = GLOBAL_TIMEOUT

        # for panorama-managed firewalls we needd to set the 'hostname' to be panorama,
        # the 'password' must be set as the api key, and the 'serial' must be saved as
        # an optional argument
        if d.name in PANOS_FW_MAP:
            optional_args = extras.get("optional_args", {})
            optional_args["api_key"] = d.password
            optional_args["serial"] = d.data["serial"]
            optional_args["panorama"] = PANOS_FW_MAP[d.name]
            extras["optional_args"] = optional_args
