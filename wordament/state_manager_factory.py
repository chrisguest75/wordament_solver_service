from state_manager import state_manager
from injector import Module, Injector, singleton, provider

class ConfigurationError(Exception):
    pass

class StateManagerProvider(Module):
    """ None singleton state_manager
    """
    @provider
    def get_state_manager(self) -> state_manager:
        return state_manager()

class SingletonStateManagerProvider(Module):
    """ Singleton state_manager
    """
    @singleton
    @provider
    def get_state_manager(self) -> state_manager:
        return state_manager()

class injector_factory():
    injector = None

    @staticmethod
    def configure(singleton):
        if singleton:
            injector_factory.injector = Injector([SingletonStateManagerProvider])
        else:
            injector_factory.injector = Injector([StateManagerProvider])

    @staticmethod
    def create() -> Injector:
        if injector_factory.injector is None:
            raise ConfigurationError()

        return injector_factory.injector

class state_manager_factory():
    """Creates a singleton instance of state_manager     
    """
    def __init__(self):
        pass
    
    @staticmethod
    def create():
        injector = injector_factory.create()
        return injector.get(state_manager)
