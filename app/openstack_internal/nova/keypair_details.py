import logging

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack.connection import Connection

LOG = logging.getLogger(__name__)


class KeyPair:
    def __init__(self, connection: Connection):
        self.__connection = connection

    def get_keypair_list(self, user_id, project_id):
        return self.__connection.list_keypairs(filters={'user_id': user_id, 'project_id': project_id})

    def get_keypair_by_id_or_name(self, keypair_id_or_name):
        return self.__connection.get_keypair(keypair_id_or_name)


def main():
    auth = AuthenticateConnection()
    key_pair_obj = KeyPair(auth.get_connection())

    for key_pair in key_pair_obj.get_keypair_list('c349d1ffd3b74fe68d1aa49d71cfce1b',
                                                  '6b5e1b91ce6d40a082004e7b60b614c4'):
        print("Get KeyPair name: {}, KeyPair id: {}".format(key_pair.name, key_pair.id))

    # key_pair = key_pair_obj.get_keypair_by_id_or_name('')
    # print("Get KeyPair name: {}".format(key_pair))


if __name__ == "__main__":
    main()
