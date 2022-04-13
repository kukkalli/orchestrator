import logging
from typing import List, Dict

LOG = logging.getLogger(__name__)


class VMTemplate:

    def __init__(self):
        self.flavor = "2"
        self.image_id = "af8b3413-3d71-429e-83e1-de279bc2f4ea"
        self.ip_addresses: Dict[str, str] = {}
        self.networks: List[Dict[str, str]] = [{"net-id": "a0ebb620-d0e6-44d9-b584-489e841bc796"},
                                               {"net-id": "9e373e2c-0372-4a06-81a1-bc1cb4c62b85"}]
        self.vm_name = "template"

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

