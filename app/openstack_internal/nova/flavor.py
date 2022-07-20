import logging

LOG = logging.getLogger(__name__)


class Flavor:
    def __init__(self, flavor):
        self.__id: str = flavor.id + ""
        self.name = flavor.name
        self.vcpus = flavor.vcpus  # number of vCPUs
        self.disk = flavor.disk  # Disk size in GB
        self.ram = flavor.ram  # RAm in MB
        self.swap = flavor.swap
        self.rxtx_factor = flavor.rxtx_factor

    @property
    def id(self) -> str:
        return self.__id
