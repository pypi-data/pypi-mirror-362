from typing import Optional, Dict, List, Union, Any
import socket
import re
from ipaddress import ip_network, ip_interface

from napalm.base import NetworkDriver
from napalm.base.helpers import textfsm_extractor
from napalm.base.netmiko_helpers import netmiko_args
from napalm.base.exceptions import ConnectionClosedException
import napalm.base.models as napalm_models


from ..base import UMnetNapalm
from .. import models
from ..utils import abbr_interface, age_to_integer


class ASA(UMnetNapalm, NetworkDriver):
    """
    Netmiko-based napalm class for pulling data from an ASA.

    Note this assumes that for multi-context devices, you are logging in as an
    'admin' that has access to all the contexts.
    """

    PROTOCOL_ABBRS = {
        "L": "local",
        "C": "connected",
        "S": "static",
        "B": "BGP",
        "V": "VPN",
    }

    IGNORE_INTERFACES = [
        r"Internal-Data",
    ]

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
        optional_args["read_timeout_override"] = timeout
        self.netmiko_optional_args = netmiko_args(optional_args)

        self._multi_context = None
        self._contexts = []
        self._running_config = {}

    def open(self):
        """
        Netmiko open
        """
        device_type = "cisco_asa"
        self.device = self._netmiko_open(
            device_type, netmiko_optional_args=self.netmiko_optional_args
        )

    def close(self):
        """
        Netmiko close
        """
        self._netmiko_close()

    def cli(
        self, commands: List[str], encoding="text", context="all", flatten_results=False
    ) -> Dict[str, Union[str, Dict[str, Any]]]:
        """
        Executes an arbitrary list of commands and returns as a dict
        mapping the executed command to its result.
        """
        return {
            cmd: self._send_command(cmd, context, flatten_results) for cmd in commands
        }

    def _send(self, command):
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

    def _send_command(
        self, command, context="all", flatten_result=False
    ) -> Union[dict, str]:
        """
        If the device is multi-context, sends the command
        to all the contexts doing a 'changeto' in between each one.

        If flatten_result is true it will return one long string
        with '!!!! changeto {context} !!!!' added between each context's output.

        Otherwise it will return the results as a dict of strings
        keyed on the context names

        If this is a non-context device, it will always return a string
        with the main context data
        """
        if not self.contexts:
            return self._send(command)

        if context == "all":
            contexts = self.contexts
        elif context in self.contexts:
            contexts = [context]
        else:
            raise ValueError(f"Invalid context {context}")

        results = {}
        for c in contexts:
            self._send(f"changeto context {c}")
            results[c] = self._send(command)

        if flatten_result:
            return self._flatten_result(results)

        return results

    def _flatten_result(self, results: dict[str]) -> str:
        """
        Flattens result for multi-context into a single string output
        delineated with '!!!! CONTEXT {c} !!!!!'
        """
        if isinstance(results, str):
            return results

        return "\n".join(
            [
                f"\n!!!!!!!! CONTEXT {c} !!!!!!!!\n\n" + result
                for c, result in results.items()
            ]
        )

    def _parse_dhcp_relay(self, context: str) -> dict[str, dict[str, list[str]]]:
        """
        Parses dhcp relay config from the running config.
        Results returned as a nested dict mapping context -> ifname -> relay IPs
        """

        if context and self.multi_context:
            configs = self.get_config(context=context, flatten_result=False)
        elif self.multi_context:
            configs = self.get_config(context="all", flatten_result=False)
        else:
            configs = {"default": self.get_config()}

        relays = {}
        for context, config in configs.items():
            relays[context] = {}
            parsed = textfsm_extractor(self, "dhcprelay", config)

            # entries with 'interface' are for a specific interface
            # if there's an entry with a blank 'interface' that is a global
            # mapping of relays to ifnames
            for entry in parsed:
                if entry["interface"]:
                    relays[context][entry["ifname"][0]] = entry["relays"]
                else:
                    for ifname in entry["ifname"]:
                        if ifname not in relays[context]:
                            relays[context][ifname] = entry["relays"]
        return relays

    @property
    def multi_context(self) -> bool:
        """
        Uses 'show version' output to determine if this is a multi-context
        ASA or not
        """
        if self._multi_context is None:
            result = self._send("show version | inc Adaptive Security Appliance")
            self._multi_context = bool(re.search(r"<(context|system)>", result))

        return self._multi_context

    @property
    def contexts(self) -> list:
        """
        Returns a list of contexts
        """
        if self.multi_context and not self._contexts:
            self._send("changeto system")
            context = self._send("show context")
            for line in context.split("\n"):
                m = re.match(r"[\*\s](\S+)\s+", line)
                if m:
                    self._contexts.append(m.group(1))

        return self._contexts

    def get_config(self, context: str = "all", flatten_result=True) -> dict[str]:
        """
        Returns the running config.
        """

        # pulling config from contexts that we haven't pulled yet
        to_get = self.contexts if context == "all" else [context]
        for c in to_get:
            if c not in self._running_config:
                self._running_config[c] = self._send_command("show running-config", c)[
                    c
                ]

        # returning result based on what the user asked for
        if context == "all" and flatten_result:
            return self._flatten_result(self._running_config)
        elif context == "all":
            return self._running_config
        else:
            return self._running_config[context]

    def get_facts(self) -> napalm_models.FactsDict:
        """
        Processes "show version" into napalm facts dict
        """

        show_version = self._send("show version")

        facts = {
            "os_version": "",
            "uptime": 0,
            "interface_list": [],
            "vendor": "cisco",
            "serial_number": "",
            "model": "",
            "hostname": "",
            "fqdn": "",
        }
        # Since most of the data isn't in a table-like format it
        # feels more straightforward to parse line-by-line than use a textFSM template
        for line in show_version.split("\n"):
            # 'Cisco Adaptive Security Appliance Software Version 9.12(4)67'
            m = re.match(
                r"Cisco Adaptive Security Appliance Software Version (\S+)( <(context|system)>)?",
                line,
            )
            if m:
                facts["os_version"] = m.group(1)
                if m.group(2):
                    self._multi_context = True
                continue

            # 'UMVPN4-NCASDN up 216 days 15 hours'
            m = re.match(r"(\S+) up (.+)$", line)
            if m:
                facts["hostname"] = m.group(1)
                facts["uptime"] = age_to_integer(m.group(2))
                continue

            # 'Hardware:   FPR4K-SM-12, 56209 MB RAM, CPU Xeon E5 series ....'
            m = re.match(r"Hardware:\s+(\S+),", line)
            if m:
                facts["model"] = m.group(1)
                continue

            # '4099: Int: Internal-Data0/0    : address is 0015.a500.01bf, irq 11'
            # '4101: Int: Internal-Data0/1    : address is 0015.a500.01ff, irq 10'
            m = re.match(r"\s*\d+: (Int|Ext): (\S+)\s*:", line)
            if m:
                facts["interface_list"].append(m.group(2))
                continue

            # 'Serial Number: FLM21510821'
            m = re.match(r"Serial Number: (\w+)$", line)
            if m:
                facts["serial_number"] = m.group(1)
                continue

        return facts

    def get_ip_interfaces(self, context: str = "all") -> List[models.IPInterfaceDict]:
        """
        Does 'show interfaces' and extracts layer 3 output.
        The 'description' field is the 'nameif' name.
        For multi-context ASAs the context is stored as the vrf.
        """

        sh_interface = self._send_command("show interface detail", context=context)

        # normalize output for single context devices
        if isinstance(sh_interface, str):
            sh_interface = {"default": sh_interface}

        # dhcp relay must be parsed from running config
        relays = self._parse_dhcp_relay(context)

        results = []
        for context, raw_output in sh_interface.items():
            output = textfsm_extractor(self, "sh_interface_detail", raw_output)
            for row in output:
                if not row["ip"] or self._ignore_interface(row["interface"]):
                    continue

                results.append(
                    {
                        "ip_address": str(
                            ip_interface(f"{row['ip']}/{row['netmask']}")
                        ),
                        "interface": abbr_interface(row["interface"]),
                        "description": row["ifname"],
                        "mtu": row["mtu"] if row["mtu"] else 0,
                        "admin_up": row["admin_state"] != "administratively down",
                        "oper_up": row["oper_state"] == "up",
                        "vrf": context,
                        "secondary": False,
                        "helpers": relays[context].get(row["ifname"], []),
                    }
                )
        return results

    def get_arp_table(self, vrf: str = "") -> List[napalm_models.ARPTableDict]:
        """
        Does show arp and translates to ARPTableDict
        {"interface": str, "mac": str, "ip": str, "age": float}

        Providing a 'vrf' will limit to a particular context.
        """

        # if no VRF is provided we want all contexts
        vrf = vrf if vrf else "all"

        # napalm arp output isn't vrf/context aware so we can flatten it
        # into one output string
        sh_arp = self._send_command("show arp", context=vrf, flatten_result=True)
        output = textfsm_extractor(self, "sh_arp", sh_arp)

        results = []
        for row in output:
            results.append(
                {
                    "interface": row["interface"],
                    "mac": row["mac"],
                    "ip": row["ip"],
                    "age": float(row["age"]),
                }
            )

        return results

    def get_active_routes(self, context: str = "all") -> List[models.RouteDict]:
        """
        Parses "show route". The 'vrf' field is the context name
        """
        sh_route = self._send_command("show route", context=context)

        # normalizing data for single-context ASA
        if isinstance(sh_route, str):
            sh_route = {"default": sh_route}

        results = []
        for context, raw_output in sh_route.items():
            output = textfsm_extractor(self, "sh_route", raw_output)
            for row in output:
                protocol = self._parse_protocol_abbr(row["protocol"])

                learned_from = "self"
                nh_interface = row["nh_interface"]

                if protocol in ["Local", "Connected", "VPN"]:
                    nh_interface = "self"

                # note that in general, for BGP, assuming the next hop IP is also the advertising
                # router is not a good idea. However, in our particular environment it is a solid assumption.
                # to really know we'd have to parse through 'show bgp' and that's more effort
                # than it's worth.
                elif protocol == "BGP":
                    learned_from = row["nh_ip"]

                prefix = ip_network(f"{row['subnet']}/{row['netmask']}")
                results.append(
                    {
                        "vrf": context,
                        "prefix": str(prefix),
                        "nh_interface": nh_interface,
                        "learned_from": learned_from,
                        "protocol": protocol,
                        "age": age_to_integer(row["age"]),
                        "nh_table": context,
                        "nh_ip": row["nh_ip"],
                        "mpls_label": [],
                        "vxlan_vni": None,
                        "vxlan_endpoint": None,
                    }
                )

        return results

    def get_inventory(self) -> List[models.InventoryDict]:
        """
        No command to show inventory on asa :(
        """
        return []

    def get_lag_interfaces(self) -> Dict[str, models.LagInterfaceDict]:
        """
        No command on ASA for this
        """
        return {}
