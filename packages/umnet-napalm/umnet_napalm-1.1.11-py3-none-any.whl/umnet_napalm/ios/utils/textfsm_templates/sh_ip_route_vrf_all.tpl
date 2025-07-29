Value Filldown VRF (\S+)
Value Filldown PREFIX (\d+.\d+.\d+.\d+\/\d+)
Value NH_INTERFACE (\S+)
Value NH_IP (\d+.\d+.\d+.\d+)
Value PREFERENCE (\d+)
Value METRIC (\d+)
Value AGE (\S+)
Value Filldown PROTO_1 (\w+)
Value Filldown PROTO_2 (\w+)

Start
  ^Routing Table: ${VRF}
  ^${PROTO_1}\s+${PREFIX} is directly connected, ${NH_INTERFACE} -> Record
  ^${PROTO_1}\**\s*${PROTO_2}*\s+${PREFIX} \[${PREFERENCE}/${METRIC}\] via ${NH_IP}, ${AGE}, ${NH_INTERFACE} -> Record
  ^${PROTO_1}\**\s*${PROTO_2}*\s+${PREFIX} \[${PREFERENCE}/${METRIC}\] via ${NH_IP}, ${AGE} -> Record
  ^\s+\[${PREFERENCE}/${METRIC}\] via ${NH_IP}, ${AGE}, ${NH_INTERFACE} -> Record
  ^${PROTO_1}\s+${PREFIX}\[${PREFERENCE}/${METRIC}\] via ${NH_IP} -> Record
  ^${PROTO_1}\**\s*${PROTO_2}*\s+${PREFIX} -> TwoLineRoute

TwoLineRoute
  ^\s+\[${PREFERENCE}/${METRIC}\] via ${NH_IP}, ${AGE}, ${NH_INTERFACE} -> Record Start

EOF
