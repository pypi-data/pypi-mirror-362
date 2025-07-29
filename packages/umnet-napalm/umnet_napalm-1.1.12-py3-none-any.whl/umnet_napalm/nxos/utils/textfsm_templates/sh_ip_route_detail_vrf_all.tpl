Value Filldown VRF (\S+)
Value Filldown PREFIX (\d+.\d+.\d+.\d+\/\d+)
Value Required PREFERENCE (\d+)
Value Required METRIC (\d+)
Value Required AGE (\S+)
Value Required PROTOCOL ([\w-]+)
Value NH_INTERFACE (\S+)
Value NH_IP (\d+.\d+.\d+.\d+)
Value NH_TABLE (\S+)
Value LABEL (\d+)
Value LABEL_PROTOCOL (\w+)
Value VNI (\d+)

Start
  ^IP Route Table for VRF "${VRF}"
  ^${PREFIX}, ubest/mbest: \d+/\d+
  ^\s+\*via ${NH_IP}%${NH_TABLE}, \[${PREFERENCE}/${METRIC}\], ${AGE}, ${PROTOCOL},.+encap: VXLAN -> VXLAN
  ^\s+\*via ${NH_IP}%${NH_TABLE}, \[${PREFERENCE}/${METRIC}\], ${AGE}, ${PROTOCOL}.+(mpls-vpn) -> MPLS
  ^\s+\*via ${NH_IP}, ${NH_INTERFACE}, \[${PREFERENCE}/${METRIC}\], ${AGE}, ${PROTOCOL}.+(mpls) -> MPLS
  ^\s+\*via ${NH_IP},( ${NH_INTERFACE},)* \[${PREFERENCE}/${METRIC}\], ${AGE}, ${PROTOCOL},* -> Record


VXLAN
  ^\s+BGP-EVPN: VNI=${VNI} \(EVPN\) -> Record Start

MPLS
  ^\s+MPLS\[0\]: Label=${LABEL} E=\d+ TTL=\d+ S=\d+ -> Record Start
  
EOF