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

import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.CdkConstructIds")
class CdkConstructIds(enum.Enum):
    '''Common cdk construct ids.'''

    DEFAULT = "DEFAULT"
    RESOURCE = "RESOURCE"
    EXPORTS = "EXPORTS"


class CdkGraph(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.CdkGraph",
):
    '''CdkGraph construct is the cdk-graph framework controller that is responsible for computing the graph, storing serialized graph, and instrumenting plugins per the plugin contract.'''

    def __init__(
        self,
        root: _constructs_77d1e7e8.Construct,
        *,
        plugins: typing.Optional[typing.Sequence["ICdkGraphPlugin"]] = None,
    ) -> None:
        '''
        :param root: -
        :param plugins: List of plugins to extends the graph. Plugins are invoked at each phases in fifo order.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94bbd0d21e41f3cace54433390a25a1906e561e4eb7434f9283e50733df3fa53)
            check_type(argname="argument root", value=root, expected_type=type_hints["root"])
        props = ICdkGraphProps(plugins=plugins)

        jsii.create(self.__class__, self, [root, props])

    @jsii.member(jsii_name="report")
    def report(self) -> None:
        '''Asynchronous report generation. This operation enables running expensive and non-synchronous report generation by plugins post synthesis.

        If a given plugin requires performing asynchronous operations or is general expensive, it should
        utilize ``report`` rather than ``synthesize``.
        '''
        return typing.cast(None, jsii.ainvoke(self, "report", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ID")
    def ID(cls) -> builtins.str:
        '''Fixed CdkGraph construct id.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION")
    def VERSION(cls) -> builtins.str:
        '''Current CdkGraph semantic version.'''
        return typing.cast(builtins.str, jsii.sget(cls, "VERSION"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Config.'''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="plugins")
    def plugins(self) -> typing.List["ICdkGraphPlugin"]:
        '''List of plugins registered with this instance.'''
        return typing.cast(typing.List["ICdkGraphPlugin"], jsii.get(self, "plugins"))

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "root"))

    @builtins.property
    @jsii.member(jsii_name="graphContext")
    def graph_context(self) -> typing.Optional["CdkGraphContext"]:
        '''Get the context for the graph instance.

        This will be ``undefined`` before construct synthesis has initiated.
        '''
        return typing.cast(typing.Optional["CdkGraphContext"], jsii.get(self, "graphContext"))


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.CdkGraphArtifact",
    jsii_struct_bases=[],
    name_mapping={
        "filename": "filename",
        "filepath": "filepath",
        "id": "id",
        "source": "source",
        "description": "description",
    },
)
class CdkGraphArtifact:
    def __init__(
        self,
        *,
        filename: builtins.str,
        filepath: builtins.str,
        id: builtins.str,
        source: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''CdkGraph artifact definition.

        :param filename: Filename of the artifact.
        :param filepath: Full path where artifact is stored.
        :param id: The unique type of the artifact.
        :param source: The source of the artifact (such as plugin, or core system, etc).
        :param description: Description of artifact.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc21baecc84529dfbcbca164ba64f57611cf25ebb446fff90b877a66752278bf)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument filepath", value=filepath, expected_type=type_hints["filepath"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filename": filename,
            "filepath": filepath,
            "id": id,
            "source": source,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def filename(self) -> builtins.str:
        '''Filename of the artifact.'''
        result = self._values.get("filename")
        assert result is not None, "Required property 'filename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filepath(self) -> builtins.str:
        '''Full path where artifact is stored.'''
        result = self._values.get("filepath")
        assert result is not None, "Required property 'filepath' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique type of the artifact.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''The source of the artifact (such as plugin, or core system, etc).'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of artifact.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkGraphArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.CdkGraphArtifacts")
class CdkGraphArtifacts(enum.Enum):
    '''CdkGraph core artifacts.'''

    GRAPH_METADATA = "GRAPH_METADATA"
    GRAPH = "GRAPH"


class CdkGraphContext(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.CdkGraphContext",
):
    '''CdkGraph context.'''

    def __init__(self, store: "Store", outdir: builtins.str) -> None:
        '''
        :param store: -
        :param outdir: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97bea2b98e38f7a897ff5336a87aa3f81c8589f06c9e3fe55e541d1f9a3670bd)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
        jsii.create(self.__class__, self, [store, outdir])

    @jsii.member(jsii_name="getArtifact")
    def get_artifact(self, id: builtins.str) -> CdkGraphArtifact:
        '''Get CdkGraph artifact by id.

        :param id: -

        :throws: Error is artifact does not exist
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9953dcded2bbb491c95bca34b0f508dcfa935a755aa4814abadc8489e0543aad)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(CdkGraphArtifact, jsii.invoke(self, "getArtifact", [id]))

    @jsii.member(jsii_name="hasArtifactFile")
    def has_artifact_file(self, filename: builtins.str) -> builtins.bool:
        '''Indicates if context has an artifact with *filename* defined.

        :param filename: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54dfa2a44dec1f2462e39277d3fbab1ab5d882e5a05f20c1f1ef3c3cc6a473dd)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasArtifactFile", [filename]))

    @jsii.member(jsii_name="logArtifact")
    def log_artifact(
        self,
        source: typing.Union[CdkGraph, "ICdkGraphPlugin"],
        id: builtins.str,
        filepath: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> CdkGraphArtifact:
        '''Logs an artifact entry.

        In general this should not be called directly, as ``writeArtifact`` should be utilized
        to perform writing and logging artifacts. However some plugins utilize other tools that generate the artifacts,
        in which case the plugin would call this method to log the entry.

        :param source: The source of the artifact, such as the name of plugin.
        :param id: Unique id of the artifact.
        :param filepath: Full path where the artifact is stored.
        :param description: Description of the artifact.

        :throws: Error is artifact id or filename already exists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e89bf27595703961827418a329025c23226a17ea261d44547cda6dcf4a50535)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument filepath", value=filepath, expected_type=type_hints["filepath"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(CdkGraphArtifact, jsii.invoke(self, "logArtifact", [source, id, filepath, description]))

    @jsii.member(jsii_name="writeArtifact")
    def write_artifact(
        self,
        source: typing.Union[CdkGraph, "ICdkGraphPlugin"],
        id: builtins.str,
        filename: builtins.str,
        data: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> CdkGraphArtifact:
        '''Writes artifact data to outdir and logs the entry.

        :param source: The source of the artifact, such as the name of plugin.
        :param id: Unique id of the artifact.
        :param filename: Relative name of the file.
        :param data: -
        :param description: Description of the artifact.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c296b043fd77e0a3b1655b2edcdaf6cba3c883b46fe45ffdc32105a5939c63a)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(CdkGraphArtifact, jsii.invoke(self, "writeArtifact", [source, id, filename, data, description]))

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Mapping[builtins.str, CdkGraphArtifact]:
        '''Get record of all graph artifacts keyed by artifact id.'''
        return typing.cast(typing.Mapping[builtins.str, CdkGraphArtifact], jsii.get(self, "artifacts"))

    @builtins.property
    @jsii.member(jsii_name="graphJson")
    def graph_json(self) -> CdkGraphArtifact:
        '''Get CdkGraph core ``graph.json`` artifact.'''
        return typing.cast(CdkGraphArtifact, jsii.get(self, "graphJson"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> "Store":
        return typing.cast("Store", jsii.get(self, "store"))


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.CfnAttributesEnum")
class CfnAttributesEnum(enum.Enum):
    '''Common cfn attribute keys.'''

    TYPE = "TYPE"
    PROPS = "PROPS"


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.ConstructInfo",
    jsii_struct_bases=[],
    name_mapping={"fqn": "fqn", "version": "version"},
)
class ConstructInfo:
    def __init__(self, *, fqn: builtins.str, version: builtins.str) -> None:
        '''Source information on a construct (class fqn and version).

        :param fqn: 
        :param version: 

        :see: https://github.com/aws/aws-cdk/blob/cea1039e3664fdfa89c6f00cdaeb1a0185a12678/packages/%40aws-cdk/core/lib/private/runtime-info.ts#L22
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b6691c3201754d126a70b5463170fdaa907dfd5f96861451435fb1b66660d1)
            check_type(argname="argument fqn", value=fqn, expected_type=type_hints["fqn"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fqn": fqn,
            "version": version,
        }

    @builtins.property
    def fqn(self) -> builtins.str:
        result = self._values.get("fqn")
        assert result is not None, "Required property 'fqn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstructInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.ConstructInfoFqnEnum")
class ConstructInfoFqnEnum(enum.Enum):
    '''Commonly used cdk construct info fqn (jsii fully-qualified ids).'''

    APP = "APP"
    PDKAPP_MONO = "PDKAPP_MONO"
    PDKAPP = "PDKAPP"
    STAGE = "STAGE"
    STACK = "STACK"
    NESTED_STACK = "NESTED_STACK"
    CFN_STACK = "CFN_STACK"
    CFN_OUTPUT = "CFN_OUTPUT"
    CFN_PARAMETER = "CFN_PARAMETER"
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    AWS_CUSTOM_RESOURCE = "AWS_CUSTOM_RESOURCE"
    CUSTOM_RESOURCE_PROVIDER = "CUSTOM_RESOURCE_PROVIDER"
    CUSTOM_RESOURCE_PROVIDER_2 = "CUSTOM_RESOURCE_PROVIDER_2"
    LAMBDA = "LAMBDA"
    CFN_LAMBDA = "CFN_LAMBDA"
    LAMBDA_LAYER_VERSION = "LAMBDA_LAYER_VERSION"
    CFN_LAMBDA_LAYER_VERSION = "CFN_LAMBDA_LAYER_VERSION"
    LAMBDA_ALIAS = "LAMBDA_ALIAS"
    CFN_LAMBDA_ALIAS = "CFN_LAMBDA_ALIAS"
    LAMBDA_BASE = "LAMBDA_BASE"
    LAMBDA_SINGLETON = "LAMBDA_SINGLETON"
    LAMBDA_LAYER_AWSCLI = "LAMBDA_LAYER_AWSCLI"
    CFN_LAMBDA_PERMISSIONS = "CFN_LAMBDA_PERMISSIONS"
    ASSET_STAGING = "ASSET_STAGING"
    S3_ASSET = "S3_ASSET"
    ECR_TARBALL_ASSET = "ECR_TARBALL_ASSET"
    EC2_INSTANCE = "EC2_INSTANCE"
    CFN_EC2_INSTANCE = "CFN_EC2_INSTANCE"
    SECURITY_GROUP = "SECURITY_GROUP"
    CFN_SECURITY_GROUP = "CFN_SECURITY_GROUP"
    VPC = "VPC"
    CFN_VPC = "CFN_VPC"
    PRIVATE_SUBNET = "PRIVATE_SUBNET"
    CFN_PRIVATE_SUBNET = "CFN_PRIVATE_SUBNET"
    PUBLIC_SUBNET = "PUBLIC_SUBNET"
    CFN_PUBLIC_SUBNET = "CFN_PUBLIC_SUBNET"
    IAM_ROLE = "IAM_ROLE"


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.EdgeDirectionEnum")
class EdgeDirectionEnum(enum.Enum):
    '''EdgeDirection specifies in which direction the edge is directed or if it is undirected.'''

    NONE = "NONE"
    '''Indicates that edge is *undirected*;

    meaning there is no directional relationship between the **source** and **target**.
    '''
    FORWARD = "FORWARD"
    '''Indicates the edge is *directed* from the **source** to the **target**.'''
    BACK = "BACK"
    '''Indicates the edge is *directed* from the **target** to the **source**.'''
    BOTH = "BOTH"
    '''Indicates the edge is *bi-directional*.'''


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.EdgeTypeEnum")
class EdgeTypeEnum(enum.Enum):
    '''Edge types handles by the graph.'''

    CUSTOM = "CUSTOM"
    '''Custom edge.'''
    REFERENCE = "REFERENCE"
    '''Reference edge (Ref, Fn::GetAtt, Fn::ImportValue).'''
    DEPENDENCY = "DEPENDENCY"
    '''CloudFormation dependency edge.'''


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.FilterPreset")
class FilterPreset(enum.Enum):
    '''Filter presets.'''

    COMPACT = "COMPACT"
    '''Collapses extraneous nodes to parent and cdk created nodes on themselves, and prunes extraneous edges.

    This most closely represents the developers code for the current application
    and reduces the noise one expects.
    '''
    NON_EXTRANEOUS = "NON_EXTRANEOUS"
    '''Collapses extraneous nodes to parent and prunes extraneous edges.'''
    NONE = "NONE"
    '''No filtering is performed which will output **verbose** graph.'''


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.FilterStrategy")
class FilterStrategy(enum.Enum):
    '''Filter strategy to apply to filter matches.'''

    PRUNE = "PRUNE"
    '''Remove filtered entity and all its edges.'''
    COLLAPSE = "COLLAPSE"
    '''Collapse all child entities of filtered entity into filtered entity;

    and hoist all edges.
    '''
    COLLAPSE_TO_PARENT = "COLLAPSE_TO_PARENT"
    '''Collapse all filtered entities into their parent entity;

    and hoist its edges to parent.
    '''


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.FilterValue",
    jsii_struct_bases=[],
    name_mapping={"regex": "regex", "value": "value"},
)
class FilterValue:
    def __init__(
        self,
        *,
        regex: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Filter value to use.

        :param regex: String representation of a regex.
        :param value: Raw value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd53d6836daf3be3c9730c0e1d468bc86571ff2a7533b7b1a218193cc86eed9b)
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if regex is not None:
            self._values["regex"] = regex
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''String representation of a regex.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Raw value.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilterValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Filters(metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.cdk_graph.Filters"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="collapseCdkOwnedResources")
    @builtins.classmethod
    def collapse_cdk_owned_resources(cls) -> "IGraphStoreFilter":
        '''Collapses all Cdk Owned containers, which more closely mirrors the application code by removing resources that are automatically created by cdk.'''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "collapseCdkOwnedResources", []))

    @jsii.member(jsii_name="collapseCdkWrappers")
    @builtins.classmethod
    def collapse_cdk_wrappers(cls) -> "IGraphStoreFilter":
        '''Collapses all Cdk Resource wrappers that wrap directly wrap a CfnResource.

        Example, s3.Bucket wraps s3.CfnBucket.
        '''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "collapseCdkWrappers", []))

    @jsii.member(jsii_name="collapseCustomResources")
    @builtins.classmethod
    def collapse_custom_resources(cls) -> "IGraphStoreFilter":
        '''Collapses Custom Resource nodes to a single node.'''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "collapseCustomResources", []))

    @jsii.member(jsii_name="compact")
    @builtins.classmethod
    def compact(cls) -> "IGraphStoreFilter":
        '''Collapses extraneous nodes to parent and cdk created nodes on themselves, and prunes extraneous edges.

        This most closely represents the developers code for the current application
        and reduces the noise one expects.

        Invokes:
        1.

        1. pruneExtraneous()(store);
        2. collapseCdkOwnedResources()(store);
        3. collapseCdkWrappers()(store);
        4. collapseCustomResources()(store);
        5. ~pruneCustomResources()(store);~
        6. pruneEmptyContainers()(store);

        :destructive: true
        :throws: Error if store is not filterable
        '''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "compact", []))

    @jsii.member(jsii_name="excludeCfnType")
    @builtins.classmethod
    def exclude_cfn_type(
        cls,
        cfn_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
    ) -> "IGraphFilter":
        '''Prune all {@link Graph.ResourceNode} and {@link Graph.CfnResourceNode} nodes *matching* specified list of CloudFormation types.

        :param cfn_types: -

        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0553f4b6eecb3118ee61590f5ccf76d43efc79b646aac3f499a8687d3813ff8b)
            check_type(argname="argument cfn_types", value=cfn_types, expected_type=type_hints["cfn_types"])
        return typing.cast("IGraphFilter", jsii.sinvoke(cls, "excludeCfnType", [cfn_types]))

    @jsii.member(jsii_name="excludeNodeType")
    @builtins.classmethod
    def exclude_node_type(
        cls,
        node_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
    ) -> "IGraphStoreFilter":
        '''Prune all {@link Graph.Node}s *matching* specified list.

        This filter targets all nodes (except root) - {@link IGraphFilter.allNodes}

        :param node_types: -

        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7002b0b10ad95a3a17090521d317871cf7b8c2e6674ef7f259c9743d41dee716)
            check_type(argname="argument node_types", value=node_types, expected_type=type_hints["node_types"])
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "excludeNodeType", [node_types]))

    @jsii.member(jsii_name="includeCfnType")
    @builtins.classmethod
    def include_cfn_type(
        cls,
        cfn_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
    ) -> "IGraphFilter":
        '''Prune all {@link Graph.ResourceNode} and {@link Graph.CfnResourceNode} nodes *except those matching* specified list of CloudFormation types.

        :param cfn_types: -

        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb056cc26114d494350e156c1d3c3dafd918e6d3def382d2b8e1540faf16419)
            check_type(argname="argument cfn_types", value=cfn_types, expected_type=type_hints["cfn_types"])
        return typing.cast("IGraphFilter", jsii.sinvoke(cls, "includeCfnType", [cfn_types]))

    @jsii.member(jsii_name="includeNodeType")
    @builtins.classmethod
    def include_node_type(
        cls,
        node_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
    ) -> "IGraphStoreFilter":
        '''Prune all {@link Graph.Node}s *except those matching* specified list.

        This filter targets all nodes (except root) - {@link IGraphFilter.allNodes}

        :param node_types: -

        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e77b9617bf2aaf8aa68b370f5fd924cd9bd3487ae168eb5f47bec27f4684e4)
            check_type(argname="argument node_types", value=node_types, expected_type=type_hints["node_types"])
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "includeNodeType", [node_types]))

    @jsii.member(jsii_name="pruneCustomResources")
    @builtins.classmethod
    def prune_custom_resources(cls) -> "IGraphStoreFilter":
        '''Prune Custom Resource nodes.'''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "pruneCustomResources", []))

    @jsii.member(jsii_name="pruneEmptyContainers")
    @builtins.classmethod
    def prune_empty_containers(cls) -> "IGraphStoreFilter":
        '''Prune empty containers, which are non-resource default nodes without any children.

        Generally L3 constructs in which all children have already been pruned, which
        would be useful as containers, but without children are considered extraneous.
        '''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "pruneEmptyContainers", []))

    @jsii.member(jsii_name="pruneExtraneous")
    @builtins.classmethod
    def prune_extraneous(cls) -> "IGraphStoreFilter":
        '''Prune **extraneous** nodes and edges.

        :destructive: true
        :throws: Error if store is not filterable
        '''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "pruneExtraneous", []))

    @jsii.member(jsii_name="uncluster")
    @builtins.classmethod
    def uncluster(
        cls,
        cluster_types: typing.Optional[typing.Sequence["NodeTypeEnum"]] = None,
    ) -> "IGraphStoreFilter":
        '''Remove clusters by hoisting their children to the parent of the cluster and collapsing the cluster itself to its parent.

        :param cluster_types: -

        :see: {@link Graph.Node.mutateUncluster }
        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f059272dd0f0e79169ae1f32881cd7bcebae5f30dca3cbf15dce74f466ea12c)
            check_type(argname="argument cluster_types", value=cluster_types, expected_type=type_hints["cluster_types"])
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "uncluster", [cluster_types]))

    @jsii.member(jsii_name="verifyFilterable")
    @builtins.classmethod
    def verify_filterable(cls, store: "Store") -> None:
        '''Verify that store is filterable, meaning it allows destructive mutations.

        :param store: -

        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c377c780608bb7f3819c6d9512dc6f915256a98cb0e48b92875e39bafdd6a19)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        return typing.cast(None, jsii.sinvoke(cls, "verifyFilterable", [store]))


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.FlagEnum")
class FlagEnum(enum.Enum):
    '''Graph flags.'''

    CLUSTER = "CLUSTER"
    '''Indicates that node is a cluster (container) and treated like an emphasized subgraph.'''
    GRAPH_CONTAINER = "GRAPH_CONTAINER"
    '''Indicates that node is non-resource container (Root, App) and used for structural purpose in the graph only.'''
    EXTRANEOUS = "EXTRANEOUS"
    '''Indicates that the entity is extraneous and considered collapsible to parent without impact of intent.'''
    ASSET = "ASSET"
    '''Indicates node is considered a CDK Asset (Lambda Code, Docker Image, etc).'''
    CDK_OWNED = "CDK_OWNED"
    '''Indicates that node was created by CDK.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Resource.html#static-iswbrownedwbrresourceconstruct
    '''
    CFN_FQN = "CFN_FQN"
    '''Indicates node ConstructInfoFqn denotes a ``aws-cdk-lib.*.Cfn*`` construct.'''
    CLOSED_EDGE = "CLOSED_EDGE"
    '''Indicates that edge is closed;

    meaning ``source === target``. This flag only gets applied on creation of edge, not during mutations to maintain initial intent.
    '''
    MUTATED = "MUTATED"
    '''Indicates that entity was mutated;

    meaning a mutation was performed to change originally computed graph value.
    '''
    IMPORT = "IMPORT"
    '''Indicates that resource is imported into CDK (eg: ``lambda.Function.fromFunctionName()``, ``s3.Bucket.fromBucketArn()``).'''
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    '''Indicates if node is a CustomResource.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html
    '''
    AWS_CUSTOM_RESOURCE = "AWS_CUSTOM_RESOURCE"
    '''Indicates if node is an AwsCustomResource, which is a custom resource that simply calls the AWS SDK API via singleton provider.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsCustomResource.html
    '''
    AWS_API_CALL_LAMBDA = "AWS_API_CALL_LAMBDA"
    '''Indicates if lambda function resource is a singleton AWS API call lambda for AwsCustomResources.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsCustomResource.html
    '''


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IBaseEntityDataProps")
class IBaseEntityDataProps(typing_extensions.Protocol):
    '''Base interface for all store entities **data** props.'''

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject", typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject"]]]]]:
        '''Attributes.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Flags.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Metadata entries.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags.'''
        ...


class _IBaseEntityDataPropsProxy:
    '''Base interface for all store entities **data** props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IBaseEntityDataProps"

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject", typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject"]]]]]:
        '''Attributes.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject", typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject"]]]]], jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Flags.'''
        return typing.cast(typing.Optional[typing.List[FlagEnum]], jsii.get(self, "flags"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Metadata entries.'''
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBaseEntityDataProps).__jsii_proxy_class__ = lambda : _IBaseEntityDataPropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IBaseEntityProps")
class IBaseEntityProps(IBaseEntityDataProps, typing_extensions.Protocol):
    '''Base interface for all store entities props.'''

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> "Store":
        '''Store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        '''UUID.'''
        ...


class _IBaseEntityPropsProxy(
    jsii.proxy_for(IBaseEntityDataProps), # type: ignore[misc]
):
    '''Base interface for all store entities props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IBaseEntityProps"

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> "Store":
        '''Store.'''
        return typing.cast("Store", jsii.get(self, "store"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        '''UUID.'''
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBaseEntityProps).__jsii_proxy_class__ = lambda : _IBaseEntityPropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.ICdkGraphPlugin")
class ICdkGraphPlugin(typing_extensions.Protocol):
    '''CdkGraph **Plugin** interface.'''

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for this plugin.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''Plugin version.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="bind")
    def bind(self) -> "IGraphPluginBindCallback":
        '''Binds the plugin to the CdkGraph instance.

        Enables plugins to receive base configs.
        '''
        ...

    @bind.setter
    def bind(self, value: "IGraphPluginBindCallback") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inspect")
    def inspect(self) -> typing.Optional["IGraphVisitorCallback"]:
        '''Node visitor callback for construct tree traversal.

        This follows IAspect.visit pattern, but the order
        of visitor traversal in managed by the CdkGraph.
        '''
        ...

    @inspect.setter
    def inspect(self, value: typing.Optional["IGraphVisitorCallback"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="report")
    def report(self) -> typing.Optional["IGraphReportCallback"]:
        '''Generate asynchronous reports based on the graph.

        This is not automatically called when synthesizing CDK.
        Developer must explicitly add ``await graphInstance.report()`` to the CDK bin or invoke this outside
        of the CDK synth. In either case, the plugin receives the in-memory graph interface when invoked, as the
        CdkGraph will deserialize the graph prior to invoking the plugin report.
        '''
        ...

    @report.setter
    def report(self, value: typing.Optional["IGraphReportCallback"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> typing.Optional["IGraphSynthesizeCallback"]:
        '''Called during CDK synthesize to generate synchronous artifacts based on the in-memory graph passed to the plugin.

        This is called in fifo order of plugins.
        '''
        ...

    @synthesize.setter
    def synthesize(self, value: typing.Optional["IGraphSynthesizeCallback"]) -> None:
        ...


class _ICdkGraphPluginProxy:
    '''CdkGraph **Plugin** interface.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.ICdkGraphPlugin"

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for this plugin.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''Plugin version.'''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]).'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="bind")
    def bind(self) -> "IGraphPluginBindCallback":
        '''Binds the plugin to the CdkGraph instance.

        Enables plugins to receive base configs.
        '''
        return typing.cast("IGraphPluginBindCallback", jsii.get(self, "bind"))

    @bind.setter
    def bind(self, value: "IGraphPluginBindCallback") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6754d39affa07fc839bab41660ae78c4853110297d33b48e2ca93e44055003c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspect")
    def inspect(self) -> typing.Optional["IGraphVisitorCallback"]:
        '''Node visitor callback for construct tree traversal.

        This follows IAspect.visit pattern, but the order
        of visitor traversal in managed by the CdkGraph.
        '''
        return typing.cast(typing.Optional["IGraphVisitorCallback"], jsii.get(self, "inspect"))

    @inspect.setter
    def inspect(self, value: typing.Optional["IGraphVisitorCallback"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66990c34d4964902327a0f145d5058d1303c7f1fc82cd74214c85867aaf5a010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="report")
    def report(self) -> typing.Optional["IGraphReportCallback"]:
        '''Generate asynchronous reports based on the graph.

        This is not automatically called when synthesizing CDK.
        Developer must explicitly add ``await graphInstance.report()`` to the CDK bin or invoke this outside
        of the CDK synth. In either case, the plugin receives the in-memory graph interface when invoked, as the
        CdkGraph will deserialize the graph prior to invoking the plugin report.
        '''
        return typing.cast(typing.Optional["IGraphReportCallback"], jsii.get(self, "report"))

    @report.setter
    def report(self, value: typing.Optional["IGraphReportCallback"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65033b5ace6f019d80b4c2eff14e6a6858258160ac2ab689bf40f674dc7bb150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "report", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> typing.Optional["IGraphSynthesizeCallback"]:
        '''Called during CDK synthesize to generate synchronous artifacts based on the in-memory graph passed to the plugin.

        This is called in fifo order of plugins.
        '''
        return typing.cast(typing.Optional["IGraphSynthesizeCallback"], jsii.get(self, "synthesize"))

    @synthesize.setter
    def synthesize(self, value: typing.Optional["IGraphSynthesizeCallback"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471f0d2243469429351b860306f51981d6ef04540bf0038199d0c7e113d31971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synthesize", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICdkGraphPlugin).__jsii_proxy_class__ = lambda : _ICdkGraphPluginProxy


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.ICdkGraphProps",
    jsii_struct_bases=[],
    name_mapping={"plugins": "plugins"},
)
class ICdkGraphProps:
    def __init__(
        self,
        *,
        plugins: typing.Optional[typing.Sequence[ICdkGraphPlugin]] = None,
    ) -> None:
        '''{@link CdkGraph} props.

        :param plugins: List of plugins to extends the graph. Plugins are invoked at each phases in fifo order.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e23c07244128808dcb67636858a881d33e9bb5cc2bc40fe660715ca7f043f6)
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if plugins is not None:
            self._values["plugins"] = plugins

    @builtins.property
    def plugins(self) -> typing.Optional[typing.List[ICdkGraphPlugin]]:
        '''List of plugins to extends the graph.

        Plugins are invoked at each phases in fifo order.
        '''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.List[ICdkGraphPlugin]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ICdkGraphProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IEdgePredicate")
class IEdgePredicate(typing_extensions.Protocol):
    '''Predicate to match edge.'''

    @jsii.member(jsii_name="filter")
    def filter(self, edge: "Edge") -> builtins.bool:
        '''
        :param edge: -
        '''
        ...


class _IEdgePredicateProxy:
    '''Predicate to match edge.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IEdgePredicate"

    @jsii.member(jsii_name="filter")
    def filter(self, edge: "Edge") -> builtins.bool:
        '''
        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b475e9f95e493d62540af568e2b2b73449d41daf4cb307704df1b1f76b18347f)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.invoke(self, "filter", [edge]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEdgePredicate).__jsii_proxy_class__ = lambda : _IEdgePredicateProxy


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.IFilter",
    jsii_struct_bases=[],
    name_mapping={"graph": "graph", "store": "store"},
)
class IFilter:
    def __init__(
        self,
        *,
        graph: typing.Optional[typing.Union["IGraphFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        store: typing.Optional["IGraphStoreFilter"] = None,
    ) -> None:
        '''A filter than can be applied to the graph.

        :param graph: Graph Filter.
        :param store: Store Filter.
        '''
        if isinstance(graph, dict):
            graph = IGraphFilter(**graph)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bafc31b18e2f14337cdcfdad4cb53e7e09fd03f4dcf1a0b37bab9058bdbd0d9b)
            check_type(argname="argument graph", value=graph, expected_type=type_hints["graph"])
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if graph is not None:
            self._values["graph"] = graph
        if store is not None:
            self._values["store"] = store

    @builtins.property
    def graph(self) -> typing.Optional["IGraphFilter"]:
        '''Graph Filter.'''
        result = self._values.get("graph")
        return typing.cast(typing.Optional["IGraphFilter"], result)

    @builtins.property
    def store(self) -> typing.Optional["IGraphStoreFilter"]:
        '''Store Filter.'''
        result = self._values.get("store")
        return typing.cast(typing.Optional["IGraphStoreFilter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IFilterFocusCallback")
class IFilterFocusCallback(typing_extensions.Protocol):
    '''Determines focus node of filter plan.'''

    @jsii.member(jsii_name="filter")
    def filter(self, store: "Store") -> "Node":
        '''
        :param store: -
        '''
        ...


class _IFilterFocusCallbackProxy:
    '''Determines focus node of filter plan.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IFilterFocusCallback"

    @jsii.member(jsii_name="filter")
    def filter(self, store: "Store") -> "Node":
        '''
        :param store: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e19f3644e37f7bee1a25e7fe7b884d11cc83b52213d72556b8c9216f8c5a117)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        return typing.cast("Node", jsii.invoke(self, "filter", [store]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFilterFocusCallback).__jsii_proxy_class__ = lambda : _IFilterFocusCallbackProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IFindEdgeOptions")
class IFindEdgeOptions(typing_extensions.Protocol):
    '''Options for edge based search operations.'''

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order of traversal during search path.'''
        ...

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional[IEdgePredicate]:
        '''The predicate to match edges(s).'''
        ...

    @predicate.setter
    def predicate(self, value: typing.Optional[IEdgePredicate]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="reverse")
    def reverse(self) -> typing.Optional[builtins.bool]:
        '''Indicates reverse order.'''
        ...

    @reverse.setter
    def reverse(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IFindEdgeOptionsProxy:
    '''Options for edge based search operations.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IFindEdgeOptions"

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order of traversal during search path.'''
        return typing.cast(typing.Optional[_constructs_77d1e7e8.ConstructOrder], jsii.get(self, "order"))

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2680bfc6423ea330cc468ae99519e650842fbc9c9ef26efed33deac72772cd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional[IEdgePredicate]:
        '''The predicate to match edges(s).'''
        return typing.cast(typing.Optional[IEdgePredicate], jsii.get(self, "predicate"))

    @predicate.setter
    def predicate(self, value: typing.Optional[IEdgePredicate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a6cf9f569b7f84aa0163c4214fedf0650fc58c17dd5a2ca3a29fd1d979db56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predicate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reverse")
    def reverse(self) -> typing.Optional[builtins.bool]:
        '''Indicates reverse order.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "reverse"))

    @reverse.setter
    def reverse(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c85a4b6a6cabb74b3c89edb5399297e514c45120fa25848232c1701ca19efd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reverse", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFindEdgeOptions).__jsii_proxy_class__ = lambda : _IFindEdgeOptionsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IFindNodeOptions")
