from typing import List, Dict

"""
from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.neutron.neutron_details import Neutron
"""


class VMTemplate:

    def __init__(self):
        self.flavor = "2"
        self.image_id = "af8b3413-3d71-429e-83e1-de279bc2f4ea"
        self.ip_addresses: Dict[str, str] = {}
        self.networks: List[Dict[str, str]] = [{"net-id": "a0ebb620-d0e6-44d9-b584-489e841bc796"},
                                               {"net-id": "9e373e2c-0372-4a06-81a1-bc1cb4c62b85"}]
        self.vm_name = "template"
        # self.update_networks_with_ip()

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

    """
    def update_networks_with_ip(self):
        neutron = Neutron(AuthenticateConnection().get_connection())
        for network in self.networks:
            network["v4-fixed-ip"] = neutron.get_available_ip(network["net-id"])
            self.ip_addresses[network["net-id"]] = network["v4-fixed-ip"]
    """
