class State(object):
    def __init__(self, state):
        self.__json = state
        self.blocked = state["blocked"]
        self.link_down = state["link-down"]
        self.live = state["live"]

    def to_string(self) -> str:
        return self.__json