class IFindNodeOptions(typing_extensions.Protocol):
    '''Options for node based search operations.'''

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order of traversal during search path.'''
        ...

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional["INodePredicate"]:
        '''The predicate to match node(s).'''
        ...

    @predicate.setter
    def predicate(self, value: typing.Optional["INodePredicate"]) -> None:
        ...


class _IFindNodeOptionsProxy:
    '''Options for node based search operations.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IFindNodeOptions"

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order of traversal during search path.'''
        return typing.cast(typing.Optional[_constructs_77d1e7e8.ConstructOrder], jsii.get(self, "order"))

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b984008ef441cf0392bfe783a92a0c278d00c0bed3b65dff65e6c69e3b09eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional["INodePredicate"]:
        '''The predicate to match node(s).'''
        return typing.cast(typing.Optional["INodePredicate"], jsii.get(self, "predicate"))

    @predicate.setter
    def predicate(self, value: typing.Optional["INodePredicate"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a28d466574c532332875bae1dfc756917c68254d8da881e9baad25d4fad7a4b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predicate", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFindNodeOptions).__jsii_proxy_class__ = lambda : _IFindNodeOptionsProxy


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.IGraphFilter",
    jsii_struct_bases=[],
    name_mapping={
        "all_nodes": "allNodes",
        "edge": "edge",
        "inverse": "inverse",
        "node": "node",
        "strategy": "strategy",
    },
)
class IGraphFilter:
    def __init__(
        self,
        *,
        all_nodes: typing.Optional[builtins.bool] = None,
        edge: typing.Optional[IEdgePredicate] = None,
        inverse: typing.Optional[builtins.bool] = None,
        node: typing.Optional["INodePredicate"] = None,
        strategy: typing.Optional[FilterStrategy] = None,
    ) -> None:
        '''Graph filter.

        :param all_nodes: Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes. By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well. In general, most users intent is to operate against resources and desire to preserve structural groupings, which is common in most Cfn/Cdk based filtering where inputs are "include" lists. Defaults to value of containing {@link IGraphFilterPlan.allNodes}
        :param edge: Predicate to match edges. Edges are evaluated after nodes are filtered.
        :param inverse: Indicates that matches will be filtered, as opposed to non-matches. The default follows common `Javascript Array.filter <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter>`_ precedence of preserving matches during filtering, while pruning non-matches. Default: false - Preserve matches, and filter out non-matches.
        :param node: Predicate to match nodes.
        :param strategy: Filter strategy to apply to matching nodes. Edges do not have a strategy, they are always pruned. Default: {FilterStrategy.PRUNE}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3caecaae2e9c8f32f3cf904d6949c9d2860cf03a21f2926251bf6205f6828e66)
            check_type(argname="argument all_nodes", value=all_nodes, expected_type=type_hints["all_nodes"])
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
            check_type(argname="argument inverse", value=inverse, expected_type=type_hints["inverse"])
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_nodes is not None:
            self._values["all_nodes"] = all_nodes
        if edge is not None:
            self._values["edge"] = edge
        if inverse is not None:
            self._values["inverse"] = inverse
        if node is not None:
            self._values["node"] = node
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def all_nodes(self) -> typing.Optional[builtins.bool]:
        '''Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes.

        By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well.
        In general, most users intent is to operate against resources and desire to preserve structural groupings,
        which is common in most Cfn/Cdk based filtering where inputs are "include" lists.

        Defaults to value of containing {@link IGraphFilterPlan.allNodes}
        '''
        result = self._values.get("all_nodes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edge(self) -> typing.Optional[IEdgePredicate]:
        '''Predicate to match edges.

        Edges are evaluated after nodes are filtered.
        '''
        result = self._values.get("edge")
        return typing.cast(typing.Optional[IEdgePredicate], result)

    @builtins.property
    def inverse(self) -> typing.Optional[builtins.bool]:
        '''Indicates that matches will be filtered, as opposed to non-matches.

        The default follows common `Javascript Array.filter <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter>`_
        precedence of preserving matches during filtering, while pruning non-matches.

        :default: false - Preserve matches, and filter out non-matches.
        '''
        result = self._values.get("inverse")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node(self) -> typing.Optional["INodePredicate"]:
        '''Predicate to match nodes.'''
        result = self._values.get("node")
        return typing.cast(typing.Optional["INodePredicate"], result)

    @builtins.property
    def strategy(self) -> typing.Optional[FilterStrategy]:
        '''Filter strategy to apply to matching nodes.

        Edges do not have a strategy, they are always pruned.

        :default: {FilterStrategy.PRUNE}
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[FilterStrategy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IGraphFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.IGraphFilterPlan",
    jsii_struct_bases=[],
    name_mapping={
        "all_nodes": "allNodes",
        "filters": "filters",
        "focus": "focus",
        "order": "order",
        "preset": "preset",
    },
)
class IGraphFilterPlan:
    def __init__(
        self,
        *,
        all_nodes: typing.Optional[builtins.bool] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[IFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        focus: typing.Optional[typing.Union["IGraphFilterPlanFocusConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        order: typing.Optional[_constructs_77d1e7e8.ConstructOrder] = None,
        preset: typing.Optional[FilterPreset] = None,
    ) -> None:
        '''Graph filter plan.

        :param all_nodes: Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes. By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well. In general, most users intent is to operate against resources and desire to preserve structural groupings, which is common in most Cfn/Cdk based filtering where inputs are "include" lists. Default: false By default only Resource and CfnResource nodes are filtered.
        :param filters: Ordered list of {@link IGraphFilter} and {@link IGraphStoreFilter} filters to apply to the store. - Filters are applied *after* the preset filtering is applied if present. - Filters are applied sequentially against all nodes, as opposed to IAspect.visitor pattern which are sequentially applied per node.
        :param focus: Config to focus the graph on specific node.
        :param order: The order to visit nodes and edges during filtering. Default: {ConstructOrder.PREORDER}
        :param preset: Optional preset filter to apply before other filters.
        '''
        if isinstance(focus, dict):
            focus = IGraphFilterPlanFocusConfig(**focus)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20a0c44dfd25acb2f1bb600625504fa235bfd399bc43f627258f06d5673ffd6)
            check_type(argname="argument all_nodes", value=all_nodes, expected_type=type_hints["all_nodes"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument focus", value=focus, expected_type=type_hints["focus"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_nodes is not None:
            self._values["all_nodes"] = all_nodes
        if filters is not None:
            self._values["filters"] = filters
        if focus is not None:
            self._values["focus"] = focus
        if order is not None:
            self._values["order"] = order
        if preset is not None:
            self._values["preset"] = preset

    @builtins.property
    def all_nodes(self) -> typing.Optional[builtins.bool]:
        '''Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes.

        By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well.
        In general, most users intent is to operate against resources and desire to preserve structural groupings,
        which is common in most Cfn/Cdk based filtering where inputs are "include" lists.

        :default: false By default only Resource and CfnResource nodes are filtered.
        '''
        result = self._values.get("all_nodes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[IFilter]]:
        '''Ordered list of {@link IGraphFilter} and {@link IGraphStoreFilter} filters to apply to the store.

        - Filters are applied *after* the preset filtering is applied if present.
        - Filters are applied sequentially against all nodes, as opposed to IAspect.visitor pattern
          which are sequentially applied per node.
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[IFilter]], result)

    @builtins.property
    def focus(self) -> typing.Optional["IGraphFilterPlanFocusConfig"]:
        '''Config to focus the graph on specific node.'''
        result = self._values.get("focus")
        return typing.cast(typing.Optional["IGraphFilterPlanFocusConfig"], result)

    @builtins.property
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order to visit nodes and edges during filtering.

        :default: {ConstructOrder.PREORDER}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[_constructs_77d1e7e8.ConstructOrder], result)

    @builtins.property
    def preset(self) -> typing.Optional[FilterPreset]:
        '''Optional preset filter to apply before other filters.'''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[FilterPreset], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IGraphFilterPlan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.IGraphFilterPlanFocusConfig",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter", "no_hoist": "noHoist"},
)
class IGraphFilterPlanFocusConfig:
    def __init__(
        self,
        *,
        filter: IFilterFocusCallback,
        no_hoist: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param filter: The node or resolver to determine the node to focus on.
        :param no_hoist: Indicates if ancestral containers are preserved (eg: Stages, Stack). If ``false``, the "focused node" will be hoisted to the graph root and all ancestors will be pruned. If ``true``, the "focused" will be left in-place, while all siblings and non-scope ancestors will be pruned. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c849737186526425fae15475d82f60020493fc7708cf91f9ce7ebd99ef1dbef5)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument no_hoist", value=no_hoist, expected_type=type_hints["no_hoist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
        }
        if no_hoist is not None:
            self._values["no_hoist"] = no_hoist

    @builtins.property
    def filter(self) -> IFilterFocusCallback:
        '''The node or resolver to determine the node to focus on.'''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(IFilterFocusCallback, result)

    @builtins.property
    def no_hoist(self) -> typing.Optional[builtins.bool]:
        '''Indicates if ancestral containers are preserved (eg: Stages, Stack).

        If ``false``, the "focused node" will be hoisted to the graph root and all ancestors will be pruned.
        If ``true``, the "focused" will be left in-place, while all siblings and non-scope ancestors will be pruned.

        :default: true
        '''
        result = self._values.get("no_hoist")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IGraphFilterPlanFocusConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IGraphPluginBindCallback")
