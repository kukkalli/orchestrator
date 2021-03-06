import logging

from templates.service_profile_template import ServiceProfileTemplate
from tosca.vm_requirement import VMRequirement
from tosca.virtual_link import VirtualLink
from typing import List, Dict

LOG = logging.getLogger(__name__)


class TOSCAInput:

    def __init__(self, request_id, service_template: ServiceProfileTemplate, delay: int = 50):
        self.request_id = request_id
        self.service_template = service_template
        self.vm_requirements = service_template.get_vm_requirements_list()
        self.vm_requirements_dict: Dict[int, VMRequirement] = {}
        for vm_requirement in self.vm_requirements:
            self.vm_requirements_dict[vm_requirement.int_id] = vm_requirement
        self.v_links = service_template.get_v_links_list()
        self.delay = delay  # delay time in ms

    """
    def __init__(self, request_id, vm_requirements: List[VMRequirement], v_links: List[VirtualLink], delay: int = 50):
        self.request_id = request_id
        self.vm_requirements = vm_requirements
        self.vm_requirements_dict: Dict[int, VMRequirement] = {}
        for vm_requirement in vm_requirements:
            self.vm_requirements_dict[vm_requirement.int_id] = vm_requirement
        self.v_links = v_links
        self.delay = delay  # delay time in ms
    """

    def add_vm(self, vm_requirement: VMRequirement):
        self.vm_requirements.append(vm_requirement)

    def add_vlink(self, v_link: VirtualLink):
        self.v_links.append(v_link)

    def get_vm_requirement_by_id(self, _id: int) -> VMRequirement:
        try:
            return self.vm_requirements_dict[_id]
        except RuntimeError:
            LOG.error("Invalid VM id")

    def build(self):
        for v_link in self.v_links:
            try:
                self.vm_requirements_dict[v_link.dst_node_id].add_in_v_link(v_link)
                self.vm_requirements_dict[v_link.src_node_id].add_out_v_link(v_link)
            except RuntimeError:
                LOG.error("Invalid link and VM mapping")
