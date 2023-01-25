import logging

from templates.four_g_core.spgwc_user_data import SPGWCUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class SPGWCTemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "2"
        self.vm_name = name+"-spgw-c"
        self.name = "spgw-c"
        self.user_data = self.get_user_data() + SPGWCUserData.USERDATA

