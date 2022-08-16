import logging

LOG = logging.getLogger(__name__)


class PortStats:

    def __init__(self, port_stats):
        self.packet_transmitted = port_stats.get('packets:transmitted')
        self.packet_received = port_stats.get('packets:received')
        self.bytes_transmitted = port_stats.get('bytes:transmitted')
        self.bytes_received = port_stats.get('bytes:received')
        self.transmitted_drops = port_stats.get('transmit-drops')
        self.receive_drops = port_stats.get('receive-drops')
        self.transmitted_errors = port_stats.get('transmit-errors')
        self.receive_errors = port_stats.get('receive-errors')

    def get_packet_transmitted(self):
        return self.packet_transmitted
