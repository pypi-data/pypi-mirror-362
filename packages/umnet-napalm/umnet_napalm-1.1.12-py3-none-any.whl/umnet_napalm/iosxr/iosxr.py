from typing import Optional, Dict, List, Union, Any
import socket
import re

from napalm.base import NetworkDriver
from napalm.base.helpers import textfsm_extractor
from napalm.base.netmiko_helpers import netmiko_args
from napalm.base.exceptions import ConnectionClosedException
import napalm.base.models as napalm_models


from ..base import UMnetNapalm, UMnetNapalmError
from ..models import RouteDict, IPInterfaceDict, InventoryDict, LagInterfaceDict
from ..utils import age_to_integer


class IOSXR(UMnetNapalm, NetworkDriver):
    """
    Netmiko-based napalm class for pulling data from an IOS-XR device.
    """

    PROTOCOL_ABBRS = {
        "L": "local",
        "C": "connected",
        "S": "static",
        "i": "ISIS",
        "B": "BGP",
        "O": "OSPF",
    }

    I_ABBRS = {
        "Lo": "Loopback",
        "BE": "Bundle-Ether",
        "Hu": "HundredGigE",
        "Te": "TenGigE",
        "Mg": "MgmtEth",
        "FH": "FourHundredGigE",
    }

    INVENTORY_TO_TYPE = {
        r"Fan Tray": "fan",
        r"Pluggable": "optic",
        r"Line Card": "linecard",
        r"Route Processor": "re",
        r"Fabric Card": "fabric_module",
        r"System Controller": None,
        r"Chassis": None,
        r"Power Supply": "psu",
    }

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        timeout: int = 60,
        optional_args: Optional[Dict] = None,
    ) -> None:
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        self.device = None

        optional_args = optional_args if optional_args else {}
        optional_args["read_timeout_override"] = timeout
        self.netmiko_optional_args = netmiko_args(optional_args)

        self._i_descrs = None

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

    def _send_command(self, command):
        """
        This is a copy of "_send_command" from the napalm ios driver
        """
        try:
            if isinstance(command, list):
                for cmd in command:
                    output = self.device.send_command(cmd)
                    if "% Invalid" not in output:
                        break
            else:
                output = self.device.send_command(command)
            return output
        except (socket.error, EOFError) as e:
            raise ConnectionClosedException(str(e))

    def open(self):
        """
        Netmiko open
        """
        device_type = "cisco_xr"
        self.device = self._netmiko_open(
            device_type, netmiko_optional_args=self.netmiko_optional_args
        )

    def close(self):
        """
        Netmiko close
        """
        self._netmiko_close()

    def cli(
        self, commands: List[str], encoding="text"
    ) -> Dict[str, Union[str, Dict[str, Any]]]:
        """
        Executes an arbitrary list of commands and returns as a dict
        mapping the executed command to its result.
        """
        return {cmd: self._send_command(cmd) for cmd in commands}

    def get_config(self) -> str:
        """
        returns the running config
        """
        return self._send_command("show running-config")

    def get_facts(self) -> napalm_models.FactsDict:
        """
        Processes "show version" into napalm facts dict
        """

        facts = {
            "os_version": "",
            "uptime": 0,
            "interface_list": self.i_descrs.keys(),
            "vendor": "cisco",
            "serial_number": "",
            "model": "",
            "hostname": "",
            "fqdn": "",
        }

        # show version has os version, hostname, and uptime
        show_version = self._send_command("show version detail")
        for line in show_version.split("\n"):
            m = re.match(r"Cisco IOS XR Software, Version (\S+)$", line)
            if m:
                facts["os_version"] = m.group(1)
                continue

            m = re.match(r"(\S+) System uptime is (.+)$", line)
            if m:
                facts["hostname"] = m.group(1)
                facts["uptime"] = age_to_integer(m.group(2))
                continue

        # show inventory chassis has model and serial number
        show_inv_chassis = self._send_command("admin show inventory chassis")
        for line in show_inv_chassis.split("\n"):
            m = re.match(r"\s+PID: (\S+).+SN: (\S+)", line)
            if m:
                facts["model"] = m.group(1)
                facts["serial_number"] = m.group(2)

        return facts

    # def get_config(
    #     self,
    #     retrieve: str = "all",
    #     full: bool = False,
    #     sanitized: bool = False,
    #     format: str = "text",
    # ) -> napalm_models.ConfigDict:
    #     """retrieves configuration"""

    #     if sanitized:
    #         raise UMnetNapalmError("Sanitized config not supported")

    #     if format != "text":
    #         raise UMnetNapalmError("Only text config format supported")

    #     # running config and startup config are the same
    #     results = {"running": "", "startup": "", "candidate": ""}
    #     if retrieve in ["all", "running", "startup"]:
    #         config = self._send_command("show running-config")

    #         if retrieve in ["all", "running"]:
    #             results["running"] = config
    #         if retrieve in ["all", "startup"]:
    #             results["startup"] = config

    #     # candidate config is only valid if we're in config mode
    #     if retrieve in ["all", "candidate"] and self.device.check_config_mode():
    #         results["candidate"] = self._send_command("show configuration merge")

    #     return results

    def get_lldp_neighbors(self) -> Dict[str, List[napalm_models.LLDPNeighborDict]]:
        """
        Parses show lldp neighbors - doing "show lldp neighbors detail" beacuse otherwise
        the hostname gets cut off
        """
        raw_output = self._send_command("show lldp neighbors detail")
        output = textfsm_extractor(self, "sh_lldp_neighbors_detail", raw_output)

        neighs = {}
        for neigh in output:
            if neigh["local_port"] not in neighs:
                neighs[neigh["local_port"]] = []

            neighs[neigh["local_port"]].append(
                {"hostname": neigh["name"], "port": neigh["port"]}
            )
        return neighs

    def get_lldp_neighbors_detail(
        self, interface: str = ""
    ) -> napalm_models.LLDPNeighborsDetailDict:
        """ "
        Parses show lldp neighbors detail
        """

        raw_output = self._send_command("show lldp neighbors detail")
        output = textfsm_extractor(self, "sh_lldp_neighbors_detail", raw_output)

        neighs = {}
        for neigh in output:
            if interface and neigh["local_port"] != interface:
                continue

            if neigh["local_port"] not in neighs:
                neighs[neigh["local_port"]] = []

                neighs[neigh["local_port"]].append(
                    {
                        "parent_interface": "",
                        "remote_chassis_id": neigh["chassis_id"],
                        "remote_system_name": neigh["name"],
                        "remote_port": neigh["port"],
                        "remote_port_description": neigh["port_descr"],
                        "remote_system_description": neigh["descr"],
                        "remote_system_capab": neigh["capab"].split(","),
                        "remote_system_enable_capab": neigh["enable_capab"].split(","),
                    }
                )
        return neighs

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        """
        Parses "show ip interface and show ipv6 interface"
        """
        raw_ip_output = self._send_command("show ip interface")
        output = textfsm_extractor(self, "sh_ip_interface", raw_ip_output)

        ip_interfaces = []

        # ipv4 processing - primary IP is in 'ip' field,
        # secondaries are a list
        for i in output:
            i_data = {
                "ip_address": i["ip"],
                "interface": i["interface"],
                "description": self.i_descrs.get(self._abbr_i(i["interface"]), ""),
                "mtu": int(i["mtu"]) if i["mtu"] else 0,
                "admin_up": i["admin_state"] != "Shutdown",
                "oper_up": i["oper_state"] == "Up",
                "vrf": i["vrf"],
                "secondary": False,
                # CSCsw65449: iosxr does not show helpers even if they are configured
                "helpers": [],
            }
            ip_interfaces.append(i_data)

            for sec_ip in i["sec_ip"]:
                sec_data = i_data.copy()
                sec_data["ip_address"] = sec_ip
                sec_data["secondary"] = True

                ip_interfaces.append(i_data)

        raw_ip6_output = self._send_command("show ipv6 interface")
        ip6_output = textfsm_extractor(self, "sh_ipv6_interface", raw_ip6_output)

        for i in ip6_output:
            for ip in i["ip"]:
                ip_interfaces.append(
                    {
                        "ip_address": ip,
                        "interface": i["interface"],
                        "description": self.i_descrs.get(
                            self._abbr_i(i["interface"]), ""
                        ),
                        "mtu": int(i["mtu"]) if i["mtu"] else 0,
                        "admin_up": i["admin_state"] != "Shutdown",
                        "oper_up": i["oper_state"] == "Up",
                        "vrf": i["vrf"],
                        "secondary": False,
                        "helpers": [],
                    }
                )

        return ip_interfaces

    def get_arp_table(self) -> List[napalm_models.ARPTableDict]:
        """
        Parses "show arp ; show arp vrf all"
        """
        raw_output = self._send_command("show arp ; show arp vrf all")
        output = textfsm_extractor(self, "sh_arp", raw_output)

        entries = []
        for entry in output:
            entries.append(
                {
                    "interface": entry["interface"],
                    "mac": entry["mac"],
                    "ip": entry["ip"],
                    "age": entry["age"] if entry["age"] != "-" else "",
                }
            )

        return entries

    def get_active_routes(self) -> List[RouteDict]:
        """
        Parses "show route"
        """
        raw_output = self._send_command("sh route afi-all ; show route vrf all afi-all")
        # raw_output = self._send_command("show route vrf all afi-all")
        output = textfsm_extractor(self, "sh_route", raw_output)
        routes = []
        for entry in output:
            routes.append(
                {
                    "vrf": entry["vrf"] if entry["vrf"] else "default",
                    "prefix": entry["prefix"],
                    "nh_interface": entry["nh_interface"],
                    "learned_from": entry["nh_ip"] if entry["nh_ip"] else "self",
                    "protocol": self._parse_protocol_abbr(entry["proto_1"]),
                    "age": age_to_integer(entry["age"]),
                    "nh_table": entry["nh_vrf"],
                    "nh_ip": entry["nh_ip"],
                    "mpls_label": None,
                    "vxlan_vni": None,
                    "vxlan_endpoint": None,
                },
            )

        return routes

    def get_inventory(self) -> List[InventoryDict]:
        """
        Parses "show invetory"
        """
        raw_output = self._send_command("show inventory")
        output = textfsm_extractor(self, "sh_inventory", raw_output)

        inventory = []
        for entry in output:
            inv_type = self._get_inventory_type(entry["desc"])
            if not inv_type:
                continue

            inventory.append(
                {
                    "name": entry["name"],
                    "type": inv_type,
                    "part_number": entry["pid"],
                    "serial_number": entry["sn"],
                }
            )

        return inventory

    def get_lag_interfaces(self) -> Dict[str, LagInterfaceDict]:
        """
        Parses 'show bundle'
        """
        raw_output = self._send_command("show bundle")
        output = textfsm_extractor(self, "sh_bundle", raw_output)

        lag_interfaces = {}

        for entry in output:
            if entry["lag_name"] not in lag_interfaces:
                lag_interfaces[entry["lag_name"]] = {
                    "admin_up": entry["lag_oper_state"] != "Admin down",
                    "oper_up": entry["lag_oper_state"] == "Up",
                    "protocol": (
                        "LACP" if entry["lacp_state"] == "Operational" else "Static"
                    ),
                    "mlag_id": (
                        int(entry["iccp_grp"]) if entry["iccp_grp"] else 0
                    ),  # best guess, don't have this in our environment
                    "peer_link": False,  # Don't have this in our environment so not sure how to test it
                    "members": {},
                }

            # not all LAGs have members
            if not entry["member_name"]:
                continue

            lag = lag_interfaces[entry["lag_name"]]
            lag["members"][entry["member_name"]] = {
                "oper_up": entry["member_state"] == "Active",
                "admin_up": entry["member_state"] != "shutdown",
            }

        # flags need to be pulled from 'show lacp
        raw_output = self._send_command("show lacp")
        output = textfsm_extractor(self, "sh_lacp", raw_output)
        for entry in output:
            if (
                entry["lag_name"] not in lag_interfaces
                or entry["member_name"]
                not in lag_interfaces[entry["lag_name"]]["members"]
            ):
                raise UMnetNapalmError(
                    f"Invalid lag {entry['lag_name']} for {entry['member_name']}"
                )

            lag_interfaces[entry["lag_name"]]["members"][entry["member_name"]][
                "flags"
            ] = entry["flags"]

        return lag_interfaces
