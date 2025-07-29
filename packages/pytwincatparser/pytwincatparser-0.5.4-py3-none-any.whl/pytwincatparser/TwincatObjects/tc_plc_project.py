from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass
class LibraryCategory:
    class Meta:
        namespace = ""

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "name": "Version",
            "type": "Element",
            "required": True,
        },
    )
    default_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DefaultName",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Compile:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    include: Optional[str] = field(
        default=None,
        metadata={
            "name": "Include",
            "type": "Attribute",
            "required": True,
        },
    )
    sub_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SubType",
            "type": "Element",
            "required": True,
        },
    )
    exclude_from_build: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ExcludeFromBuild",
            "type": "Element",
        },
    )


@dataclass
class Folder:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    include: Optional[str] = field(
        default=None,
        metadata={
            "name": "Include",
            "type": "Attribute",
            "required": True,
        },
    )
    exclude_from_build: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ExcludeFromBuild",
            "type": "Element",
        },
    )


@dataclass
class NoneType:
    class Meta:
        name = "None"
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    include: Optional[str] = field(
        default=None,
        metadata={
            "name": "Include",
            "type": "Attribute",
            "required": True,
        },
    )
    sub_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SubType",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class PlaceholderReference:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    include: Optional[str] = field(
        default=None,
        metadata={
            "name": "Include",
            "type": "Attribute",
            "required": True,
        },
    )
    default_resolution: Optional[str] = field(
        default=None,
        metadata={
            "name": "DefaultResolution",
            "type": "Element",
            "required": True,
        },
    )
    namespace: Optional[str] = field(
        default=None,
        metadata={
            "name": "Namespace",
            "type": "Element",
            "required": True,
        },
    )
    system_library: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SystemLibrary",
            "type": "Element",
        },
    )
    resolver_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResolverGuid",
            "type": "Element",
        },
    )
    publish_symbols_in_container: Optional[bool] = field(
        default=None,
        metadata={
            "name": "PublishSymbolsInContainer",
            "type": "Element",
        },
    )
    qualified_only: Optional[bool] = field(
        default=None,
        metadata={
            "name": "QualifiedOnly",
            "type": "Element",
        },
    )


@dataclass
class SelectedLibraryCategories:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


@dataclass
class SubObject:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    include: Optional[str] = field(
        default=None,
        metadata={
            "name": "Include",
            "type": "Attribute",
            "required": True,
        },
    )
    exclude_from_build: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ExcludeFromBuild",
            "type": "Element",
        },
    )


@dataclass
class Type:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    n: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class D:
    class Meta:
        name = "d"
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    n: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    t: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    ckt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cvt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    v: list[Union[int, str, bool]] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "sequence": 1,
        },
    )
    o: list["O1"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "sequence": 1,
        },
    )


@dataclass
class V:
    class Meta:
        name = "v"
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    n: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class ItemGroup:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    sub_object: list[SubObject] = field(
        default_factory=list,
        metadata={
            "name": "SubObject",
            "type": "Element",
        },
    )
    placeholder_reference: list[PlaceholderReference] = field(
        default_factory=list,
        metadata={
            "name": "PlaceholderReference",
            "type": "Element",
        },
    )
    none: Optional[NoneType] = field(
        default=None,
        metadata={
            "name": "None",
            "type": "Element",
        },
    )
    compile: list[Compile] = field(
        default_factory=list,
        metadata={
            "name": "Compile",
            "type": "Element",
        },
    )
    folder: list[Folder] = field(
        default_factory=list,
        metadata={
            "name": "Folder",
            "type": "Element",
        },
    )


