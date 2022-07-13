import logging

LOG = logging.getLogger(__name__)


class PortState:
    
    def __init__(self, port_state):
        self.port_state = port_state
        # {'blocked': False, 'link-down': False, 'live': False}
        self.blocked = port_state['blocked']
        self.link_down = port_state['link-down']
        self.live = port_state['live']

    def is_blocked(self):
        return self.blocked

    def is_link_down(self):
        return self.link_down

    def is_live(self):
        return self.live
