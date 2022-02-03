from odl.ethernet_match import EthernetMatch


class FlowMatch(object):
    def __init__(self, flow_match):
        self.__json = flow_match
        self.ipv4_source = None
        self.ipv4_destination = None
        self.arp_op = None
        if "ipv4-source" in flow_match:
            self.ipv4_source = flow_match["ipv4-source"]
        if "ipv4-destination" in flow_match:
            self.ipv4_destination = flow_match["ipv4-destination"]
        if "arp-op" in flow_match:
            self.arp_op = flow_match["arp-op"]
        self.ethernet_match = EthernetMatch(flow_match["ethernet-match"])

    def to_string(self) -> str:
        return self.__json
