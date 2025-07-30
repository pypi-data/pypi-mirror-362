from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Clsid:
    class Meta:
        name = "CLSID"

    class_factory: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClassFactory",
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
class IoIdleTask:
    priority: Optional[int] = field(
        default=None,
        metadata={
            "name": "Priority",
            "type": "Attribute",
            "required": True,
        },
    )
    cycle_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "CycleTime",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ManualConfig:
    otcid: Optional[str] = field(
        default=None,
        metadata={
            "name": "OTCID",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Target:
    bkhf_order: Optional[int] = field(
        default=None,
        metadata={
            "name": "BkhfOrder",
            "type": "Attribute",
            "required": True,
        },
    )
    custom_order: Optional[str] = field(
        default=None,
        metadata={
            "name": "CustomOrder",
            "type": "Attribute",
            "required": True,
        },
    )
    custom_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "CustomComment",
            "type": "Element",
            "required": True,
        },
    )
    manual_select: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManualSelect",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Task:
    id: Optional[int] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    priority: Optional[int] = field(
        default=None,
        metadata={
            "name": "Priority",
            "type": "Attribute",
            "required": True,
        },
    )
    cycle_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "CycleTime",
            "type": "Attribute",
            "required": True,
        },
    )
    ams_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "AmsPort",
            "type": "Attribute",
            "required": True,
        },
    )
    watchdog_stack_capacity: Optional[int] = field(
        default=None,
        metadata={
            "name": "WatchdogStackCapacity",
            "type": "Attribute",
        },
    )
    adt_tasks: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AdtTasks",
            "type": "Attribute",
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


@dataclass
class TaskPouOid:
    prio: Optional[int] = field(
        default=None,
        metadata={
            "name": "Prio",
            "type": "Attribute",
            "required": True,
        },
    )
    otcid: Optional[str] = field(
        default=None,
        metadata={
            "name": "OTCID",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Context:
    id: Optional[int] = field(
        default=None,
        metadata={
            "name": "Id",
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
    manual_config: Optional[ManualConfig] = field(
        default=None,
        metadata={
            "name": "ManualConfig",
            "type": "Element",
            "required": True,
        },
    )
    priority: Optional[int] = field(
        default=None,
        metadata={
            "name": "Priority",
            "type": "Element",
            "required": True,
        },
    )
    cycle_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "CycleTime",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Licenses:
    target: Optional[Target] = field(
        default=None,
        metadata={
            "name": "Target",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Settings:
    router_memory: Optional[int] = field(
        default=None,
        metadata={
            "name": "RouterMemory",
            "type": "Attribute",
            "required": True,
        },
    )
    io_idle_task: Optional[IoIdleTask] = field(
        default=None,
        metadata={
            "name": "IoIdleTask",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class TaskPouOids:
    task_pou_oid: Optional[TaskPouOid] = field(
        default=None,
        metadata={
            "name": "TaskPouOid",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Tasks:
    task: list[Task] = field(
        default_factory=list,
        metadata={
            "name": "Task",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Contexts:
    context: Optional[Context] = field(
        default=None,
        metadata={
            "name": "Context",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class System:
    settings: Optional[Settings] = field(
        default=None,
        metadata={
            "name": "Settings",
            "type": "Element",
            "required": True,
        },
    )
    licenses: Optional[Licenses] = field(
        default=None,
        metadata={
            "name": "Licenses",
            "type": "Element",
            "required": True,
        },
    )
    tasks: Optional[Tasks] = field(
        default=None,
        metadata={
            "name": "Tasks",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Instance:
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )
    tc_sm_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "TcSmClass",
            "type": "Attribute",
            "required": True,
        },
    )
    keep_unrestored_links: Optional[int] = field(
        default=None,
        metadata={
            "name": "KeepUnrestoredLinks",
            "type": "Attribute",
            "required": True,
        },
    )
    tmc_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "TmcPath",
            "type": "Attribute",
            "required": True,
        },
    )
    tmc_hash: Optional[str] = field(
        default=None,
        metadata={
            "name": "TmcHash",
            "type": "Attribute",
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
    clsid: Optional[Clsid] = field(
        default=None,
        metadata={
            "name": "CLSID",
            "type": "Element",
            "required": True,
        },
    )
    contexts: Optional[Contexts] = field(
        default=None,
        metadata={
            "name": "Contexts",
            "type": "Element",
            "required": True,
        },
    )
    task_pou_oids: Optional[TaskPouOids] = field(
        default=None,
        metadata={
            "name": "TaskPouOids",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Project:
    guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
        },
    )
    prj_file_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrjFilePath",
            "type": "Attribute",
        },
    )
    tmc_file_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "TmcFilePath",
            "type": "Attribute",
        },
    )
    reload_tmc: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ReloadTmc",
            "type": "Attribute",
        },
    )
    ams_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "AmsPort",
            "type": "Attribute",
        },
    )
    file_archive_settings: Optional[str] = field(
        default=None,
        metadata={
            "name": "FileArchiveSettings",
            "type": "Attribute",
        },
    )
    symbolic_mapping: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SymbolicMapping",
            "type": "Attribute",
        },
    )
    instance: Optional[Instance] = field(
        default=None,
        metadata={
            "name": "Instance",
            "type": "Element",
        },
    )
    project_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProjectGUID",
            "type": "Attribute",
        },
    )
    target64_bit: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Target64Bit",
            "type": "Attribute",
        },
    )
    show_hide_configurations: Optional[str] = field(
        default=None,
        metadata={
            "name": "ShowHideConfigurations",
            "type": "Attribute",
        },
    )
    system: Optional[System] = field(
        default=None,
        metadata={
            "name": "System",
            "type": "Element",
        },
    )
    plc: Optional["Plc"] = field(
        default=None,
        metadata={
            "name": "Plc",
            "type": "Element",
        },
    )
    file: Optional[str] = field(
        default=None,
        metadata={
            "name": "File",
            "type": "Attribute",
        },
    )


@dataclass
class Plc:
    project: list[Project] = field(
        default_factory=list,
        metadata={
            "name": "Project",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class TcSmProject:
    no_namespace_schema_location: Optional[str] = field(
        default=None,
        metadata={
            "name": "noNamespaceSchemaLocation",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
            "required": True,
        },
    )
    tc_sm_version: Optional[float] = field(
        default=None,
        metadata={
            "name": "TcSmVersion",
            "type": "Attribute",
            "required": True,
        },
    )
    tc_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "TcVersion",
            "type": "Attribute",
            "required": True,
        },
    )
    tc_version_fixed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "TcVersionFixed",
            "type": "Attribute",
            "required": True,
        },
    )
    project: Optional[Project] = field(
        default=None,
        metadata={
            "name": "Project",
            "type": "Element",
            "required": True,
        },
    )
