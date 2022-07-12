import logging

from templates.four_g_core_cass_db.hss_user_data import HSSUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class HSS(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "2"
        self.vm_name = name+"-hss"
        self.name = "hss"
        self.user_data = self.get_user_data() + HSSUserData.USERDATA

