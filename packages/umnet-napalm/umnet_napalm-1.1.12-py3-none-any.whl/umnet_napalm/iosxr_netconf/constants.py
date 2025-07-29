NS = {
    "int": "http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper",
    "int4": "http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-oper",
    "int6": "http://cisco.com/ns/yang/Cisco-IOS-XR-ipv6-ma-oper",
    "rib4": "http://cisco.com/ns/yang/Cisco-IOS-XR-ip-rib-ipv4-oper",
    "rib6": "http://cisco.com/ns/yang/Cisco-IOS-XR-ip-rib-ipv6-oper",
    "inv": "http://cisco.com/ns/yang/Cisco-IOS-XR-invmgr-oper",
}


IP_INT_RPC_REQ = """
<get xmlns="urn:ietf:params:xml:ns:netconf:base:1.1">
  <filter>
    <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper">
      <interfaces>
        <interface/>
      </interfaces>
    </interfaces>
    <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-oper">
      <nodes>
        <node>
          <interface-data>
            <vrfs>
              <vrf>
                <details>
                  <detail/>
                </details>
              </vrf>
            </vrfs>
          </interface-data>
        </node>
      </nodes>
    </ipv4-network>
    <ipv6-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv6-ma-oper">
      <nodes>
        <node>
          <interface-data>
            <vrfs>
              <vrf>
                <global-details>
                  <global-detail/>
                </global-details>
              </vrf>
            </vrfs>
          </interface-data>
        </node>
      </nodes>
    </ipv6-network>
  </filter>
</get>"""

IP_ROUTE_RPC_REQ = """
<get xmlns="urn:ietf:params:xml:ns:netconf:base:1.1">
  <filter>
    <rib xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-rib-ipv4-oper">
      <vrfs>
        <vrf>
          <afs>
            <af>
              <af-name>IPv4</af-name>
              <safs>
                <saf>
                  <saf-name>Unicast</saf-name>
                  <ip-rib-route-table-names>
                    <ip-rib-route-table-name>
                      <route-table-name>default</route-table-name>
                      <routes>
                        <route>
                          <prefix-length/>
                          <protocol-name/>
                          <route-age/>
                          <route-path>
                            <active>true</active>
                          </route-path>
                        </route>
                      </routes>
                    </ip-rib-route-table-name>
                  </ip-rib-route-table-names>
                </saf>
              </safs>
            </af>
          </afs>
        </vrf>
      </vrfs>
    </rib>
  
    <ipv6-rib xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-rib-ipv6-oper">
      <vrfs>
        <vrf>
          <afs>
            <af>
              <af-name>IPv6</af-name>
              <safs>
                <saf>
                  <saf-name>Unicast</saf-name>
                  <ip-rib-route-table-names>
                    <ip-rib-route-table-name>
                      <route-table-name>default</route-table-name>
                      <routes>
                        <route>
                          <prefix-length/>
                          <protocol-name/>
                          <route-age/>
                          <route-path>
                            <active>true</active>
                          </route-path>
                        </route>
                      </routes>
                    </ip-rib-route-table-name>
                  </ip-rib-route-table-names>
                </saf>
              </safs>
            </af>
          </afs>
        </vrf>
      </vrfs>
    </ipv6-rib>

  </filter>
</get>
"""

INV_RPC_REQ = """
<get xmlns="urn:ietf:params:xml:ns:netconf:base:1.1">
  <filter>
    <inventory xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-invmgr-oper">
      <entities>
        <entity>
          <attributes>
            <inv-basic-bag>
              <description/>
              <name/>
              <serial-number/>
              <manufacturer-name/>
              <model-name/>
              <is-field-replaceable-unit>true</is-field-replaceable-unit>
            </inv-basic-bag>
          </attributes>
        </entity>
      </entities>
    </inventory>
  </filter>
</get>
"""
