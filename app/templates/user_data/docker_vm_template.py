import logging

from templates.user_data.common_docker_user_data import CommonDockerVMUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class DockerVMTemplate(VMTemplate):

    def __init__(self, prefix: str, name: str):
        super().__init__(prefix, name)
        self.user_data = CommonDockerVMUserData.USERDATA
