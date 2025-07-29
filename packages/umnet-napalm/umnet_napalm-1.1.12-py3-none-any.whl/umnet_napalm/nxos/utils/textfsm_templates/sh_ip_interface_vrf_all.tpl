Value Filldown VRF (\S+)
Value Filldown INTERFACE (\S+)
Value Filldown PROTOCOL_STATE (\S+)
Value Filldown LINK_STATE (\S+)
Value Filldown ADMIN_STATE (\S+)
Value Required IP_ADDRESS (\d+.\d+.\d+.\d+)
Value PREFIXLEN (\d+)
Value SECONDARY (secondary)
Value Fillup MTU (\d+)

Start
  ^IP Interface Status for VRF "${VRF}"
  ^${INTERFACE}, Interface status: ${PROTOCOL_STATE}/${LINK_STATE}/${ADMIN_STATE}, iod: \d+,
  ^\s+IP address: ${IP_ADDRESS}, IP subnet: \d+.\d+.\d+.\d+/${PREFIXLEN}( ${SECONDARY})? -> Record
  ^\s+IP MTU: ${MTU} bytes

EOF
