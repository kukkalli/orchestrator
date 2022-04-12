class EthernetMatch(object):
    def __init__(self, ethernet_match):
        self.__json = ethernet_match
        self.ethernet_type = EthernetType(ethernet_match["ethernet-type"])

    def to_string(self) -> str:
        return self.__json


class EthernetType(object):
    def __init__(self, ethernet_type):
        self.__json = ethernet_type
        self.type = ethernet_type["type"]

    def to_string(self) -> str:
        return self.__json
