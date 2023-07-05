import logging

from openstack_internal.glance.glance_details import Glance
from openstack_internal.openstack_constants import OpenStackConstants
from templates.four_g_vm_core.four_g_vm_core_template import FourGVMCoreTemplate
from templates.four_g_vm_core.mme_user_data import MMEUserData

LOG = logging.getLogger(__name__)


class MMETemplate(FourGVMCoreTemplate):

    def __init__(self, prefix: str, nf_name: str):
        super().__init__(prefix, nf_name)
        self.flavor = "3"
        self.image_name: str = OpenStackConstants.OAI_MME_VMI
        self.image_id: str | None = Glance().get_image_id(self.image_name)
        self.user_data = self.get_user_data() + MMEUserData.USERDATA

