Value INTERFACE (\S+)
Value List IFNAME (\S+)
Value List,Required RELAYS (\d+.\d+.\d+.\d+)

Start
# per interface parsing
 ^interface ${INTERFACE}
 ^ nameif ${IFNAME}
 ^ dhcprelay server ${RELAYS}
 ^! -> Record
# global parsing
 ^dhcprelay server ${RELAYS}
 ^dhcprelay enable ${IFNAME}
 ^\: end -> Record