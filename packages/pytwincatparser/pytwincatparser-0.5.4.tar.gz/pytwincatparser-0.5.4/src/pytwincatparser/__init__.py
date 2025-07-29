"""
pytwincatparser - A Python package for parsing TwinCAT PLC files using xsdata.
"""

from .TwincatDataclasses import (
    Pou,
    Dut,
    Itf,
    Method,
    Property,
    Get,
    Set,
    Variable,
    Documentation,
    Objects,
    Solution,
    PlcProject,
    Dependency
)
from .Loader import add_strategy, Loader, get_default_strategy, get_strategy, get_strategy_by_object_path
from .Twincat4024Strategy import Twincat4024Strategy
from .BaseStrategy import BaseStrategy

__version__ = "0.1.1"
__all__ = [
    "Pou",
    "Dut",
    "Itf",
    "Method",
    "Property",
    "Get",
    "Set",
    "Variable",
    "Documentation",
    "Objects",
    "Solution",
    "PlcProject",
    "add_strategy",
    "Twincat4024Strategy",
    "BaseStrategy",
    "Loader",
    "get_default_strategy", 
    "get_strategy", 
    "get_strategy_by_object_path",
    "Dependency",
]
