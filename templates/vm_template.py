class VMTemplate:

    def __init__(self):
        self.flavor = "1"
        self.image_id = ""
        self.ip_address = ""
        self.network_id = "9e373e2c-0372-4a06-81a1-bc1cb4c62b85"
        self.vm_name = "default"

    def get_flavour(self):
        return self.flavor

    def get_image_id(self):
        return self.image_id

    def get_ip_address(self):
        return self.ip_address

    def get_network_id(self):
        return self.network_id

    def get_vm_name(self):
        return self.vm_name

