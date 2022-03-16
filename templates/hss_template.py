from templates.vm_template import VMTemplate


class HSSTemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "1"
        self.image_id = "c761dd72-eba8-4b73-8f07-b6e575115bff"
        self.ip_address = ""
        self.network_id = "9e373e2c-0372-4a06-81a1-bc1cb4c62b85"
        self.vm_name = name+"-hss"

