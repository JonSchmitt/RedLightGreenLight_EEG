class StateResult:
    def __init__(self):
        self._quit = False
        self._keys = []
        self._next_state = None
        # self._other = []

    def set_quit(self,value:bool):
        self._quit = value

    def get_quit(self):
        return self._quit

    def add_key(self, key):
        self._keys.append(key)

    def get_keys(self):
        return self._keys


    def set_next_state(self, state):
        self._next_state = state

    def get_next_state(self):
        return self._next_state


    # def add_other(self, other):
    #     self._other.append(other)
    #
    # def get_other(self):
    #     return self._other