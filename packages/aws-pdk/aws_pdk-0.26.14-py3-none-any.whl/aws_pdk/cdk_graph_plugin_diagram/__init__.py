from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

from ..cdk_graph import (
    CdkGraphArtifact as _CdkGraphArtifact_0059de6d,
    FilterPreset as _FilterPreset_47315c13,
    ICdkGraphPlugin as _ICdkGraphPlugin_b5ef2d02,
    IGraphFilterPlan as _IGraphFilterPlan_106744ef,
    IGraphPluginBindCallback as _IGraphPluginBindCallback_58b6edd3,
    IGraphReportCallback as _IGraphReportCallback_858cc871,
)


@jsii.implements(_ICdkGraphPlugin_b5ef2d02)
class CdkGraphDiagramPlugin(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph_plugin_diagram.CdkGraphDiagramPlugin",
):
    '''CdkGraphDiagramPlugin is a {@link ICdkGraphPluginCdkGraph Plugin} implementation for generating diagram artifacts from the {@link CdkGraph} framework.'''

    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Union["IDiagramConfigBase", typing.Dict[builtins.str, typing.Any]]] = None,
        diagrams: typing.Optional[typing.Sequence[typing.Union["IDiagramConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param defaults: Default configuration to apply to all diagrams.
        :param diagrams: List of diagram configurations to generate diagrams.
        '''
        config = IPluginConfig(defaults=defaults, diagrams=diagrams)

        jsii.create(self.__class__, self, [config])

    @jsii.member(jsii_name="artifactFilename")
    @builtins.classmethod
    def artifact_filename(
        cls,
        name: builtins.str,
        format: "DiagramFormat",
    ) -> builtins.str:
        '''Get standardized artifact file name for diagram artifacts.

        :param name: -
        :param format: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4346963f07e4e9c3b8383a218621295b8ef3268cc57838f451eb9df609af3c70)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "artifactFilename", [name, format]))

    @jsii.member(jsii_name="artifactId")
    @builtins.classmethod
    def artifact_id(cls, name: builtins.str, format: "DiagramFormat") -> builtins.str:
        '''Get standardized artifact id for diagram artifacts.

        :param name: -
        :param format: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30660626fed6954ad6226458572b6fed7f29b3a1846a993d63d71c4243c55632)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "artifactId", [name, format]))

    @jsii.member(jsii_name="getDiagramArtifact")
    def get_diagram_artifact(
        self,
        name: builtins.str,
        format: "DiagramFormat",
    ) -> typing.Optional[_CdkGraphArtifact_0059de6d]:
        '''Get diagram artifact for a given name and format.

        :param name: -
        :param format: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e4a1adae905752cca74bb474bf98e36ace3c448910ee031c4742a70a25445a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        return typing.cast(typing.Optional[_CdkGraphArtifact_0059de6d], jsii.invoke(self, "getDiagramArtifact", [name, format]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ARTIFACT_NS")
    def ARTIFACT_NS(cls) -> builtins.str:
        '''Namespace for artifacts of the diagram plugin.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ARTIFACT_NS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ID")
    def ID(cls) -> builtins.str:
        '''Fixed id of the diagram plugin.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION")
    def VERSION(cls) -> builtins.str:
        '''Current semantic version of the diagram plugin.'''
        return typing.cast(builtins.str, jsii.sget(cls, "VERSION"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "IPluginConfig":
        '''Get diagram plugin config.'''
        return typing.cast("IPluginConfig", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for this plugin.

        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''Plugin version.

        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="defaultDotArtifact")
    def default_dot_artifact(self) -> typing.Optional[_CdkGraphArtifact_0059de6d]:
        '''Get default dot artifact.'''
        return typing.cast(typing.Optional[_CdkGraphArtifact_0059de6d], jsii.get(self, "defaultDotArtifact"))

    @builtins.property
    @jsii.member(jsii_name="defaultPngArtifact")
    def default_png_artifact(self) -> typing.Optional[_CdkGraphArtifact_0059de6d]:
        '''Get default PNG artifact.'''
        return typing.cast(typing.Optional[_CdkGraphArtifact_0059de6d], jsii.get(self, "defaultPngArtifact"))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]).

        :inheritdoc: true
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="bind")
    def bind(self) -> _IGraphPluginBindCallback_58b6edd3:
        '''Binds the plugin to the CdkGraph instance.

        Enables plugins to receive base configs.

        :inheritdoc: true
        '''
        return typing.cast(_IGraphPluginBindCallback_58b6edd3, jsii.get(self, "bind"))

    @bind.setter
    def bind(self, value: _IGraphPluginBindCallback_58b6edd3) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62fd8490a6fe5c8a58c2949b1b834be775be44e10b1e0f512d048d3d48d14d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="report")
    def report(self) -> typing.Optional[_IGraphReportCallback_858cc871]:
        '''Generate asynchronous reports based on the graph.

        This is not automatically called when synthesizing CDK.
        Developer must explicitly add ``await graphInstance.report()`` to the CDK bin or invoke this outside
        of the CDK synth. In either case, the plugin receives the in-memory graph interface when invoked, as the
        CdkGraph will deserialize the graph prior to invoking the plugin report.

        :inheritdoc: true
        '''
        return typing.cast(typing.Optional[_IGraphReportCallback_858cc871], jsii.get(self, "report"))

    @report.setter
    def report(self, value: typing.Optional[_IGraphReportCallback_858cc871]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2478a8d6de8d0b65c7e28e6ee42176f82ac6fa77bb6a501926430454aa9ea04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "report", value) # pyright: ignore[reportArgumentType]


