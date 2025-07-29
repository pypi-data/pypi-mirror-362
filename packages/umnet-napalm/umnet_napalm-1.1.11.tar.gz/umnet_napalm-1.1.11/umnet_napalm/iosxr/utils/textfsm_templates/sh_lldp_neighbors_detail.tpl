Value LOCAL_PORT (\S+)
Value PORT (\S+)
Value CHASSIS_ID (\S+)
Value PORT_DESCR (.+)
Value NAME (\S+)
Value DESCR (.+)
Value CAPAB (\S+)
Value ENABLE_CAPAB (\S+)
Value IPV4_IP (\d+.\d+.\d+.\d+)
Value IPV6_IP ([\w\:]+)
Value MAC (\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})

Start
 ^Local Interface: ${LOCAL_PORT}
 ^Chassis id: ${CHASSIS_ID}
 ^Port id: ${PORT}
 ^Port Description: ${PORT_DESCR}
 ^System Name: ${NAME}
 ^System Description: -> SysDescr
 ^System Capabilities: ${CAPAB}
 ^Enabled Capabilities: ${ENABLE_CAPAB}
 ^Management Addresses -> Addrs 
 ^-------------- -> Record

SysDescr
 ^${DESCR} -> IgnoreRemainingDescription

IgnoreRemainingDescription
  ^\S+
  ^$$ -> Start
  ^.* -> Error


Addrs
 ^\s+IPv4 address: ${IPV4_IP}
 ^\s+IPv6 address: ${IPV6_IP}
 ^Peer MAC Address: ${MAC} -> Record Start
 


