import logging
from typing import List


from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.nova.flavor import Flavor
from openstack_internal.nova.hypervisor_details import OSHypervisor
from openstack.connection import Connection

LOG = logging.getLogger(__name__)


class Nova:
    def __init__(self, connection: Connection):
        self.__connection = connection

    def close_connection(self) -> None:
        self.__connection.close()

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

    def get_hypervisor_list(self) -> List[OSHypervisor]:
        hypervisor_list: List[OSHypervisor] = []
        for hypervisor in self.__connection.list_hypervisors():
            hypervisor_list.append(OSHypervisor(hypervisor))
        return hypervisor_list

    def get_hypervisor_by_id(self, hypervisor_id: str) -> OSHypervisor:
        return OSHypervisor(self.__connection.compute.find_hypervisor(hypervisor_id))

    def get_hypervisor_by_name(self, hypervisor_name: str) -> OSHypervisor:
        return OSHypervisor(self.__connection.compute.find_hypervisor(hypervisor_name))


def main():
    auth = AuthenticateConnection()
    nova = Nova(auth.get_connection())
    for flavor in nova.get_flavors_list():
        print("Get Flavor name: {}, Flavor id: {}, Flavor details: {}".format(flavor.name, flavor.id, flavor))
    flavor = nova.get_flavor_by_id("1")
    print("Get Flavor name: {}, id: {}, vcpus: {}, ram: {}, disk: {}".format(flavor.name, flavor.id, flavor.vcpus,
                                                                             flavor.ram, flavor.disk))
    for hypervisor in nova.get_hypervisor_list():
        print("name: {}, id: {}, available vcpus: {}, ip: {}"
              .format(hypervisor.get_name(), hypervisor.get_id(), hypervisor.get_available_vcpus(),
                      hypervisor.get_host_ip()))

    hypervisor = nova.get_hypervisor_by_id('97582edb-4ab7-4190-ab14-243349e43c67')
    print("Get hypervisor id details: {}".format(hypervisor.get_host_ip()))
    auth.close_connection()


if __name__ == "__main__":
    main()
