Value INTERFACE (\S+)
Value DESCRIPTION (.+)

Start
 ^${INTERFACE}\s+(up|down|admin down)\s+(up|down|admin down)\s+${DESCRIPTION} -> Record


