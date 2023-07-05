import logging

from openstack_internal.glance.glance_details import Glance
from openstack_internal.openstack_constants import OpenStackConstants
from templates.four_g_vm_core.four_g_vm_core_template import FourGVMCoreTemplate
from templates.four_g_vm_core.hss_user_data import HSSUserData

LOG = logging.getLogger(__name__)


class HSSTemplate(FourGVMCoreTemplate):

    def __init__(self, prefix: str, nf_name: str):
        super().__init__(prefix, nf_name)
        self.flavor = "2"
        self.image_name: str = OpenStackConstants.OAI_HSS_VMI
        self.image_id: str | None = Glance().get_image_id(self.image_name)
        self.user_data = self.get_user_data() + HSSUserData.USERDATA

