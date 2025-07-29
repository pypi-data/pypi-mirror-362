import os
import re
import socket
from datetime import datetime
from git import Repo
from typing import Union
import logging
import pynetbox

from nornir.core.inventory import Host
from ..utils import agador_cfg

logger = logging.getLogger(__name__)


class SaveResult:
    """
    Generic "take nornir getter result and save it to a file" class
    """

    def __init__(self, destination: str):
        self._base_dir = destination

    def _get_hostname(self, netbox_name: str) -> str:
        """
        Removes stack member prefix from netbox hostnames
        """
        return re.sub(r"_\d$", "", netbox_name)

    def _set_output_file(self, host: Host) -> str:
        """
        Uses nornir host role data to determine sub-folder
        and ensures its created at the right path
        """
        role = host.data["device_role"]["slug"]
        if not os.path.exists(f"{self._base_dir}/{role}"):
            os.makedirs(f"{self._base_dir}/{role}")

        return f"{self._base_dir}/{role}/{self._get_hostname(host.name)}"

    def _git_update(self):
        """
        Updates git repo and if applicable, the remote origin.
        Will overwrite origin.
        """
        repo = Repo(self._base_dir)

        repo.git.add(all=True)

        formatted_date = datetime.strftime(datetime.now(), "%a %d %b %Y, %I:%M%p")
        commit_msg = f"Agador backup from {socket.gethostname()} at {formatted_date}"
        commit = repo.index.commit(commit_msg)
        logger.info(f"Committing {self._base_dir}: {commit}")
        try:
            origin = repo.remote(name="origin")
        except ValueError:
            logger.info("No origin found - skipping push")
            origin = None

        if origin:
            result = origin.push(force=True)
            urls = ",".join([u for u in origin.urls])
            summary = ",".join([r.summary for r in result])
            logger.info(f"Pushed to {urls}: {summary}")

    def write_to_file(self, host: Host, result: Union[dict, list]):
        """
        Saves data to file. Override in child classes if a
        different type of transformation needs to happen
        """
        if isinstance(result, dict):
            result = [result]
        with open(self._set_output_file(host), "w", encoding="utf-8") as fh:
            fh.write(",".join(result[0].keys()) + "\n")

            for row in result:
                values = [str(r) for r in row]
                fh.writelines(",".join(values) + "\n" for r in result)

    def post_processing(self):
        """
        Function that runs after all files are updated (post nornir run)
        """
        self._git_update()


class SaveConfig(SaveResult):
    """
    Saves running config from "get_config" to a file, redacting
    out passwords
    """

    def __init__(self, destination: str):
        super().__init__(destination)

        logger.debug(f"Checking for {self._base_dir}/obsolete")
        if not os.path.exists(f"{self._base_dir}/obsolete"):
            logger.debug("creating obsolete")
            os.makedirs(f"{self._base_dir}/obsolete")

    def write_to_file(self, host: Host, result: str):
        with open(self._set_output_file(host), "w", encoding="utf-8") as fh:
            for line in result.split("\n"):
                # ios - ignore ntp clock period
                if re.match(r"ntp clock-period", line):
                    continue

                # nxos - ignore current time statement
                if re.match(r"Time:", line):
                    continue

                # iosxr date at top of file, format:
                # Tue May 13 00:00:34.586 EDT
                # Tue May  7 00:00:34.586 EDT
                if re.match(
                    r"[A-Z][a-z]{2} [A-Z][a-z]{2}\s{1,2}\d{1,2} \d{2}:\d{2}:\d{2}.\d{3} [A-Z]{3}$",
                    line,
                ):
                    continue

                # cisco type 7 password redaction
                if re.search(r"(password|key) 7", line):
                    line = "!!!" + re.sub(
                        r"(password|key) 7 \S+", r"\g<1> [redacted]", line
                    )

                # juniper type 9 password redaction
                if re.search(r"(secret|password) \"$9$", line):
                    line = "#" + re.sub(
                        r"(secret|password) \S+", r"\g<1> [redacted]", line
                    )

                fh.write(f"{line}\n")

    def post_processing(self):
        """
        Moves files for devices that are no longer listed in netbox as
        'active' to the 'retired' folder
        """
        logger.debug(f"Starting post processing for save_config in {self._base_dir}")

        roles = [
            r for r in os.listdir(self._base_dir) if not re.match(r"(\.|obsolete)", r)
        ]
        nb = pynetbox.api(agador_cfg("NB_URL"), token=agador_cfg("NB_TOKEN"))

        for role in roles:
            logger.debug(f"Processing role file {role}")

            role_dir = f"{self._base_dir}/{role}"
            nb_devices = [
                d.name for d in nb.dcim.devices.filter(role=role, status="active")
            ]

            for cfg_file in os.listdir(role_dir):
                if cfg_file not in nb_devices:
                    logger.debug(f"Moving {cfg_file} to obsolete directory")
                    os.rename(
                        f"{role_dir}/{cfg_file}",
                        f"{self._base_dir}/obsolete/{cfg_file}",
                    )

        super().post_processing()
