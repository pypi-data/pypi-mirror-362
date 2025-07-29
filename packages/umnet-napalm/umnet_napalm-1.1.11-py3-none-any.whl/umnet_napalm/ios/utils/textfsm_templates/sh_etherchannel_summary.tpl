Value Filldown GROUP (\d+)
Value Filldown LAG_NAME (Po\d+)
Value Filldown LAG_FLAGS (\w+)
Value Filldown PROTOCOL ([\w\-]+)
Value M1_NAME ([\w\/]+)
Value M1_FLAGS (\w+)
Value M2_NAME ([\w\/]+)
Value M2_FLAGS (\w+)

Start
  ^${GROUP}\s+${LAG_NAME}\(${LAG_FLAGS}\)\s+${PROTOCOL}(\s+${M1_NAME}\(${M1_FLAGS}\))?(\s+${M2_NAME}\(${M2_FLAGS}\))? -> Record
  ^\s+${M1_NAME}\(${M1_FLAGS}\)(\s+${M2_NAME}\(${M2_FLAGS}\))? -> Record