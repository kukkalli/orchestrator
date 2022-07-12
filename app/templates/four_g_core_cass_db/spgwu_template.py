import logging

from templates.four_g_core.spgwu_user_data import SPGWUUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class SPGWUTemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "3"
        self.vm_name = name+"-spgw-u"
        self.name = "spgw-u"
        self.user_data = self.get_user_data() + SPGWUUserData.USERDATA

