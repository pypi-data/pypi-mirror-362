from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Dut:
    class Meta:
        name = "DUT"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    declaration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Declaration",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Gvl:
    class Meta:
        name = "GVL"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    declaration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Declaration",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Folder:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    folder: list["Folder"] = field(
        default_factory=list,
        metadata={
            "name": "Folder",
            "type": "Element",
        },
    )


@dataclass
class Implementation:
    st: Optional[str] = field(
        default=None,
        metadata={
            "name": "ST",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class LineId:
    id: Optional[int] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Get:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    declaration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Declaration",
            "type": "Element",
            "required": True,
        },
    )
    implementation: Optional[Implementation] = field(
        default=None,
        metadata={
            "name": "Implementation",
            "type": "Element",
        },
    )


@dataclass
class LineIds:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    line_id: list[LineId] = field(
        default_factory=list,
        metadata={
            "name": "LineId",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Method:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    folder_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "FolderPath",
            "type": "Attribute",
        },
    )
    declaration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Declaration",
            "type": "Element",
            "required": True,
        },
    )
    implementation: Optional[Implementation] = field(
        default=None,
        metadata={
            "name": "Implementation",
            "type": "Element",
        },
    )


@dataclass
class Set:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    declaration: Optional[object] = field(
        default=None,
        metadata={
            "name": "Declaration",
            "type": "Element",
        },
    )
    implementation: Optional[Implementation] = field(
        default=None,
        metadata={
            "name": "Implementation",
            "type": "Element",
        },
    )


@dataclass
class Property:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    folder_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "FolderPath",
            "type": "Attribute",
        },
    )
    declaration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Declaration",
            "type": "Element",
            "required": True,
        },
    )
    get: Optional[Get] = field(
        default=None,
        metadata={
            "name": "Get",
            "type": "Element",
        },
    )
    set: Optional[Set] = field(
        default=None,
        metadata={
            "name": "Set",
            "type": "Element",
        },
    )


@dataclass
class Itf:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    declaration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Declaration",
            "type": "Element",
            "required": True,
        },
    )
    folder: list[Folder] = field(
        default_factory=list,
        metadata={
            "name": "Folder",
            "type": "Element",
            "sequence": 1,
        },
    )
    property: list[Property] = field(
        default_factory=list,
        metadata={
            "name": "Property",
            "type": "Element",
        },
    )
    method: list[Method] = field(
        default_factory=list,
        metadata={
            "name": "Method",
            "type": "Element",
            "sequence": 1,
        },
    )


@dataclass
class Pou:
    class Meta:
        name = "POU"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    special_func: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecialFunc",
            "type": "Attribute",
            "required": True,
        },
    )
    declaration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Declaration",
            "type": "Element",
            "required": True,
        },
    )
    implementation: Optional[Implementation] = field(
        default=None,
        metadata={
            "name": "Implementation",
            "type": "Element",
            "required": True,
        },
    )
    folder: list[Folder] = field(
        default_factory=list,
        metadata={
            "name": "Folder",
            "type": "Element",
        },
    )
    method: list[Method] = field(
        default_factory=list,
        metadata={
            "name": "Method",
            "type": "Element",
        },
    )
    property: list[Property] = field(
        default_factory=list,
        metadata={
            "name": "Property",
            "type": "Element",
        },
    )
    line_ids: list[LineIds] = field(
        default_factory=list,
        metadata={
            "name": "LineIds",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class TcPlcObject:
    version: Optional[str] = field(
        default=None,
        metadata={
            "name": "Version",
            "type": "Attribute",
            "required": True,
        },
    )
    product_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProductVersion",
            "type": "Attribute",
            "required": True,
        },
    )
    pou: Optional[Pou] = field(
        default=None,
        metadata={
            "name": "POU",
            "type": "Element",
        },
    )
    dut: Optional[Dut] = field(
        default=None,
        metadata={
            "name": "DUT",
            "type": "Element",
        },
    )
    itf: Optional[Itf] = field(
        default=None,
        metadata={
            "name": "Itf",
            "type": "Element",
        },
    )
    gvl: Optional[Gvl] = field(
        default=None,
        metadata={
            "name": "GVL",
            "type": "Element",
        },
    )