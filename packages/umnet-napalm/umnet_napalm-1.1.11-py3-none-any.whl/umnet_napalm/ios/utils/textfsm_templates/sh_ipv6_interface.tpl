Value Filldown,Required INTERFACE (\S+)
Value Filldown ADMIN_STATE (\S+)
Value Filldown OPER_STATE (\S+)
Value List,Required IP ([\w\:]+\/\d+)
Value MTU (\d+)
Value VRF (\S+)

Start
 ^${INTERFACE} is ${ADMIN_STATE}, line protocol is ${OPER_STATE}
 ^\s+[\w\:]+, subnet is ${IP}
 ^\s+MTU is ${MTU} bytes
 ^\s+VPN Routing/Forwarding "${VRF}"
 ^\s+ND -> Record
