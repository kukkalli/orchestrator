import logging
from enum import Enum, unique

LOG = logging.getLogger(__name__)


@unique
class ServiceProfiles(Enum):
    FOUR_G_LTE_CORE = "FOUR_G_LTE_CORE"
    FOUR_G_LTE_CORE_CASS_DB = "FOUR_G_LTE_CORE_CASS_DB"
    FOUR_G_LTE_CORE_BBU = "FOUR_G_LTE_CORE_BBU"
    FOUR_G_LTE_CORE_BBU_CASS_DB = "FOUR_G_LTE_CORE_BBU_CASS_DB"
    FOUR_G_VM_LTE_CORE = "FOUR_G_VM_LTE_CORE"
    FIVE_G_CORE = "FIVE_G_CORE"
    FIVE_G_CORE_DU = "FIVE_G_CORE_DU"

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return 'ServiceProfile: name: {0}, value: {1}'.format(self.get_name(), self.get_value())

    @classmethod
    def default(cls):
        return cls.FOUR_G_VM_LTE_CORE


def main():
    print(ServiceProfiles("FOUR_G_VM_LTE_CORE") in ServiceProfiles)
    print(repr(ServiceProfiles.FOUR_G_VM_LTE_CORE))
    print(type(ServiceProfiles.FOUR_G_VM_LTE_CORE))
    print(isinstance(ServiceProfiles.FOUR_G_VM_LTE_CORE, ServiceProfiles))
    print(ServiceProfiles.default())
    print(ServiceProfiles.FOUR_G_LTE_CORE_BBU.describe())
    print(ServiceProfiles.FIVE_G_CORE_DU.__str__())


if __name__ == "__main__":
    main()