class IGraphPluginBindCallback(typing_extensions.Protocol):
    '''Callback signature for graph ``Plugin.bind`` operation.'''

    pass


class _IGraphPluginBindCallbackProxy:
    '''Callback signature for graph ``Plugin.bind`` operation.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IGraphPluginBindCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphPluginBindCallback).__jsii_proxy_class__ = lambda : _IGraphPluginBindCallbackProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IGraphReportCallback")
class IGraphReportCallback(typing_extensions.Protocol):
    '''Callback signature for graph ``Plugin.report`` operation.'''

    pass


class _IGraphReportCallbackProxy:
    '''Callback signature for graph ``Plugin.report`` operation.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IGraphReportCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphReportCallback).__jsii_proxy_class__ = lambda : _IGraphReportCallbackProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IGraphStoreFilter")
class IGraphStoreFilter(typing_extensions.Protocol):
    '''Store filter callback interface used to perform filtering operations directly against the store, as opposed to using {@link IGraphFilter} definitions.'''

    @jsii.member(jsii_name="filter")
    def filter(self, store: "Store") -> None:
        '''
        :param store: -
        '''
        ...


class _IGraphStoreFilterProxy:
    '''Store filter callback interface used to perform filtering operations directly against the store, as opposed to using {@link IGraphFilter} definitions.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IGraphStoreFilter"

    @jsii.member(jsii_name="filter")
    def filter(self, store: "Store") -> None:
        '''
        :param store: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62d46db6e5a4ac2fe96fbe74b8356df6dec151c554b917749694744c78376ee)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        return typing.cast(None, jsii.invoke(self, "filter", [store]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphStoreFilter).__jsii_proxy_class__ = lambda : _IGraphStoreFilterProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IGraphSynthesizeCallback")
class IGraphSynthesizeCallback(typing_extensions.Protocol):
    '''Callback signature for graph ``Plugin.synthesize`` operation.'''

    pass


class _IGraphSynthesizeCallbackProxy:
    '''Callback signature for graph ``Plugin.synthesize`` operation.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IGraphSynthesizeCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphSynthesizeCallback).__jsii_proxy_class__ = lambda : _IGraphSynthesizeCallbackProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IGraphVisitorCallback")
class IGraphVisitorCallback(typing_extensions.Protocol):
    '''Callback signature for graph ``Plugin.inspect`` operation.'''

    pass


class _IGraphVisitorCallbackProxy:
    '''Callback signature for graph ``Plugin.inspect`` operation.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IGraphVisitorCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphVisitorCallback).__jsii_proxy_class__ = lambda : _IGraphVisitorCallbackProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.INodePredicate")
class INodePredicate(typing_extensions.Protocol):
    '''Predicate to match node.'''

    @jsii.member(jsii_name="filter")
    def filter(self, node: "Node") -> builtins.bool:
        '''
        :param node: -
        '''
        ...


class _INodePredicateProxy:
    '''Predicate to match node.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.INodePredicate"

    @jsii.member(jsii_name="filter")
    def filter(self, node: "Node") -> builtins.bool:
        '''
        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534e1a47a1685555f3e9115b1d5894e1ed342064598ac6c56dfff7ce4ce86288)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "filter", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodePredicate).__jsii_proxy_class__ = lambda : _INodePredicateProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.ISerializableEdge")
class ISerializableEdge(typing_extensions.Protocol):
    '''Interface for serializable graph edge entity.'''

    pass


class _ISerializableEdgeProxy:
    '''Interface for serializable graph edge entity.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.ISerializableEdge"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableEdge).__jsii_proxy_class__ = lambda : _ISerializableEdgeProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.ISerializableEntity")
class ISerializableEntity(typing_extensions.Protocol):
    '''Interface for serializable graph entities.'''

    pass


class _ISerializableEntityProxy:
    '''Interface for serializable graph entities.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.ISerializableEntity"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableEntity).__jsii_proxy_class__ = lambda : _ISerializableEntityProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.ISerializableGraphStore")
class ISerializableGraphStore(typing_extensions.Protocol):
    '''Interface for serializable graph store.'''

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> "SGGraphStore":
        ...


class _ISerializableGraphStoreProxy:
    '''Interface for serializable graph store.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.ISerializableGraphStore"

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> "SGGraphStore":
        return typing.cast("SGGraphStore", jsii.invoke(self, "serialize", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableGraphStore).__jsii_proxy_class__ = lambda : _ISerializableGraphStoreProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.ISerializableNode")
class ISerializableNode(typing_extensions.Protocol):
    '''Interface for serializable graph node entity.'''

    pass


class _ISerializableNodeProxy:
    '''Interface for serializable graph node entity.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.ISerializableNode"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableNode).__jsii_proxy_class__ = lambda : _ISerializableNodeProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IStoreCounts")
