from typing import List
import logging

from lxml import etree

from napalm.iosxr_netconf import IOSXRNETCONFDriver
from ncclient.xml_ import to_ele

from ..base import UMnetNapalm
from ..models import RouteDict, IPInterfaceDict, InventoryDict

from .constants import IP_INT_RPC_REQ, IP_ROUTE_RPC_REQ, NS, INV_RPC_REQ

logger = logging.getLogger(__name__)


class IOSXRNetconf(IOSXRNETCONFDriver, UMnetNapalm):
    """
    IOSXR Class
    """

    INVENTORY_TO_TYPE = {
        r"PM\d+$": "psu",
        r"FT\d+$": "fan",
        r"FC\d+$": "fabric_module",
        r"RP\d$": "re",
        r"SC\d": None,  # don't care about system controller
        r"Rack 0": None,  # this is the chassis, don't care about it
        r"^(FourHundred|Hundred|Forty)GigE": "optic",
        r"\d/\d": "linecard",
    }

    # Helper xml methods that always pass in our namespaces by default
    def _text(self, xml_tree, path, default=None, namespaces=NS):
        return super()._find_txt(xml_tree, path, default, namespaces=namespaces)

    def _xpath(self, xml_tree, path, namespaces=NS):
        return getattr(xml_tree, "xpath")(path, namespaces=namespaces)

    def _find(self, xml_tree, element, namespaces=NS):
        return getattr(xml_tree, "find")(element, namespaces=namespaces)

    def _iterfind(self, xml_tree, element, namespaces=NS):
        return getattr(xml_tree, "iterfind")(element, namespaces=namespaces)

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        """
        Gets IP interfaces
        """
        rpc_reply = self.device.dispatch(to_ele(IP_INT_RPC_REQ)).xml
        xml_result = etree.fromstring(rpc_reply)
        results = []

        # looking at every interface and pulling operation state and description
        for i in self._xpath(xml_result, "//int:interfaces/int:interface"):
            i_name = self._text(i, "int:interface-name")
            i_data = {
                "interface": i_name,
                "description": self._text(i, "int:description"),
                "admin_up": self._text(i, "int:state") != "im-state-admin-down",
                "oper_up": self._text(i, "int:line-state") == "im-state-up",
            }

            # pulling primary IPv4 for the interface. Note that though we're looping,
            # we only expect the xpath query to return a single entry.
            for pri_ipv4 in self._xpath(
                xml_result,
                f"//int4:vrf/int4:details/int4:detail[int4:interface-name='{i_name}']",
            ):
                ip = self._text(pri_ipv4, "int4:primary-address")

                prefixlen = self._text(pri_ipv4, "int4:prefix-length")

                i_data.update(
                    {
                        "vrf": self._text(pri_ipv4, "../../int4:vrf-name"),
                        "mtu": self._text(pri_ipv4, "int4:mtu"),
                    }
                )
                if ip != "0.0.0.0":
                    i_data.update(
                        {
                            "ip_address": f"{ip}/{prefixlen}",
                            "mtu": self._text(pri_ipv4, "int4:mtu"),
                        }
                    )
                    results.append(i_data.copy())

                # ipv4 secondaries
                for sec_ipv4 in self._iterfind(pri_ipv4, "int4:secondary-address"):
                    ip = self._text(sec_ipv4, "int4:address")
                    prefixlen = self._text(sec_ipv4, "int4:prefix-length")
                    i_data["ip_address"] = f"{ip}/{prefixlen}"
                    results.append(i_data.copy())

            # ipv6 addresses
            for ipv6 in self._xpath(
                xml_result,
                f"//int6:global-detail[int6:interface-name='{i_name}']/int6:address",
            ):
                i_data["mtu"] = self._text(ipv6, "../int6:mtu")
                ip = self._text(ipv6, "int6:address")
                prefixlen = self._text(ipv6, "int6:prefix-length")
                i_data["ip_address"] = f"{ip}/{prefixlen}"
                results.append(i_data.copy())

        return results

    def get_active_routes(self) -> List[RouteDict]:
        """
        Pulls active routes from the rib
        """
        rpc_reply = self.device.dispatch(to_ele(IP_ROUTE_RPC_REQ)).xml
        xml_result = etree.fromstring(rpc_reply)

        output = []

        # ipv4 rib and ipv6 rib yang models are similar enough that we can
        # use the same logic for both
        for v in ["4", "6"]:
            for route in self._xpath(
                xml_result,
                f"//rib{v}:ip-rib-route-table-name/rib{v}:routes/rib{v}:route",
            ):
                vrf = self._text(route, f"../../../../../../../../rib{v}:vrf-name")

                subnet = self._text(route, f"rib{v}:address")
                prefixlen = self._text(route, f"rib{v}:prefix-length")
                protocol = self._text(route, f"rib{v}:protocol-name")
                age = self._text(route, f"rib{v}:route-age")

                for nh in self._xpath(
                    route, f"rib{v}:route-path/rib{v}:ipv{v}-rib-edm-path"
                ):
                    learned_from = self._text(nh, f"rib{v}:information-source")
                    if learned_from == "0.0.0.0":
                        learned_from = "self"

                    # not currently dealing with enapsulation (where the next hop
                    # could be in a different table), but we do have some PBR
                    # that shows up under 'next-hop-vrf-name
                    if self._text(nh, f"rib{v}:next-hop-vrf-name"):
                        nh_table = self._text(nh, f"rib{v}:next-hop-vrf-name")
                    else:
                        nh_table = vrf

                    output.append(
                        {
                            "vrf": vrf,
                            "prefix": f"{subnet}/{prefixlen}",
                            "nh_interface": self._text(nh, f"rib{v}:interface-name"),
                            "learned_from": learned_from,
                            "protocol": protocol,
                            "nh_ip": self._text(nh, f"rib{v}:address"),
                            "age": age,
                            "mpls_label": [],
                            "vxlan_vni": None,
                            "nh_table": nh_table,
                        }
                    )

        return output

    def get_inventory(self) -> List[InventoryDict]:
        """
        Gets inventory data
        """
        rpc_reply = self.device.dispatch(to_ele(INV_RPC_REQ)).xml
        xml_result = etree.fromstring(rpc_reply)

        output = []
        for item in self._xpath(xml_result, "//inv:inv-basic-bag"):
            name = self._text(item, "inv:name")
            item_type = self._get_inventory_type(name)
            if item_type:
                output.append(
                    {
                        "type": item_type,
                        "name": name,
                        "part_number": self._text(item, "inv:model-name"),
                        "serial_number": self._text(item, "inv:serial-number"),
                        "parent": None,
                    }
                )

        return output
