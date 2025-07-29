Value INTERFACE (\S+)
Value ADMIN_STATE (\S+)
Value OPER_STATE (\S+)
Value VRF (\S+)
Value Required IP (\d+.\d+.\d+.\d+\/\d+)
Value List SEC_IP (\d+.\d+.\d+.\d+\/\d+)
Value MTU (\d+)

Start
 ^${INTERFACE} is ${ADMIN_STATE}, ipv4 protocol is ${OPER_STATE}
 ^  Vrf is ${VRF}
 ^  Internet address is ${IP}
 ^  Secondary address ${SEC_IP}
 ^  MTU is \d+ \(${MTU} is available to IP\)
 ^\s+Table Id -> Record


