import logging
from typing import List, Dict

from templates.common_user_data import CommonUserData
from tosca.virtual_link import VirtualLink

LOG = logging.getLogger(__name__)


class VMTemplate:

    def __init__(self, sc_name: str = "template", name: str = "network-function", flavor: str = "2",
                 user_data: str = "exit 0"):
        self.vm_name = sc_name + "-" + name
        self.name = name
        self.flavor = flavor
        self.image_id = "af8b3413-3d71-429e-83e1-de279bc2f4ea"
        self.ip_addresses: Dict[str, str] = {}
        self.networks: List[Dict[str, str]] = [{"net-id": "d2a49c41-6f42-486d-b96a-212b0b933273"},
                                               {"net-id": "200cd190-6171-4b26-aa83-e42f447ba90a"}]
        self.user_data = CommonUserData.USERDATA + user_data
        self.in_v_links: List[VirtualLink] = []
        self.out_v_links: List[VirtualLink] = []

    def get_flavour(self):
        return self.flavor

    def get_image_id(self):
        return self.image_id

    def get_ip_addresses(self):
        return self.ip_addresses

    def get_networks(self):
        return self.networks

    def get_vm_name(self):
        return self.vm_name

    def get_user_data(self):
        return self.user_data
