import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path, PurePath, PureWindowsPath
from typing import List, Optional

from . import parse_declaration as parse_decl
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

from . import TwincatDataclasses as tcd
from .BaseStrategy import BaseStrategy
from .Loader import add_strategy
from .TwincatObjects.tc_plc_object import (
    Dut,
    Get,
    Gvl,
    Itf,
    Method,
    Pou,
    Property,
    Set,
    TcPlcObject,
)
from .TwincatObjects.tc_plc_project import Compile, PlaceholderReference, Project

logger = logging.getLogger(__name__)


def parse_documentation(declaration: str) -> Optional[tcd.Documentation]:
    # Helper function to clean up tag content
    def clean_tag_content(content):
        if content:
            # Remove lines that are just asterisks
            content = re.sub(r"^\s*\*+\s*$", "", content, flags=re.MULTILINE)
            # Remove trailing asterisks and whitespace
            content = re.sub(r"\s*\*+\s*$", "", content)
            # Remove leading asterisks and whitespace from each line
            content = re.sub(r"^\s*\*+\s*", "", content, flags=re.MULTILINE)
            # Remove leading and trailing whitespace
            #content = content.strip()
            # Replace multiple whitespace with a single space
            #content = re.sub(r"\s+", " ", content)
        return content

    # Parse documentation tags
    doc = tcd.Documentation()
    comments = parse_decl.get_comments(decl=declaration)
    for comment in comments.get("comments"):
        temp = parse_decl.get_comment_content(comment)
        for key, value in temp.get("documentation").items():
            if key == "details":
                doc.details = clean_tag_content(value)
            elif key == "return":
                doc.returns = (clean_tag_content(value))
            elif key == "usage":
                doc.usage = (clean_tag_content(value))
            else:
                doc.custom_tags.update({key: clean_tag_content(value)})

    return doc


def parse_variables(declaration: str) -> List[tcd.Variable]:
    """
    Parse variables from a declaration string.

    Args:
        declaration: The declaration string containing variable sections.

    Returns:
        A list of tcd.Variable objects.
    """
    variables = []

    found_var = []
    found_var_blocks = parse_decl.get_var_blocks(declaration)
    for var_block in found_var_blocks:
        temp_variables = parse_decl.get_var(var_block["content"])
        keyword = parse_decl.get_var_keyword(var_block["content"])
        for var in temp_variables:
            temp = parse_decl.get_var_content(var)
            for temp_var in temp:
                temp_var["var_type"] = var_block["name"]
                temp_var["access_modifier"] = keyword
                found_var.append(temp_var)

    for var in found_var:
        comments = parse_decl.get_comment_content(var["comments"])
        doc = tcd.Documentation(
            details=comments["standard"][0] if len(comments["standard"]) > 0 else None
        )

        
        # Create the variable
        current_var = tcd.Variable(
            name=var["name"],
            type=var["type"],
            initial_value=var["init"],
            comment=var["comments"],
            attributes=var["attributes"],
            section_type=var["var_type"].lower(),
            documentation=doc,
            section_modifier=var["access_modifier"],

        )
        current_var.labels.append(var["type"])
        variables.append(current_var)

    return variables


def load_method(method: Method):
    if method is None:
        return None

    # Extract implementation text
    implementation_text = ""
    if hasattr(method.implementation, "st"):
        implementation_text = method.implementation.st

    # Parse access modifier and return type from declaration
    accessModifier = None
    returnType = None
    variables = []
    documentation = None

    if method.declaration:
        returnType = parse_decl.get_return(method.declaration)
        accessModifier = parse_decl.get_access_modifier(method.declaration)
        variables = parse_variables(method.declaration)
        documentation = parse_documentation(method.declaration)

    tcMeth = tcd.Method(
        name=method.name,
        accessModifier=accessModifier,
        returnType=returnType,
        declaration=method.declaration,
        implementation=implementation_text,
        documentation=documentation,
    )

    for var in variables:
        var.parent = tcMeth
        var.name_space = tcMeth.name_space

    if returnType is not None:
        tcMeth.labels.append(returnType)
    if accessModifier is not None:
        tcMeth.labels.append(accessModifier)

    tcMeth.variables = variables
    return tcMeth


