from .nxos.nxos import NXOS
from .ios.ios import IOS
from .junos.junos import Junos
from .panos.panos import PANOS

from .iosxr.iosxr import IOSXR
from .asa.asa import ASA

PLATFORM_MAP = {
    "ios": IOS,
    "nxos_ssh": NXOS,
    "junos": Junos,
    "panos": PANOS,
    #    "iosxr_netconf": IOSXRNetconf,
    "iosxr": IOSXR,
    "asa": ASA,
}


def get_network_driver(platform: str):
    """
    Returns network driver based on platform string.
    """
    for valid_platform, driver in PLATFORM_MAP.items():
        if valid_platform == platform:
            return driver

    raise NotImplementedError(f"Unsupported platform {platform}")
