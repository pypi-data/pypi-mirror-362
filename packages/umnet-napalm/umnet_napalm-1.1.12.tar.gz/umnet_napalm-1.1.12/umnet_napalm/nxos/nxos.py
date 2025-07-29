from typing import List, Dict
import re
import logging

from napalm.nxos_ssh import NXOSSSHDriver
from napalm.base.helpers import textfsm_extractor
from napalm.base.models import FactsDict

from ..base import UMnetNapalmError, UMnetNapalm
from ..models import (
    RouteDict,
    MPLSDict,
    IPInterfaceDict,
    VNIDict,
    InventoryDict,
    LagInterfaceDict,
)
from ..utils import age_to_integer

logger = logging.getLogger(__name__)


class NXOS(UMnetNapalm, NXOSSSHDriver):
    """
    NXOS Parser
    """

    LABEL_VALUE_MAP = {
        "No": [],
        "Pop": ["pop"],
    }

    # for nexus we're going to map the 'description' provided by
    # show inventory to the type
    INVENTORY_TO_TYPE = {
        # note we're using the fact that this dict gets evaluated
        # sequentially to catch the linecards, whose descriptions are varied
        # but all end in 'Module'
        r"Fabric Module": "fabric_module",
        r"Fabric card": "fabric_module",  # N7K fabric modules in umd
        r"Fabric Extender": None,  # FEXes in Dearborn
        r"N2K-C2": "stack_member",  # FEXes in Dearborn
        r"Eth\s?Mod": None,  # chassis for fixed config Nexus
        r"Supervisor Module": "re",
        r"Fan Module": "fan",
        r"Module": "linecard",
        r"System Controller": None,
        r"Chassis": None,
        r"Power Supply": "psu",
    }

    I_ABBRS = {
        "Lo": "loopback",
        "Po": "port-channel",
        "Eth": "Ethernet",
    }

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        if not optional_args:
            optional_args = {}
        optional_args["read_timeout_override"] = timeout
        super().__init__(hostname, username, password, timeout, optional_args)

    def get_config(self) -> str:
        """
        Returns the running config
        """
        return self._send_command("show running-config")

    def get_active_routes(self) -> List[RouteDict]:
        """
        Parses 'sh ip route detail vrf all'
        """

        parsed_routes = []

        raw_routes = self._send_command("show ip route detail vrf all")
        routes = textfsm_extractor(self, "sh_ip_route_detail_vrf_all", raw_routes)

        for route in routes:
            # skip 'broadcast' and 'local' routes, we don't really care about these
            if route["protocol"] in ["broadcast", "local"]:
                continue

            # "learned from" is one of the keys in our route table that determines
            # uniqueness, as such we need to make sure it's set. Usually it's
            # the IP of the advertising router, but for local/direct/static it should
            # get set to 'self'
            if route["nh_ip"]:
                learned_from = route["nh_ip"]
            elif route["protocol"] in ["direct", "local", "vrrp", "static"]:
                learned_from = "self"
            else:
                raise UMnetNapalmError(f"Could not determine learned from for {route}")

            parsed_routes.append(
                {
                    "vrf": route["vrf"],
                    "prefix": route["prefix"],
                    "nh_interface": route["nh_interface"],
                    "learned_from": learned_from,
                    "protocol": route["protocol"],
                    "age": age_to_integer(route["age"]),
                    "nh_ip": route["nh_ip"],
                    "mpls_label": [route["label"]] if route["label"] else [],
                    "vxlan_vni": int(route["vni"]) if route["vni"] else None,
                    "vxlan_endpoint": route["nh_ip"],
                    "nh_table": (
                        "default" if route["label"] or route["vni"] else route["vrf"]
                    ),
                }
            )

        return parsed_routes

    def get_facts(self) -> FactsDict:
        """
        Cleans up model number on napalm get_facts
        """

        results = super().get_facts()

        model = results["model"]
        m = re.match(r"Nexus(3|9)\d+ (\S+) (\(\d Slot\) )*Chassis$", model)

        # some models have the "N9K" or "N3K already in them, some don't.
        if m and re.match(r"N\dK", m.group(2)):
            results["model"] = m.group(2)
        elif m:
            results["model"] = f"N{m.group(1)}K-{m.group(2)}"

        return results

    def get_mpls_switching(self) -> List[MPLSDict]:
        """
        parses show mpls into a dict that outputs
        aggregate labels and
        """
        output = []

        raw_entries = self._send_command("show mpls switching detail")
        entries = textfsm_extractor(self, "sh_mpls_switching_detail", raw_entries)

        for entry in entries:
            # for aggregate labels the next hop is the VRF
            nh_interface = entry["vrf"] if entry["vrf"] else entry["nh_interface"]
            output.append(
                {
                    "in_label": entry["in_label"],
                    "out_label": self._parse_label_value(entry["out_label"]),
                    "fec": entry["fec"] if entry["fec"] else None,
                    "nh_ip": entry["nh_ip"],
                    "nh_interface": nh_interface,
                    "rd": entry["rd"],
                    "aggregate": bool(entry["vrf"]),
                }
            )

        return output

    def get_inventory(self) -> List[InventoryDict]:
        """
        Parses "show inventory" and "show interface transciever"
        """

        raw_inventory = self._send_command("show inventory")
        inventory = textfsm_extractor(self, "sh_inventory", raw_inventory)

        output = []
        for entry in inventory:
            inventory_type = self._get_inventory_type(entry["desc"])
            if not inventory_type:
                continue

            output.append(
                {
                    "type": inventory_type,
                    "name": entry["name"],
                    "part_number": entry["pid"],
                    "serial_number": entry["sn"],
                }
            )

        raw_trans = self._send_command("show interface transceiver")
        trans = textfsm_extractor(self, "sh_int_transceiver", raw_trans)
        for entry in trans:
            
            if "AOC" in entry["type"]:
                db_type = "aoc"
            elif "DAC" in entry["type"]:
                db_type = "dac"
            else:
                db_type = "optic"

            output.append(
                {
                    "type": db_type,
                    "subtype": entry["type"],
                    "name": entry["interface"],
                    "part_number": entry["pn"],
                    "serial_number": entry["sn"],
                }
            )

        return output

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        """
        Parses "show ip interface vrf all", "show ip dhcp relay address",
        and uses the napalm get_interfaces to get IP interface information
        """
        output = []

        raw_interfaces = self._send_command("show ip interface vrf all")
        ip_interfaces = textfsm_extractor(
            self, "sh_ip_interface_vrf_all", raw_interfaces
        )

        raw_helpers = self._send_command("show ip dhcp relay address")
        helpers = textfsm_extractor(self, "sh_ip_dhcp_relay_address", raw_helpers)

        phy_interfaces = super().get_interfaces()

        for i in ip_interfaces:
            phy_i = phy_interfaces.get(i["interface"], {})

            output.append(
                {
                    "ip_address": f"{i['ip_address']}/{i['prefixlen']}",
                    "interface": self._abbr_i(i["interface"]),
                    "description": phy_i.get("description", ""),
                    "mtu": int(i["mtu"]),
                    "admin_up": (i["admin_state"] == "admin-up"),
                    "oper_up": (i["protocol_state"] == "protocol-up"),
                    "vrf": i["vrf"],
                    "secondary": bool(i["secondary"]),
                    "helpers": [
                        h["address"]
                        for h in helpers
                        if h["interface"] == i["interface"]
                    ],
                }
            )

        raw_ipv6_interfaces = self._send_command("show ipv6 interface vrf all")
        ipv6_interfaces = textfsm_extractor(
            self, "sh_ipv6_interface_vrf_all", raw_ipv6_interfaces
        )

        for i in ipv6_interfaces:
            phy_i = phy_interfaces.get(i["interface"], {})
            output.append(
                {
                    "ip_address": f"{i['ipv6_address']}",
                    "interface": self._abbr_i(i["interface"]),
                    "description": phy_i.get("description", ""),
                    "mtu": int(i["mtu"]),
                    "admin_up": (i["admin_state"] == "admin-up"),
                    "oper_up": (i["protocol_state"] == "protocol-up"),
                    "vrf": i["vrf"],
                    "secondary": False,
                    "helpers": [],
                }
            )

        return output

    def get_vni_information(self) -> List[VNIDict]:
        """
        Runs "show nve vni" to get vni info
        """
        output = []
        raw_vnis = self._send_command("show nve vni")
        vnis = textfsm_extractor(self, "sh_nve_vni", raw_vnis)

        for vni in vnis:
            output.append(
                {
                    "vni": vni["vni"],
                    "mcast_group": (
                        None if vni["mcast_grp"] == "n/a" else vni["mcast_grp"]
                    ),
                    "vrf": vni["bd_vrf"] if vni["type"] == "L3" else None,
                    "vlan_id": (
                        vni["bd_vrf"]
                        if vni["type"] == "L2" and vni["bd_vrf"] != "UC"
                        else None
                    ),
                },
            )

        return output

    def get_lag_interfaces(self) -> Dict[str, LagInterfaceDict]:
        """
        Parses 'show port-channel summary' and 'show vpc brief'
        """
        raw_output = self._send_command("show port-channel summary")
        output = textfsm_extractor(self, "sh_portchannel_summary", raw_output)

        lag_interfaces = {}
        for line in output:
            if line["lag_name"] not in lag_interfaces:
                lag_interfaces[line["lag_name"]] = {
                    "oper_up": "D" not in line["lag_flags"],
                    "admin_up": True,  # don't see member admin state in 'show etherchannel summ'
                    "protocol": (
                        line["protocol"] if line["protocol"] != "-" else "Static"
                    ),
                    "mlag_id": 0,
                    "peer_link": False,
                    "members": {},
                }

            lag = lag_interfaces[line["lag_name"]]

            for member in ["m1", "m2", "m3"]:
                member_name = line[f"{member}_name"]
                member_flags = line[f"{member}_flags"]
                if not member_name:
                    continue

                lag["members"][member_name] = {
                    "oper_up": "P" in member_flags,
                    "admin_up": True,
                    "flags": member_flags,
                }

        # show vpc brief will set the MLAG ID and peer link fields
        raw_output = self._send_command("show vpc brief")
        output = textfsm_extractor(self, "sh_vpc_brief", raw_output)

        for line in output:
            if line["lag_name"] not in lag_interfaces:
                raise UMnetNapalmError(
                    f"Invalid LAG {line['lag_name']} parsed from show vpc brief"
                )

            lag = lag_interfaces[line["lag_name"]]

            if line["peer_link_id"]:
                lag["peer_link"] = True

            elif line["vpc_id"]:
                lag["mlag_id"] = int(line["vpc_id"])

        return lag_interfaces
