from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class SolutionProject:
    """Represents a project entry in a TwinCAT solution file."""
    project_type_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProjectTypeGuid",
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
    path: Optional[str] = field(
        default=None,
        metadata={
            "name": "Path",
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


@dataclass
class ConfigurationPlatform:
    """Represents a configuration platform in the solution."""
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ProjectConfiguration:
    """Represents a project's configuration for a specific platform."""
    project_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProjectGuid",
            "type": "Element",
            "required": True,
        },
    )
    platform_config: Optional[str] = field(
        default=None,
        metadata={
            "name": "PlatformConfig",
            "type": "Element",
            "required": True,
        },
    )
    active_cfg: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActiveCfg",
            "type": "Element",
            "required": True,
        },
    )
    build: Optional[str] = field(
        default=None,
        metadata={
            "name": "Build",
            "type": "Element",
        },
    )


@dataclass
class SolutionProperties:
    """Represents solution properties."""
    hide_solution_node: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HideSolutionNode",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ExtensibilityGlobals:
    """Represents extensibility globals for the solution."""
    solution_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "SolutionGuid",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class SolutionConfigurationPlatforms:
    """Represents the solution configuration platforms section."""
    configuration_platforms: List[ConfigurationPlatform] = field(
        default_factory=list,
        metadata={
            "name": "ConfigurationPlatform",
            "type": "Element",
            "min_occurs": 0,
        },
    )


@dataclass
class ProjectConfigurationPlatforms:
    """Represents the project configuration platforms section."""
    project_configurations: List[ProjectConfiguration] = field(
        default_factory=list,
        metadata={
            "name": "ProjectConfiguration",
            "type": "Element",
            "min_occurs": 0,
        },
    )


@dataclass
class GlobalSection:
    """Represents a global section in the solution file."""
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "required": True,
        },
    )
    position: Optional[str] = field(
        default=None,
        metadata={
            "name": "Position",
            "type": "Attribute",
            "required": True,
        },
    )
    solution_configuration_platforms: Optional[SolutionConfigurationPlatforms] = field(
        default=None,
        metadata={
            "name": "SolutionConfigurationPlatforms",
            "type": "Element",
        },
    )
    project_configuration_platforms: Optional[ProjectConfigurationPlatforms] = field(
        default=None,
        metadata={
            "name": "ProjectConfigurationPlatforms",
            "type": "Element",
        },
    )
    solution_properties: Optional[SolutionProperties] = field(
        default=None,
        metadata={
            "name": "SolutionProperties",
            "type": "Element",
        },
    )
    extensibility_globals: Optional[ExtensibilityGlobals] = field(
        default=None,
        metadata={
            "name": "ExtensibilityGlobals",
            "type": "Element",
        },
    )


@dataclass
class Global:
    """Represents the Global section of the solution file."""
    global_sections: List[GlobalSection] = field(
        default_factory=list,
        metadata={
            "name": "GlobalSection",
            "type": "Element",
            "min_occurs": 0,
        },
    )


@dataclass
class TwincatSolution:
    """Represents a TwinCAT solution file."""
    format_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "FormatVersion",
            "type": "Element",
            "required": True,
        },
    )
    tcxae_shell_format_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "TcXaeShellFormatVersion",
            "type": "Element",
            "required": True,
        },
    )
    visual_studio_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "VisualStudioVersion",
            "type": "Element",
            "required": True,
        },
    )
    minimum_visual_studio_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "MinimumVisualStudioVersion",
            "type": "Element",
            "required": True,
        },
    )
    projects: List[SolutionProject] = field(
        default_factory=list,
        metadata={
            "name": "Project",
            "type": "Element",
            "min_occurs": 0,
        },
    )
    global_section: Optional[Global] = field(
        default=None,
        metadata={
            "name": "Global",
            "type": "Element",
            "required": True,
        },
    )
