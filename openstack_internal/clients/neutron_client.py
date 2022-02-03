from openstack_internal.authenticate.authenticate import AuthenticateConnection


class Neutron:

    def __init__(self, session: AuthenticateConnection):
        self.__conn = session.get_connection()

    def get_networks_list(self):
        networks_list = []
        for _network in self.__conn.list_networks():
            __network = {'id': _network.get('id'), 'name': _network.get('name')}
            networks_list.append(__network)
            print("Get Network dir: {}".format(dir(_network)))
            print("Get Network id: {} and name: {}".format(_network.get('id'), _network.get('name')))
        return networks_list

    def get_network_by_id(self, network_id):
        for _network in self.__conn.list_networks():
            if _network.get('id') == network_id:
                return _network
        return None


def main():
    auth = AuthenticateConnection()
    neutron = Neutron(auth)

    for network in neutron.get_networks_list():
        print("Get Network name: {}".format(network))


if __name__ == "__main__":
    main()
