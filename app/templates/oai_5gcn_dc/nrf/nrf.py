import logging

from templates.oai_5gcn_dc.nrf.nrf_user_data import NRFUserData
from templates.user_data.prepared_image_template import PreparedImageVMTemplate

LOG = logging.getLogger(__name__)


class NRF(PreparedImageVMTemplate):

    def __init__(self, prefix: str, name: str, flavor: str = "3"):
        super().__init__(prefix, name, flavor)
        self.vm_name = prefix + "-" + name
        self.name = name
        # self.image_name: str = OAI5GConstants.OAI_5GCN_NRF_VMI
        # self.image_id: str | None = Glance().get_image_id(self.image_name)
        self.user_data = self.get_user_data() + NRFUserData.USERDATA


def main():
    mysql = NRF("oai", "nrf")
    print("Image ID: {}\nUserData: {}".format(mysql.image_id, mysql.user_data))
    exit()


if __name__ == "__main__":
    main()
