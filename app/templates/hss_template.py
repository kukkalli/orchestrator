from templates.vm_template import VMTemplate


class HSSTemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "1"
        self.vm_name = name+"-hss"
        self.name = "hss"

