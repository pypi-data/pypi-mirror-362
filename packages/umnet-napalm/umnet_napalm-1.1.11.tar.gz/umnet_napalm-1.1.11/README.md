# umnet-napalm
This is a project that augments the [NAPALM](https://napalm.readthedocs.io/en/latest/) library in ways that are relevant to our interests.
More specifically, new [getter functions](https://napalm.readthedocs.io/en/latest/support/index.html#getters-support-matrix) have been implemented to pull
data from routers and parse it into a vender agnostic format.

The following platforms all have their own `umnet-napalm` drivers. Most of these inherit from other libraries.
* `ASA` does not inherit - the NAPALM community ASA driver uses the web API which is currently impractical for us.
* `IOS` inherits `napalm.ios.IOSDriver`
* `IOSXRNetconf` inherits `napalm.iosxr_netconf.IOSXRNETCONFDriver`
* `Junos` inherits `napalm.junos.JunOSDriver`
* `NXOS` inherits `napalm.nxos_ssh.NXOSSSHDriver`
* `PANOS` does not inherit - the NAPALM community PANOS driver but it doesn't support connecting via Panorama.

See the `umnet_napalm` [Abstract Base Class](https://github.com/umich-its-networking/umnet-napalm/blob/main/umnet_napalm/abstract_base.py) definition to see what commands are supported across all platforms. For platforms that inherit from core NAPALM drivers, refer to the [getter matrix](https://napalm.readthedocs.io/en/latest/support/index.html#getters-support-matrix). For PANOS see [napalm-panos repo](https://github.com/napalm-automation-community/napalm-panos)

## Using umnet-napalm
When you install the code it comes with a cli script called `umnet-napalm-get`. You can use this to run a command against a particular device. Note that umnet-napalm doesn't inherently
know the platform or the credentials to use. You can supply all of these on the cli as arguments, or you can set the credentials as environment variables. Here are the different environment
variables you can set:
```
export NAPALM_PASSWORD=<redacted>
export NAPALM_USERNAME=automaton
export NAPALM_ENABLE=<redacted>

## only if you want to query ngfw devices
export PANORAMA_API_KEY=<redacted>
```
Note you currently can't pass a Panorama API key as a cli argument (because that's just messy) - you must set it in your environment. When querying a Panos device via Panorama you must provide
`--pan-host [panorama hostname]` and  `--pan-serial [serial number of the firewall]`

Here's some quick examples. You can reference `umnet_napalm.models` for expected output format. Output is in json:
```
amylieb@wintermute:~/src/agador$ umnet-napalm-get dl-arbl-1 nxos_ssh get_inventory
[{'name': 'Slot 1',
  'part_number': 'N9K-C93360YC-FX2',
  'serial_number': 'FDO261320CY',
  'type': 'linecard'},
 {'name': 'Fan 1',
  'part_number': 'NXA-FAN-160CFM-PI',
  'serial_number': 'N/A',
  'type': 'fan'},
....
amylieb@wintermute:~/src/agador$ umnet-napalm-get r-seb junos get_lag_interfaces
{'ae0': {'admin_up': True,
         'members': {'et-0/1/0': {'admin_up': False,
                                  'flags': 'AF',
                                  'oper_up': False}},
         'mlag_id': 0,
         'oper_up': False,
         'peer_link': False,
         'protocol': 'LACP'},
 'ae1': {'admin_up': True,
         'members': {'ge-11/1/0': {'admin_up': False,
                                   'flags': 'AF',
                                   'oper_up': False},
                     'ge-11/3/7': {'admin_up': False,
                                   'flags': 'AF',
                                   'oper_up': False}},
         'mlag_id': 0,
         'oper_up': False,
         'peer_link': False,
         'protocol': 'LACP'},**
amylieb@wintermute:~/src/agador$ umnet-napalm-get ngfw-1 panos get_active_routes --pan-host panorama-1 --pan-serial 010701000554
[{'age': 1874469,
  'learned_from': '10.250.0.114',
  'mpls_label': [],
  'nh_interface': None,
  'nh_ip': '10.250.0.114',
  'nh_table': 'default',
  'prefix': '0.0.0.0/0',
  'protocol': 'BGP',
  'vrf': 'default',
  'vxlan_endpoint': None,
  'vxlan_vni': None},
 {'age': 1874469,
  'learned_from': '10.224.191.241',
  'mpls_label': [],
  'nh_interface': 'ethernet2/14.233',
  'nh_ip': '10.224.191.241',
  'nh_table': 'default',
  'prefix': '10.224.14.32/29',
  'protocol': 'OSPF',
  'vrf': 'default',
  'vxlan_endpoint': None,
  'vxlan_vni': None},
....
```


