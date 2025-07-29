from typing import Optional, Dict

from typing_extensions import TypedDict

# using TypedDict to model our standardized output because that's
# what nampalm does and I like it - ref
# https://github.com/napalm-automation/napalm/blob/develop/napalm/base/models.py
VNIDict = TypedDict(
    "VNIDict",
    {
        "vni": int,
        "mcast_group": Optional[str],
        "vrf": Optional[str],
        "vlan_id": Optional[int],
    },
)

RouteDict = TypedDict(
    "RouteDict",
    {
        "vrf": str,
        "prefix": str,
        "nh_interface": str,
        "learned_from": str,
        "protocol": str,
        "age": int,
        "nh_table": str,
        "nh_ip": Optional[str],
        "mpls_label": Optional[list[str]],
        "vxlan_vni": Optional[int],
        "vxlan_endpoint": Optional[str],
    },
)

MPLSDict = TypedDict(
    "MPLSDict",
    {
        "in_label": str,
        "out_label": list,
        "nh_interface": Optional[str],
        "fec": Optional[str],
        "nh_ip": Optional[str],
        "rd": Optional[str],
        "aggregate": bool,
    },
)

IPInterfaceDict = TypedDict(
    "IPInterfaceDict",
    {
        "ip_address": str,
        "interface": str,
        "description": str,
        "mtu": int,
        "admin_up": bool,
        "oper_up": bool,
        "vrf": str,
        "secondary": bool,
        "helpers": list[str],
    },
)

VALID_INVENTORY_TYPES = (
    "fabric_module",
    "fan",
    "linecard",
    "optic",
    "psu",
    "re",
    "stack_cable",
    "stack_member",
    "uplink_module",
    "aoc",
    "dac",
)

InventoryDict = TypedDict(
    "InventoryDict",
    {
        "type": str,
        "name": str,
        "part_number": str,
        "serial_number": str,
    },
)

LagMemberDict = TypedDict(
    "LagMemberDict", {"oper_up": bool, "admin_up": bool, "flags": str}
)

LagInterfaceDict = TypedDict(
    "LagInterfaceDict",
    {
        "admin_up": bool,
        "oper_up": bool,
        "protocol": str,
        "mlag_id": int,
        "peer_link": bool,
        "members": Dict[str, LagMemberDict],
    },
)