class IStoreCounts(typing_extensions.Protocol):
    '''Interface for store counts.'''

    @builtins.property
    @jsii.member(jsii_name="cfnResources")
    def cfn_resources(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *cfnResourceType*.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="edges")
    def edges(self) -> jsii.Number:
        '''Counts total number of edges in the store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="edgeTypes")
    def edge_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *edge type* ({@link EdgeTypeEnum}).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> jsii.Number:
        '''Counts total number of nodes in the store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeTypes")
    def node_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *node type* ({@link NodeTypeEnum}).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> jsii.Number:
        '''Counts total number of stacks in the store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> jsii.Number:
        '''Counts total number of stages in the store.'''
        ...


class _IStoreCountsProxy:
    '''Interface for store counts.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IStoreCounts"

    @builtins.property
    @jsii.member(jsii_name="cfnResources")
    def cfn_resources(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *cfnResourceType*.'''
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "cfnResources"))

    @builtins.property
    @jsii.member(jsii_name="edges")
    def edges(self) -> jsii.Number:
        '''Counts total number of edges in the store.'''
        return typing.cast(jsii.Number, jsii.get(self, "edges"))

    @builtins.property
    @jsii.member(jsii_name="edgeTypes")
    def edge_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *edge type* ({@link EdgeTypeEnum}).'''
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "edgeTypes"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> jsii.Number:
        '''Counts total number of nodes in the store.'''
        return typing.cast(jsii.Number, jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypes")
    def node_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *node type* ({@link NodeTypeEnum}).'''
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "nodeTypes"))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> jsii.Number:
        '''Counts total number of stacks in the store.'''
        return typing.cast(jsii.Number, jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> jsii.Number:
        '''Counts total number of stages in the store.'''
        return typing.cast(jsii.Number, jsii.get(self, "stages"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStoreCounts).__jsii_proxy_class__ = lambda : _IStoreCountsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.ITypedEdgeProps")
class ITypedEdgeProps(IBaseEntityProps, typing_extensions.Protocol):
    '''Base edge props agnostic to edge type.

    Used for extending per edge class with type specifics.
    '''

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Node":
        '''Edge **source** is the node that defines the edge (tail).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Node":
        '''Edge **target** is the node being referenced by the **source** (head).'''
        ...


class _ITypedEdgePropsProxy(
    jsii.proxy_for(IBaseEntityProps), # type: ignore[misc]
):
    '''Base edge props agnostic to edge type.

    Used for extending per edge class with type specifics.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.ITypedEdgeProps"

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Node":
        '''Edge **source** is the node that defines the edge (tail).'''
        return typing.cast("Node", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Node":
        '''Edge **target** is the node being referenced by the **source** (head).'''
        return typing.cast("Node", jsii.get(self, "target"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITypedEdgeProps).__jsii_proxy_class__ = lambda : _ITypedEdgePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.ITypedNodeProps")
class ITypedNodeProps(IBaseEntityProps, typing_extensions.Protocol):
    '''Base node props agnostic to node type.

    Used for extending per node class with type specifics.
    '''

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Node id, which is unique within parent scope.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''Path of the node.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Type of CloudFormation resource.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional["StackNode"]:
        '''Stack the node is contained.'''
        ...


class _ITypedNodePropsProxy(
    jsii.proxy_for(IBaseEntityProps), # type: ignore[misc]
):
    '''Base node props agnostic to node type.

    Used for extending per node class with type specifics.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.ITypedNodeProps"

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Node id, which is unique within parent scope.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''Path of the node.'''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Type of CloudFormation resource.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        return typing.cast(typing.Optional[ConstructInfo], jsii.get(self, "constructInfo"))

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalId"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.'''
        return typing.cast(typing.Optional["Node"], jsii.get(self, "parent"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional["StackNode"]:
        '''Stack the node is contained.'''
        return typing.cast(typing.Optional["StackNode"], jsii.get(self, "stack"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITypedNodeProps).__jsii_proxy_class__ = lambda : _ITypedNodePropsProxy


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.MetadataTypeEnum")
class MetadataTypeEnum(enum.Enum):
    '''Common cdk metadata types.'''

    LOGICAL_ID = "LOGICAL_ID"


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.NodeTypeEnum")
class NodeTypeEnum(enum.Enum):
    '''Node types handled by the graph.'''

    DEFAULT = "DEFAULT"
    '''Default node type - used for all nodes that don't have explicit type defined.'''
    CFN_RESOURCE = "CFN_RESOURCE"
    '''L1 cfn resource node.'''
    RESOURCE = "RESOURCE"
    '''L2 cdk resource node.'''
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    '''Cdk customer resource node.'''
    ROOT = "ROOT"
    '''Graph root node.'''
    APP = "APP"
    '''Cdk App node.'''
    STAGE = "STAGE"
    '''Cdk Stage node.'''
    STACK = "STACK"
    '''Cdk Stack node.'''
    NESTED_STACK = "NESTED_STACK"
    '''Cdk NestedStack node.'''
    OUTPUT = "OUTPUT"
    '''CfnOutput node.'''
    PARAMETER = "PARAMETER"
    '''CfnParameter node.'''
    ASSET = "ASSET"
    '''Cdk asset node.'''


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.PlainObject",
    jsii_struct_bases=[],
    name_mapping={},
)
class PlainObject:
    def __init__(self) -> None:
        '''Serializable plain object value (JSII supported).'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlainObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws/pdk.cdk_graph.ReferenceTypeEnum")
class ReferenceTypeEnum(enum.Enum):
    '''Reference edge types.'''

    REF = "REF"
    '''CloudFormation **Ref** reference.'''
    ATTRIBUTE = "ATTRIBUTE"
    '''CloudFormation **Fn::GetAtt** reference.'''
    IMPORT = "IMPORT"
    '''CloudFormation **Fn::ImportValue** reference.'''
    IMPORT_ARN = "IMPORT_ARN"
    '''CloudFormation **Fn::Join** reference of imported resourced (eg: ``s3.Bucket.fromBucketArn()``).'''


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.SGEntity",
    jsii_struct_bases=[],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
    },
)
class SGEntity:
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Serializable graph entity.

        :param uuid: Universally unique identity.
        :param attributes: Serializable entity attributes.
        :param flags: Serializable entity flags.
        :param metadata: Serializable entity metadata.
        :param tags: Serializable entity tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57d42c921f696a1e699387c3bc6a85c96a3961090be642e132494056271895e)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def uuid(self) -> builtins.str:
        '''Universally unique identity.'''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''Serializable entity attributes.

        :see: {@link Attributes }
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Serializable entity flags.

        :see: {@link FlagEnum }
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Serializable entity metadata.

        :see: {@link Metadata }
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Serializable entity tags.

        :see: {@link Tags }
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGEntity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.SGGraphStore",
    jsii_struct_bases=[],
    name_mapping={"edges": "edges", "tree": "tree", "version": "version"},
)
class SGGraphStore:
    def __init__(
        self,
        *,
        edges: typing.Sequence[typing.Union["SGEdge", typing.Dict[builtins.str, typing.Any]]],
        tree: typing.Union["SGNode", typing.Dict[builtins.str, typing.Any]],
        version: builtins.str,
    ) -> None:
        '''Serializable graph store.

        :param edges: List of edges.
        :param tree: Node tree.
        :param version: Store version.
        '''
        if isinstance(tree, dict):
            tree = SGNode(**tree)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d73d18b936d180fe819e73e1051d2d3303b710ec5b7bb170fb8c5cc71b9b25)
            check_type(argname="argument edges", value=edges, expected_type=type_hints["edges"])
            check_type(argname="argument tree", value=tree, expected_type=type_hints["tree"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edges": edges,
            "tree": tree,
            "version": version,
        }

    @builtins.property
    def edges(self) -> typing.List["SGEdge"]:
        '''List of edges.'''
        result = self._values.get("edges")
        assert result is not None, "Required property 'edges' is missing"
        return typing.cast(typing.List["SGEdge"], result)

    @builtins.property
    def tree(self) -> "SGNode":
        '''Node tree.'''
        result = self._values.get("tree")
        assert result is not None, "Required property 'tree' is missing"
        return typing.cast("SGNode", result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Store version.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGGraphStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.SGNode",
    jsii_struct_bases=[SGEntity],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
        "id": "id",
        "node_type": "nodeType",
        "path": "path",
        "cfn_type": "cfnType",
        "children": "children",
        "construct_info": "constructInfo",
        "edges": "edges",
        "logical_id": "logicalId",
        "parent": "parent",
        "stack": "stack",
    },
)
class SGNode(SGEntity):
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: builtins.str,
        node_type: NodeTypeEnum,
        path: builtins.str,
        cfn_type: typing.Optional[builtins.str] = None,
        children: typing.Optional[typing.Mapping[builtins.str, typing.Union["SGNode", typing.Dict[builtins.str, typing.Any]]]] = None,
        construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        edges: typing.Optional[typing.Sequence[builtins.str]] = None,
        logical_id: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        stack: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Serializable graph node entity.

        :param uuid: Universally unique identity.
        :param attributes: Serializable entity attributes.
        :param flags: Serializable entity flags.
        :param metadata: Serializable entity metadata.
        :param tags: Serializable entity tags.
        :param id: Node id within parent (unique only between parent child nodes).
        :param node_type: Node type.
        :param path: Node path.
        :param cfn_type: CloudFormation resource type for this node.
        :param children: Child node record.
        :param construct_info: Synthesized construct information defining jii resolution data.
        :param edges: List of edge UUIDs where this node is the **source**.
        :param logical_id: Logical id of the node, which is only unique within containing stack.
        :param parent: UUID of node parent.
        :param stack: UUID of node stack.
        '''
        if isinstance(construct_info, dict):
            construct_info = ConstructInfo(**construct_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4213b110238dd63624e961e064c18e94c85cd54fbb39ce98592eeec8be6ecfc8)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument cfn_type", value=cfn_type, expected_type=type_hints["cfn_type"])
            check_type(argname="argument children", value=children, expected_type=type_hints["children"])
            check_type(argname="argument construct_info", value=construct_info, expected_type=type_hints["construct_info"])
            check_type(argname="argument edges", value=edges, expected_type=type_hints["edges"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
            "id": id,
            "node_type": node_type,
            "path": path,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags
        if cfn_type is not None:
            self._values["cfn_type"] = cfn_type
        if children is not None:
            self._values["children"] = children
        if construct_info is not None:
            self._values["construct_info"] = construct_info
        if edges is not None:
            self._values["edges"] = edges
        if logical_id is not None:
            self._values["logical_id"] = logical_id
        if parent is not None:
            self._values["parent"] = parent
        if stack is not None:
            self._values["stack"] = stack

    @builtins.property
    def uuid(self) -> builtins.str:
        '''Universally unique identity.'''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''Serializable entity attributes.

        :see: {@link Attributes }
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Serializable entity flags.

        :see: {@link FlagEnum }
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Serializable entity metadata.

        :see: {@link Metadata }
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Serializable entity tags.

        :see: {@link Tags }
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Node id within parent (unique only between parent child nodes).'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type(self) -> NodeTypeEnum:
        '''Node type.'''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(NodeTypeEnum, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Node path.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''CloudFormation resource type for this node.'''
        result = self._values.get("cfn_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def children(self) -> typing.Optional[typing.Mapping[builtins.str, "SGNode"]]:
        '''Child node record.'''
        result = self._values.get("children")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "SGNode"]], result)

    @builtins.property
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        result = self._values.get("construct_info")
        return typing.cast(typing.Optional[ConstructInfo], result)

    @builtins.property
    def edges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of edge UUIDs where this node is the **source**.'''
        result = self._values.get("edges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        result = self._values.get("logical_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''UUID of node parent.'''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack(self) -> typing.Optional[builtins.str]:
        '''UUID of node stack.'''
        result = self._values.get("stack")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.SGUnresolvedReference",
    jsii_struct_bases=[],
    name_mapping={
        "reference_type": "referenceType",
        "source": "source",
        "target": "target",
        "value": "value",
    },
)
class SGUnresolvedReference:
    def __init__(
        self,
        *,
        reference_type: ReferenceTypeEnum,
        source: builtins.str,
        target: builtins.str,
        value: typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Unresolved reference struct.

        During graph computation references are unresolved and stored in this struct.

        :param reference_type: 
        :param source: 
        :param target: 
        :param value: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa7431867434a2137e5846e44d85951458fff9bfec89b6d18baf695ccac1152)
            check_type(argname="argument reference_type", value=reference_type, expected_type=type_hints["reference_type"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "reference_type": reference_type,
            "source": source,
            "target": target,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def reference_type(self) -> ReferenceTypeEnum:
        result = self._values.get("reference_type")
        assert result is not None, "Required property 'reference_type' is missing"
        return typing.cast(ReferenceTypeEnum, result)

    @builtins.property
    def source(self) -> builtins.str:
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]:
        result = self._values.get("value")
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGUnresolvedReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISerializableGraphStore)
class Store(metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.cdk_graph.Store"):
    '''Store class provides the in-memory database-like interface for managing all entities in the graph.'''

    def __init__(
        self,
        allow_destructive_mutations: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allow_destructive_mutations: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ea6e00aa63b42bbe0309faca00f3f2c33d792a7f545356abb532ec5104139e)
            check_type(argname="argument allow_destructive_mutations", value=allow_destructive_mutations, expected_type=type_hints["allow_destructive_mutations"])
        jsii.create(self.__class__, self, [allow_destructive_mutations])

    @jsii.member(jsii_name="fromSerializedStore")
    @builtins.classmethod
    def from_serialized_store(
        cls,
        *,
        edges: typing.Sequence[typing.Union["SGEdge", typing.Dict[builtins.str, typing.Any]]],
        tree: typing.Union[SGNode, typing.Dict[builtins.str, typing.Any]],
        version: builtins.str,
    ) -> "Store":
        '''Builds store from serialized store data.

        :param edges: List of edges.
        :param tree: Node tree.
        :param version: Store version.
        '''
        serialized_store = SGGraphStore(edges=edges, tree=tree, version=version)

        return typing.cast("Store", jsii.sinvoke(cls, "fromSerializedStore", [serialized_store]))

    @jsii.member(jsii_name="addEdge")
    def add_edge(self, edge: "Edge") -> None:
        '''Add **edge** to the store.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8c18b23d089868cb67226ca256b4cd10e9a7ca155fc7fe7309f3dbd5acc515)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "addEdge", [edge]))

    @jsii.member(jsii_name="addNode")
    def add_node(self, node: "Node") -> None:
        '''Add **node** to the store.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08df7ce71eba51d6b30e1165fd1ab8f2c1147aabef5307492d804d8b07a75e0)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addNode", [node]))

    @jsii.member(jsii_name="addStack")
    def add_stack(self, stack: "StackNode") -> None:
        '''Add **stack** node to the store.

        :param stack: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6bf01f1892100d80d0239da16617fdb0103a713554a7ba408519ad30450a0b)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "addStack", [stack]))

    @jsii.member(jsii_name="addStage")
    def add_stage(self, stage: "StageNode") -> None:
        '''Add **stage** to the store.

        :param stage: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088bfd5b6716f6f522b208805a39d18f01551b2949404fd8881c389f1ec71250)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast(None, jsii.invoke(self, "addStage", [stage]))

    @jsii.member(jsii_name="clone")
    def clone(
        self,
        allow_destructive_mutations: typing.Optional[builtins.bool] = None,
    ) -> "Store":
        '''Clone the store to allow destructive mutations.

        :param allow_destructive_mutations: Indicates if destructive mutations are allowed; defaults to ``true``

        :return: Returns a clone of the store that allows destructive mutations
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f83929500aaef9ce0301bdba7aef03afbc068ca7095661cac48b149311bb4ed)
            check_type(argname="argument allow_destructive_mutations", value=allow_destructive_mutations, expected_type=type_hints["allow_destructive_mutations"])
        return typing.cast("Store", jsii.invoke(self, "clone", [allow_destructive_mutations]))

    @jsii.member(jsii_name="computeLogicalUniversalId")
    def compute_logical_universal_id(
        self,
        stack: "StackNode",
        logical_id: builtins.str,
    ) -> builtins.str:
        '''Compute **universal** *logicalId* based on parent stack and construct *logicalId* (``<stack>:<logicalId>``).

        Construct *logicalIds are only unique within their containing stack, so to use *logicalId*
        lookups universally (like resolving references) we need a universal key.

        :param stack: -
        :param logical_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf5980e2a4a5a92457cdb1dc8d112425f98ee7ba06b38d9e4a02a1883698570)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "computeLogicalUniversalId", [stack, logical_id]))

    @jsii.member(jsii_name="findNodeByImportArn")
    def find_node_by_import_arn(self, value: typing.Any) -> typing.Optional["Node"]:
        '''Attempts to lookup the {@link Node} associated with a given *import arn token*.

        :param value: Import arn value, which is either object to tokenize or already tokenized string.

        :return: Returns matching {@link Node } if found, otherwise undefined.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45900ff0bb2bf1bd5a21faaf7123309f7c60287f797678df38c5f93fbef97282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "findNodeByImportArn", [value]))

    @jsii.member(jsii_name="findNodeByLogicalId")
    def find_node_by_logical_id(
        self,
        stack: "StackNode",
        logical_id: builtins.str,
    ) -> "Node":
        '''Find node within given **stack** with given *logicalId*.

        :param stack: -
        :param logical_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a343ed5216c7ef2bab0990b5bdf95578baa1b6177b7d4ab9c380cbf53ec5e75f)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast("Node", jsii.invoke(self, "findNodeByLogicalId", [stack, logical_id]))

    @jsii.member(jsii_name="findNodeByLogicalUniversalId")
    def find_node_by_logical_universal_id(self, uid: builtins.str) -> "Node":
        '''Find node by **universal** *logicalId* (``<stack>:<logicalId>``).

        :param uid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310fbedcaec37e662e2ed916f8b1c1018e1f6073e799b9196f401f39fba043d7)
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
        return typing.cast("Node", jsii.invoke(self, "findNodeByLogicalUniversalId", [uid]))

    @jsii.member(jsii_name="getEdge")
    def get_edge(self, uuid: builtins.str) -> "Edge":
        '''Get stored **edge** by UUID.

        :param uuid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab611670597ab4204704ecf8628bb796f88e048d01e42a8e5dce89b9e2d70a84)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("Edge", jsii.invoke(self, "getEdge", [uuid]))

    @jsii.member(jsii_name="getNode")
    def get_node(self, uuid: builtins.str) -> "Node":
        '''Get stored **node** by UUID.

        :param uuid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fbfc38993abde01b2db38aa6cc9edbf45adf130d09f6899c303a187168e023f)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("Node", jsii.invoke(self, "getNode", [uuid]))

    @jsii.member(jsii_name="getStack")
    def get_stack(self, uuid: builtins.str) -> "StackNode":
        '''Get stored **stack** node by UUID.

        :param uuid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830ba15764b106ae5f4d556295109e29d4d257cc27c20c59e01cc997c2f2eef0)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("StackNode", jsii.invoke(self, "getStack", [uuid]))

    @jsii.member(jsii_name="getStage")
    def get_stage(self, uuid: builtins.str) -> "StageNode":
        '''Get stored **stage** node by UUID.

        :param uuid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd66f46b6709793fc905605f4bc82c3dc913b19a1315eb0e7e4e1b8f1552cc01)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("StageNode", jsii.invoke(self, "getStage", [uuid]))

    @jsii.member(jsii_name="mutateRemoveEdge")
    def mutate_remove_edge(self, edge: "Edge") -> builtins.bool:
        '''Remove **edge** from the store.

        :param edge: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c61747d401d86dfa5347ad8bc919fd049739ed2dfdf99fd1f1dbad7c99b4520)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveEdge", [edge]))

    @jsii.member(jsii_name="mutateRemoveNode")
    def mutate_remove_node(self, node: "Node") -> builtins.bool:
        '''Remove **node** from the store.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7fbd2c49f36932ad82b78557f77bdd66ea5ff0cf861a1d2193bcf8ec067c90)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveNode", [node]))

    @jsii.member(jsii_name="recordImportArn")
    def record_import_arn(self, arn_token: builtins.str, resource: "Node") -> None:
        '''Records arn tokens from imported resources (eg: ``s3.Bucket.fromBucketArn()``) that are used for resolving references.

        :param arn_token: -
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8c984509a82dcce046ddc465440eb4aaafc4c90c3159e0367b2842d416b12f)
            check_type(argname="argument arn_token", value=arn_token, expected_type=type_hints["arn_token"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(None, jsii.invoke(self, "recordImportArn", [arn_token, resource]))

    @jsii.member(jsii_name="recordLogicalId")
    def record_logical_id(
        self,
        stack: "StackNode",
        logical_id: builtins.str,
        resource: "Node",
    ) -> None:
        '''Record a **universal** *logicalId* to node mapping in the store.

        :param stack: -
        :param logical_id: -
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0147cd2865c56325149b8ced263add8c62182a44f2d4dac4516d9af216c12e)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(None, jsii.invoke(self, "recordLogicalId", [stack, logical_id, resource]))

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> SGGraphStore:
        '''Serialize the store.'''
        return typing.cast(SGGraphStore, jsii.invoke(self, "serialize", []))

    @jsii.member(jsii_name="verifyDestructiveMutationAllowed")
    def verify_destructive_mutation_allowed(self) -> None:
        '''Verifies that the store allows destructive mutations.

        :throws: Error is store does **not** allow mutations
        '''
        return typing.cast(None, jsii.invoke(self, "verifyDestructiveMutationAllowed", []))

    @builtins.property
    @jsii.member(jsii_name="allowDestructiveMutations")
    def allow_destructive_mutations(self) -> builtins.bool:
        '''Indicates if the store allows destructive mutations.

        Destructive mutations are only allowed on clones of the store to prevent plugins and filters from
        mutating the store for downstream plugins.

        All ``mutate*`` methods are only allowed on stores that allow destructive mutations.

        This behavior may change in the future if the need arises for plugins to pass mutated stores
        to downstream plugins. But it will be done cautiously with ensuring the intent of
        downstream plugin is to receive the mutated store.
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowDestructiveMutations"))

    @builtins.property
    @jsii.member(jsii_name="counts")
    def counts(self) -> IStoreCounts:
        '''Get record of all store counters.'''
        return typing.cast(IStoreCounts, jsii.get(self, "counts"))

    @builtins.property
    @jsii.member(jsii_name="edges")
    def edges(self) -> typing.List["Edge"]:
        '''Gets all stored **edges**.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["Edge"], jsii.get(self, "edges"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> typing.List["Node"]:
        '''Gets all stored **nodes**.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> "RootNode":
        '''Root node in the store.

        The **root** node is not the computed root, but the graph root
        which is auto-generated and can not be mutated.
        '''
        return typing.cast("RootNode", jsii.get(self, "root"))

    @builtins.property
    @jsii.member(jsii_name="rootStacks")
    def root_stacks(self) -> typing.List["StackNode"]:
        '''Gets all stored **root stack** nodes.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["StackNode"], jsii.get(self, "rootStacks"))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List["StackNode"]:
        '''Gets all stored **stack** nodes.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["StackNode"], jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> typing.List["StageNode"]:
        '''Gets all stored **stage** nodes.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["StageNode"], jsii.get(self, "stages"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''Current SemVer version of the store.'''
        return typing.cast(builtins.str, jsii.get(self, "version"))


@jsii.implements(ISerializableEntity)
class BaseEntity(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws/pdk.cdk_graph.BaseEntity",
):
    '''Base class for all store entities (Node and Edges).'''

    def __init__(self, props: IBaseEntityProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daeb695a45aac73f4be0d8c6ef31e5368bd9d911f28d037a99949396c77fe6b0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addAttribute")
    def add_attribute(self, key: builtins.str, value: typing.Any) -> None:
        '''Add attribute.

        :param key: -
        :param value: -

        :throws: Error if attribute for key already exists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6dba75c8541a9883f96e96f61d9fd09b00357b6f7ea584b0e266b95778c3b0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addAttribute", [key, value]))

    @jsii.member(jsii_name="addFlag")
    def add_flag(self, flag: FlagEnum) -> None:
        '''Add flag.

        :param flag: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223ed34d4f83c84c2bc1a76467cd3a313f8bef582eb08e037082049da0925e65)
            check_type(argname="argument flag", value=flag, expected_type=type_hints["flag"])
        return typing.cast(None, jsii.invoke(self, "addFlag", [flag]))

    @jsii.member(jsii_name="addMetadata")
    def add_metadata(self, metadata_type: builtins.str, data: typing.Any) -> None:
        '''Add metadata entry.

        :param metadata_type: -
        :param data: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef4a8615be9f9211703124ffe8024c2484ae4052765e3d09fff5a2ffd451568)
            check_type(argname="argument metadata_type", value=metadata_type, expected_type=type_hints["metadata_type"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(None, jsii.invoke(self, "addMetadata", [metadata_type, data]))

    @jsii.member(jsii_name="addTag")
    def add_tag(self, key: builtins.str, value: builtins.str) -> None:
        '''Add tag.

        :param key: -
        :param value: -

        :throws: Throws Error is tag for key already exists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e666f8316c06f165c0672e3604d1cd73a700f5adbdc3a01becbdeec5b0ecba3)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addTag", [key, value]))

    @jsii.member(jsii_name="applyData")
    def apply_data(
        self,
        data: IBaseEntityDataProps,
        overwrite: typing.Optional[builtins.bool] = None,
        apply_flags: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Applies data (attributes, metadata, tags, flag) to entity.

        Generally used only for mutations such as collapse and consume to retain data.

        :param data: - The data to apply.
        :param overwrite: -
        :param apply_flags: - Indicates if data is overwritten - Indicates if flags should be applied.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e6b0e95faf9def98436116c7023e5be038f5b25b9cf74d27ce7454257d0e4e)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument overwrite", value=overwrite, expected_type=type_hints["overwrite"])
            check_type(argname="argument apply_flags", value=apply_flags, expected_type=type_hints["apply_flags"])
        return typing.cast(None, jsii.invoke(self, "applyData", [data, overwrite, apply_flags]))

    @jsii.member(jsii_name="findMetadata")
    def find_metadata(
        self,
        metadata_type: builtins.str,
    ) -> typing.List[_constructs_77d1e7e8.MetadataEntry]:
        '''Retrieves all metadata entries of a given type.

        :param metadata_type: -

        :type: Readonly<SerializedGraph.Metadata>
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49fcde4ea0e044c357a7302988f27de1593097203b5e0331177826e455ffecba)
            check_type(argname="argument metadata_type", value=metadata_type, expected_type=type_hints["metadata_type"])
        return typing.cast(typing.List[_constructs_77d1e7e8.MetadataEntry], jsii.invoke(self, "findMetadata", [metadata_type]))

    @jsii.member(jsii_name="getAttribute")
    def get_attribute(self, key: builtins.str) -> typing.Any:
        '''Get attribute by key.

        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062235bde2341056bb4308ef25c016a70b5850ff85396e53689d093e86347668)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Any, jsii.invoke(self, "getAttribute", [key]))

    @jsii.member(jsii_name="getTag")
    def get_tag(self, key: builtins.str) -> typing.Optional[builtins.str]:
        '''Get tag by key.

        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7323868bcc859eef95d19d417971746f17b6acdcc6a601a29cdd45f3e64d6c24)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getTag", [key]))

    @jsii.member(jsii_name="hasAttribute")
    def has_attribute(
        self,
        key: builtins.str,
        value: typing.Any = None,
    ) -> builtins.bool:
        '''Indicates if entity has a given attribute defined, and optionally with a specific value.

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65f039381b352ad4d492533c6b8109f7f2081cf1f56ba451e127a94ca3043ce1)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasAttribute", [key, value]))

    @jsii.member(jsii_name="hasFlag")
    def has_flag(self, flag: FlagEnum) -> builtins.bool:
        '''Indicates if entity has a given flag.

        :param flag: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7588896203296569a3d61e4ecec20db9f6a4a1c8cb1d98c386c1daa03fa093c8)
            check_type(argname="argument flag", value=flag, expected_type=type_hints["flag"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasFlag", [flag]))

    @jsii.member(jsii_name="hasMetadata")
    def has_metadata(
        self,
        metadata_type: builtins.str,
        data: typing.Any,
    ) -> builtins.bool:
        '''Indicates if entity has matching metadata entry.

        :param metadata_type: -
        :param data: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796c96046119f43257244800d8c8af882de4ae32d7420019b36820128dab8ed9)
            check_type(argname="argument metadata_type", value=metadata_type, expected_type=type_hints["metadata_type"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasMetadata", [metadata_type, data]))

    @jsii.member(jsii_name="hasTag")
    def has_tag(
        self,
        key: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> builtins.bool:
        '''Indicates if entity has tag, optionally verifying tag value.

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87398f6b45a668f7d65aced530383298bc5c0c8a043b7e9262cf69eaba6d759)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasTag", [key, value]))

    @jsii.member(jsii_name="mutateDestroy")
    @abc.abstractmethod
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroy the entity be removing all references and removing from store.

        :param strict: - If ``strict``, then entity must not have any references remaining when attempting to destroy.

        :destructive: true
        '''
        ...

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(self, key: builtins.str, value: typing.Any) -> None:
        '''Set attribute.

        This will overwrite existing attribute.

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62ae658852843297cb8f7a467aca6902551f3a9378113b105aa40e03c0072dc)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setAttribute", [key, value]))

    @jsii.member(jsii_name="setTag")
    def set_tag(self, key: builtins.str, value: builtins.str) -> None:
        '''Set tag.

        Will overwrite existing tag.

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83734012a451f19d48936f35f4e3f38f32eecc4503b43641936621e4b2c147dc)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setTag", [key, value]))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]:
        '''Get *readonly* record of all attributes.

        :type: Readonly<SerializedGraph.Attributes>
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]], jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.List[FlagEnum]:
        '''Get *readonly* list of all flags.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List[FlagEnum], jsii.get(self, "flags"))

    @builtins.property
    @jsii.member(jsii_name="isDestroyed")
    def is_destroyed(self) -> builtins.bool:
        '''Indicates if the entity has been destroyed (eg: removed from store).'''
        return typing.cast(builtins.bool, jsii.get(self, "isDestroyed"))

    @builtins.property
    @jsii.member(jsii_name="isMutated")
    def is_mutated(self) -> builtins.bool:
        '''Indicates if the entity has had destructive mutations applied.'''
        return typing.cast(builtins.bool, jsii.get(self, "isMutated"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.List[_constructs_77d1e7e8.MetadataEntry]:
        '''Get *readonly* list of all metadata entries.

        :type: Readonly<SerializedGraph.Metadata>
        '''
        return typing.cast(typing.List[_constructs_77d1e7e8.MetadataEntry], jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> Store:
        '''Reference to the store.'''
        return typing.cast(Store, jsii.get(self, "store"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Get *readonly* record of all tags.

        :type: Readonly<SerializedGraph.Tags>
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        '''Universally unique identifier.'''
        return typing.cast(builtins.str, jsii.get(self, "uuid"))


class _BaseEntityProxy(BaseEntity):
    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroy the entity be removing all references and removing from store.

        :param strict: - If ``strict``, then entity must not have any references remaining when attempting to destroy.

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f725d5a70a6b7fe6fad050e71509d865870f4bd635b2cc6eac66438d2c9e096)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BaseEntity).__jsii_proxy_class__ = lambda : _BaseEntityProxy


@jsii.implements(ISerializableEdge)
class Edge(BaseEntity, metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.cdk_graph.Edge"):
    '''Edge class defines a link (relationship) between nodes, as in standard `graph theory <https://en.wikipedia.org/wiki/Graph_theory>`_.'''

    def __init__(self, props: "IEdgeProps") -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab6ab7e189b4330415a37a51ebd37978c8189cccc8412bf611324161e2ab6fd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="findAllInChain")
    @builtins.classmethod
    def find_all_in_chain(
        cls,
        chain: typing.Sequence[typing.Any],
        predicate: IEdgePredicate,
    ) -> typing.List["Edge"]:
        '''Find all matching edges based on predicate within an EdgeChain.

        :param chain: -
        :param predicate: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5be3398beba49f9b3c52ea752d3528c05126b5c6515c60628d6535b73b42ef)
            check_type(argname="argument chain", value=chain, expected_type=type_hints["chain"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast(typing.List["Edge"], jsii.sinvoke(cls, "findAllInChain", [chain, predicate]))

    @jsii.member(jsii_name="findInChain")
    @builtins.classmethod
    def find_in_chain(
        cls,
        chain: typing.Sequence[typing.Any],
        predicate: IEdgePredicate,
    ) -> typing.Optional["Edge"]:
        '''Find first edge matching predicate within an EdgeChain.

        :param chain: -
        :param predicate: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a5bc50eadc381e5b3d45537040fa59fd26417b346c447ed288f77c91fba922)
            check_type(argname="argument chain", value=chain, expected_type=type_hints["chain"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast(typing.Optional["Edge"], jsii.sinvoke(cls, "findInChain", [chain, predicate]))

    @jsii.member(jsii_name="isEquivalent")
    def is_equivalent(self, edge: "Edge") -> builtins.bool:
        '''Indicates if this edge is equivalent to another edge.

        Edges are considered equivalent if they share same type, source, and target.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d67b4580af0da089331ae3889959fb2c01ca12f7cc4b34171913880c83d4840)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEquivalent", [edge]))

    @jsii.member(jsii_name="mutateConsume")
    def mutate_consume(self, edge: "Edge") -> None:
        '''Merge an equivalent edge's data into this edge and destroy the other edge.

        Used during filtering operations to consolidate equivalent edges.

        :param edge: - The edge to consume.

        :destructive: true
        :throws: Error is edge is not *equivalent*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed48f1605b531f8f7bdf9179be661069a4dc639e50a0c9dd6dec2a6d1ce884d)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "mutateConsume", [edge]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, _strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroy the edge.

        Remove all references and remove from store.

        :param _strict: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93efbfbd1860bda9c89a23a6fee4cb6fa162c1b804b9add268f083e5e9c8bbc7)
            check_type(argname="argument _strict", value=_strict, expected_type=type_hints["_strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [_strict]))

    @jsii.member(jsii_name="mutateDirection")
    def mutate_direction(self, direction: EdgeDirectionEnum) -> None:
        '''Change the edge **direction**.

        :param direction: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0392d8cc408dec6d4139add0acba2e1d9352b669425b414740f5d5a3210d41aa)
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
        return typing.cast(None, jsii.invoke(self, "mutateDirection", [direction]))

    @jsii.member(jsii_name="mutateSource")
    def mutate_source(self, node: "Node") -> None:
        '''Change the edge **source**.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87226ff0c3d1a50dea3a4c07eae7b03252d68b4c40f2c7836cf1406c836218d1)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "mutateSource", [node]))

    @jsii.member(jsii_name="mutateTarget")
    def mutate_target(self, node: "Node") -> None:
        '''Change the edge **target**.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8def7b646c4b685dcedf3851f3994050ed501edf65e6e4a1bb597d42c396fcca)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "mutateTarget", [node]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Get string representation of this edge.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="allowDestructiveMutations")
    def allow_destructive_mutations(self) -> builtins.bool:
        '''Indicates if edge allows destructive mutations.'''
        return typing.cast(builtins.bool, jsii.get(self, "allowDestructiveMutations"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> EdgeDirectionEnum:
        '''Indicates the direction in which the edge is directed.'''
        return typing.cast(EdgeDirectionEnum, jsii.get(self, "direction"))

    @builtins.property
    @jsii.member(jsii_name="edgeType")
    def edge_type(self) -> EdgeTypeEnum:
        '''Type of edge.'''
        return typing.cast(EdgeTypeEnum, jsii.get(self, "edgeType"))

    @builtins.property
    @jsii.member(jsii_name="isClosed")
    def is_closed(self) -> builtins.bool:
        '''Indicates if the Edge's **source** and **target** are the same, or were the same when it was created (prior to mutations).

        To check whether it was originally closed, use ``hasFlag(FlagEnum.CLOSED_EDGE)`` instead.
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isClosed"))

    @builtins.property
    @jsii.member(jsii_name="isCrossStack")
    def is_cross_stack(self) -> builtins.bool:
        '''Indicates if **source** and **target** nodes reside in different *root* stacks.'''
        return typing.cast(builtins.bool, jsii.get(self, "isCrossStack"))

    @builtins.property
    @jsii.member(jsii_name="isExtraneous")
    def is_extraneous(self) -> builtins.bool:
        '''Indicates if edge is extraneous which is determined by explicitly having *EXTRANEOUS* flag added and/or being a closed loop (source===target).'''
        return typing.cast(builtins.bool, jsii.get(self, "isExtraneous"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Node":
        '''Edge **source** is the node that defines the edge (tail).'''
        return typing.cast("Node", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Node":
        '''Edge **target** is the node being referenced by the **source** (head).'''
        return typing.cast("Node", jsii.get(self, "target"))


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IAppNodeProps")
class IAppNodeProps(IBaseEntityDataProps, typing_extensions.Protocol):
    '''{@link AppNode} props.'''

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> Store:
        '''Store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Type of CloudFormation resource.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.'''
        ...


class _IAppNodePropsProxy(
    jsii.proxy_for(IBaseEntityDataProps), # type: ignore[misc]
):
    '''{@link AppNode} props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IAppNodeProps"

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> Store:
        '''Store.'''
        return typing.cast(Store, jsii.get(self, "store"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Type of CloudFormation resource.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        return typing.cast(typing.Optional[ConstructInfo], jsii.get(self, "constructInfo"))

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalId"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.'''
        return typing.cast(typing.Optional["Node"], jsii.get(self, "parent"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAppNodeProps).__jsii_proxy_class__ = lambda : _IAppNodePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IAttributeReferenceProps")
class IAttributeReferenceProps(ITypedEdgeProps, typing_extensions.Protocol):
    '''Attribute type reference props.'''

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]:
        '''Resolved attribute value.'''
        ...

    @value.setter
    def value(
        self,
        value: typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]],
    ) -> None:
        ...


class _IAttributeReferencePropsProxy(
    jsii.proxy_for(ITypedEdgeProps), # type: ignore[misc]
):
    '''Attribute type reference props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IAttributeReferenceProps"

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]:
        '''Resolved attribute value.'''
        return typing.cast(typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]], jsii.get(self, "value"))

    @value.setter
    def value(
        self,
        value: typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af3d92f06eb65a1920d5855076e065bfb5aca635a999cf264b600b99c0464bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAttributeReferenceProps).__jsii_proxy_class__ = lambda : _IAttributeReferencePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.ICfnResourceNodeProps")
class ICfnResourceNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''CfnResourceNode props.'''

    @builtins.property
    @jsii.member(jsii_name="importArnToken")
    def import_arn_token(self) -> typing.Optional[builtins.str]:
        ...

    @import_arn_token.setter
    def import_arn_token(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        ...

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        ...


class _ICfnResourceNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''CfnResourceNode props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.ICfnResourceNodeProps"

    @builtins.property
    @jsii.member(jsii_name="importArnToken")
    def import_arn_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importArnToken"))

    @import_arn_token.setter
    def import_arn_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b853dfee42346b9d862590c9d269c32ebbf386d00b4c6e8121c852dc25d2016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importArnToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        return typing.cast(typing.Optional[NodeTypeEnum], jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec170afff8dfbb938ecb7c921ed87126e068e25e4b60b34a109a6272908d5b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICfnResourceNodeProps).__jsii_proxy_class__ = lambda : _ICfnResourceNodePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IEdgeProps")
class IEdgeProps(ITypedEdgeProps, typing_extensions.Protocol):
    '''Edge props interface.'''

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> EdgeDirectionEnum:
        '''Indicates the direction in which the edge is directed.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="edgeType")
    def edge_type(self) -> EdgeTypeEnum:
        '''Type of edge.'''
        ...


class _IEdgePropsProxy(
    jsii.proxy_for(ITypedEdgeProps), # type: ignore[misc]
):
    '''Edge props interface.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IEdgeProps"

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> EdgeDirectionEnum:
        '''Indicates the direction in which the edge is directed.'''
        return typing.cast(EdgeDirectionEnum, jsii.get(self, "direction"))

    @builtins.property
    @jsii.member(jsii_name="edgeType")
    def edge_type(self) -> EdgeTypeEnum:
        '''Type of edge.'''
        return typing.cast(EdgeTypeEnum, jsii.get(self, "edgeType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEdgeProps).__jsii_proxy_class__ = lambda : _IEdgePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.INodeProps")
class INodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''Node props.'''

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> NodeTypeEnum:
        '''Type of node.'''
        ...


class _INodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''Node props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.INodeProps"

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> NodeTypeEnum:
        '''Type of node.'''
        return typing.cast(NodeTypeEnum, jsii.get(self, "nodeType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodeProps).__jsii_proxy_class__ = lambda : _INodePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IOutputNodeProps")
class IOutputNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''OutputNode props.'''

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Resolved output value.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> typing.Optional[builtins.str]:
        '''Export name.'''
        ...


class _IOutputNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''OutputNode props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IOutputNodeProps"

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Resolved output value.'''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> typing.Optional[builtins.str]:
        '''Export name.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOutputNodeProps).__jsii_proxy_class__ = lambda : _IOutputNodePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IParameterNodeProps")
class IParameterNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''{@link ParameterNode} props.'''

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        '''Parameter type.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Resolved value.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.'''
        ...


class _IParameterNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''{@link ParameterNode} props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IParameterNodeProps"

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        '''Parameter type.'''
        return typing.cast(builtins.str, jsii.get(self, "parameterType"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Resolved value.'''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IParameterNodeProps).__jsii_proxy_class__ = lambda : _IParameterNodePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IReferenceProps")
class IReferenceProps(ITypedEdgeProps, typing_extensions.Protocol):
    '''Reference edge props.'''

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> typing.Optional[ReferenceTypeEnum]:
        '''Type of reference.'''
        ...

    @reference_type.setter
    def reference_type(self, value: typing.Optional[ReferenceTypeEnum]) -> None:
        ...


class _IReferencePropsProxy(
    jsii.proxy_for(ITypedEdgeProps), # type: ignore[misc]
):
    '''Reference edge props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IReferenceProps"

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> typing.Optional[ReferenceTypeEnum]:
        '''Type of reference.'''
        return typing.cast(typing.Optional[ReferenceTypeEnum], jsii.get(self, "referenceType"))

    @reference_type.setter
    def reference_type(self, value: typing.Optional[ReferenceTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0cc6c6fa4f8ee72758b7835a592762d1dca3de1ebf9c042fd0c08d8619f8360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceType", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReferenceProps).__jsii_proxy_class__ = lambda : _IReferencePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IResourceNodeProps")
class IResourceNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''ResourceNode props.'''

    @builtins.property
    @jsii.member(jsii_name="cdkOwned")
    def cdk_owned(self) -> builtins.bool:
        '''Indicates if this resource is owned by cdk (defined in cdk library).'''
        ...

    @cdk_owned.setter
    def cdk_owned(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''Type of node.'''
        ...

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        ...


class _IResourceNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''ResourceNode props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IResourceNodeProps"

    @builtins.property
    @jsii.member(jsii_name="cdkOwned")
    def cdk_owned(self) -> builtins.bool:
        '''Indicates if this resource is owned by cdk (defined in cdk library).'''
        return typing.cast(builtins.bool, jsii.get(self, "cdkOwned"))

    @cdk_owned.setter
    def cdk_owned(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e557d041c601e686c9d26ec6d21342360782f783d7a10da36018f0cae4554b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdkOwned", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''Type of node.'''
        return typing.cast(typing.Optional[NodeTypeEnum], jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b6fe631ac472ee879910fc4468af7beb78a03ac84d0ebf328845d6f9cac165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResourceNodeProps).__jsii_proxy_class__ = lambda : _IResourceNodePropsProxy


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.IStackNodeProps")
class IStackNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''{@link StackNode} props.'''

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''Type of node.'''
        ...

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        ...


class _IStackNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''{@link StackNode} props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.IStackNodeProps"

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''Type of node.'''
        return typing.cast(typing.Optional[NodeTypeEnum], jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24dec8cf2a8e099c6ba8c24f1a9fc263f2db157e7a1a7e1c6c479e4d7a312de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStackNodeProps).__jsii_proxy_class__ = lambda : _IStackNodePropsProxy


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.InferredNodeProps",
    jsii_struct_bases=[SGEntity],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
        "dependencies": "dependencies",
        "unresolved_references": "unresolvedReferences",
        "cfn_type": "cfnType",
        "construct_info": "constructInfo",
        "logical_id": "logicalId",
    },
)
class InferredNodeProps(SGEntity):
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        dependencies: typing.Sequence[builtins.str],
        unresolved_references: typing.Sequence[typing.Union[SGUnresolvedReference, typing.Dict[builtins.str, typing.Any]]],
        cfn_type: typing.Optional[builtins.str] = None,
        construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        logical_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Inferred node props.

        :param uuid: Universally unique identity.
        :param attributes: Serializable entity attributes.
        :param flags: Serializable entity flags.
        :param metadata: Serializable entity metadata.
        :param tags: Serializable entity tags.
        :param dependencies: 
        :param unresolved_references: 
        :param cfn_type: 
        :param construct_info: 
        :param logical_id: 
        '''
        if isinstance(construct_info, dict):
            construct_info = ConstructInfo(**construct_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eacd87f06afeb956eb173d8f94120330de6d6edc0570bba958f7ab3265cc974)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument unresolved_references", value=unresolved_references, expected_type=type_hints["unresolved_references"])
            check_type(argname="argument cfn_type", value=cfn_type, expected_type=type_hints["cfn_type"])
            check_type(argname="argument construct_info", value=construct_info, expected_type=type_hints["construct_info"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
            "dependencies": dependencies,
            "unresolved_references": unresolved_references,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags
        if cfn_type is not None:
            self._values["cfn_type"] = cfn_type
        if construct_info is not None:
            self._values["construct_info"] = construct_info
        if logical_id is not None:
            self._values["logical_id"] = logical_id

    @builtins.property
    def uuid(self) -> builtins.str:
        '''Universally unique identity.'''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''Serializable entity attributes.

        :see: {@link Attributes }
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Serializable entity flags.

        :see: {@link FlagEnum }
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Serializable entity metadata.

        :see: {@link Metadata }
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Serializable entity tags.

        :see: {@link Tags }
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def dependencies(self) -> typing.List[builtins.str]:
        result = self._values.get("dependencies")
        assert result is not None, "Required property 'dependencies' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def unresolved_references(self) -> typing.List[SGUnresolvedReference]:
        result = self._values.get("unresolved_references")
        assert result is not None, "Required property 'unresolved_references' is missing"
        return typing.cast(typing.List[SGUnresolvedReference], result)

    @builtins.property
    def cfn_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cfn_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        result = self._values.get("construct_info")
        return typing.cast(typing.Optional[ConstructInfo], result)

    @builtins.property
    def logical_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("logical_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InferredNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISerializableNode)
class Node(BaseEntity, metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.cdk_graph.Node"):
    '''Node class is the base definition of **node** entities in the graph, as in standard `graph theory <https://en.wikipedia.org/wiki/Graph_theory>`_.'''

    def __init__(self, props: INodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c044f8a8f65047634c290bd30cb01706503d338e658a07d8284c48adf3b9bb)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addChild")
    def add_child(self, node: "Node") -> None:
        '''Add *child* node.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d03f96f16f19869cd1c00de00e0584cafa103a93172080ed6f9598840a5e35)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addChild", [node]))

    @jsii.member(jsii_name="addLink")
    def add_link(self, edge: Edge) -> None:
        '''Add *link* to another node.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198071812d0a9d0d8eff09cdb17512adeaafd2d8d2da0c52e29a53307cd7948e)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "addLink", [edge]))

    @jsii.member(jsii_name="addReverseLink")
    def add_reverse_link(self, edge: Edge) -> None:
        '''Add *link* from another node.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c235e130710ac7faa707502265f3b8555eba35f5c4835190fe4f3b280d29c753)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "addReverseLink", [edge]))

    @jsii.member(jsii_name="doesDependOn")
    def does_depend_on(self, node: "Node") -> builtins.bool:
        '''Indicates if *this node* depends on *another node*.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c8dbe0444fcc170522913b01ab01586841c9da4a3cc2e9e1b1bba829f28c7f)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "doesDependOn", [node]))

    @jsii.member(jsii_name="doesReference")
    def does_reference(self, node: "Node") -> builtins.bool:
        '''Indicates if *this node* references *another node*.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91dc33cb071e4848ae1fed6f609d8197d7c8d7d9393d42470d7fa08d25f1f86)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "doesReference", [node]))

    @jsii.member(jsii_name="find")
    def find(self, predicate: INodePredicate) -> typing.Optional["Node"]:
        '''Recursively find the nearest sub-node matching predicate.

        :param predicate: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1118f8a31090d57684b9544621ad692d5ff87628fd069bc14103fb9ba9bbb16b)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "find", [predicate]))

    @jsii.member(jsii_name="findAll")
    def find_all(
        self,
        options: typing.Optional[IFindNodeOptions] = None,
    ) -> typing.List["Node"]:
        '''Return this construct and all of its sub-nodes in the given order.

        Optionally filter nodes based on predicate.

        :param options: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b847a14ccf7e62529c3d009411401ce63b374b1d763ce613bbd8f3dedae9e6)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(typing.List["Node"], jsii.invoke(self, "findAll", [options]))

    @jsii.member(jsii_name="findAllLinks")
    def find_all_links(
        self,
        options: typing.Optional[IFindEdgeOptions] = None,
    ) -> typing.List[Edge]:
        '''Return all direct links of this node and that of all sub-nodes.

        Optionally filter links based on predicate.

        :param options: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb006539eb07f788404c73f2e37e4eb77b4398a89e3ddd7c70e4d1dc8803645)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(typing.List[Edge], jsii.invoke(self, "findAllLinks", [options]))

    @jsii.member(jsii_name="findAncestor")
    def find_ancestor(
        self,
        predicate: INodePredicate,
        max: typing.Optional[jsii.Number] = None,
    ) -> typing.Optional["Node"]:
        '''Find nearest *ancestor* of *this node* matching given predicate.

        :param predicate: - Predicate to match ancestor.
        :param max: -

        :max: {number} [max] - Optional maximum levels to ascend
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c577eb6e9b7988d124c694764e1ee423bf2f3c4ff5afebfbe4a9d91c3bf99046)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "findAncestor", [predicate, max]))

    @jsii.member(jsii_name="findChild")
    def find_child(self, id: builtins.str) -> typing.Optional["Node"]:
        '''Find child with given *id*.

        Similar to ``find`` but does not throw error if no child found.

        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c579449b394221e0c6139c7a822c328e9c33f8755165ca213d23681a51ffe486)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "findChild", [id]))

    @jsii.member(jsii_name="findLink")
    def find_link(
        self,
        predicate: IEdgePredicate,
        reverse: typing.Optional[builtins.bool] = None,
        follow: typing.Optional[builtins.bool] = None,
        direct: typing.Optional[builtins.bool] = None,
    ) -> typing.Optional[Edge]:
        '''Find link of this node based on predicate.

        By default this will follow link
        chains to evaluate the predicate against and return the matching direct link
        of this node.

        :param predicate: Edge predicate function to match edge.
        :param reverse: Indicates if links are search in reverse order.
        :param follow: Indicates if link chain is followed.
        :param direct: Indicates that only *direct* links should be searched.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b870f9738220cb6754e6a2e63a7df3507848a71faf6425c672928318f907d5b0)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument direct", value=direct, expected_type=type_hints["direct"])
        return typing.cast(typing.Optional[Edge], jsii.invoke(self, "findLink", [predicate, reverse, follow, direct]))

    @jsii.member(jsii_name="findLinks")
    def find_links(
        self,
        predicate: IEdgePredicate,
        reverse: typing.Optional[builtins.bool] = None,
        follow: typing.Optional[builtins.bool] = None,
        direct: typing.Optional[builtins.bool] = None,
    ) -> typing.List[Edge]:
        '''Find all links of this node based on predicate.

        By default this will follow link
        chains to evaluate the predicate against and return the matching direct links
        of this node.

        :param predicate: Edge predicate function to match edge.
        :param reverse: Indicates if links are search in reverse order.
        :param follow: Indicates if link chain is followed.
        :param direct: Indicates that only *direct* links should be searched.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ddc4f2ab306bda5958b7a56113ea29778d15ef49859515aab9ea74cdde4e94)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument direct", value=direct, expected_type=type_hints["direct"])
        return typing.cast(typing.List[Edge], jsii.invoke(self, "findLinks", [predicate, reverse, follow, direct]))

    @jsii.member(jsii_name="getCfnProp")
    def get_cfn_prop(
        self,
        key: builtins.str,
    ) -> typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]:
        '''Get specific CloudFormation property.

        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a75b45f39d99968c01e0198aab540b24e269ad0844175ec82ef7313ea5ead7)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]], jsii.invoke(self, "getCfnProp", [key]))

    @jsii.member(jsii_name="getChild")
    def get_child(self, id: builtins.str) -> "Node":
        '''Get *child* node with given *id*.

        :param id: -

        :throws: Error if no child with given id
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb491e2fd9649eb3cd30f698b6b21fabd672c09c5002b1f813d499bf903d809)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("Node", jsii.invoke(self, "getChild", [id]))

    @jsii.member(jsii_name="getLinkChains")
    def get_link_chains(
        self,
        reverse: typing.Optional[builtins.bool] = None,
    ) -> typing.List[typing.List[typing.Any]]:
        '''Resolve all link chains.

        :param reverse: -

        :see: {@link EdgeChain }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f8b0b569b50b22beceaef1fa83a27acdaeb136a852be22a090c2f4afe32157)
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
        return typing.cast(typing.List[typing.List[typing.Any]], jsii.invoke(self, "getLinkChains", [reverse]))

    @jsii.member(jsii_name="getNearestAncestor")
    def get_nearest_ancestor(self, node: "Node") -> "Node":
        '''Gets the nearest **common** *ancestor* shared between *this node* and another *node*.

        :param node: -

        :throws: Error if *node* does not share a **common** *ancestor*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdf30bcfa12b1fadefa7d26aad527efdf11e417ed0d6d505ba3e2ec4652db07)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("Node", jsii.invoke(self, "getNearestAncestor", [node]))

    @jsii.member(jsii_name="isAncestor")
    def is_ancestor(self, ancestor: "Node") -> builtins.bool:
        '''Indicates if a specific *node* is an *ancestor* of *this node*.

        :param ancestor: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3426039160d35ea7a26817863b092ac89c4108d0c754b57b153ba6bce552ba0c)
            check_type(argname="argument ancestor", value=ancestor, expected_type=type_hints["ancestor"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isAncestor", [ancestor]))

    @jsii.member(jsii_name="isChild")
    def is_child(self, node: "Node") -> builtins.bool:
        '''Indicates if specific *node* is a *child* of *this node*.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2735ea376e9de6b6fddaeda923cc84656049413de27ccabbbcf6deb45c17ccb4)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isChild", [node]))

    @jsii.member(jsii_name="mutateCollapse")
    def mutate_collapse(self) -> None:
        '''Collapses all sub-nodes of *this node* into *this node*.

        :destructive: true
        '''
        return typing.cast(None, jsii.invoke(self, "mutateCollapse", []))

    @jsii.member(jsii_name="mutateCollapseTo")
    def mutate_collapse_to(self, ancestor: "Node") -> "Node":
        '''Collapses *this node* into *an ancestor*.

        :param ancestor: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa25b0a3b6b70a902bf8e32f8c5811e617446b61b567c9fb6381da7da8828ee4)
            check_type(argname="argument ancestor", value=ancestor, expected_type=type_hints["ancestor"])
        return typing.cast("Node", jsii.invoke(self, "mutateCollapseTo", [ancestor]))

    @jsii.member(jsii_name="mutateCollapseToParent")
    def mutate_collapse_to_parent(self) -> "Node":
        '''Collapses *this node* into *it's parent node*.

        :destructive: true
        '''
        return typing.cast("Node", jsii.invoke(self, "mutateCollapseToParent", []))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: - Indicates that this node must not have references.

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ed1e09ff81256afc84f16f40ddbd7eeee4c7cba3fd29a49dd6cd3f19c7d5d4)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, new_parent: "Node") -> None:
        '''Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        :param new_parent: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49846287b799fd3c70091023007e33f5051245b089f9256467c5962233a3e433)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [new_parent]))

    @jsii.member(jsii_name="mutateMove")
    def mutate_move(self, new_parent: "Node") -> None:
        '''Move this node into a new parent node.

        :param new_parent: - The parent to move this node to.

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f7329b5432b02654e1ad703695942a6d28fa2dd8a07f809763f62ac0c64371)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateMove", [new_parent]))

    @jsii.member(jsii_name="mutateRemoveChild")
    def mutate_remove_child(self, node: "Node") -> builtins.bool:
        '''Remove a *child* node from *this node*.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75733325f56e106350fa1ee95e8d307c7e0dcbee94064b581a6e86beb1683680)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveChild", [node]))

    @jsii.member(jsii_name="mutateRemoveLink")
    def mutate_remove_link(self, link: Edge) -> builtins.bool:
        '''Remove a *link* from *this node*.

        :param link: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6897ad4601f6abf9e6b03c91ff8efbcd2af93968abc441fdf67d35839b7c2722)
            check_type(argname="argument link", value=link, expected_type=type_hints["link"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveLink", [link]))

    @jsii.member(jsii_name="mutateRemoveReverseLink")
    def mutate_remove_reverse_link(self, link: Edge) -> builtins.bool:
        '''Remove a *link* to *this node*.

        :param link: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbeafcd0c1ad6249dd3c40949962bcbecc8572ecd38794c4f7c78893b195e275)
            check_type(argname="argument link", value=link, expected_type=type_hints["link"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveReverseLink", [link]))

    @jsii.member(jsii_name="mutateUncluster")
    def mutate_uncluster(self) -> None:
        '''Hoist all children to parent and collapse node to parent.

        :destructive: true
        '''
        return typing.cast(None, jsii.invoke(self, "mutateUncluster", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Get string representation of this node.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="allowDestructiveMutations")
    def allow_destructive_mutations(self) -> builtins.bool:
        '''Indicates if this node allows destructive mutations.

        :see: {@link Store.allowDestructiveMutations }
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowDestructiveMutations"))

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List["Node"]:
        '''Get all direct child nodes.'''
        return typing.cast(typing.List["Node"], jsii.get(self, "children"))

    @builtins.property
    @jsii.member(jsii_name="dependedOnBy")
    def depended_on_by(self) -> typing.List["Node"]:
        '''Get list of **Nodes** that *depend on this node*.

        :see: {@link Node.reverseDependencyLinks }
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "dependedOnBy"))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["Node"]:
        '''Get list of **Nodes** that *this node depends on*.

        :see: {@link Node.dependencyLinks }
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="dependencyLinks")
    def dependency_links(self) -> typing.List["Dependency"]:
        '''Gets list of {@link Dependency} links (edges) where this node is the **source**.'''
        return typing.cast(typing.List["Dependency"], jsii.get(self, "dependencyLinks"))

    @builtins.property
    @jsii.member(jsii_name="depth")
    def depth(self) -> jsii.Number:
        '''Indicates the depth of the node relative to root (0).'''
        return typing.cast(jsii.Number, jsii.get(self, "depth"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Node id, which is only unique within parent scope.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="isAsset")
    def is_asset(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.ASSET}.'''
        return typing.cast(builtins.bool, jsii.get(self, "isAsset"))

    @builtins.property
    @jsii.member(jsii_name="isCfnFqn")
    def is_cfn_fqn(self) -> builtins.bool:
        '''Indicates if node ConstructInfoFqn denotes a ``aws-cdk-lib.*.Cfn*`` construct.

        :see: {@link FlagEnum.CFN_FQN }
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isCfnFqn"))

    @builtins.property
    @jsii.member(jsii_name="isCluster")
    def is_cluster(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.CLUSTER}.'''
        return typing.cast(builtins.bool, jsii.get(self, "isCluster"))

    @builtins.property
    @jsii.member(jsii_name="isCustomResource")
    def is_custom_resource(self) -> builtins.bool:
        '''Indicates if node is a *Custom Resource*.'''
        return typing.cast(builtins.bool, jsii.get(self, "isCustomResource"))

    @builtins.property
    @jsii.member(jsii_name="isExtraneous")
    def is_extraneous(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.EXTRANEOUS} node or determined to be extraneous: - Clusters that contain no children.'''
        return typing.cast(builtins.bool, jsii.get(self, "isExtraneous"))

    @builtins.property
    @jsii.member(jsii_name="isGraphContainer")
    def is_graph_container(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.GRAPH_CONTAINER}.'''
        return typing.cast(builtins.bool, jsii.get(self, "isGraphContainer"))

    @builtins.property
    @jsii.member(jsii_name="isLeaf")
    def is_leaf(self) -> builtins.bool:
        '''Indicates if this node is a *leaf* node, which means it does not have children.'''
        return typing.cast(builtins.bool, jsii.get(self, "isLeaf"))

    @builtins.property
    @jsii.member(jsii_name="isTopLevel")
    def is_top_level(self) -> builtins.bool:
        '''Indicates if node is direct child of the graph root node.'''
        return typing.cast(builtins.bool, jsii.get(self, "isTopLevel"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> typing.List[Edge]:
        '''Gets all links (edges) in which this node is the **source**.'''
        return typing.cast(typing.List[Edge], jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> NodeTypeEnum:
        '''Type of node.'''
        return typing.cast(NodeTypeEnum, jsii.get(self, "nodeType"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''Path of the node.'''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="referencedBy")
    def referenced_by(self) -> typing.List["Node"]:
        '''Get list of **Nodes** that *reference this node*.

        :see: {@link Node.reverseReferenceLinks }
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "referencedBy"))

    @builtins.property
    @jsii.member(jsii_name="referenceLinks")
    def reference_links(self) -> typing.List["Reference"]:
        '''Gets list of {@link Reference} links (edges) where this node is the **source**.'''
        return typing.cast(typing.List["Reference"], jsii.get(self, "referenceLinks"))

    @builtins.property
    @jsii.member(jsii_name="references")
    def references(self) -> typing.List["Node"]:
        '''Get list of **Nodes** that *this node references*.

        :see: {@link Node.referenceLinks }
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "references"))

    @builtins.property
    @jsii.member(jsii_name="reverseDependencyLinks")
    def reverse_dependency_links(self) -> typing.List["Dependency"]:
        '''Gets list of {@link Dependency} links (edges) where this node is the **target**.'''
        return typing.cast(typing.List["Dependency"], jsii.get(self, "reverseDependencyLinks"))

    @builtins.property
    @jsii.member(jsii_name="reverseLinks")
    def reverse_links(self) -> typing.List[Edge]:
        '''Gets all links (edges) in which this node is the **target**.'''
        return typing.cast(typing.List[Edge], jsii.get(self, "reverseLinks"))

    @builtins.property
    @jsii.member(jsii_name="reverseReferenceLinks")
    def reverse_reference_links(self) -> typing.List["Reference"]:
        '''Gets list of {@link Reference} links (edges) where this node is the **target**.'''
        return typing.cast(typing.List["Reference"], jsii.get(self, "reverseReferenceLinks"))

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List["Node"]:
        '''Gets descending ordered list of ancestors from the root.'''
        return typing.cast(typing.List["Node"], jsii.get(self, "scopes"))

    @builtins.property
    @jsii.member(jsii_name="siblings")
    def siblings(self) -> typing.List["Node"]:
        '''Get list of *siblings* of this node.'''
        return typing.cast(typing.List["Node"], jsii.get(self, "siblings"))

    @builtins.property
    @jsii.member(jsii_name="cfnProps")
    def cfn_props(self) -> typing.Optional[PlainObject]:
        '''Gets CloudFormation properties for this node.'''
        return typing.cast(typing.Optional[PlainObject], jsii.get(self, "cfnProps"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Get the CloudFormation resource type for this node.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        return typing.cast(typing.Optional[ConstructInfo], jsii.get(self, "constructInfo"))

    @builtins.property
    @jsii.member(jsii_name="constructInfoFqn")
    def construct_info_fqn(self) -> typing.Optional[builtins.str]:
        '''Synthesized construct information defining jii resolution data.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "constructInfoFqn"))

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalId"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.

        Only the root node should not have parent.
        '''
        return typing.cast(typing.Optional["Node"], jsii.get(self, "parent"))

    @builtins.property
    @jsii.member(jsii_name="rootStack")
    def root_stack(self) -> typing.Optional["StackNode"]:
        '''Get **root** stack.'''
        return typing.cast(typing.Optional["StackNode"], jsii.get(self, "rootStack"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional["StackNode"]:
        '''Stack the node is contained in.'''
        return typing.cast(typing.Optional["StackNode"], jsii.get(self, "stack"))


class OutputNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.OutputNode",
):
    '''OutputNode defines a cdk CfnOutput resources.'''

    def __init__(self, props: IOutputNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed71596e37a35e0636fc38dfb3007da46414fc4b15359b0d552f61fbca643de)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isOutputNode")
    @builtins.classmethod
    def is_output_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is an {@link OutputNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e9eb1bf349e1d4018b9586b0cc274ff2a5f2feb16b8037573683d1965d614ec)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isOutputNode", [node]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3921680ac1dd8fc422fb68fdea498275bfd2a7c5019599295dddfcfc23e89fa3)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_EXPORT_NAME")
    def ATTR_EXPORT_NAME(cls) -> builtins.str:
        '''Attribute key where output export name is stored.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_EXPORT_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_VALUE")
    def ATTR_VALUE(cls) -> builtins.str:
        '''Attribute key where output value is stored.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_VALUE"))

    @builtins.property
    @jsii.member(jsii_name="isExport")
    def is_export(self) -> builtins.bool:
        '''Indicates if {@link OutputNode} is **exported**.'''
        return typing.cast(builtins.bool, jsii.get(self, "isExport"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Get the *value** attribute.'''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> typing.Optional[builtins.str]:
        '''Get the export name attribute.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportName"))


class ParameterNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.ParameterNode",
):
    '''ParameterNode defines a CfnParameter node.'''

    def __init__(self, props: IParameterNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6af02cc2fc74978e9626fb5844f8e8a8be13c6614d1918de991cb6d2972f2d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isParameterNode")
    @builtins.classmethod
    def is_parameter_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link ParameterNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a28c720f2c3aeda10f04ad7d97ffb429a777a49c9baba6b10336454c15f0ed)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isParameterNode", [node]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1184e3e97f69dba27fc8b6b4f7e67d849e006f7d47b489659cfd0f89609c434b)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_TYPE")
    def ATTR_TYPE(cls) -> builtins.str:
        '''Attribute key where parameter type is stored.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_VALUE")
    def ATTR_VALUE(cls) -> builtins.str:
        '''Attribute key where parameter value is store.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_VALUE"))

    @builtins.property
    @jsii.member(jsii_name="isStackReference")
    def is_stack_reference(self) -> builtins.bool:
        '''Indicates if parameter is a reference to a stack.'''
        return typing.cast(builtins.bool, jsii.get(self, "isStackReference"))

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> typing.Any:
        '''Get the parameter type attribute.'''
        return typing.cast(typing.Any, jsii.get(self, "parameterType"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Get the value attribute.'''
        return typing.cast(typing.Any, jsii.get(self, "value"))


class Reference(
    Edge,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.Reference",
):
    '''Reference edge class defines a directed relationship between nodes.'''

    def __init__(self, props: IReferenceProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8badf88f3abd3427e44f2b4990b8e53878f04099a6cbb3fa2be81bb8801fad43)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isRef")
    @builtins.classmethod
    def is_ref(cls, edge: Edge) -> builtins.bool:
        '''Indicates if edge is a **Ref** based {@link Reference} edge.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f900ad592251e3da18f561007745ac3afb09f9e17b8f0e5b0f419aa5c8a1ed6d)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isRef", [edge]))

    @jsii.member(jsii_name="isReference")
    @builtins.classmethod
    def is_reference(cls, edge: Edge) -> builtins.bool:
        '''Indicates if edge is a {@link Reference}.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc467db16516a30e91fc3b1d10146caffbd78b3dee110b4b32b32778bc76ad3)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isReference", [edge]))

    @jsii.member(jsii_name="resolveChain")
    def resolve_chain(self) -> typing.List[typing.Any]:
        '''Resolve reference chain.'''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "resolveChain", []))

    @jsii.member(jsii_name="resolveTargets")
    def resolve_targets(self) -> typing.List[Node]:
        '''Resolve targets by following potential edge chain.

        :see: {@link EdgeChain }
        '''
        return typing.cast(typing.List[Node], jsii.invoke(self, "resolveTargets", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_TYPE")
    def ATT_TYPE(cls) -> builtins.str:
        '''Attribute defining the type of reference.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''Edge prefix to denote **Ref** type reference edge.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> ReferenceTypeEnum:
        '''Get type of reference.'''
        return typing.cast(ReferenceTypeEnum, jsii.get(self, "referenceType"))


class ResourceNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.ResourceNode",
):
    '''ResourceNode class defines a L2 cdk resource construct.'''

    def __init__(self, props: IResourceNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab7fbb9f68d49cf9fe9ceac18872f881e0ac4324d2343b65ec4e4046c88ccee)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isResourceNode")
    @builtins.classmethod
    def is_resource_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link ResourceNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f313bdc83492a1f712a614426e66f0985d89572180f2748e3dcefb78200e4ae)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isResourceNode", [node]))

    @jsii.member(jsii_name="mutateCfnResource")
    def mutate_cfn_resource(
        self,
        cfn_resource: typing.Optional["CfnResourceNode"] = None,
    ) -> None:
        '''Modifies the L1 resource wrapped by this L2 resource.

        :param cfn_resource: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b495d95ea2d6027725ebd56226b4ccd6e1fa8c4909c899f1faa40e8ed42673)
            check_type(argname="argument cfn_resource", value=cfn_resource, expected_type=type_hints["cfn_resource"])
        return typing.cast(None, jsii.invoke(self, "mutateCfnResource", [cfn_resource]))

    @jsii.member(jsii_name="mutateRemoveChild")
    def mutate_remove_child(self, node: Node) -> builtins.bool:
        '''Remove a *child* node from *this node*.

        :param node: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac7612e5e5be5d7c2563f557ac98d88197511cd31fc0456e4bb744506bd602a)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveChild", [node]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_WRAPPED_CFN_PROPS")
    def ATT_WRAPPED_CFN_PROPS(cls) -> builtins.str:
        '''Attribute key for cfn properties.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_WRAPPED_CFN_PROPS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_WRAPPED_CFN_TYPE")
    def ATT_WRAPPED_CFN_TYPE(cls) -> builtins.str:
        '''Attribute key for cfn resource type.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_WRAPPED_CFN_TYPE"))

    @builtins.property
    @jsii.member(jsii_name="isCdkOwned")
    def is_cdk_owned(self) -> builtins.bool:
        '''Indicates if this resource is owned by cdk (defined in cdk library).'''
        return typing.cast(builtins.bool, jsii.get(self, "isCdkOwned"))

    @builtins.property
    @jsii.member(jsii_name="isWrapper")
    def is_wrapper(self) -> builtins.bool:
        '''Indicates if Resource wraps a single CfnResource.'''
        return typing.cast(builtins.bool, jsii.get(self, "isWrapper"))

    @builtins.property
    @jsii.member(jsii_name="cfnProps")
    def cfn_props(self) -> typing.Optional[PlainObject]:
        '''Get the cfn properties from the L1 resource that this L2 resource wraps.'''
        return typing.cast(typing.Optional[PlainObject], jsii.get(self, "cfnProps"))

    @builtins.property
    @jsii.member(jsii_name="cfnResource")
    def cfn_resource(self) -> typing.Optional["CfnResourceNode"]:
        '''Get the default/primary CfnResource that this Resource wraps.'''
        return typing.cast(typing.Optional["CfnResourceNode"], jsii.get(self, "cfnResource"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Get the CloudFormation resource type for this L2 resource or for the L1 resource is wraps.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))


class RootNode(Node, metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.cdk_graph.RootNode"):
    '''RootNode represents the root of the store tree.'''

    def __init__(self, store: Store) -> None:
        '''
        :param store: Reference to the store.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e5346d075b2479f66d7464928a4c7fff8b9da2ecb894a024e207d7b52c17354)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        jsii.create(self.__class__, self, [store])

    @jsii.member(jsii_name="isRootNode")
    @builtins.classmethod
    def is_root_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link RootNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3abac9207872e959161e02ce2bfbce4e67d05297979f2bf1a3197b0335a98f44)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isRootNode", [node]))

    @jsii.member(jsii_name="findAll")
    def find_all(
        self,
        options: typing.Optional[IFindNodeOptions] = None,
    ) -> typing.List[Node]:
        '''Return this construct and all of its sub-nodes in the given order.

        Optionally filter nodes based on predicate.
        **The root not is excluded from list**

        :param options: -

        :inheritdoc: **The root not is excluded from list**
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4cf7ad982505f29a1bf19ec1541e7cc26dfe10356c04dd39a8673b5aed191e8)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(typing.List[Node], jsii.invoke(self, "findAll", [options]))

    @jsii.member(jsii_name="mutateCollapse")
    def mutate_collapse(self) -> None:
        '''Collapses all sub-nodes of *this node* into *this node*.

        .. epigraph::

           {@link RootNode} does not support this mutation

        :inheritdoc: true
        :throws: Error does not support
        '''
        return typing.cast(None, jsii.invoke(self, "mutateCollapse", []))

    @jsii.member(jsii_name="mutateCollapseTo")
    def mutate_collapse_to(self, _ancestor: Node) -> Node:
        '''Collapses *this node* into *an ancestor* > {@link RootNode} does not support this mutation.

        :param _ancestor: -

        :inheritdoc: true
        :throws: Error does not support
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a329370e0d7c7d33fd9ff5886d120a7c63f73a23d3eb3dd70289b635861d87)
            check_type(argname="argument _ancestor", value=_ancestor, expected_type=type_hints["_ancestor"])
        return typing.cast(Node, jsii.invoke(self, "mutateCollapseTo", [_ancestor]))

    @jsii.member(jsii_name="mutateCollapseToParent")
    def mutate_collapse_to_parent(self) -> Node:
        '''Collapses *this node* into *it's parent node* > {@link RootNode} does not support this mutation.

        :inheritdoc: true
        :throws: Error does not support
        '''
        return typing.cast(Node, jsii.invoke(self, "mutateCollapseToParent", []))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, _strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        .. epigraph::

           {@link RootNode} does not support this mutation

        :param _strict: -

        :inheritdoc: true
        :throws: Error does not support
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a4bf78315f69c74c892bfceb9bc6d044480fd59997260eba075494da3869dc)
            check_type(argname="argument _strict", value=_strict, expected_type=type_hints["_strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [_strict]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, _new_parent: Node) -> None:
        '''Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        .. epigraph::

           {@link RootNode} does not support this mutation

        :param _new_parent: -

        :inheritdoc: true
        :throws: Error does not support
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108861ca325ad24ba3f68920053fd24a97a9dddbe771888244077e7cb3b76f5f)
            check_type(argname="argument _new_parent", value=_new_parent, expected_type=type_hints["_new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [_new_parent]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PATH")
    def PATH(cls) -> builtins.str:
        '''Fixed path of root.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UUID")
    def UUID(cls) -> builtins.str:
        '''Fixed UUID of root.'''
        return typing.cast(builtins.str, jsii.sget(cls, "UUID"))


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph.SGEdge",
    jsii_struct_bases=[SGEntity],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
        "direction": "direction",
        "edge_type": "edgeType",
        "source": "source",
        "target": "target",
    },
)
class SGEdge(SGEntity):
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        direction: EdgeDirectionEnum,
        edge_type: EdgeTypeEnum,
        source: builtins.str,
        target: builtins.str,
    ) -> None:
        '''Serializable graph edge entity.

        :param uuid: Universally unique identity.
        :param attributes: Serializable entity attributes.
        :param flags: Serializable entity flags.
        :param metadata: Serializable entity metadata.
        :param tags: Serializable entity tags.
        :param direction: Indicates the direction in which the edge is directed.
        :param edge_type: Type of edge.
        :param source: UUID of edge **source** node (tail).
        :param target: UUID of edge **target** node (head).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddff8d68af5cd7268e6d71f570829df122147a7ff8555327598fb2d72e7de9d2)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument edge_type", value=edge_type, expected_type=type_hints["edge_type"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
            "direction": direction,
            "edge_type": edge_type,
            "source": source,
            "target": target,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def uuid(self) -> builtins.str:
        '''Universally unique identity.'''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''Serializable entity attributes.

        :see: {@link Attributes }
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Serializable entity flags.

        :see: {@link FlagEnum }
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Serializable entity metadata.

        :see: {@link Metadata }
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Serializable entity tags.

        :see: {@link Tags }
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def direction(self) -> EdgeDirectionEnum:
        '''Indicates the direction in which the edge is directed.'''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(EdgeDirectionEnum, result)

    @builtins.property
    def edge_type(self) -> EdgeTypeEnum:
        '''Type of edge.'''
        result = self._values.get("edge_type")
        assert result is not None, "Required property 'edge_type' is missing"
        return typing.cast(EdgeTypeEnum, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''UUID of edge **source**  node (tail).'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''UUID of edge **target**  node (head).'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGEdge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.StackNode",
):
    '''StackNode defines a cdk Stack.'''

    def __init__(self, props: IStackNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214334fddbdfdb5b8890a5f1ec4ce71e4bea33db3891357cc6c4eee098f5f85d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isStackNode")
    @builtins.classmethod
    def is_stack_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link StackNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd3c080ef567e757a6948e4b4ae64b503a64a83fb0b3b7f661e76b4e2bafb66b)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStackNode", [node]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, node: Node) -> "StackNode":
        '''Gets the {@link StackNode} containing a given resource.

        :param node: -

        :throws: Error is node is not contained in a stack
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f469c6d1d0c870c1217e56aad870498a3c8c74ff1037dd2f1dfab1dcdf237d59)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("StackNode", jsii.sinvoke(cls, "of", [node]))

    @jsii.member(jsii_name="addOutput")
    def add_output(self, node: OutputNode) -> None:
        '''Associate {@link OutputNode} with this stack.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01390d8fbab550ab9b7fe0be9afdd5fef16023fa253b812217486965e56e355d)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addOutput", [node]))

    @jsii.member(jsii_name="addParameter")
    def add_parameter(self, node: ParameterNode) -> None:
        '''Associate {@link ParameterNode} with this stack.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfd77363e6f3be11a9ae3ffd40786090c8864d25f3b5d43800ae52948c8d6df)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addParameter", [node]))

    @jsii.member(jsii_name="findOutput")
    def find_output(self, logical_id: builtins.str) -> OutputNode:
        '''Find {@link OutputNode} with *logicalId* defined by this stack.

        :param logical_id: -

        :throws: Error is no output found matching *logicalId*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08efe87ca0fc942e4ef45eceb73d2a81d2f1812a96b06e305b6df3ecf1f33e4b)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast(OutputNode, jsii.invoke(self, "findOutput", [logical_id]))

    @jsii.member(jsii_name="findParameter")
    def find_parameter(self, parameter_id: builtins.str) -> ParameterNode:
        '''Find {@link ParameterNode} with *parameterId* defined by this stack.

        :param parameter_id: -

        :throws: Error is no parameter found matching *parameterId*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22206334ffedc950168a664e68843a19e115901e62ad76cde0441d79be17dcd4)
            check_type(argname="argument parameter_id", value=parameter_id, expected_type=type_hints["parameter_id"])
        return typing.cast(ParameterNode, jsii.invoke(self, "findParameter", [parameter_id]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c101a514d513f496bf720133140b42a68fddf55ffdbd103dd376bf02e4975a1)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, new_parent: Node) -> None:
        '''Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        :param new_parent: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c611df42668de673d25b358a896cb95435ebac6563684d743d3f55612617d0)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [new_parent]))

    @jsii.member(jsii_name="mutateRemoveOutput")
    def mutate_remove_output(self, node: OutputNode) -> builtins.bool:
        '''Disassociate {@link OutputNode} from this stack.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50bb3b84d4d5a478e9c2aa0108688841ea46503495adce419a5f634ef490ad0)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveOutput", [node]))

    @jsii.member(jsii_name="mutateRemoveParameter")
    def mutate_remove_parameter(self, node: ParameterNode) -> builtins.bool:
        '''Disassociate {@link ParameterNode} from this stack.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed30ded726ea140c7007c184f19287732d397de06409c85f21639e7fee97666)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveParameter", [node]))

    @builtins.property
    @jsii.member(jsii_name="exports")
    def exports(self) -> typing.List[OutputNode]:
        '''Get all **exported** {@link OutputNode}s defined by this stack.'''
        return typing.cast(typing.List[OutputNode], jsii.get(self, "exports"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.List[OutputNode]:
        '''Get all {@link OutputNode}s defined by this stack.'''
        return typing.cast(typing.List[OutputNode], jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.List[ParameterNode]:
        '''Get all {@link ParameterNode}s defined by this stack.'''
        return typing.cast(typing.List[ParameterNode], jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional["StageNode"]:
        '''Get {@link StageNode} containing this stack.'''
        return typing.cast(typing.Optional["StageNode"], jsii.get(self, "stage"))


class StageNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.StageNode",
):
    '''StageNode defines a cdk Stage.'''

    def __init__(self, props: ITypedNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541e8c0f1a72250fc8ea6113c2bf61646d098ddf01a3da7d2f26bb247c93a445)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isStageNode")
    @builtins.classmethod
    def is_stage_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link StageNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38955797a4d22cb4fc20b63df6ce512f5214f60df97e4b045dd068dd854a14c2)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStageNode", [node]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, node: Node) -> "StageNode":
        '''Gets the {@link StageNode} containing a given resource.

        :param node: -

        :throws: Error is node is not contained in a stage
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0036ab7a7ade621459078354b0ddf4ba9f118d4897c466c68e589a5e7e256c)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("StageNode", jsii.sinvoke(cls, "of", [node]))

    @jsii.member(jsii_name="addStack")
    def add_stack(self, stack: StackNode) -> None:
        '''Associate a {@link StackNode} with this stage.

        :param stack: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0060c1529a42c00f8c4379a73a4d82acc5e250b4b89ef23500f83fd55084f9fc)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "addStack", [stack]))

    @jsii.member(jsii_name="mutateRemoveStack")
    def mutate_remove_stack(self, stack: StackNode) -> builtins.bool:
        '''Disassociate {@link StackNode} from this stage.

        :param stack: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c873622490206d4a1e2aeaa397352e0853716b06269c11d15e9acfb1820a24)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveStack", [stack]))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[StackNode]:
        '''Gets all stacks contained by this stage.'''
        return typing.cast(typing.List[StackNode], jsii.get(self, "stacks"))


