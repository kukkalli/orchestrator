import logging
from typing import List, Dict

from templates.input_request import InputRequest
from templates.service_profile_template import ServiceProfileTemplate
from tosca.vm_requirement import VMRequirement
from tosca.virtual_link import VirtualLink

LOG = logging.getLogger(__name__)


class TOSCAInput:

    def __init__(self, input_request: InputRequest):
        self.request_id: str = input_request.get_service_chain_name()
        self.service_template: ServiceProfileTemplate = input_request.get_service_template()
        self.vm_requirements: List[VMRequirement] = self.service_template.get_vm_requirements_list()
        self.vm_requirements_dict: Dict[int, VMRequirement] = {}
        for vm_requirement in self.vm_requirements:
            self.vm_requirements_dict[vm_requirement.int_id] = vm_requirement
        self.v_links = self.service_template.get_v_links_list()
        # delay time in ms
        self.delay = input_request.max_link_delay
        # vm_name to fabric ip dictionary
        self.vm_ip_dict: Dict[str, str] = {}

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
