class TxRxBytes(object):
    def __init__(self, _bytes):
        self.__json = _bytes
        self.transmitted = _bytes["transmitted"]
        self.received = _bytes["received"]
