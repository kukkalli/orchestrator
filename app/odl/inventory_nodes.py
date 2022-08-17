import logging
from typing import List, Dict

from odl.inventory_node import InventoryNode
from utilities.list_utility import add_elements_with_type

LOG = logging.getLogger(__name__)


class InventoryNodes(object):
    def __init__(self, root):
        self.__json = root
        self.nodes: List[InventoryNode] = []
        self.dict_nodes: Dict[str, InventoryNode] = {}
        add_elements_with_type(self.nodes, root["nodes"]["node"], InventoryNode)
        for node in self.nodes:
            self.dict_nodes[node.id] = node

    def to_string(self) -> str:
        return self.__json

    def get_node_by_id(self, node_id) -> InventoryNode:
        return self.dict_nodes[node_id]
