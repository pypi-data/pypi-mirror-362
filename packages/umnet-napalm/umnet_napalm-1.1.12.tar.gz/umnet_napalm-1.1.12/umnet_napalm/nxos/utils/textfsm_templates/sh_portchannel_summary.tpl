Value Filldown GROUP (\d+)
Value Filldown LAG_NAME (Po\d+)
Value Filldown LAG_FLAGS (\w+)
Value Filldown PROTOCOL ([\w\-]+)
Value M1_NAME ([\w\/]+)
Value M1_FLAGS (\w+)
Value M2_NAME ([\w\/]+)
Value M2_FLAGS (\w+)
Value M3_NAME ([\w\/]+)
Value M3_FLAGS (\w+)

Start
  ^${GROUP}\s+${LAG_NAME}\(${LAG_FLAGS}\)\s+\S+\s+${PROTOCOL}(\s+${M1_NAME}\(${M1_FLAGS}\))?(\s+${M2_NAME}\(${M2_FLAGS}\))?(\s+${M3_NAME}\(${M3_FLAGS}\))? -> Record
  ^\s+${M1_NAME}\(${M1_FLAGS}\)(\s+${M2_NAME}\(${M2_FLAGS}\))?(\s+${M3_NAME}\(${M3_FLAGS}\))? -> Record


# dl-shallow-1# show port-channel summ
# Flags:  D - Down        P - Up in port-channel (members)
#         I - Individual  H - Hot-standby (LACP only)
#         s - Suspended   r - Module-removed
#         b - BFD Session Wait
#         S - Switched    R - Routed
#         U - Up (port-channel)
#         p - Up in delay-lacp mode (member)
#         M - Not in use. Min-links not met
# --------------------------------------------------------------------------------
# Group Port-       Type     Protocol  Member Ports
#       Channel
# --------------------------------------------------------------------------------
# 10    Po10(SU)    Eth      LACP      Eth1/1(P)
# 11    Po11(SD)    Eth      LACP      Eth1/2(s)
# 12    Po12(SD)    Eth      NONE      --
# 13    Po13(SD)    Eth      LACP      Eth1/6(D)
# 1000  Po1000(SU)  Eth      LACP      Eth1/51(D)   Eth1/52(P)