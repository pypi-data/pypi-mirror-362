Value INTERFACE (\S+)
Value VNI (\d+)
Value MCAST_GRP (\d+.\d+.\d+.\d+|n/a)
Value STATE (\S+)
Value TYPE (\S+)
Value MODE (\S+)
Value BD_VRF (\S+?)

Start
  ^${INTERFACE}\s+${VNI}\s+${MCAST_GRP}\s+${STATE}\s+${MODE}\s+${TYPE}\s+\[${BD_VRF}\] -> Record

EOF
