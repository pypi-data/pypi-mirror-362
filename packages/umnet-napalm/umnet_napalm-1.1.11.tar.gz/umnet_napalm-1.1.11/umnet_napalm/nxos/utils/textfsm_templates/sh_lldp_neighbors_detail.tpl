Value Required LOCAL_PORT (\S+)
Value Required REMOTE_PORT (\S+)
Value CHASSIS_ID (\S+)
Value PORT_DESCR (.+)
Value Required NAME (\S+)
Value DESCR (.+)
Value CAPAB (\S+)
Value ENABLE_CAPAB (\S+)
Value IPV4_IP (\d+.\d+.\d+.\d+)
Value IPV6_IP ([\w\:]+)
Value MAC (\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})

Start
 ^Chassis id: ${CHASSIS_ID} -> Record
 ^Port id: ${REMOTE_PORT}
 ^Local Port id: ${LOCAL_PORT}
 ^Port Description: ${PORT_DESCR}
 ^System Name: ${NAME}
 ^System Description: ${DESCR}
 ^System Capabilities: ${CAPAB}
 ^Enabled Capabilities: ${ENABLE_CAPAB}
 ^Management Address: ${IPV4_IP}
 ^Management Address IPV6: ${IPV6_IP}$$

 

# Chassis id: 5c31.9217.0f54
# Port id: mgmt0
# Local Port id: mgmt0
# Port Description: mgmt0
# System Name: dl-arbl-2.umnet.umich.edu
# System Description: Cisco Nexus Operating System (NX-OS) Software 9.3(9)
# TAC support: http://www.cisco.com/tac
# Copyright (c) 2002-2022, Cisco Systems, Inc. All rights reserved.
# Time remaining: 108 seconds
# System Capabilities: B, R
# Enabled Capabilities: B, R
# Management Address: 10.255.0.1
# Management Address IPV6: not advertised
# Vlan ID: 3
#
#
#
# Chassis id: e4fc.826c.d5d7
# Port id: ge-0/1/0
# Local Port id: Eth1/1
# Port Description: ge-0/1/0
# System Name: s-arbl2-1496-1.umnet.umich.edu
# System Description: Juniper Networks, Inc. ex2300-48p Ethernet Switch, kernel JUNOS 20.4R3-S1.3, Build date: 2021-11-20 10:48:25 UTC Copyright (c) 1996-2021 Juniper Networks, Inc.
# Time remaining: 119 seconds
# System Capabilities: B, R
# Enabled Capabilities: B, R
# Management Address: 10.233.0.35
# Management Address IPV6: not advertised
# Vlan ID: 15