import logging
from typing import List, Dict

LOG = logging.getLogger(__name__)


class VMTemplate:

    def __init__(self):
        self.flavor = "2"
        self.image_id = "af8b3413-3d71-429e-83e1-de279bc2f4ea"
        self.ip_addresses: Dict[str, str] = {}
        self.networks: List[Dict[str, str]] = [{"net-id": "d2a49c41-6f42-486d-b96a-212b0b933273"},
                                               {"net-id": "200cd190-6171-4b26-aa83-e42f447ba90a"}]
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

