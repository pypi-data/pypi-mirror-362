from typing import Optional, Dict, Any
import ipaddress
from email.message import EmailMessage
import smtplib
import re

from git import Repo

from nornir.core.inventory import Host


class AgadorError(Exception):
    pass


def is_ip_address(ip: str) -> bool:
    """
    Returns whether a string is an IP (eg 10.233.0.10 or fe80::1)
    """
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    return True


def is_ip_or_prefix(ip: str) -> bool:
    """
    Returns whether a string is an ip (10.233.0.10) or
    IP + prefix (10.233.0.10/24). IPv6 works as well.
    """
    try:
        ipaddress.ip_interface(ip)
    except ValueError:
        return False
    return True


def agador_cfg(var: str) -> Any:
    """
    Looks up an agador config setting
    """
    try:
        from .loaders import AGADOR
    except ImportError:
        raise AgadorError(
            "Agador settings not loaded from file - run loaders/apply_config_settings first!"
        )

    return AGADOR.get(var, None)


def validate_email_list(input_str: str):
    """
    Makes sure that the input string is a comma-separated list
    of email addresses. Fun fact - the 'local' part of the email address
    can have a super wide range of characters, so we're just checking for non-whitespace
    The domain can have a-zA-Z0-9 and -, so we can be a bit more circumspect there.

    Function does nothing but throw an exception if the email is invalid
    """
    for email in re.split(r",", input_str):
        if not re.match(r"\S+@[\w\-.]+\.\w+$", email):
            raise ValueError(f"Invalid email {email}")


def git_update(repo_path: str, commit_message: str):
    """
    Updates git repo and if applicable, the remote origin.
    Will overwrite origin.
    """
    repo = Repo(repo_path)
    repo.git.status()

    repo.git.add(all=True)
    repo.index.commit(commit_message)
    try:
        origin = repo.remote(name="origin")
    except ValueError:
        origin = None

    if origin:
        origin.push()


def get_device_cmd_list(
    cmd_map: dict, host: Host, cmd_list_filter: Optional[list] = None
) -> Dict[str, str]:
    """
    Gets list of commands tied to a device based on its
    host inventory data. Optionally provide a list of commands to
    restrict the output to.

    Returns a dict mapping the agador command to the umnet_napalm getter
    """
    cmd_list = {}
    for cmd, data in cmd_map.items():
        if cmd_list_filter and cmd not in cmd_list_filter:
            continue

        if not data.get("inventory_filter") or data["inventory_filter"](host):
            cmd_list[cmd] = data["getter"]

    return cmd_list


def send_email(email_from: str, email_to: str, subject: str, message: str):
    """
    Sends an email via smtp.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_from
    msg["To"] = email_to
    msg.set_content(message)

    with smtplib.SMTP("localhost") as s:
        s.send_message(msg)
