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
import aws_cdk.aws_codecommit as _aws_cdk_aws_codecommit_ceddda9d
import aws_cdk.aws_codepipeline as _aws_cdk_aws_codepipeline_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.pipelines as _aws_cdk_pipelines_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws/pdk.pipeline.CodePipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_bucket": "artifactBucket",
        "asset_publishing_code_build_defaults": "assetPublishingCodeBuildDefaults",
        "cli_version": "cliVersion",
        "code_build_defaults": "codeBuildDefaults",
        "code_pipeline": "codePipeline",
        "cross_account_keys": "crossAccountKeys",
        "cross_region_replication_buckets": "crossRegionReplicationBuckets",
        "docker_credentials": "dockerCredentials",
        "docker_enabled_for_self_mutation": "dockerEnabledForSelfMutation",
        "docker_enabled_for_synth": "dockerEnabledForSynth",
        "enable_key_rotation": "enableKeyRotation",
        "pipeline_name": "pipelineName",
        "publish_assets_in_parallel": "publishAssetsInParallel",
        "reuse_cross_region_support_stacks": "reuseCrossRegionSupportStacks",
        "role": "role",
        "self_mutation": "selfMutation",
        "self_mutation_code_build_defaults": "selfMutationCodeBuildDefaults",
        "synth": "synth",
        "synth_code_build_defaults": "synthCodeBuildDefaults",
        "use_change_sets": "useChangeSets",
    },
)
class CodePipelineProps:
    def __init__(
        self,
        *,
        artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cli_version: typing.Optional[builtins.str] = None,
        code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
        docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
        docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
        reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        self_mutation: typing.Optional[builtins.bool] = None,
        self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
        synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        use_change_sets: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''CodePipelineProps.

        :param artifact_bucket: An existing S3 Bucket to use for storing the pipeline's artifact. Default: - A new S3 bucket will be created.
        :param asset_publishing_code_build_defaults: Additional customizations to apply to the asset publishing CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param cli_version: CDK CLI version to use in self-mutation and asset publishing steps. If you want to lock the CDK CLI version used in the pipeline, by steps that are automatically generated for you, specify the version here. We recommend you do not specify this value, as not specifying it always uses the latest CLI version which is backwards compatible with old versions. If you do specify it, be aware that this version should always be equal to or higher than the version of the CDK framework used by the CDK app, when the CDK commands are run during your pipeline execution. When you change this version, the *next time* the ``SelfMutate`` step runs it will still be using the CLI of the the *previous* version that was in this property: it will only start using the new version after ``SelfMutate`` completes successfully. That means that if you want to update both framework and CLI version, you should update the CLI version first, commit, push and deploy, and only then update the framework version. Default: - Latest version
        :param code_build_defaults: Customize the CodeBuild projects created for this pipeline. Default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_7_0
        :param code_pipeline: An existing Pipeline to be reused and built upon. [disable-awslint:ref-via-interface] Default: - a new underlying pipeline is created.
        :param cross_account_keys: Create KMS keys for the artifact buckets, allowing cross-account deployments. The artifact buckets have to be encrypted to support deploying CDK apps to another account, so if you want to do that or want to have your artifact buckets encrypted, be sure to set this value to ``true``. Be aware there is a cost associated with maintaining the KMS keys. Default: false
        :param cross_region_replication_buckets: A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region. Passed directly through to the {@link cp.Pipeline }. Default: - no cross region replication buckets.
        :param docker_credentials: A list of credentials used to authenticate to Docker registries. Specify any credentials necessary within the pipeline to build, synth, update, or publish assets. Default: []
        :param docker_enabled_for_self_mutation: Enable Docker for the self-mutate step. Set this to true if the pipeline itself uses Docker container assets (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build image of a CodeBuild step in the pipeline). You do not need to set it if you build Docker image assets in the application Stages and Stacks that are *deployed* by this pipeline. Configures privileged mode for the self-mutation CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the Docker asset in the pipeline. Default: false
        :param docker_enabled_for_synth: Enable Docker for the 'synth' step. Set this to true if you are using file assets that require "bundling" anywhere in your application (meaning an asset compilation step will be run with the tools provided by a Docker image), both for the Pipeline stack as well as the application stacks. A common way to use bundling assets in your application is by using the ``aws-cdk-lib/aws-lambda-nodejs`` library. Configures privileged mode for the synth CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the bundled asset. Default: false
        :param enable_key_rotation: Enable KMS key rotation for the generated KMS keys. By default KMS key rotation is disabled, but will add additional costs when enabled. Default: - false (key rotation is disabled)
        :param pipeline_name: The name of the CodePipeline pipeline. Default: - Automatically generated
        :param publish_assets_in_parallel: Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets. Publishing in parallel improves concurrency and may reduce publishing latency, but may also increase overall provisioning time of the CodeBuild projects. Experiment and see what value works best for you. Default: true
        :param reuse_cross_region_support_stacks: Reuse the same cross region support stack for all pipelines in the App. Default: - true (Use the same support stack for all pipelines in App)
        :param role: The IAM role to be assumed by this Pipeline. Default: - A new role is created
        :param self_mutation: Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param self_mutation_code_build_defaults: Additional customizations to apply to the self mutation CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param synth: The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        :param synth_code_build_defaults: Additional customizations to apply to the synthesize CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param use_change_sets: Deploy every stack by creating a change set and executing it. When enabled, creates a "Prepare" and "Execute" action for each stack. Disable to deploy the stack in one pipeline action. Default: true
        '''
        if isinstance(asset_publishing_code_build_defaults, dict):
            asset_publishing_code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**asset_publishing_code_build_defaults)
        if isinstance(code_build_defaults, dict):
            code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**code_build_defaults)
        if isinstance(self_mutation_code_build_defaults, dict):
            self_mutation_code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**self_mutation_code_build_defaults)
        if isinstance(synth_code_build_defaults, dict):
            synth_code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**synth_code_build_defaults)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3cde37f902c1991f07ce6cca86ee234479782b49c56f386ea31b03ba832f0fc)
            check_type(argname="argument artifact_bucket", value=artifact_bucket, expected_type=type_hints["artifact_bucket"])
            check_type(argname="argument asset_publishing_code_build_defaults", value=asset_publishing_code_build_defaults, expected_type=type_hints["asset_publishing_code_build_defaults"])
            check_type(argname="argument cli_version", value=cli_version, expected_type=type_hints["cli_version"])
            check_type(argname="argument code_build_defaults", value=code_build_defaults, expected_type=type_hints["code_build_defaults"])
            check_type(argname="argument code_pipeline", value=code_pipeline, expected_type=type_hints["code_pipeline"])
            check_type(argname="argument cross_account_keys", value=cross_account_keys, expected_type=type_hints["cross_account_keys"])
            check_type(argname="argument cross_region_replication_buckets", value=cross_region_replication_buckets, expected_type=type_hints["cross_region_replication_buckets"])
            check_type(argname="argument docker_credentials", value=docker_credentials, expected_type=type_hints["docker_credentials"])
            check_type(argname="argument docker_enabled_for_self_mutation", value=docker_enabled_for_self_mutation, expected_type=type_hints["docker_enabled_for_self_mutation"])
            check_type(argname="argument docker_enabled_for_synth", value=docker_enabled_for_synth, expected_type=type_hints["docker_enabled_for_synth"])
            check_type(argname="argument enable_key_rotation", value=enable_key_rotation, expected_type=type_hints["enable_key_rotation"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument publish_assets_in_parallel", value=publish_assets_in_parallel, expected_type=type_hints["publish_assets_in_parallel"])
            check_type(argname="argument reuse_cross_region_support_stacks", value=reuse_cross_region_support_stacks, expected_type=type_hints["reuse_cross_region_support_stacks"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument self_mutation", value=self_mutation, expected_type=type_hints["self_mutation"])
            check_type(argname="argument self_mutation_code_build_defaults", value=self_mutation_code_build_defaults, expected_type=type_hints["self_mutation_code_build_defaults"])
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
            check_type(argname="argument synth_code_build_defaults", value=synth_code_build_defaults, expected_type=type_hints["synth_code_build_defaults"])
            check_type(argname="argument use_change_sets", value=use_change_sets, expected_type=type_hints["use_change_sets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if artifact_bucket is not None:
            self._values["artifact_bucket"] = artifact_bucket
        if asset_publishing_code_build_defaults is not None:
            self._values["asset_publishing_code_build_defaults"] = asset_publishing_code_build_defaults
        if cli_version is not None:
            self._values["cli_version"] = cli_version
        if code_build_defaults is not None:
            self._values["code_build_defaults"] = code_build_defaults
        if code_pipeline is not None:
            self._values["code_pipeline"] = code_pipeline
        if cross_account_keys is not None:
            self._values["cross_account_keys"] = cross_account_keys
        if cross_region_replication_buckets is not None:
            self._values["cross_region_replication_buckets"] = cross_region_replication_buckets
        if docker_credentials is not None:
            self._values["docker_credentials"] = docker_credentials
        if docker_enabled_for_self_mutation is not None:
            self._values["docker_enabled_for_self_mutation"] = docker_enabled_for_self_mutation
        if docker_enabled_for_synth is not None:
            self._values["docker_enabled_for_synth"] = docker_enabled_for_synth
        if enable_key_rotation is not None:
            self._values["enable_key_rotation"] = enable_key_rotation
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if publish_assets_in_parallel is not None:
            self._values["publish_assets_in_parallel"] = publish_assets_in_parallel
        if reuse_cross_region_support_stacks is not None:
            self._values["reuse_cross_region_support_stacks"] = reuse_cross_region_support_stacks
        if role is not None:
            self._values["role"] = role
        if self_mutation is not None:
            self._values["self_mutation"] = self_mutation
        if self_mutation_code_build_defaults is not None:
            self._values["self_mutation_code_build_defaults"] = self_mutation_code_build_defaults
        if synth is not None:
            self._values["synth"] = synth
        if synth_code_build_defaults is not None:
            self._values["synth_code_build_defaults"] = synth_code_build_defaults
        if use_change_sets is not None:
            self._values["use_change_sets"] = use_change_sets

    @builtins.property
    def artifact_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''An existing S3 Bucket to use for storing the pipeline's artifact.

        :default: - A new S3 bucket will be created.
        '''
        result = self._values.get("artifact_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def asset_publishing_code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Additional customizations to apply to the asset publishing CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied
        '''
        result = self._values.get("asset_publishing_code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def cli_version(self) -> typing.Optional[builtins.str]:
        '''CDK CLI version to use in self-mutation and asset publishing steps.

        If you want to lock the CDK CLI version used in the pipeline, by steps
        that are automatically generated for you, specify the version here.

        We recommend you do not specify this value, as not specifying it always
        uses the latest CLI version which is backwards compatible with old versions.

        If you do specify it, be aware that this version should always be equal to or higher than the
        version of the CDK framework used by the CDK app, when the CDK commands are
        run during your pipeline execution. When you change this version, the *next
        time* the ``SelfMutate`` step runs it will still be using the CLI of the the
        *previous* version that was in this property: it will only start using the
        new version after ``SelfMutate`` completes successfully. That means that if
        you want to update both framework and CLI version, you should update the
        CLI version first, commit, push and deploy, and only then update the
        framework version.

        :default: - Latest version
        '''
        result = self._values.get("cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Customize the CodeBuild projects created for this pipeline.

        :default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_7_0
        '''
        result = self._values.get("code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def code_pipeline(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline]:
        '''An existing Pipeline to be reused and built upon.

        [disable-awslint:ref-via-interface]

        :default: - a new underlying pipeline is created.
        '''
        result = self._values.get("code_pipeline")
        return typing.cast(typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline], result)

    @builtins.property
    def cross_account_keys(self) -> typing.Optional[builtins.bool]:
        '''Create KMS keys for the artifact buckets, allowing cross-account deployments.

        The artifact buckets have to be encrypted to support deploying CDK apps to
        another account, so if you want to do that or want to have your artifact
        buckets encrypted, be sure to set this value to ``true``.

        Be aware there is a cost associated with maintaining the KMS keys.

        :default: false
        '''
        result = self._values.get("cross_account_keys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_replication_buckets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]]:
        '''A map of region to S3 bucket name used for cross-region CodePipeline.

        For every Action that you specify targeting a different region than the Pipeline itself,
        if you don't provide an explicit Bucket for that region using this property,
        the construct will automatically create a Stack containing an S3 Bucket in that region.
        Passed directly through to the {@link cp.Pipeline }.

        :default: - no cross region replication buckets.
        '''
        result = self._values.get("cross_region_replication_buckets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]], result)

    @builtins.property
    def docker_credentials(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.DockerCredential]]:
        '''A list of credentials used to authenticate to Docker registries.

        Specify any credentials necessary within the pipeline to build, synth, update, or publish assets.

        :default: []
        '''
        result = self._values.get("docker_credentials")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.DockerCredential]], result)

    @builtins.property
    def docker_enabled_for_self_mutation(self) -> typing.Optional[builtins.bool]:
        '''Enable Docker for the self-mutate step.

        Set this to true if the pipeline itself uses Docker container assets
        (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build
        image of a CodeBuild step in the pipeline).

        You do not need to set it if you build Docker image assets in the
        application Stages and Stacks that are *deployed* by this pipeline.

        Configures privileged mode for the self-mutation CodeBuild action.

        If you are about to turn this on in an already-deployed Pipeline,
        set the value to ``true`` first, commit and allow the pipeline to
        self-update, and only then use the Docker asset in the pipeline.

        :default: false
        '''
        result = self._values.get("docker_enabled_for_self_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docker_enabled_for_synth(self) -> typing.Optional[builtins.bool]:
        '''Enable Docker for the 'synth' step.

        Set this to true if you are using file assets that require
        "bundling" anywhere in your application (meaning an asset
        compilation step will be run with the tools provided by
        a Docker image), both for the Pipeline stack as well as the
        application stacks.

        A common way to use bundling assets in your application is by
        using the ``aws-cdk-lib/aws-lambda-nodejs`` library.

        Configures privileged mode for the synth CodeBuild action.

        If you are about to turn this on in an already-deployed Pipeline,
        set the value to ``true`` first, commit and allow the pipeline to
        self-update, and only then use the bundled asset.

        :default: false
        '''
        result = self._values.get("docker_enabled_for_synth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_key_rotation(self) -> typing.Optional[builtins.bool]:
        '''Enable KMS key rotation for the generated KMS keys.

        By default KMS key rotation is disabled, but will add
        additional costs when enabled.

        :default: - false (key rotation is disabled)
        '''
        result = self._values.get("enable_key_rotation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        '''The name of the CodePipeline pipeline.

        :default: - Automatically generated
        '''
        result = self._values.get("pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_assets_in_parallel(self) -> typing.Optional[builtins.bool]:
        '''Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets.

        Publishing in parallel improves concurrency and may reduce publishing
        latency, but may also increase overall provisioning time of the CodeBuild
        projects.

        Experiment and see what value works best for you.

        :default: true
        '''
        result = self._values.get("publish_assets_in_parallel")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reuse_cross_region_support_stacks(self) -> typing.Optional[builtins.bool]:
        '''Reuse the same cross region support stack for all pipelines in the App.

        :default: - true (Use the same support stack for all pipelines in App)
        '''
        result = self._values.get("reuse_cross_region_support_stacks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The IAM role to be assumed by this Pipeline.

        :default: - A new role is created
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def self_mutation(self) -> typing.Optional[builtins.bool]:
        '''Whether the pipeline will update itself.

        This needs to be set to ``true`` to allow the pipeline to reconfigure
        itself when assets or stages are being added to it, and ``true`` is the
        recommended setting.

        You can temporarily set this to ``false`` while you are iterating
        on the pipeline itself and prefer to deploy changes using ``cdk deploy``.

        :default: true
        '''
        result = self._values.get("self_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def self_mutation_code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Additional customizations to apply to the self mutation CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied
        '''
        result = self._values.get("self_mutation_code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def synth(self) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer]:
        '''The build step that produces the CDK Cloud Assembly.

        The primary output of this step needs to be the ``cdk.out`` directory
        generated by the ``cdk synth`` command.

        If you use a ``ShellStep`` here and you don't configure an output directory,
        the output directory will automatically be assumed to be ``cdk.out``.
        '''
        result = self._values.get("synth")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer], result)

    @builtins.property
    def synth_code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Additional customizations to apply to the synthesize CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied
        '''
        result = self._values.get("synth_code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def use_change_sets(self) -> typing.Optional[builtins.bool]:
        '''Deploy every stack by creating a change set and executing it.

        When enabled, creates a "Prepare" and "Execute" action for each stack. Disable
        to deploy the stack in one pipeline action.

        :default: true
        '''
        result = self._values.get("use_change_sets")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodePipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.pipeline.IsDefaultBranchProps",
    jsii_struct_bases=[],
    name_mapping={"default_branch_name": "defaultBranchName", "node": "node"},
)
class IsDefaultBranchProps:
    def __init__(
        self,
        *,
        default_branch_name: typing.Optional[builtins.str] = None,
        node: typing.Optional[_constructs_77d1e7e8.Node] = None,
    ) -> None:
        '''Properties to help the isDefaultBranch function determine the default branch name.

        :param default_branch_name: Specify the default branch name without context.
        :param node: The current node to fetch defaultBranchName from context.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9af73ab3cb4e5653a7fbbf5939157ed24cd9e40ac7adc479ed17150e7328293)
            check_type(argname="argument default_branch_name", value=default_branch_name, expected_type=type_hints["default_branch_name"])
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_branch_name is not None:
            self._values["default_branch_name"] = default_branch_name
        if node is not None:
            self._values["node"] = node

    @builtins.property
    def default_branch_name(self) -> typing.Optional[builtins.str]:
        '''Specify the default branch name without context.'''
        result = self._values.get("default_branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node(self) -> typing.Optional[_constructs_77d1e7e8.Node]:
        '''The current node to fetch defaultBranchName from context.'''
        result = self._values.get("node")
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Node], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IsDefaultBranchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PDKPipeline(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.pipeline.PDKPipeline",
):
    '''An extension to CodePipeline which configures same defaults for a NX Monorepo codebase.

    In addition to this, it also creates a CodeCommit repository with
    automated PR builds and approvals.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        primary_synth_directory: builtins.str,
        repository_name: builtins.str,
        branch_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command: typing.Optional[builtins.str] = None,
        cdk_src_dir: typing.Optional[builtins.str] = None,
        code_commit_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        code_commit_repository: typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository] = None,
        default_branch_name: typing.Optional[builtins.str] = None,
        sonar_code_scanner_config: typing.Optional[typing.Union["SonarCodeScannerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        synth_shell_step_partial_props: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.ShellStepProps, typing.Dict[builtins.str, typing.Any]]] = None,
        artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cli_version: typing.Optional[builtins.str] = None,
        code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
        docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
        docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
        reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        self_mutation: typing.Optional[builtins.bool] = None,
        self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
        synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        use_change_sets: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param primary_synth_directory: Output directory for cdk synthesized artifacts i.e: packages/infra/cdk.out.
        :param repository_name: Name of the CodeCommit repository to create.
        :param branch_name_prefixes: Branch name prefixes Any branches created matching this list of prefixes will create a new pipeline and stack. Default: undefined
        :param cdk_command: CDK command. Override the command used to call cdk for synth and deploy. Default: 'npx cdk'
        :param cdk_src_dir: The directory with ``cdk.json`` to run cdk synth from. Set this if you enabled feature branches and ``cdk.json`` is not located in the parent directory of ``primarySynthDirectory``. Default: The parent directory of ``primarySynthDirectory``
        :param code_commit_removal_policy: Possible values for a resource's Removal Policy The removal policy controls what happens to the resource if it stops being managed by CloudFormation.
        :param code_commit_repository: The repository to add the pipeline to.
        :param default_branch_name: Branch to trigger the pipeline execution. Default: mainline
        :param sonar_code_scanner_config: Configuration for enabling Sonarqube code scanning on a successful synth. Default: undefined
        :param synth_shell_step_partial_props: PDKPipeline by default assumes a NX Monorepo structure for it's codebase and uses sane defaults for the install and run commands. To override these defaults and/or provide additional inputs, specify env settings, etc you can provide a partial ShellStepProps.
        :param artifact_bucket: An existing S3 Bucket to use for storing the pipeline's artifact. Default: - A new S3 bucket will be created.
        :param asset_publishing_code_build_defaults: Additional customizations to apply to the asset publishing CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param cli_version: CDK CLI version to use in self-mutation and asset publishing steps. If you want to lock the CDK CLI version used in the pipeline, by steps that are automatically generated for you, specify the version here. We recommend you do not specify this value, as not specifying it always uses the latest CLI version which is backwards compatible with old versions. If you do specify it, be aware that this version should always be equal to or higher than the version of the CDK framework used by the CDK app, when the CDK commands are run during your pipeline execution. When you change this version, the *next time* the ``SelfMutate`` step runs it will still be using the CLI of the the *previous* version that was in this property: it will only start using the new version after ``SelfMutate`` completes successfully. That means that if you want to update both framework and CLI version, you should update the CLI version first, commit, push and deploy, and only then update the framework version. Default: - Latest version
        :param code_build_defaults: Customize the CodeBuild projects created for this pipeline. Default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_7_0
        :param code_pipeline: An existing Pipeline to be reused and built upon. [disable-awslint:ref-via-interface] Default: - a new underlying pipeline is created.
        :param cross_account_keys: Create KMS keys for the artifact buckets, allowing cross-account deployments. The artifact buckets have to be encrypted to support deploying CDK apps to another account, so if you want to do that or want to have your artifact buckets encrypted, be sure to set this value to ``true``. Be aware there is a cost associated with maintaining the KMS keys. Default: false
        :param cross_region_replication_buckets: A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region. Passed directly through to the {@link cp.Pipeline }. Default: - no cross region replication buckets.
        :param docker_credentials: A list of credentials used to authenticate to Docker registries. Specify any credentials necessary within the pipeline to build, synth, update, or publish assets. Default: []
        :param docker_enabled_for_self_mutation: Enable Docker for the self-mutate step. Set this to true if the pipeline itself uses Docker container assets (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build image of a CodeBuild step in the pipeline). You do not need to set it if you build Docker image assets in the application Stages and Stacks that are *deployed* by this pipeline. Configures privileged mode for the self-mutation CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the Docker asset in the pipeline. Default: false
        :param docker_enabled_for_synth: Enable Docker for the 'synth' step. Set this to true if you are using file assets that require "bundling" anywhere in your application (meaning an asset compilation step will be run with the tools provided by a Docker image), both for the Pipeline stack as well as the application stacks. A common way to use bundling assets in your application is by using the ``aws-cdk-lib/aws-lambda-nodejs`` library. Configures privileged mode for the synth CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the bundled asset. Default: false
        :param enable_key_rotation: Enable KMS key rotation for the generated KMS keys. By default KMS key rotation is disabled, but will add additional costs when enabled. Default: - false (key rotation is disabled)
        :param pipeline_name: The name of the CodePipeline pipeline. Default: - Automatically generated
        :param publish_assets_in_parallel: Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets. Publishing in parallel improves concurrency and may reduce publishing latency, but may also increase overall provisioning time of the CodeBuild projects. Experiment and see what value works best for you. Default: true
        :param reuse_cross_region_support_stacks: Reuse the same cross region support stack for all pipelines in the App. Default: - true (Use the same support stack for all pipelines in App)
        :param role: The IAM role to be assumed by this Pipeline. Default: - A new role is created
        :param self_mutation: Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param self_mutation_code_build_defaults: Additional customizations to apply to the self mutation CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param synth: The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        :param synth_code_build_defaults: Additional customizations to apply to the synthesize CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param use_change_sets: Deploy every stack by creating a change set and executing it. When enabled, creates a "Prepare" and "Execute" action for each stack. Disable to deploy the stack in one pipeline action. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1fc30725663d11b68afc62a715c01473c5ff1442fd16970c05eb9b88c2d55f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PDKPipelineProps(
            primary_synth_directory=primary_synth_directory,
            repository_name=repository_name,
            branch_name_prefixes=branch_name_prefixes,
            cdk_command=cdk_command,
            cdk_src_dir=cdk_src_dir,
            code_commit_removal_policy=code_commit_removal_policy,
            code_commit_repository=code_commit_repository,
            default_branch_name=default_branch_name,
            sonar_code_scanner_config=sonar_code_scanner_config,
            synth_shell_step_partial_props=synth_shell_step_partial_props,
            artifact_bucket=artifact_bucket,
            asset_publishing_code_build_defaults=asset_publishing_code_build_defaults,
            cli_version=cli_version,
            code_build_defaults=code_build_defaults,
            code_pipeline=code_pipeline,
            cross_account_keys=cross_account_keys,
            cross_region_replication_buckets=cross_region_replication_buckets,
            docker_credentials=docker_credentials,
            docker_enabled_for_self_mutation=docker_enabled_for_self_mutation,
            docker_enabled_for_synth=docker_enabled_for_synth,
            enable_key_rotation=enable_key_rotation,
            pipeline_name=pipeline_name,
            publish_assets_in_parallel=publish_assets_in_parallel,
            reuse_cross_region_support_stacks=reuse_cross_region_support_stacks,
            role=role,
            self_mutation=self_mutation,
            self_mutation_code_build_defaults=self_mutation_code_build_defaults,
            synth=synth,
            synth_code_build_defaults=synth_code_build_defaults,
            use_change_sets=use_change_sets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getBranchPrefix")
    @builtins.classmethod
    def get_branch_prefix(
        cls,
        *,
        default_branch_name: typing.Optional[builtins.str] = None,
        node: typing.Optional[_constructs_77d1e7e8.Node] = None,
    ) -> builtins.str:
        '''A helper function to create a branch prefix.

        The prefix is empty on the default branch.

        :param default_branch_name: Specify the default branch name without context.
        :param node: The current node to fetch defaultBranchName from context.

        :return: The branch prefix.
        '''
        props = IsDefaultBranchProps(
            default_branch_name=default_branch_name, node=node
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "getBranchPrefix", [props]))

    @jsii.member(jsii_name="isDefaultBranch")
    @builtins.classmethod
    def is_default_branch(
        cls,
        *,
        default_branch_name: typing.Optional[builtins.str] = None,
        node: typing.Optional[_constructs_77d1e7e8.Node] = None,
    ) -> builtins.bool:
        '''A helper function to determine if the current branch is the default branch.

        If there is no BRANCH environment variable, then assume this is the default
        branch. Otherwise, check that BRANCH matches the default branch name.

        The default branch name is determined in the following priority:

        1. defaultBranchName property
        2. defaultBranchName context
        3. PDKPipeline.defaultBranchName constant

        :param default_branch_name: Specify the default branch name without context.
        :param node: The current node to fetch defaultBranchName from context.

        :return: True if the current branch is the default branch.
        '''
        props = IsDefaultBranchProps(
            default_branch_name=default_branch_name, node=node
        )

        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isDefaultBranch", [props]))

    @jsii.member(jsii_name="normalizeBranchName")
    @builtins.classmethod
    def normalize_branch_name(cls, branch_name: builtins.str) -> builtins.str:
        '''A helper function to normalize the branch name with only alphanumeric characters and hypens ('-').

        :param branch_name: The name of the branch to normalize.

        :return: The normalized branch name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd9d65ebcdf7f007bfface73cce98ed9b6536787a15dcf4c5fc44679c09df26)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "normalizeBranchName", [branch_name]))

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        stage: _aws_cdk_ceddda9d.Stage,
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _aws_cdk_pipelines_ceddda9d.StageDeployment:
        '''
        :param stage: -
        :param post: Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: Instructions for stack level steps. Default: - No additional instructions

        :inheritDoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6b99d170e0fccb842092fe64d3c8cfd0993145d60e03b63ddfafae1d354b1c)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = _aws_cdk_pipelines_ceddda9d.AddStageOpts(
            post=post, pre=pre, stack_steps=stack_steps
        )

        return typing.cast(_aws_cdk_pipelines_ceddda9d.StageDeployment, jsii.invoke(self, "addStage", [stage, options]))

    @jsii.member(jsii_name="buildPipeline")
    def build_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "buildPipeline", []))

    @jsii.member(jsii_name="suppressCDKViolations")
    def suppress_cdk_violations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "suppressCDKViolations", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_BRANCHES")
    def ALL_BRANCHES(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "ALL_BRANCHES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="defaultBranchName")
    def DEFAULT_BRANCH_NAME(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "defaultBranchName"))

    @builtins.property
    @jsii.member(jsii_name="codePipeline")
    def code_pipeline(self) -> _aws_cdk_pipelines_ceddda9d.CodePipeline:
        return typing.cast(_aws_cdk_pipelines_ceddda9d.CodePipeline, jsii.get(self, "codePipeline"))

    @builtins.property
    @jsii.member(jsii_name="codeRepository")
    def code_repository(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository]:
        return typing.cast(typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository], jsii.get(self, "codeRepository"))


@jsii.data_type(
    jsii_type="@aws/pdk.pipeline.PDKPipelineProps",
    jsii_struct_bases=[CodePipelineProps],
    name_mapping={
        "artifact_bucket": "artifactBucket",
        "asset_publishing_code_build_defaults": "assetPublishingCodeBuildDefaults",
        "cli_version": "cliVersion",
        "code_build_defaults": "codeBuildDefaults",
        "code_pipeline": "codePipeline",
        "cross_account_keys": "crossAccountKeys",
        "cross_region_replication_buckets": "crossRegionReplicationBuckets",
        "docker_credentials": "dockerCredentials",
        "docker_enabled_for_self_mutation": "dockerEnabledForSelfMutation",
        "docker_enabled_for_synth": "dockerEnabledForSynth",
        "enable_key_rotation": "enableKeyRotation",
        "pipeline_name": "pipelineName",
        "publish_assets_in_parallel": "publishAssetsInParallel",
        "reuse_cross_region_support_stacks": "reuseCrossRegionSupportStacks",
        "role": "role",
        "self_mutation": "selfMutation",
        "self_mutation_code_build_defaults": "selfMutationCodeBuildDefaults",
        "synth": "synth",
        "synth_code_build_defaults": "synthCodeBuildDefaults",
        "use_change_sets": "useChangeSets",
        "primary_synth_directory": "primarySynthDirectory",
        "repository_name": "repositoryName",
        "branch_name_prefixes": "branchNamePrefixes",
        "cdk_command": "cdkCommand",
        "cdk_src_dir": "cdkSrcDir",
        "code_commit_removal_policy": "codeCommitRemovalPolicy",
        "code_commit_repository": "codeCommitRepository",
        "default_branch_name": "defaultBranchName",
        "sonar_code_scanner_config": "sonarCodeScannerConfig",
        "synth_shell_step_partial_props": "synthShellStepPartialProps",
    },
)
class PDKPipelineProps(CodePipelineProps):
    def __init__(
        self,
        *,
        artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cli_version: typing.Optional[builtins.str] = None,
        code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
        docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
        docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
        reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        self_mutation: typing.Optional[builtins.bool] = None,
        self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
        synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        use_change_sets: typing.Optional[builtins.bool] = None,
        primary_synth_directory: builtins.str,
        repository_name: builtins.str,
        branch_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command: typing.Optional[builtins.str] = None,
        cdk_src_dir: typing.Optional[builtins.str] = None,
        code_commit_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        code_commit_repository: typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository] = None,
        default_branch_name: typing.Optional[builtins.str] = None,
        sonar_code_scanner_config: typing.Optional[typing.Union["SonarCodeScannerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        synth_shell_step_partial_props: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.ShellStepProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties to configure the PDKPipeline with CodeCommit as source.

        Note: Due to limitations with JSII and generic support it should be noted that
        the synth, synthShellStepPartialProps.input and
        synthShellStepPartialProps.primaryOutputDirectory properties will be ignored
        if passed in to this construct.

        synthShellStepPartialProps.commands is marked as a required field, however
        if you pass in [] the default commands of this construct will be retained.

        :param artifact_bucket: An existing S3 Bucket to use for storing the pipeline's artifact. Default: - A new S3 bucket will be created.
        :param asset_publishing_code_build_defaults: Additional customizations to apply to the asset publishing CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param cli_version: CDK CLI version to use in self-mutation and asset publishing steps. If you want to lock the CDK CLI version used in the pipeline, by steps that are automatically generated for you, specify the version here. We recommend you do not specify this value, as not specifying it always uses the latest CLI version which is backwards compatible with old versions. If you do specify it, be aware that this version should always be equal to or higher than the version of the CDK framework used by the CDK app, when the CDK commands are run during your pipeline execution. When you change this version, the *next time* the ``SelfMutate`` step runs it will still be using the CLI of the the *previous* version that was in this property: it will only start using the new version after ``SelfMutate`` completes successfully. That means that if you want to update both framework and CLI version, you should update the CLI version first, commit, push and deploy, and only then update the framework version. Default: - Latest version
        :param code_build_defaults: Customize the CodeBuild projects created for this pipeline. Default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_7_0
        :param code_pipeline: An existing Pipeline to be reused and built upon. [disable-awslint:ref-via-interface] Default: - a new underlying pipeline is created.
        :param cross_account_keys: Create KMS keys for the artifact buckets, allowing cross-account deployments. The artifact buckets have to be encrypted to support deploying CDK apps to another account, so if you want to do that or want to have your artifact buckets encrypted, be sure to set this value to ``true``. Be aware there is a cost associated with maintaining the KMS keys. Default: false
        :param cross_region_replication_buckets: A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region. Passed directly through to the {@link cp.Pipeline }. Default: - no cross region replication buckets.
        :param docker_credentials: A list of credentials used to authenticate to Docker registries. Specify any credentials necessary within the pipeline to build, synth, update, or publish assets. Default: []
        :param docker_enabled_for_self_mutation: Enable Docker for the self-mutate step. Set this to true if the pipeline itself uses Docker container assets (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build image of a CodeBuild step in the pipeline). You do not need to set it if you build Docker image assets in the application Stages and Stacks that are *deployed* by this pipeline. Configures privileged mode for the self-mutation CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the Docker asset in the pipeline. Default: false
        :param docker_enabled_for_synth: Enable Docker for the 'synth' step. Set this to true if you are using file assets that require "bundling" anywhere in your application (meaning an asset compilation step will be run with the tools provided by a Docker image), both for the Pipeline stack as well as the application stacks. A common way to use bundling assets in your application is by using the ``aws-cdk-lib/aws-lambda-nodejs`` library. Configures privileged mode for the synth CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the bundled asset. Default: false
        :param enable_key_rotation: Enable KMS key rotation for the generated KMS keys. By default KMS key rotation is disabled, but will add additional costs when enabled. Default: - false (key rotation is disabled)
        :param pipeline_name: The name of the CodePipeline pipeline. Default: - Automatically generated
        :param publish_assets_in_parallel: Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets. Publishing in parallel improves concurrency and may reduce publishing latency, but may also increase overall provisioning time of the CodeBuild projects. Experiment and see what value works best for you. Default: true
        :param reuse_cross_region_support_stacks: Reuse the same cross region support stack for all pipelines in the App. Default: - true (Use the same support stack for all pipelines in App)
        :param role: The IAM role to be assumed by this Pipeline. Default: - A new role is created
        :param self_mutation: Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param self_mutation_code_build_defaults: Additional customizations to apply to the self mutation CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param synth: The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        :param synth_code_build_defaults: Additional customizations to apply to the synthesize CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param use_change_sets: Deploy every stack by creating a change set and executing it. When enabled, creates a "Prepare" and "Execute" action for each stack. Disable to deploy the stack in one pipeline action. Default: true
        :param primary_synth_directory: Output directory for cdk synthesized artifacts i.e: packages/infra/cdk.out.
        :param repository_name: Name of the CodeCommit repository to create.
        :param branch_name_prefixes: Branch name prefixes Any branches created matching this list of prefixes will create a new pipeline and stack. Default: undefined
        :param cdk_command: CDK command. Override the command used to call cdk for synth and deploy. Default: 'npx cdk'
        :param cdk_src_dir: The directory with ``cdk.json`` to run cdk synth from. Set this if you enabled feature branches and ``cdk.json`` is not located in the parent directory of ``primarySynthDirectory``. Default: The parent directory of ``primarySynthDirectory``
        :param code_commit_removal_policy: Possible values for a resource's Removal Policy The removal policy controls what happens to the resource if it stops being managed by CloudFormation.
        :param code_commit_repository: The repository to add the pipeline to.
        :param default_branch_name: Branch to trigger the pipeline execution. Default: mainline
        :param sonar_code_scanner_config: Configuration for enabling Sonarqube code scanning on a successful synth. Default: undefined
        :param synth_shell_step_partial_props: PDKPipeline by default assumes a NX Monorepo structure for it's codebase and uses sane defaults for the install and run commands. To override these defaults and/or provide additional inputs, specify env settings, etc you can provide a partial ShellStepProps.
        '''
        if isinstance(asset_publishing_code_build_defaults, dict):
            asset_publishing_code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**asset_publishing_code_build_defaults)
        if isinstance(code_build_defaults, dict):
            code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**code_build_defaults)
        if isinstance(self_mutation_code_build_defaults, dict):
            self_mutation_code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**self_mutation_code_build_defaults)
        if isinstance(synth_code_build_defaults, dict):
            synth_code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**synth_code_build_defaults)
        if isinstance(sonar_code_scanner_config, dict):
            sonar_code_scanner_config = SonarCodeScannerConfig(**sonar_code_scanner_config)
        if isinstance(synth_shell_step_partial_props, dict):
            synth_shell_step_partial_props = _aws_cdk_pipelines_ceddda9d.ShellStepProps(**synth_shell_step_partial_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2347ec2a52a4becace9d89a95498a999fea5998347cde10b8a43bc88a33bbc3e)
            check_type(argname="argument artifact_bucket", value=artifact_bucket, expected_type=type_hints["artifact_bucket"])
            check_type(argname="argument asset_publishing_code_build_defaults", value=asset_publishing_code_build_defaults, expected_type=type_hints["asset_publishing_code_build_defaults"])
            check_type(argname="argument cli_version", value=cli_version, expected_type=type_hints["cli_version"])
            check_type(argname="argument code_build_defaults", value=code_build_defaults, expected_type=type_hints["code_build_defaults"])
            check_type(argname="argument code_pipeline", value=code_pipeline, expected_type=type_hints["code_pipeline"])
            check_type(argname="argument cross_account_keys", value=cross_account_keys, expected_type=type_hints["cross_account_keys"])
            check_type(argname="argument cross_region_replication_buckets", value=cross_region_replication_buckets, expected_type=type_hints["cross_region_replication_buckets"])
            check_type(argname="argument docker_credentials", value=docker_credentials, expected_type=type_hints["docker_credentials"])
            check_type(argname="argument docker_enabled_for_self_mutation", value=docker_enabled_for_self_mutation, expected_type=type_hints["docker_enabled_for_self_mutation"])
            check_type(argname="argument docker_enabled_for_synth", value=docker_enabled_for_synth, expected_type=type_hints["docker_enabled_for_synth"])
            check_type(argname="argument enable_key_rotation", value=enable_key_rotation, expected_type=type_hints["enable_key_rotation"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument publish_assets_in_parallel", value=publish_assets_in_parallel, expected_type=type_hints["publish_assets_in_parallel"])
            check_type(argname="argument reuse_cross_region_support_stacks", value=reuse_cross_region_support_stacks, expected_type=type_hints["reuse_cross_region_support_stacks"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument self_mutation", value=self_mutation, expected_type=type_hints["self_mutation"])
            check_type(argname="argument self_mutation_code_build_defaults", value=self_mutation_code_build_defaults, expected_type=type_hints["self_mutation_code_build_defaults"])
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
            check_type(argname="argument synth_code_build_defaults", value=synth_code_build_defaults, expected_type=type_hints["synth_code_build_defaults"])
            check_type(argname="argument use_change_sets", value=use_change_sets, expected_type=type_hints["use_change_sets"])
            check_type(argname="argument primary_synth_directory", value=primary_synth_directory, expected_type=type_hints["primary_synth_directory"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument branch_name_prefixes", value=branch_name_prefixes, expected_type=type_hints["branch_name_prefixes"])
            check_type(argname="argument cdk_command", value=cdk_command, expected_type=type_hints["cdk_command"])
            check_type(argname="argument cdk_src_dir", value=cdk_src_dir, expected_type=type_hints["cdk_src_dir"])
            check_type(argname="argument code_commit_removal_policy", value=code_commit_removal_policy, expected_type=type_hints["code_commit_removal_policy"])
            check_type(argname="argument code_commit_repository", value=code_commit_repository, expected_type=type_hints["code_commit_repository"])
            check_type(argname="argument default_branch_name", value=default_branch_name, expected_type=type_hints["default_branch_name"])
            check_type(argname="argument sonar_code_scanner_config", value=sonar_code_scanner_config, expected_type=type_hints["sonar_code_scanner_config"])
            check_type(argname="argument synth_shell_step_partial_props", value=synth_shell_step_partial_props, expected_type=type_hints["synth_shell_step_partial_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "primary_synth_directory": primary_synth_directory,
            "repository_name": repository_name,
        }
        if artifact_bucket is not None:
            self._values["artifact_bucket"] = artifact_bucket
        if asset_publishing_code_build_defaults is not None:
            self._values["asset_publishing_code_build_defaults"] = asset_publishing_code_build_defaults
        if cli_version is not None:
            self._values["cli_version"] = cli_version
        if code_build_defaults is not None:
            self._values["code_build_defaults"] = code_build_defaults
        if code_pipeline is not None:
            self._values["code_pipeline"] = code_pipeline
        if cross_account_keys is not None:
            self._values["cross_account_keys"] = cross_account_keys
        if cross_region_replication_buckets is not None:
            self._values["cross_region_replication_buckets"] = cross_region_replication_buckets
        if docker_credentials is not None:
            self._values["docker_credentials"] = docker_credentials
        if docker_enabled_for_self_mutation is not None:
            self._values["docker_enabled_for_self_mutation"] = docker_enabled_for_self_mutation
        if docker_enabled_for_synth is not None:
            self._values["docker_enabled_for_synth"] = docker_enabled_for_synth
        if enable_key_rotation is not None:
            self._values["enable_key_rotation"] = enable_key_rotation
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if publish_assets_in_parallel is not None:
            self._values["publish_assets_in_parallel"] = publish_assets_in_parallel
        if reuse_cross_region_support_stacks is not None:
            self._values["reuse_cross_region_support_stacks"] = reuse_cross_region_support_stacks
        if role is not None:
            self._values["role"] = role
        if self_mutation is not None:
            self._values["self_mutation"] = self_mutation
        if self_mutation_code_build_defaults is not None:
            self._values["self_mutation_code_build_defaults"] = self_mutation_code_build_defaults
        if synth is not None:
            self._values["synth"] = synth
        if synth_code_build_defaults is not None:
            self._values["synth_code_build_defaults"] = synth_code_build_defaults
        if use_change_sets is not None:
            self._values["use_change_sets"] = use_change_sets
        if branch_name_prefixes is not None:
            self._values["branch_name_prefixes"] = branch_name_prefixes
        if cdk_command is not None:
            self._values["cdk_command"] = cdk_command
        if cdk_src_dir is not None:
            self._values["cdk_src_dir"] = cdk_src_dir
        if code_commit_removal_policy is not None:
            self._values["code_commit_removal_policy"] = code_commit_removal_policy
        if code_commit_repository is not None:
            self._values["code_commit_repository"] = code_commit_repository
        if default_branch_name is not None:
            self._values["default_branch_name"] = default_branch_name
        if sonar_code_scanner_config is not None:
            self._values["sonar_code_scanner_config"] = sonar_code_scanner_config
        if synth_shell_step_partial_props is not None:
            self._values["synth_shell_step_partial_props"] = synth_shell_step_partial_props

    @builtins.property
    def artifact_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''An existing S3 Bucket to use for storing the pipeline's artifact.

        :default: - A new S3 bucket will be created.
        '''
        result = self._values.get("artifact_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def asset_publishing_code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Additional customizations to apply to the asset publishing CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied
        '''
        result = self._values.get("asset_publishing_code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def cli_version(self) -> typing.Optional[builtins.str]:
        '''CDK CLI version to use in self-mutation and asset publishing steps.

        If you want to lock the CDK CLI version used in the pipeline, by steps
        that are automatically generated for you, specify the version here.

        We recommend you do not specify this value, as not specifying it always
        uses the latest CLI version which is backwards compatible with old versions.

        If you do specify it, be aware that this version should always be equal to or higher than the
        version of the CDK framework used by the CDK app, when the CDK commands are
        run during your pipeline execution. When you change this version, the *next
        time* the ``SelfMutate`` step runs it will still be using the CLI of the the
        *previous* version that was in this property: it will only start using the
        new version after ``SelfMutate`` completes successfully. That means that if
        you want to update both framework and CLI version, you should update the
        CLI version first, commit, push and deploy, and only then update the
        framework version.

        :default: - Latest version
        '''
        result = self._values.get("cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Customize the CodeBuild projects created for this pipeline.

        :default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_7_0
        '''
        result = self._values.get("code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def code_pipeline(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline]:
        '''An existing Pipeline to be reused and built upon.

        [disable-awslint:ref-via-interface]

        :default: - a new underlying pipeline is created.
        '''
        result = self._values.get("code_pipeline")
        return typing.cast(typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline], result)

    @builtins.property
    def cross_account_keys(self) -> typing.Optional[builtins.bool]:
        '''Create KMS keys for the artifact buckets, allowing cross-account deployments.

        The artifact buckets have to be encrypted to support deploying CDK apps to
        another account, so if you want to do that or want to have your artifact
        buckets encrypted, be sure to set this value to ``true``.

        Be aware there is a cost associated with maintaining the KMS keys.

        :default: false
        '''
        result = self._values.get("cross_account_keys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_replication_buckets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]]:
        '''A map of region to S3 bucket name used for cross-region CodePipeline.

        For every Action that you specify targeting a different region than the Pipeline itself,
        if you don't provide an explicit Bucket for that region using this property,
        the construct will automatically create a Stack containing an S3 Bucket in that region.
        Passed directly through to the {@link cp.Pipeline }.

        :default: - no cross region replication buckets.
        '''
        result = self._values.get("cross_region_replication_buckets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]], result)

    @builtins.property
    def docker_credentials(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.DockerCredential]]:
        '''A list of credentials used to authenticate to Docker registries.

        Specify any credentials necessary within the pipeline to build, synth, update, or publish assets.

        :default: []
        '''
        result = self._values.get("docker_credentials")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.DockerCredential]], result)

    @builtins.property
    def docker_enabled_for_self_mutation(self) -> typing.Optional[builtins.bool]:
        '''Enable Docker for the self-mutate step.

        Set this to true if the pipeline itself uses Docker container assets
        (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build
        image of a CodeBuild step in the pipeline).

        You do not need to set it if you build Docker image assets in the
        application Stages and Stacks that are *deployed* by this pipeline.

        Configures privileged mode for the self-mutation CodeBuild action.

        If you are about to turn this on in an already-deployed Pipeline,
        set the value to ``true`` first, commit and allow the pipeline to
        self-update, and only then use the Docker asset in the pipeline.

        :default: false
        '''
        result = self._values.get("docker_enabled_for_self_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docker_enabled_for_synth(self) -> typing.Optional[builtins.bool]:
        '''Enable Docker for the 'synth' step.

        Set this to true if you are using file assets that require
        "bundling" anywhere in your application (meaning an asset
        compilation step will be run with the tools provided by
        a Docker image), both for the Pipeline stack as well as the
        application stacks.

        A common way to use bundling assets in your application is by
        using the ``aws-cdk-lib/aws-lambda-nodejs`` library.

        Configures privileged mode for the synth CodeBuild action.

        If you are about to turn this on in an already-deployed Pipeline,
        set the value to ``true`` first, commit and allow the pipeline to
        self-update, and only then use the bundled asset.

        :default: false
        '''
        result = self._values.get("docker_enabled_for_synth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_key_rotation(self) -> typing.Optional[builtins.bool]:
        '''Enable KMS key rotation for the generated KMS keys.

        By default KMS key rotation is disabled, but will add
        additional costs when enabled.

        :default: - false (key rotation is disabled)
        '''
        result = self._values.get("enable_key_rotation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        '''The name of the CodePipeline pipeline.

        :default: - Automatically generated
        '''
        result = self._values.get("pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_assets_in_parallel(self) -> typing.Optional[builtins.bool]:
        '''Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets.

        Publishing in parallel improves concurrency and may reduce publishing
        latency, but may also increase overall provisioning time of the CodeBuild
        projects.

        Experiment and see what value works best for you.

        :default: true
        '''
        result = self._values.get("publish_assets_in_parallel")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reuse_cross_region_support_stacks(self) -> typing.Optional[builtins.bool]:
        '''Reuse the same cross region support stack for all pipelines in the App.

        :default: - true (Use the same support stack for all pipelines in App)
        '''
        result = self._values.get("reuse_cross_region_support_stacks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The IAM role to be assumed by this Pipeline.

        :default: - A new role is created
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def self_mutation(self) -> typing.Optional[builtins.bool]:
        '''Whether the pipeline will update itself.

        This needs to be set to ``true`` to allow the pipeline to reconfigure
        itself when assets or stages are being added to it, and ``true`` is the
        recommended setting.

        You can temporarily set this to ``false`` while you are iterating
        on the pipeline itself and prefer to deploy changes using ``cdk deploy``.

        :default: true
        '''
        result = self._values.get("self_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def self_mutation_code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Additional customizations to apply to the self mutation CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied
        '''
        result = self._values.get("self_mutation_code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def synth(self) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer]:
        '''The build step that produces the CDK Cloud Assembly.

        The primary output of this step needs to be the ``cdk.out`` directory
        generated by the ``cdk synth`` command.

        If you use a ``ShellStep`` here and you don't configure an output directory,
        the output directory will automatically be assumed to be ``cdk.out``.
        '''
        result = self._values.get("synth")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer], result)

    @builtins.property
    def synth_code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Additional customizations to apply to the synthesize CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied
        '''
        result = self._values.get("synth_code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def use_change_sets(self) -> typing.Optional[builtins.bool]:
        '''Deploy every stack by creating a change set and executing it.

        When enabled, creates a "Prepare" and "Execute" action for each stack. Disable
        to deploy the stack in one pipeline action.

        :default: true
        '''
        result = self._values.get("use_change_sets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def primary_synth_directory(self) -> builtins.str:
        '''Output directory for cdk synthesized artifacts i.e: packages/infra/cdk.out.'''
        result = self._values.get("primary_synth_directory")
        assert result is not None, "Required property 'primary_synth_directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''Name of the CodeCommit repository to create.'''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Branch name prefixes Any branches created matching this list of prefixes will create a new pipeline and stack.

        :default: undefined

        Example::

            // Disables feature branches (default)
            new PDKPipeline(this, 'PDKPipeline', {
              repositoryName: 'my-repo',
              branchNamePrefixes: [], // or simply exclude this line
            }
        '''
        result = self._values.get("branch_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command(self) -> typing.Optional[builtins.str]:
        '''CDK command.

        Override the command used to call cdk for synth and deploy.

        :default: 'npx cdk'
        '''
        result = self._values.get("cdk_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_src_dir(self) -> typing.Optional[builtins.str]:
        '''The directory with ``cdk.json`` to run cdk synth from. Set this if you enabled feature branches and ``cdk.json`` is not located in the parent directory of ``primarySynthDirectory``.

        :default: The parent directory of ``primarySynthDirectory``
        '''
        result = self._values.get("cdk_src_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_commit_removal_policy(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Possible values for a resource's Removal Policy The removal policy controls what happens to the resource if it stops being managed by CloudFormation.'''
        result = self._values.get("code_commit_removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def code_commit_repository(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository]:
        '''The repository to add the pipeline to.'''
        result = self._values.get("code_commit_repository")
        return typing.cast(typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository], result)

    @builtins.property
    def default_branch_name(self) -> typing.Optional[builtins.str]:
        '''Branch to trigger the pipeline execution.

        :default: mainline
        '''
        result = self._values.get("default_branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sonar_code_scanner_config(self) -> typing.Optional["SonarCodeScannerConfig"]:
        '''Configuration for enabling Sonarqube code scanning on a successful synth.

        :default: undefined
        '''
        result = self._values.get("sonar_code_scanner_config")
        return typing.cast(typing.Optional["SonarCodeScannerConfig"], result)

    @builtins.property
    def synth_shell_step_partial_props(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.ShellStepProps]:
        '''PDKPipeline by default assumes a NX Monorepo structure for it's codebase and uses sane defaults for the install and run commands.

        To override these defaults
        and/or provide additional inputs, specify env settings, etc you can provide
        a partial ShellStepProps.
        '''
        result = self._values.get("synth_shell_step_partial_props")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.ShellStepProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PDKPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PDKPipelineWithCodeConnection(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.pipeline.PDKPipelineWithCodeConnection",
):
    '''An extension to CodePipeline which configures same defaults for a NX Monorepo and using a AWS CodeConnections as source.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        code_connection_arn: builtins.str,
        primary_synth_directory: builtins.str,
        repository_owner_and_name: builtins.str,
        cdk_command: typing.Optional[builtins.str] = None,
        cdk_src_dir: typing.Optional[builtins.str] = None,
        default_branch_name: typing.Optional[builtins.str] = None,
        sonar_code_scanner_config: typing.Optional[typing.Union["SonarCodeScannerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        synth_shell_step_partial_props: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.ShellStepProps, typing.Dict[builtins.str, typing.Any]]] = None,
        artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cli_version: typing.Optional[builtins.str] = None,
        code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
        docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
        docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
        reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        self_mutation: typing.Optional[builtins.bool] = None,
        self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
        synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        use_change_sets: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param code_connection_arn: The Arn of the CodeConnection.
        :param primary_synth_directory: Output directory for cdk synthesized artifacts i.e: packages/infra/cdk.out.
        :param repository_owner_and_name: The Owner and Repository name for instance, user Bob with git repository ACME becomes "Bob/ACME".
        :param cdk_command: CDK command. Override the command used to call cdk for synth and deploy. Default: 'npx cdk'
        :param cdk_src_dir: The directory with ``cdk.json`` to run cdk synth from. Set this if you enabled feature branches and ``cdk.json`` is not located in the parent directory of ``primarySynthDirectory``. Default: The parent directory of ``primarySynthDirectory``
        :param default_branch_name: Branch to trigger the pipeline execution. Default: mainline
        :param sonar_code_scanner_config: Configuration for enabling Sonarqube code scanning on a successful synth. Default: undefined
        :param synth_shell_step_partial_props: PDKPipeline by default assumes a NX Monorepo structure for it's codebase and uses sane defaults for the install and run commands. To override these defaults and/or provide additional inputs, specify env settings, etc you can provide a partial ShellStepProps.
        :param artifact_bucket: An existing S3 Bucket to use for storing the pipeline's artifact. Default: - A new S3 bucket will be created.
        :param asset_publishing_code_build_defaults: Additional customizations to apply to the asset publishing CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param cli_version: CDK CLI version to use in self-mutation and asset publishing steps. If you want to lock the CDK CLI version used in the pipeline, by steps that are automatically generated for you, specify the version here. We recommend you do not specify this value, as not specifying it always uses the latest CLI version which is backwards compatible with old versions. If you do specify it, be aware that this version should always be equal to or higher than the version of the CDK framework used by the CDK app, when the CDK commands are run during your pipeline execution. When you change this version, the *next time* the ``SelfMutate`` step runs it will still be using the CLI of the the *previous* version that was in this property: it will only start using the new version after ``SelfMutate`` completes successfully. That means that if you want to update both framework and CLI version, you should update the CLI version first, commit, push and deploy, and only then update the framework version. Default: - Latest version
        :param code_build_defaults: Customize the CodeBuild projects created for this pipeline. Default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_7_0
        :param code_pipeline: An existing Pipeline to be reused and built upon. [disable-awslint:ref-via-interface] Default: - a new underlying pipeline is created.
        :param cross_account_keys: Create KMS keys for the artifact buckets, allowing cross-account deployments. The artifact buckets have to be encrypted to support deploying CDK apps to another account, so if you want to do that or want to have your artifact buckets encrypted, be sure to set this value to ``true``. Be aware there is a cost associated with maintaining the KMS keys. Default: false
        :param cross_region_replication_buckets: A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region. Passed directly through to the {@link cp.Pipeline }. Default: - no cross region replication buckets.
        :param docker_credentials: A list of credentials used to authenticate to Docker registries. Specify any credentials necessary within the pipeline to build, synth, update, or publish assets. Default: []
        :param docker_enabled_for_self_mutation: Enable Docker for the self-mutate step. Set this to true if the pipeline itself uses Docker container assets (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build image of a CodeBuild step in the pipeline). You do not need to set it if you build Docker image assets in the application Stages and Stacks that are *deployed* by this pipeline. Configures privileged mode for the self-mutation CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the Docker asset in the pipeline. Default: false
        :param docker_enabled_for_synth: Enable Docker for the 'synth' step. Set this to true if you are using file assets that require "bundling" anywhere in your application (meaning an asset compilation step will be run with the tools provided by a Docker image), both for the Pipeline stack as well as the application stacks. A common way to use bundling assets in your application is by using the ``aws-cdk-lib/aws-lambda-nodejs`` library. Configures privileged mode for the synth CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the bundled asset. Default: false
        :param enable_key_rotation: Enable KMS key rotation for the generated KMS keys. By default KMS key rotation is disabled, but will add additional costs when enabled. Default: - false (key rotation is disabled)
        :param pipeline_name: The name of the CodePipeline pipeline. Default: - Automatically generated
        :param publish_assets_in_parallel: Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets. Publishing in parallel improves concurrency and may reduce publishing latency, but may also increase overall provisioning time of the CodeBuild projects. Experiment and see what value works best for you. Default: true
        :param reuse_cross_region_support_stacks: Reuse the same cross region support stack for all pipelines in the App. Default: - true (Use the same support stack for all pipelines in App)
        :param role: The IAM role to be assumed by this Pipeline. Default: - A new role is created
        :param self_mutation: Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param self_mutation_code_build_defaults: Additional customizations to apply to the self mutation CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param synth: The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        :param synth_code_build_defaults: Additional customizations to apply to the synthesize CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param use_change_sets: Deploy every stack by creating a change set and executing it. When enabled, creates a "Prepare" and "Execute" action for each stack. Disable to deploy the stack in one pipeline action. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f18b2a44c7e3c2ea97323a8a8eaa0d9f38f23517ebf3d64569cf2d478f6fd3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PDKPipelineWithCodeConnectionProps(
            code_connection_arn=code_connection_arn,
            primary_synth_directory=primary_synth_directory,
            repository_owner_and_name=repository_owner_and_name,
            cdk_command=cdk_command,
            cdk_src_dir=cdk_src_dir,
            default_branch_name=default_branch_name,
            sonar_code_scanner_config=sonar_code_scanner_config,
            synth_shell_step_partial_props=synth_shell_step_partial_props,
            artifact_bucket=artifact_bucket,
            asset_publishing_code_build_defaults=asset_publishing_code_build_defaults,
            cli_version=cli_version,
            code_build_defaults=code_build_defaults,
            code_pipeline=code_pipeline,
            cross_account_keys=cross_account_keys,
            cross_region_replication_buckets=cross_region_replication_buckets,
            docker_credentials=docker_credentials,
            docker_enabled_for_self_mutation=docker_enabled_for_self_mutation,
            docker_enabled_for_synth=docker_enabled_for_synth,
            enable_key_rotation=enable_key_rotation,
            pipeline_name=pipeline_name,
            publish_assets_in_parallel=publish_assets_in_parallel,
            reuse_cross_region_support_stacks=reuse_cross_region_support_stacks,
            role=role,
            self_mutation=self_mutation,
            self_mutation_code_build_defaults=self_mutation_code_build_defaults,
            synth=synth,
            synth_code_build_defaults=synth_code_build_defaults,
            use_change_sets=use_change_sets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getBranchPrefix")
    @builtins.classmethod
    def get_branch_prefix(
        cls,
        *,
        default_branch_name: typing.Optional[builtins.str] = None,
        node: typing.Optional[_constructs_77d1e7e8.Node] = None,
    ) -> builtins.str:
        '''A helper function to create a branch prefix.

        The prefix is empty on the default branch.

        :param default_branch_name: Specify the default branch name without context.
        :param node: The current node to fetch defaultBranchName from context.

        :return: The branch prefix.
        '''
        props = IsDefaultBranchProps(
            default_branch_name=default_branch_name, node=node
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "getBranchPrefix", [props]))

    @jsii.member(jsii_name="isDefaultBranch")
    @builtins.classmethod
    def is_default_branch(
        cls,
        *,
        default_branch_name: typing.Optional[builtins.str] = None,
        node: typing.Optional[_constructs_77d1e7e8.Node] = None,
    ) -> builtins.bool:
        '''A helper function to determine if the current branch is the default branch.

        If there is no BRANCH environment variable, then assume this is the default
        branch. Otherwise, check that BRANCH matches the default branch name.

        The default branch name is determined in the following priority:

        1. defaultBranchName property
        2. defaultBranchName context
        3. PDKPipeline.defaultBranchName constant

        :param default_branch_name: Specify the default branch name without context.
        :param node: The current node to fetch defaultBranchName from context.

        :return: True if the current branch is the default branch.
        '''
        props = IsDefaultBranchProps(
            default_branch_name=default_branch_name, node=node
        )

        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isDefaultBranch", [props]))

    @jsii.member(jsii_name="normalizeBranchName")
    @builtins.classmethod
    def normalize_branch_name(cls, branch_name: builtins.str) -> builtins.str:
        '''A helper function to normalize the branch name with only alphanumeric characters and hypens ('-').

        :param branch_name: The name of the branch to normalize.

        :return: The normalized branch name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49e5799c83007a10ebd29aa57e030002095ba8bc63eb901fcbf4fa847cd45a5)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "normalizeBranchName", [branch_name]))

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        stage: _aws_cdk_ceddda9d.Stage,
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _aws_cdk_pipelines_ceddda9d.StageDeployment:
        '''
        :param stage: -
        :param post: Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: Instructions for stack level steps. Default: - No additional instructions

        :inheritDoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fc478ffdf001ccc8638b25715631e842b68ebb45c6029faf66034b9a1a32bd)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = _aws_cdk_pipelines_ceddda9d.AddStageOpts(
            post=post, pre=pre, stack_steps=stack_steps
        )

        return typing.cast(_aws_cdk_pipelines_ceddda9d.StageDeployment, jsii.invoke(self, "addStage", [stage, options]))

    @jsii.member(jsii_name="buildPipeline")
    def build_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "buildPipeline", []))

    @jsii.member(jsii_name="suppressCDKViolations")
    def suppress_cdk_violations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "suppressCDKViolations", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_BRANCHES")
    def ALL_BRANCHES(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "ALL_BRANCHES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="defaultBranchName")
    def DEFAULT_BRANCH_NAME(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "defaultBranchName"))

    @builtins.property
    @jsii.member(jsii_name="codePipeline")
    def code_pipeline(self) -> _aws_cdk_pipelines_ceddda9d.CodePipeline:
        return typing.cast(_aws_cdk_pipelines_ceddda9d.CodePipeline, jsii.get(self, "codePipeline"))

    @builtins.property
    @jsii.member(jsii_name="codeRepository")
    def code_repository(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository]:
        return typing.cast(typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository], jsii.get(self, "codeRepository"))


@jsii.data_type(
    jsii_type="@aws/pdk.pipeline.PDKPipelineWithCodeConnectionProps",
    jsii_struct_bases=[CodePipelineProps],
    name_mapping={
        "artifact_bucket": "artifactBucket",
        "asset_publishing_code_build_defaults": "assetPublishingCodeBuildDefaults",
        "cli_version": "cliVersion",
        "code_build_defaults": "codeBuildDefaults",
        "code_pipeline": "codePipeline",
        "cross_account_keys": "crossAccountKeys",
        "cross_region_replication_buckets": "crossRegionReplicationBuckets",
        "docker_credentials": "dockerCredentials",
        "docker_enabled_for_self_mutation": "dockerEnabledForSelfMutation",
        "docker_enabled_for_synth": "dockerEnabledForSynth",
        "enable_key_rotation": "enableKeyRotation",
        "pipeline_name": "pipelineName",
        "publish_assets_in_parallel": "publishAssetsInParallel",
        "reuse_cross_region_support_stacks": "reuseCrossRegionSupportStacks",
        "role": "role",
        "self_mutation": "selfMutation",
        "self_mutation_code_build_defaults": "selfMutationCodeBuildDefaults",
        "synth": "synth",
        "synth_code_build_defaults": "synthCodeBuildDefaults",
        "use_change_sets": "useChangeSets",
        "code_connection_arn": "codeConnectionArn",
        "primary_synth_directory": "primarySynthDirectory",
        "repository_owner_and_name": "repositoryOwnerAndName",
        "cdk_command": "cdkCommand",
        "cdk_src_dir": "cdkSrcDir",
        "default_branch_name": "defaultBranchName",
        "sonar_code_scanner_config": "sonarCodeScannerConfig",
        "synth_shell_step_partial_props": "synthShellStepPartialProps",
    },
)
class PDKPipelineWithCodeConnectionProps(CodePipelineProps):
    def __init__(
        self,
        *,
        artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cli_version: typing.Optional[builtins.str] = None,
        code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
        docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
        docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
        reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        self_mutation: typing.Optional[builtins.bool] = None,
        self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
        synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        use_change_sets: typing.Optional[builtins.bool] = None,
        code_connection_arn: builtins.str,
        primary_synth_directory: builtins.str,
        repository_owner_and_name: builtins.str,
        cdk_command: typing.Optional[builtins.str] = None,
        cdk_src_dir: typing.Optional[builtins.str] = None,
        default_branch_name: typing.Optional[builtins.str] = None,
        sonar_code_scanner_config: typing.Optional[typing.Union["SonarCodeScannerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        synth_shell_step_partial_props: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.ShellStepProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties to configure the PDKPipeline with a CodeConnections as source.

        Note: Due to limitations with JSII and generic support it should be noted that
        the synth, synthShellStepPartialProps.input and
        synthShellStepPartialProps.primaryOutputDirectory properties will be ignored
        if passed in to this construct.

        synthShellStepPartialProps.commands is marked as a required field, however
        if you pass in [] the default commands of this construct will be retained.

        :param artifact_bucket: An existing S3 Bucket to use for storing the pipeline's artifact. Default: - A new S3 bucket will be created.
        :param asset_publishing_code_build_defaults: Additional customizations to apply to the asset publishing CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param cli_version: CDK CLI version to use in self-mutation and asset publishing steps. If you want to lock the CDK CLI version used in the pipeline, by steps that are automatically generated for you, specify the version here. We recommend you do not specify this value, as not specifying it always uses the latest CLI version which is backwards compatible with old versions. If you do specify it, be aware that this version should always be equal to or higher than the version of the CDK framework used by the CDK app, when the CDK commands are run during your pipeline execution. When you change this version, the *next time* the ``SelfMutate`` step runs it will still be using the CLI of the the *previous* version that was in this property: it will only start using the new version after ``SelfMutate`` completes successfully. That means that if you want to update both framework and CLI version, you should update the CLI version first, commit, push and deploy, and only then update the framework version. Default: - Latest version
        :param code_build_defaults: Customize the CodeBuild projects created for this pipeline. Default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_7_0
        :param code_pipeline: An existing Pipeline to be reused and built upon. [disable-awslint:ref-via-interface] Default: - a new underlying pipeline is created.
        :param cross_account_keys: Create KMS keys for the artifact buckets, allowing cross-account deployments. The artifact buckets have to be encrypted to support deploying CDK apps to another account, so if you want to do that or want to have your artifact buckets encrypted, be sure to set this value to ``true``. Be aware there is a cost associated with maintaining the KMS keys. Default: false
        :param cross_region_replication_buckets: A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region. Passed directly through to the {@link cp.Pipeline }. Default: - no cross region replication buckets.
        :param docker_credentials: A list of credentials used to authenticate to Docker registries. Specify any credentials necessary within the pipeline to build, synth, update, or publish assets. Default: []
        :param docker_enabled_for_self_mutation: Enable Docker for the self-mutate step. Set this to true if the pipeline itself uses Docker container assets (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build image of a CodeBuild step in the pipeline). You do not need to set it if you build Docker image assets in the application Stages and Stacks that are *deployed* by this pipeline. Configures privileged mode for the self-mutation CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the Docker asset in the pipeline. Default: false
        :param docker_enabled_for_synth: Enable Docker for the 'synth' step. Set this to true if you are using file assets that require "bundling" anywhere in your application (meaning an asset compilation step will be run with the tools provided by a Docker image), both for the Pipeline stack as well as the application stacks. A common way to use bundling assets in your application is by using the ``aws-cdk-lib/aws-lambda-nodejs`` library. Configures privileged mode for the synth CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the bundled asset. Default: false
        :param enable_key_rotation: Enable KMS key rotation for the generated KMS keys. By default KMS key rotation is disabled, but will add additional costs when enabled. Default: - false (key rotation is disabled)
        :param pipeline_name: The name of the CodePipeline pipeline. Default: - Automatically generated
        :param publish_assets_in_parallel: Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets. Publishing in parallel improves concurrency and may reduce publishing latency, but may also increase overall provisioning time of the CodeBuild projects. Experiment and see what value works best for you. Default: true
        :param reuse_cross_region_support_stacks: Reuse the same cross region support stack for all pipelines in the App. Default: - true (Use the same support stack for all pipelines in App)
        :param role: The IAM role to be assumed by this Pipeline. Default: - A new role is created
        :param self_mutation: Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param self_mutation_code_build_defaults: Additional customizations to apply to the self mutation CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param synth: The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        :param synth_code_build_defaults: Additional customizations to apply to the synthesize CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param use_change_sets: Deploy every stack by creating a change set and executing it. When enabled, creates a "Prepare" and "Execute" action for each stack. Disable to deploy the stack in one pipeline action. Default: true
        :param code_connection_arn: The Arn of the CodeConnection.
        :param primary_synth_directory: Output directory for cdk synthesized artifacts i.e: packages/infra/cdk.out.
        :param repository_owner_and_name: The Owner and Repository name for instance, user Bob with git repository ACME becomes "Bob/ACME".
        :param cdk_command: CDK command. Override the command used to call cdk for synth and deploy. Default: 'npx cdk'
        :param cdk_src_dir: The directory with ``cdk.json`` to run cdk synth from. Set this if you enabled feature branches and ``cdk.json`` is not located in the parent directory of ``primarySynthDirectory``. Default: The parent directory of ``primarySynthDirectory``
        :param default_branch_name: Branch to trigger the pipeline execution. Default: mainline
        :param sonar_code_scanner_config: Configuration for enabling Sonarqube code scanning on a successful synth. Default: undefined
        :param synth_shell_step_partial_props: PDKPipeline by default assumes a NX Monorepo structure for it's codebase and uses sane defaults for the install and run commands. To override these defaults and/or provide additional inputs, specify env settings, etc you can provide a partial ShellStepProps.
        '''
        if isinstance(asset_publishing_code_build_defaults, dict):
            asset_publishing_code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**asset_publishing_code_build_defaults)
        if isinstance(code_build_defaults, dict):
            code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**code_build_defaults)
        if isinstance(self_mutation_code_build_defaults, dict):
            self_mutation_code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**self_mutation_code_build_defaults)
        if isinstance(synth_code_build_defaults, dict):
            synth_code_build_defaults = _aws_cdk_pipelines_ceddda9d.CodeBuildOptions(**synth_code_build_defaults)
        if isinstance(sonar_code_scanner_config, dict):
            sonar_code_scanner_config = SonarCodeScannerConfig(**sonar_code_scanner_config)
        if isinstance(synth_shell_step_partial_props, dict):
            synth_shell_step_partial_props = _aws_cdk_pipelines_ceddda9d.ShellStepProps(**synth_shell_step_partial_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a853ce5a4054d1ccf4a1609847820cdbb922828725b4385b74c0f1d624a10550)
            check_type(argname="argument artifact_bucket", value=artifact_bucket, expected_type=type_hints["artifact_bucket"])
            check_type(argname="argument asset_publishing_code_build_defaults", value=asset_publishing_code_build_defaults, expected_type=type_hints["asset_publishing_code_build_defaults"])
            check_type(argname="argument cli_version", value=cli_version, expected_type=type_hints["cli_version"])
            check_type(argname="argument code_build_defaults", value=code_build_defaults, expected_type=type_hints["code_build_defaults"])
            check_type(argname="argument code_pipeline", value=code_pipeline, expected_type=type_hints["code_pipeline"])
            check_type(argname="argument cross_account_keys", value=cross_account_keys, expected_type=type_hints["cross_account_keys"])
            check_type(argname="argument cross_region_replication_buckets", value=cross_region_replication_buckets, expected_type=type_hints["cross_region_replication_buckets"])
            check_type(argname="argument docker_credentials", value=docker_credentials, expected_type=type_hints["docker_credentials"])
            check_type(argname="argument docker_enabled_for_self_mutation", value=docker_enabled_for_self_mutation, expected_type=type_hints["docker_enabled_for_self_mutation"])
            check_type(argname="argument docker_enabled_for_synth", value=docker_enabled_for_synth, expected_type=type_hints["docker_enabled_for_synth"])
            check_type(argname="argument enable_key_rotation", value=enable_key_rotation, expected_type=type_hints["enable_key_rotation"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument publish_assets_in_parallel", value=publish_assets_in_parallel, expected_type=type_hints["publish_assets_in_parallel"])
            check_type(argname="argument reuse_cross_region_support_stacks", value=reuse_cross_region_support_stacks, expected_type=type_hints["reuse_cross_region_support_stacks"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument self_mutation", value=self_mutation, expected_type=type_hints["self_mutation"])
            check_type(argname="argument self_mutation_code_build_defaults", value=self_mutation_code_build_defaults, expected_type=type_hints["self_mutation_code_build_defaults"])
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
            check_type(argname="argument synth_code_build_defaults", value=synth_code_build_defaults, expected_type=type_hints["synth_code_build_defaults"])
            check_type(argname="argument use_change_sets", value=use_change_sets, expected_type=type_hints["use_change_sets"])
            check_type(argname="argument code_connection_arn", value=code_connection_arn, expected_type=type_hints["code_connection_arn"])
            check_type(argname="argument primary_synth_directory", value=primary_synth_directory, expected_type=type_hints["primary_synth_directory"])
            check_type(argname="argument repository_owner_and_name", value=repository_owner_and_name, expected_type=type_hints["repository_owner_and_name"])
            check_type(argname="argument cdk_command", value=cdk_command, expected_type=type_hints["cdk_command"])
            check_type(argname="argument cdk_src_dir", value=cdk_src_dir, expected_type=type_hints["cdk_src_dir"])
            check_type(argname="argument default_branch_name", value=default_branch_name, expected_type=type_hints["default_branch_name"])
            check_type(argname="argument sonar_code_scanner_config", value=sonar_code_scanner_config, expected_type=type_hints["sonar_code_scanner_config"])
            check_type(argname="argument synth_shell_step_partial_props", value=synth_shell_step_partial_props, expected_type=type_hints["synth_shell_step_partial_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code_connection_arn": code_connection_arn,
            "primary_synth_directory": primary_synth_directory,
            "repository_owner_and_name": repository_owner_and_name,
        }
        if artifact_bucket is not None:
            self._values["artifact_bucket"] = artifact_bucket
        if asset_publishing_code_build_defaults is not None:
            self._values["asset_publishing_code_build_defaults"] = asset_publishing_code_build_defaults
        if cli_version is not None:
            self._values["cli_version"] = cli_version
        if code_build_defaults is not None:
            self._values["code_build_defaults"] = code_build_defaults
        if code_pipeline is not None:
            self._values["code_pipeline"] = code_pipeline
        if cross_account_keys is not None:
            self._values["cross_account_keys"] = cross_account_keys
        if cross_region_replication_buckets is not None:
            self._values["cross_region_replication_buckets"] = cross_region_replication_buckets
        if docker_credentials is not None:
            self._values["docker_credentials"] = docker_credentials
        if docker_enabled_for_self_mutation is not None:
            self._values["docker_enabled_for_self_mutation"] = docker_enabled_for_self_mutation
        if docker_enabled_for_synth is not None:
            self._values["docker_enabled_for_synth"] = docker_enabled_for_synth
        if enable_key_rotation is not None:
            self._values["enable_key_rotation"] = enable_key_rotation
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if publish_assets_in_parallel is not None:
            self._values["publish_assets_in_parallel"] = publish_assets_in_parallel
        if reuse_cross_region_support_stacks is not None:
            self._values["reuse_cross_region_support_stacks"] = reuse_cross_region_support_stacks
        if role is not None:
            self._values["role"] = role
        if self_mutation is not None:
            self._values["self_mutation"] = self_mutation
        if self_mutation_code_build_defaults is not None:
            self._values["self_mutation_code_build_defaults"] = self_mutation_code_build_defaults
        if synth is not None:
            self._values["synth"] = synth
        if synth_code_build_defaults is not None:
            self._values["synth_code_build_defaults"] = synth_code_build_defaults
        if use_change_sets is not None:
            self._values["use_change_sets"] = use_change_sets
        if cdk_command is not None:
            self._values["cdk_command"] = cdk_command
        if cdk_src_dir is not None:
            self._values["cdk_src_dir"] = cdk_src_dir
        if default_branch_name is not None:
            self._values["default_branch_name"] = default_branch_name
        if sonar_code_scanner_config is not None:
            self._values["sonar_code_scanner_config"] = sonar_code_scanner_config
        if synth_shell_step_partial_props is not None:
            self._values["synth_shell_step_partial_props"] = synth_shell_step_partial_props

    @builtins.property
    def artifact_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''An existing S3 Bucket to use for storing the pipeline's artifact.

        :default: - A new S3 bucket will be created.
        '''
        result = self._values.get("artifact_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def asset_publishing_code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Additional customizations to apply to the asset publishing CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied
        '''
        result = self._values.get("asset_publishing_code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def cli_version(self) -> typing.Optional[builtins.str]:
        '''CDK CLI version to use in self-mutation and asset publishing steps.

        If you want to lock the CDK CLI version used in the pipeline, by steps
        that are automatically generated for you, specify the version here.

        We recommend you do not specify this value, as not specifying it always
        uses the latest CLI version which is backwards compatible with old versions.

        If you do specify it, be aware that this version should always be equal to or higher than the
        version of the CDK framework used by the CDK app, when the CDK commands are
        run during your pipeline execution. When you change this version, the *next
        time* the ``SelfMutate`` step runs it will still be using the CLI of the the
        *previous* version that was in this property: it will only start using the
        new version after ``SelfMutate`` completes successfully. That means that if
        you want to update both framework and CLI version, you should update the
        CLI version first, commit, push and deploy, and only then update the
        framework version.

        :default: - Latest version
        '''
        result = self._values.get("cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Customize the CodeBuild projects created for this pipeline.

        :default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_7_0
        '''
        result = self._values.get("code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def code_pipeline(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline]:
        '''An existing Pipeline to be reused and built upon.

        [disable-awslint:ref-via-interface]

        :default: - a new underlying pipeline is created.
        '''
        result = self._values.get("code_pipeline")
        return typing.cast(typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline], result)

    @builtins.property
    def cross_account_keys(self) -> typing.Optional[builtins.bool]:
        '''Create KMS keys for the artifact buckets, allowing cross-account deployments.

        The artifact buckets have to be encrypted to support deploying CDK apps to
        another account, so if you want to do that or want to have your artifact
        buckets encrypted, be sure to set this value to ``true``.

        Be aware there is a cost associated with maintaining the KMS keys.

        :default: false
        '''
        result = self._values.get("cross_account_keys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_replication_buckets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]]:
        '''A map of region to S3 bucket name used for cross-region CodePipeline.

        For every Action that you specify targeting a different region than the Pipeline itself,
        if you don't provide an explicit Bucket for that region using this property,
        the construct will automatically create a Stack containing an S3 Bucket in that region.
        Passed directly through to the {@link cp.Pipeline }.

        :default: - no cross region replication buckets.
        '''
        result = self._values.get("cross_region_replication_buckets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]], result)

    @builtins.property
    def docker_credentials(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.DockerCredential]]:
        '''A list of credentials used to authenticate to Docker registries.

        Specify any credentials necessary within the pipeline to build, synth, update, or publish assets.

        :default: []
        '''
        result = self._values.get("docker_credentials")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.DockerCredential]], result)

    @builtins.property
    def docker_enabled_for_self_mutation(self) -> typing.Optional[builtins.bool]:
        '''Enable Docker for the self-mutate step.

        Set this to true if the pipeline itself uses Docker container assets
        (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build
        image of a CodeBuild step in the pipeline).

        You do not need to set it if you build Docker image assets in the
        application Stages and Stacks that are *deployed* by this pipeline.

        Configures privileged mode for the self-mutation CodeBuild action.

        If you are about to turn this on in an already-deployed Pipeline,
        set the value to ``true`` first, commit and allow the pipeline to
        self-update, and only then use the Docker asset in the pipeline.

        :default: false
        '''
        result = self._values.get("docker_enabled_for_self_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docker_enabled_for_synth(self) -> typing.Optional[builtins.bool]:
        '''Enable Docker for the 'synth' step.

        Set this to true if you are using file assets that require
        "bundling" anywhere in your application (meaning an asset
        compilation step will be run with the tools provided by
        a Docker image), both for the Pipeline stack as well as the
        application stacks.

        A common way to use bundling assets in your application is by
        using the ``aws-cdk-lib/aws-lambda-nodejs`` library.

        Configures privileged mode for the synth CodeBuild action.

        If you are about to turn this on in an already-deployed Pipeline,
        set the value to ``true`` first, commit and allow the pipeline to
        self-update, and only then use the bundled asset.

        :default: false
        '''
        result = self._values.get("docker_enabled_for_synth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_key_rotation(self) -> typing.Optional[builtins.bool]:
        '''Enable KMS key rotation for the generated KMS keys.

        By default KMS key rotation is disabled, but will add
        additional costs when enabled.

        :default: - false (key rotation is disabled)
        '''
        result = self._values.get("enable_key_rotation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        '''The name of the CodePipeline pipeline.

        :default: - Automatically generated
        '''
        result = self._values.get("pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_assets_in_parallel(self) -> typing.Optional[builtins.bool]:
        '''Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets.

        Publishing in parallel improves concurrency and may reduce publishing
        latency, but may also increase overall provisioning time of the CodeBuild
        projects.

        Experiment and see what value works best for you.

        :default: true
        '''
        result = self._values.get("publish_assets_in_parallel")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reuse_cross_region_support_stacks(self) -> typing.Optional[builtins.bool]:
        '''Reuse the same cross region support stack for all pipelines in the App.

        :default: - true (Use the same support stack for all pipelines in App)
        '''
        result = self._values.get("reuse_cross_region_support_stacks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The IAM role to be assumed by this Pipeline.

        :default: - A new role is created
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def self_mutation(self) -> typing.Optional[builtins.bool]:
        '''Whether the pipeline will update itself.

        This needs to be set to ``true`` to allow the pipeline to reconfigure
        itself when assets or stages are being added to it, and ``true`` is the
        recommended setting.

        You can temporarily set this to ``false`` while you are iterating
        on the pipeline itself and prefer to deploy changes using ``cdk deploy``.

        :default: true
        '''
        result = self._values.get("self_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def self_mutation_code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Additional customizations to apply to the self mutation CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied
        '''
        result = self._values.get("self_mutation_code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def synth(self) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer]:
        '''The build step that produces the CDK Cloud Assembly.

        The primary output of this step needs to be the ``cdk.out`` directory
        generated by the ``cdk synth`` command.

        If you use a ``ShellStep`` here and you don't configure an output directory,
        the output directory will automatically be assumed to be ``cdk.out``.
        '''
        result = self._values.get("synth")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer], result)

    @builtins.property
    def synth_code_build_defaults(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions]:
        '''Additional customizations to apply to the synthesize CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied
        '''
        result = self._values.get("synth_code_build_defaults")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions], result)

    @builtins.property
    def use_change_sets(self) -> typing.Optional[builtins.bool]:
        '''Deploy every stack by creating a change set and executing it.

        When enabled, creates a "Prepare" and "Execute" action for each stack. Disable
        to deploy the stack in one pipeline action.

        :default: true
        '''
        result = self._values.get("use_change_sets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def code_connection_arn(self) -> builtins.str:
        '''The Arn of the CodeConnection.'''
        result = self._values.get("code_connection_arn")
        assert result is not None, "Required property 'code_connection_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_synth_directory(self) -> builtins.str:
        '''Output directory for cdk synthesized artifacts i.e: packages/infra/cdk.out.'''
        result = self._values.get("primary_synth_directory")
        assert result is not None, "Required property 'primary_synth_directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_owner_and_name(self) -> builtins.str:
        '''The Owner and Repository name for instance, user Bob with git repository ACME becomes "Bob/ACME".'''
        result = self._values.get("repository_owner_and_name")
        assert result is not None, "Required property 'repository_owner_and_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cdk_command(self) -> typing.Optional[builtins.str]:
        '''CDK command.

        Override the command used to call cdk for synth and deploy.

        :default: 'npx cdk'
        '''
        result = self._values.get("cdk_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_src_dir(self) -> typing.Optional[builtins.str]:
        '''The directory with ``cdk.json`` to run cdk synth from. Set this if you enabled feature branches and ``cdk.json`` is not located in the parent directory of ``primarySynthDirectory``.

        :default: The parent directory of ``primarySynthDirectory``
        '''
        result = self._values.get("cdk_src_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_branch_name(self) -> typing.Optional[builtins.str]:
        '''Branch to trigger the pipeline execution.

        :default: mainline
        '''
        result = self._values.get("default_branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sonar_code_scanner_config(self) -> typing.Optional["SonarCodeScannerConfig"]:
        '''Configuration for enabling Sonarqube code scanning on a successful synth.

        :default: undefined
        '''
        result = self._values.get("sonar_code_scanner_config")
        return typing.cast(typing.Optional["SonarCodeScannerConfig"], result)

    @builtins.property
    def synth_shell_step_partial_props(
        self,
    ) -> typing.Optional[_aws_cdk_pipelines_ceddda9d.ShellStepProps]:
        '''PDKPipeline by default assumes a NX Monorepo structure for it's codebase and uses sane defaults for the install and run commands.

        To override these defaults
        and/or provide additional inputs, specify env settings, etc you can provide
        a partial ShellStepProps.
        '''
        result = self._values.get("synth_shell_step_partial_props")
        return typing.cast(typing.Optional[_aws_cdk_pipelines_ceddda9d.ShellStepProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PDKPipelineWithCodeConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SonarCodeScanner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.pipeline.SonarCodeScanner",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        artifact_bucket_arn: builtins.str,
        synth_build_arn: builtins.str,
        artifact_bucket_key_arn: typing.Optional[builtins.str] = None,
        sonarqube_authorized_group: builtins.str,
        sonarqube_default_profile_or_gate_name: builtins.str,
        sonarqube_endpoint: builtins.str,
        sonarqube_project_name: builtins.str,
        cdk_out_dir: typing.Optional[builtins.str] = None,
        cfn_nag_ignore_path: typing.Optional[builtins.str] = None,
        exclude_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_archive_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        sonarqube_specific_profile_or_gate_name: typing.Optional[builtins.str] = None,
        sonarqube_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param artifact_bucket_arn: S3 bucket ARN containing the built artifacts from the synth build.
        :param synth_build_arn: ARN for the CodeBuild task responsible for executing the synth command.
        :param artifact_bucket_key_arn: Artifact bucket key ARN used to encrypt the artifacts.
        :param sonarqube_authorized_group: Group name in Sonarqube with access to administer this project.
        :param sonarqube_default_profile_or_gate_name: Default profile/gate name i.e: your org profile. Note: These need to be set up in Sonarqube manually.
        :param sonarqube_endpoint: endpoint of the sonarqube instance i.e: https://. Note: Ensure a trailing '/' is not included.
        :param sonarqube_project_name: Name of the project to create in Sonarqube.
        :param cdk_out_dir: directory containing the synthesized cdk resources.
        :param cfn_nag_ignore_path: path to a file containing the cfn nag suppression rules.
        :param exclude_globs_for_scan: glob patterns to exclude from sonar scan.
        :param include_globs_for_scan: glob patterns to include from sonar scan.
        :param pre_archive_commands: Hook which allows custom commands to be executed before the process commences the archival process.
        :param sonarqube_specific_profile_or_gate_name: Specific profile/gate name i.e: language specific. Note: These need to be set up in Sonarqube manually.
        :param sonarqube_tags: Tags to associate with this project.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c19351e649e4bfdc83c5bdb3d1be90ce2913d15d7594c2a190003c02819fb6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SonarCodeScannerProps(
            artifact_bucket_arn=artifact_bucket_arn,
            synth_build_arn=synth_build_arn,
            artifact_bucket_key_arn=artifact_bucket_key_arn,
            sonarqube_authorized_group=sonarqube_authorized_group,
            sonarqube_default_profile_or_gate_name=sonarqube_default_profile_or_gate_name,
            sonarqube_endpoint=sonarqube_endpoint,
            sonarqube_project_name=sonarqube_project_name,
            cdk_out_dir=cdk_out_dir,
            cfn_nag_ignore_path=cfn_nag_ignore_path,
            exclude_globs_for_scan=exclude_globs_for_scan,
            include_globs_for_scan=include_globs_for_scan,
            pre_archive_commands=pre_archive_commands,
            sonarqube_specific_profile_or_gate_name=sonarqube_specific_profile_or_gate_name,
            sonarqube_tags=sonarqube_tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws/pdk.pipeline.SonarCodeScannerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "sonarqube_authorized_group": "sonarqubeAuthorizedGroup",
        "sonarqube_default_profile_or_gate_name": "sonarqubeDefaultProfileOrGateName",
        "sonarqube_endpoint": "sonarqubeEndpoint",
        "sonarqube_project_name": "sonarqubeProjectName",
        "cdk_out_dir": "cdkOutDir",
        "cfn_nag_ignore_path": "cfnNagIgnorePath",
        "exclude_globs_for_scan": "excludeGlobsForScan",
        "include_globs_for_scan": "includeGlobsForScan",
        "pre_archive_commands": "preArchiveCommands",
        "sonarqube_specific_profile_or_gate_name": "sonarqubeSpecificProfileOrGateName",
        "sonarqube_tags": "sonarqubeTags",
    },
)
class SonarCodeScannerConfig:
    def __init__(
        self,
        *,
        sonarqube_authorized_group: builtins.str,
        sonarqube_default_profile_or_gate_name: builtins.str,
        sonarqube_endpoint: builtins.str,
        sonarqube_project_name: builtins.str,
        cdk_out_dir: typing.Optional[builtins.str] = None,
        cfn_nag_ignore_path: typing.Optional[builtins.str] = None,
        exclude_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_archive_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        sonarqube_specific_profile_or_gate_name: typing.Optional[builtins.str] = None,
        sonarqube_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param sonarqube_authorized_group: Group name in Sonarqube with access to administer this project.
        :param sonarqube_default_profile_or_gate_name: Default profile/gate name i.e: your org profile. Note: These need to be set up in Sonarqube manually.
        :param sonarqube_endpoint: endpoint of the sonarqube instance i.e: https://. Note: Ensure a trailing '/' is not included.
        :param sonarqube_project_name: Name of the project to create in Sonarqube.
        :param cdk_out_dir: directory containing the synthesized cdk resources.
        :param cfn_nag_ignore_path: path to a file containing the cfn nag suppression rules.
        :param exclude_globs_for_scan: glob patterns to exclude from sonar scan.
        :param include_globs_for_scan: glob patterns to include from sonar scan.
        :param pre_archive_commands: Hook which allows custom commands to be executed before the process commences the archival process.
        :param sonarqube_specific_profile_or_gate_name: Specific profile/gate name i.e: language specific. Note: These need to be set up in Sonarqube manually.
        :param sonarqube_tags: Tags to associate with this project.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff1e359730d2d2b3dec40e7aa965c39991eff4621aa818272d1274e62da561e)
            check_type(argname="argument sonarqube_authorized_group", value=sonarqube_authorized_group, expected_type=type_hints["sonarqube_authorized_group"])
            check_type(argname="argument sonarqube_default_profile_or_gate_name", value=sonarqube_default_profile_or_gate_name, expected_type=type_hints["sonarqube_default_profile_or_gate_name"])
            check_type(argname="argument sonarqube_endpoint", value=sonarqube_endpoint, expected_type=type_hints["sonarqube_endpoint"])
            check_type(argname="argument sonarqube_project_name", value=sonarqube_project_name, expected_type=type_hints["sonarqube_project_name"])
            check_type(argname="argument cdk_out_dir", value=cdk_out_dir, expected_type=type_hints["cdk_out_dir"])
            check_type(argname="argument cfn_nag_ignore_path", value=cfn_nag_ignore_path, expected_type=type_hints["cfn_nag_ignore_path"])
            check_type(argname="argument exclude_globs_for_scan", value=exclude_globs_for_scan, expected_type=type_hints["exclude_globs_for_scan"])
            check_type(argname="argument include_globs_for_scan", value=include_globs_for_scan, expected_type=type_hints["include_globs_for_scan"])
            check_type(argname="argument pre_archive_commands", value=pre_archive_commands, expected_type=type_hints["pre_archive_commands"])
            check_type(argname="argument sonarqube_specific_profile_or_gate_name", value=sonarqube_specific_profile_or_gate_name, expected_type=type_hints["sonarqube_specific_profile_or_gate_name"])
            check_type(argname="argument sonarqube_tags", value=sonarqube_tags, expected_type=type_hints["sonarqube_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sonarqube_authorized_group": sonarqube_authorized_group,
            "sonarqube_default_profile_or_gate_name": sonarqube_default_profile_or_gate_name,
            "sonarqube_endpoint": sonarqube_endpoint,
            "sonarqube_project_name": sonarqube_project_name,
        }
        if cdk_out_dir is not None:
            self._values["cdk_out_dir"] = cdk_out_dir
        if cfn_nag_ignore_path is not None:
            self._values["cfn_nag_ignore_path"] = cfn_nag_ignore_path
        if exclude_globs_for_scan is not None:
            self._values["exclude_globs_for_scan"] = exclude_globs_for_scan
        if include_globs_for_scan is not None:
            self._values["include_globs_for_scan"] = include_globs_for_scan
        if pre_archive_commands is not None:
            self._values["pre_archive_commands"] = pre_archive_commands
        if sonarqube_specific_profile_or_gate_name is not None:
            self._values["sonarqube_specific_profile_or_gate_name"] = sonarqube_specific_profile_or_gate_name
        if sonarqube_tags is not None:
            self._values["sonarqube_tags"] = sonarqube_tags

    @builtins.property
    def sonarqube_authorized_group(self) -> builtins.str:
        '''Group name in Sonarqube with access to administer this project.'''
        result = self._values.get("sonarqube_authorized_group")
        assert result is not None, "Required property 'sonarqube_authorized_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sonarqube_default_profile_or_gate_name(self) -> builtins.str:
        '''Default profile/gate name i.e: your org profile.

        Note: These need to be set up in Sonarqube manually.
        '''
        result = self._values.get("sonarqube_default_profile_or_gate_name")
        assert result is not None, "Required property 'sonarqube_default_profile_or_gate_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sonarqube_endpoint(self) -> builtins.str:
        '''endpoint of the sonarqube instance i.e: https://.

        Note: Ensure a trailing '/' is not included.
        '''
        result = self._values.get("sonarqube_endpoint")
        assert result is not None, "Required property 'sonarqube_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sonarqube_project_name(self) -> builtins.str:
        '''Name of the project to create in Sonarqube.'''
        result = self._values.get("sonarqube_project_name")
        assert result is not None, "Required property 'sonarqube_project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cdk_out_dir(self) -> typing.Optional[builtins.str]:
        '''directory containing the synthesized cdk resources.'''
        result = self._values.get("cdk_out_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cfn_nag_ignore_path(self) -> typing.Optional[builtins.str]:
        '''path to a file containing the cfn nag suppression rules.'''
        result = self._values.get("cfn_nag_ignore_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_globs_for_scan(self) -> typing.Optional[typing.List[builtins.str]]:
        '''glob patterns to exclude from sonar scan.'''
        result = self._values.get("exclude_globs_for_scan")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_globs_for_scan(self) -> typing.Optional[typing.List[builtins.str]]:
        '''glob patterns to include from sonar scan.'''
        result = self._values.get("include_globs_for_scan")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pre_archive_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Hook which allows custom commands to be executed before the process commences the archival process.'''
        result = self._values.get("pre_archive_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sonarqube_specific_profile_or_gate_name(self) -> typing.Optional[builtins.str]:
        '''Specific profile/gate name i.e: language specific.

        Note: These need to be set up in Sonarqube manually.
        '''
        result = self._values.get("sonarqube_specific_profile_or_gate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sonarqube_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags to associate with this project.'''
        result = self._values.get("sonarqube_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarCodeScannerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.pipeline.SonarCodeScannerProps",
    jsii_struct_bases=[SonarCodeScannerConfig],
    name_mapping={
        "sonarqube_authorized_group": "sonarqubeAuthorizedGroup",
        "sonarqube_default_profile_or_gate_name": "sonarqubeDefaultProfileOrGateName",
        "sonarqube_endpoint": "sonarqubeEndpoint",
        "sonarqube_project_name": "sonarqubeProjectName",
        "cdk_out_dir": "cdkOutDir",
        "cfn_nag_ignore_path": "cfnNagIgnorePath",
        "exclude_globs_for_scan": "excludeGlobsForScan",
        "include_globs_for_scan": "includeGlobsForScan",
        "pre_archive_commands": "preArchiveCommands",
        "sonarqube_specific_profile_or_gate_name": "sonarqubeSpecificProfileOrGateName",
        "sonarqube_tags": "sonarqubeTags",
        "artifact_bucket_arn": "artifactBucketArn",
        "synth_build_arn": "synthBuildArn",
        "artifact_bucket_key_arn": "artifactBucketKeyArn",
    },
)
class SonarCodeScannerProps(SonarCodeScannerConfig):
    def __init__(
        self,
        *,
        sonarqube_authorized_group: builtins.str,
        sonarqube_default_profile_or_gate_name: builtins.str,
        sonarqube_endpoint: builtins.str,
        sonarqube_project_name: builtins.str,
        cdk_out_dir: typing.Optional[builtins.str] = None,
        cfn_nag_ignore_path: typing.Optional[builtins.str] = None,
        exclude_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_archive_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        sonarqube_specific_profile_or_gate_name: typing.Optional[builtins.str] = None,
        sonarqube_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        artifact_bucket_arn: builtins.str,
        synth_build_arn: builtins.str,
        artifact_bucket_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''SonarCodeScanners properties.

        :param sonarqube_authorized_group: Group name in Sonarqube with access to administer this project.
        :param sonarqube_default_profile_or_gate_name: Default profile/gate name i.e: your org profile. Note: These need to be set up in Sonarqube manually.
        :param sonarqube_endpoint: endpoint of the sonarqube instance i.e: https://. Note: Ensure a trailing '/' is not included.
        :param sonarqube_project_name: Name of the project to create in Sonarqube.
        :param cdk_out_dir: directory containing the synthesized cdk resources.
        :param cfn_nag_ignore_path: path to a file containing the cfn nag suppression rules.
        :param exclude_globs_for_scan: glob patterns to exclude from sonar scan.
        :param include_globs_for_scan: glob patterns to include from sonar scan.
        :param pre_archive_commands: Hook which allows custom commands to be executed before the process commences the archival process.
        :param sonarqube_specific_profile_or_gate_name: Specific profile/gate name i.e: language specific. Note: These need to be set up in Sonarqube manually.
        :param sonarqube_tags: Tags to associate with this project.
        :param artifact_bucket_arn: S3 bucket ARN containing the built artifacts from the synth build.
        :param synth_build_arn: ARN for the CodeBuild task responsible for executing the synth command.
        :param artifact_bucket_key_arn: Artifact bucket key ARN used to encrypt the artifacts.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd71d87ed3691932a5863fdc5aaa95e4f78aa579028b55812eabb12a88c273b8)
            check_type(argname="argument sonarqube_authorized_group", value=sonarqube_authorized_group, expected_type=type_hints["sonarqube_authorized_group"])
            check_type(argname="argument sonarqube_default_profile_or_gate_name", value=sonarqube_default_profile_or_gate_name, expected_type=type_hints["sonarqube_default_profile_or_gate_name"])
            check_type(argname="argument sonarqube_endpoint", value=sonarqube_endpoint, expected_type=type_hints["sonarqube_endpoint"])
            check_type(argname="argument sonarqube_project_name", value=sonarqube_project_name, expected_type=type_hints["sonarqube_project_name"])
            check_type(argname="argument cdk_out_dir", value=cdk_out_dir, expected_type=type_hints["cdk_out_dir"])
            check_type(argname="argument cfn_nag_ignore_path", value=cfn_nag_ignore_path, expected_type=type_hints["cfn_nag_ignore_path"])
            check_type(argname="argument exclude_globs_for_scan", value=exclude_globs_for_scan, expected_type=type_hints["exclude_globs_for_scan"])
            check_type(argname="argument include_globs_for_scan", value=include_globs_for_scan, expected_type=type_hints["include_globs_for_scan"])
            check_type(argname="argument pre_archive_commands", value=pre_archive_commands, expected_type=type_hints["pre_archive_commands"])
            check_type(argname="argument sonarqube_specific_profile_or_gate_name", value=sonarqube_specific_profile_or_gate_name, expected_type=type_hints["sonarqube_specific_profile_or_gate_name"])
            check_type(argname="argument sonarqube_tags", value=sonarqube_tags, expected_type=type_hints["sonarqube_tags"])
            check_type(argname="argument artifact_bucket_arn", value=artifact_bucket_arn, expected_type=type_hints["artifact_bucket_arn"])
            check_type(argname="argument synth_build_arn", value=synth_build_arn, expected_type=type_hints["synth_build_arn"])
            check_type(argname="argument artifact_bucket_key_arn", value=artifact_bucket_key_arn, expected_type=type_hints["artifact_bucket_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sonarqube_authorized_group": sonarqube_authorized_group,
            "sonarqube_default_profile_or_gate_name": sonarqube_default_profile_or_gate_name,
            "sonarqube_endpoint": sonarqube_endpoint,
            "sonarqube_project_name": sonarqube_project_name,
            "artifact_bucket_arn": artifact_bucket_arn,
            "synth_build_arn": synth_build_arn,
        }
        if cdk_out_dir is not None:
            self._values["cdk_out_dir"] = cdk_out_dir
        if cfn_nag_ignore_path is not None:
            self._values["cfn_nag_ignore_path"] = cfn_nag_ignore_path
        if exclude_globs_for_scan is not None:
            self._values["exclude_globs_for_scan"] = exclude_globs_for_scan
        if include_globs_for_scan is not None:
            self._values["include_globs_for_scan"] = include_globs_for_scan
        if pre_archive_commands is not None:
            self._values["pre_archive_commands"] = pre_archive_commands
        if sonarqube_specific_profile_or_gate_name is not None:
            self._values["sonarqube_specific_profile_or_gate_name"] = sonarqube_specific_profile_or_gate_name
        if sonarqube_tags is not None:
            self._values["sonarqube_tags"] = sonarqube_tags
        if artifact_bucket_key_arn is not None:
            self._values["artifact_bucket_key_arn"] = artifact_bucket_key_arn

    @builtins.property
    def sonarqube_authorized_group(self) -> builtins.str:
        '''Group name in Sonarqube with access to administer this project.'''
        result = self._values.get("sonarqube_authorized_group")
        assert result is not None, "Required property 'sonarqube_authorized_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sonarqube_default_profile_or_gate_name(self) -> builtins.str:
        '''Default profile/gate name i.e: your org profile.

        Note: These need to be set up in Sonarqube manually.
        '''
        result = self._values.get("sonarqube_default_profile_or_gate_name")
        assert result is not None, "Required property 'sonarqube_default_profile_or_gate_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sonarqube_endpoint(self) -> builtins.str:
        '''endpoint of the sonarqube instance i.e: https://.

        Note: Ensure a trailing '/' is not included.
        '''
        result = self._values.get("sonarqube_endpoint")
        assert result is not None, "Required property 'sonarqube_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sonarqube_project_name(self) -> builtins.str:
        '''Name of the project to create in Sonarqube.'''
        result = self._values.get("sonarqube_project_name")
        assert result is not None, "Required property 'sonarqube_project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cdk_out_dir(self) -> typing.Optional[builtins.str]:
        '''directory containing the synthesized cdk resources.'''
        result = self._values.get("cdk_out_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cfn_nag_ignore_path(self) -> typing.Optional[builtins.str]:
        '''path to a file containing the cfn nag suppression rules.'''
        result = self._values.get("cfn_nag_ignore_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_globs_for_scan(self) -> typing.Optional[typing.List[builtins.str]]:
        '''glob patterns to exclude from sonar scan.'''
        result = self._values.get("exclude_globs_for_scan")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_globs_for_scan(self) -> typing.Optional[typing.List[builtins.str]]:
        '''glob patterns to include from sonar scan.'''
        result = self._values.get("include_globs_for_scan")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pre_archive_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Hook which allows custom commands to be executed before the process commences the archival process.'''
        result = self._values.get("pre_archive_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sonarqube_specific_profile_or_gate_name(self) -> typing.Optional[builtins.str]:
        '''Specific profile/gate name i.e: language specific.

        Note: These need to be set up in Sonarqube manually.
        '''
        result = self._values.get("sonarqube_specific_profile_or_gate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sonarqube_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags to associate with this project.'''
        result = self._values.get("sonarqube_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def artifact_bucket_arn(self) -> builtins.str:
        '''S3 bucket ARN containing the built artifacts from the synth build.'''
        result = self._values.get("artifact_bucket_arn")
        assert result is not None, "Required property 'artifact_bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def synth_build_arn(self) -> builtins.str:
        '''ARN for the CodeBuild task responsible for executing the synth command.'''
        result = self._values.get("synth_build_arn")
        assert result is not None, "Required property 'synth_build_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifact_bucket_key_arn(self) -> typing.Optional[builtins.str]:
        '''Artifact bucket key ARN used to encrypt the artifacts.'''
        result = self._values.get("artifact_bucket_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SonarCodeScannerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CodePipelineProps",
    "IsDefaultBranchProps",
    "PDKPipeline",
    "PDKPipelineProps",
    "PDKPipelineWithCodeConnection",
    "PDKPipelineWithCodeConnectionProps",
    "SonarCodeScanner",
    "SonarCodeScannerConfig",
    "SonarCodeScannerProps",
]

publication.publish()

def _typecheckingstub__b3cde37f902c1991f07ce6cca86ee234479782b49c56f386ea31b03ba832f0fc(
    *,
    artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cli_version: typing.Optional[builtins.str] = None,
    code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
    cross_account_keys: typing.Optional[builtins.bool] = None,
    cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
    docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
    docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
    enable_key_rotation: typing.Optional[builtins.bool] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
    reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    self_mutation: typing.Optional[builtins.bool] = None,
    self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
    synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    use_change_sets: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9af73ab3cb4e5653a7fbbf5939157ed24cd9e40ac7adc479ed17150e7328293(
    *,
    default_branch_name: typing.Optional[builtins.str] = None,
    node: typing.Optional[_constructs_77d1e7e8.Node] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1fc30725663d11b68afc62a715c01473c5ff1442fd16970c05eb9b88c2d55f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    primary_synth_directory: builtins.str,
    repository_name: builtins.str,
    branch_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command: typing.Optional[builtins.str] = None,
    cdk_src_dir: typing.Optional[builtins.str] = None,
    code_commit_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    code_commit_repository: typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository] = None,
    default_branch_name: typing.Optional[builtins.str] = None,
    sonar_code_scanner_config: typing.Optional[typing.Union[SonarCodeScannerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    synth_shell_step_partial_props: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.ShellStepProps, typing.Dict[builtins.str, typing.Any]]] = None,
    artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cli_version: typing.Optional[builtins.str] = None,
    code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
    cross_account_keys: typing.Optional[builtins.bool] = None,
    cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
    docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
    docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
    enable_key_rotation: typing.Optional[builtins.bool] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
    reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    self_mutation: typing.Optional[builtins.bool] = None,
    self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
    synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    use_change_sets: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd9d65ebcdf7f007bfface73cce98ed9b6536787a15dcf4c5fc44679c09df26(
    branch_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6b99d170e0fccb842092fe64d3c8cfd0993145d60e03b63ddfafae1d354b1c(
    stage: _aws_cdk_ceddda9d.Stage,
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2347ec2a52a4becace9d89a95498a999fea5998347cde10b8a43bc88a33bbc3e(
    *,
    artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cli_version: typing.Optional[builtins.str] = None,
    code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
    cross_account_keys: typing.Optional[builtins.bool] = None,
    cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
    docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
    docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
    enable_key_rotation: typing.Optional[builtins.bool] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
    reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    self_mutation: typing.Optional[builtins.bool] = None,
    self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
    synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    use_change_sets: typing.Optional[builtins.bool] = None,
    primary_synth_directory: builtins.str,
    repository_name: builtins.str,
    branch_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command: typing.Optional[builtins.str] = None,
    cdk_src_dir: typing.Optional[builtins.str] = None,
    code_commit_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    code_commit_repository: typing.Optional[_aws_cdk_aws_codecommit_ceddda9d.IRepository] = None,
    default_branch_name: typing.Optional[builtins.str] = None,
    sonar_code_scanner_config: typing.Optional[typing.Union[SonarCodeScannerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    synth_shell_step_partial_props: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.ShellStepProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f18b2a44c7e3c2ea97323a8a8eaa0d9f38f23517ebf3d64569cf2d478f6fd3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    code_connection_arn: builtins.str,
    primary_synth_directory: builtins.str,
    repository_owner_and_name: builtins.str,
    cdk_command: typing.Optional[builtins.str] = None,
    cdk_src_dir: typing.Optional[builtins.str] = None,
    default_branch_name: typing.Optional[builtins.str] = None,
    sonar_code_scanner_config: typing.Optional[typing.Union[SonarCodeScannerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    synth_shell_step_partial_props: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.ShellStepProps, typing.Dict[builtins.str, typing.Any]]] = None,
    artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cli_version: typing.Optional[builtins.str] = None,
    code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
    cross_account_keys: typing.Optional[builtins.bool] = None,
    cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
    docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
    docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
    enable_key_rotation: typing.Optional[builtins.bool] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
    reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    self_mutation: typing.Optional[builtins.bool] = None,
    self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
    synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    use_change_sets: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49e5799c83007a10ebd29aa57e030002095ba8bc63eb901fcbf4fa847cd45a5(
    branch_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fc478ffdf001ccc8638b25715631e842b68ebb45c6029faf66034b9a1a32bd(
    stage: _aws_cdk_ceddda9d.Stage,
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a853ce5a4054d1ccf4a1609847820cdbb922828725b4385b74c0f1d624a10550(
    *,
    artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    asset_publishing_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cli_version: typing.Optional[builtins.str] = None,
    code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_pipeline: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline] = None,
    cross_account_keys: typing.Optional[builtins.bool] = None,
    cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    docker_credentials: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.DockerCredential]] = None,
    docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
    docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
    enable_key_rotation: typing.Optional[builtins.bool] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
    reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    self_mutation: typing.Optional[builtins.bool] = None,
    self_mutation_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    synth: typing.Optional[_aws_cdk_pipelines_ceddda9d.IFileSetProducer] = None,
    synth_code_build_defaults: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    use_change_sets: typing.Optional[builtins.bool] = None,
    code_connection_arn: builtins.str,
    primary_synth_directory: builtins.str,
    repository_owner_and_name: builtins.str,
    cdk_command: typing.Optional[builtins.str] = None,
    cdk_src_dir: typing.Optional[builtins.str] = None,
    default_branch_name: typing.Optional[builtins.str] = None,
    sonar_code_scanner_config: typing.Optional[typing.Union[SonarCodeScannerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    synth_shell_step_partial_props: typing.Optional[typing.Union[_aws_cdk_pipelines_ceddda9d.ShellStepProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c19351e649e4bfdc83c5bdb3d1be90ce2913d15d7594c2a190003c02819fb6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    artifact_bucket_arn: builtins.str,
    synth_build_arn: builtins.str,
    artifact_bucket_key_arn: typing.Optional[builtins.str] = None,
    sonarqube_authorized_group: builtins.str,
    sonarqube_default_profile_or_gate_name: builtins.str,
    sonarqube_endpoint: builtins.str,
    sonarqube_project_name: builtins.str,
    cdk_out_dir: typing.Optional[builtins.str] = None,
    cfn_nag_ignore_path: typing.Optional[builtins.str] = None,
    exclude_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_archive_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    sonarqube_specific_profile_or_gate_name: typing.Optional[builtins.str] = None,
    sonarqube_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff1e359730d2d2b3dec40e7aa965c39991eff4621aa818272d1274e62da561e(
    *,
    sonarqube_authorized_group: builtins.str,
    sonarqube_default_profile_or_gate_name: builtins.str,
    sonarqube_endpoint: builtins.str,
    sonarqube_project_name: builtins.str,
    cdk_out_dir: typing.Optional[builtins.str] = None,
    cfn_nag_ignore_path: typing.Optional[builtins.str] = None,
    exclude_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_archive_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    sonarqube_specific_profile_or_gate_name: typing.Optional[builtins.str] = None,
    sonarqube_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd71d87ed3691932a5863fdc5aaa95e4f78aa579028b55812eabb12a88c273b8(
    *,
    sonarqube_authorized_group: builtins.str,
    sonarqube_default_profile_or_gate_name: builtins.str,
    sonarqube_endpoint: builtins.str,
    sonarqube_project_name: builtins.str,
    cdk_out_dir: typing.Optional[builtins.str] = None,
    cfn_nag_ignore_path: typing.Optional[builtins.str] = None,
    exclude_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_globs_for_scan: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_archive_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    sonarqube_specific_profile_or_gate_name: typing.Optional[builtins.str] = None,
    sonarqube_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    artifact_bucket_arn: builtins.str,
    synth_build_arn: builtins.str,
    artifact_bucket_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
