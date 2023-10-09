import logging

from templates.oai_5gcn_dc.mysql.mysql_user_data import MySQLUserData
from templates.user_data.prepared_image_template import PreparedImageVMTemplate

LOG = logging.getLogger(__name__)


class MySQL(PreparedImageVMTemplate):

    def __init__(self, prefix: str, name: str, flavor: str = "3"):
        super().__init__(prefix, name, flavor)
        self.vm_name = prefix + "-" + name
        self.name = name
        self.user_data = self.get_user_data() + MySQLUserData.USERDATA


def main():
    mysql = MySQL("oai", "mysql")
    print("Image ID: {}\nUserData: {}".format(mysql.image_id, mysql.user_data))
    exit()


if __name__ == "__main__":
    main()
