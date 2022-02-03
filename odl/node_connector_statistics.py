from odl.txrxbytes import TxRxBytes
from odl.duration import Duration
from odl.packets import Packets


class NodeConnectorStatistics(object):
    def __init__(self, node_connector_statistics):
        self.__json = node_connector_statistics
        self.packets = Packets(node_connector_statistics["packets"])
        self.receive_frame_error = node_connector_statistics["receive-frame-error"]
        self.collision_count = node_connector_statistics["collision-count"]
        self.receive_errors = node_connector_statistics["receive-errors"]
        self.transmit_errors = node_connector_statistics["transmit-errors"]
        self.bytes = TxRxBytes(node_connector_statistics["bytes"])
        self.receive_crc_error = node_connector_statistics["receive-crc-error"]
        self.duration = Duration(node_connector_statistics["duration"])
        self.receive_drops = node_connector_statistics["receive-drops"]
        self.transmit_drops = node_connector_statistics["transmit-drops"]
        self.receive_over_run_error = node_connector_statistics["receive-over-run-error"]

    def to_string(self) -> str:
        return self.__json
