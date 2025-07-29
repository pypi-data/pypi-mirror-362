import xml.etree.ElementTree as ET
from typing import List, Dict
import re

import xmltodict

from napalm.base import NetworkDriver
import napalm.base.models as napalm_models
from napalm.base.exceptions import ConnectionException
import pan.xapi

from umnet_napalm.models import (
    IPInterfaceDict,
    RouteDict,
    InventoryDict,
    LagInterfaceDict,
)
from ..base import UMnetNapalm, UMnetNapalmError
from .utils import parse_system_state
from ..utils import age_to_integer


PANOS_ROUTING_PROTOCOLS = {
    "H": "local",
    "C": "connected",
    "S": "static",
    "B": "BGP",
    "R": "RIP",
    "O": "OSPF",
    "Oi": "OSPF intra-area",
    "Oo": "OSPF inter-area",
    "O2": "OSPF External Type 2",
    "O1": "OSPF External Type 1",
}


class PANOS(UMnetNapalm, NetworkDriver):
    """
    PANOS Parser
    """

    # maps the 'type' field in slots/entry returned by 'show chassis inventory'
    # to our standard types
    INVENTORY_TO_TYPE = {
        "power": "psu",
        "slot": "linecard",
        "fan": "fan",
    }

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        self.device = None

        self.api_key = optional_args.get("api_key", "")
        self._effective_running_config = None
        self._system_state = None

        self.serial = None
        if optional_args:
            self.serial = optional_args.get("serial")
            self.panorama = optional_args.get("panorama")

    def open(self):
        """PANOS version of `open` method, see NAPALM for documentation."""
        try:
            hostname = self.panorama if self.panorama else self.hostname

            if self.api_key:
                self.device = pan.xapi.PanXapi(
                    hostname=hostname, api_key=self.api_key, serial=self.serial
                )
            else:
                self.device = pan.xapi.PanXapi(
                    hostname=hostname,
                    api_username=self.username,
                    api_password=self.password,
                    serial=self.serial,
                )

        except ConnectionException as exc:
            raise ConnectionException(str(exc))

    def close(self):
        """PANOS version of `close` method, see NAPALM for documentation."""
        self.device = None

    def _config_search(self, xpath: str, no_cache: bool = False) -> list:
        """
        Does an xpath search of the effective running config and returns the results.
        """
        cfg = self._get_effective_running_config(no_cache=no_cache)
        return cfg.findall(xpath)

    def _get_effective_running_config(self, no_cache: bool = False) -> ET:
        """
        Gets effective running config and saves it to the local object
        """
        if self._effective_running_config is None or no_cache:
            result = self._send_command(
                "<show><config><effective-running></effective-running></config></show>"
            )
            self._effective_running_config = ET.fromstring(result)

        return self._effective_running_config

    def _get_system_state(self, no_cache: bool = False) -> dict:
        """
        runs 'show system state' and parses the returned pseudo-json into structured output
        """
        if not self._system_state or no_cache:
            raw_result = self._send_command("<show><system><state/></system></show>")
            result = xmltodict.parse(raw_result)["response"]["result"]
            self._system_state = parse_system_state(result)

        return self._system_state

    def _get_mtu_and_comment(self, interface: ET) -> dict:
        """
        Looks up mtu and comment on a particular interface or subinterface
        object. Returns a dict with mtu and comment key/value pairs
        """
        results = {"mtu": 0, "comment": ""}

        # subinterfaces have mtu set at their same level.
        # for non-subinterfaces it is set under "layer3"
        if "." in interface.attrib["name"]:
            mtu = interface.find("./mtu")
        else:
            mtu = interface.find("./layer3/mtu")

        if mtu is not None:
            results["mtu"] = mtu.text

        comment = interface.find("./comment")
        if comment is not None:
            results["comment"] = comment.text

        return results

    def _get_interface_mtus_and_comments(self) -> dict:
        """
        Looks through the effective running config at network/interface for MTU configurations
        and descriptions, aka "comments"
        returns a dict keyed on interface names, with
        dict vaules, eg results[interface_name] = {'mtu':mtu, and 'comment': comment }
        """

        interfaces = self._config_search(".//network/interface/ethernet/entry")

        # for logical interfaces we only care about the subints
        interfaces.extend(
            self._config_search(".//network/interface/tunnel/units/entry")
        )
        interfaces.extend(
            self._config_search(".//network/interface/loopback/units/entry")
        )

        results = {}
        # looping over all the ethernet interfaces
        for interface in interfaces:
            results[interface.attrib["name"]] = self._get_mtu_and_comment(interface)

            # subinterfaces
            for subint in interface.findall("./layer3/units/entry"):
                results[subint.attrib["name"]] = self._get_mtu_and_comment(subint)

        return results

    def _send_command(self, cmd: str) -> str:
        """
        Send XML command to PANOS and get result
        """
        self.device.op(cmd=cmd)
        return self.device.xml_root()

    def get_facts(self) -> napalm_models.FactsDict:
        """
        Parses 'show system info'
        """
        result = self._send_command("<show><system><info/></system></show>")
        sys_info = xmltodict.parse(result)["response"]["result"]["system"]

        return {
            "os_version": sys_info["sw-version"],
            "uptime": age_to_integer(sys_info["uptime"]),
            "interface_list": [],  # we don't care about this
            "vendor": "Palo Alto",
            "serial_number": sys_info["serial"],
            "model": sys_info["model"],
            "hostname": sys_info["hostname"],
            "fqdn": "NA",
        }

    def get_config(self) -> str:
        """
        We just want the effective running config
        """
        return self._send_command(
            "<show><config><effective-running></effective-running></config></show>"
        )

    def get_inventory(self) -> List[InventoryDict]:
        """
        Digs through "show chassis inventory" and "show system state" to pull out linecard and optics information
        """
        # need access to a chassis PAN to implement "show chassis inventory"
        result = self._send_command("<show><chassis><inventory/></chassis></show>")
        inventory = ET.fromstring(result)

        output = []

        # modules
        for entry in inventory.findall(".//slots/entry"):
            if entry.find("model").text in ["empty", "Not Present"]:
                continue

            inventory_type = self._get_inventory_type(entry.find("type").text)
            if not inventory_type:
                continue

            name = entry.find("slot").text
            name = re.sub(r"^(\d+)$", r"Slot \g<1>", name)

            output.append(
                {
                    "type": inventory_type,
                    "name": name,
                    "part_number": entry.find("model").text,
                    "serial_number": entry.find("serial").text,
                }
            )

        # optics data is in system state
        raw_result = self._send_command(
            "<show><system><state><filter>sys.s*.p*.phy</filter></state></system></show>"
        )
        data = parse_system_state(raw_result)

        for phy_name, phy_data in data.items():
            # skip unpopulated ports
            # if re.match(r'(CAT|-Empty$)', phy_data["media"]):
            if not phy_data.get("sfp"):
                continue

            # the 'phy name' is in the format 'sys.sX.pY.phy' which translates to 'EthernetX/Y'
            m = re.match(r"sys.s(\d+).p(\d+).phy$", phy_name)
            i_name = f"Ethernet{m.group(1)}/{m.group(2)}"

            output.append(
                {
                    "type": "optic",
                    "name": i_name,
                    "part_number": phy_data["sfp"]
                    .get("vendor-part-number", "")
                    .strip(),
                    "serial_number": phy_data["sfp"]
                    .get("vendor-serial-number", "")
                    .strip(),
                    "parent": "",
                }
            )

        return output

    def get_arp_table(self) -> List[napalm_models.ARPTableDict]:
        """
        Queries the arp table
        """
        result = self._send_command("<show><arp><entry name = 'all'/></arp></show>")
        arp_table = xmltodict.parse(result)["response"]["result"]

        timeout = int(arp_table["timeout"])

        output = []
        for entry in arp_table["entries"]["entry"]:
            output.append(
                {
                    "interface": entry["interface"],
                    "mac": entry["mac"],
                    "ip": entry["ip"],
                    "age": timeout - int(entry["ttl"]),
                },
            )

        return output

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        """
        napalm_panos doesn't support "get_routing_instances".
        While we could implement that function and combine it with "get_interfaces_ip" and
        "get_interfaces", it's simpler to just run "show interface all" to get most of what we need.

        Note that MTU is in 'system state' so we have to parse it out of there.
        """

        # "show interface all" gives us most of what we need here
        result = self._send_command("<show><interface>all</interface></show>")
        interfaces = xmltodict.parse(result)["response"]["result"]

        hw_interfaces_by_name = {i["name"]: i for i in interfaces["hw"]["entry"]}
        mtus_and_comments = self._get_interface_mtus_and_comments()

        l3_interfaces = []
        for l3_i in interfaces["ifnet"]["entry"]:
            if l3_i["ip"] == "N/A" and not l3_i["addr6"]:
                continue

            # vrf (aka route-domain) is stored in the 'fwd' attribute
            vrf = None
            if l3_i["fwd"] != "N/A":
                vrf = l3_i["fwd"].replace("vr:", "")

            # look up admin/oper status in 'hw' section of the output
            if "." in l3_i["name"]:
                phy_name = l3_i["name"].split(".")[0]
            else:
                phy_name = l3_i["name"]
            phy = hw_interfaces_by_name.get(phy_name, None)

            # description and mtu came from an xpath query
            mtu_and_desc = mtus_and_comments.get(
                l3_i["name"], {"mtu": 0, "comment": ""}
            )

            # all the non-IP attributes for each IP entry are the same
            l3i_entry = {
                "interface": l3_i["name"],
                "description": mtu_and_desc["comment"],
                "mtu": mtu_and_desc["mtu"] if mtu_and_desc["mtu"] else 1500,
                "admin_up": bool(phy["mode"] != "(power-down)") if phy else None,
                "oper_up": bool(phy["state"] == "up") if phy else None,
                "vrf": vrf,
                # no helpers or secondaries - not currently configured
                # in our environment
                "secondary": False,
                "helpers": [],
            }

            # IPv4 interfaces
            if l3_i["ip"] and l3_i["ip"] != "N/A":
                ipv4_entry = l3i_entry.copy()
                ipv4_entry["ip_address"] = l3_i["ip"]
                l3_interfaces.append(ipv4_entry)

            # IPv6 interfaces are stored as a list, or a string if there's only one
            if l3_i["addr6"]:
                if isinstance(l3_i["addr6"]["member"], str):
                    l3_i["addr6"]["member"] = [l3_i["addr6"]["member"]]

                for ipv6_addr in l3_i["addr6"]["member"]:
                    ipv6_entry = l3i_entry.copy()
                    ipv6_entry["ip_address"] = ipv6_addr
                    l3_interfaces.append(ipv6_entry)

        return l3_interfaces

    def get_active_routes(self) -> List[RouteDict]:
        """
        Gets active routes from all vsyses on the PAN
        """
        result = self._send_command("<show><routing><route/></routing></show>")
        routing = xmltodict.parse(result)

        parsed_routes = []
        for route in routing["response"]["result"]["entry"]:
            # if route isn't active (no A in protocol field), skip it
            if not (route["flags"].startswith("A")):
                continue

            # look at the third character in the flags field to determine
            # protocol - don't really care about the different OSPF types
            if route["flags"][2] not in PANOS_ROUTING_PROTOCOLS:
                raise UMnetNapalmError(
                    f"{self.hostname}: Unknown panos routing protocol {route['flags']}"
                )
            protocol = PANOS_ROUTING_PROTOCOLS[route["flags"][2]]

            # next hops of all zeros indicate local routes
            if route["nexthop"] in ["0.0.0.0", "::"]:
                learned_from = "self"
            else:
                learned_from = route["nexthop"]

            # if this is a local route and we don't have a nh interface, the
            # next hop interface is also 'self' (because it's a host route or a locally-owned IP)
            if learned_from == "self" and not route["interface"]:
                route["interface"] = "self"

            parsed_routes.append(
                {
                    "vrf": route["virtual-router"],
                    "prefix": route["destination"],
                    "nh_interface": route["interface"],
                    "nh_table": route["virtual-router"],
                    "learned_from": learned_from,
                    "protocol": protocol,
                    "age": int(route["age"]) if route["age"] else None,
                    "nh_ip": None if learned_from == "self" else route["nexthop"],
                    "mpls_label": [],
                    "vxlan_vni": None,
                    "vxlan_endpoint": None,
                }
            )

        return parsed_routes

    def get_lag_interfaces(self) -> Dict[str, LagInterfaceDict]:
        """
        parses "show interface interface" and "show lacp aggregate-ethernet all"
        """
        result = self._send_command(
            "<show><lacp><aggregate-ethernet>all</aggregate-ethernet></lacp></show>"
        )
        lacp = ET.fromstring(result)

        lag_interfaces = {}
        for entry in lacp.findall("result/entry"):
            lag_name = entry.attrib.get("name")
            if not lag_name:
                continue

            # 'mode' is Active or Passive, 'rate' is Slow or Fast, and is set
            # at the parent level
            flags = entry.find("mode").text[0] + entry.find("rate").text[0]

            # to get oper status of parent we are going to parse the
            # the members first
            lag_members = {}
            for member in entry.findall("entry"):
                lag_members[member.attrib["name"]] = {
                    "oper_up": member.find("lacp-state") == "active",
                    "admin_up": True,
                    "flags": flags,
                }

            lag_interfaces[lag_name] = {
                # if one of the members is up then the parent is up
                "oper_up": len(
                    [m["oper-up"] for m in lag_members.values() if m["oper_up"]]
                ),
                "admin_up": entry.find("lacp").text == "Enabled",
                "protocol": "LACP",  # only supporting LACP
                "peer_link": False,
                "mlag_id": 0,
                "members": lag_members,
            }

        return lag_interfaces
