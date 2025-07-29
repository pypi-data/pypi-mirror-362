Value Required IN_LABEL (\d+)
Value FEC (\S+?)
Value OUT_LABEL (\d+|No Label|Pop Label)
Value NH_INTERFACE (\S+)
Value NH_IP (\S+)
Value VRF (\S+)

Start
  ^${IN_LABEL}\s+Pop Label.+aggregate/${VRF} -> Record
  ^${IN_LABEL}\s+${OUT_LABEL}\s+${FEC}(\[V\])*\s+\d+\s+${NH_INTERFACE}\s+${NH_IP} -> Record
  ^${IN_LABEL}\s+${OUT_LABEL}\s+${FEC}(\[V\])*\s+\\ -> MultiLine

MultiLine
  ^\s+\d+\s+${NH_INTERFACE}\s+${NH_IP} -> Record Start

EOF
