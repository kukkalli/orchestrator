from templates.vm_template import VMTemplate


class MMETemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "3"
        self.vm_name = name+"-mme"
        self.name = "mme"

