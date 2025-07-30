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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.cx_api as _aws_cdk_cx_api_ceddda9d
import cdk_nag as _cdk_nag_263d9695
import constructs as _constructs_77d1e7e8


class AwsPrototypingChecks(
    _cdk_nag_263d9695.NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.pdk_nag.AwsPrototypingChecks",
):
    '''Check best practices for prototypes.'''

    def __init__(
        self,
        *,
        additional_loggers: typing.Optional[typing.Sequence[_cdk_nag_263d9695.INagLogger]] = None,
        log_ignores: typing.Optional[builtins.bool] = None,
        report_formats: typing.Optional[typing.Sequence[_cdk_nag_263d9695.NagReportFormat]] = None,
        reports: typing.Optional[builtins.bool] = None,
        suppression_ignore_condition: typing.Optional[_cdk_nag_263d9695.INagSuppressionIgnore] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param additional_loggers: Additional NagLoggers for logging rule validation outputs.
        :param log_ignores: Whether or not to log suppressed rule violations as informational messages (default: false).
        :param report_formats: If reports are enabled, the output formats of compliance reports in the App's output directory (default: only CSV).
        :param reports: Whether or not to generate compliance reports for applied Stacks in the App's output directory (default: true).
        :param suppression_ignore_condition: Conditionally prevent rules from being suppressed (default: no user provided condition).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = _cdk_nag_263d9695.NagPackProps(
            additional_loggers=additional_loggers,
            log_ignores=log_ignores,
            report_formats=report_formats,
            reports=reports,
            suppression_ignore_condition=suppression_ignore_condition,
            verbose=verbose,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''Check if CfnResource and apply rules.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8aa12b05f34ae8c5f2ba1473e38e19d866fb8f4b520412005d0fe346b7fb8e7)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@aws/pdk.pdk_nag.ExtendedNagResult",
    jsii_struct_bases=[],
    name_mapping={
        "compliance": "compliance",
        "nag_pack_name": "nagPackName",
        "resource": "resource",
        "rule_explanation": "ruleExplanation",
        "rule_id": "ruleId",
        "rule_info": "ruleInfo",
        "rule_level": "ruleLevel",
        "rule_original_name": "ruleOriginalName",
        "error_message": "errorMessage",
        "finding_id": "findingId",
        "suppression_reason": "suppressionReason",
    },
)
class ExtendedNagResult:
    def __init__(
        self,
        *,
        compliance: "NagResultCompliance",
        nag_pack_name: builtins.str,
        resource: _aws_cdk_ceddda9d.CfnResource,
        rule_explanation: builtins.str,
        rule_id: builtins.str,
        rule_info: builtins.str,
        rule_level: _cdk_nag_263d9695.NagMessageLevel,
        rule_original_name: builtins.str,
        error_message: typing.Optional[builtins.str] = None,
        finding_id: typing.Optional[builtins.str] = None,
        suppression_reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Represents the result of applying a CDK Nag rule to a resource.

        :param compliance: Compliance status of the rule against the resource.
        :param nag_pack_name: The name of the nag pack this rule is from.
        :param resource: The resource the rule was applied to.
        :param rule_explanation: Why the rule exists.
        :param rule_id: The ID of the rule in this nag pack.
        :param rule_info: Why the rule was triggered.
        :param rule_level: The severity level of the rule.
        :param rule_original_name: The original name of the rule (regardless of nag pack).
        :param error_message: The error that was thrown, only set for error results.
        :param finding_id: The finding that was checked, only set for non-compliant results.
        :param suppression_reason: The reason the rule was suppressed, if any.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8449c5c2cfffdf3f73061d623bdbfb9a6f8c1a04846ab12f3c08d754a61977e5)
            check_type(argname="argument compliance", value=compliance, expected_type=type_hints["compliance"])
            check_type(argname="argument nag_pack_name", value=nag_pack_name, expected_type=type_hints["nag_pack_name"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument rule_explanation", value=rule_explanation, expected_type=type_hints["rule_explanation"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument rule_info", value=rule_info, expected_type=type_hints["rule_info"])
            check_type(argname="argument rule_level", value=rule_level, expected_type=type_hints["rule_level"])
            check_type(argname="argument rule_original_name", value=rule_original_name, expected_type=type_hints["rule_original_name"])
            check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
            check_type(argname="argument finding_id", value=finding_id, expected_type=type_hints["finding_id"])
            check_type(argname="argument suppression_reason", value=suppression_reason, expected_type=type_hints["suppression_reason"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compliance": compliance,
            "nag_pack_name": nag_pack_name,
            "resource": resource,
            "rule_explanation": rule_explanation,
            "rule_id": rule_id,
            "rule_info": rule_info,
            "rule_level": rule_level,
            "rule_original_name": rule_original_name,
        }
        if error_message is not None:
            self._values["error_message"] = error_message
        if finding_id is not None:
            self._values["finding_id"] = finding_id
        if suppression_reason is not None:
            self._values["suppression_reason"] = suppression_reason

    @builtins.property
    def compliance(self) -> "NagResultCompliance":
        '''Compliance status of the rule against the resource.'''
        result = self._values.get("compliance")
        assert result is not None, "Required property 'compliance' is missing"
        return typing.cast("NagResultCompliance", result)

    @builtins.property
    def nag_pack_name(self) -> builtins.str:
        '''The name of the nag pack this rule is from.'''
        result = self._values.get("nag_pack_name")
        assert result is not None, "Required property 'nag_pack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource(self) -> _aws_cdk_ceddda9d.CfnResource:
        '''The resource the rule was applied to.'''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(_aws_cdk_ceddda9d.CfnResource, result)

    @builtins.property
    def rule_explanation(self) -> builtins.str:
        '''Why the rule exists.'''
        result = self._values.get("rule_explanation")
        assert result is not None, "Required property 'rule_explanation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_id(self) -> builtins.str:
        '''The ID of the rule in this nag pack.'''
        result = self._values.get("rule_id")
        assert result is not None, "Required property 'rule_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_info(self) -> builtins.str:
        '''Why the rule was triggered.'''
        result = self._values.get("rule_info")
        assert result is not None, "Required property 'rule_info' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_level(self) -> _cdk_nag_263d9695.NagMessageLevel:
        '''The severity level of the rule.'''
        result = self._values.get("rule_level")
        assert result is not None, "Required property 'rule_level' is missing"
        return typing.cast(_cdk_nag_263d9695.NagMessageLevel, result)

    @builtins.property
    def rule_original_name(self) -> builtins.str:
        '''The original name of the rule (regardless of nag pack).'''
        result = self._values.get("rule_original_name")
        assert result is not None, "Required property 'rule_original_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_message(self) -> typing.Optional[builtins.str]:
        '''The error that was thrown, only set for error results.'''
        result = self._values.get("error_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def finding_id(self) -> typing.Optional[builtins.str]:
        '''The finding that was checked, only set for non-compliant results.'''
        result = self._values.get("finding_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suppression_reason(self) -> typing.Optional[builtins.str]:
        '''The reason the rule was suppressed, if any.'''
        result = self._values.get("suppression_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExtendedNagResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.pdk_nag.Message",
    jsii_struct_bases=[],
    name_mapping={
        "message_description": "messageDescription",
        "message_type": "messageType",
    },
)
class Message:
    def __init__(
        self,
        *,
        message_description: builtins.str,
        message_type: builtins.str,
    ) -> None:
        '''Message instance.

        :param message_description: Message description.
        :param message_type: Message type as returned from cdk-nag.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c93182a4922d7452f57be229082f9c3d5dd9ca71941154fcdac4df76b43c528)
            check_type(argname="argument message_description", value=message_description, expected_type=type_hints["message_description"])
            check_type(argname="argument message_type", value=message_type, expected_type=type_hints["message_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message_description": message_description,
            "message_type": message_type,
        }

    @builtins.property
    def message_description(self) -> builtins.str:
        '''Message description.'''
        result = self._values.get("message_description")
        assert result is not None, "Required property 'message_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_type(self) -> builtins.str:
        '''Message type as returned from cdk-nag.'''
        result = self._values.get("message_type")
        assert result is not None, "Required property 'message_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Message(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.pdk_nag.NagResult",
    jsii_struct_bases=[],
    name_mapping={"messages": "messages", "resource": "resource"},
)
class NagResult:
    def __init__(
        self,
        *,
        messages: typing.Sequence[typing.Union[Message, typing.Dict[builtins.str, typing.Any]]],
        resource: builtins.str,
    ) -> None:
        '''Nag result.

        :param messages: List of messages.
        :param resource: Resource which triggered the message.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f28e99b6450320d049052294b8732c9914971212aecba15ae4e76747213125)
            check_type(argname="argument messages", value=messages, expected_type=type_hints["messages"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "messages": messages,
            "resource": resource,
        }

    @builtins.property
    def messages(self) -> typing.List[Message]:
        '''List of messages.'''
        result = self._values.get("messages")
        assert result is not None, "Required property 'messages' is missing"
        return typing.cast(typing.List[Message], result)

    @builtins.property
    def resource(self) -> builtins.str:
        '''Resource which triggered the message.'''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NagResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws/pdk.pdk_nag.NagResultCompliance")
class NagResultCompliance(enum.Enum):
    '''Possible statuses for nag rules.'''

    COMPLIANT = "COMPLIANT"
    '''Resource complies with the rule.'''
    NON_COMPLIANT = "NON_COMPLIANT"
    '''Resource does not comply with the rule.'''
    NON_COMPLIANT_SUPPRESSED = "NON_COMPLIANT_SUPPRESSED"
    '''Resource does not comply with the rule, but the rule was suppressed.'''
    ERROR = "ERROR"
    '''An error occurred applying the rule.'''
    ERROR_SUPPRESSED = "ERROR_SUPPRESSED"
    '''An error occurred applying the rule, but the rule was suppressed.'''
    NOT_APPLICABLE = "NOT_APPLICABLE"
    '''The rule is not applicable to the resource.'''


class PDKNag(metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.pdk_nag.PDKNag"):
    '''Helper for create a Nag Enabled App.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addResourceSuppressionsByPathNoThrow")
    @builtins.classmethod
    def add_resource_suppressions_by_path_no_throw(
        cls,
        stack: _aws_cdk_ceddda9d.Stack,
        path: builtins.str,
        suppressions: typing.Sequence[typing.Union[_cdk_nag_263d9695.NagPackSuppression, typing.Dict[builtins.str, typing.Any]]],
        apply_to_children: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Wrapper around NagSuppressions which does not throw.

        :param stack: stack instance.
        :param path: resource path.
        :param suppressions: list of suppressions to apply.
        :param apply_to_children: whether to apply to children.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df4154748281a399576171b2f69c41577cb5a8b1ea4b026921fbf1e7feed914)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument suppressions", value=suppressions, expected_type=type_hints["suppressions"])
            check_type(argname="argument apply_to_children", value=apply_to_children, expected_type=type_hints["apply_to_children"])
        return typing.cast(None, jsii.sinvoke(cls, "addResourceSuppressionsByPathNoThrow", [stack, path, suppressions, apply_to_children]))

    @jsii.member(jsii_name="app")
    @builtins.classmethod
    def app(
        cls,
        *,
        fail_on_error: typing.Optional[builtins.bool] = None,
        fail_on_warning: typing.Optional[builtins.bool] = None,
        nag_packs: typing.Optional[typing.Sequence[_cdk_nag_263d9695.NagPack]] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        auto_synth: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        default_stack_synthesizer: typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer] = None,
        outdir: typing.Optional[builtins.str] = None,
        policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
        post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        tree_metadata: typing.Optional[builtins.bool] = None,
    ) -> "PDKNagApp":
        '''Returns an instance of an App with Nag enabled.

        :param fail_on_error: Determines whether any errors encountered should trigger a test failure. Default: false
        :param fail_on_warning: Determines whether any warnings encountered should trigger a test failure. Default: false
        :param nag_packs: Custom nag packs to execute. Default: DEFAULT_NAG_PACKS
        :param analytics_reporting: Include runtime versioning information in the Stacks of this app. Default: Value of 'aws:cdk:version-reporting' context key
        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param default_stack_synthesizer: The stack synthesizer to use by default for all Stacks in the App. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. Default: - A ``DefaultStackSynthesizer`` with default settings
        :param outdir: The output directory into which to emit synthesized artifacts. You should never need to set this value. By default, the value you pass to the CLI's ``--output`` flag will be used, and if you change it to a different directory the CLI will fail to pick up the generated Cloud Assembly. This property is intended for internal and testing use. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param policy_validation_beta1: Validation plugins to run after synthesis. Default: - no validation plugins
        :param post_cli_context: Additional context values for the application. Context provided here has precedence over context set by: - The CLI via --context - The ``context`` key in ``cdk.json`` - The ``AppProps.context`` property This property is recommended over the ``AppProps.context`` property since you can make final decision over which context value to take in your app. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        '''
        props = PDKNagAppProps(
            fail_on_error=fail_on_error,
            fail_on_warning=fail_on_warning,
            nag_packs=nag_packs,
            analytics_reporting=analytics_reporting,
            auto_synth=auto_synth,
            context=context,
            default_stack_synthesizer=default_stack_synthesizer,
            outdir=outdir,
            policy_validation_beta1=policy_validation_beta1,
            post_cli_context=post_cli_context,
            stack_traces=stack_traces,
            tree_metadata=tree_metadata,
        )

        return typing.cast("PDKNagApp", jsii.sinvoke(cls, "app", [props]))

    @jsii.member(jsii_name="getStackAccountRegex")
    @builtins.classmethod
    def get_stack_account_regex(cls, stack: _aws_cdk_ceddda9d.Stack) -> builtins.str:
        '''Returns a stack account regex.

        :param stack: stack instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9c7b8ca6e6cf7067508e077a349f6970a468d6f27683ecf2baab2767c4a24e6)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getStackAccountRegex", [stack]))

    @jsii.member(jsii_name="getStackPartitionRegex")
    @builtins.classmethod
    def get_stack_partition_regex(cls, stack: _aws_cdk_ceddda9d.Stack) -> builtins.str:
        '''Returns a stack partition regex.

        :param stack: stack instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa0bbf9e40945577406f43f4ea42623d4fe13e5e55279a3613263349deeea63)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getStackPartitionRegex", [stack]))

    @jsii.member(jsii_name="getStackPrefix")
    @builtins.classmethod
    def get_stack_prefix(cls, stack: _aws_cdk_ceddda9d.Stack) -> builtins.str:
        '''Returns a prefix comprising of a delimited set of Stack Ids.

        For example: StackA/NestedStackB/

        :param stack: stack instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3571ab007307dce3ff9ffc4cbe7060b3eb33d9a5019948d82aca2dd1edf04c18)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getStackPrefix", [stack]))

    @jsii.member(jsii_name="getStackRegionRegex")
    @builtins.classmethod
    def get_stack_region_regex(cls, stack: _aws_cdk_ceddda9d.Stack) -> builtins.str:
        '''Returns a stack region regex.

        :param stack: stack instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9f55608ad622f385b97d568c1b49a24059612e0fe4dde7d461d193d8779f26)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getStackRegionRegex", [stack]))


class PDKNagApp(
    _aws_cdk_ceddda9d.App,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.pdk_nag.PDKNagApp",
):
    '''
    :inheritDoc: true
    '''

    def __init__(
        self,
        *,
        fail_on_error: typing.Optional[builtins.bool] = None,
        fail_on_warning: typing.Optional[builtins.bool] = None,
        nag_packs: typing.Optional[typing.Sequence[_cdk_nag_263d9695.NagPack]] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        auto_synth: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        default_stack_synthesizer: typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer] = None,
        outdir: typing.Optional[builtins.str] = None,
        policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
        post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        tree_metadata: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param fail_on_error: Determines whether any errors encountered should trigger a test failure. Default: false
        :param fail_on_warning: Determines whether any warnings encountered should trigger a test failure. Default: false
        :param nag_packs: Custom nag packs to execute. Default: DEFAULT_NAG_PACKS
        :param analytics_reporting: Include runtime versioning information in the Stacks of this app. Default: Value of 'aws:cdk:version-reporting' context key
        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param default_stack_synthesizer: The stack synthesizer to use by default for all Stacks in the App. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. Default: - A ``DefaultStackSynthesizer`` with default settings
        :param outdir: The output directory into which to emit synthesized artifacts. You should never need to set this value. By default, the value you pass to the CLI's ``--output`` flag will be used, and if you change it to a different directory the CLI will fail to pick up the generated Cloud Assembly. This property is intended for internal and testing use. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param policy_validation_beta1: Validation plugins to run after synthesis. Default: - no validation plugins
        :param post_cli_context: Additional context values for the application. Context provided here has precedence over context set by: - The CLI via --context - The ``context`` key in ``cdk.json`` - The ``AppProps.context`` property This property is recommended over the ``AppProps.context`` property since you can make final decision over which context value to take in your app. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        '''
        props = PDKNagAppProps(
            fail_on_error=fail_on_error,
            fail_on_warning=fail_on_warning,
            nag_packs=nag_packs,
            analytics_reporting=analytics_reporting,
            auto_synth=auto_synth,
            context=context,
            default_stack_synthesizer=default_stack_synthesizer,
            outdir=outdir,
            policy_validation_beta1=policy_validation_beta1,
            post_cli_context=post_cli_context,
            stack_traces=stack_traces,
            tree_metadata=tree_metadata,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addExtendedNagResults")
    def add_extended_nag_results(self, *results: ExtendedNagResult) -> None:
        '''
        :param results: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2fcf25e53176b62e6528f199f19b5eb0ba7082819a349f5a61264769c40505e)
            check_type(argname="argument results", value=results, expected_type=typing.Tuple[type_hints["results"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addExtendedNagResults", [*results]))

    @jsii.member(jsii_name="addNagResult")
    def add_nag_result(
        self,
        *,
        messages: typing.Sequence[typing.Union[Message, typing.Dict[builtins.str, typing.Any]]],
        resource: builtins.str,
    ) -> None:
        '''
        :param messages: List of messages.
        :param resource: Resource which triggered the message.
        '''
        result = NagResult(messages=messages, resource=resource)

        return typing.cast(None, jsii.invoke(self, "addNagResult", [result]))

    @jsii.member(jsii_name="extendedNagResults")
    def extended_nag_results(self) -> typing.List[ExtendedNagResult]:
        '''Returns a list of ExtendedNagResult.

        Note: app.synth() must be called before this to retrieve results.
        '''
        return typing.cast(typing.List[ExtendedNagResult], jsii.invoke(self, "extendedNagResults", []))

    @jsii.member(jsii_name="nagResults")
    def nag_results(self) -> typing.List[NagResult]:
        '''Returns a list of NagResult.

        Note: app.synth() must be called before this to retrieve results.
        '''
        return typing.cast(typing.List[NagResult], jsii.invoke(self, "nagResults", []))

    @jsii.member(jsii_name="synth")
    def synth(
        self,
        *,
        force: typing.Optional[builtins.bool] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
        validate_on_synthesis: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_cx_api_ceddda9d.CloudAssembly:
        '''Synthesize this stage into a cloud assembly.

        Once an assembly has been synthesized, it cannot be modified. Subsequent
        calls will return the same assembly.

        :param force: Force a re-synth, even if the stage has already been synthesized. This is used by tests to allow for incremental verification of the output. Do not use in production. Default: false
        :param skip_validation: Should we skip construct validation. Default: - false
        :param validate_on_synthesis: Whether the stack should be validated after synthesis to check for error metadata. Default: - false
        '''
        options = _aws_cdk_ceddda9d.StageSynthesisOptions(
            force=force,
            skip_validation=skip_validation,
            validate_on_synthesis=validate_on_synthesis,
        )

        return typing.cast(_aws_cdk_cx_api_ceddda9d.CloudAssembly, jsii.invoke(self, "synth", [options]))

    @builtins.property
    @jsii.member(jsii_name="nagPacks")
    def nag_packs(self) -> typing.List[_cdk_nag_263d9695.NagPack]:
        return typing.cast(typing.List[_cdk_nag_263d9695.NagPack], jsii.get(self, "nagPacks"))


@jsii.data_type(
    jsii_type="@aws/pdk.pdk_nag.PDKNagAppProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.AppProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "auto_synth": "autoSynth",
        "context": "context",
        "default_stack_synthesizer": "defaultStackSynthesizer",
        "outdir": "outdir",
        "policy_validation_beta1": "policyValidationBeta1",
        "post_cli_context": "postCliContext",
        "stack_traces": "stackTraces",
        "tree_metadata": "treeMetadata",
        "fail_on_error": "failOnError",
        "fail_on_warning": "failOnWarning",
        "nag_packs": "nagPacks",
    },
)
class PDKNagAppProps(_aws_cdk_ceddda9d.AppProps):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        auto_synth: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        default_stack_synthesizer: typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer] = None,
        outdir: typing.Optional[builtins.str] = None,
        policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
        post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        tree_metadata: typing.Optional[builtins.bool] = None,
        fail_on_error: typing.Optional[builtins.bool] = None,
        fail_on_warning: typing.Optional[builtins.bool] = None,
        nag_packs: typing.Optional[typing.Sequence[_cdk_nag_263d9695.NagPack]] = None,
    ) -> None:
        '''
        :param analytics_reporting: Include runtime versioning information in the Stacks of this app. Default: Value of 'aws:cdk:version-reporting' context key
        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param default_stack_synthesizer: The stack synthesizer to use by default for all Stacks in the App. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. Default: - A ``DefaultStackSynthesizer`` with default settings
        :param outdir: The output directory into which to emit synthesized artifacts. You should never need to set this value. By default, the value you pass to the CLI's ``--output`` flag will be used, and if you change it to a different directory the CLI will fail to pick up the generated Cloud Assembly. This property is intended for internal and testing use. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param policy_validation_beta1: Validation plugins to run after synthesis. Default: - no validation plugins
        :param post_cli_context: Additional context values for the application. Context provided here has precedence over context set by: - The CLI via --context - The ``context`` key in ``cdk.json`` - The ``AppProps.context`` property This property is recommended over the ``AppProps.context`` property since you can make final decision over which context value to take in your app. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        :param fail_on_error: Determines whether any errors encountered should trigger a test failure. Default: false
        :param fail_on_warning: Determines whether any warnings encountered should trigger a test failure. Default: false
        :param nag_packs: Custom nag packs to execute. Default: DEFAULT_NAG_PACKS

        :inheritDoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ff6b436e20d432d5ee6d09f9604df61e816b58f9601272a85d1cfceb83d7bc)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument auto_synth", value=auto_synth, expected_type=type_hints["auto_synth"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument default_stack_synthesizer", value=default_stack_synthesizer, expected_type=type_hints["default_stack_synthesizer"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument policy_validation_beta1", value=policy_validation_beta1, expected_type=type_hints["policy_validation_beta1"])
            check_type(argname="argument post_cli_context", value=post_cli_context, expected_type=type_hints["post_cli_context"])
            check_type(argname="argument stack_traces", value=stack_traces, expected_type=type_hints["stack_traces"])
            check_type(argname="argument tree_metadata", value=tree_metadata, expected_type=type_hints["tree_metadata"])
            check_type(argname="argument fail_on_error", value=fail_on_error, expected_type=type_hints["fail_on_error"])
            check_type(argname="argument fail_on_warning", value=fail_on_warning, expected_type=type_hints["fail_on_warning"])
            check_type(argname="argument nag_packs", value=nag_packs, expected_type=type_hints["nag_packs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if auto_synth is not None:
            self._values["auto_synth"] = auto_synth
        if context is not None:
            self._values["context"] = context
        if default_stack_synthesizer is not None:
            self._values["default_stack_synthesizer"] = default_stack_synthesizer
        if outdir is not None:
            self._values["outdir"] = outdir
        if policy_validation_beta1 is not None:
            self._values["policy_validation_beta1"] = policy_validation_beta1
        if post_cli_context is not None:
            self._values["post_cli_context"] = post_cli_context
        if stack_traces is not None:
            self._values["stack_traces"] = stack_traces
        if tree_metadata is not None:
            self._values["tree_metadata"] = tree_metadata
        if fail_on_error is not None:
            self._values["fail_on_error"] = fail_on_error
        if fail_on_warning is not None:
            self._values["fail_on_warning"] = fail_on_warning
        if nag_packs is not None:
            self._values["nag_packs"] = nag_packs

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in the Stacks of this app.

        :default: Value of 'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_synth(self) -> typing.Optional[builtins.bool]:
        '''Automatically call ``synth()`` before the program exits.

        If you set this, you don't have to call ``synth()`` explicitly. Note that
        this feature is only available for certain programming languages, and
        calling ``synth()`` is still recommended.

        :default:

        true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false``
        otherwise
        '''
        result = self._values.get("auto_synth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional context values for the application.

        Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence.

        Context can be read from any construct using ``node.getContext(key)``.

        :default: - no additional context
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def default_stack_synthesizer(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer]:
        '''The stack synthesizer to use by default for all Stacks in the App.

        The Stack Synthesizer controls aspects of synthesis and deployment,
        like how assets are referenced and what IAM roles to use. For more
        information, see the README of the main CDK package.

        :default: - A ``DefaultStackSynthesizer`` with default settings
        '''
        result = self._values.get("default_stack_synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''The output directory into which to emit synthesized artifacts.

        You should never need to set this value. By default, the value you pass to
        the CLI's ``--output`` flag will be used, and if you change it to a different
        directory the CLI will fail to pick up the generated Cloud Assembly.

        This property is intended for internal and testing use.

        :default:

        - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``.
        If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_validation_beta1(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]]:
        '''Validation plugins to run after synthesis.

        :default: - no validation plugins
        '''
        result = self._values.get("policy_validation_beta1")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]], result)

    @builtins.property
    def post_cli_context(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional context values for the application.

        Context provided here has precedence over context set by:

        - The CLI via --context
        - The ``context`` key in ``cdk.json``
        - The ``AppProps.context`` property

        This property is recommended over the ``AppProps.context`` property since you
        can make final decision over which context value to take in your app.

        Context can be read from any construct using ``node.getContext(key)``.

        :default: - no additional context

        Example::

            // context from the CLI and from `cdk.json` are stored in the
            // CDK_CONTEXT env variable
            const cliContext = JSON.parse(process.env.CDK_CONTEXT!);
            
            // determine whether to take the context passed in the CLI or not
            const determineValue = process.env.PROD ? cliContext.SOMEKEY : 'my-prod-value';
            new App({
              postCliContext: {
                SOMEKEY: determineValue,
              },
            });
        '''
        result = self._values.get("post_cli_context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def stack_traces(self) -> typing.Optional[builtins.bool]:
        '''Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs.

        :default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        '''
        result = self._values.get("stack_traces")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tree_metadata(self) -> typing.Optional[builtins.bool]:
        '''Include construct tree metadata as part of the Cloud Assembly.

        :default: true
        '''
        result = self._values.get("tree_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fail_on_error(self) -> typing.Optional[builtins.bool]:
        '''Determines whether any errors encountered should trigger a test failure.

        :default: false
        '''
        result = self._values.get("fail_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fail_on_warning(self) -> typing.Optional[builtins.bool]:
        '''Determines whether any warnings encountered should trigger a test failure.

        :default: false
        '''
        result = self._values.get("fail_on_warning")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nag_packs(self) -> typing.Optional[typing.List[_cdk_nag_263d9695.NagPack]]:
        '''Custom nag packs to execute.

        :default: DEFAULT_NAG_PACKS
        '''
        result = self._values.get("nag_packs")
        return typing.cast(typing.Optional[typing.List[_cdk_nag_263d9695.NagPack]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PDKNagAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsPrototypingChecks",
    "ExtendedNagResult",
    "Message",
    "NagResult",
    "NagResultCompliance",
    "PDKNag",
    "PDKNagApp",
    "PDKNagAppProps",
]

publication.publish()

def _typecheckingstub__b8aa12b05f34ae8c5f2ba1473e38e19d866fb8f4b520412005d0fe346b7fb8e7(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8449c5c2cfffdf3f73061d623bdbfb9a6f8c1a04846ab12f3c08d754a61977e5(
    *,
    compliance: NagResultCompliance,
    nag_pack_name: builtins.str,
    resource: _aws_cdk_ceddda9d.CfnResource,
    rule_explanation: builtins.str,
    rule_id: builtins.str,
    rule_info: builtins.str,
    rule_level: _cdk_nag_263d9695.NagMessageLevel,
    rule_original_name: builtins.str,
    error_message: typing.Optional[builtins.str] = None,
    finding_id: typing.Optional[builtins.str] = None,
    suppression_reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c93182a4922d7452f57be229082f9c3d5dd9ca71941154fcdac4df76b43c528(
    *,
    message_description: builtins.str,
    message_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f28e99b6450320d049052294b8732c9914971212aecba15ae4e76747213125(
    *,
    messages: typing.Sequence[typing.Union[Message, typing.Dict[builtins.str, typing.Any]]],
    resource: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df4154748281a399576171b2f69c41577cb5a8b1ea4b026921fbf1e7feed914(
    stack: _aws_cdk_ceddda9d.Stack,
    path: builtins.str,
    suppressions: typing.Sequence[typing.Union[_cdk_nag_263d9695.NagPackSuppression, typing.Dict[builtins.str, typing.Any]]],
    apply_to_children: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c7b8ca6e6cf7067508e077a349f6970a468d6f27683ecf2baab2767c4a24e6(
    stack: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa0bbf9e40945577406f43f4ea42623d4fe13e5e55279a3613263349deeea63(
    stack: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3571ab007307dce3ff9ffc4cbe7060b3eb33d9a5019948d82aca2dd1edf04c18(
    stack: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9f55608ad622f385b97d568c1b49a24059612e0fe4dde7d461d193d8779f26(
    stack: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fcf25e53176b62e6528f199f19b5eb0ba7082819a349f5a61264769c40505e(
    *results: ExtendedNagResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ff6b436e20d432d5ee6d09f9604df61e816b58f9601272a85d1cfceb83d7bc(
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    auto_synth: typing.Optional[builtins.bool] = None,
    context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    default_stack_synthesizer: typing.Optional[_aws_cdk_ceddda9d.IReusableStackSynthesizer] = None,
    outdir: typing.Optional[builtins.str] = None,
    policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
    post_cli_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    stack_traces: typing.Optional[builtins.bool] = None,
    tree_metadata: typing.Optional[builtins.bool] = None,
    fail_on_error: typing.Optional[builtins.bool] = None,
    fail_on_warning: typing.Optional[builtins.bool] = None,
    nag_packs: typing.Optional[typing.Sequence[_cdk_nag_263d9695.NagPack]] = None,
) -> None:
    """Type checking stubs"""
    pass
