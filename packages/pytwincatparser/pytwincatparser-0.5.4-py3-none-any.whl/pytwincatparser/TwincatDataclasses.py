from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from abc import ABC, abstractmethod


@dataclass
class Base(ABC):
    path: Path = None
    sub_paths: Optional[List[Path]] = None
    parent: Optional[object | None] = None
    name_space: Optional[str] = None
    name: Optional[str] = None
    kind: str = ""
    labels: Optional[List[str]] = None

    def __post_init__(self):
        if self.sub_paths is None:
            self.sub_paths = []    
        if self.labels is None:
            self.labels = []    
        self.kind = self.__class__.__name__.lower()

    @abstractmethod
    def get_identifier(self) -> str:
        pass




@dataclass
class Documentation(Base):
    details: Optional[str] = None
    usage: Optional[str] = None
    returns: Optional[str] = None
    custom_tags: Optional[Dict[str, str]] = None

    def __post_init__(self):
        if self.custom_tags is None:
            self.custom_tags = {}
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        return ""

@dataclass
class Variable(Base):
    type: str = ""
    initial_value: Optional[str] = None
    comment: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    documentation: Optional[Documentation] = None
    section_type: str = None
    section_modifier: Optional[str] = None

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        _identifier = ""
        if self.name_space is not None:
            _identifier = self.name_space + "."
        if self.parent.name is not None:
            _identifier += self.parent.name
            _identifier += "."
        _identifier += self.name
        return _identifier

@dataclass
class Get(Base):
    declaration: str = ""
    implementation: str = ""

    def __post_init__(self):
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        return ""

@dataclass
class Set(Base):
    declaration: str = ""
    implementation: str = ""

    def __post_init__(self):
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        return ""

@dataclass
class Method(Base):
    accessModifier: Optional[str] = None
    returnType: Optional[str] = None
    declaration: str = ""
    implementation: str = ""
    variables: Optional[List[Variable]] = None
    documentation: Optional[Documentation] = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = []
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        _identifier = ""
        if self.name_space is not None:
            _identifier = self.name_space + "."
        if self.parent.name is not None:
            _identifier += self.parent.name
            _identifier += "."
        _identifier += self.name
        return _identifier

@dataclass
class Property(Base):
    returnType: Optional[str] = None
    get: Optional[Get] = None
    set: Optional[Set] = None
    documentation: Optional[Documentation] = None

    def __post_init__(self):
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        _identifier = ""
        if self.name_space is not None:
            _identifier = self.name_space + "."
        if self.parent.name is not None:
            _identifier += self.parent.name
            _identifier += "."
        _identifier += self.name
        return _identifier


@dataclass
class Pou(Base):
    implements: Optional[list[str]] = None
    extends: Optional[list[str]] = None
    declaration: str = ""
    implementation: str = ""
    access_specifier: str = ""

    methods: Optional[list[Method]] = None
    properties: Optional[list[Property]] = None
    variables: Optional[List[Variable]] = None
    documentation: Optional[Documentation] = None

    def __post_init__(self):
        if self.implements is None:
            self.implements = []
        if self.methods is None:
            self.methods = []
        if self.properties is None:
            self.properties = []
        if self.variables is None:
            self.variables = []
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        _identifier = ""
        if self.name_space is not None:
            _identifier = self.name_space + "."
        _identifier += self.name
        return _identifier

@dataclass
class Itf(Base):
    extends: Optional[list[str]] = None

    methods: Optional[list[Method]] = None
    properties: Optional[list[Property]] = None
    documentation: Optional[Documentation] = None

    def __post_init__(self):
        if self.extends is None:
            self.extends = []
        if self.methods is None:
            self.methods = []
        if self.properties is None:
            self.properties = []
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        _identifier = ""
        if self.name_space is not None:
            _identifier = self.name_space + "."
        _identifier += self.name
        return _identifier

@dataclass
class Dut(Base):
    declaration: str = ""
    variables: Optional[List[Variable]] = None
    documentation: Optional[Documentation] = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = []
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        _identifier = ""
        if self.name_space is not None:
            _identifier = self.name_space + "."
        _identifier += self.name
        return _identifier
    

@dataclass
class Gvl(Base):
    declaration: str = ""
    variables: Optional[List[Variable]] = None
    documentation: Optional[Documentation] = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = []
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        _identifier = ""
        if self.name_space is not None:
            _identifier = self.name_space + "."
        _identifier += self.name
        return _identifier


@dataclass
class Dependency(Base):
    version : str = ""
    category : str = ""

    def __post_init__(self):
        Base.__post_init__(self)

    def get_identifier(self) -> str:
        return ""



@dataclass
class PlcProject(Base):
    """Represents a plc project in a TwinCAT solution."""

    default_namespace: str = ""
    version: str = ""
    dependencies: Optional[List[Dependency]] = None
    documentation: Optional[Documentation] = None
    pous: Optional[List[Pou]] = None
    duts: Optional[List[Dut]] = None
    itfs: Optional[List[Itf]] = None
    gvls: Optional[List[Gvl]] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []              
        if self.pous is None:
            self.pous = []    
        if self.duts is None:
            self.duts = []    
        if self.itfs is None:
            self.itfs = []    
        if self.gvls is None:
            self.gvls = []    


        Base.__post_init__(self)

    def get_identifier(self) -> str:
        return self.name
    





@dataclass
class Project(Base):
    """Represents a project in a TwinCAT solution."""

    def __post_init__(self):
        Base.__post_init__(self)

@dataclass
class Solution(Base):
    """Represents a TwinCAT solution with its projects."""

    _projects: List[Project] = None

    def __post_init__(self):
        if self._projects is None:
            self._projects = []
        Base.__post_init__(self)



Objects = Base
