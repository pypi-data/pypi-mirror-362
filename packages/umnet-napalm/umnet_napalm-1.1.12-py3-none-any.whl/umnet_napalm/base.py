from typing import List, Dict
import re


from .models import (
    IPInterfaceDict,
    RouteDict,
    MPLSDict,
    VNIDict,
    InventoryDict,
    LagInterfaceDict,
    VALID_INVENTORY_TYPES,
)


class UMnetNapalmError(Exception):
    """
    Generic error class
    """


class UMnetNapalm:
    """
    Base class for um-specific (but also non-vendor specific)
    implementations.
    """

    # populate in child classes
    IGNORE_INTERFACES = []
    LABEL_VALUE_MAP = {}
    INVENTORY_TO_TYPE = {}
    PROTOCOL_ABBRS = {}
    I_ABBRS = {}

    def _parse_protocol_abbr(self, abbr) -> str:
        if abbr in self.PROTOCOL_ABBRS:
            return self.PROTOCOL_ABBRS[abbr]

        raise UMnetNapalmError(f"Unknown protocol abbr {abbr}")

    def _expand_i(self, interface: str) -> str:
        """
        Converts short interface to long (I_ABBRS defined
        in child classes)
        """
        for short, long in self.I_ABBRS.items():
            if re.match(short, interface):
                return re.sub(short, long, interface)

        return interface

    def _abbr_i(self, interface: str) -> str:
        """
        Converts long interface to short (I_ABBRS defined
        in child classes)
        """
        for short, long in self.I_ABBRS.items():
            if re.match(long, interface):
                return re.sub(long, short, interface)

        return interface

    def _ignore_interface(self, interface: str) -> bool:
        """
        Checks to see if this interface matches any regexes in our
        IGNORE_INTERFACE list (implemented) in child class
        """
        for i in self.IGNORE_INTERFACES:
            if re.match(i, interface):
                return True

        return False

    def _get_inventory_type(self, name: str) -> str:
        """
        Maps the name of the inventory item to its type
        """
        for pattern, inv_type in self.INVENTORY_TO_TYPE.items():
            if inv_type and inv_type not in VALID_INVENTORY_TYPES:
                raise UMnetNapalmError(f"Invalid Inventory type {inv_type}")
            if re.search(pattern, name):
                return inv_type

        raise UMnetNapalmError(f"Unknown inventory item {name}")

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        raise NotImplementedError

    def get_active_routes(self) -> List[RouteDict]:
        """get active routes"""
        raise NotImplementedError

    def get_mpls_switching(self) -> List[MPLSDict]:
        """get mpls switching (the mpls forwarding table)"""
        raise NotImplementedError

    def get_vni_information(self) -> List[VNIDict]:
        """get vni to vlan and VRF mapping"""
        raise NotImplementedError

    def get_inventory(self) -> List[InventoryDict]:
        """get inventory items"""
        raise NotImplementedError

    def get_lag_interfaces(self) -> Dict[str, LagInterfaceDict]:
        """get lag parents, their status, and their children"""
        raise NotImplementedError

    def _parse_label_value(self, label) -> list:
        """
        Parses mpls label value into normalized data
        """
        if label in self.LABEL_VALUE_MAP:
            return self.LABEL_VALUE_MAP[label]

        return [label]
