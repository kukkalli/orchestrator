from typing import List

from topology.link import Link


class VirtualLink:

    def __init__(self, name: str, int_id: int, dst_node_id: int, src_node_id: int, bandwidth=100, max_link_delay=100,
                 bidirectional=False):
        self.__id = name
        self.int_id = int_id
        self.dst_node_id = dst_node_id
        self.src_node_id = src_node_id
        self.bandwidth = bandwidth              # in Mbps
        self.max_link_delay = max_link_delay    # in milliseconds
        self.bidirectional = bidirectional
        self.implemented_links: List[Link] = []

    @property
    def id(self):
        return self.__id

