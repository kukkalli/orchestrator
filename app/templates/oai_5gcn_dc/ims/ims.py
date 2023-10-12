import logging

from templates.oai_5gcn_dc.ims.ims_user_data import IMSUserData
from templates.user_data.prepared_image_template import PreparedImageVMTemplate

LOG = logging.getLogger(__name__)


class IMS(PreparedImageVMTemplate):

    def __init__(self, prefix: str, name: str, flavor: str = "3"):
        super().__init__(prefix, name, flavor)
        self.vm_name = prefix + "-" + name
        self.name = name
        self.user_data = self.get_user_data() + IMSUserData.USERDATA


def main():
    vmt = IMS("oai", "ims")
    print("Image ID: {}\nUserData: {}".format(vmt.image_id, vmt.user_data))
    exit()


if __name__ == "__main__":
    main()
