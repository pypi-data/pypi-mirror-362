Value NAME (.+)
Value DESC (.+)
Value PID (\S*)
Value SN (\S+)

Start
  ^NAME: "${NAME}", DESCR: "${DESC}"
  ^PID: ${PID}\s*,\s+VID:.*, SN: ${SN} -> Record