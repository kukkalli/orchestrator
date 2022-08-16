import logging

from odl.flow_table import FlowTable
from odl.node_connector import NodeConnector
from odl.node_group_features import GroupFeatures
from odl.switch_features import SwitchFeatures
from utilities.validate_ipaddress import IPAddress
from utilities.list_utility import add_elements_with_type

LOG = logging.getLogger(__name__)


class InventoryNode(object):
    def __init__(self, node):
        self.__json = node
        self.__id = node["id"]
        self.group_features = GroupFeatures(node["opendaylight-group-statistics:group-features"])
        self.serial_number = node["flow-node-inventory:serial-number"]
        self.port_number = node["flow-node-inventory:port-number"]
        self.description = node["flow-node-inventory:description"]
        self.hardware = node["flow-node-inventory:hardware"]
        self.manufacturer = node["flow-node-inventory:manufacturer"]
        self.switch_features = SwitchFeatures(node["flow-node-inventory:switch-features"])
        self.software = node["flow-node-inventory:software"]
        self.ip_address = IPAddress(node["flow-node-inventory:ip-address"])
        self.list_flow_tables: list[FlowTable] = []
        self.list_node_connector: list[NodeConnector] = []
        self.dict_flow_tables: dict[str, FlowTable] = {}
        self.dict_node_connector: dict[str, NodeConnector] = {}
        add_elements_with_type(self.list_flow_tables, node["flow-node-inventory:table"], FlowTable)
        add_elements_with_type(self.list_node_connector, node["node-connector"], NodeConnector)
        for flow_table in self.list_flow_tables:
            self.dict_flow_tables[flow_table.id] = flow_table
        for node_connector in self.list_node_connector:
            self.dict_node_connector[node_connector.id] = node_connector

    @property
    def id(self) -> str:
        return self.__id

    def to_string(self) -> str:
        return self.__json

    def get_flow_table_by_id(self, flow_table_id):
        return self.dict_flow_tables[flow_table_id]

    def get_node_connector_by_id(self, node_connector_id):
        return self.dict_node_connector[node_connector_id]
