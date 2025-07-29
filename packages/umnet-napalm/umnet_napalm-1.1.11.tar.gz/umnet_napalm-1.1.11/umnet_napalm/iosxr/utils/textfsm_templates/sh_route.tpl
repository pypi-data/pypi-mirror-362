Value Filldown VRF (\S+)
Value Filldown PREFIX (\d+.\d+.\d+.\d+\/\d+)
Value NH_INTERFACE (\S+)
Value NH_IP (\d+.\d+.\d+.\d+)
Value PREFERENCE (\d+)
Value METRIC (\d+)
Value AGE (\S+)
Value NH_VRF (\S+)
Value Filldown PROTO_1 (\w+)
Value Filldown PROTO_2 (\w+)

Start
  ^VRF: ${VRF}
  ^${PROTO_1}\*?\s+${PREFIX} is directly connected, ${AGE}, ${NH_INTERFACE} -> Record
  ^${PROTO_1}\*?\s+${PREFIX} \[${PREFERENCE}/${METRIC}\] via ${NH_IP}( \(nexthop in vrf ${NH_VRF}\))?, ${AGE} -> Record
  ^\s+\[${PREFERENCE}/${METRIC}\] via ${NH_IP}( \(nexthop in vrf ${NH_VRF}\))?, ${AGE} -> Record
  
EOF
