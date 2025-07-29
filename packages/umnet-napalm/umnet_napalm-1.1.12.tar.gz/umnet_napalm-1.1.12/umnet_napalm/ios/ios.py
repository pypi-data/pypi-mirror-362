import re
from typing import List, Dict
from ipaddress import ip_network
import logging

from napalm.ios import IOSDriver
from napalm.base.helpers import textfsm_extractor
import napalm.base.models as napalm_models

from ..models import (
    RouteDict,
    MPLSDict,
    InventoryDict,
    IPInterfaceDict,
    LagInterfaceDict,
)
from ..base import UMnetNapalmError, UMnetNapalm
from ..utils import age_to_integer

IOS_LABEL_VALUES = {
    "": [],
    "No Label": [],
    "Pop Label": ["pop"],
}

logger = logging.getLogger(__name__)


class IOS(UMnetNapalm, IOSDriver):
    """
    IOS Parser
    """

    LABEL_VALUE_MAP = {
        "": [],
        "No Label": [],
        "Pop Label": ["pop"],
    }

    INVENTORY_TO_TYPE = {
        # weird one-offs we care about
        r"4500X-16 10GE": "stack_member",  # umd core vss "stack_member"
        r"10/100BaseTX \(RJ45\)V? with 48 10/100 baseT": "linecard",  # linecard in 4500 chassis
        # re
        r"Supervisor": "re",

        # linecard
        r"10GE SFP\+":"linecard", #d-mon-asb-1 'Linecard(slot 2)'
        r"10/100/1000BaseT": "linecard", #s-ssw-b832p-3
        r"^WS-X": "linecard",
        r"Async Serial NIM": "linecard",  # ISR NIM
        r"Eth Mod": "linecard",
        r"[HV]WIC": "linecard",
        r"DIMM": "linecard",
        r"Fan": "fan",
        r"[Pp]ower [Ss]upply": "psu",
        r"RPS": "psu",
        r"Uplink Module": "uplink_module",
        r"FRULink": "uplink_module",
        r"gigabit ethernet port adapter": "uplink_module",
        r"(WS-C[234]|C9[23]00)": "stack_member",
        r"StackPort": "stack_cable",
        r"StackAdapter": "stack_cable",

        # optic matches are last since they're loose
        r"Interface Adapter": "optic",
        r"TwinGig": "optic",
        r"Converter Module": "optic",
        r"Transceiver": "optic",
        r"SFP": "optic",
        r"1000[Bb]ase": "optic",
        r"10G[Bb]ase": "optic",
        r"^GE": "optic",  # r-ipflex 'GE LX'
        r"GigabitEthernet\d/\d port adapter": "optic", # s-nccomm-1241t-1
        
        # items we want to ignore
        r"WS-F": None,  # forwarding card
        r"Daughterboard": None,  # daughterboard
        r"daughtercard": None,
        r"Policy Feature Card": None,
        r"Clock": None,
        r"Mux Buffers": None,
        # 'chassis'
        r"([Cc]hassis|CHASSIS)": None,
        r"c(92|93|36)xx": None,  # duplicate 'chassis' entry
        r"C1000": None,  # AV C1000 chassis
        r"Cisco [Cc]atalyst c2950 switch": None,  # s-vaughn-252c-1 c2950
        r"Cisco [Cc]atalyst 3550": None,  # s-nccomm-1241t-1
        r"Cisco Systems, Inc. WS-C4500X-16 2 slot switch": None,  # umd core vss sup entry
        r"Cisco 3900 ISR": None,  # r-sipgw-seb-1
        r"^ME-3800X": None,
        r"Stacking Module": None,  # replaceable stacking module in 2960X
        # terminal server components we don't care about
        r"terminal server": None,
        r"Built-In NIM controller": None,
        r"Front Panel 2 ports Gigabitethernet Module": None,
        r"(Route|Forwarding) Processor": None,
        r"VTT-E": None, # Voltage termination module? s-macc-11w-a-1 (ancient 6509)
    }

    I_ABBRS = {
        "Lo": "Loopback",
        "Po": "Port-channel",
        "Fa": "FastEthernet",
        "Ge": "GigabitEthernet",
        # longer matches must go first!
        "Twe": "TwentyFiveGigE",
        "Tw": "TwoGigabitEthernet",
        "Te": "TenGigabitEthernet",
        "Vl": "Vlan",
    }

    PROTOCOL_ABBRS = {
        "L": "local",
        "C": "connected",
        "S": "static",
        "i": "ISIS",
        "B": "BGP",
        "O": "OSPF",
    }

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        if not optional_args:
            optional_args = {}
        optional_args["read_timeout_override"] = timeout

        super().__init__(hostname, username, password, timeout, optional_args)

        self._i_descrs = None

    def _parse_label_value(self, label) -> list:
        """
        Parses mpls label value into normalized data
        """
        if label in IOS_LABEL_VALUES:
            return IOS_LABEL_VALUES[label]

        return [label]

    def _get_route_labels(self) -> Dict[tuple, str]:
        """
        Runs "show bgp vpnv4 unicast labels" and parses the result.

        The output is a dictionary with (vrf, prefix) as key
        and the outbound label as a value, eg
        output[ ("vrf_VOIP_NGFW", "0.0.0.0/0") ] = "12345"
        """

        raw_labels = self._send_command("show bgp vpnv4 unicast all labels")
        labels = textfsm_extractor(self, "sh_bgp_vpnv4_unicast_all_labels", raw_labels)

        # default route shows up as '0.0.0.0' so we have to munge that
        output = {}
        for label in labels:
            prefix = "0.0.0.0/0" if label["prefix"] == "0.0.0.0" else label["prefix"]
            output[(label["vrf"], ip_network(prefix))] = label["out_label"]

        return output

    @property
    def i_descrs(self):
        """
        Pulls interface descriptions into an internal data structure
        """

        if self._i_descrs is None:
            raw_output = self._send_command("show interface description")
            output = textfsm_extractor(self, "sh_interface_description", raw_output)
            self._i_descrs = {o["interface"]: o["description"] for o in output}
        return self._i_descrs

    def get_config(self) -> str:
        """
        Gets the running config and returns it as plain text
        """
        return self._send_command("show running-config")

    def get_facts(self) -> napalm_models.FactsDict:
        """
        Overriding napalm 'get facts' because it returns the whole string for
        os version (eg Cisco IOS Software .+) instead of just the version number like we want
        https://github.com/napalm-automation/napalm/issues/469
        """
        show_version = self._send_command("show version")
        show_hosts = self._send_command("show hosts")

        output = {
            "os_version": "Unknown",
            "uptime": 0.0,
            "interface_list": list(self.i_descrs.keys()),
            "vendor": "Cisco",
            "serial_number": "Unknown",
            "model": "Unknown",
            "hostname": "Unknown",
            "fqdn": "Unknown",
        }

        for line in show_version.split("\n"):
            # version
            m = re.match(
                r"(Cisco IOS Software|IOS \(tm\)).+Version ([0-9\.\(\)A-Za-z]+)", line
            )
            if m:
                output["os_version"] = m.group(2)
                continue

            # uptime and hostname are conveniently on one line
            # example: s-arbl3-2536-6 uptime is 6 weeks, 14 hours, 31 minutes
            m = re.search(r"(\S+) uptime is (.*)", line)
            if m:
                output["hostname"] = m.group(1)
                output["uptime"] = age_to_integer(m.group(2))
                continue

            # model, regex adapted from parent method
            # example: cisco C9300-48UXM (X86) processor with 1309193K/6147K bytes of memory.
            m = re.search(r"[Cc]isco (\S+).+bytes of memory", line)
            if m:
                output["model"] = m.group(1)
                continue

            # S/N
            m = re.match(r"Processor board ID ([A-Z0-9]+)", line)
            if m:
                output["serial_number"] = m.group(1)
                continue

        # domain name is in 'show hosts'
        m = re.search(r"Default domain is (\S+)", show_hosts)
        if m and output["hostname"] != "Unknown":
            output["fqdn"] = f"{output['hostname'].lower()}.{m.group(1)}"

        return output

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        """
        Parses 'show ip interface' and 'show ipv6 interface'
        """
        raw_output = self._send_command("show ip interface")
        output = textfsm_extractor(self, "sh_ip_interface", raw_output)

        ip_interfaces = []
        for i in output:
            i_data = {
                "ip_address": i["ip"],
                "interface": i["interface"],
                "description": self.i_descrs.get(self._abbr_i(i["interface"]), ""),
                "mtu": int(i["mtu"]) if i["mtu"] else None,
                "admin_up": i["admin_state"] != "administratively down",
                "oper_up": i["oper_state"] == "up",
                "vrf": i["vrf"] if i["vrf"] else "default",
                "secondary": False,
                "helpers": set(i["helpers"]) if i["helpers"] else [],
            }
            ip_interfaces.append(i_data)

            for sec_i in i["sec_ip"]:
                sec_data = i_data.copy()
                sec_data["ip_address"] = sec_i
                sec_data["secondary"] = True

                ip_interfaces.append(sec_data)

        raw_output = self._send_command("show ipv6 interface")
        output = textfsm_extractor(self, "sh_ipv6_interface", raw_output)

        for i in output:
            for ip in i["ip"]:
                ip_interfaces.append(
                    {
                        "ip_address": ip,
                        "interface": i["interface"],
                        "description": self.i_descrs.get(
                            self._abbr_i(i["interface"]), ""
                        ),
                        "mtu": int(i["mtu"]) if i["mtu"] else None,
                        "admin_up": i["admin_state"] != "administratively down",
                        "oper_up": i["oper_state"] == "up",
                        "vrf": i["vrf"] if i["vrf"] else "default",
                        # IPv6 secondary and helpers not relevant in our environment
                        "secondary": False,
                        "helpers": [],
                    }
                )

        return ip_interfaces

    def get_active_routes(self) -> List[RouteDict]:
        """
        Parses "show ip route vrf *" for IOS. Will also run
        "show bgp vpnv4 unicast labels" to get label bindings
        """

        output = []

        raw_routes = self._send_command("show ip route vrf *")
        routes = textfsm_extractor(self, "sh_ip_route_vrf_all", raw_routes)

        for route in routes:
            logger.info(f"found proto {route['proto_1']} for route {route}")
            protocol = self._parse_protocol_abbr(route["proto_1"])

            # "learned from" is one of the keys in our route table that determines
            # uniqueness, as such we need to make sure it's set. Usually it's
            # the IP of the advertising router, but for local/direct/static it should
            # get set to 'self'
            if route["nh_ip"]:
                learned_from = route["nh_ip"]
            elif protocol in ["local", "connected", "static"]:
                learned_from = "self"
            else:
                raise UMnetNapalmError(f"Could not determine learned from for {route}")

            output.append(
                {
                    "vrf": route["vrf"] if route["vrf"] else "default",
                    "prefix": route["prefix"],
                    "nh_interface": route["nh_interface"],
                    "learned_from": learned_from,
                    "protocol": self._parse_protocol_abbr(route["proto_1"]),
                    "age": age_to_integer(route["age"]),
                    "nh_ip": route["nh_ip"],
                    "mpls_label": None,
                    "vxlan_vni": None,
                    "vxlan_endpoint": None,
                    "nh_table": route["vrf"] if route["vrf"] else "default",
                }
            )

        return output

    def get_inventory(self) -> list[InventoryDict]:
        """
        Parses "show inventory" for IOS
        """
        raw_inventory = self._send_command("show inventory")
        inventory = textfsm_extractor(self, "sh_inventory", raw_inventory)

        output = []
        for entry in inventory:
            inventory_type = self._get_inventory_type(entry["desc"])

            if not inventory_type:
                continue

            name = re.sub(r"^(\d+)$", r"Slot \g<1>", entry["name"])
            name = re.sub(r"^Transceiver (\S+)", r"\g<1>", name)

            # pulling optic type out of description field, which is messy and ugly
            subtype = re.sub(r"^\S+ Transceiver (\S+) \S+", r"\g<1>", entry["desc"])
            output.append(
                {
                    "name": name,
                    "type": inventory_type,
                    "subtype": subtype if inventory_type == "optic" else None,
                    "part_number": entry["pid"],
                    "serial_number": entry["sn"],
                }
            )

        return output

    def get_mpls_switching(self) -> List[MPLSDict]:
        """
        Parses "show mpls forwarding table" for IOS
        """
        raw_labels = self._send_command("show mpls forwarding-table")
        labels = textfsm_extractor(self, "sh_mpls_forwarding_table", raw_labels)

        output = []
        for entry in labels:
            # extract RD from 'FEC'
            m = re.match(r"([\d\.]+:\d+):(\d+.\d+.\d+.\d+\/\d+)", entry["fec"])
            if m:
                rd = m.group(1)
                fec = m.group(2)
            else:
                rd = None
                fec = entry["fec"]

            aggregate = bool(entry["vrf"])
            nh_interface = entry["vrf"] if entry["vrf"] else entry["nh_interface"]

            output.append(
                {
                    "in_label": entry["in_label"],
                    "fec": fec,
                    "out_label": self._parse_label_value(entry["out_label"]),
                    "nh_ip": entry["nh_ip"],
                    "nh_interface": nh_interface,
                    "rd": rd,
                    "aggregate": aggregate,
                }
            )

        return output

    def get_lag_interfaces_old(self) -> Dict[str, LagInterfaceDict]:
        """
        Parses "show etherchannel detail"
        """
        raw_output = self._send_command("show etherchannel detail")
        output = textfsm_extractor(self, "sh_etherchannel_detail", raw_output)

        # template has two distinct sets of fields, one for lags
        # and the other for members. First we'll initialize our parent class
        groups = [line for line in output if line["lag_name"]]
        members = [line for line in output if line["member_name"]]

        lag_interfaces = {}
        for line in groups:
            lag_interfaces[line["lag_name"]] = {
                "admin_up": "Down" not in line["lag_state"],
                "oper_up": "Ag-Inuse" in line["lag_state"],
                "protocol": line["lag_proto"] if line["lag_proto"] != "-" else "Static",
                "mlag_id": 0,  # no vpc/mlag for ios
                "members": {},
            }

        for line in members:
            group_name = f"Po{line['member_group']}"
            if group_name not in lag_interfaces:
                raise UMnetNapalmError(
                    f"Unknown LAG group {group_name} for member {line['member_name']}"
                )

            lag_interfaces[group_name]["members"][line["member_name"]] = {
                "admin_up": True,  # don't see member admin state in 'show etherchannel detail'
                "oper_up": line["member_state"] == "Up",
                "flags": line["member_flags"].strip(),
            }

        return lag_interfaces

    def get_lag_interfaces(self) -> Dict[str, LagInterfaceDict]:
        """
        Parses "show etherchannel summary"
        """
        raw_output = self._send_command("show etherchannel summary")
        output = textfsm_extractor(self, "sh_etherchannel_summary", raw_output)

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

            for member in ["m1", "m2"]:
                member_name = line[f"{member}_name"]
                member_flags = line[f"{member}_flags"]
                if not member_name:
                    continue

                lag["members"][member_name] = {
                    "oper_up": "P" in member_flags,
                    "admin_up": True,
                    "flags": member_flags,
                }

        return lag_interfaces
