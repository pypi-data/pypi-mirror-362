Value INTERFACE (\S+)
Value ADDRESS (\d+.\d+.\d+.\d+)


Start
  ^\s${INTERFACE}\s+${ADDRESS} -> Record

EOF
