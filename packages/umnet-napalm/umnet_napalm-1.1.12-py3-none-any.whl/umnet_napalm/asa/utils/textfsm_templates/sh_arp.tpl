Value INTERFACE (\S+)
Value IP (\d+.\d+.\d+.\d+)
Value MAC (\w{4}.\w{4}.\w{4})
Value AGE (\d+)

Start
 ^\s+${INTERFACE} ${IP} ${MAC} ${AGE} -> Record

EOF