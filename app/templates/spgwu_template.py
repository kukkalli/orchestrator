import logging

from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class SPGWUTemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "2"
        self.vm_name = name+"-spgw-u"
        self.name = "spgw-u"

