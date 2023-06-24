import logging

from templates.four_g_core.four_g_core_template import FourGCoreTemplate
from templates.four_g_core.hss_user_data import HSSUserData

LOG = logging.getLogger(__name__)


class HSSTemplate(FourGCoreTemplate):

    def __init__(self, prefix: str, nf_name: str):
        super().__init__(prefix, nf_name)
        self.flavor = "2"
        self.user_data = self.get_user_data() + HSSUserData.USERDATA

