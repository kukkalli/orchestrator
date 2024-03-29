import logging
from typing import List, Dict

from openstack_internal.openstack_constants import OpenStackConstants
from tosca.virtual_link import VirtualLink

LOG = logging.getLogger(__name__)


class VMTemplate:

    def __init__(self, prefix: str = "template", name: str = "network-function", flavor: str = "2",
                 user_data: str = "", image_name: str = OpenStackConstants.UBUNTU_18_04):
        self.vm_name = prefix + "-" + name
        self.name = name
        self.flavor = flavor
        self.image_name: str = image_name
        self.image_id: str = "4dc9d880-672a-4eb9-b93e-49540e263657"
        self.ip_addresses: Dict[str, str] = {}
        self.networks: List[Dict[str, str]] = [{"net-id": ""}]
        self.user_data = user_data
        self.in_v_links: List[VirtualLink] = []
        self.out_v_links: List[VirtualLink] = []
        self.key_pair = "hanif-kukkalli"

    def get_flavour(self) -> str:
        return self.flavor

    def get_image_id(self) -> str:
        return self.image_id

    def get_image_name(self) -> str:
        return self.image_name

    def get_ip_addresses(self) -> Dict[str, str]:
        return self.ip_addresses

    def get_networks(self) -> List[Dict[str, str]]:
        return self.networks

    def get_vm_name(self) -> str:
        return self.vm_name

    def get_name(self) -> str:
        return self.name

    def get_user_data(self) -> str:
        return self.user_data

    def create_vm(self):
        pass
