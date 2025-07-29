Value Filldown PROTOCOL (\w)
Value Filldown SUBNET (\d+.\d+.\d+.\d+)
Value Filldown NETMASK (\d+.\d+.\d+.\d+)
Value PREFERENCE (\d+)
Value METRIC (\d+)
Value AGE ((\d+w)?(\d+d)?(\d+h)?(\d{2}\:\d{2}\:\d{2})?)
Value NH_INTERFACE (\S+)
Value NH_IP (\d+.\d+.\d+.\d+)


Start
 ^${PROTOCOL}\*?\s+${SUBNET} ${NETMASK} \[${PREFERENCE}/${METRIC}\] via ${NH_IP}, ${AGE} -> Record
 ^\s+\[${PREFERENCE}/${METRIC}\] via ${NH_IP}, ${AGE} -> Record
 ^${PROTOCOL}\*?\s+${SUBNET} ${NETMASK} \[${PREFERENCE}/${METRIC}\] via ${NH_IP}, ${NH_INTERFACE} -> Record
 ^${PROTOCOL}\s+${SUBNET} ${NETMASK} (is directly connected|connected by VPN \(advertised\)), ${NH_INTERFACE} -> Record
 ^${PROTOCOL}\s+${SUBNET} ${NETMASK}\s*$$ -> TwoLineLocalRoute

TwoLineLocalRoute
 ^\s+is directly connected, ${NH_INTERFACE} -> Record Start

EOF