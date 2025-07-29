Value IP (\d+.\d+.\d+.\d+)
Value MAC (\w{4}.\w{4}.\w{4})
Value AGE (\S+)
Value INTERFACE (\S+)

Start
 ^${IP}\s+${AGE}\s+${MAC}\s+\S+\s+ARPA\s+${INTERFACE} -> Record


