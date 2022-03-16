from templates.vm_template import VMTemplate


class MMETemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "3"
        self.image_id = "c82a2ad8-cb21-44c0-8daa-7bf8a03bf138"
        self.ip_address = ""
        self.network_id = "9e373e2c-0372-4a06-81a1-bc1cb4c62b85"
        self.vm_name = name+"-mme"

