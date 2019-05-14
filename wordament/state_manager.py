
from py_wordament_helper.dictionary_trie import dictionary_trie

class state_manager_factory(object):
    """Creates a singleton instance of state_manager     
    """
    store = None

    def __init__(self):
        pass

    @classmethod
    def create(cls):
        if cls.store is None:
            cls.store = state_manager()

        return cls.store

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


