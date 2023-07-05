import logging

from templates.four_g_vm_core.vm_common_user_data import CommonUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class FourGVMCoreTemplate(VMTemplate):

    def __init__(self, prefix: str, nf_name: str):
        super().__init__(prefix)
        self.vm_name = prefix+"-"+nf_name
        self.name = nf_name
        self.user_data = CommonUserData.USERDATA
