import logging

from openstack_internal.authenticate.authenticate import AuthenticateConnection

LOG = logging.getLogger(__name__)


class Neutron:

    def __init__(self, session: AuthenticateConnection):
        self.__conn = session.get_connection()
        # self.__client = Clients(session).get_neutron_client()

    """
    def get_networks_list(self):
        networks_list = []
        for _network in self.__conn.list_networks():
            __network = {'id': _network.get('id'), 'name': _network.get('name')}
            networks_list.append(__network)
            LOG.debug("Get Network dir: {}".format(dir(_network)))
            LOG.debug("Get Network id: {} and name: {}".format(_network.get('id'), _network.get('name')))
        return networks_list
    """

    def get_network_by_id(self, network_id: str):
        LOG.debug(f"Network by Id: {self.__conn.get_network_by_id(network_id)}")
        for _network in self.__conn.list_networks():
            if _network.get('id') == network_id:
                return _network
        return None

    def get_available_ip(self, network_id: str):
        port = self.__conn.create_port(network_id)
        LOG.debug(f"Port details: {port}")
        LOG.debug(f"Port id: {port['id']}")
        self.__conn.delete_port(port.id)
        ip_address = port.fixed_ips[0]['ip_address']
        LOG.debug(f"Available ip_address: {ip_address}")
        return ip_address

    def get_available_ip_list(self, network_id: str, count: int = 1):
        ip_list = []
        for i in range(0, count):
            ip_list.append(self.get_available_ip(network_id))
        return ip_list


def main():
    """
    auth = AuthenticateConnection()
    neutron = Neutron(auth)

    for network in neutron.get_networks_list():
        print("Get Network name: {}".format(network))

    neutron.get_network_by_id("9e373e2c-0372-4a06-81a1-bc1cb4c62b85")
    neutron.get_available_ip("9e373e2c-0372-4a06-81a1-bc1cb4c62b85")
    ip_list = neutron.get_available_ip_list("9e373e2c-0372-4a06-81a1-bc1cb4c62b85", 4)
    for ip in ip_list:
        print(f"Returned IP is: {ip}")
    """


if __name__ == "__main__":
    main()
