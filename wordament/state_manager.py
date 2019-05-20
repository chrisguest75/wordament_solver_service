

class state_manager(object):
    def __init__(self):
        self.state = {}

    def add(self, name, state):
        self.state[name] = state

    def get(self, name):
        return self.state[name]

    def exists(self, name):
        return name in self.state

    def names(self):
        return(list(self.state.keys()))


