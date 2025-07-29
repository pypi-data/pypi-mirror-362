Value Required IN_LABEL (\d+)
Value FEC (\S+)
Value OUT_LABEL (\S+)
Value NH_INTERFACE (\S+)
Value NH_IP (\S+)
Value RD (\S+)
Value VRF (\S+)
Value TYPE (IPv4|IPv6|Deaggregation|VPNV4|VPNV6)

Start
  ^${TYPE}\s+FEC(\s+type)*
  ^IAS\s+${TYPE}
  ^\s+In-Label\s+:\s+${IN_LABEL}
  ^\s+VRF\s+:\s+${VRF} -> Record 
  ^\s+Out-Label\s+stack\s+:\s+${OUT_LABEL}
  ^\s+FEC\s+:\s+${FEC}
  ^\s+RD\s+:\s+${RD}
  ^\s+Out\s+interface\s+:\s+${NH_INTERFACE}
  ^\s+Next\s+hop\s+:\s+${NH_IP} -> Record

EOF