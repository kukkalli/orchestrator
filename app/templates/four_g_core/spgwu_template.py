import logging

from templates.four_g_core.four_g_core_template import FourGCoreTemplate
from templates.four_g_core.spgwu_user_data import SPGWUUserData

LOG = logging.getLogger(__name__)


class SPGWUTemplate(FourGCoreTemplate):

    def __init__(self, prefix: str, nf_name: str):
        super().__init__(prefix, nf_name)
        self.flavor = "3"
        self.user_data = self.get_user_data() + SPGWUUserData.USERDATA

