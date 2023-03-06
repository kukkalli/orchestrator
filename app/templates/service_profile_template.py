import logging
import time
from typing import Dict, List

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.nova.flavor import Flavor
from openstack_internal.nova.nova_details import Nova
from templates.vm_template import VMTemplate
from tosca.virtual_link import VirtualLink
from tosca.vm_requirement import VMRequirement

LOG = logging.getLogger(__name__)


class ServiceProfileTemplate:

    def __init__(self, name: str, domain_name: str, bandwidth: int, max_delay: float = 50.0):
        self.name = name
        self.domain_name = domain_name
        self.bandwidth = bandwidth
        self.max_delay = max_delay
        self.network_functions: List[VMTemplate] = []
        self.vm_requirements_list: List[VMRequirement] = []
        self.vnf_vm_map: Dict[str, VMRequirement] = {}
        self.nfv_v_links_list: List[Dict] = []
        self.v_links: List[VirtualLink] = []
        nova = Nova(AuthenticateConnection())
        self.flavor_id_map: Dict[str, Flavor] = nova.get_flavor_id_map()
        nova.close_connection()
        self.vm_user_data_dict: Dict[str, str] = {}

    def get_vm_requirements_list(self):
        return self.vm_requirements_list

    def get_v_links_list(self):
        return self.v_links

    def get_network_functions(self):
        return self.network_functions

    def build(self):
        LOG.info(f"Build ServiceProfileTemplate: {time.time()}")
        print(f"Build ServiceProfileTemplate: {time.time()}")
        for index, network_function in enumerate(self.network_functions):
            LOG.info(f"Network Function Name: {network_function.name}, Index: {index}")
            vm_request = VMRequirement(int_id=index, network_function=network_function)
            # vm_request = VMRequirement(int_id=index, hostname=network_function.vm_name,
            # flavor=network_function.flavor, image_id=network_function.image_id, networks=network_function.networks,
            # ip_addresses=network_function.ip_addresses)

            self.vnf_vm_map[network_function.name] = vm_request
            self.vm_requirements_list.append(vm_request)

        for index, link in enumerate(self.nfv_v_links_list):
            v_link = VirtualLink(link['out'] + "-" + link['in'], index, self.vnf_vm_map.get(link['in']).int_id,
                                 self.vnf_vm_map.get(link['out']).int_id, self.bandwidth, link['delay'])
            # self.vnf_vm_map.get(link['out']).out_v_links.append(v_link)
            # self.vnf_vm_map.get(link['in']).in_v_links.append(v_link)
            self.v_links.append(v_link)

        LOG.info(f"Built ServiceProfileTemplate: {time.time()}")
        print(f"Built ServiceProfileTemplate: {time.time()}")

    def populate_user_data(self, nf_ip_dict: Dict[str, str]) -> Dict[str, str]:
        LOG.debug(f"I am in service profile template, {self.domain_name}")
        print(f"I am in service profile template, {self.domain_name}")
        self.vm_user_data_dict: Dict[str, str] = {}
        return {}
