Value Required INTERFACE (\S+)
Value IFNAME (\S*)
Value ADMIN_STATE (up|down|administratively down)
Value OPER_STATE (up|down)
Value IFTYPE (.+)
Value SPEED (\d+)
Value VID (\d+)
Value MAC (\w{4}.\w{4}.\w{4}|N/A)
Value MTU (\d+)
Value IP (\d+.\d+.\d+.\d+)
Value NETMASK (\d+.\d+.\d+.\d+)


Start
 ^Interface ${INTERFACE}( "${IFNAME}",)? is ${ADMIN_STATE}, line protocol is ${OPER_STATE}
 ^\s+Hardware is ${IFTYPE}, BW ${SPEED}
 ^\s+Hardware is ${IFTYPE}	MAC address ${MAC}, MTU ${MTU}
 ^\s+VLAN identifier ${VID}
 ^\s+MAC address ${MAC}, MTU ${MTU}
 ^\s+IP address ${IP}, subnet mask ${NETMASK}
 ^\s+Control Point -> Record

EOF