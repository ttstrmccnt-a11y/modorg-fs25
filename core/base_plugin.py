from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """
    Base class for all modorg modules.
    Every module must inherit from this class and implement its abstract methods.
    """
    def __init__(self, config_manager):
        self.config_manager = config_manager

    @abstractmethod
    def register_arguments(self, parser):
        """Registers CLI arguments for the module."""
        pass

    @abstractmethod
    def execute(self, args):
        """Executes the module logic."""
        pass
