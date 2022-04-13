import logging

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack.connection import Connection

LOG = logging.getLogger(__name__)


class Glance:

    def __init__(self, connection: Connection):
        self.__connection = connection

    def get_image_list(self):
        return self.__connection.image.images()

    def get_image_by_id(self, image_id):
        return self.__connection.get_image_by_id(image_id)


def main():
    auth = AuthenticateConnection()
    glance = Glance(auth.get_connection())
    for image in glance.get_image_list():
        print("Image name {}: Image id: {}".format(image.name, image.id))

    image = glance.get_image_by_id('0af72659-a5c0-40a3-8b55-0b398e6b94f2')
    print("Image name {}: Image id: {}".format(image.name, image.id))


if __name__ == "__main__":
    main()
