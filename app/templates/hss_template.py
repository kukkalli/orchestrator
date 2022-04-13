import logging

from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class HSSTemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "1"
        self.vm_name = name+"-hss"
        self.name = "hss"

