Value LAG_NAME (Po\d+)
Value LAG_STATE (.+)
Value LAG_PROTO (\S+)
Value MEMBER_NAME (\S+)
Value MEMBER_STATE (\w+)
Value MEMBER_GROUP (\d+)
Value MEMBER_MODE (\w+)
Value MEMBER_FLAGS (\w+)

Start
  ^\s+Ports in the group: -> Members
  ^\s+Port-channels in the group: -> Parent

Parent
  ^Port-channel: -> Continue.Record
  ^Port-channel: ${LAG_NAME}
  ^Port state\s+=\s+Port-channel ${LAG_STATE}
  ^Protocol\s+=\s+${LAG_PROTO}
  ^\s+Ports in the group: -> Members

Members
  ^Port: -> Continue.Record
  ^Port: ${MEMBER_NAME}
  ^Port state\s+= ${MEMBER_STATE}
  ^Channel group = ${MEMBER_GROUP}\s+Mode = ${MEMBER_MODE}\s+Gcchange
  ^Local information: -> MemberInfo
  ^\s+Port-channels in the group: -> Parent

MemberInfo
  ^Port\s+
  ^\S+\s+${MEMBER_FLAGS}\s+\S+\s+\d+\s+0x\w -> Members
