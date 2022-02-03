from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack.connection import Connection


class Neutron:

    def __init__(self, connection: Connection):
        self.__connection = connection

    def get_networks_list(self, project_id):
        return self.__connection.list_networks(filters={'project_id': project_id})

    def get_network_by_id(self, network_id):
        return self.__connection.get_network_by_id(network_id)

    def get_security_groups_list(self, project_id):
        return self.__connection.list_security_groups(filters={'project_id': project_id})

    def get_security_group_by_id(self, security_group_id):
        return self.__connection.get_security_group_by_id(security_group_id)


def main():
    auth = AuthenticateConnection()
    neutron = Neutron(auth.get_connection())

    for network in neutron.get_networks_list('6b5e1b91ce6d40a082004e7b60b614c4'):
        print("Get Network name: {}, network id: {}".format(network.name, network.id))

    print("---------------------------------------------------------------------------------------------------")
    print("Security Group: {}".format(neutron.get_security_group_by_id('ef249e36-3cf8-4ca5-a6ea-45107f4d5491').name))
    print("---------------------------------------------------------------------------------------------------")

    for sg in neutron.get_security_groups_list('6b5e1b91ce6d40a082004e7b60b614c4'):
        print("Get security group name: {}, security group id: {}".format(sg.name, sg.id))
        for rules in sg.security_group_rules:
            print("security group rule: {}".format(rules))


if __name__ == "__main__":
    main()
