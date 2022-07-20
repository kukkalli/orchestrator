import logging

from topology.link import Link
from topology.node import Node

LOG = logging.getLogger(__name__)


class Server(Node):

    def __init__(self, int_id: int, str_id: str, name: str):
        super().__init__(int_id=int_id, str_id=str_id, name=name, is_switch=False)
        LOG.debug(f"Server Name: {self.name}")
        self.in_links: Link or None = None
        self.out_links: Link or None = None

    def add_in_link(self, link: Link):
        self.in_links = link

    def add_out_link(self, link: Link):
        self.out_links = link

