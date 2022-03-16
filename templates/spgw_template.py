from templates.vm_template import VMTemplate


class SPGWTemplate(VMTemplate):

    def __init__(self, name: str):
        super().__init__()
        self.flavor = "3"
        self.image_id = "49bb635a-d8c2-4d28-b439-e7c7e1c2b275"
        self.ip_address = ""
        self.network_id = "9e373e2c-0372-4a06-81a1-bc1cb4c62b85"
        self.vm_name = name+"-spgw"

