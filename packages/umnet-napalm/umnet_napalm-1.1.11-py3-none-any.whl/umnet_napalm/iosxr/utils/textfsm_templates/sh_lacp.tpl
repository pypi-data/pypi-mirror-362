Value Filldown LAG_NAME (\S+)
Value Required MEMBER_NAME (\S+)
Value LACP_RATE (\d+s|none)
Value FLAGS ([\w\-]+)

Start
  ^Local
  ^\s+Partner
  ^${LAG_NAME}$$
  ^\s+${MEMBER_NAME}\s+${LACP_RATE}\s+${FLAGS}\s+0x\d+, -> Record
