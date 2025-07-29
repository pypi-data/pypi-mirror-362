from ..credentials.cyberark import Cyberark
from ..utils import agador_cfg


def plaintext(cred: str) -> str:
    """
    Plain text mapper returns cred as is
    """
    return cred


def cyberark_umnet(cred: str) -> str:
    """
    Looks up a credential in the cyberark UMnet environment
    """
    c = Cyberark(env_file=agador_cfg("CYBERARK_ENV_FILE"), environment="UMNET")
    return c.query_cyberark(cred)


def cyberark_nso(cred: str) -> str:
    """
    Looks up a credential in the cyberark NSO environment
    """
    c = Cyberark(env_file=agador_cfg("CYBERARK_ENV_FILE"), environment="NSO")
    return c.query_cyberark(cred)
