from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from .TwincatDataclasses import Objects


class BaseStrategy(ABC): # extract to seperate file

    def __init__(self):
        super().__init__()

    @abstractmethod
    def check_strategy(self, path:Path) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def load_objects(self, path:Path) -> List[Objects]:
        raise NotImplementedError()