def load_property(property: Property):
    if property is None:
        return None

    # Parse return type from declaration
    returnType = None
    if property.declaration:
        returnType = parse_decl.get_return(property.declaration)
        # Parse documentation
        documentation = parse_documentation(property.declaration)

    tcProp = tcd.Property(
        name=property.name,
        returnType=returnType,
        get=load_get_property(get=property.get),
        set=load_set_property(set=property.set),
        documentation=documentation,
    )

    if returnType is not None:
        tcProp.labels.append(returnType)
    if tcProp.get is not None and tcProp.set is not None:
        tcProp.labels.append("Get/Set")
    elif tcProp.get is not None:
        tcProp.labels.append("Get")
    elif tcProp.set is not None:
        tcProp.labels.append("Set")

    return tcProp


def load_get_property(get: Get):
    if get is None:
        return None

    # Extract implementation text
    implementation_text = ""
    if hasattr(get.implementation, "st"):
        implementation_text = get.implementation.st

    return tcd.Get(
        name=get.name, declaration=get.declaration, implementation=implementation_text
    )


def load_set_property(set: Set):
    if set is None:
        return None

    # Extract implementation text
    implementation_text = ""
    if hasattr(set.implementation, "st"):
        implementation_text = set.implementation.st

    return tcd.Set(
        name=set.name, declaration=set.declaration, implementation=implementation_text
    )


def parse_placeholder_reference(placeholder: PlaceholderReference) -> tcd.Dependency:
    pattern = r"^(.*?),\s*([\d\.\*]+)\s*\((.*?)\)$"
    match = re.match(pattern, placeholder.default_resolution)
    if match:
        name, version, vendor = match.groups()
        return tcd.Dependency(name=name, version=version, category=vendor)


class FileHandler(ABC):
    def __init__(self, suffix):
        self.suffix: str = suffix.lower()
        self.config = ParserConfig(fail_on_unknown_properties=False)
        self.parser = XmlParser(config=self.config)
        super().__init__()

    @abstractmethod
    def load_object(
        self,
        path: Path,
        obj_store: List[tcd.Objects],
        parent: tcd.Objects | None = None,
    ):
        raise NotImplementedError()


_handler: List[FileHandler] = []


def add_handler(handler: FileHandler):
    _handler.append(handler)


def get_all_handler() -> List[FileHandler]:
    return _handler


def is_handler_in_list(suffix: str) -> bool:
    for handler in _handler:
        if handler.suffix.lower() == suffix.lower():
            return True
    logger.error(f"no handler found for: {suffix}")
    return False


def get_handler(suffix: str) -> FileHandler:
    for handler in _handler:
        if handler.suffix.lower() == suffix.lower():
            return handler
    raise Exception(
        f"Handler for suffix:  <{suffix}> not found. Registered Handlers: {', '.join(x.suffix for x in _handler)}"
    )


class SolutionHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".sln")

    def load_object(
        self, path, obj_store: List[tcd.Objects], parent: tcd.Objects | None = None
    ):
        raise NotImplementedError("SolutionFileHandler not implemented")


class TwincatProjectHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tsproj")

    def load_object(
        self, path, obj_store: List[tcd.Objects], parent: tcd.Objects | None = None
    ):
        raise NotImplementedError("TwincatProjectHandler not implemented")


class XtiHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".xti")

    def load_object(
        self, path, obj_store: List[tcd.Objects], parent: tcd.Objects | None = None
    ):
        raise NotImplementedError("XtiHandler not implemented")


class TcTtoHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tctto")

    def load_object(
        self, path, obj_store: List[tcd.Objects], parent: tcd.Objects | None = None
    ):
        raise NotImplementedError("tcttoHandler not implemented")


class PlcProjectHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".plcproj")

    def load_object(
        self, path, obj_store: List[tcd.Objects], parent: tcd.Objects | None = None
    ):
        _prj: Project = self.parser.parse(path, Project)
        if _prj is None:
            return None

        # Sub Elements
        object_paths: List[Path] = []
        dependencies: List[tcd.Dependency] = []
        compile_elements: List[Compile] = []
        for object in _prj.item_group:
            for elem in object.compile:
                if not elem.exclude_from_build:
                    compile_elements.append(elem)

            # Dependencies
            for dependency in object.placeholder_reference:
                if not dependency.system_library:
                    _dep = parse_placeholder_reference(placeholder=dependency)
                    if _dep:
                        dependencies.append(_dep)

        for elem in compile_elements:
            object_paths.append(
                (path.parent / Path(PureWindowsPath(elem.include))).resolve()
            )

        doc = tcd.Documentation(details=_prj.property_group.description)

        plcproj = tcd.PlcProject(
            name=_prj.property_group.name,
            path=path.resolve(),
            default_namespace=_prj.property_group.default_namespace,
            name_space=_prj.property_group.default_namespace,
            version=_prj.property_group.project_version,
            sub_paths=object_paths,
            dependencies=dependencies,
            documentation=doc,
        )

        for object_path in object_paths:
            if is_handler_in_list(object_path.suffix):
                handler = get_handler(object_path.suffix)
                handler.load_object(
                    path=object_path, obj_store=obj_store, parent=plcproj
                )

        if plcproj.version is not None:
            plcproj.labels.append(plcproj.version)

        obj_store.append(plcproj)


class TcPouHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tcpou")

    def load_object(
        self, path, obj_store: List[tcd.Objects], parent: tcd.Objects | None = None
    ):
        _pou: Pou = self.parser.parse(path, TcPlcObject).pou
        if _pou is None:
            return None

        # Extract implementation text
        implementation_text = ""
        if hasattr(_pou.implementation, "st"):
            implementation_text = _pou.implementation.st

        properties = []
        if hasattr(_pou, "property") and _pou.property:
            properties = [load_property(property=prop) for prop in _pou.property]
        for prop in properties:
            prop.parent = _pou.name

        methods = []
        if hasattr(_pou, "method") and _pou.method:
            methods = [load_method(method=meth) for meth in _pou.method]
        for meth in methods:
            meth.parent = _pou.name

        # Parse extends and implements from declaration
        extends = []
        implements = []
        variables = []
        access_specifier = ""

        if _pou.declaration:
            extends = parse_decl.get_extend(_pou.declaration)
            implements = parse_decl.get_implements(_pou.declaration)
            access_specifier = parse_decl.get_abstract_keyword(_pou.declaration)

            # Parse variable sections
            variables = parse_variables(_pou.declaration)

            # Parse documentation
            documentation = parse_documentation(_pou.declaration)

        tcPou = tcd.Pou(
            name=_pou.name,
            path=path.resolve(),
            declaration=_pou.declaration,
            implementation=implementation_text,
            extends=extends,
            implements=implements,
            documentation=documentation,
            access_specifier=access_specifier,
        )

        if parent is not None:
            tcPou.parent = parent
            if parent.__class__ == tcd.PlcProject:
                if hasattr(parent, "name_space"):
                    tcPou.name_space = parent.name_space
                if hasattr(parent, "pous"):
                    parent.pous.append(tcPou)

        for var in variables:
            var.parent = tcPou
            var.name_space = tcPou.name_space
        for prop in properties:
            prop.parent = tcPou
            prop.name_space = tcPou.name_space
        for meth in methods:
            meth.parent = tcPou
            meth.name_space = tcPou.name_space

        tcPou.variables = variables
        tcPou.properties = properties
        tcPou.methods = methods

        if extends is not None:
            tcPou.labels.append("Extends: " + ", ".join([ext for ext in extends]))
        if implements is not None:
            tcPou.labels.append("Implements: " + ", ".join([impl for impl in implements]))

        obj_store.append(tcPou)
        obj_store.extend(methods)
        obj_store.extend(properties)


class TcItfHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tcio")

    def load_object(
        self, path, obj_store: List[tcd.Objects], parent: tcd.Objects | None = None
    ):
        _itf: Itf = self.parser.parse(path, TcPlcObject).itf
        if _itf is None:
            return None

        properties = []
        if hasattr(_itf, "property") and _itf.property:
            properties = [load_property(property=prop) for prop in _itf.property]

        methods = []
        if hasattr(_itf, "method") and _itf.method:
            methods = [load_method(method=meth) for meth in _itf.method]

        # Parse extends from declaration
        extends = None

        if _itf.declaration:
            extends = parse_decl.get_extend(_itf.declaration)

        tcitf = tcd.Itf(
            name=_itf.name,
            path=path.resolve(),
            extends=extends,
        )

        for prop in properties:
            prop.parent = tcitf
        for meth in methods:
            meth.parent = tcitf

        tcitf.properties = properties
        tcitf.methods = methods

        if parent is not None:
            tcitf.parent = parent
            if parent.__class__ == tcd.PlcProject:
                if hasattr(parent, "name_space"):
                    tcitf.name_space = parent.name_space
                if hasattr(parent, "itfs"):
                    parent.itfs.append(tcitf)

        if extends is not None:
            tcitf.labels.append("Ext: " + ", ".join([ext for ext in extends]))

        obj_store.append(tcitf)
        obj_store.extend(methods)
        obj_store.extend(properties)


class TcDutHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tcdut")

    def load_object(
        self, path, obj_store: List[tcd.Objects], parent: tcd.Objects | None = None
    ):
        _dut: Dut = self.parser.parse(path, TcPlcObject).dut
        if _dut is None:
            return None

        variables = []
        documentation = None
        if _dut.declaration:
            # Parse variable sections
            variables = parse_variables(_dut.declaration)

            # Parse documentation
            documentation = parse_documentation(_dut.declaration)

        dut = tcd.Dut(
            name=_dut.name,
            path=path.resolve(),
            declaration=_dut.declaration,
            documentation=documentation,
        )

        for var in variables:
            var.parent = dut
            var.name_space = dut.name_space

        if parent is not None:
            dut.parent = parent
            if parent.__class__ == tcd.PlcProject:
                if hasattr(parent, "name_space"):
                    dut.name_space = parent.name_space
                if hasattr(parent, "duts"):
                    parent.duts.append(dut)

        dut.variables = variables

        obj_store.append(dut)


class TcGvlHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tcgvl")

    def load_object(
        self, path, obj_store: List[tcd.Objects], parent: tcd.Objects | None = None
    ):
        _gvl: Gvl = self.parser.parse(path, TcPlcObject).gvl
        if _gvl is None:
            return None

        variables = []
        documentation = None
        if _gvl.declaration:
            # Parse variable sections
            variables = parse_variables(_gvl.declaration)

            # Parse documentation
            documentation = parse_documentation(_gvl.declaration)

        gvl: tcd.Gvl = tcd.Gvl(
            name=_gvl.name,
            path=path.resolve(),
            declaration=_gvl.declaration,
            documentation=documentation,
        )

        for var in variables:
            var.parent = gvl
            var.name_space = gvl.name_space

        if parent is not None:
            gvl.parent = parent
            if parent.__class__ == tcd.PlcProject:
                if hasattr(parent, "name_space"):
                    gvl.name_space = parent.name_space
                if hasattr(parent, "gvls"):
                    parent.gvls.append(gvl)

        gvl.variables = variables

        obj_store.append(gvl)


# add_handler(handler=SolutionHandler())
# add_handler(handler=TwincatProjectHandler())
# add_handler(handler=XtiHandler())
add_handler(handler=PlcProjectHandler())
add_handler(handler=TcPouHandler())
add_handler(handler=TcItfHandler())
add_handler(handler=TcDutHandler())
add_handler(handler=TcGvlHandler())
# add_handler(handler=TcTtoHandler())


class Twincat4024Strategy(BaseStrategy):
    def check_strategy(self, path: Path):
        for handler in _handler:
            if path.suffix == handler.suffix:
                return True

    def load_objects(self, path: Path) -> List[tcd.Objects]:
        _path = PurePath(path)
        _obj: List[tcd.Objects] = []
        if is_handler_in_list(suffix=_path.suffix):
            handler = get_handler(suffix=_path.suffix)
            handler.load_object(path, obj_store=_obj)
            return _obj
        else:
            return []


# present the strategy to the loader
add_strategy(Twincat4024Strategy)
