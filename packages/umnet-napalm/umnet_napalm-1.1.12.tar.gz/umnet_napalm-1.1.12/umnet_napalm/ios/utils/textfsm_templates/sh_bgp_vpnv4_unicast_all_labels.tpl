Value Filldown VRF (\S+)
Value Filldown PREFIX (\d+.\d+.\d+.\d+(\/\d+)*)
Value NH_IP (\d+.\d+.\d+.\d+)
Value IN_LABEL (\S.+)
Value OUT_LABEL (\S.+)

Start
  ^Route Distinguisher: \S+ \(${VRF}\)
  ^\s+${PREFIX}\s+${NH_IP}\s+${IN_LABEL}/${OUT_LABEL} -> Record
  ^\s+${NH_IP}\s+${IN_LABEL}/${OUT_LABEL} -> Record
  ^\s+${PREFIX} -> TwoLineEntry

TwoLineEntry
  ^\s+${NH_IP}\s+${IN_LABEL}/${OUT_LABEL} -> Record Start

EOF
