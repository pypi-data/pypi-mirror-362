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
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_s3_deployment as _aws_cdk_aws_s3_deployment_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws/pdk.static_website.BucketDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_control": "accessControl",
        "cache_control": "cacheControl",
        "content_disposition": "contentDisposition",
        "content_encoding": "contentEncoding",
        "content_language": "contentLanguage",
        "content_type": "contentType",
        "destination_bucket": "destinationBucket",
        "destination_key_prefix": "destinationKeyPrefix",
        "distribution": "distribution",
        "distribution_paths": "distributionPaths",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "exclude": "exclude",
        "expires": "expires",
        "extract": "extract",
        "include": "include",
        "log_group": "logGroup",
        "log_retention": "logRetention",
        "memory_limit": "memoryLimit",
        "metadata": "metadata",
        "output_object_keys": "outputObjectKeys",
        "prune": "prune",
        "retain_on_delete": "retainOnDelete",
        "role": "role",
        "server_side_encryption": "serverSideEncryption",
        "server_side_encryption_aws_kms_key_id": "serverSideEncryptionAwsKmsKeyId",
        "server_side_encryption_customer_algorithm": "serverSideEncryptionCustomerAlgorithm",
        "sign_content": "signContent",
        "sources": "sources",
        "storage_class": "storageClass",
        "use_efs": "useEfs",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "website_redirect_location": "websiteRedirectLocation",
    },
)
class BucketDeploymentProps:
    def __init__(
        self,
        *,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        cache_control: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_deployment_ceddda9d.CacheControl]] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        destination_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        destination_key_prefix: typing.Optional[builtins.str] = None,
        distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
        distribution_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        expires: typing.Optional[_aws_cdk_ceddda9d.Expiration] = None,
        extract: typing.Optional[builtins.bool] = None,
        include: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        output_object_keys: typing.Optional[builtins.bool] = None,
        prune: typing.Optional[builtins.bool] = None,
        retain_on_delete: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        server_side_encryption: typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.ServerSideEncryption] = None,
        server_side_encryption_aws_kms_key_id: typing.Optional[builtins.str] = None,
        server_side_encryption_customer_algorithm: typing.Optional[builtins.str] = None,
        sign_content: typing.Optional[builtins.bool] = None,
        sources: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_deployment_ceddda9d.ISource]] = None,
        storage_class: typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.StorageClass] = None,
        use_efs: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        website_redirect_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''BucketDeploymentProps.

        :param access_control: System-defined x-amz-acl metadata to be set on all objects in the deployment. Default: - Not set.
        :param cache_control: System-defined cache-control metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_disposition: System-defined cache-disposition metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_encoding: System-defined content-encoding metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_language: System-defined content-language metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_type: System-defined content-type metadata to be set on all objects in the deployment. Default: - Not set.
        :param destination_bucket: The S3 bucket to sync the contents of the zip file to.
        :param destination_key_prefix: Key prefix in the destination bucket. Must be <=104 characters Default: "/" (unzip to root of the destination bucket)
        :param distribution: The CloudFront distribution using the destination bucket as an origin. Files in the distribution's edge caches will be invalidated after files are uploaded to the destination bucket. Default: - No invalidation occurs
        :param distribution_paths: The file paths to invalidate in the CloudFront distribution. Default: - All files under the destination bucket key prefix will be invalidated.
        :param ephemeral_storage_size: The size of the AWS Lambda function’s /tmp directory in MiB. Default: 512 MiB
        :param exclude: If this is set, matching files or objects will be excluded from the deployment's sync command. This can be used to exclude a file from being pruned in the destination bucket. If you want to just exclude files from the deployment package (which excludes these files evaluated when invalidating the asset), you should leverage the ``exclude`` property of ``AssetOptions`` when defining your source. Default: - No exclude filters are used
        :param expires: System-defined expires metadata to be set on all objects in the deployment. Default: - The objects in the distribution will not expire.
        :param extract: If this is set, the zip file will be synced to the destination S3 bucket and extracted. If false, the file will remain zipped in the destination bucket. Default: true
        :param include: If this is set, matching files or objects will be included with the deployment's sync command. Since all files from the deployment package are included by default, this property is usually leveraged alongside an ``exclude`` filter. Default: - No include filters are used and all files are included with the sync command
        :param log_group: The Log Group used for logging of events emitted by the custom resource's lambda function. Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16. If you are deploying to another type of region, please check regional availability first. Default: - a default log group created by AWS Lambda
        :param log_retention: The number of days that the lambda function's log events are kept in CloudWatch Logs. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: logs.RetentionDays.INFINITE
        :param memory_limit: The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: 128
        :param metadata: User-defined object metadata to be set on all objects in the deployment. Default: - No user metadata is set
        :param output_object_keys: If set to false, the custom resource will not send back the SourceObjectKeys. This is useful when you are facing the error ``Response object is too long`` See https://github.com/aws/aws-cdk/issues/28579 Default: true
        :param prune: If this is set to false, files in the destination bucket that do not exist in the asset, will NOT be deleted during deployment (create/update). Default: true
        :param retain_on_delete: If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated. NOTICE: Configuring this to "false" might have operational implications. Please visit to the package documentation referred below to make sure you fully understand those implications. Default: true - when resource is deleted/updated, files are retained
        :param role: Execution role associated with this function. Default: - A role is automatically created
        :param server_side_encryption: System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment. Default: - Server side encryption is not used.
        :param server_side_encryption_aws_kms_key_id: System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment. Default: - Not set.
        :param server_side_encryption_customer_algorithm: System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment. Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080 Default: - Not set.
        :param sign_content: If set to true, uploads will precompute the value of ``x-amz-content-sha256`` and include it in the signed S3 request headers. Default: - ``x-amz-content-sha256`` will not be computed
        :param sources: The sources from which to deploy the contents of this bucket.
        :param storage_class: System-defined x-amz-storage-class metadata to be set on all objects in the deployment. Default: - Default storage-class for the bucket is used.
        :param use_efs: Mount an EFS file system. Enable this if your assets are large and you encounter disk space errors. Enabling this option will require a VPC to be specified. Default: - No EFS. Lambda has access only to 512MB of disk space.
        :param vpc: The VPC network to place the deployment lambda handler in. This is required if ``useEfs`` is set. Default: None
        :param vpc_subnets: Where in the VPC to place the deployment lambda handler. Only used if 'vpc' is supplied. Default: - the Vpc default strategy if not specified
        :param website_redirect_location: System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment. Default: - No website redirection.
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac3ac892a82bdd981340a9bff81d3e846e798cd03c6b162864b0df3ac5cdba4)
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument cache_control", value=cache_control, expected_type=type_hints["cache_control"])
            check_type(argname="argument content_disposition", value=content_disposition, expected_type=type_hints["content_disposition"])
            check_type(argname="argument content_encoding", value=content_encoding, expected_type=type_hints["content_encoding"])
            check_type(argname="argument content_language", value=content_language, expected_type=type_hints["content_language"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument destination_bucket", value=destination_bucket, expected_type=type_hints["destination_bucket"])
            check_type(argname="argument destination_key_prefix", value=destination_key_prefix, expected_type=type_hints["destination_key_prefix"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument distribution_paths", value=distribution_paths, expected_type=type_hints["distribution_paths"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument expires", value=expires, expected_type=type_hints["expires"])
            check_type(argname="argument extract", value=extract, expected_type=type_hints["extract"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument output_object_keys", value=output_object_keys, expected_type=type_hints["output_object_keys"])
            check_type(argname="argument prune", value=prune, expected_type=type_hints["prune"])
            check_type(argname="argument retain_on_delete", value=retain_on_delete, expected_type=type_hints["retain_on_delete"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument server_side_encryption_aws_kms_key_id", value=server_side_encryption_aws_kms_key_id, expected_type=type_hints["server_side_encryption_aws_kms_key_id"])
            check_type(argname="argument server_side_encryption_customer_algorithm", value=server_side_encryption_customer_algorithm, expected_type=type_hints["server_side_encryption_customer_algorithm"])
            check_type(argname="argument sign_content", value=sign_content, expected_type=type_hints["sign_content"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument use_efs", value=use_efs, expected_type=type_hints["use_efs"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument website_redirect_location", value=website_redirect_location, expected_type=type_hints["website_redirect_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_control is not None:
            self._values["access_control"] = access_control
        if cache_control is not None:
            self._values["cache_control"] = cache_control
        if content_disposition is not None:
            self._values["content_disposition"] = content_disposition
        if content_encoding is not None:
            self._values["content_encoding"] = content_encoding
        if content_language is not None:
            self._values["content_language"] = content_language
        if content_type is not None:
            self._values["content_type"] = content_type
        if destination_bucket is not None:
            self._values["destination_bucket"] = destination_bucket
        if destination_key_prefix is not None:
            self._values["destination_key_prefix"] = destination_key_prefix
        if distribution is not None:
            self._values["distribution"] = distribution
        if distribution_paths is not None:
            self._values["distribution_paths"] = distribution_paths
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if exclude is not None:
            self._values["exclude"] = exclude
        if expires is not None:
            self._values["expires"] = expires
        if extract is not None:
            self._values["extract"] = extract
        if include is not None:
            self._values["include"] = include
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if metadata is not None:
            self._values["metadata"] = metadata
        if output_object_keys is not None:
            self._values["output_object_keys"] = output_object_keys
        if prune is not None:
            self._values["prune"] = prune
        if retain_on_delete is not None:
            self._values["retain_on_delete"] = retain_on_delete
        if role is not None:
            self._values["role"] = role
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if server_side_encryption_aws_kms_key_id is not None:
            self._values["server_side_encryption_aws_kms_key_id"] = server_side_encryption_aws_kms_key_id
        if server_side_encryption_customer_algorithm is not None:
            self._values["server_side_encryption_customer_algorithm"] = server_side_encryption_customer_algorithm
        if sign_content is not None:
            self._values["sign_content"] = sign_content
        if sources is not None:
            self._values["sources"] = sources
        if storage_class is not None:
            self._values["storage_class"] = storage_class
        if use_efs is not None:
            self._values["use_efs"] = use_efs
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if website_redirect_location is not None:
            self._values["website_redirect_location"] = website_redirect_location

    @builtins.property
    def access_control(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl]:
        '''System-defined x-amz-acl metadata to be set on all objects in the deployment.

        :default: - Not set.
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl], result)

    @builtins.property
    def cache_control(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.CacheControl]]:
        '''System-defined cache-control metadata to be set on all objects in the deployment.

        :default: - Not set.
        '''
        result = self._values.get("cache_control")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.CacheControl]], result)

    @builtins.property
    def content_disposition(self) -> typing.Optional[builtins.str]:
        '''System-defined cache-disposition metadata to be set on all objects in the deployment.

        :default: - Not set.
        '''
        result = self._values.get("content_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_encoding(self) -> typing.Optional[builtins.str]:
        '''System-defined content-encoding metadata to be set on all objects in the deployment.

        :default: - Not set.
        '''
        result = self._values.get("content_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_language(self) -> typing.Optional[builtins.str]:
        '''System-defined content-language metadata to be set on all objects in the deployment.

        :default: - Not set.
        '''
        result = self._values.get("content_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''System-defined content-type metadata to be set on all objects in the deployment.

        :default: - Not set.
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''The S3 bucket to sync the contents of the zip file to.'''
        result = self._values.get("destination_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def destination_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Key prefix in the destination bucket.

        Must be <=104 characters

        :default: "/" (unzip to root of the destination bucket)
        '''
        result = self._values.get("destination_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution]:
        '''The CloudFront distribution using the destination bucket as an origin.

        Files in the distribution's edge caches will be invalidated after
        files are uploaded to the destination bucket.

        :default: - No invalidation occurs
        '''
        result = self._values.get("distribution")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution], result)

    @builtins.property
    def distribution_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The file paths to invalidate in the CloudFront distribution.

        :default: - All files under the destination bucket key prefix will be invalidated.
        '''
        result = self._values.get("distribution_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''The size of the AWS Lambda function’s /tmp directory in MiB.

        :default: 512 MiB
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If this is set, matching files or objects will be excluded from the deployment's sync command.

        This can be used to exclude a file from being pruned in the destination bucket.

        If you want to just exclude files from the deployment package (which excludes these files
        evaluated when invalidating the asset), you should leverage the ``exclude`` property of
        ``AssetOptions`` when defining your source.

        :default: - No exclude filters are used
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def expires(self) -> typing.Optional[_aws_cdk_ceddda9d.Expiration]:
        '''System-defined expires metadata to be set on all objects in the deployment.

        :default: - The objects in the distribution will not expire.
        '''
        result = self._values.get("expires")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Expiration], result)

    @builtins.property
    def extract(self) -> typing.Optional[builtins.bool]:
        '''If this is set, the zip file will be synced to the destination S3 bucket and extracted.

        If false, the file will remain zipped in the destination bucket.

        :default: true
        '''
        result = self._values.get("extract")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If this is set, matching files or objects will be included with the deployment's sync command.

        Since all files from the deployment package are included by default, this property
        is usually leveraged alongside an ``exclude`` filter.

        :default: - No include filters are used and all files are included with the sync command
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''The Log Group used for logging of events emitted by the custom resource's lambda function.

        Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16.
        If you are deploying to another type of region, please check regional availability first.

        :default: - a default log group created by AWS Lambda
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''The number of days that the lambda function's log events are kept in CloudWatch Logs.

        This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can.
        ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it.

        :default: logs.RetentionDays.INFINITE
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket.

        If you are deploying large files, you will need to increase this number
        accordingly.

        :default: 128
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined object metadata to be set on all objects in the deployment.

        :default: - No user metadata is set
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def output_object_keys(self) -> typing.Optional[builtins.bool]:
        '''If set to false, the custom resource will not send back the SourceObjectKeys.

        This is useful when you are facing the error ``Response object is too long``

        See https://github.com/aws/aws-cdk/issues/28579

        :default: true
        '''
        result = self._values.get("output_object_keys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prune(self) -> typing.Optional[builtins.bool]:
        '''If this is set to false, files in the destination bucket that do not exist in the asset, will NOT be deleted during deployment (create/update).

        :default: true
        '''
        result = self._values.get("prune")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retain_on_delete(self) -> typing.Optional[builtins.bool]:
        '''If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated.

        NOTICE: Configuring this to "false" might have operational implications. Please
        visit to the package documentation referred below to make sure you fully understand those implications.

        :default: true - when resource is deleted/updated, files are retained
        '''
        result = self._values.get("retain_on_delete")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Execution role associated with this function.

        :default: - A role is automatically created
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def server_side_encryption(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.ServerSideEncryption]:
        '''System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment.

        :default: - Server side encryption is not used.
        '''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.ServerSideEncryption], result)

    @builtins.property
    def server_side_encryption_aws_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment.

        :default: - Not set.
        '''
        result = self._values.get("server_side_encryption_aws_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_customer_algorithm(
        self,
    ) -> typing.Optional[builtins.str]:
        '''System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment.

        Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080

        :default: - Not set.
        '''
        result = self._values.get("server_side_encryption_customer_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_content(self) -> typing.Optional[builtins.bool]:
        '''If set to true, uploads will precompute the value of ``x-amz-content-sha256`` and include it in the signed S3 request headers.

        :default: - ``x-amz-content-sha256`` will not be computed
        '''
        result = self._values.get("sign_content")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.ISource]]:
        '''The sources from which to deploy the contents of this bucket.'''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.ISource]], result)

    @builtins.property
    def storage_class(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.StorageClass]:
        '''System-defined x-amz-storage-class metadata to be set on all objects in the deployment.

        :default: - Default storage-class for the bucket is used.
        '''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.StorageClass], result)

    @builtins.property
    def use_efs(self) -> typing.Optional[builtins.bool]:
        '''Mount an EFS file system.

        Enable this if your assets are large and you encounter disk space errors.
        Enabling this option will require a VPC to be specified.

        :default: - No EFS. Lambda has access only to 512MB of disk space.
        '''
        result = self._values.get("use_efs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''The VPC network to place the deployment lambda handler in.

        This is required if ``useEfs`` is set.

        :default: None
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where in the VPC to place the deployment lambda handler.

        Only used if 'vpc' is supplied.

        :default: - the Vpc default strategy if not specified
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def website_redirect_location(self) -> typing.Optional[builtins.str]:
        '''System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment.

        :default: - No website redirection.
        '''
        result = self._values.get("website_redirect_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.static_website.CidrAllowList",
    jsii_struct_bases=[],
    name_mapping={"cidr_ranges": "cidrRanges", "cidr_type": "cidrType"},
)
class CidrAllowList:
    def __init__(
        self,
        *,
        cidr_ranges: typing.Sequence[builtins.str],
        cidr_type: builtins.str,
    ) -> None:
        '''Representation of a CIDR range.

        :param cidr_ranges: Specify an IPv4 address by using CIDR notation. For example: To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify 192.0.2.44/32 . To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify 192.0.2.0/24 . For more information about CIDR notation, see the Wikipedia entry Classless Inter-Domain Routing . Specify an IPv6 address by using CIDR notation. For example: To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify 1111:0000:0000:0000:0000:0000:0000:0111/128 . To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify 1111:0000:0000:0000:0000:0000:0000:0000/64 .
        :param cidr_type: Type of CIDR range.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1267163e7fcc8cf0006acbd7d5f318bdc920012f2da422be9edbc7bac06ba58)
            check_type(argname="argument cidr_ranges", value=cidr_ranges, expected_type=type_hints["cidr_ranges"])
            check_type(argname="argument cidr_type", value=cidr_type, expected_type=type_hints["cidr_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr_ranges": cidr_ranges,
            "cidr_type": cidr_type,
        }

    @builtins.property
    def cidr_ranges(self) -> typing.List[builtins.str]:
        '''Specify an IPv4 address by using CIDR notation.

        For example:
        To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify 192.0.2.44/32 .
        To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify 192.0.2.0/24 .

        For more information about CIDR notation, see the Wikipedia entry Classless Inter-Domain Routing .

        Specify an IPv6 address by using CIDR notation. For example:
        To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify 1111:0000:0000:0000:0000:0000:0000:0111/128 .
        To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify 1111:0000:0000:0000:0000:0000:0000:0000/64 .
        '''
        result = self._values.get("cidr_ranges")
        assert result is not None, "Required property 'cidr_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cidr_type(self) -> builtins.str:
        '''Type of CIDR range.'''
        result = self._values.get("cidr_type")
        assert result is not None, "Required property 'cidr_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CidrAllowList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.static_website.CloudFrontWebAclProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr_allow_list": "cidrAllowList",
        "disable": "disable",
        "managed_rules": "managedRules",
    },
)
class CloudFrontWebAclProps:
    def __init__(
        self,
        *,
        cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[builtins.str, typing.Any]]] = None,
        disable: typing.Optional[builtins.bool] = None,
        managed_rules: typing.Optional[typing.Sequence[typing.Union["ManagedRule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties to configure the web acl.

        :param cidr_allow_list: List of cidr ranges to allow. Default: - undefined
        :param disable: Set to true to prevent creation of a web acl for the static website. Default: false
        :param managed_rules: List of managed rules to apply to the web acl. Default: - [{ vendor: "AWS", name: "AWSManagedRulesCommonRuleSet" }]
        '''
        if isinstance(cidr_allow_list, dict):
            cidr_allow_list = CidrAllowList(**cidr_allow_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281e597b1d3293d9222882c06265c8295681b7a1ca52817d8d13f247fda862ab)
            check_type(argname="argument cidr_allow_list", value=cidr_allow_list, expected_type=type_hints["cidr_allow_list"])
            check_type(argname="argument disable", value=disable, expected_type=type_hints["disable"])
            check_type(argname="argument managed_rules", value=managed_rules, expected_type=type_hints["managed_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidr_allow_list is not None:
            self._values["cidr_allow_list"] = cidr_allow_list
        if disable is not None:
            self._values["disable"] = disable
        if managed_rules is not None:
            self._values["managed_rules"] = managed_rules

    @builtins.property
    def cidr_allow_list(self) -> typing.Optional[CidrAllowList]:
        '''List of cidr ranges to allow.

        :default: - undefined
        '''
        result = self._values.get("cidr_allow_list")
        return typing.cast(typing.Optional[CidrAllowList], result)

    @builtins.property
    def disable(self) -> typing.Optional[builtins.bool]:
        '''Set to true to prevent creation of a web acl for the static website.

        :default: false
        '''
        result = self._values.get("disable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def managed_rules(self) -> typing.Optional[typing.List["ManagedRule"]]:
        '''List of managed rules to apply to the web acl.

        :default: - [{ vendor: "AWS", name: "AWSManagedRulesCommonRuleSet" }]
        '''
        result = self._values.get("managed_rules")
        return typing.cast(typing.Optional[typing.List["ManagedRule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFrontWebAclProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontWebAcl(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.static_website.CloudfrontWebAcl",
):
    '''This construct creates a WAFv2 Web ACL for cloudfront in the us-east-1 region (required for cloudfront) no matter the region of the parent cdk stack.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[builtins.str, typing.Any]]] = None,
        disable: typing.Optional[builtins.bool] = None,
        managed_rules: typing.Optional[typing.Sequence[typing.Union["ManagedRule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cidr_allow_list: List of cidr ranges to allow. Default: - undefined
        :param disable: Set to true to prevent creation of a web acl for the static website. Default: false
        :param managed_rules: List of managed rules to apply to the web acl. Default: - [{ vendor: "AWS", name: "AWSManagedRulesCommonRuleSet" }]
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8786eb313347778f068f76fe2f2b76f8c245a30cf36116a7d53addfe47ba792)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudFrontWebAclProps(
            cidr_allow_list=cidr_allow_list,
            disable=disable,
            managed_rules=managed_rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="webAclArn")
    def web_acl_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webAclArn"))

    @builtins.property
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webAclId"))


@jsii.data_type(
    jsii_type="@aws/pdk.static_website.DistributionProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_behaviors": "additionalBehaviors",
        "certificate": "certificate",
        "comment": "comment",
        "default_behavior": "defaultBehavior",
        "default_root_object": "defaultRootObject",
        "domain_names": "domainNames",
        "enabled": "enabled",
        "enable_ipv6": "enableIpv6",
        "enable_logging": "enableLogging",
        "error_responses": "errorResponses",
        "geo_restriction": "geoRestriction",
        "http_version": "httpVersion",
        "log_bucket": "logBucket",
        "log_file_prefix": "logFilePrefix",
        "log_includes_cookies": "logIncludesCookies",
        "minimum_protocol_version": "minimumProtocolVersion",
        "price_class": "priceClass",
        "publish_additional_metrics": "publishAdditionalMetrics",
        "ssl_support_method": "sslSupportMethod",
        "web_acl_id": "webAclId",
    },
)
class DistributionProps:
    def __init__(
        self,
        *,
        additional_behaviors: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        comment: typing.Optional[builtins.str] = None,
        default_behavior: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_ipv6: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
        geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
        http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
        log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
        minimum_protocol_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol] = None,
        price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
        publish_additional_metrics: typing.Optional[builtins.bool] = None,
        ssl_support_method: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''DistributionProps.

        :param additional_behaviors: Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to. Default: - no additional behaviors are added.
        :param certificate: A certificate to associate with the distribution. The certificate must be located in N. Virginia (us-east-1). Default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        :param comment: Any comments you want to include about the distribution. Default: - no comment
        :param default_behavior: The default behavior for the distribution.
        :param default_root_object: The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/). Default: - no default root object
        :param domain_names: Alternative domain names for this distribution. If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name, you can add an alternate domain name to your distribution. If you attach a certificate to the distribution, you should add (at least one of) the domain names of the certificate to this list. When you want to move a domain name between distributions, you can associate a certificate without specifying any domain names. For more information, see the *Moving an alternate domain name to a different distribution* section in the README. Default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        :param enabled: Enable or disable the distribution. Default: true
        :param enable_ipv6: Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address. If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses. This allows viewers to submit a second request, for an IPv4 address for your distribution. Default: true
        :param enable_logging: Enable access logging for the distribution. Default: - false, unless ``logBucket`` is specified.
        :param error_responses: How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - No custom error responses.
        :param geo_restriction: Controls the countries in which your content is distributed. Default: - No geographic restrictions
        :param http_version: Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront. For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI). Default: HttpVersion.HTTP2
        :param log_bucket: The Amazon S3 bucket to store the access logs in. Make sure to set ``objectOwnership`` to ``s3.ObjectOwnership.OBJECT_WRITER`` in your custom bucket. Default: - A bucket is created if ``enableLogging`` is true
        :param log_file_prefix: An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: Specifies whether you want CloudFront to include cookies in access logs. Default: false
        :param minimum_protocol_version: The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify. Default: - SecurityPolicyProtocol.TLS_V1_2_2021 if the '@aws-cdk/aws-cloudfront:defaultSecurityPolicyTLSv1.2_2021' feature flag is set; otherwise, SecurityPolicyProtocol.TLS_V1_2_2019.
        :param price_class: The price class that corresponds with the maximum price that you want to pay for CloudFront service. If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations. If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location that has the lowest latency among the edge locations in your price class. Default: PriceClass.PRICE_CLASS_ALL
        :param publish_additional_metrics: Whether to enable additional CloudWatch metrics. Default: false
        :param ssl_support_method: The SSL method CloudFront will use for your distribution. Server Name Indication (SNI) - is an extension to the TLS computer networking protocol by which a client indicates which hostname it is attempting to connect to at the start of the handshaking process. This allows a server to present multiple certificates on the same IP address and TCP port number and hence allows multiple secure (HTTPS) websites (or any other service over TLS) to be served by the same IP address without requiring all those sites to use the same certificate. CloudFront can use SNI to host multiple distributions on the same IP - which a large majority of clients will support. If your clients cannot support SNI however - CloudFront can use dedicated IPs for your distribution - but there is a prorated monthly charge for using this feature. By default, we use SNI - but you can optionally enable dedicated IPs (VIP). See the CloudFront SSL for more details about pricing : https://aws.amazon.com/cloudfront/custom-ssl-domains/ Default: SSLMethod.SNI
        :param web_acl_id: Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).
        '''
        if isinstance(default_behavior, dict):
            default_behavior = _aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions(**default_behavior)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51caeda5a7a1165ca66a169352220b2e8ce33a39028b802dd5721fb1761b8fc7)
            check_type(argname="argument additional_behaviors", value=additional_behaviors, expected_type=type_hints["additional_behaviors"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument default_behavior", value=default_behavior, expected_type=type_hints["default_behavior"])
            check_type(argname="argument default_root_object", value=default_root_object, expected_type=type_hints["default_root_object"])
            check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_ipv6", value=enable_ipv6, expected_type=type_hints["enable_ipv6"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument error_responses", value=error_responses, expected_type=type_hints["error_responses"])
            check_type(argname="argument geo_restriction", value=geo_restriction, expected_type=type_hints["geo_restriction"])
            check_type(argname="argument http_version", value=http_version, expected_type=type_hints["http_version"])
            check_type(argname="argument log_bucket", value=log_bucket, expected_type=type_hints["log_bucket"])
            check_type(argname="argument log_file_prefix", value=log_file_prefix, expected_type=type_hints["log_file_prefix"])
            check_type(argname="argument log_includes_cookies", value=log_includes_cookies, expected_type=type_hints["log_includes_cookies"])
            check_type(argname="argument minimum_protocol_version", value=minimum_protocol_version, expected_type=type_hints["minimum_protocol_version"])
            check_type(argname="argument price_class", value=price_class, expected_type=type_hints["price_class"])
            check_type(argname="argument publish_additional_metrics", value=publish_additional_metrics, expected_type=type_hints["publish_additional_metrics"])
            check_type(argname="argument ssl_support_method", value=ssl_support_method, expected_type=type_hints["ssl_support_method"])
            check_type(argname="argument web_acl_id", value=web_acl_id, expected_type=type_hints["web_acl_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_behaviors is not None:
            self._values["additional_behaviors"] = additional_behaviors
        if certificate is not None:
            self._values["certificate"] = certificate
        if comment is not None:
            self._values["comment"] = comment
        if default_behavior is not None:
            self._values["default_behavior"] = default_behavior
        if default_root_object is not None:
            self._values["default_root_object"] = default_root_object
        if domain_names is not None:
            self._values["domain_names"] = domain_names
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_ipv6 is not None:
            self._values["enable_ipv6"] = enable_ipv6
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if error_responses is not None:
            self._values["error_responses"] = error_responses
        if geo_restriction is not None:
            self._values["geo_restriction"] = geo_restriction
        if http_version is not None:
            self._values["http_version"] = http_version
        if log_bucket is not None:
            self._values["log_bucket"] = log_bucket
        if log_file_prefix is not None:
            self._values["log_file_prefix"] = log_file_prefix
        if log_includes_cookies is not None:
            self._values["log_includes_cookies"] = log_includes_cookies
        if minimum_protocol_version is not None:
            self._values["minimum_protocol_version"] = minimum_protocol_version
        if price_class is not None:
            self._values["price_class"] = price_class
        if publish_additional_metrics is not None:
            self._values["publish_additional_metrics"] = publish_additional_metrics
        if ssl_support_method is not None:
            self._values["ssl_support_method"] = ssl_support_method
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

    @builtins.property
    def additional_behaviors(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions]]:
        '''Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to.

        :default: - no additional behaviors are added.
        '''
        result = self._values.get("additional_behaviors")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''A certificate to associate with the distribution.

        The certificate must be located in N. Virginia (us-east-1).

        :default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Any comments you want to include about the distribution.

        :default: - no comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_behavior(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions]:
        '''The default behavior for the distribution.'''
        result = self._values.get("default_behavior")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions], result)

    @builtins.property
    def default_root_object(self) -> typing.Optional[builtins.str]:
        '''The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/).

        :default: - no default root object
        '''
        result = self._values.get("default_root_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Alternative domain names for this distribution.

        If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name,
        you can add an alternate domain name to your distribution. If you attach a certificate to the distribution,
        you should add (at least one of) the domain names of the certificate to this list.

        When you want to move a domain name between distributions, you can associate a certificate without specifying any domain names.
        For more information, see the *Moving an alternate domain name to a different distribution* section in the README.

        :default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        '''
        result = self._values.get("domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Enable or disable the distribution.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_ipv6(self) -> typing.Optional[builtins.bool]:
        '''Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address.

        If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses.
        This allows viewers to submit a second request, for an IPv4 address for your distribution.

        :default: true
        '''
        result = self._values.get("enable_ipv6")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Enable access logging for the distribution.

        :default: - false, unless ``logBucket`` is specified.
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def error_responses(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]]:
        '''How CloudFront should handle requests that are not successful (e.g., PageNotFound).

        :default: - No custom error responses.
        '''
        result = self._values.get("error_responses")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]], result)

    @builtins.property
    def geo_restriction(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction]:
        '''Controls the countries in which your content is distributed.

        :default: - No geographic restrictions
        '''
        result = self._values.get("geo_restriction")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction], result)

    @builtins.property
    def http_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion]:
        '''Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront.

        For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI).

        :default: HttpVersion.HTTP2
        '''
        result = self._values.get("http_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion], result)

    @builtins.property
    def log_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''The Amazon S3 bucket to store the access logs in.

        Make sure to set ``objectOwnership`` to ``s3.ObjectOwnership.OBJECT_WRITER`` in your custom bucket.

        :default: - A bucket is created if ``enableLogging`` is true
        '''
        result = self._values.get("log_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def log_file_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional string that you want CloudFront to prefix to the access log filenames for this distribution.

        :default: - no prefix
        '''
        result = self._values.get("log_file_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_includes_cookies(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether you want CloudFront to include cookies in access logs.

        :default: false
        '''
        result = self._values.get("log_includes_cookies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minimum_protocol_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol]:
        '''The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections.

        CloudFront serves your objects only to browsers or devices that support at
        least the SSL version that you specify.

        :default: - SecurityPolicyProtocol.TLS_V1_2_2021 if the '@aws-cdk/aws-cloudfront:defaultSecurityPolicyTLSv1.2_2021' feature flag is set; otherwise, SecurityPolicyProtocol.TLS_V1_2_2019.
        '''
        result = self._values.get("minimum_protocol_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol], result)

    @builtins.property
    def price_class(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass]:
        '''The price class that corresponds with the maximum price that you want to pay for CloudFront service.

        If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations.
        If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location
        that has the lowest latency among the edge locations in your price class.

        :default: PriceClass.PRICE_CLASS_ALL
        '''
        result = self._values.get("price_class")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass], result)

    @builtins.property
    def publish_additional_metrics(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable additional CloudWatch metrics.

        :default: false
        '''
        result = self._values.get("publish_additional_metrics")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ssl_support_method(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod]:
        '''The SSL method CloudFront will use for your distribution.

        Server Name Indication (SNI) - is an extension to the TLS computer networking protocol by which a client indicates
        which hostname it is attempting to connect to at the start of the handshaking process. This allows a server to present
        multiple certificates on the same IP address and TCP port number and hence allows multiple secure (HTTPS) websites
        (or any other service over TLS) to be served by the same IP address without requiring all those sites to use the same certificate.

        CloudFront can use SNI to host multiple distributions on the same IP - which a large majority of clients will support.

        If your clients cannot support SNI however - CloudFront can use dedicated IPs for your distribution - but there is a prorated monthly charge for
        using this feature. By default, we use SNI - but you can optionally enable dedicated IPs (VIP).

        See the CloudFront SSL for more details about pricing : https://aws.amazon.com/cloudfront/custom-ssl-domains/

        :default: SSLMethod.SNI
        '''
        result = self._values.get("ssl_support_method")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod], result)

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution.

        To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example
        ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``.
        To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``.

        :default: - No AWS Web Application Firewall web access control list (web ACL).
        '''
        result = self._values.get("web_acl_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DistributionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.static_website.ManagedRule",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "vendor": "vendor"},
)
class ManagedRule:
    def __init__(self, *, name: builtins.str, vendor: builtins.str) -> None:
        '''Represents a WAF V2 managed rule.

        :param name: The name of the managed rule group. You use this, along with the vendor name, to identify the rule group.
        :param vendor: The name of the managed rule group vendor. You use this, along with the rule group name, to identify the rule group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037433be7d5e686c0208bf07132e613d9d38cebafa7e7e61dd6f7af6e2caafba)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vendor", value=vendor, expected_type=type_hints["vendor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vendor": vendor,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the managed rule group.

        You use this, along with the vendor name, to identify the rule group.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vendor(self) -> builtins.str:
        '''The name of the managed rule group vendor.

        You use this, along with the rule group name, to identify the rule group.
        '''
        result = self._values.get("vendor")
        assert result is not None, "Required property 'vendor' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.static_website.RuntimeOptions",
    jsii_struct_bases=[],
    name_mapping={"json_payload": "jsonPayload", "json_file_name": "jsonFileName"},
)
class RuntimeOptions:
    def __init__(
        self,
        *,
        json_payload: typing.Any,
        json_file_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Dynamic configuration which gets resolved only during deployment.

        :param json_payload: Arbitrary JSON payload containing runtime values to deploy. Typically this contains resourceArns, etc which are only known at deploy time.
        :param json_file_name: File name to store runtime configuration (jsonPayload). Must follow pattern: '*.json' Default: "runtime-config.json"

        Example::

            // Will store a JSON file called runtime-config.json in the root of the StaticWebsite S3 bucket containing any
            // and all resolved values.
            const runtimeConfig = {jsonPayload: {bucketArn: s3Bucket.bucketArn}};
            new StaticWebsite(scope, 'StaticWebsite', {websiteContentPath: 'path/to/website', runtimeConfig});
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c6e2afa52fd59c7ccd05ca815a4ea2dbe589f82cbe7ae6436fcc7361133650)
            check_type(argname="argument json_payload", value=json_payload, expected_type=type_hints["json_payload"])
            check_type(argname="argument json_file_name", value=json_file_name, expected_type=type_hints["json_file_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "json_payload": json_payload,
        }
        if json_file_name is not None:
            self._values["json_file_name"] = json_file_name

    @builtins.property
    def json_payload(self) -> typing.Any:
        '''Arbitrary JSON payload containing runtime values to deploy.

        Typically this contains resourceArns, etc which
        are only known at deploy time.

        Example::

            { userPoolId: some.userPool.userPoolId, someResourceArn: some.resource.Arn }
        '''
        result = self._values.get("json_payload")
        assert result is not None, "Required property 'json_payload' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def json_file_name(self) -> typing.Optional[builtins.str]:
        '''File name to store runtime configuration (jsonPayload).

        Must follow pattern: '*.json'

        :default: "runtime-config.json"
        '''
        result = self._values.get("json_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuntimeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StaticWebsite(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.static_website.StaticWebsite",
):
    '''Deploys a Static Website using by default a private S3 bucket as an origin and Cloudfront as the entrypoint.

    This construct configures a webAcl containing rules that are generally applicable to web applications. This
    provides protection against exploitation of a wide range of vulnerabilities, including some of the high risk
    and commonly occurring vulnerabilities described in OWASP publications such as OWASP Top 10.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        website_content_path: builtins.str,
        bucket_deployment_props: typing.Optional[typing.Union[BucketDeploymentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        default_website_bucket_encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
        default_website_bucket_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        distribution_props: typing.Optional[typing.Union[DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[builtins.str, typing.Any]]] = None,
        website_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param website_content_path: Path to the directory containing the static website files and assets. This directory must contain an index.html file.
        :param bucket_deployment_props: Custom bucket deployment properties. Example::
        :param default_website_bucket_encryption: Bucket encryption to use for the default bucket. Supported options are KMS or S3MANAGED. Note: If planning to use KMS, ensure you associate a Lambda Edge function to sign requests to S3 as OAI does not currently support KMS encryption. Refer to {@link https://aws.amazon.com/blogs/networking-and-content-delivery/serving-sse-kms-encrypted-content-from-s3-using-cloudfront/} Default: - "S3MANAGED"
        :param default_website_bucket_encryption_key: A predefined KMS customer encryption key to use for the default bucket that gets created. Note: This is only used if the websiteBucket is left undefined, otherwise all settings from the provided websiteBucket will be used.
        :param distribution_props: Custom distribution properties. Note: defaultBehaviour.origin is a required parameter, however it will not be used as this construct will wire it on your behalf. You will need to pass in an instance of StaticWebsiteOrigin (NoOp) to keep the compiler happy.
        :param runtime_options: Dynamic configuration which gets resolved only during deployment.
        :param web_acl_props: Limited configuration settings for the generated webAcl. For more advanced settings, create your own ACL and pass in the webAclId as a param to distributionProps. Note: If pass in your own ACL, make sure the SCOPE is CLOUDFRONT and it is created in us-east-1.
        :param website_bucket: Predefined bucket to deploy the website into.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e861586e70512ee1a5a11620e2444be497d63cc6cc69e3fd1302c3413987fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StaticWebsiteProps(
            website_content_path=website_content_path,
            bucket_deployment_props=bucket_deployment_props,
            default_website_bucket_encryption=default_website_bucket_encryption,
            default_website_bucket_encryption_key=default_website_bucket_encryption_key,
            distribution_props=distribution_props,
            runtime_options=runtime_options,
            web_acl_props=web_acl_props,
            website_bucket=website_bucket,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucketDeployment")
    def bucket_deployment(self) -> _aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment:
        return typing.cast(_aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment, jsii.get(self, "bucketDeployment"))

    @builtins.property
    @jsii.member(jsii_name="cloudFrontDistribution")
    def cloud_front_distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.Distribution:
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.Distribution, jsii.get(self, "cloudFrontDistribution"))

    @builtins.property
    @jsii.member(jsii_name="websiteBucket")
    def website_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "websiteBucket"))


@jsii.implements(_aws_cdk_aws_cloudfront_ceddda9d.IOrigin)
class StaticWebsiteOrigin(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.static_website.StaticWebsiteOrigin",
):
    '''If passing in distributionProps, the default behaviour.origin is a required parameter. An instance of this class can be passed in to make the compiler happy.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        *,
        origin_id: builtins.str,
        distribution_id: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.OriginBindConfig:
        '''The method called when a given Origin is added (for the first time) to a Distribution.

        :param _scope: -
        :param origin_id: The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.
        :param distribution_id: The identifier of the Distribution this Origin is used for. This is used to grant origin access permissions to the distribution for origin access control. Default: - no distribution id
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3291cdc3536b7266290b0ad7000ee922e18bcfa35c396d1b19a5a6d2f4e4d33e)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        _options = _aws_cdk_aws_cloudfront_ceddda9d.OriginBindOptions(
            origin_id=origin_id, distribution_id=distribution_id
        )

        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.OriginBindConfig, jsii.invoke(self, "bind", [_scope, _options]))


@jsii.data_type(
    jsii_type="@aws/pdk.static_website.StaticWebsiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "website_content_path": "websiteContentPath",
        "bucket_deployment_props": "bucketDeploymentProps",
        "default_website_bucket_encryption": "defaultWebsiteBucketEncryption",
        "default_website_bucket_encryption_key": "defaultWebsiteBucketEncryptionKey",
        "distribution_props": "distributionProps",
        "runtime_options": "runtimeOptions",
        "web_acl_props": "webAclProps",
        "website_bucket": "websiteBucket",
    },
)
class StaticWebsiteProps:
    def __init__(
        self,
        *,
        website_content_path: builtins.str,
        bucket_deployment_props: typing.Optional[typing.Union[BucketDeploymentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        default_website_bucket_encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
        default_website_bucket_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        distribution_props: typing.Optional[typing.Union[DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[builtins.str, typing.Any]]] = None,
        website_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    ) -> None:
        '''Properties for configuring the StaticWebsite.

        :param website_content_path: Path to the directory containing the static website files and assets. This directory must contain an index.html file.
        :param bucket_deployment_props: Custom bucket deployment properties. Example::
        :param default_website_bucket_encryption: Bucket encryption to use for the default bucket. Supported options are KMS or S3MANAGED. Note: If planning to use KMS, ensure you associate a Lambda Edge function to sign requests to S3 as OAI does not currently support KMS encryption. Refer to {@link https://aws.amazon.com/blogs/networking-and-content-delivery/serving-sse-kms-encrypted-content-from-s3-using-cloudfront/} Default: - "S3MANAGED"
        :param default_website_bucket_encryption_key: A predefined KMS customer encryption key to use for the default bucket that gets created. Note: This is only used if the websiteBucket is left undefined, otherwise all settings from the provided websiteBucket will be used.
        :param distribution_props: Custom distribution properties. Note: defaultBehaviour.origin is a required parameter, however it will not be used as this construct will wire it on your behalf. You will need to pass in an instance of StaticWebsiteOrigin (NoOp) to keep the compiler happy.
        :param runtime_options: Dynamic configuration which gets resolved only during deployment.
        :param web_acl_props: Limited configuration settings for the generated webAcl. For more advanced settings, create your own ACL and pass in the webAclId as a param to distributionProps. Note: If pass in your own ACL, make sure the SCOPE is CLOUDFRONT and it is created in us-east-1.
        :param website_bucket: Predefined bucket to deploy the website into.
        '''
        if isinstance(bucket_deployment_props, dict):
            bucket_deployment_props = BucketDeploymentProps(**bucket_deployment_props)
        if isinstance(distribution_props, dict):
            distribution_props = DistributionProps(**distribution_props)
        if isinstance(runtime_options, dict):
            runtime_options = RuntimeOptions(**runtime_options)
        if isinstance(web_acl_props, dict):
            web_acl_props = CloudFrontWebAclProps(**web_acl_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06d868e725c22a43b080fe9e6d5be5da6c929595866c513d3c6d1249463e7dac)
            check_type(argname="argument website_content_path", value=website_content_path, expected_type=type_hints["website_content_path"])
            check_type(argname="argument bucket_deployment_props", value=bucket_deployment_props, expected_type=type_hints["bucket_deployment_props"])
            check_type(argname="argument default_website_bucket_encryption", value=default_website_bucket_encryption, expected_type=type_hints["default_website_bucket_encryption"])
            check_type(argname="argument default_website_bucket_encryption_key", value=default_website_bucket_encryption_key, expected_type=type_hints["default_website_bucket_encryption_key"])
            check_type(argname="argument distribution_props", value=distribution_props, expected_type=type_hints["distribution_props"])
            check_type(argname="argument runtime_options", value=runtime_options, expected_type=type_hints["runtime_options"])
            check_type(argname="argument web_acl_props", value=web_acl_props, expected_type=type_hints["web_acl_props"])
            check_type(argname="argument website_bucket", value=website_bucket, expected_type=type_hints["website_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "website_content_path": website_content_path,
        }
        if bucket_deployment_props is not None:
            self._values["bucket_deployment_props"] = bucket_deployment_props
        if default_website_bucket_encryption is not None:
            self._values["default_website_bucket_encryption"] = default_website_bucket_encryption
        if default_website_bucket_encryption_key is not None:
            self._values["default_website_bucket_encryption_key"] = default_website_bucket_encryption_key
        if distribution_props is not None:
            self._values["distribution_props"] = distribution_props
        if runtime_options is not None:
            self._values["runtime_options"] = runtime_options
        if web_acl_props is not None:
            self._values["web_acl_props"] = web_acl_props
        if website_bucket is not None:
            self._values["website_bucket"] = website_bucket

    @builtins.property
    def website_content_path(self) -> builtins.str:
        '''Path to the directory containing the static website files and assets.

        This directory must contain an index.html file.
        '''
        result = self._values.get("website_content_path")
        assert result is not None, "Required property 'website_content_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_deployment_props(self) -> typing.Optional[BucketDeploymentProps]:
        '''Custom bucket deployment properties.

        Example::
        '''
        result = self._values.get("bucket_deployment_props")
        return typing.cast(typing.Optional[BucketDeploymentProps], result)

    @builtins.property
    def default_website_bucket_encryption(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption]:
        '''Bucket encryption to use for the default bucket.

        Supported options are KMS or S3MANAGED.

        Note: If planning to use KMS, ensure you associate a Lambda Edge function to sign requests to S3 as OAI does not currently support KMS encryption. Refer to {@link https://aws.amazon.com/blogs/networking-and-content-delivery/serving-sse-kms-encrypted-content-from-s3-using-cloudfront/}

        :default: - "S3MANAGED"
        '''
        result = self._values.get("default_website_bucket_encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption], result)

    @builtins.property
    def default_website_bucket_encryption_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key]:
        '''A predefined KMS customer encryption key to use for the default bucket that gets created.

        Note: This is only used if the websiteBucket is left undefined, otherwise all settings from the provided websiteBucket will be used.
        '''
        result = self._values.get("default_website_bucket_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key], result)

    @builtins.property
    def distribution_props(self) -> typing.Optional[DistributionProps]:
        '''Custom distribution properties.

        Note: defaultBehaviour.origin is a required parameter, however it will not be used as this construct will wire it on your behalf.
        You will need to pass in an instance of StaticWebsiteOrigin (NoOp) to keep the compiler happy.
        '''
        result = self._values.get("distribution_props")
        return typing.cast(typing.Optional[DistributionProps], result)

    @builtins.property
    def runtime_options(self) -> typing.Optional[RuntimeOptions]:
        '''Dynamic configuration which gets resolved only during deployment.'''
        result = self._values.get("runtime_options")
        return typing.cast(typing.Optional[RuntimeOptions], result)

    @builtins.property
    def web_acl_props(self) -> typing.Optional[CloudFrontWebAclProps]:
        '''Limited configuration settings for the generated webAcl.

        For more advanced settings, create your own ACL and pass in the webAclId as a param to distributionProps.

        Note: If pass in your own ACL, make sure the SCOPE is CLOUDFRONT and it is created in us-east-1.
        '''
        result = self._values.get("web_acl_props")
        return typing.cast(typing.Optional[CloudFrontWebAclProps], result)

    @builtins.property
    def website_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''Predefined bucket to deploy the website into.'''
        result = self._values.get("website_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticWebsiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BucketDeploymentProps",
    "CidrAllowList",
    "CloudFrontWebAclProps",
    "CloudfrontWebAcl",
    "DistributionProps",
    "ManagedRule",
    "RuntimeOptions",
    "StaticWebsite",
    "StaticWebsiteOrigin",
    "StaticWebsiteProps",
]

publication.publish()

def _typecheckingstub__6ac3ac892a82bdd981340a9bff81d3e846e798cd03c6b162864b0df3ac5cdba4(
    *,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    cache_control: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_deployment_ceddda9d.CacheControl]] = None,
    content_disposition: typing.Optional[builtins.str] = None,
    content_encoding: typing.Optional[builtins.str] = None,
    content_language: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    destination_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    destination_key_prefix: typing.Optional[builtins.str] = None,
    distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
    distribution_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    expires: typing.Optional[_aws_cdk_ceddda9d.Expiration] = None,
    extract: typing.Optional[builtins.bool] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    output_object_keys: typing.Optional[builtins.bool] = None,
    prune: typing.Optional[builtins.bool] = None,
    retain_on_delete: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    server_side_encryption: typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.ServerSideEncryption] = None,
    server_side_encryption_aws_kms_key_id: typing.Optional[builtins.str] = None,
    server_side_encryption_customer_algorithm: typing.Optional[builtins.str] = None,
    sign_content: typing.Optional[builtins.bool] = None,
    sources: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_deployment_ceddda9d.ISource]] = None,
    storage_class: typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.StorageClass] = None,
    use_efs: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    website_redirect_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1267163e7fcc8cf0006acbd7d5f318bdc920012f2da422be9edbc7bac06ba58(
    *,
    cidr_ranges: typing.Sequence[builtins.str],
    cidr_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281e597b1d3293d9222882c06265c8295681b7a1ca52817d8d13f247fda862ab(
    *,
    cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[builtins.str, typing.Any]]] = None,
    disable: typing.Optional[builtins.bool] = None,
    managed_rules: typing.Optional[typing.Sequence[typing.Union[ManagedRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8786eb313347778f068f76fe2f2b76f8c245a30cf36116a7d53addfe47ba792(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[builtins.str, typing.Any]]] = None,
    disable: typing.Optional[builtins.bool] = None,
    managed_rules: typing.Optional[typing.Sequence[typing.Union[ManagedRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51caeda5a7a1165ca66a169352220b2e8ce33a39028b802dd5721fb1761b8fc7(
    *,
    additional_behaviors: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    comment: typing.Optional[builtins.str] = None,
    default_behavior: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    default_root_object: typing.Optional[builtins.str] = None,
    domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    enable_ipv6: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
    geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
    http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
    log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    log_file_prefix: typing.Optional[builtins.str] = None,
    log_includes_cookies: typing.Optional[builtins.bool] = None,
    minimum_protocol_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol] = None,
    price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
    publish_additional_metrics: typing.Optional[builtins.bool] = None,
    ssl_support_method: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037433be7d5e686c0208bf07132e613d9d38cebafa7e7e61dd6f7af6e2caafba(
    *,
    name: builtins.str,
    vendor: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c6e2afa52fd59c7ccd05ca815a4ea2dbe589f82cbe7ae6436fcc7361133650(
    *,
    json_payload: typing.Any,
    json_file_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e861586e70512ee1a5a11620e2444be497d63cc6cc69e3fd1302c3413987fc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    website_content_path: builtins.str,
    bucket_deployment_props: typing.Optional[typing.Union[BucketDeploymentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    default_website_bucket_encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
    default_website_bucket_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    distribution_props: typing.Optional[typing.Union[DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[builtins.str, typing.Any]]] = None,
    website_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3291cdc3536b7266290b0ad7000ee922e18bcfa35c396d1b19a5a6d2f4e4d33e(
    _scope: _constructs_77d1e7e8.Construct,
    *,
    origin_id: builtins.str,
    distribution_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d868e725c22a43b080fe9e6d5be5da6c929595866c513d3c6d1249463e7dac(
    *,
    website_content_path: builtins.str,
    bucket_deployment_props: typing.Optional[typing.Union[BucketDeploymentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    default_website_bucket_encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
    default_website_bucket_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    distribution_props: typing.Optional[typing.Union[DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[builtins.str, typing.Any]]] = None,
    website_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
) -> None:
    """Type checking stubs"""
    pass
