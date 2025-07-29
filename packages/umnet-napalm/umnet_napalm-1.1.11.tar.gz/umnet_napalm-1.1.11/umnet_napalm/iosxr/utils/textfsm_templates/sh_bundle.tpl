Value Filldown LAG_NAME (\S+)
Value Filldown LAG_OPER_STATE (Up|Down|Admin down)
Value Filldown LACP_STATE (\S+.+)
Value Filldown ICCP_GRP (\d+)
Value Filldown ICL (\w+)
Value MEMBER_NAME (\S+)
Value MEMBER_DEVICE (\S+)
Value MEMBER_STATE (\w+)
Value MEMBER_LAG_STATE (\w+)

Start
  ^\S+ -> Continue.Record
  ^${LAG_NAME}$$
  ^\s+Status:\s+${LAG_OPER_STATE}$$
  ^\s+Inter-chassis link:\s+${ICL}$$
  ^\s+LACP:\s+${LACP_STATE}
  ^\s+ICCP Group:\s+${ICCP_GRP}
  ^\s+Port\s+Device\s+State\s+Port ID\s+B/W, kbps -> Member

Member
  ^\s+${MEMBER_NAME}\s+${MEMBER_DEVICE}\s+${MEMBER_LAG_STATE}\s+0x\d+, 0x\d+
  ^\s+Link is ${MEMBER_STATE} -> Record
  ^\s*$$ -> Start
  

