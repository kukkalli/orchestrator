import logging

from openstack_internal.glance.glance_details import Glance
from templates.oai_5gcn.oai_5gcn_constants import OAI5GConstants
from templates.user_data.prepared_image_common_user_data import CommonOAI5GCNUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class PreparedImageVMTemplate(VMTemplate):

    def __init__(self, prefix: str, name: str, flavor: str = "3"):
        super().__init__(prefix, name)
        self.flavor = flavor
        self.image_name: str = OAI5GConstants.UBUNTU_22_04_DOCKER_VM_LOW_LATENCY
        self.image_id: str | None = Glance().get_image_id(self.image_name)
        self.user_data = CommonOAI5GCNUserData.USERDATA
