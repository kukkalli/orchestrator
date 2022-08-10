import logging

from keystoneclient.v3.client import Client as KeystoneClient
from glanceclient.v2.client import Client as GlanceClient
from novaclient.client import Client as NovaClient
from novaclient.v2.client import Client as NovaV2Client
from neutronclient.v2_0.client import Client as NeutronClient
from openstack.connection import Connection

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.openstack_constants import OpenStackConstants

LOG = logging.getLogger(__name__)


class Clients:

    def __init__(self, authenticate: AuthenticateConnection):
        self.__auth = authenticate

    def get_connection(self) -> Connection:
        return self.__auth.get_connection()

    def get_keystone_client(self) -> KeystoneClient:
        return KeystoneClient(session=self.__auth.get_session())

    def get_glance_client(self) -> GlanceClient:
        return GlanceClient(endpoint=OpenStackConstants.GLANCE_URL, token=self.__auth.get_token(),
                            version=OpenStackConstants.GLANCE_VERSION)

    def get_nova_client(self) -> NovaClient:
        return NovaClient(session=self.__auth.get_session(), version=OpenStackConstants.NOVA_VERSION)

    def get_neutron_client(self) -> NeutronClient:
        return NeutronClient(endpoint_url=OpenStackConstants.NEUTRON_URL, token=self.__auth.get_token())


def test_keystone(clients: Clients):
    for user in clients.get_connection().list_users():
        print("User id: {}, User Name: {}".format(user.id, user.name))
    print("Keystone Client: {}".format(clients.get_keystone_client()))


def test_glance(clients: Clients):
    print("Glance Client: {}".format(clients.get_glance_client()))


def test_nova(clients: Clients):
    nova = clients.get_nova_client()
    """
    print("Nova Client: {}".format(nova))
    print("Nova Server list:", nova.servers.list())
    print('Server: ', dir(nova.servers.list()))
    print('----------------------------------------------------')
    for item in nova.servers.list():
        print('Server: ', dir(item))
        print('Server Name: ', item.image)
        print('Server Name: ', item.name)
        print('Server ID: ', item.id)
        print('Server Compute Node: ', getattr(item, 'OS-EXT-SRV-ATTR:hypervisor_hostname'))
        print('----------------------------------------------------')
    """

    for hypervisor in nova.hypervisors.list():
        print('Hypervisor: ', dir(hypervisor))
        print('Hypervisor ID: ', hypervisor.id)
        print('Hypervisor _info: ', hypervisor._info)
        print('Hypervisor api_version: ', hypervisor.api_version)
        print('Hypervisor append_request_ids: ', hypervisor.append_request_ids)
        print('Hypervisor cpu_info: ', hypervisor.cpu_info)
        print('Hypervisor current_workload: ', hypervisor.current_workload)
        print('Hypervisor disk_available_least: ', hypervisor.disk_available_least)
        print('Hypervisor free_disk_gb: ', hypervisor.free_disk_gb)
        print('Hypervisor human_id: ', hypervisor.human_id)
        print('Hypervisor free_ram_mb: ', hypervisor.free_ram_mb)
        print('Hypervisor hypervisor_type: ', hypervisor.hypervisor_type)
        print('Hypervisor host_ip: ', hypervisor.host_ip)
        print('Hypervisor human_id: ', hypervisor.human_id)
        print('Hypervisor hypervisor_hostname: ', hypervisor.hypervisor_hostname)
        print('Hypervisor hypervisor_type: ', hypervisor.hypervisor_type)
        print('Hypervisor hypervisor_version: ', hypervisor.hypervisor_version)
        print('Hypervisor is_loaded(): ', hypervisor.is_loaded())
        print('Hypervisor local_gb: ', hypervisor.local_gb)
        print('Hypervisor local_gb_used: ', hypervisor.local_gb_used)
        print('Hypervisor manager: ', hypervisor.manager)
        print('Hypervisor memory_mb: ', hypervisor.memory_mb)
        print('Hypervisor memory_mb_used: ', hypervisor.memory_mb_used)
        print('Hypervisor request_ids: ', hypervisor.request_ids)
        print('Hypervisor request_ids_setup: ', hypervisor.request_ids_setup)
        print('Hypervisor running_vms: ', hypervisor.running_vms)
        print('Hypervisor service: ', hypervisor.service)
        print('Hypervisor state: ', hypervisor.state)
        print('Hypervisor status: ', hypervisor.status)
        print('Hypervisor vcpus: ', hypervisor.vcpus)
        print('Hypervisor vcpus_used: ', hypervisor.vcpus_used)
        print('Hypervisor x_openstack_request_ids: ', hypervisor.x_openstack_request_ids)
        print('----------------------------------------------------')


def test_neutron(clients: Clients):
    neutron = clients.get_neutron_client()
    for network in neutron.list_networks():
        print('Networks: {}'.format(network))


def main():
    clients = Clients(AuthenticateConnection())
    # test_keystone(clients)
    # test_glance(clients)
    test_nova(clients)
    # test_neutron(clients)


if __name__ == "__main__":
    main()
