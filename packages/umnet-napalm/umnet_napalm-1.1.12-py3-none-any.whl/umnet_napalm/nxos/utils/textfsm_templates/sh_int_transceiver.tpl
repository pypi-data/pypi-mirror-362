Value Required INTERFACE (\S+)
Value TYPE (\S+)
Value PN (\S+)
Value Required SN (\w+)

Start
  ^\S+ -> Continue.Record
  ^${INTERFACE}$$
  ^\s+type is ${TYPE}
  ^\s+part number is ${PN}
  ^\s+serial number is ${SN}


#Ethernet1/101
#    transceiver is present
#    type is QSFP-100G-SR4
#    name is FS
#    part number is QSFP28-SR4-100G
#    revision is 04
#    serial number is G2240392123
#    nominal bitrate is 25500 MBit/sec
#    Link length supported for 50/125um OM3 fiber is 70 m
#    cisco id is 17
#    cisco extended id number is 220
#
#Ethernet1/102
#    transceiver is not present