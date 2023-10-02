import logging

from templates.user_data.prepared_image_common_user_data import CommonOAI5GCNUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class PreparedImageVMTemplate(VMTemplate):

    def __init__(self, prefix: str, name: str, flavor: str = "3"):
        super().__init__(prefix, name)
        self.flavor = flavor
        self.user_data = CommonOAI5GCNUserData.USERDATA