class AppNode(Node, metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.cdk_graph.AppNode"):
    '''AppNode defines a cdk App.'''

    def __init__(self, props: IAppNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739f1561565f269abf8ddf1001e5031738d6dd497c13cfe3995d4d54ccbcfb65)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isAppNode")
    @builtins.classmethod
    def is_app_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link AppNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bd7da5daf2def243349d3a975bb0b6078d2a54fe77a1ac897c50face6822c9)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isAppNode", [node]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PATH")
    def PATH(cls) -> builtins.str:
        '''Fixed path of the App.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UUID")
    def UUID(cls) -> builtins.str:
        '''Fixed UUID for App node.'''
        return typing.cast(builtins.str, jsii.sget(cls, "UUID"))


class AttributeReference(
    Reference,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.AttributeReference",
):
    '''Attribute type reference edge.'''

    def __init__(self, props: IAttributeReferenceProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd65695412c23b057af4c788298676d03d47a64c95c1fe14efa6164f586b66a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isAtt")
    @builtins.classmethod
    def is_att(cls, edge: Edge) -> builtins.bool:
        '''Indicates if edge in an **Fn::GetAtt** {@link Reference}.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822d80f3a40b12eed417099ec2b64ac06836e0dab84489d7a10f28ce571dfed7)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isAtt", [edge]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_VALUE")
    def ATT_VALUE(cls) -> builtins.str:
        '''Attribute key for resolved value of attribute reference.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_VALUE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''Edge prefix to denote **Fn::GetAtt** type reference edge.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''Get the resolved attribute value.'''
        return typing.cast(builtins.str, jsii.get(self, "value"))


class CfnResourceNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.CfnResourceNode",
):
    '''CfnResourceNode defines an L1 cdk resource.'''

    def __init__(self, props: ICfnResourceNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b4909167c4ec814e31cb80d43be1227b68bf3ceab65648e684dbdd8aa8bcfc)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isCfnResourceNode")
    @builtins.classmethod
    def is_cfn_resource_node(cls, node: Node) -> builtins.bool:
        '''Indicates if a node is a {@link CfnResourceNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bc6c0df2c621db05595566d295936c3898490ecfac1a0e358994b11d9e26de)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnResourceNode", [node]))

    @jsii.member(jsii_name="isEquivalentFqn")
    def is_equivalent_fqn(self, resource: ResourceNode) -> builtins.bool:
        '''Evaluates if CfnResourceNode fqn is equivalent to ResourceNode fqn.

        :param resource: - {@link Graph.ResourceNode } to compare.

        :return: Returns ``true`` if equivalent, otherwise ``false``

        Example::

            `aws-cdk-lib.aws_lambda.Function` => `aws-cdk-lib.aws_lambda.CfnFunction`
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6864031b0074d0123ff669d9572a89e0e1f8c26afbcf44b0200ea8cac5edd96)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEquivalentFqn", [resource]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862784a149b27e7deb929fe15991070c67e4fa16d70c9e63267a3a60b29e72d7)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_IMPORT_ARN_TOKEN")
    def ATT_IMPORT_ARN_TOKEN(cls) -> builtins.str:
        '''Normalized CfnReference attribute.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_IMPORT_ARN_TOKEN"))

    @builtins.property
    @jsii.member(jsii_name="isExtraneous")
    def is_extraneous(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.EXTRANEOUS} node or determined to be extraneous: - Clusters that contain no children.

        :inheritdoc: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isExtraneous"))

    @builtins.property
    @jsii.member(jsii_name="isImport")
    def is_import(self) -> builtins.bool:
        '''Indicates if this CfnResource is imported (eg: ``s3.Bucket.fromBucketArn``).'''
        return typing.cast(builtins.bool, jsii.get(self, "isImport"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> typing.Optional[ResourceNode]:
        '''Reference to the L2 Resource that wraps this L1 CfnResource if it is wrapped.'''
        return typing.cast(typing.Optional[ResourceNode], jsii.get(self, "resource"))


class Dependency(
    Edge,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.Dependency",
):
    '''Dependency edge class defines CloudFormation dependency between resources.'''

    def __init__(self, props: ITypedEdgeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b65e8bb5d20af3164b6f30a6041e75dd67bf4459b9ad42e5e0f89bdd222d9d5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isDependency")
    @builtins.classmethod
    def is_dependency(cls, edge: Edge) -> builtins.bool:
        '''Indicates if given edge is a {@link Dependency} edge.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d167b14ecbeb67ac4b1a6c043c252357c546c9547e34e16790486d5c3af3d7)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isDependency", [edge]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''Edge prefix to denote dependency edge.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))


