class Packets(object):
    def __init__(self, packets):
        self.__json = packets
        self.transmitted = packets["transmitted"]
        self.received = packets["received"]
