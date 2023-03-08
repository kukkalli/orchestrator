import logging
from enum import Enum, unique

LOG = logging.getLogger(__name__)


@unique
class PDNType(Enum):
    IPv4 = 'IPv4'
    IPv6 = 'IPv6'
    IPv4v6 = 'IPv4v6'
    IPv4_or_IPv6 = 'IPv4_or_IPv6'

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return 'PDNType: name: {0}, value: {1}'.format(self.get_name(), self.get_value())

    @classmethod
    def default(cls):
        return cls.IPv4


def main():
    print(PDNType("IPv4") in PDNType)
    print(type(PDNType.IPv4))
    print(repr(PDNType.IPv4))
    print(isinstance(PDNType.IPv6, PDNType))
    print(PDNType.default())
    print(PDNType.IPv4v6.describe())
    print(PDNType.IPv4_or_IPv6.__str__())


if __name__ == "__main__":
    main()