@jsii.interface(jsii_type="@aws/pdk.cdk_graph.INestedStackNodeProps")
class INestedStackNodeProps(IStackNodeProps, typing_extensions.Protocol):
    '''{@link NestedStackNode} props.'''

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> StackNode:
        '''Parent stack.'''
        ...


class _INestedStackNodePropsProxy(
    jsii.proxy_for(IStackNodeProps), # type: ignore[misc]
):
    '''{@link NestedStackNode} props.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.cdk_graph.INestedStackNodeProps"

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> StackNode:
        '''Parent stack.'''
        return typing.cast(StackNode, jsii.get(self, "parentStack"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INestedStackNodeProps).__jsii_proxy_class__ = lambda : _INestedStackNodePropsProxy


class ImportReference(
    Reference,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.ImportReference",
):
    '''Import reference defines **Fn::ImportValue** type reference edge.'''

    def __init__(self, props: ITypedEdgeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7edb5a82fb61befeb79e66c62e040ff745030e56e0dd96603ace0e65a10fb4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isImport")
    @builtins.classmethod
    def is_import(cls, edge: Edge) -> builtins.bool:
        '''Indicates if edge is **Fn::ImportValue** based {@link Reference}.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3482a0317339fc528f400ec4d3f9c3ccd3d939717d7d14b65c42980ab58ef215)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isImport", [edge]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''Edge prefix to denote **Fn::ImportValue** type reference edge.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))


