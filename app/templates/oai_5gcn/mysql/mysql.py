import logging

from openstack_internal.glance.glance_details import Glance
from templates.oai_5gcn.mysql.mysql_user_data import MySQLUserData
from templates.user_data.oai_5gcn_constants import OAI5GConstants
from templates.user_data.prepared_image_template import PreparedImageVMTemplate

LOG = logging.getLogger(__name__)


class MySQL(PreparedImageVMTemplate):

    def __init__(self, prefix: str, name: str, flavor: str = "3"):
        super().__init__(prefix, name, flavor)
        self.vm_name = prefix + "-" + name
        self.name = name
        self.image_name: str = OAI5GConstants.OAI_5GCN_MYSQL_VMI
        self.image_id: str | None = Glance().get_image_id(self.image_name)
        self.user_data = self.get_user_data() + MySQLUserData.USERDATA


def main():
    mysql = MySQL("oai", "mysql")
    print("Image ID: {}\nUserData: {}".format(mysql.image_id, mysql.user_data))
    exit()


if __name__ == "__main__":
    main()
