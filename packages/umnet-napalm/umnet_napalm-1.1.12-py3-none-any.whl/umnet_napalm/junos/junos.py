# # pylint: disable=no-member
from typing import List, Union, Optional, Dict
import re
from ipaddress import ip_network
import logging

from napalm.junos import JunOSDriver
from napalm.base.models import ARPTableDict, LLDPNeighborDict

from lxml import etree

from ..base import UMnetNapalmError, UMnetNapalm
from ..models import (
    RouteDict,
    MPLSDict,
    InventoryDict,
    IPInterfaceDict,
    LagInterfaceDict,
)
from ..utils import age_to_integer

from . import junos_views

logger = logging.getLogger(__name__)

XCVR_DESC_TO_INTERFACE_PREFIX = {
    r"100GBASE-": "et-",
    r"QSFP": "et-",
    r"SFP28": "et-",
    r"SFP\+": "xe-",
    r"SFP-": "ge-",
    r"CFP-": "et-",
    r"(UNKNOWN|UNSUPPORTED)": "ge-",  # default

}

DEFAULT_ARP_AGING_TIMER = 1200


class Junos(UMnetNapalm, JunOSDriver):
    """
    Junos parser
    """

    # interfaces to ignore when doing 'show ip interfaces'
    IGNORE_INTERFACES = [
        "bme",
        "jsrv",
        "em1",
        "em0",
    ]

    # tables to ignore when doing 'show route'
    IGNORE_ROUTE_TABLES = [
        "bgp.evpn.0",
        "bgp.l3vpn.0",
        "bgp.l3vpn-inet6.0",
        "inet.1",
        "inet.2",
        "inet.3",
        "inet.4",
        "inet6.3",
        "inet6.1",
        "iso.0",
        "mpls.0",
        ":vxlan.inet.0",
        "__default_evpn__.evpn.0",
        "default-switch.evpn.0",
    ]

    # mapping of inventory name regex to their netbox types
    INVENTORY_TO_TYPE = {
        r"Fan Tray": "fan",
        r"(PIC|MIC|FPC)": "linecard",
        r"Xcvr": "optic",
        r"(PEM|Power Supply)": "psu",
        r"Routing Engine": "re",
        # don't care about these inventory items
        r"(CPU|PDM|FPM|Midplane|CB)": None,
    }

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        timeout: int = 60,
        optional_args: Optional[Dict] = None,
    ) -> None:
        super().__init__(hostname, username, password, timeout, optional_args)

        self._running_config = None
        self.arp_aging_timer = DEFAULT_ARP_AGING_TIMER

    def _get_junos_inventory_type(self, name: str, model_number: str) -> str:
        """
        Maps the name and part number of the Junos inventory item to its type
        """
        # "Xcvr" parts are always optics
        if name.startswith("Xcvr"):
            return "optic"

        # non-optic parts should always have a model number, if not
        # we don't care about them
        if not (model_number):
            return None

        # EX switches and virtual chassis save their vc members and uplink modules
        # as FPC X and PIC X - we want to classify those correctly
        if re.match(r"EX[234]", model_number):
            if re.search(r"FPC \d+", name):
                return "stack-member"

            if re.search(r"PIC \d+", name):
                return None

        # uplink modules are also saved under PIC X, must classify based
        # on their model number
        if re.match(r"EX-UM", model_number):
            return "uplink-module"

        # otherwise we want to pattern-match based on the INVENTORY_TO_TYPE
        # dictionary
        return self._get_inventory_type(name)

    def _get_xcvr_interface_prefix(self, xcvr_desc: str) -> str:
        """
        Maps xcvr description from "show chassis hardware" to
        interface prefix
        """
        for pattern, prefix in XCVR_DESC_TO_INTERFACE_PREFIX.items():
            if re.match(pattern, xcvr_desc):
                return prefix

        raise UMnetNapalmError(f"{self.hostname}: Unknown xcvr type {xcvr_desc}")

    def _get_mod_number(self, mod_name: str) -> str:
        """
        Strips out "FPC|MIC|PIC" from a module name seen in "show chassis hardware"
        """
        return re.sub(r"(MIC|PIC|FPC) ", "", mod_name)

    def _send_command(self, view: str) -> str:
        """
        Uses junos views to send an RPC command and gets the results
        """
        view = getattr(junos_views, view)
        result = view(self.device)  # pylint: disable=no-member
        return result.get()

    def _parse_dhcp_helpers(self):
        """
        Parses dhcp relay helpers from the running config
        """

        server_groups = {"default": {}}
        groups = {"default": {}}

        vrf = "default"
        group = None

        dhcp_relay_flag = False
        dhcp_relay_indent = ""
        vrf_flag = False
        server_group_flag = False
        indent = ""

        for line in self.running_config.split("\n"):
            # detecting which vrf we're in
            m = re.match(r"routing-instances {", line)
            if m:
                vrf_flag = True
                continue

            m = re.match(r"    (\S+) {", line)
            if m and vrf_flag:
                vrf = m.group(1)
                server_groups[vrf] = {}
                groups[vrf] = {}
                continue

            m = re.match(r"}$", line)
            if m and vrf_flag:
                vrf_flag = False
                continue

            # dhcp relay section flag
            m = re.match(r"(\s+)dhcp-relay {", line)
            if m:
                dhcp_relay_flag = True
                dhcp_relay_indent = m.group(1)
                continue

            # dhcp server group parsing start
            m = re.match(r"(\s+)server-group {", line)
            if m and dhcp_relay_flag:
                indent = m.group(1)
                server_group_flag = True
                continue

            # new server group definition
            m = re.match(r"\s+(\S+) {", line)
            if m and dhcp_relay_flag and server_group_flag:
                server_group = m.group(1)
                server_groups[vrf][server_group] = []
                continue

            # new server in server group
            m = re.match(r"\s+(\d+.\d+.\d+.\d+);", line)
            if m and dhcp_relay_flag and server_group_flag:
                server_groups[vrf][server_group].append(m.group(1))
                continue

            ### dhcp group parsing start
            m = re.match(r"(\s+)group (\S+) {", line)
            if m and dhcp_relay_flag:
                indent = m.group(1)
                group = m.group(2)
                groups[vrf][group] = {"interfaces": []}
                continue

            # active-server group for group
            m = re.match(r"\s+active-server-group (\S+);", line)
            if m and dhcp_relay_flag and group:
                groups[vrf][group]["server-group"] = m.group(1)
                continue

            # interface in group
            m = re.match(r"\s+interface (\S+);", line)
            if m and dhcp_relay_flag and group:
                groups[vrf][group]["interfaces"].append(m.group(1))
                continue

            # end server group or group parsing
            m = re.match(r"(\s+)}", line)
            if m and m.group(1) == indent and server_group_flag:
                server_group_flag = False
                continue

            if m and m.group(1) == indent and group:
                group = False
                continue

            if m and m.group(1) == dhcp_relay_indent:
                dhcp_relay_flag = False
                continue

        # final output 'resolves' the server-group name into
        # list of IPs from the server-group dictionary
        output = {}
        for vrf, groups in groups.items():
            output[vrf] = {}
            for group in groups.values():
                if (
                    vrf not in server_groups
                    or group["server-group"] not in server_groups[vrf]
                ):
                    continue
                server_list = server_groups[vrf][group["server-group"]]
                for interface in group["interfaces"]:
                    output[vrf][interface] = server_list

        return output

    @property
    def running_config(self):
        if not self._running_config:
            self._running_config = self.get_config()
        return self._running_config

    def get_config(self):
        """
        If we run our nornir getters right we can pull the arp aging timer
        out of the config
        """
        config = super().get_config("running", full=False, sanitized=False)
        self._running_config = config["running"]
        return config["running"]

    def get_arp_table(self, vrf="") -> ARPTableDict:
        """
        Pulls ARP table - napalm does have get_arp_table for junos but it doesn't
        support VRFs :(

        Because we have to dynamically query every VPN on the device we can't use
        junos views for this since they're based on statically defined rpc calls.
        Instead we'll have to do our own rpc calls.
        """

        # figure out the ARP aging timer - no operational command appears to show this,
        # pulling it from the config.
        m = re.search(r"system \{.+arp {\+aging-timer (\d+);", self.running_config)
        if m:
            self.arp_aging_timer = int(m.group(1))

        # building the rpc call as an lxml element so we can dynamically add a vrf if we want
        # if no vrf is provided all ARP entries are returned
        arp_rpc = etree.Element("get-arp-table-information")
        etree.SubElement(arp_rpc, "no-resolve")
        etree.SubElement(arp_rpc, "expiration-time")
        if vrf:
            xml_vrf = etree.SubElement(arp_rpc, "vpn")
            xml_vrf.text = vrf

        rpc_result = self.device.execute(arp_rpc)

        results = []
        for xml_entry in rpc_result.iterfind("arp-table-entry"):
            interface = xml_entry.find("interface-name").text.strip("\n")

            # MX and EX9200 include the physical interface in brackets - stripping
            # that out so only the logical interface is shown
            interface = re.sub(r" \[.+\]$", "", interface)

            exp = xml_entry.find("time-to-expire")
            if exp is not None:
                age = self.arp_aging_timer - int(exp.text)
            else:
                age = 0

            results.append(
                {
                    "interface": interface,
                    "ip": xml_entry.find("ip-address").text.strip("\n"),
                    "mac": xml_entry.find("mac-address").text.strip("\n").upper(),
                    "age": age,
                }
            )

        return results

    def get_lldp_neighbors(self) -> LLDPNeighborDict:
        """
        Overrides napalm get_lldp_neighbors so that we actually get the remote
        interface ID instead of the description.

        NAPALM's get_lldp_neighbors_detail gets this for us - note that to get this detail,
        you need to execute a command for each interface just like on the cli :(
        """
        neighs = super().get_lldp_neighbors_detail()
        output = {}
        for port, neighs in neighs.items():
            output[port] = []
            for neigh in neighs:
                output[port].append(
                    {
                        "hostname": neigh["remote_system_name"]
                        if neigh["remote_system_name"]
                        else neigh["remote_chassis_id"],
                        "port": neigh["remote_port"],
                    }
                )
        return output

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        """
        Parses 'get interface' and show route instance detail
        """

        # parsing dhcp helpers from the running config
        helpers = self._parse_dhcp_helpers()

        interface_vrfs = self._send_command("junos_vrf_interfaces")
        i_vrfs = {i.name: i.vrf for i in dict(interface_vrfs).values()}

        interfaces = self._send_command("junos_ip_interfaces")

        results = []
        for i in dict(interfaces).values():
            if self._ignore_interface(i.interface) or i.family not in ["inet", "inet6"]:
                continue

            # ignore ipv6 link local
            if i.family == "inet6" and i.ip.startswith("fe80"):
                continue

            # ignore non-preferred addresses, these appear to be vrrp virtuals
            if not (i.preferred):
                continue

            # host networks don't have 'ifa-destination' (subnet) field
            if i.subnet:
                prefixlen = i.subnet.split("/")[1]
            elif i.family == "inet":
                prefixlen = "32"
            else:
                prefixlen = "128"

            vrf = i_vrfs.get(i.interface, "default")

            # junos has weird internal private VRFs with loopbacks
            if vrf.startswith("__"):
                continue

            if helpers.get(vrf):
                i_helpers = helpers[vrf].get(i.interface, [])
            else:
                i_helpers = []

            results.append(
                {
                    "ip_address": f"{i.ip}/{prefixlen}",
                    "interface": i.interface,
                    "description": i.description,
                    "mtu": 9216 if i.mtu == "Unlimited" else int(i.mtu),
                    "admin_up": bool(i.admin_up),
                    "oper_up": not (i.device_down or i.hardware_down),
                    "vrf": vrf,
                    "secondary": not (i.primary),
                    "helpers": i_helpers,
                }
            )

        return results

    def get_active_routes(self) -> List[RouteDict]:
        """
        Parses rpc call show route detail
        """
        logger.debug("getting active routes")
        result = self._send_command("junos_route_table")
        logger.debug("Done getting routes")

        output = []

        # junos views returns data as a list of entries, where each entry
        # is a list of tuples (key, val) from the junos view.
        # You can cast the data to a list of dicts (see get_inventory)
        # but for large results converting to dict is very slow so we're not doing
        # that here.
        for (_, vrf), (_, prefix), (_, rt_entry) in result.values():
            if vrf in self.IGNORE_ROUTE_TABLES:
                continue

            prefix = ip_network(prefix)

            if vrf in ["inet.0", "inet6.0"]:
                vrf = "default"
            else:
                vrf = vrf.split(".")[0]

            # also skip link local prefixes
            if prefix.is_link_local:
                continue

            for (
                (_, age),
                (_, protocol),
                (_, learned_from),
                (_, next_hop),
            ) in rt_entry.values():
                for (
                    (_, nh_ip),
                    (_, nh_interface),
                    (_, mpls_label),
                    (_, selected_next_hop),
                ) in next_hop.values():
                    if not selected_next_hop:
                        continue

                    if learned_from:
                        learned_from = learned_from
                    elif nh_ip:
                        learned_from = nh_ip
                    elif protocol in ["Direct", "Local", "Static"]:
                        learned_from = "self"
                    else:
                        raise UMnetNapalmError(
                            f"Could not determine learned from for {prefix}"
                        )

                    mpls_label = self._parse_mpls_label(mpls_label)

                    output.append(
                        RouteDict(
                            vrf=vrf,
                            prefix=str(prefix),
                            nh_interface=nh_interface,
                            learned_from=learned_from,
                            protocol=protocol,
                            age=age_to_integer(age),
                            nh_ip=nh_ip,
                            mpls_label=mpls_label,
                            nh_table="default" if mpls_label else vrf,
                            # not supporting junos VXLAN
                            vxlan_vni=None,
                            vxlan_endpoint=None,
                        )
                    )

        return output

    def get_inventory(self) -> List[InventoryDict]:
        """
        parses the get-chassis-inventory RPC call, which maps to "show chassis hardware"
        """
        result = self._send_command("junos_inventory")

        output = []
        for chassis in dict(result).values():
            # note that the chassis model and s/n are at this level, but
            # that doesn't count as an 'inventory item' so we're ignoring it

            # saving modules, sub-modules and sub-sub modules
            for module in dict(chassis.modules).values():
                self._save_inventory_item(output, module)

                for sub_module in dict(module.sub_modules).values():
                    self._save_inventory_item(output, sub_module, parent=module.name)

                    for sub_sub_module in dict(sub_module.sub_sub_modules).values():
                        self._save_inventory_item(
                            output,
                            sub_sub_module,
                            parent=sub_module.name,
                            grandparent=module.name,
                        )

        return output

    def _save_inventory_item(
        self, output: list, item: any, parent: str = None, grandparent: str = None
    ) -> bool:
        """
        Extracts data from a particular inventory item object.
        Returns whether we care aobut this item or not (so we know whether or not)
        to loop over its children
        """
        # skip builtin types, or parts without model numbers that aren't transcievers
        if item.part_number == "BUILTIN":
            return False

        # get inventory type based on item name and P/N
        inv_type = self._get_junos_inventory_type(item.name, item.model_number)

        if not inv_type:
            return False

        # for transcievers, change the name from Xcvr X to be the junos interface name
        # note that we expect transcievers to always be at the sub-sub module level
        # and thus to have a grandparent and parent
        m = re.search(r"Xcvr (\d+)", item.name)
        if m:
            if not (grandparent or parent):
                raise UMnetNapalmError(
                    f"{self.hostname}: No MIC and PIC found for {item.name}"
                )
            prefix = self._get_xcvr_interface_prefix(item.description)

            item_name = f"{prefix}{self._get_mod_number(grandparent)}/{self._get_mod_number(parent)}/{m.group(1)}"

        # for sub-linecards (mics or pics) we want to prepend the parent to the item name
        elif parent:
            item_name = f"{parent} {item.name}"
        else:
            item_name = item.name

        output.append(
            {
                "type": inv_type,
                "name": item_name,
                "subtype": item.description,
                "part_number": self._get_inventory_part_number(item),
                "serial_number": item.serial_number,
            }
        )

        return True

    def _get_inventory_part_number(self, item: any) -> str:
        """
        Extracts the part number from an inventory item
        which, depending on the specific item, is stashed in
        the part number, model number, or description field
        """
        if item.model_number and item.model_number != "model-number":
            return item.model_number
        return item.part_number

    def get_mpls_switching(self) -> List[MPLSDict]:
        """
        Parses 'show route active-path table mpls.0'
        """
        result = self._send_command("junos_mpls_table")

        output = []
        for (_, prefix), (_, rt_entry) in result.values():
            # in our network we can skip these 'label is not at the top
            # of the stack' entries - they're redundant
            # also labels 0-2 are junos-internal
            if "(S=0)" in prefix or prefix in ["0", "1", "2"]:
                continue

            for entry in rt_entry.values():
                next_hop = entry[0][1]
                for (
                    (_, nh_ip),
                    (_, nh_interface),
                    (_, mpls_label),
                    (_, nh_table_receive),
                    (_, nh_table),
                ) in next_hop.values():
                    # next hop table is either in 'nh-table-receive' or 'nh-table'
                    nh_table = nh_table if nh_table else nh_table_receive

                    (nh_interface, out_label, aggregate) = self._process_mpls_nh(
                        nh_interface, mpls_label, nh_table
                    )

                    # 'fec' and 'rd' aren't in the Junos mpls.0 table - this is a Cisco
                    # thing from "show mpls switching"
                    output.append(
                        {
                            "in_label": prefix,
                            "out_label": out_label,
                            "nh_interface": nh_interface,
                            "fec": None,
                            "nh_ip": nh_ip,
                            "rd": None,
                            "aggregate": aggregate,
                        },
                    )

        return output

    def _parse_mpls_label(self, label_str) -> Union[List[int], None]:
        """
        Parses mpls-label parameter into a list of integers
        """
        if not label_str:
            return None

        m = re.match(r"Push (?P<inner>\d+)(, Push (?P<outer>\d+))*", label_str)
        if not m:
            raise UMnetNapalmError(f"Couldn't parse label op {label_str}")

        labels = [m.group("inner")]
        if m.group("outer"):
            labels.append(m.group("outer"))

        return labels

    def _process_mpls_nh(
        self, nh_interface: str, mpls_label: str, nh_table: str
    ) -> tuple:
        """
        Parses 'nh interface', 'mpls_label', and nh_table values
        into something our standardized outpur likes.
        Returns a tuple (nh_interface:str, out_label:list, aggregate:bool )
        """
        # when the next hop is a table, not an interface we're going to
        # classify it as an aggregate label
        if not nh_interface and nh_table:
            nh_vrf = re.sub(r".inet6?.0", "", nh_table)
            return (nh_vrf, ["pop"], True)

        # aggregate labels also show up as nh_interface "lsi.X (VRF_NAME)"
        m = re.match(r"^lsi.\d+ \((\S+)\)", nh_interface)
        if m:
            return (m.group(1), [], True)

        # 'pop' label has trailing whitespace
        if mpls_label and re.match(r"^Pop", mpls_label):
            return (nh_interface, ["pop"], False)

        # 'swap' with optional 'push'
        if mpls_label:
            m = re.match(r"^Swap (?P<inner>\d+)(, Push (?P<outer>\d+))*", mpls_label)
            if m:
                out_label = [m.group("inner")]
                if m.group("outer"):
                    out_label.append(m.group("outer"))

                return (nh_interface, out_label, False)

        raise UMnetNapalmError(
            f"Cannot parse MPLS route nh: {nh_interface} label: {mpls_label}"
        )

    def get_lag_interfaces(self) -> Dict[str, LagInterfaceDict]:
        """
        Extracts LAG info from 'show interfaces terse' and 'show lacp interface'
        """
        result = self._send_command("junos_show_int_lag")

        result_dict = dict(result)

        parents = {k: v for k, v in result_dict.items() if k.startswith("ae")}
        children = {k: v for k, v in result_dict.items() if v.lag_name}

        # building parent list
        lag_interfaces = {}
        for name, entry in parents.items():
            # stripping off logical port
            name = name.split(".")[0]

            lag_interfaces[name] = {
                "oper_up": entry.oper_status == "up",
                "admin_up": entry.admin_status == "up",
                "protocol": "Static",  # to be overridden if LAG is seen in 'show lacp interfaces'
                "members": {},
                "mlag_id": 0,  # don't care about MC-LAG (shudder) or EVPN multihoming
                "peer_link": False,  # don't care about MC-LAG (shudder)
            }

        # adding children to parents
        for name, entry in children.items():
            # want physical interface names only
            name = name.split(".")[0]
            lag_name = entry.lag_name.split(".")[0]

            if lag_name not in lag_interfaces:
                raise UMnetNapalmError(f"Invalid LAG assignment {lag_name} for {name}")

            lag_interfaces[lag_name]["members"][name] = {
                "oper_up": entry.oper_status == "up",
                "admin_up": entry.admin_status == "up"
                and entry.phy_admin_status == "up",
                "flags": "",
            }

        # next we're going to flag LACP ports
        try:
            result = self._send_command("junos_show_lacp")

        # if lacp isn't running the junos device returns an RPC error,
        # which raises an exception
        except Exception as e:
            # if the exception is because lacp isn't running, return
            # our list of LAGs as is, otherwise we want to raise
            if "lacp subsystem not running" in e.message:
                return lag_interfaces
            raise

        for lag_name, entry in dict(result).items():
            for member_name, member_entry in dict(entry.members).items():
                if (
                    member_name
                    not in lag_interfaces.get(lag_name, {"members": {}})["members"]
                ):
                    raise UMnetNapalmError(
                        f"Invalid LACP entry for LAG {lag_name} member {member_name}"
                    )

                # all LAGs appear in 'show lacp' but the ones actually running LACP have members.
                lag_interfaces[lag_name]["protocol"] = "LACP"

                # lacp_activity = "Active" or "Passive", lacp_timeout = "Slow" or "Fast"
                flags = member_entry.lacp_activity[0] + member_entry.lacp_timeout[0]
                lag_interfaces[lag_name]["members"][member_name]["flags"] = flags

        return lag_interfaces
