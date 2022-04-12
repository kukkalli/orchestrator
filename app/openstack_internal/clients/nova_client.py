from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.clients.clients import Clients


class NovaClient:

    def __init__(self, session: AuthenticateConnection):
        self.__conn = session.get_connection()
        self.__client = Clients(session).get_nova_client()


