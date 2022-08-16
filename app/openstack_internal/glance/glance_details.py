import logging

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack.connection import Connection

LOG = logging.getLogger(__name__)


def get_image_list(connection: Connection) -> list:
    image_list = connection.image.images()
    connection.close()
    return image_list


class Glance:

    def __init__(self, connection: Connection):
        self.image_list = get_image_list(connection)
        self.image_name_id_dict: dict[str, str] = {}
        self.create_image_name_id_map()

    def create_image_name_id_map(self):
        for image in self.image_list:
            print(f"create map: image: id: {image.id}, name: {image.name}")
            self.image_name_id_dict[image.name] = image.id

    def get_image_list(self) -> list:
        return self.image_list

    def get_image_by_id(self, image_id):
        for image in self.image_list:
            if image.id == image_id:
                return image
        return None

    def get_image_id(self, image_name):
        return self.image_name_id_dict[image_name]

    def get_image_map(self) -> dict[str, str]:
        return self.image_name_id_dict


def main():
    auth = AuthenticateConnection()
    glance = Glance(auth.get_connection())
    for image in glance.get_image_list():
        print("Image name {}: Image id: {}".format(image.name, image.id))
    image_name = "bionic-server-cloudimg-amd64"
    image_id = glance.get_image_id(image_name)
    print(f"Image Id of {image_name} is {image_id}")
    """
    image = glance.get_image_by_id('0af72659-a5c0-40a3-8b55-0b398e6b94f2')
    print("Image name {}: Image id: {}".format(image.name, image.id))
    """


if __name__ == "__main__":
    main()
