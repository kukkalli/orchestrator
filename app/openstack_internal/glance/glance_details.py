import logging
from typing import List, Dict

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack.connection import Connection

from openstack_internal.openstack_constants import OpenStackConstants

LOG = logging.getLogger(__name__)


class Glance:

    def __init__(self):
        self.connection: Connection | None = None
        self.image_list = []
        self.image_name_id_dict: Dict[str, str] = {}

    def create_connection(self):
        self.connection = AuthenticateConnection().get_connection()

    def close_connection(self):
        self.connection.close()

    def get_image_list(self) -> List:
        self.create_connection()
        image_list = self.connection.list_images()
        self.close_connection()
        return image_list

    def get_image_by_id(self, image_id):
        self.create_connection()
        image = self.connection.get_image_by_id(image_id)
        self.close_connection()
        return image

    def get_image_id(self, image_name):
        self.create_connection()
        image_id = self.connection.get_image_id(image_name)
        self.close_connection()
        return image_id


def main():
    glance = Glance()
    for image in glance.get_image_list():
        print("Image name {}: Image id: {}".format(image.name, image.id))
    image_name = "bionic-server-cloudimg-amd64"
    image_id = glance.get_image_id(OpenStackConstants.UBUNTU_18_04)
    print(f"Image Id of {image_name} is {image_id}")

    image = glance.get_image_by_id(image_id)
    # print(f"image: {image}")
    print("Image name {}: Image id: {}".format(image.name, image.id))


if __name__ == "__main__":
    main()
