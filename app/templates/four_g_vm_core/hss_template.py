import logging

from openstack_internal.openstack_constants import OpenStackConstants
from templates.four_g_vm_core.hss_user_data import HSSUserData
from templates.four_g_vm_core.vm_common_user_data import CommonUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class HSSTemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "2"
        self.vm_name = name+"-hss"
        self.name = "hss"
        self.image_name: str = OpenStackConstants.OAI_HSS
        self.image_id = "be75324b-2625-4fc7-8861-9b5087196b57"
        self.user_data = CommonUserData.USERDATA + HSSUserData.USERDATA

