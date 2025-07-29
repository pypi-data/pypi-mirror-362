from typing import Union
from datetime import timedelta
import re
import logging
import sys
from ipaddress import ip_network, ip_interface, ip_address
from ipaddress import (
    IPv4Address,
    IPv6Address,
    IPv4Interface,
    IPv6Interface,
    IPv4Network,
    IPv6Network,
)
import json
from typing import List
from copy import deepcopy
from .models import RouteDict


# eventually want to pull this from a more central place
# as we've defined it in so many places already
INTERFACE_ABBRS = {
    # ios
    "Fastethernet": "Fa",
    "GigabitEthernet": "Gi",
    "TwoGigabitEthernet": "Tw",
    "TenGigabitEthernet": "Te",
    "TwentyFiveGigE": "Twe",
    "Port-channel": "Po",
    "Loopback": "Lo",
    # nxos
    "Ethernet": "Eth",
    "port-channel": "Po",
    "loopback": "Lo",
    "Management": "Mgmt",
}


class UMnetNapalmJsonEncoder(json.JSONEncoder):
    """
    custom json encoder that handles types
    in our results that aren't encodable by default.
    Reference the "Extending JSONEncoder" section of: https://docs.python.org/3/library/json.html

    Currently ipaddress and timedelta types are the only non-encodable
    types among the results
    """

    def default(self, obj):
        if isinstance(
            obj,
            (
                IPv4Address,
                IPv6Address,
                IPv4Interface,
                IPv6Interface,
                IPv4Network,
                IPv6Network,
                timedelta,
            ),
        ):
            return str(obj)

        return super().default(obj)


def abbr_interface(interface: str) -> str:
    """
    Converts long version of interface name to short one
    if applicable
    """
    for long, short in INTERFACE_ABBRS.items():
        if interface.startswith(long):
            return interface.replace(long, short)

    return interface


def age_to_integer(age: str) -> Union[int, None]:
    """
    Across platforms age strings can be:
    10y5w, 5w4d, 05d04h, 01:10:12, 3w4d 01:02:03,
    50 days 10 hours (ASA)
    """

    # convert empty string to none
    if age == "":
        return None

    # integer age is seconds - we don't need further parsing
    # if we got an integer value
    m = re.search(r"^\d+$", age)
    if m:
        return int(age)

    # Extracting digits out of different time strings
    TIME_MATCHES = [
        r"(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)",
        r"(?P<years>\d+) years?",
        r"(?P<months>\d+) months?",
        r"(?P<weeks>\d+) weeks?",
        r"(?P<days>\d+) days?",
        r"(?P<hours>\d+) hours?",
        r"(?P<minutes>\d+) minutes?",
        r"(?P<years>\d+)y",
        r"(?P<weeks>\d+)w",
        r"(?P<days>\d+)d",
        r"(?P<hours>\d+)h",
    ]
    # Multipliers for different units
    UNIT_TO_SECONDS = {
        "years": 31536000,
        "months": 2628000,
        "weeks": 604800,
        "days": 86400,
        "hours": 3600,
        "minutes": 60,
        "seconds": 1,
    }

    seconds = 0

    # search for every time match regex. If  a match is found
    # extract data, apply multiplier, and add to our seconds total
    for match in TIME_MATCHES:
        m = re.search(match, age)
        if not m:
            continue

        for unit, multiplier in UNIT_TO_SECONDS.items():
            if unit in m.groupdict():
                seconds += int(m.groupdict()[unit]) * multiplier

    return seconds


def resolve_nh(nh_ip: str, nh_table: str, routes: List[RouteDict]) -> List[RouteDict]:
    """
    Given a next hop IP and next hop table, search a list of
    routes for that next hop and return LPMs that have a next hop
    interface
    """
    nh_routes = [
        r
        for r in routes
        if r["vrf"] == nh_table
        and r["prefix"].version == ip_network(nh_ip).version
        and r["prefix"].supernet_of(ip_network(nh_ip))
        and r["nh_interface"]
    ]

    if not nh_routes:
        return []

    nh_routes.sort(key=lambda x: x["prefix"].prefixlen, reverse=True)

    # the first entry is a longest prefix match because of our sort,
    # but with ECMP there could be more than one!
    # we'll peel routes off the front with matching lengths to find
    # the rest.
    lpms = [nh_routes[0]]
    if len(nh_routes) > 1:
        for nh_route in nh_routes[1::]:
            if nh_route["prefix"].prefixlen == nh_routes[0]["prefix"].prefixlen:
                lpms.append(nh_route)

    return lpms


def resolve_all_nhs(routes: List[RouteDict], raise_on_error=False) -> List[RouteDict]:
    """
    Goes through a list of routes and resolves the interface for any
    next hops that don't already have them listed.
    """
    output = []
    for route in routes:
        if route["nh_interface"]:
            output.append(route)
            continue

        # attempt to resolve next hop
        nh_table = (
            "default" if route["mpls_label"] or route["vxlan_vni"] else route["vrf"]
        )
        nh_lpms = resolve_nh(route["nh_ip"], nh_table, routes)
        if not nh_lpms and raise_on_error:
            raise LookupError(f"Could not resolve next hop for {route}")

        # for every lpm found create an entry in our table for this recursive
        # route
        for lpm in nh_lpms:
            resolved = deepcopy(route)
            resolved["nh_ip"] = lpm["nh_ip"]
            resolved["nh_interface"] = lpm["nh_interface"]
            resolved["mpls_label"].extend(lpm["mpls_label"])
            output.append(resolved)

    return output


def str_to_type(string: str) -> object:
    """
    Converts string output to obvious types.
    empty quote is converted to "None".
    ip_address, ip_interface, and ip_network are converted to their appropriate objecst
    integers are converted to int
    """
    if string in ["", "None"]:
        return None
    if re.match(r"^\d+$", string):
        return int(string)

    for ip_type in [ip_network, ip_interface, ip_address]:
        try:
            return ip_type(string)
        except ValueError:
            pass

    return string


LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.WARNING,
    "CRITICAL": logging.CRITICAL,
}
LOG_FORMAT = "%(asctime)-15s  %(levelname)8s %(name)s %(message)s"


def configure_logging(
    log_level: Union[int, str],
    log_globally: bool = False,
    log_file: str = None,
    log_to_console: bool = False,
):
    """
    Configures logging for the module, or globally as indicated by the input
    """

    if log_globally:
        logger = logging.getLogger()
    else:
        module_name = __name__.split(".")[0]
        logger = logging.getLogger(module_name)

    if isinstance(log_level, str):
        log_level = LOG_LEVELS[log_level.upper()]
    logger.setLevel(log_level)

    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=1024 * 1024 * 10, backupCount=20
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)

    if log_to_console:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(stdout_handler)
