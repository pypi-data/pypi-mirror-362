Value PEER_LINK_ID (\d+)
Value VPC_ID (\d+)
Value Required LAG_NAME (\S+)
Value Required STATUS (\S+)


Start
  ^vPC Peer-link status -> PeerLink

PeerLink
  ^${PEER_LINK_ID}\s+${LAG_NAME}\s+${STATUS} -> Record
  ^vPC status -> VPC

VPC
  ^${VPC_ID}\s+${LAG_NAME}\s+${STATUS} -> Record


# vPC Peer-link status
# ---------------------------------------------------------------------
# id    Port   Status Active vlans
# --    ----   ------ -------------------------------------------------
# 1     Po1000 up     1-4,9-17,20,22,102-132,254,301,317-318,537,666,
#                     1000,2000-2001,3845

# vPC status
# ----------------------------------------------------------------------------
# Id    Port          Status Consistency Reason                Active vlans
# --    ------------  ------ ----------- ------                ---------------
# 10    Po10          up     success     success               2-4,9-13,22,
#                                                              111-115,537
# 11    Po11          down*  success     success               -

# 12    Po12          down*  Not         Consistency Check Not -
#                            Applicable   Performed
# 13    Po13          down*  success     success               -


# Please check "show vpc consistency-parameters vpc <vpc-num>" for the
# consistency reason of down vpc and for type-2 consistency reasons for
# any vpc.
