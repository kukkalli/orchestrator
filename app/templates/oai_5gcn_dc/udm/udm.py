import logging

from templates.oai_5gcn_dc.udm.udm_user_data import UDMUserData
from templates.user_data.prepared_image_template import PreparedImageVMTemplate

LOG = logging.getLogger(__name__)


class UDM(PreparedImageVMTemplate):

    def __init__(self, prefix: str, name: str, flavor: str = "3"):
        super().__init__(prefix, name, flavor)
        self.vm_name = prefix + "-" + name
        self.name = name
        self.user_data = self.get_user_data() + UDMUserData.USERDATA


def main():
    vmt = UDM("oai", "udm")
    print("Image ID: {}\nUserData: {}".format(vmt.image_id, vmt.user_data))
    exit()


if __name__ == "__main__":
    main()
