class PortStats:

    #    def __init__(self, packet_transmitted: int, packet_received:int, bytes_transmitted: int, bytes_received: int,
    #                 transmitted_drops: int, receive_drops: int, transmitted_errors: int, receive_errors: int,
    #                 load_stats: int = 50):
    #        self.packet_transmitted = packet_transmitted
    #        self.packet_received = packet_received
    #        self.bytes_transmitted = bytes_transmitted
    #        self.bytes_received = bytes_received
    #        self.transmitted_drops = transmitted_drops
    #        self.receive_drops = receive_drops
    #        self.transmitted_errors = transmitted_errors
    #        self.receive_errors = receive_errors

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
