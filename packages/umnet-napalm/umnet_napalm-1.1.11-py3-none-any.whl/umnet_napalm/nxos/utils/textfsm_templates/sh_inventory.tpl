Value NAME (.+)
Value DESC (.+)
Value PID (\S*)
Value SN (\S+)

Start
  ^NAME: "${NAME}",\s+DESCR: "${DESC}"
  ^PID: ${PID}\s*,\s+VID:.*,\s+SN: ${SN} -> Record