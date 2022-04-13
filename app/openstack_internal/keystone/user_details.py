import logging

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack.connection import Connection

LOG = logging.getLogger(__name__)


class User:
    def __init__(self, connection: Connection):
        self.__connection = connection

    def get_users_list(self):
        return self.__connection.list_users()

    def get_user_by_name(self, user_name):
        return self.__connection.search_users(name_or_id=user_name)


def main():
    auth = AuthenticateConnection()
    user_obj = User(auth.get_connection())

    for user in user_obj.get_users_list():
        print("Get User name: {}, User id: {}".format(user.name, user.id))

    for user in user_obj.get_user_by_name('admin'):
        print("Admin: Get User name: {}, User id: {}".format(user.name, user.id))


if __name__ == "__main__":
    main()
