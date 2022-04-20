import logging

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack.connection import Connection

LOG = logging.getLogger(__name__)


class Neutron:

    def __init__(self, connection: Connection):
        self.connection = connection
        self.ports_list = []

    def get_networks_list(self):
        networks_list = []
        for _network in self.connection.list_networks():
            __network = {'id': _network.get('id'), 'name': _network.get('name')}
            networks_list.append(__network)
            LOG.debug("Get Network dir: {}".format(dir(_network)))
            LOG.debug("Get Network id: {} and name: {}".format(_network.get('id'), _network.get('name')))
        return networks_list

    """
    def get_networks_list(self, project_id):
        return self.__connection.list_networks(filters={'project_id': project_id})
    """

    def get_network_by_name_or_id(self, name_or_id: str, filters=None):
        """Get Network By Name or ID

        :param name_or_id: Name or ID of the desired network.
        :param filters: a dict containing additional filters to use. e.g.
                        {'router:external': True}
        """
        return self.connection.get_network(name_or_id, filters)

    def get_network_by_id(self, network_id: str):
        LOG.debug(f"Network by Id: {self.connection.get_network_by_id(network_id)}")
        for _network in self.connection.list_networks():
            if _network.get('id') == network_id:
                return _network
        return None

    """
    def get_network_by_id(self, network_id):
        return self.connection.get_network_by_id(network_id)
    """

    def get_security_groups_list(self, project_id):
        return self.connection.list_security_groups(filters={'project_id': project_id})

    def get_security_group_by_id(self, security_group_id):
        return self.connection.get_security_group_by_id(security_group_id)

    def get_ip_address(self, network_id: str, name: str):
        return self.connection.create_port(network_id, name)

    def get_available_ip(self, network_id: str, is_delete: bool = True):
        port = self.connection.create_port(network_id)
        LOG.debug(f"Port details: {port}")
        LOG.debug(f"Port id: {port['id']}")
        ip_address = port.fixed_ips[0]['ip_address']
        LOG.debug(f"Available ip_address: {ip_address}")
        if is_delete:
            self.connection.delete_port(port)
        else:
            self.ports_list.append(port)

        return ip_address

    def get_available_ip_list(self, network_id: str, count: int = 1):
        ip_list = []
        for i in range(0, count):
            ip_list.append(self.get_available_ip(network_id=network_id, is_delete=False))
            self.connection.delete_port(self.ports_list[i].id)
            self.ports_list.remove(self.ports_list[i])
        return ip_list


def main():
    auth = AuthenticateConnection()
    neutron = Neutron(auth.get_connection())
    # project id '6b5e1b91ce6d40a082004e7b60b614c4'
    for network in neutron.get_networks_list():
        print("Get Network name: {}, network id: {}".format(network.get("name"), network.get("id")))

    print("---------------------------------------------------------------------------------------------------")
    print("Security Group: {}".format(neutron.get_security_group_by_id('ef249e36-3cf8-4ca5-a6ea-45107f4d5491').name))
    print("---------------------------------------------------------------------------------------------------")

    for sg in neutron.get_security_groups_list('6b5e1b91ce6d40a082004e7b60b614c4'):
        print("Get security group name: {}, security group id: {}".format(sg.name, sg.id))
        for rules in sg.security_group_rules:
            print("security group rule: {}".format(rules))

    for network in neutron.get_networks_list():
        print("Get Network name: {}".format(network))

    neutron.get_network_by_id("9e373e2c-0372-4a06-81a1-bc1cb4c62b85")
    neutron.get_available_ip("9e373e2c-0372-4a06-81a1-bc1cb4c62b85")
    ip_list = neutron.get_available_ip_list("9e373e2c-0372-4a06-81a1-bc1cb4c62b85", 4)
    for ip in ip_list:
        print(f"Returned IP is: {ip}")


if __name__ == "__main__":
    main()
