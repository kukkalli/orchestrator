import logging

from templates.four_g_core.mme_user_data import MMEUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class MMETemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "3"
        self.vm_name = name+"-mme"
        self.name = "mme"
        self.user_data = self.get_user_data() + MMEUserData.USERDATA

