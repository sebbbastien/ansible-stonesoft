#!/usr/bin/python
# Copyright (c) 2017 David LePage
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: external_gw_facts
short_description: Facts about external VPN gateways
description:
  - An external vpn gateway is a non-SMC managed endpoint used for
    terminating a VPN. It defines the remote side networks and settings
    specific to handling VPN. Use I(expand) to specify attributes that
    should be resolved to raw data instead of href.

version_added: '2.5'

options:
  expand:
    description:
      - Expand sub elements that only provide href data. Specify a list of
        external gateways by name
    type: list
    choices:
      - vpn_site
      - gateway_profile
    
extends_documentation_fragment:
  - stonesoft
  - stonesoft_facts

requirements:
  - smc-python
author:
  - David LePage (@gabstopper)
'''


EXAMPLES = '''
- name: Facts related to external VPN gateways
  hosts: localhost
  gather_facts: no
  tasks:
  - name: Retrieve all external GW's
    external_gateway_facts:
  
  - name: Get a specific external GW details
    external_gateway_facts:
      filter: myremotevpn
  
  - name: Get a specific external GW, and expand supported attributes
    external_gateway_facts:
      filter: myremotevpn
      expand:
        - gateway_profile
        - vpn_site 
'''


RETURN = '''
external_gateway:
    description: Example external gateway data 
    returned: always
    type: list
    sample: [
        external_endpoint": [{
            "address": "33.33.33.35", 
            "balancing_mode": "active", 
            "dynamic": false, 
            "enabled": true, 
            "force_nat_t": true, 
            "ike_phase1_id_type": 3, 
            "ipsec_vpn": true, 
            "name": "endpoint2", 
            "nat_t": true, 
            "read_only": false, 
            "system": false, 
            "udp_encapsulation": false
        }], 
        "gateway_profile": "http://1.1.1.1:8082/6.4/elements/gateway_profile/3", 
        "name": "myremotevpn", 
        "read_only": false, 
        "system": false, 
        "trust_all_cas": true, 
        "trusted_certificate_authorities": [], 
        "vpn_site": [{
            "gateway": "http://1.1.1.1:8082/6.4/elements/external_gateway/47", 
            "name": "myremotevpn-site", 
            "read_only": false, 
            "site_element": [
                "http://1.1.1.1:8082/6.4/elements/network/708"
            ], 
            "system": false
        }]]
'''

from ansible.module_utils.stonesoft_util import (
    StonesoftModuleBase,
    format_element)


try:
    from smc.vpn.elements import ExternalGateway
except ImportError:
    pass

       
def to_dict(external_gw, expand=None):
    """
    Flatten the external gateway
    
    :param ExternalGateway external_gw
    :return dict
    """
    external_gw.data.update(external_endpoint=
        [format_element(ep) for ep in external_gw.external_endpoint])
    
    expand = expand if expand else []
    
    if 'gateway_profile' in expand:
        external_gw.data['gateway_profile'] = format_element(external_gw.gateway_profile)
    
    if 'vpn_site' in expand:
        vpn_site = []
        for site in external_gw.vpn_site:
            site.data['site_element'] = [format_element(s) for s in site.site_element]
            vpn_site.append(format_element(site))
        external_gw.data['vpn_site'] = vpn_site
    else:
        external_gw.data.update(vpn_site=
            [format_element(site) for site in external_gw.vpn_site])

    return format_element(external_gw)


def expandable():
    return ('vpn_site', 'gateway_profile')


class ExternalGWFacts(StonesoftModuleBase):
    def __init__(self):
        
        self.module_args = dict(
            expand=dict(type='list')
        )
        self.element = 'external_gateway'
        self.limit = None
        self.filter = None
        self.expand = None
        self.exact_match = None
        self.case_sensitive = None
        
        self.results = dict(
            ansible_facts=dict(
                external_gateway=[]
            )
        )
        super(ExternalGWFacts, self).__init__(self.module_args, is_fact=True)

    def exec_module(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        
        if self.expand:
            for specified in self.expand:
                if specified not in expandable():
                    self.fail(msg='Expandable attributes: {}, got: {}'.format(
                        expandable(), specified))
                    
        result = self.search_by_type(ExternalGateway)
        # Search by specific element type
        if self.filter:    
            elements = [to_dict(element, self.expand) for element in result]
        else:
            elements = [{'name': element.name, 'type': element.typeof} for element in result]
        
        self.results['ansible_facts']['external_gateway'] = elements
        return self.results

def main():
    ExternalGWFacts()
    
if __name__ == '__main__':
    main()
