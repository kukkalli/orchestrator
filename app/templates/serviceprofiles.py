from enum import Enum, unique, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


@unique
class ServiceProfiles(Enum):
    FOUR_G_LTE_CORE = "FOUR_G_LTE_CORE"
    FOUR_G_LTE_CORE_BBU = "FOUR_G_LTE_CORE_BBU"
    FIVE_G_CORE = "FIVE_G_CORE"
    FIVE_G_CORE_DU = "FIVE_G_CORE_DU"


def main():
    print(ServiceProfiles("FOUR_G_LTE_CORE") in ServiceProfiles)
    print(repr(ServiceProfiles.FOUR_G_LTE_CORE))
    print(type(ServiceProfiles.FOUR_G_LTE_CORE))
    print(isinstance(ServiceProfiles.FOUR_G_LTE_CORE, ServiceProfiles))
    print(ServiceProfiles.FOUR_G_LTE_CORE.name)


if __name__ == "__main__":
    main()

