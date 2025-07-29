Value Required INTERFACE (\S+)
Value ADMIN_STATE (up|down|administratively down)
Value OPER_STATE (\S+)
Value MTU (\d+)
Value Required IP (\d+.\d+.\d+.\d+\/\d+)
Value List SEC_IP (\d+.\d+.\d+.\d+\/\d+)
Value List HELPERS (\d+.\d+.\d+.\d+)
Value VRF (\S+)


Start
 ^${INTERFACE} is ${ADMIN_STATE}, line protocol is ${OPER_STATE}
 ^\s+Internet address is ${IP}
 ^\s+MTU is ${MTU}
 ^\s+Helper address is ${HELPERS}
 ^\s+Helper addresses are ${HELPERS} -> Helpers
 ^\s+VPN Routing/Forwarding "${VRF}"
 ^\s+Secondary address ${SEC_IP}
 ^\s+Proxy ARP -> Record Start

Helpers
 ^\s+${HELPERS}
 ^\s+Directed -> Start
