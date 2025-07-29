Value Filldown VRF (\S+)
Value Filldown INTERFACE (\S+)
Value Filldown PROTOCOL_STATE (\S+)
Value Filldown LINK_STATE (\S+)
Value Filldown ADMIN_STATE (\S+)
Value Required IPV6_ADDRESS ([0-9a-f\:]+/\d+)
Value Fillup MTU (\d+)

Start
  ^IPv6 Interface Status for VRF "${VRF}"
  ^${INTERFACE}, Interface status: ${PROTOCOL_STATE}/${LINK_STATE}/${ADMIN_STATE}, iod: \d+
  ^\s+${IPV6_ADDRESS} \[VALID\] -> Record
  ^\s+IPv6 MTU: ${MTU}

EOF
