import logging
from typing import List

from templates.vm_template import VMTemplate
from tosca.virtual_link import VirtualLink

LOG = logging.getLogger(__name__)


class VMRequirement:

    def __init__(self, int_id: int, network_function: VMTemplate, key_pair: str = None, subnet_mask: str = "/32",
                 security_groups: List[str] = ["default"]):
        self.__id = network_function.vm_name
        self.name = network_function.name
        self.hostname = network_function.vm_name
        self.__int_id = int_id
        self.flavor = network_function.flavor
        self.image_name = network_function.image_name
        self.image_id = network_function.image_id
        self.networks = network_function.networks
        self.key_pair = key_pair
        self.ip_addresses = network_function.ip_addresses
        self.subnet_mask = subnet_mask
        self.security_groups = security_groups
        self.hypervisor_hostname = ""
        self.in_v_links: List[VirtualLink] = []
        self.out_v_links: List[VirtualLink] = []

    """
    def __init__(self, int_id: int, hostname: str, flavor: str, image_id: str, networks: List[Dict[str, str]],
                 key_pair: str = None, ip_addresses: Dict[str, str] = {}, subnet_mask: str = "/32",
                 security_groups: [str] = ["default"]):
        self.__id = hostname
        self.hostname = hostname
        self.__int_id = int_id
        self.flavor = flavor
        self.image_id = image_id
        self.networks = networks
        self.key_pair = key_pair
        self.ip_addresses = ip_addresses
        self.subnet_mask = subnet_mask
        self.security_groups = security_groups
        self.hypervisor_hostname = ""
        self.in_v_links: List[VirtualLink] = []
        self.out_v_links: List[VirtualLink] = []
    """

    @property
    def id(self):
        return self.__id

    @property
    def int_id(self):
        return self.__int_id

    def add_in_v_link(self, v_link: VirtualLink):
        self.in_v_links.append(v_link)

    def add_out_v_link(self, v_link: VirtualLink):
        self.out_v_links.append(v_link)
