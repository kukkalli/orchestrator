import logging

LOG = logging.getLogger(__name__)


class Link:

    def __init__(self, _id: str, int_id: int, dst_node_id: int, src_node_id: int, dst_port_id: str = None,
                 src_port_id: str = None, capacity: int = 10000000, length_of_link: float = 0.001,
                 delay_per_km: float = 0.035, bi_directional=False):
        self.__id = _id
        self.__int_id = int_id
        self.dst_node_id = dst_node_id  # to node name
        self.src_node_id = src_node_id  # from node name

        self.dst_port_id = dst_port_id  # to port if it is a switch
        self.src_port_id = src_port_id  # from port if it is a switch

        self.capacity = capacity  # in kbps
        self.delay = length_of_link * delay_per_km  # in microseconds
        self.length_of_link = length_of_link  # in kilometres
        self.delay_per_km = delay_per_km  # in microseconds
        self.bi_directional = bi_directional  # true if bidirectional

    @property
    def id(self):
        return self.__id

    @property
    def int_id(self):
        return self.__int_id
