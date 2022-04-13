import logging

from configuration_constants import ConfigurationConstants
from openstack_internal.openstack_constants import OpenStackConstants
from openstack import connect
from keystoneauth1.identity.v3 import Password
from keystoneauth1.session import Session
from openstack.connection import Connection

LOG = logging.getLogger(__name__)


class AuthenticateConnection:
    """
    Authentication and provide the OpenStack Connection object
    """

    def __init__(self):
        self.__connection: Connection = connect(auth_url=OpenStackConstants.KEYSTONE_URL,
                                                project_name=ConfigurationConstants.OS_PROJECT_NAME,
                                                username=ConfigurationConstants.OS_USERNAME,
                                                password=ConfigurationConstants.OS_PASSWORD,
                                                region_name=ConfigurationConstants.OS_REGION,
                                                user_domain_name=ConfigurationConstants.OS_DOMAIN_NAME,
                                                project_domain_name=ConfigurationConstants.OS_DOMAIN_NAME,
                                                keystone_version=OpenStackConstants.KEYSTONE_VERSION,
                                                glance_version=OpenStackConstants.GLANCE_VERSION,
                                                nova_version=OpenStackConstants.NOVA_VERSION)

        self.__auth: Password = Password(auth_url=OpenStackConstants.KEYSTONE_URL,
                                         username=ConfigurationConstants.OS_USERNAME,
                                         user_domain_name=ConfigurationConstants.OS_DOMAIN_NAME,
                                         password=ConfigurationConstants.OS_PASSWORD,
                                         project_name=ConfigurationConstants.OS_PROJECT_NAME,
                                         project_domain_name=ConfigurationConstants.OS_DOMAIN_NAME)

        self.__sess: Session = Session(auth=self.__auth)

    def get_session(self) -> Session:
        return self.__sess

    def get_token(self) -> str:
        return self.get_session().get_token()

    def get_connection(self) -> Connection:
        return self.__connection

    def close_connection(self) -> None:
        self.__connection.close()


def test_identity(conn):
    for user in conn.list_users():
        print("Get Username: {}, id: {}".format(user.name, user.id))


def test_glance(conn):
    for image in conn.image.images():
        print("Get Image name: {}".format(image.name))
        # print("Get Images: {}".format(image))


def test_nova(conn):
    print("Compute: {}".format(dir(conn.compute)))
    print("Compute Version: {}".format(conn.compute.version))


def test_neutron(conn):
    for network in conn.list_networks():
        print("Get Network name: {}".format(network.name))


def main():
    auth = AuthenticateConnection()
    print("Get tokens: {}".format(auth.get_token()))
    conn = auth.get_connection()

    test_identity(conn)
    test_glance(conn)
    test_nova(conn)
    test_neutron(conn)


if __name__ == "__main__":
    main()
