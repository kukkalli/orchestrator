import logging

from templates.four_g_core.four_g_core_template import FourGCoreTemplate
from templates.four_g_core.spgwc_user_data import SPGWCUserData

LOG = logging.getLogger(__name__)


class SPGWCTemplate(FourGCoreTemplate):

    def __init__(self, prefix: str, nf_name: str):
        super().__init__(prefix, nf_name)
        self.flavor = "2"
        self.user_data = self.get_user_data() + SPGWCUserData.USERDATA

