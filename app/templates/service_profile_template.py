from typing import List

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.nova.nova_details import Nova
from tosca.virtual_link import VirtualLink
from tosca.vm_requirement import VMRequirement


class ServiceProfileTemplate:

    def __init__(self, name: str, domain_name: str, bandwidth: int):
        self.name = name
        self.domain_name = domain_name
        self.bandwidth = bandwidth
        self.vm_requirements: List[VMRequirement] = []
        self.v_links: List[VirtualLink] = []
        self.nova = Nova(AuthenticateConnection().get_connection())

    def get_vm_requirements_list(self):
        return self.vm_requirements

    def get_v_links_list(self):
        return self.v_links
