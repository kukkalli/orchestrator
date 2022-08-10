import logging
from typing import List, Dict

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.clients.clients import Clients
from openstack_internal.nova.flavor import Flavor
from openstack_internal.nova.hypervisor_details import OSHypervisor

LOG = logging.getLogger(__name__)


class Nova:
    def __init__(self, auth: AuthenticateConnection):
        self.auth_connect = auth
        self.__connection = auth.get_connection()
        self.nova_client = Clients(self.auth_connect).get_nova_client()

    def close_connection(self) -> None:
        self.__connection.close()
        self.auth_connect.close_connection()

    def create_virtual_machine(self, vm_name, image=None, flavor=None, auto_ip=True, ips=None, ip_pool=None,
                               wait=False, network=None, key_pair=None, security_groups=None,
                               min_count=1):
        return self.__connection.create_server(vm_name, image=image, flavor=flavor, auto_ip=auto_ip, ips=ips,
                                               ip_pool=ip_pool, wait=wait, network=network, key_name=key_pair,
                                               security_groups=security_groups, min_count=min_count)

    def get_flavors_list(self):
        return self.__connection.compute.flavors()

    def get_flavor_by_id(self, flavor_id: str) -> Flavor:
        flavor = self.__connection.get_flavor_by_id(flavor_id)
        return Flavor(flavor)

    def get_flavor_id_map(self) -> Dict[str, Flavor]:
        flavor_dict: Dict[str, Flavor] = {}
        for os_flavor in self.get_flavors_list():
            flavor = Flavor(os_flavor)
            flavor_dict[flavor.id] = flavor
        return flavor_dict

    def get_hypervisor_list(self) -> List[OSHypervisor]:
        # auth = AuthenticateConnection()
        # nova_client = Clients(auth).get_nova_client()

        hypervisor_list: List[OSHypervisor] = []
        # self.__connection.list_hypervisors()
        hypervisors_list = self.nova_client.hypervisors.list()
        for hypervisor in hypervisors_list:
            hypervisor_list.append(OSHypervisor(hypervisor))
        return hypervisor_list

    def get_hypervisor_by_id(self, hypervisor_id: str) -> OSHypervisor:
        return OSHypervisor(self.__connection.compute.find_hypervisor(hypervisor_id))

    def get_hypervisor_by_name(self, hypervisor_name: str) -> OSHypervisor:
        return OSHypervisor(self.__connection.compute.find_hypervisor(hypervisor_name))


def main():
    auth = AuthenticateConnection()
    """
    nova_client = Clients(auth).get_nova_client()
    print(f"hypervisors: {dir(nova_client.hypervisors)}")
    hypervisors_list = nova_client.hypervisors.list()
    for hypervisor in hypervisors_list:
        print(f"hypervisors: {dir(hypervisor)}")
        print(f"hypervisors local_gb: {hypervisor.local_gb}")
        print(f"hypervisors local_gb_used: {hypervisor.local_gb_used}")
        print(f"hypervisors memory_mb: {hypervisor.memory_mb}")
        print(f"hypervisors memory_mb_used: {hypervisor.memory_mb_used}")
        print(f"hypervisors vcpus: {hypervisor.vcpus}")
        print(f"hypervisors vcpus_used: {hypervisor.vcpus_used}")
    """

    nova = Nova(auth)
    nova.get_hypervisor_list()
    """
    flavor_id_map = nova.get_flavor_id_map()

    for flavor in nova.get_flavors_list():
        print("Get Flavor name: {}, Flavor id: {}, Flavor details: {}".format(flavor.name, flavor.id, flavor))
        _flavor = Flavor(flavor)
        print(f"Get Flavor name: {_flavor.name}, id: {_flavor.id}, vcpus: {_flavor.vcpus},"
              f" ram: {_flavor.ram}, disk: {_flavor.disk}")

    flavor = flavor_id_map["2"]
    print(f"Get Flavor name: {flavor.name}, id: {flavor.id}, vcpus: {flavor.vcpus},"
          f" ram: {flavor.ram}, disk: {flavor.disk}")

    for hypervisor in nova.get_hypervisor_list():
        print(f"Hypervisor name: {hypervisor.get_available_vcpus()}, id: {hypervisor.get_id()},")
        # f" available vcpus: {hypervisor.get_available_vcpus()}, ip: {hypervisor.get_host_ip()}")

    hypervisor = nova.get_hypervisor_by_id('12098ef6-4a2b-48de-be98-d4535bb5ffae')
    print(f"Get hypervisor id details: {hypervisor.get_available_vcpus()}")
    """
    nova.close_connection()


if __name__ == "__main__":
    main()
