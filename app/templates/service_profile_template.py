import logging
import time
from datetime import datetime
from typing import Dict, List

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.nova.flavor import Flavor
from openstack_internal.nova.nova_details import Nova
from templates.vm_template import VMTemplate
from tosca.virtual_link import VirtualLink
from tosca.vm_requirement import VMRequirement

LOG = logging.getLogger(__name__)


class ServiceProfileTemplate:

    def __init__(self, prefix: str, domain_name: str, bandwidth: int, max_delay: float = 50.0):
        self.prefix = prefix
        self.domain_name = domain_name
        self.bandwidth = bandwidth
        self.max_delay = max_delay
        self.network_functions: List[VMTemplate] = []
        self.vm_requirements_list: List[VMRequirement] = []
        self.vnf_vm_map: Dict[str, VMRequirement] = {}
        self.nfv_v_links_list: List[Dict[str, any]] = []
        self.v_links: List[VirtualLink] = []
        nova = Nova(AuthenticateConnection())
        self.flavor_id_map: Dict[str, Flavor] = nova.get_flavor_id_map()
        nova.close_connection()
        self.vm_user_data_dict: Dict[str, str] = {}

    def get_vm_requirements_list(self):
        return self.vm_requirements_list

    def get_v_links_list(self) -> List[VirtualLink]:
        return self.v_links

    def get_nfv_v_links_list(self) -> List[Dict]:
        return self.nfv_v_links_list

    def get_network_functions(self) -> List[VMTemplate]:
        return self.network_functions

    def build(self):
        start_time = time.time()
        date_time = datetime.fromtimestamp(start_time)
        LOG.info(f"Build ServiceProfileTemplate: {date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')}")
        print(f"Build ServiceProfileTemplate: {date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')}")
        for index, network_function in enumerate(self.network_functions):
            LOG.info(f"Network Function Name: {network_function.name}, Index: {index}")
            vm_request = VMRequirement(int_id=index, network_function=network_function)

            self.vnf_vm_map[network_function.name] = vm_request
            self.vm_requirements_list.append(vm_request)

        for index, link in enumerate(self.nfv_v_links_list):
            v_link = VirtualLink(link['out'] + "-" + link['in'], index, self.vnf_vm_map.get(link['in']).int_id,
                                 self.vnf_vm_map.get(link['out']).int_id, self.bandwidth, link['delay'])
            self.v_links.append(v_link)

        start_time = time.time()
        date_time = datetime.fromtimestamp(start_time)
        LOG.info(f"Built ServiceProfileTemplate: {date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')}")
        print(f"Built ServiceProfileTemplate: {date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')}")
        return self

    def populate_user_data(self, nf_ip_dict: Dict[str, str]) -> Dict[str, str]:
        LOG.debug(f"I am in service profile template, {self.domain_name}")
        # print(f"I am in service profile template, {self.domain_name}")
        self.vm_user_data_dict: Dict[str, str] = {}
        return {}
