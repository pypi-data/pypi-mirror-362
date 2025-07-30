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
    ICdkGraphPlugin as _ICdkGraphPlugin_b5ef2d02,
    IGraphPluginBindCallback as _IGraphPluginBindCallback_58b6edd3,
    IGraphReportCallback as _IGraphReportCallback_858cc871,
)


@jsii.implements(_ICdkGraphPlugin_b5ef2d02)
class CdkGraphThreatComposerPlugin(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.cdk_graph_plugin_threat_composer.CdkGraphThreatComposerPlugin",
):
    '''CdkGraphThreatComposerPlugin is a {@link ICdkGraphPluginCdkGraph Plugin} implementation for generating Threat Composer threat models.

    :see: https://github.com/awslabs/threat-composer
    '''

    def __init__(
        self,
        *,
        application_details: typing.Optional[typing.Union["ThreatComposerApplicationDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param application_details: Details about the application to include in the threat model.
        '''
        options = CdkGraphThreatComposerPluginOptions(
            application_details=application_details
        )

        jsii.create(self.__class__, self, [options])

    @jsii.python.classproperty
    @jsii.member(jsii_name="ID")
    def ID(cls) -> builtins.str:
        '''Fixed ID of the threat-composer plugin.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION")
    def VERSION(cls) -> builtins.str:
        '''Curent semantic version of the threat-composer plugin.'''
        return typing.cast(builtins.str, jsii.sget(cls, "VERSION"))

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
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]).

        :inheritdoc: true
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="threatModelArtifact")
    def threat_model_artifact(self) -> typing.Optional[_CdkGraphArtifact_0059de6d]:
        '''Retrieve the threat model artifact.'''
        return typing.cast(typing.Optional[_CdkGraphArtifact_0059de6d], jsii.get(self, "threatModelArtifact"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__004df50936b7e9d66b1ed9050f1929103969ae05c656b62aa74d1e4e090c0bb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__035069cd2d747ed069143fb7dcd15cc668561fda5e1131e69067e8390c369b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "report", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph_plugin_threat_composer.CdkGraphThreatComposerPluginOptions",
    jsii_struct_bases=[],
    name_mapping={"application_details": "applicationDetails"},
)
class CdkGraphThreatComposerPluginOptions:
    def __init__(
        self,
        *,
        application_details: typing.Optional[typing.Union["ThreatComposerApplicationDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Options for the Threat Composer CDK Graph plugin.

        :param application_details: Details about the application to include in the threat model.
        '''
        if isinstance(application_details, dict):
            application_details = ThreatComposerApplicationDetails(**application_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639c16f872bbcd9a96470baacb14439baa1a77a4b72bca89f8f99db36b96223a)
            check_type(argname="argument application_details", value=application_details, expected_type=type_hints["application_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_details is not None:
            self._values["application_details"] = application_details

    @builtins.property
    def application_details(
        self,
    ) -> typing.Optional["ThreatComposerApplicationDetails"]:
        '''Details about the application to include in the threat model.'''
        result = self._values.get("application_details")
        return typing.cast(typing.Optional["ThreatComposerApplicationDetails"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkGraphThreatComposerPluginOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.cdk_graph_plugin_threat_composer.ThreatComposerApplicationDetails",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name"},
)
class ThreatComposerApplicationDetails:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Details about the application to include in the threat model.

        :param description: A description of the application.
        :param name: The name of the application. Default: "My Application"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9303e5c0974005851dfe891098a48818ab06b87628678818de66c1e67bea662)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the application.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :default: "My Application"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThreatComposerApplicationDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CdkGraphThreatComposerPlugin",
    "CdkGraphThreatComposerPluginOptions",
    "ThreatComposerApplicationDetails",
]

publication.publish()

def _typecheckingstub__004df50936b7e9d66b1ed9050f1929103969ae05c656b62aa74d1e4e090c0bb1(
    value: _IGraphPluginBindCallback_58b6edd3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035069cd2d747ed069143fb7dcd15cc668561fda5e1131e69067e8390c369b5a(
    value: typing.Optional[_IGraphReportCallback_858cc871],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639c16f872bbcd9a96470baacb14439baa1a77a4b72bca89f8f99db36b96223a(
    *,
    application_details: typing.Optional[typing.Union[ThreatComposerApplicationDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9303e5c0974005851dfe891098a48818ab06b87628678818de66c1e67bea662(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
