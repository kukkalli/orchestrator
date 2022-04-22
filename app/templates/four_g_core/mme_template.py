import logging

from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class MMETemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "3"
        self.vm_name = name+"-mme"
        self.name = "mme"