@jsii.enum(jsii_type="@aws/pdk.cdk_graph_plugin_diagram.DiagramFormat")
class DiagramFormat(enum.Enum):
    '''Supported diagram formats that can be generated.

    Extended formats are automatically generated, for example if you generate "png" which extends
    "svg" which extends "dot", the resulting generated files will be all aforementioned.
    '''

    DOT = "DOT"
    '''Graphviz `DOT Language <https://graphviz.org/doc/info/lang.html>`_.'''
    SVG = "SVG"
    '''`SVG <https://developer.mozilla.org/en-US/docs/Web/SVG>`_ generated using `dot-wasm <https://hpcc-systems.github.io/hpcc-js-wasm/classes/graphviz.Graphviz.html>`_ from {@link DiagramFormat.DOT} file.

    :extends: DiagramFormat.DOT
    '''
    PNG = "PNG"
    '''`PNG <https://en.wikipedia.org/wiki/Portable_Network_Graphics>`_ generated using `sharp <https://sharp.pixelplumbing.com/api-output#png>`_ from {@link DiagramFormat.SVG} file.

    :extends: DiagramFormat.SVG
    '''


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph_plugin_diagram.DiagramOptions",
    jsii_struct_bases=[],
    name_mapping={
        "title": "title",
        "node_positions": "nodePositions",
        "preset": "preset",
        "theme": "theme",
    },
)
class DiagramOptions:
    def __init__(
        self,
        *,
        title: builtins.str,
        node_positions: typing.Optional[typing.Mapping[builtins.str, "INodePosition"]] = None,
        preset: typing.Optional[_FilterPreset_47315c13] = None,
        theme: typing.Optional[typing.Union[builtins.str, "IGraphThemeConfigAlt"]] = None,
    ) -> None:
        '''Options for diagrams.

        :param title: 
        :param node_positions: 
        :param preset: 
        :param theme: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3019720d8f4e085ad4bfbad17e4e6e3436b97f1a0e3718ae6413f430f4ed97a9)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument node_positions", value=node_positions, expected_type=type_hints["node_positions"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "title": title,
        }
        if node_positions is not None:
            self._values["node_positions"] = node_positions
        if preset is not None:
            self._values["preset"] = preset
        if theme is not None:
            self._values["theme"] = theme

    @builtins.property
    def title(self) -> builtins.str:
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_positions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "INodePosition"]]:
        result = self._values.get("node_positions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "INodePosition"]], result)

    @builtins.property
    def preset(self) -> typing.Optional[_FilterPreset_47315c13]:
        result = self._values.get("preset")
        return typing.cast(typing.Optional[_FilterPreset_47315c13], result)

    @builtins.property
    def theme(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IGraphThemeConfigAlt"]]:
        result = self._values.get("theme")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IGraphThemeConfigAlt"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiagramOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws/pdk.cdk_graph_plugin_diagram.GraphThemeRenderingIconTarget")
class GraphThemeRenderingIconTarget(enum.Enum):
    '''Icon rendering target options for GraphTheme.'''

    DATA = "DATA"
    '''Data icon (eg: EC2 instance type icon, T2).

    Resolution precedence: ``data => resource => general => service => category``
    '''
    RESOURCE = "RESOURCE"
    '''Resource icon.

    Resolution precedence: ``resource => general => service => category``
    '''
    GENERAL = "GENERAL"
    '''General icon.

    Resolution precedence: ``resource => general => service => category``
    '''
    SERVICE = "SERVICE"
    '''Service icon.

    Resolution precedence: ``service => category``
    '''
    CATEGORY = "CATEGORY"
    '''Category icon.

    Resolution precedence: ``category``
    '''


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph_plugin_diagram.IDiagramConfigBase",
    jsii_struct_bases=[],
    name_mapping={
        "filter_plan": "filterPlan",
        "format": "format",
        "node_positions": "nodePositions",
        "theme": "theme",
    },
)
class IDiagramConfigBase:
    def __init__(
        self,
        *,
        filter_plan: typing.Optional[typing.Union[_IGraphFilterPlan_106744ef, typing.Dict[builtins.str, typing.Any]]] = None,
        format: typing.Optional[typing.Union[DiagramFormat, typing.Sequence[DiagramFormat]]] = None,
        node_positions: typing.Optional[typing.Mapping[builtins.str, "INodePosition"]] = None,
        theme: typing.Optional[typing.Union[builtins.str, "IGraphThemeConfigAlt"]] = None,
    ) -> None:
        '''Base config to specific a unique diagram to be generated.

        :param filter_plan: Graph {@link IGraphFilterPlanFilter Plan} used to generate a unique diagram.
        :param format: The output format(s) to generated. Default: ``DiagramFormat.PNG`` - which will through extension also generate ``DiagramFormat.SVG`` and ``DiagramFormat.DOT``
        :param node_positions: Config for predetermined node positions given their CDK construct id.
        :param theme: Config for graph theme.
        '''
        if isinstance(filter_plan, dict):
            filter_plan = _IGraphFilterPlan_106744ef(**filter_plan)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b574db97ce884a6029ce524ba5a0bcf4120c926644bb305c271f9942a4bff53)
            check_type(argname="argument filter_plan", value=filter_plan, expected_type=type_hints["filter_plan"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument node_positions", value=node_positions, expected_type=type_hints["node_positions"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_plan is not None:
            self._values["filter_plan"] = filter_plan
        if format is not None:
            self._values["format"] = format
        if node_positions is not None:
            self._values["node_positions"] = node_positions
        if theme is not None:
            self._values["theme"] = theme

    @builtins.property
    def filter_plan(self) -> typing.Optional[_IGraphFilterPlan_106744ef]:
        '''Graph {@link IGraphFilterPlanFilter Plan}  used to generate a unique diagram.'''
        result = self._values.get("filter_plan")
        return typing.cast(typing.Optional[_IGraphFilterPlan_106744ef], result)

    @builtins.property
    def format(
        self,
    ) -> typing.Optional[typing.Union[DiagramFormat, typing.List[DiagramFormat]]]:
        '''The output format(s) to generated.

        :default: ``DiagramFormat.PNG`` - which will through extension also generate ``DiagramFormat.SVG`` and ``DiagramFormat.DOT``
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[typing.Union[DiagramFormat, typing.List[DiagramFormat]]], result)

    @builtins.property
    def node_positions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "INodePosition"]]:
        '''Config for predetermined node positions given their CDK construct id.'''
        result = self._values.get("node_positions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "INodePosition"]], result)

    @builtins.property
    def theme(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IGraphThemeConfigAlt"]]:
        '''Config for graph theme.'''
        result = self._values.get("theme")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IGraphThemeConfigAlt"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IDiagramConfigBase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws/pdk.cdk_graph_plugin_diagram.IGraphThemeConfigAlt")
class IGraphThemeConfigAlt(typing_extensions.Protocol):
    '''GraphThemeConfigAlt is simplified definition of theme to apply.'''

    @builtins.property
    @jsii.member(jsii_name="rendering")
    def rendering(self) -> typing.Optional["IGraphThemeRendering"]:
        ...

    @builtins.property
    @jsii.member(jsii_name="theme")
    def theme(self) -> typing.Optional[builtins.str]:
        ...


class _IGraphThemeConfigAltProxy:
    '''GraphThemeConfigAlt is simplified definition of theme to apply.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph_plugin_diagram.IGraphThemeConfigAlt"

    @builtins.property
    @jsii.member(jsii_name="rendering")
    def rendering(self) -> typing.Optional["IGraphThemeRendering"]:
        return typing.cast(typing.Optional["IGraphThemeRendering"], jsii.get(self, "rendering"))

    @builtins.property
    @jsii.member(jsii_name="theme")
    def theme(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "theme"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphThemeConfigAlt).__jsii_proxy_class__ = lambda : _IGraphThemeConfigAltProxy


@jsii.interface(
    jsii_type="@aws/pdk.cdk_graph_plugin_diagram.IGraphThemeRenderingIconProps"
)
class IGraphThemeRenderingIconProps(typing_extensions.Protocol):
    '''Icon specific properties for configuring graph rendering of resource icons.'''

    @builtins.property
    @jsii.member(jsii_name="cfnResourceIconMax")
    def cfn_resource_icon_max(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''Highest Graph.CfnResourceNode icon to render.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="cfnResourceIconMin")
    def cfn_resource_icon_min(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''Lowest Graph.CfnResourceNode icon to render.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="resourceIconMax")
    def resource_icon_max(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''Highest Graph.ResourceNode icon to render.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="resourceIconMin")
    def resource_icon_min(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''Lowest Graph.ResourceNode icon to render.'''
        ...


class _IGraphThemeRenderingIconPropsProxy:
    '''Icon specific properties for configuring graph rendering of resource icons.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph_plugin_diagram.IGraphThemeRenderingIconProps"

    @builtins.property
    @jsii.member(jsii_name="cfnResourceIconMax")
    def cfn_resource_icon_max(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''Highest Graph.CfnResourceNode icon to render.'''
        return typing.cast(typing.Optional[GraphThemeRenderingIconTarget], jsii.get(self, "cfnResourceIconMax"))

    @builtins.property
    @jsii.member(jsii_name="cfnResourceIconMin")
    def cfn_resource_icon_min(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''Lowest Graph.CfnResourceNode icon to render.'''
        return typing.cast(typing.Optional[GraphThemeRenderingIconTarget], jsii.get(self, "cfnResourceIconMin"))

    @builtins.property
    @jsii.member(jsii_name="resourceIconMax")
    def resource_icon_max(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''Highest Graph.ResourceNode icon to render.'''
        return typing.cast(typing.Optional[GraphThemeRenderingIconTarget], jsii.get(self, "resourceIconMax"))

    @builtins.property
    @jsii.member(jsii_name="resourceIconMin")
    def resource_icon_min(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''Lowest Graph.ResourceNode icon to render.'''
        return typing.cast(typing.Optional[GraphThemeRenderingIconTarget], jsii.get(self, "resourceIconMin"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphThemeRenderingIconProps).__jsii_proxy_class__ = lambda : _IGraphThemeRenderingIconPropsProxy


@jsii.interface(
    jsii_type="@aws/pdk.cdk_graph_plugin_diagram.IGraphThemeRenderingOptions"
)
class IGraphThemeRenderingOptions(typing_extensions.Protocol):
    '''Additional graph rendering options.'''

    @builtins.property
    @jsii.member(jsii_name="layout")
    def layout(self) -> typing.Optional[builtins.str]:
        '''Layout direction of the graph.

        :default: horizontal
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional[builtins.str]:
        '''Specify regex pattern to match root stacks to render.

        :default: undefined Will render all stacks
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional[builtins.str]:
        '''Specify which stage to render when multiple stages are available.

        Can be a preset value of "first", "last", and "all", or regex string of the stage(s) to render.

        :default: last
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="unconstrainedCrossClusterEdges")
    def unconstrained_cross_cluster_edges(self) -> typing.Optional[builtins.bool]:
        '''Prevent cross-cluster edges from ranking nodes in layout.

        :default: false

        :see: https://graphviz.org/docs/attrs/constraint/
        '''
        ...


class _IGraphThemeRenderingOptionsProxy:
    '''Additional graph rendering options.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph_plugin_diagram.IGraphThemeRenderingOptions"

    @builtins.property
    @jsii.member(jsii_name="layout")
    def layout(self) -> typing.Optional[builtins.str]:
        '''Layout direction of the graph.

        :default: horizontal
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "layout"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional[builtins.str]:
        '''Specify regex pattern to match root stacks to render.

        :default: undefined Will render all stacks
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stack"))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional[builtins.str]:
        '''Specify which stage to render when multiple stages are available.

        Can be a preset value of "first", "last", and "all", or regex string of the stage(s) to render.

        :default: last
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stage"))

    @builtins.property
    @jsii.member(jsii_name="unconstrainedCrossClusterEdges")
    def unconstrained_cross_cluster_edges(self) -> typing.Optional[builtins.bool]:
        '''Prevent cross-cluster edges from ranking nodes in layout.

        :default: false

        :see: https://graphviz.org/docs/attrs/constraint/
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "unconstrainedCrossClusterEdges"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphThemeRenderingOptions).__jsii_proxy_class__ = lambda : _IGraphThemeRenderingOptionsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph_plugin_diagram.INodePosition")
class INodePosition(typing_extensions.Protocol):
    '''Positional coordinates for a node in inches.'''

    @builtins.property
    @jsii.member(jsii_name="x")
    def x(self) -> jsii.Number:
        ...

    @builtins.property
    @jsii.member(jsii_name="y")
    def y(self) -> jsii.Number:
        ...


class _INodePositionProxy:
    '''Positional coordinates for a node in inches.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph_plugin_diagram.INodePosition"

    @builtins.property
    @jsii.member(jsii_name="x")
    def x(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "x"))

    @builtins.property
    @jsii.member(jsii_name="y")
    def y(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "y"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodePosition).__jsii_proxy_class__ = lambda : _INodePositionProxy


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph_plugin_diagram.IPluginConfig",
    jsii_struct_bases=[],
    name_mapping={"defaults": "defaults", "diagrams": "diagrams"},
)
class IPluginConfig:
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Union[IDiagramConfigBase, typing.Dict[builtins.str, typing.Any]]] = None,
        diagrams: typing.Optional[typing.Sequence[typing.Union["IDiagramConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Plugin configuration for diagram plugin.

        :param defaults: Default configuration to apply to all diagrams.
        :param diagrams: List of diagram configurations to generate diagrams.
        '''
        if isinstance(defaults, dict):
            defaults = IDiagramConfigBase(**defaults)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2adfa41ae4eaeab3ece8e56a1f97cefd4038a38e982ab24e64dae37cc45764cd)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument diagrams", value=diagrams, expected_type=type_hints["diagrams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if defaults is not None:
            self._values["defaults"] = defaults
        if diagrams is not None:
            self._values["diagrams"] = diagrams

    @builtins.property
    def defaults(self) -> typing.Optional[IDiagramConfigBase]:
        '''Default configuration to apply to all diagrams.'''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[IDiagramConfigBase], result)

    @builtins.property
    def diagrams(self) -> typing.Optional[typing.List["IDiagramConfig"]]:
        '''List of diagram configurations to generate diagrams.'''
        result = self._values.get("diagrams")
        return typing.cast(typing.Optional[typing.List["IDiagramConfig"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IPluginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph_plugin_diagram.IDiagramConfig",
    jsii_struct_bases=[IDiagramConfigBase],
    name_mapping={
        "filter_plan": "filterPlan",
        "format": "format",
        "node_positions": "nodePositions",
        "theme": "theme",
        "name": "name",
        "title": "title",
        "ignore_defaults": "ignoreDefaults",
    },
)
class IDiagramConfig(IDiagramConfigBase):
    def __init__(
        self,
        *,
        filter_plan: typing.Optional[typing.Union[_IGraphFilterPlan_106744ef, typing.Dict[builtins.str, typing.Any]]] = None,
        format: typing.Optional[typing.Union[DiagramFormat, typing.Sequence[DiagramFormat]]] = None,
        node_positions: typing.Optional[typing.Mapping[builtins.str, INodePosition]] = None,
        theme: typing.Optional[typing.Union[builtins.str, IGraphThemeConfigAlt]] = None,
        name: builtins.str,
        title: builtins.str,
        ignore_defaults: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Diagram configuration definition.

        :param filter_plan: Graph {@link IGraphFilterPlanFilter Plan} used to generate a unique diagram.
        :param format: The output format(s) to generated. Default: ``DiagramFormat.PNG`` - which will through extension also generate ``DiagramFormat.SVG`` and ``DiagramFormat.DOT``
        :param node_positions: Config for predetermined node positions given their CDK construct id.
        :param theme: Config for graph theme.
        :param name: Name of the diagram. Used as the basename of the generated file(s) which gets the extension appended.
        :param title: The title of the diagram.
        :param ignore_defaults: Indicates if default diagram config is applied as defaults to this config. Default: false
        '''
        if isinstance(filter_plan, dict):
            filter_plan = _IGraphFilterPlan_106744ef(**filter_plan)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30354dea79562b734bd6bd3e6c15fccb355105edbf147fdb0790dcca3730ddb5)
            check_type(argname="argument filter_plan", value=filter_plan, expected_type=type_hints["filter_plan"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument node_positions", value=node_positions, expected_type=type_hints["node_positions"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument ignore_defaults", value=ignore_defaults, expected_type=type_hints["ignore_defaults"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "title": title,
        }
        if filter_plan is not None:
            self._values["filter_plan"] = filter_plan
        if format is not None:
            self._values["format"] = format
        if node_positions is not None:
            self._values["node_positions"] = node_positions
        if theme is not None:
            self._values["theme"] = theme
        if ignore_defaults is not None:
            self._values["ignore_defaults"] = ignore_defaults

    @builtins.property
    def filter_plan(self) -> typing.Optional[_IGraphFilterPlan_106744ef]:
        '''Graph {@link IGraphFilterPlanFilter Plan}  used to generate a unique diagram.'''
        result = self._values.get("filter_plan")
        return typing.cast(typing.Optional[_IGraphFilterPlan_106744ef], result)

    @builtins.property
    def format(
        self,
    ) -> typing.Optional[typing.Union[DiagramFormat, typing.List[DiagramFormat]]]:
        '''The output format(s) to generated.

        :default: ``DiagramFormat.PNG`` - which will through extension also generate ``DiagramFormat.SVG`` and ``DiagramFormat.DOT``
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[typing.Union[DiagramFormat, typing.List[DiagramFormat]]], result)

    @builtins.property
    def node_positions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, INodePosition]]:
        '''Config for predetermined node positions given their CDK construct id.'''
        result = self._values.get("node_positions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, INodePosition]], result)

    @builtins.property
    def theme(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IGraphThemeConfigAlt]]:
        '''Config for graph theme.'''
        result = self._values.get("theme")
        return typing.cast(typing.Optional[typing.Union[builtins.str, IGraphThemeConfigAlt]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the diagram.

        Used as the basename of the generated file(s) which gets the extension appended.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''The title of the diagram.'''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ignore_defaults(self) -> typing.Optional[builtins.bool]:
        '''Indicates if default diagram config is applied as defaults to this config.

        :default: false
        '''
        result = self._values.get("ignore_defaults")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IDiagramConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws/pdk.cdk_graph_plugin_diagram.IGraphThemeRendering")
class IGraphThemeRendering(
    IGraphThemeRenderingIconProps,
    IGraphThemeRenderingOptions,
    typing_extensions.Protocol,
):
    '''Properties for defining the rendering options for the graph theme.'''

    pass


class _IGraphThemeRenderingProxy(
    jsii.proxy_for(IGraphThemeRenderingIconProps), # type: ignore[misc]
    jsii.proxy_for(IGraphThemeRenderingOptions), # type: ignore[misc]
):
    '''Properties for defining the rendering options for the graph theme.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph_plugin_diagram.IGraphThemeRendering"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphThemeRendering).__jsii_proxy_class__ = lambda : _IGraphThemeRenderingProxy


__all__ = [
    "CdkGraphDiagramPlugin",
    "DiagramFormat",
    "DiagramOptions",
    "GraphThemeRenderingIconTarget",
    "IDiagramConfig",
    "IDiagramConfigBase",
    "IGraphThemeConfigAlt",
    "IGraphThemeRendering",
    "IGraphThemeRenderingIconProps",
    "IGraphThemeRenderingOptions",
    "INodePosition",
    "IPluginConfig",
]

publication.publish()

def _typecheckingstub__4346963f07e4e9c3b8383a218621295b8ef3268cc57838f451eb9df609af3c70(
    name: builtins.str,
    format: DiagramFormat,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30660626fed6954ad6226458572b6fed7f29b3a1846a993d63d71c4243c55632(
    name: builtins.str,
    format: DiagramFormat,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e4a1adae905752cca74bb474bf98e36ace3c448910ee031c4742a70a25445a(
    name: builtins.str,
    format: DiagramFormat,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62fd8490a6fe5c8a58c2949b1b834be775be44e10b1e0f512d048d3d48d14d4(
    value: _IGraphPluginBindCallback_58b6edd3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2478a8d6de8d0b65c7e28e6ee42176f82ac6fa77bb6a501926430454aa9ea04(
    value: typing.Optional[_IGraphReportCallback_858cc871],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3019720d8f4e085ad4bfbad17e4e6e3436b97f1a0e3718ae6413f430f4ed97a9(
    *,
    title: builtins.str,
    node_positions: typing.Optional[typing.Mapping[builtins.str, INodePosition]] = None,
    preset: typing.Optional[_FilterPreset_47315c13] = None,
    theme: typing.Optional[typing.Union[builtins.str, IGraphThemeConfigAlt]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b574db97ce884a6029ce524ba5a0bcf4120c926644bb305c271f9942a4bff53(
    *,
    filter_plan: typing.Optional[typing.Union[_IGraphFilterPlan_106744ef, typing.Dict[builtins.str, typing.Any]]] = None,
    format: typing.Optional[typing.Union[DiagramFormat, typing.Sequence[DiagramFormat]]] = None,
    node_positions: typing.Optional[typing.Mapping[builtins.str, INodePosition]] = None,
    theme: typing.Optional[typing.Union[builtins.str, IGraphThemeConfigAlt]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2adfa41ae4eaeab3ece8e56a1f97cefd4038a38e982ab24e64dae37cc45764cd(
    *,
    defaults: typing.Optional[typing.Union[IDiagramConfigBase, typing.Dict[builtins.str, typing.Any]]] = None,
    diagrams: typing.Optional[typing.Sequence[typing.Union[IDiagramConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30354dea79562b734bd6bd3e6c15fccb355105edbf147fdb0790dcca3730ddb5(
    *,
    filter_plan: typing.Optional[typing.Union[_IGraphFilterPlan_106744ef, typing.Dict[builtins.str, typing.Any]]] = None,
    format: typing.Optional[typing.Union[DiagramFormat, typing.Sequence[DiagramFormat]]] = None,
    node_positions: typing.Optional[typing.Mapping[builtins.str, INodePosition]] = None,
    theme: typing.Optional[typing.Union[builtins.str, IGraphThemeConfigAlt]] = None,
    name: builtins.str,
    title: builtins.str,
    ignore_defaults: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
