from keystoneclient.v3.client import Client as KeystoneClient
from glanceclient.v2.client import Client as GlanceClient
from novaclient.client import Client as NovaClient
from novaclient.v2.client import Client as NovaV2Client
from neutronclient.v2_0.client import Client as NeutronClient
from openstack.connection import Connection

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.openstack_constants import OpenStackConstants


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

    def get_nova_client(self) -> NovaV2Client:
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


def test_neutron(clients: Clients):
    neutron = clients.get_neutron_client()
    for network in neutron.list_networks():
        print('Networks: {}'.format(network))


def main():
    clients = Clients(AuthenticateConnection())
    test_keystone(clients)
    test_glance(clients)
    test_nova(clients)
    test_neutron(clients)


if __name__ == "__main__":
    main()
