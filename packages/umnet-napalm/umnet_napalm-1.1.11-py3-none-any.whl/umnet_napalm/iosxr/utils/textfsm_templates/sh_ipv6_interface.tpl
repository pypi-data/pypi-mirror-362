Value Required INTERFACE (\S+)
Value ADMIN_STATE (\S+)
Value OPER_STATE (\S+)
Value VRF (\S+)
Value List,Required IP ([\w\:]+\/\d+)
Value Fillup MTU (\d+)

Start
 ^${INTERFACE} is ${ADMIN_STATE}, ipv6 protocol is ${OPER_STATE}, Vrfid is ${VRF} 
 ^\s+[\w\:]+, subnet is ${IP}
 ^\s+MTU is \d+ \(${MTU} is available to IPv6\)
 ^\s+RA DNS -> Record 