@dataclass
class LibraryCategories:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    library_category: Optional[LibraryCategory] = field(
        default=None,
        metadata={
            "name": "LibraryCategory",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


@dataclass
class TypeList:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    type_value: list[Type] = field(
        default_factory=list,
        metadata={
            "name": "Type",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class O1:
    class Meta:
        name = "o"
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    space: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    t: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    v: Optional[V] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    d: list[D] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Data:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    o: Optional[O1] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class PropertyGroup:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    file_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "FileVersion",
            "type": "Element",
            "required": True,
        },
    )
    schema_version: Optional[float] = field(
        default=None,
        metadata={
            "name": "SchemaVersion",
            "type": "Element",
            "required": True,
        },
    )
    project_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProjectGuid",
            "type": "Element",
            "required": True,
        },
    )
    sub_objects_sorted_by_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SubObjectsSortedByName",
            "type": "Element",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
        },
    )
    program_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProgramVersion",
            "type": "Element",
            "required": True,
        },
    )
    application: Optional[str] = field(
        default=None,
        metadata={
            "name": "Application",
            "type": "Element",
            "required": True,
        },
    )
    type_system: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeSystem",
            "type": "Element",
            "required": True,
        },
    )
    implicit_task_info: Optional[str] = field(
        default=None,
        metadata={
            "name": "Implicit_Task_Info",
            "type": "Element",
            "required": True,
        },
    )
    implicit_kind_of_task: Optional[str] = field(
        default=None,
        metadata={
            "name": "Implicit_KindOfTask",
            "type": "Element",
            "required": True,
        },
    )
    implicit_jitter_distribution: Optional[str] = field(
        default=None,
        metadata={
            "name": "Implicit_Jitter_Distribution",
            "type": "Element",
            "required": True,
        },
    )
    library_references: Optional[str] = field(
        default=None,
        metadata={
            "name": "LibraryReferences",
            "type": "Element",
            "required": True,
        },
    )
    combine_ids: Optional[bool] = field(
        default=None,
        metadata={
            "name": "CombineIds",
            "type": "Element",
            "required": True,
        },
    )
    released: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Released",
            "type": "Element",
            "required": True,
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "Title",
            "type": "Element",
            "required": True,
        },
    )
    default_namespace: Optional[str] = field(
        default=None,
        metadata={
            "name": "DefaultNamespace",
            "type": "Element",
            "required": True,
        },
    )
    placeholder: Optional[str] = field(
        default=None,
        metadata={
            "name": "Placeholder",
            "type": "Element",
            "required": True,
        },
    )
    author: Optional[str] = field(
        default=None,
        metadata={
            "name": "Author",
            "type": "Element",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "required": True,
        },
    )
    company: Optional[str] = field(
        default=None,
        metadata={
            "name": "Company",
            "type": "Element",
            "required": True,
        },
    )
    project_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProjectVersion",
            "type": "Element",
            "required": True,
        },
    )
    library_categories: Optional[LibraryCategories] = field(
        default=None,
        metadata={
            "name": "LibraryCategories",
            "type": "Element",
            "required": True,
        },
    )
    selected_library_categories: Optional[SelectedLibraryCategories] = field(
        default=None,
        metadata={
            "name": "SelectedLibraryCategories",
            "type": "Element",
            "required": True,
        },
    )
    compiler_defines: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompilerDefines",
            "type": "Element",
            "required": True,
        },
    )
    doc_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocFormat",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class XmlArchive:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    data: Optional[Data] = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "required": True,
        },
    )
    type_list: Optional[TypeList] = field(
        default=None,
        metadata={
            "name": "TypeList",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class PlcProjectOptions:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    xml_archive: Optional[XmlArchive] = field(
        default=None,
        metadata={
            "name": "XmlArchive",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ProjectExtensions:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    plc_project_options: Optional[PlcProjectOptions] = field(
        default=None,
        metadata={
            "name": "PlcProjectOptions",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Project:
    class Meta:
        namespace = "http://schemas.microsoft.com/developer/msbuild/2003"

    default_targets: Optional[str] = field(
        default=None,
        metadata={
            "name": "DefaultTargets",
            "type": "Attribute",
            "required": True,
        },
    )
    property_group: Optional[PropertyGroup] = field(
        default=None,
        metadata={
            "name": "PropertyGroup",
            "type": "Element",
            "required": True,
        },
    )
    item_group: list[ItemGroup] = field(
        default_factory=list,
        metadata={
            "name": "ItemGroup",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    project_extensions: Optional[ProjectExtensions] = field(
        default=None,
        metadata={
            "name": "ProjectExtensions",
            "type": "Element",
            "required": True,
        },
    )
