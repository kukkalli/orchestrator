from odl.node_connector_statistics import NodeConnectorStatistics
from odl.state import State


class NodeConnector(object):
    def __init__(self, node_connector):
        self.__json = node_connector
        self.__id = node_connector["id"]
        self.__hardware_address = node_connector["flow-node-inventory:hardware-address"]
        self.supported = node_connector["flow-node-inventory:supported"]
        self.peer_features = node_connector["flow-node-inventory:peer-features"]
        self.advertised_features = node_connector["flow-node-inventory:advertised-features"]
        self.name = node_connector["flow-node-inventory:name"]
        self.port_number = node_connector["flow-node-inventory:port-number"]
        self.current_speed = node_connector["flow-node-inventory:current-speed"]
        self.configuration = node_connector["flow-node-inventory:configuration"]
        self.current_feature = node_connector["flow-node-inventory:current-feature"]
        self.maximum_speed = node_connector["flow-node-inventory:maximum-speed"]
        self.state = State(node_connector["flow-node-inventory:state"])
        self.node_connector_statistics = NodeConnectorStatistics(
            node_connector["opendaylight-port-statistics:flow-capable-node-connector-statistics"])

    @property
    def id(self):
        return self.__id

    @property
    def hardware_address(self):
        return self.__hardware_address

    def to_string(self) -> str:
        return self.__json
