from .BaseStrategy import BaseStrategy
from typing import List
from pathlib import Path
from .TwincatDataclasses import Objects


_strategies: List[BaseStrategy] = []


def add_strategy(strategy: BaseStrategy):
    _strategies.append(strategy)


def get_strategy(strategy_name: str) -> BaseStrategy:
    for strategy in _strategies:
        if strategy.__name__.lower() == strategy_name.lower():
            return strategy
    raise Exception(f"No strategy found with name: {strategy_name}")


def get_default_strategy() -> BaseStrategy:
    return get_strategy("twincat4024strategy")


def get_strategy_by_object_path(path: Path) -> BaseStrategy:
    """searches for first handler which returns true. even if there are multiple valid handlers"""
    for strategy in _strategies:
        if strategy.check_strategy(path):
            return strategy
    raise Exception(f"No strategy found for path: {path}")


class Loader:
    def __init__(self, loader_strategy: BaseStrategy):
        self._strategy = loader_strategy

    @property
    def strategy(self) -> BaseStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BaseStrategy) -> None:
        self._strategy = strategy

    def load_objects(self, path: Path) -> List[Objects] | None:
        _path = Path(path)
        return self._strategy.load_objects(path=_path)

    # @abstractmethod
    # def get_item_by_name(self, name:str) -> TcObjects | None:

    #     # Check if the name contains a dot (indicating a method or property)
    #     if '.' in name:
    #         # Split the name by dots
    #         parts = name.split('.')

    #         # If there are more than 2 parts, the first parts form the parent name
    #         if len(parts) > 2:
    #             parent_name = '.'.join(parts[:-1])
    #             item_name = parts[-1]
    #         else:
    #             parent_name, item_name = parts

    #         # Find the parent object
    #         parent_obj = None
    #         for obj_name, obj in self.tcObjects:
    #             if str(obj_name) == parent_name:
    #                 parent_obj = obj
    #                 break

    #         if parent_obj:
    #             # Check if the parent object has methods
    #             if hasattr(parent_obj, 'methods') and parent_obj.methods:
    #                 for method in parent_obj.methods:
    #                     if method.name == item_name: # @todo add a second check if asked with klammern
    #                         return method

    #             # Check if the parent object has properties
    #             if hasattr(parent_obj, 'properties') and parent_obj.properties:
    #                 for prop in parent_obj.properties:
    #                     if prop.name == item_name:
    #                         return prop

    #         return None

    #     # Search for top-level objects
    #     for obj_name, obj in self.tcObjects:
    #         if str(obj_name) == name:
    #             return obj

    # @abstractmethod
    # def get_all_items(self)->List[TcObjects]|None:
    #     return self.tcObjects
