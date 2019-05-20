

class state_manager(object):
    """Use this class to store named global state
    Add objects into the property bag as a dictionary.  
    """
    def __init__(self):
        self.state = {}

    def add(self, name, state):
        if name not in self.state:
            self.state[name] = state
        else:
            self.state[name] = {**self.state[name], **state}

    def get(self, name):
        return self.state[name]

    def exists(self, name):
        return name in self.state

    def names(self):
        return(list(self.state.keys()))