class NestedStackNode(
    StackNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph.NestedStackNode",
):
    '''NestedStackNode defines a cdk NestedStack.'''

    def __init__(self, props: INestedStackNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc0faa1c6cfb7796d63bbd9dce0942ce3cbf8a967d018e9240d931692a84bf2)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isNestedStackNode")
    @builtins.classmethod
    def is_nested_stack_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link NestedStackNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32704960f35e4de554dbca2c323ce08f077b03f68d20936f55c2261ad3950394)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isNestedStackNode", [node]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, new_parent: Node) -> None:
        '''Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        :param new_parent: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81880c6c6fcb604e9ac027a3ce7db676ace1a0366d92a6bfc881cadb8cc7bfba)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [new_parent]))

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> typing.Optional[StackNode]:
        '''Get parent stack of this nested stack.'''
        return typing.cast(typing.Optional[StackNode], jsii.get(self, "parentStack"))


__all__ = [
    "AppNode",
    "AttributeReference",
    "BaseEntity",
    "CdkConstructIds",
    "CdkGraph",
    "CdkGraphArtifact",
    "CdkGraphArtifacts",
    "CdkGraphContext",
    "CfnAttributesEnum",
    "CfnResourceNode",
    "ConstructInfo",
    "ConstructInfoFqnEnum",
    "Dependency",
    "Edge",
    "EdgeDirectionEnum",
    "EdgeTypeEnum",
    "FilterPreset",
    "FilterStrategy",
    "FilterValue",
    "Filters",
    "FlagEnum",
    "IAppNodeProps",
    "IAttributeReferenceProps",
    "IBaseEntityDataProps",
    "IBaseEntityProps",
    "ICdkGraphPlugin",
    "ICdkGraphProps",
    "ICfnResourceNodeProps",
    "IEdgePredicate",
    "IEdgeProps",
    "IFilter",
    "IFilterFocusCallback",
    "IFindEdgeOptions",
    "IFindNodeOptions",
    "IGraphFilter",
    "IGraphFilterPlan",
    "IGraphFilterPlanFocusConfig",
    "IGraphPluginBindCallback",
    "IGraphReportCallback",
    "IGraphStoreFilter",
    "IGraphSynthesizeCallback",
    "IGraphVisitorCallback",
    "INestedStackNodeProps",
    "INodePredicate",
    "INodeProps",
    "IOutputNodeProps",
    "IParameterNodeProps",
    "IReferenceProps",
    "IResourceNodeProps",
    "ISerializableEdge",
    "ISerializableEntity",
    "ISerializableGraphStore",
    "ISerializableNode",
    "IStackNodeProps",
    "IStoreCounts",
    "ITypedEdgeProps",
    "ITypedNodeProps",
    "ImportReference",
    "InferredNodeProps",
    "MetadataTypeEnum",
    "NestedStackNode",
    "Node",
    "NodeTypeEnum",
    "OutputNode",
    "ParameterNode",
    "PlainObject",
    "Reference",
    "ReferenceTypeEnum",
    "ResourceNode",
    "RootNode",
    "SGEdge",
    "SGEntity",
    "SGGraphStore",
    "SGNode",
    "SGUnresolvedReference",
    "StackNode",
    "StageNode",
    "Store",
]

publication.publish()

def _typecheckingstub__94bbd0d21e41f3cace54433390a25a1906e561e4eb7434f9283e50733df3fa53(
    root: _constructs_77d1e7e8.Construct,
    *,
    plugins: typing.Optional[typing.Sequence[ICdkGraphPlugin]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc21baecc84529dfbcbca164ba64f57611cf25ebb446fff90b877a66752278bf(
    *,
    filename: builtins.str,
    filepath: builtins.str,
    id: builtins.str,
    source: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97bea2b98e38f7a897ff5336a87aa3f81c8589f06c9e3fe55e541d1f9a3670bd(
    store: Store,
    outdir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9953dcded2bbb491c95bca34b0f508dcfa935a755aa4814abadc8489e0543aad(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54dfa2a44dec1f2462e39277d3fbab1ab5d882e5a05f20c1f1ef3c3cc6a473dd(
    filename: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e89bf27595703961827418a329025c23226a17ea261d44547cda6dcf4a50535(
    source: typing.Union[CdkGraph, ICdkGraphPlugin],
    id: builtins.str,
    filepath: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c296b043fd77e0a3b1655b2edcdaf6cba3c883b46fe45ffdc32105a5939c63a(
    source: typing.Union[CdkGraph, ICdkGraphPlugin],
    id: builtins.str,
    filename: builtins.str,
    data: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b6691c3201754d126a70b5463170fdaa907dfd5f96861451435fb1b66660d1(
    *,
    fqn: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd53d6836daf3be3c9730c0e1d468bc86571ff2a7533b7b1a218193cc86eed9b(
    *,
    regex: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0553f4b6eecb3118ee61590f5ccf76d43efc79b646aac3f499a8687d3813ff8b(
    cfn_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7002b0b10ad95a3a17090521d317871cf7b8c2e6674ef7f259c9743d41dee716(
    node_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb056cc26114d494350e156c1d3c3dafd918e6d3def382d2b8e1540faf16419(
    cfn_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e77b9617bf2aaf8aa68b370f5fd924cd9bd3487ae168eb5f47bec27f4684e4(
    node_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f059272dd0f0e79169ae1f32881cd7bcebae5f30dca3cbf15dce74f466ea12c(
    cluster_types: typing.Optional[typing.Sequence[NodeTypeEnum]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c377c780608bb7f3819c6d9512dc6f915256a98cb0e48b92875e39bafdd6a19(
    store: Store,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6754d39affa07fc839bab41660ae78c4853110297d33b48e2ca93e44055003c2(
    value: IGraphPluginBindCallback,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66990c34d4964902327a0f145d5058d1303c7f1fc82cd74214c85867aaf5a010(
    value: typing.Optional[IGraphVisitorCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65033b5ace6f019d80b4c2eff14e6a6858258160ac2ab689bf40f674dc7bb150(
    value: typing.Optional[IGraphReportCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471f0d2243469429351b860306f51981d6ef04540bf0038199d0c7e113d31971(
    value: typing.Optional[IGraphSynthesizeCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e23c07244128808dcb67636858a881d33e9bb5cc2bc40fe660715ca7f043f6(
    *,
    plugins: typing.Optional[typing.Sequence[ICdkGraphPlugin]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b475e9f95e493d62540af568e2b2b73449d41daf4cb307704df1b1f76b18347f(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafc31b18e2f14337cdcfdad4cb53e7e09fd03f4dcf1a0b37bab9058bdbd0d9b(
    *,
    graph: typing.Optional[typing.Union[IGraphFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    store: typing.Optional[IGraphStoreFilter] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e19f3644e37f7bee1a25e7fe7b884d11cc83b52213d72556b8c9216f8c5a117(
    store: Store,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2680bfc6423ea330cc468ae99519e650842fbc9c9ef26efed33deac72772cd95(
    value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a6cf9f569b7f84aa0163c4214fedf0650fc58c17dd5a2ca3a29fd1d979db56(
    value: typing.Optional[IEdgePredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c85a4b6a6cabb74b3c89edb5399297e514c45120fa25848232c1701ca19efd9(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b984008ef441cf0392bfe783a92a0c278d00c0bed3b65dff65e6c69e3b09eb3(
    value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28d466574c532332875bae1dfc756917c68254d8da881e9baad25d4fad7a4b2(
    value: typing.Optional[INodePredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caecaae2e9c8f32f3cf904d6949c9d2860cf03a21f2926251bf6205f6828e66(
    *,
    all_nodes: typing.Optional[builtins.bool] = None,
    edge: typing.Optional[IEdgePredicate] = None,
    inverse: typing.Optional[builtins.bool] = None,
    node: typing.Optional[INodePredicate] = None,
    strategy: typing.Optional[FilterStrategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20a0c44dfd25acb2f1bb600625504fa235bfd399bc43f627258f06d5673ffd6(
    *,
    all_nodes: typing.Optional[builtins.bool] = None,
    filters: typing.Optional[typing.Sequence[typing.Union[IFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    focus: typing.Optional[typing.Union[IGraphFilterPlanFocusConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    order: typing.Optional[_constructs_77d1e7e8.ConstructOrder] = None,
    preset: typing.Optional[FilterPreset] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c849737186526425fae15475d82f60020493fc7708cf91f9ce7ebd99ef1dbef5(
    *,
    filter: IFilterFocusCallback,
    no_hoist: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62d46db6e5a4ac2fe96fbe74b8356df6dec151c554b917749694744c78376ee(
    store: Store,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534e1a47a1685555f3e9115b1d5894e1ed342064598ac6c56dfff7ce4ce86288(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57d42c921f696a1e699387c3bc6a85c96a3961090be642e132494056271895e(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d73d18b936d180fe819e73e1051d2d3303b710ec5b7bb170fb8c5cc71b9b25(
    *,
    edges: typing.Sequence[typing.Union[SGEdge, typing.Dict[builtins.str, typing.Any]]],
    tree: typing.Union[SGNode, typing.Dict[builtins.str, typing.Any]],
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4213b110238dd63624e961e064c18e94c85cd54fbb39ce98592eeec8be6ecfc8(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: builtins.str,
    node_type: NodeTypeEnum,
    path: builtins.str,
    cfn_type: typing.Optional[builtins.str] = None,
    children: typing.Optional[typing.Mapping[builtins.str, typing.Union[SGNode, typing.Dict[builtins.str, typing.Any]]]] = None,
    construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    edges: typing.Optional[typing.Sequence[builtins.str]] = None,
    logical_id: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    stack: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa7431867434a2137e5846e44d85951458fff9bfec89b6d18baf695ccac1152(
    *,
    reference_type: ReferenceTypeEnum,
    source: builtins.str,
    target: builtins.str,
    value: typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ea6e00aa63b42bbe0309faca00f3f2c33d792a7f545356abb532ec5104139e(
    allow_destructive_mutations: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8c18b23d089868cb67226ca256b4cd10e9a7ca155fc7fe7309f3dbd5acc515(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08df7ce71eba51d6b30e1165fd1ab8f2c1147aabef5307492d804d8b07a75e0(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6bf01f1892100d80d0239da16617fdb0103a713554a7ba408519ad30450a0b(
    stack: StackNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088bfd5b6716f6f522b208805a39d18f01551b2949404fd8881c389f1ec71250(
    stage: StageNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f83929500aaef9ce0301bdba7aef03afbc068ca7095661cac48b149311bb4ed(
    allow_destructive_mutations: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf5980e2a4a5a92457cdb1dc8d112425f98ee7ba06b38d9e4a02a1883698570(
    stack: StackNode,
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45900ff0bb2bf1bd5a21faaf7123309f7c60287f797678df38c5f93fbef97282(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a343ed5216c7ef2bab0990b5bdf95578baa1b6177b7d4ab9c380cbf53ec5e75f(
    stack: StackNode,
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310fbedcaec37e662e2ed916f8b1c1018e1f6073e799b9196f401f39fba043d7(
    uid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab611670597ab4204704ecf8628bb796f88e048d01e42a8e5dce89b9e2d70a84(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fbfc38993abde01b2db38aa6cc9edbf45adf130d09f6899c303a187168e023f(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830ba15764b106ae5f4d556295109e29d4d257cc27c20c59e01cc997c2f2eef0(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd66f46b6709793fc905605f4bc82c3dc913b19a1315eb0e7e4e1b8f1552cc01(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c61747d401d86dfa5347ad8bc919fd049739ed2dfdf99fd1f1dbad7c99b4520(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7fbd2c49f36932ad82b78557f77bdd66ea5ff0cf861a1d2193bcf8ec067c90(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8c984509a82dcce046ddc465440eb4aaafc4c90c3159e0367b2842d416b12f(
    arn_token: builtins.str,
    resource: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0147cd2865c56325149b8ced263add8c62182a44f2d4dac4516d9af216c12e(
    stack: StackNode,
    logical_id: builtins.str,
    resource: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daeb695a45aac73f4be0d8c6ef31e5368bd9d911f28d037a99949396c77fe6b0(
    props: IBaseEntityProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6dba75c8541a9883f96e96f61d9fd09b00357b6f7ea584b0e266b95778c3b0(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223ed34d4f83c84c2bc1a76467cd3a313f8bef582eb08e037082049da0925e65(
    flag: FlagEnum,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef4a8615be9f9211703124ffe8024c2484ae4052765e3d09fff5a2ffd451568(
    metadata_type: builtins.str,
    data: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e666f8316c06f165c0672e3604d1cd73a700f5adbdc3a01becbdeec5b0ecba3(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e6b0e95faf9def98436116c7023e5be038f5b25b9cf74d27ce7454257d0e4e(
    data: IBaseEntityDataProps,
    overwrite: typing.Optional[builtins.bool] = None,
    apply_flags: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fcde4ea0e044c357a7302988f27de1593097203b5e0331177826e455ffecba(
    metadata_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062235bde2341056bb4308ef25c016a70b5850ff85396e53689d093e86347668(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7323868bcc859eef95d19d417971746f17b6acdcc6a601a29cdd45f3e64d6c24(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f039381b352ad4d492533c6b8109f7f2081cf1f56ba451e127a94ca3043ce1(
    key: builtins.str,
    value: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7588896203296569a3d61e4ecec20db9f6a4a1c8cb1d98c386c1daa03fa093c8(
    flag: FlagEnum,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796c96046119f43257244800d8c8af882de4ae32d7420019b36820128dab8ed9(
    metadata_type: builtins.str,
    data: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87398f6b45a668f7d65aced530383298bc5c0c8a043b7e9262cf69eaba6d759(
    key: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62ae658852843297cb8f7a467aca6902551f3a9378113b105aa40e03c0072dc(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83734012a451f19d48936f35f4e3f38f32eecc4503b43641936621e4b2c147dc(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f725d5a70a6b7fe6fad050e71509d865870f4bd635b2cc6eac66438d2c9e096(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab6ab7e189b4330415a37a51ebd37978c8189cccc8412bf611324161e2ab6fd(
    props: IEdgeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5be3398beba49f9b3c52ea752d3528c05126b5c6515c60628d6535b73b42ef(
    chain: typing.Sequence[typing.Any],
    predicate: IEdgePredicate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a5bc50eadc381e5b3d45537040fa59fd26417b346c447ed288f77c91fba922(
    chain: typing.Sequence[typing.Any],
    predicate: IEdgePredicate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d67b4580af0da089331ae3889959fb2c01ca12f7cc4b34171913880c83d4840(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed48f1605b531f8f7bdf9179be661069a4dc639e50a0c9dd6dec2a6d1ce884d(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93efbfbd1860bda9c89a23a6fee4cb6fa162c1b804b9add268f083e5e9c8bbc7(
    _strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0392d8cc408dec6d4139add0acba2e1d9352b669425b414740f5d5a3210d41aa(
    direction: EdgeDirectionEnum,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87226ff0c3d1a50dea3a4c07eae7b03252d68b4c40f2c7836cf1406c836218d1(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8def7b646c4b685dcedf3851f3994050ed501edf65e6e4a1bb597d42c396fcca(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af3d92f06eb65a1920d5855076e065bfb5aca635a999cf264b600b99c0464bd(
    value: typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b853dfee42346b9d862590c9d269c32ebbf386d00b4c6e8121c852dc25d2016(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec170afff8dfbb938ecb7c921ed87126e068e25e4b60b34a109a6272908d5b6c(
    value: typing.Optional[NodeTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0cc6c6fa4f8ee72758b7835a592762d1dca3de1ebf9c042fd0c08d8619f8360(
    value: typing.Optional[ReferenceTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e557d041c601e686c9d26ec6d21342360782f783d7a10da36018f0cae4554b6f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b6fe631ac472ee879910fc4468af7beb78a03ac84d0ebf328845d6f9cac165(
    value: typing.Optional[NodeTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24dec8cf2a8e099c6ba8c24f1a9fc263f2db157e7a1a7e1c6c479e4d7a312de(
    value: typing.Optional[NodeTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eacd87f06afeb956eb173d8f94120330de6d6edc0570bba958f7ab3265cc974(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    dependencies: typing.Sequence[builtins.str],
    unresolved_references: typing.Sequence[typing.Union[SGUnresolvedReference, typing.Dict[builtins.str, typing.Any]]],
    cfn_type: typing.Optional[builtins.str] = None,
    construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    logical_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c044f8a8f65047634c290bd30cb01706503d338e658a07d8284c48adf3b9bb(
    props: INodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d03f96f16f19869cd1c00de00e0584cafa103a93172080ed6f9598840a5e35(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198071812d0a9d0d8eff09cdb17512adeaafd2d8d2da0c52e29a53307cd7948e(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c235e130710ac7faa707502265f3b8555eba35f5c4835190fe4f3b280d29c753(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c8dbe0444fcc170522913b01ab01586841c9da4a3cc2e9e1b1bba829f28c7f(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91dc33cb071e4848ae1fed6f609d8197d7c8d7d9393d42470d7fa08d25f1f86(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1118f8a31090d57684b9544621ad692d5ff87628fd069bc14103fb9ba9bbb16b(
    predicate: INodePredicate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b847a14ccf7e62529c3d009411401ce63b374b1d763ce613bbd8f3dedae9e6(
    options: typing.Optional[IFindNodeOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb006539eb07f788404c73f2e37e4eb77b4398a89e3ddd7c70e4d1dc8803645(
    options: typing.Optional[IFindEdgeOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c577eb6e9b7988d124c694764e1ee423bf2f3c4ff5afebfbe4a9d91c3bf99046(
    predicate: INodePredicate,
    max: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c579449b394221e0c6139c7a822c328e9c33f8755165ca213d23681a51ffe486(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b870f9738220cb6754e6a2e63a7df3507848a71faf6425c672928318f907d5b0(
    predicate: IEdgePredicate,
    reverse: typing.Optional[builtins.bool] = None,
    follow: typing.Optional[builtins.bool] = None,
    direct: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ddc4f2ab306bda5958b7a56113ea29778d15ef49859515aab9ea74cdde4e94(
    predicate: IEdgePredicate,
    reverse: typing.Optional[builtins.bool] = None,
    follow: typing.Optional[builtins.bool] = None,
    direct: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a75b45f39d99968c01e0198aab540b24e269ad0844175ec82ef7313ea5ead7(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb491e2fd9649eb3cd30f698b6b21fabd672c09c5002b1f813d499bf903d809(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f8b0b569b50b22beceaef1fa83a27acdaeb136a852be22a090c2f4afe32157(
    reverse: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdf30bcfa12b1fadefa7d26aad527efdf11e417ed0d6d505ba3e2ec4652db07(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3426039160d35ea7a26817863b092ac89c4108d0c754b57b153ba6bce552ba0c(
    ancestor: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2735ea376e9de6b6fddaeda923cc84656049413de27ccabbbcf6deb45c17ccb4(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa25b0a3b6b70a902bf8e32f8c5811e617446b61b567c9fb6381da7da8828ee4(
    ancestor: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ed1e09ff81256afc84f16f40ddbd7eeee4c7cba3fd29a49dd6cd3f19c7d5d4(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49846287b799fd3c70091023007e33f5051245b089f9256467c5962233a3e433(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f7329b5432b02654e1ad703695942a6d28fa2dd8a07f809763f62ac0c64371(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75733325f56e106350fa1ee95e8d307c7e0dcbee94064b581a6e86beb1683680(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6897ad4601f6abf9e6b03c91ff8efbcd2af93968abc441fdf67d35839b7c2722(
    link: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbeafcd0c1ad6249dd3c40949962bcbecc8572ecd38794c4f7c78893b195e275(
    link: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed71596e37a35e0636fc38dfb3007da46414fc4b15359b0d552f61fbca643de(
    props: IOutputNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e9eb1bf349e1d4018b9586b0cc274ff2a5f2feb16b8037573683d1965d614ec(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3921680ac1dd8fc422fb68fdea498275bfd2a7c5019599295dddfcfc23e89fa3(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6af02cc2fc74978e9626fb5844f8e8a8be13c6614d1918de991cb6d2972f2d(
    props: IParameterNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a28c720f2c3aeda10f04ad7d97ffb429a777a49c9baba6b10336454c15f0ed(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1184e3e97f69dba27fc8b6b4f7e67d849e006f7d47b489659cfd0f89609c434b(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8badf88f3abd3427e44f2b4990b8e53878f04099a6cbb3fa2be81bb8801fad43(
    props: IReferenceProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f900ad592251e3da18f561007745ac3afb09f9e17b8f0e5b0f419aa5c8a1ed6d(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc467db16516a30e91fc3b1d10146caffbd78b3dee110b4b32b32778bc76ad3(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab7fbb9f68d49cf9fe9ceac18872f881e0ac4324d2343b65ec4e4046c88ccee(
    props: IResourceNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f313bdc83492a1f712a614426e66f0985d89572180f2748e3dcefb78200e4ae(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b495d95ea2d6027725ebd56226b4ccd6e1fa8c4909c899f1faa40e8ed42673(
    cfn_resource: typing.Optional[CfnResourceNode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac7612e5e5be5d7c2563f557ac98d88197511cd31fc0456e4bb744506bd602a(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5346d075b2479f66d7464928a4c7fff8b9da2ecb894a024e207d7b52c17354(
    store: Store,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abac9207872e959161e02ce2bfbce4e67d05297979f2bf1a3197b0335a98f44(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4cf7ad982505f29a1bf19ec1541e7cc26dfe10356c04dd39a8673b5aed191e8(
    options: typing.Optional[IFindNodeOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a329370e0d7c7d33fd9ff5886d120a7c63f73a23d3eb3dd70289b635861d87(
    _ancestor: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a4bf78315f69c74c892bfceb9bc6d044480fd59997260eba075494da3869dc(
    _strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108861ca325ad24ba3f68920053fd24a97a9dddbe771888244077e7cb3b76f5f(
    _new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddff8d68af5cd7268e6d71f570829df122147a7ff8555327598fb2d72e7de9d2(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    direction: EdgeDirectionEnum,
    edge_type: EdgeTypeEnum,
    source: builtins.str,
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214334fddbdfdb5b8890a5f1ec4ce71e4bea33db3891357cc6c4eee098f5f85d(
    props: IStackNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3c080ef567e757a6948e4b4ae64b503a64a83fb0b3b7f661e76b4e2bafb66b(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f469c6d1d0c870c1217e56aad870498a3c8c74ff1037dd2f1dfab1dcdf237d59(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01390d8fbab550ab9b7fe0be9afdd5fef16023fa253b812217486965e56e355d(
    node: OutputNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfd77363e6f3be11a9ae3ffd40786090c8864d25f3b5d43800ae52948c8d6df(
    node: ParameterNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08efe87ca0fc942e4ef45eceb73d2a81d2f1812a96b06e305b6df3ecf1f33e4b(
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22206334ffedc950168a664e68843a19e115901e62ad76cde0441d79be17dcd4(
    parameter_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c101a514d513f496bf720133140b42a68fddf55ffdbd103dd376bf02e4975a1(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c611df42668de673d25b358a896cb95435ebac6563684d743d3f55612617d0(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50bb3b84d4d5a478e9c2aa0108688841ea46503495adce419a5f634ef490ad0(
    node: OutputNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed30ded726ea140c7007c184f19287732d397de06409c85f21639e7fee97666(
    node: ParameterNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541e8c0f1a72250fc8ea6113c2bf61646d098ddf01a3da7d2f26bb247c93a445(
    props: ITypedNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38955797a4d22cb4fc20b63df6ce512f5214f60df97e4b045dd068dd854a14c2(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0036ab7a7ade621459078354b0ddf4ba9f118d4897c466c68e589a5e7e256c(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0060c1529a42c00f8c4379a73a4d82acc5e250b4b89ef23500f83fd55084f9fc(
    stack: StackNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c873622490206d4a1e2aeaa397352e0853716b06269c11d15e9acfb1820a24(
    stack: StackNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739f1561565f269abf8ddf1001e5031738d6dd497c13cfe3995d4d54ccbcfb65(
    props: IAppNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bd7da5daf2def243349d3a975bb0b6078d2a54fe77a1ac897c50face6822c9(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd65695412c23b057af4c788298676d03d47a64c95c1fe14efa6164f586b66a(
    props: IAttributeReferenceProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822d80f3a40b12eed417099ec2b64ac06836e0dab84489d7a10f28ce571dfed7(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b4909167c4ec814e31cb80d43be1227b68bf3ceab65648e684dbdd8aa8bcfc(
    props: ICfnResourceNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bc6c0df2c621db05595566d295936c3898490ecfac1a0e358994b11d9e26de(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6864031b0074d0123ff669d9572a89e0e1f8c26afbcf44b0200ea8cac5edd96(
    resource: ResourceNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862784a149b27e7deb929fe15991070c67e4fa16d70c9e63267a3a60b29e72d7(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b65e8bb5d20af3164b6f30a6041e75dd67bf4459b9ad42e5e0f89bdd222d9d5(
    props: ITypedEdgeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d167b14ecbeb67ac4b1a6c043c252357c546c9547e34e16790486d5c3af3d7(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7edb5a82fb61befeb79e66c62e040ff745030e56e0dd96603ace0e65a10fb4(
    props: ITypedEdgeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3482a0317339fc528f400ec4d3f9c3ccd3d939717d7d14b65c42980ab58ef215(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc0faa1c6cfb7796d63bbd9dce0942ce3cbf8a967d018e9240d931692a84bf2(
    props: INestedStackNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32704960f35e4de554dbca2c323ce08f077b03f68d20936f55c2261ad3950394(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81880c6c6fcb604e9ac027a3ce7db676ace1a0366d92a6bfc881cadb8cc7bfba(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass
