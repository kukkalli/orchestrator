import logging
from typing import List, Dict

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.clients.clients import Clients
from openstack_internal.glance.glance_details import Glance
from openstack_internal.nova.keypair_details import KeyPair
from openstack_internal.neutron.neutron_details import Neutron
from openstack_internal.nova.nova_details import Nova
from openstack_internal.keystone.project_details import Project
from openstack_internal.keystone.user_details import User

from novaclient.v2.client import Client as NovaV2Client

from templates.hss_docker import HSSDocker

LOG = logging.getLogger(__name__)


class VirtualMachine(object):

    def __init__(self, vm_id: str):
        self.__id = vm_id
        self.authenticate = AuthenticateConnection()
        self.connection = self.authenticate.get_connection()
        self.__clients = Clients(self.authenticate)
        self.__glance = Glance(self.connection)
        self.__keypair = KeyPair(self.connection)
        self.__neutron = Neutron(self.connection)
        self.__nova = Nova(self.connection)
        self.__project = Project(self.connection)
        self.__user = User(self.connection)

    def create_virtual_machine(self, name, image, flavor=2, vm_count=1, security_groups: list = None,
                               userdata: str = "", key_pair=None, networks: list = None, host=None):
        if security_groups is None:
            security_groups = ["default"]
        if networks is None:
            networks = [{"net-id": "a0ebb620-d0e6-44d9-b584-489e841bc796", "v4-fixed-ip": "10.10.1.50"},
                        {"net-id": "9e373e2c-0372-4a06-81a1-bc1cb4c62b85", "v4-fixed-ip": "10.11.1.50"}]
        nova_client: NovaV2Client = self.__clients.get_nova_client()
        return nova_client.servers.create(name=name, image=image, flavor=flavor, min_count=vm_count, max_count=vm_count,
                                          security_groups=security_groups, userdata=userdata, key_name=key_pair, admin_pass=None,
                                          nics=networks, access_ip_v4=None, access_ip_v6=None, host=host,
                                          hypervisor_hostname=None)

    def get_vm_info(self):
        nova = self.__get_nova_api()
        return nova.get_hypervisor_by_id(self.__id)

    def get_image_info(self):
        self.get_glance_api().get_image_by_id()
        return

    def get_vm_host(self):
        self.__get_nova_api()
        return

    def get_ips(self):
        nova = self.__get_nova_api()
        nova.get_hypervisor_by_id(self.__id)

        return

    def get_glance_api(self):
        return self.__glance

    def get_keypair_api(self):
        return self.__keypair

    def get_neutron_api(self):
        return self.__neutron

    def __get_nova_api(self):
        return self.__nova

    def get_project_api(self):
        return self.__project

    def get_user_api(self):
        return self.__user

    def close_connection(self):
        self.authenticate.close_connection()


def main():
    vm = VirtualMachine("prof-hss")
    name = "prof-hss"
    image = "af8b3413-3d71-429e-83e1-de279bc2f4ea"
    security_groups = ["default"]
    # key_pair = "compute01"
    neutron = Neutron(AuthenticateConnection().get_connection())
    networks = [{"net-id": "a0ebb620-d0e6-44d9-b584-489e841bc796"},
                {"net-id": "9e373e2c-0372-4a06-81a1-bc1cb4c62b85"}]
    for network in networks:
        print(f"network: {network}")
        network["v4-fixed-ip"] = neutron.get_available_ip(network["net-id"])
    print(f"networks: {networks}")

    host = "compute02.etit.tu-chemnitz.de"
    domain = "tu-chemnitz.de"
    server = vm.create_virtual_machine(name, image, flavor=2, security_groups=security_groups,
                                       userdata=HSSDocker.USERDATA.format(domain), key_pair=None, networks=networks, host=host)
    print("Created HSS Server: {}".format(server))


if __name__ == "__main__":
    main()
