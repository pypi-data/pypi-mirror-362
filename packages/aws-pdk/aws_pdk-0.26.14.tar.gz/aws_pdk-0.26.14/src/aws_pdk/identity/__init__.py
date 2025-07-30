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
import aws_cdk.aws_cognito as _aws_cdk_aws_cognito_ceddda9d
import aws_cdk.aws_cognito_identitypool_alpha as _aws_cdk_aws_cognito_identitypool_alpha_e0ee7798
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import constructs as _constructs_77d1e7e8


class UserIdentity(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.identity.UserIdentity",
):
    '''Creates a UserPool and Identity Pool with sane defaults configured intended for usage from a web client.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allow_signup: typing.Optional[builtins.bool] = None,
        identity_pool_options: typing.Optional[typing.Union[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps, typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allow_signup: Allow self sign up. Default: - false
        :param identity_pool_options: Configuration for the Identity Pool.
        :param user_pool: User provided Cognito UserPool. Default: - a userpool with mfa will be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dda65570bf25bbaff83417268c7c0a7e08163811a20c7a7401e4a59fb1b444b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UserIdentityProps(
            allow_signup=allow_signup,
            identity_pool_options=identity_pool_options,
            user_pool=user_pool,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="identityPool")
    def identity_pool(
        self,
    ) -> _aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPool:
        return typing.cast(_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPool, jsii.get(self, "identityPool"))

    @builtins.property
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> _aws_cdk_aws_cognito_ceddda9d.UserPool:
        return typing.cast(_aws_cdk_aws_cognito_ceddda9d.UserPool, jsii.get(self, "userPool"))

    @builtins.property
    @jsii.member(jsii_name="userPoolClient")
    def user_pool_client(self) -> _aws_cdk_aws_cognito_ceddda9d.UserPoolClient:
        return typing.cast(_aws_cdk_aws_cognito_ceddda9d.UserPoolClient, jsii.get(self, "userPoolClient"))


@jsii.data_type(
    jsii_type="@aws/pdk.identity.UserIdentityProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_signup": "allowSignup",
        "identity_pool_options": "identityPoolOptions",
        "user_pool": "userPool",
    },
)
class UserIdentityProps:
    def __init__(
        self,
        *,
        allow_signup: typing.Optional[builtins.bool] = None,
        identity_pool_options: typing.Optional[typing.Union[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps, typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool] = None,
    ) -> None:
        '''Properties which configures the Identity Pool.

        :param allow_signup: Allow self sign up. Default: - false
        :param identity_pool_options: Configuration for the Identity Pool.
        :param user_pool: User provided Cognito UserPool. Default: - a userpool with mfa will be created.
        '''
        if isinstance(identity_pool_options, dict):
            identity_pool_options = _aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps(**identity_pool_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222a3b2caa10c1bfa3835077067d8216decf681bd0f8bec700ca69ceace9e3e8)
            check_type(argname="argument allow_signup", value=allow_signup, expected_type=type_hints["allow_signup"])
            check_type(argname="argument identity_pool_options", value=identity_pool_options, expected_type=type_hints["identity_pool_options"])
            check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_signup is not None:
            self._values["allow_signup"] = allow_signup
        if identity_pool_options is not None:
            self._values["identity_pool_options"] = identity_pool_options
        if user_pool is not None:
            self._values["user_pool"] = user_pool

    @builtins.property
    def allow_signup(self) -> typing.Optional[builtins.bool]:
        '''Allow self sign up.

        :default: - false
        '''
        result = self._values.get("allow_signup")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def identity_pool_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps]:
        '''Configuration for the Identity Pool.'''
        result = self._values.get("identity_pool_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps], result)

    @builtins.property
    def user_pool(self) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool]:
        '''User provided Cognito UserPool.

        :default: - a userpool with mfa will be created.
        '''
        result = self._values.get("user_pool")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserIdentityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserPoolWithMfa(
    _aws_cdk_aws_cognito_ceddda9d.UserPool,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.identity.UserPoolWithMfa",
):
    '''Configures a UserPool with MFA across SMS/TOTP using sane defaults.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_recovery: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AccountRecovery] = None,
        advanced_security_mode: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AdvancedSecurityMode] = None,
        auto_verify: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.AutoVerifiedAttrs, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cognito_ceddda9d.ICustomAttribute]] = None,
        custom_sender_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        device_tracking: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.DeviceTracking, typing.Dict[builtins.str, typing.Any]]] = None,
        email: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolEmail] = None,
        enable_sms_role: typing.Optional[builtins.bool] = None,
        keep_original: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.KeepOriginalAttrs, typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_triggers: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserPoolTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
        mfa: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.Mfa] = None,
        mfa_message: typing.Optional[builtins.str] = None,
        mfa_second_factor: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.MfaSecondFactor, typing.Dict[builtins.str, typing.Any]]] = None,
        password_policy: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.PasswordPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        self_sign_up_enabled: typing.Optional[builtins.bool] = None,
        sign_in_aliases: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.SignInAliases, typing.Dict[builtins.str, typing.Any]]] = None,
        sign_in_case_sensitive: typing.Optional[builtins.bool] = None,
        sms_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        sms_role_external_id: typing.Optional[builtins.str] = None,
        sns_region: typing.Optional[builtins.str] = None,
        standard_attributes: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.StandardAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
        user_invitation: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserInvitationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool_name: typing.Optional[builtins.str] = None,
        user_verification: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserVerificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account_recovery: How will a user be able to recover their account? Default: AccountRecovery.PHONE_WITHOUT_MFA_AND_EMAIL
        :param advanced_security_mode: The user pool's Advanced Security Mode. Default: - no value
        :param auto_verify: Attributes which Cognito will look to verify automatically upon user sign up. EMAIL and PHONE are the only available options. Default: - If ``signInAlias`` includes email and/or phone, they will be included in ``autoVerifiedAttributes`` by default. If absent, no attributes will be auto-verified.
        :param custom_attributes: Define a set of custom attributes that can be configured for each user in the user pool. Default: - No custom attributes.
        :param custom_sender_kms_key: This key will be used to encrypt temporary passwords and authorization codes that Amazon Cognito generates. Default: - no key ID configured
        :param deletion_protection: Indicates whether the user pool should have deletion protection enabled. Default: false
        :param device_tracking: Device tracking settings. Default: - see defaults on each property of DeviceTracking.
        :param email: Email settings for a user pool. Default: - cognito will use the default email configuration
        :param enable_sms_role: Setting this would explicitly enable or disable SMS role creation. When left unspecified, CDK will determine based on other properties if a role is needed or not. Default: - CDK will determine based on other properties of the user pool if an SMS role should be created or not.
        :param keep_original: Attributes which Cognito will look to handle changes to the value of your users' email address and phone number attributes. EMAIL and PHONE are the only available options. Default: - Nothing is kept.
        :param lambda_triggers: Lambda functions to use for supported Cognito triggers. Default: - No Lambda triggers.
        :param mfa: Configure whether users of this user pool can or are required use MFA to sign in. Default: Mfa.OFF
        :param mfa_message: The SMS message template sent during MFA verification. Use '{####}' in the template where Cognito should insert the verification code. Default: 'Your authentication code is {####}.'
        :param mfa_second_factor: Configure the MFA types that users can use in this user pool. Ignored if ``mfa`` is set to ``OFF``. Default: - { sms: true, otp: false }, if ``mfa`` is set to ``OPTIONAL`` or ``REQUIRED``. { sms: false, otp: false }, otherwise
        :param password_policy: Password policy for this user pool. Default: - see defaults on each property of PasswordPolicy.
        :param removal_policy: Policy to apply when the user pool is removed from the stack. Default: RemovalPolicy.RETAIN
        :param self_sign_up_enabled: Whether self sign-up should be enabled. To configure self sign-up configuration use the ``userVerification`` property. Default: - false
        :param sign_in_aliases: Methods in which a user registers or signs in to a user pool. Allows either username with aliases OR sign in with email, phone, or both. Read the sections on usernames and aliases to learn more - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html To match with 'Option 1' in the above link, with a verified email, this property should be set to ``{ username: true, email: true }``. To match with 'Option 2' in the above link with both a verified email and phone number, this property should be set to ``{ email: true, phone: true }``. Default: { username: true }
        :param sign_in_case_sensitive: Whether sign-in aliases should be evaluated with case sensitivity. For example, when this option is set to false, users will be able to sign in using either ``MyUsername`` or ``myusername``. Default: true
        :param sms_role: The IAM role that Cognito will assume while sending SMS messages. Default: - a new IAM role is created.
        :param sms_role_external_id: The 'ExternalId' that Cognito service must be using when assuming the ``smsRole``, if the role is restricted with an 'sts:ExternalId' conditional. Learn more about ExternalId here - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html This property will be ignored if ``smsRole`` is not specified. Default: - No external id will be configured.
        :param sns_region: The region to integrate with SNS to send SMS messages. This property will do nothing if SMS configuration is not configured. Default: - The same region as the user pool, with a few exceptions - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html#user-pool-sms-settings-first-time
        :param standard_attributes: The set of attributes that are required for every user in the user pool. Read more on attributes here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html Default: - All standard attributes are optional and mutable.
        :param user_invitation: Configuration around admins signing up users into a user pool. Default: - see defaults in UserInvitationConfig.
        :param user_pool_name: Name of the user pool. Default: - automatically generated name by CloudFormation at deploy time.
        :param user_verification: Configuration around users signing themselves up to the user pool. Enable or disable self sign-up via the ``selfSignUpEnabled`` property. Default: - see defaults in UserVerificationConfig.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa66be073edba83d19edc44f0da937d528deb57625d13c7719a5f653bf5482b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UserPoolWithMfaProps(
            account_recovery=account_recovery,
            advanced_security_mode=advanced_security_mode,
            auto_verify=auto_verify,
            custom_attributes=custom_attributes,
            custom_sender_kms_key=custom_sender_kms_key,
            deletion_protection=deletion_protection,
            device_tracking=device_tracking,
            email=email,
            enable_sms_role=enable_sms_role,
            keep_original=keep_original,
            lambda_triggers=lambda_triggers,
            mfa=mfa,
            mfa_message=mfa_message,
            mfa_second_factor=mfa_second_factor,
            password_policy=password_policy,
            removal_policy=removal_policy,
            self_sign_up_enabled=self_sign_up_enabled,
            sign_in_aliases=sign_in_aliases,
            sign_in_case_sensitive=sign_in_case_sensitive,
            sms_role=sms_role,
            sms_role_external_id=sms_role_external_id,
            sns_region=sns_region,
            standard_attributes=standard_attributes,
            user_invitation=user_invitation,
            user_pool_name=user_pool_name,
            user_verification=user_verification,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws/pdk.identity.UserPoolWithMfaProps",
    jsii_struct_bases=[_aws_cdk_aws_cognito_ceddda9d.UserPoolProps],
    name_mapping={
        "account_recovery": "accountRecovery",
        "advanced_security_mode": "advancedSecurityMode",
        "auto_verify": "autoVerify",
        "custom_attributes": "customAttributes",
        "custom_sender_kms_key": "customSenderKmsKey",
        "deletion_protection": "deletionProtection",
        "device_tracking": "deviceTracking",
        "email": "email",
        "enable_sms_role": "enableSmsRole",
        "keep_original": "keepOriginal",
        "lambda_triggers": "lambdaTriggers",
        "mfa": "mfa",
        "mfa_message": "mfaMessage",
        "mfa_second_factor": "mfaSecondFactor",
        "password_policy": "passwordPolicy",
        "removal_policy": "removalPolicy",
        "self_sign_up_enabled": "selfSignUpEnabled",
        "sign_in_aliases": "signInAliases",
        "sign_in_case_sensitive": "signInCaseSensitive",
        "sms_role": "smsRole",
        "sms_role_external_id": "smsRoleExternalId",
        "sns_region": "snsRegion",
        "standard_attributes": "standardAttributes",
        "user_invitation": "userInvitation",
        "user_pool_name": "userPoolName",
        "user_verification": "userVerification",
    },
)
class UserPoolWithMfaProps(_aws_cdk_aws_cognito_ceddda9d.UserPoolProps):
    def __init__(
        self,
        *,
        account_recovery: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AccountRecovery] = None,
        advanced_security_mode: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AdvancedSecurityMode] = None,
        auto_verify: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.AutoVerifiedAttrs, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cognito_ceddda9d.ICustomAttribute]] = None,
        custom_sender_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        device_tracking: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.DeviceTracking, typing.Dict[builtins.str, typing.Any]]] = None,
        email: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolEmail] = None,
        enable_sms_role: typing.Optional[builtins.bool] = None,
        keep_original: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.KeepOriginalAttrs, typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_triggers: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserPoolTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
        mfa: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.Mfa] = None,
        mfa_message: typing.Optional[builtins.str] = None,
        mfa_second_factor: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.MfaSecondFactor, typing.Dict[builtins.str, typing.Any]]] = None,
        password_policy: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.PasswordPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        self_sign_up_enabled: typing.Optional[builtins.bool] = None,
        sign_in_aliases: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.SignInAliases, typing.Dict[builtins.str, typing.Any]]] = None,
        sign_in_case_sensitive: typing.Optional[builtins.bool] = None,
        sms_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        sms_role_external_id: typing.Optional[builtins.str] = None,
        sns_region: typing.Optional[builtins.str] = None,
        standard_attributes: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.StandardAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
        user_invitation: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserInvitationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool_name: typing.Optional[builtins.str] = None,
        user_verification: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserVerificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''UserPoolWithMfa props.

        :param account_recovery: How will a user be able to recover their account? Default: AccountRecovery.PHONE_WITHOUT_MFA_AND_EMAIL
        :param advanced_security_mode: The user pool's Advanced Security Mode. Default: - no value
        :param auto_verify: Attributes which Cognito will look to verify automatically upon user sign up. EMAIL and PHONE are the only available options. Default: - If ``signInAlias`` includes email and/or phone, they will be included in ``autoVerifiedAttributes`` by default. If absent, no attributes will be auto-verified.
        :param custom_attributes: Define a set of custom attributes that can be configured for each user in the user pool. Default: - No custom attributes.
        :param custom_sender_kms_key: This key will be used to encrypt temporary passwords and authorization codes that Amazon Cognito generates. Default: - no key ID configured
        :param deletion_protection: Indicates whether the user pool should have deletion protection enabled. Default: false
        :param device_tracking: Device tracking settings. Default: - see defaults on each property of DeviceTracking.
        :param email: Email settings for a user pool. Default: - cognito will use the default email configuration
        :param enable_sms_role: Setting this would explicitly enable or disable SMS role creation. When left unspecified, CDK will determine based on other properties if a role is needed or not. Default: - CDK will determine based on other properties of the user pool if an SMS role should be created or not.
        :param keep_original: Attributes which Cognito will look to handle changes to the value of your users' email address and phone number attributes. EMAIL and PHONE are the only available options. Default: - Nothing is kept.
        :param lambda_triggers: Lambda functions to use for supported Cognito triggers. Default: - No Lambda triggers.
        :param mfa: Configure whether users of this user pool can or are required use MFA to sign in. Default: Mfa.OFF
        :param mfa_message: The SMS message template sent during MFA verification. Use '{####}' in the template where Cognito should insert the verification code. Default: 'Your authentication code is {####}.'
        :param mfa_second_factor: Configure the MFA types that users can use in this user pool. Ignored if ``mfa`` is set to ``OFF``. Default: - { sms: true, otp: false }, if ``mfa`` is set to ``OPTIONAL`` or ``REQUIRED``. { sms: false, otp: false }, otherwise
        :param password_policy: Password policy for this user pool. Default: - see defaults on each property of PasswordPolicy.
        :param removal_policy: Policy to apply when the user pool is removed from the stack. Default: RemovalPolicy.RETAIN
        :param self_sign_up_enabled: Whether self sign-up should be enabled. To configure self sign-up configuration use the ``userVerification`` property. Default: - false
        :param sign_in_aliases: Methods in which a user registers or signs in to a user pool. Allows either username with aliases OR sign in with email, phone, or both. Read the sections on usernames and aliases to learn more - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html To match with 'Option 1' in the above link, with a verified email, this property should be set to ``{ username: true, email: true }``. To match with 'Option 2' in the above link with both a verified email and phone number, this property should be set to ``{ email: true, phone: true }``. Default: { username: true }
        :param sign_in_case_sensitive: Whether sign-in aliases should be evaluated with case sensitivity. For example, when this option is set to false, users will be able to sign in using either ``MyUsername`` or ``myusername``. Default: true
        :param sms_role: The IAM role that Cognito will assume while sending SMS messages. Default: - a new IAM role is created.
        :param sms_role_external_id: The 'ExternalId' that Cognito service must be using when assuming the ``smsRole``, if the role is restricted with an 'sts:ExternalId' conditional. Learn more about ExternalId here - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html This property will be ignored if ``smsRole`` is not specified. Default: - No external id will be configured.
        :param sns_region: The region to integrate with SNS to send SMS messages. This property will do nothing if SMS configuration is not configured. Default: - The same region as the user pool, with a few exceptions - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html#user-pool-sms-settings-first-time
        :param standard_attributes: The set of attributes that are required for every user in the user pool. Read more on attributes here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html Default: - All standard attributes are optional and mutable.
        :param user_invitation: Configuration around admins signing up users into a user pool. Default: - see defaults in UserInvitationConfig.
        :param user_pool_name: Name of the user pool. Default: - automatically generated name by CloudFormation at deploy time.
        :param user_verification: Configuration around users signing themselves up to the user pool. Enable or disable self sign-up via the ``selfSignUpEnabled`` property. Default: - see defaults in UserVerificationConfig.
        '''
        if isinstance(auto_verify, dict):
            auto_verify = _aws_cdk_aws_cognito_ceddda9d.AutoVerifiedAttrs(**auto_verify)
        if isinstance(device_tracking, dict):
            device_tracking = _aws_cdk_aws_cognito_ceddda9d.DeviceTracking(**device_tracking)
        if isinstance(keep_original, dict):
            keep_original = _aws_cdk_aws_cognito_ceddda9d.KeepOriginalAttrs(**keep_original)
        if isinstance(lambda_triggers, dict):
            lambda_triggers = _aws_cdk_aws_cognito_ceddda9d.UserPoolTriggers(**lambda_triggers)
        if isinstance(mfa_second_factor, dict):
            mfa_second_factor = _aws_cdk_aws_cognito_ceddda9d.MfaSecondFactor(**mfa_second_factor)
        if isinstance(password_policy, dict):
            password_policy = _aws_cdk_aws_cognito_ceddda9d.PasswordPolicy(**password_policy)
        if isinstance(sign_in_aliases, dict):
            sign_in_aliases = _aws_cdk_aws_cognito_ceddda9d.SignInAliases(**sign_in_aliases)
        if isinstance(standard_attributes, dict):
            standard_attributes = _aws_cdk_aws_cognito_ceddda9d.StandardAttributes(**standard_attributes)
        if isinstance(user_invitation, dict):
            user_invitation = _aws_cdk_aws_cognito_ceddda9d.UserInvitationConfig(**user_invitation)
        if isinstance(user_verification, dict):
            user_verification = _aws_cdk_aws_cognito_ceddda9d.UserVerificationConfig(**user_verification)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e225bd23db65e1b9bdf7a2e58c785a8fc5274a7f7eefd8ff5e9901dab81ff5)
            check_type(argname="argument account_recovery", value=account_recovery, expected_type=type_hints["account_recovery"])
            check_type(argname="argument advanced_security_mode", value=advanced_security_mode, expected_type=type_hints["advanced_security_mode"])
            check_type(argname="argument auto_verify", value=auto_verify, expected_type=type_hints["auto_verify"])
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument custom_sender_kms_key", value=custom_sender_kms_key, expected_type=type_hints["custom_sender_kms_key"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument device_tracking", value=device_tracking, expected_type=type_hints["device_tracking"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument enable_sms_role", value=enable_sms_role, expected_type=type_hints["enable_sms_role"])
            check_type(argname="argument keep_original", value=keep_original, expected_type=type_hints["keep_original"])
            check_type(argname="argument lambda_triggers", value=lambda_triggers, expected_type=type_hints["lambda_triggers"])
            check_type(argname="argument mfa", value=mfa, expected_type=type_hints["mfa"])
            check_type(argname="argument mfa_message", value=mfa_message, expected_type=type_hints["mfa_message"])
            check_type(argname="argument mfa_second_factor", value=mfa_second_factor, expected_type=type_hints["mfa_second_factor"])
            check_type(argname="argument password_policy", value=password_policy, expected_type=type_hints["password_policy"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument self_sign_up_enabled", value=self_sign_up_enabled, expected_type=type_hints["self_sign_up_enabled"])
            check_type(argname="argument sign_in_aliases", value=sign_in_aliases, expected_type=type_hints["sign_in_aliases"])
            check_type(argname="argument sign_in_case_sensitive", value=sign_in_case_sensitive, expected_type=type_hints["sign_in_case_sensitive"])
            check_type(argname="argument sms_role", value=sms_role, expected_type=type_hints["sms_role"])
            check_type(argname="argument sms_role_external_id", value=sms_role_external_id, expected_type=type_hints["sms_role_external_id"])
            check_type(argname="argument sns_region", value=sns_region, expected_type=type_hints["sns_region"])
            check_type(argname="argument standard_attributes", value=standard_attributes, expected_type=type_hints["standard_attributes"])
            check_type(argname="argument user_invitation", value=user_invitation, expected_type=type_hints["user_invitation"])
            check_type(argname="argument user_pool_name", value=user_pool_name, expected_type=type_hints["user_pool_name"])
            check_type(argname="argument user_verification", value=user_verification, expected_type=type_hints["user_verification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_recovery is not None:
            self._values["account_recovery"] = account_recovery
        if advanced_security_mode is not None:
            self._values["advanced_security_mode"] = advanced_security_mode
        if auto_verify is not None:
            self._values["auto_verify"] = auto_verify
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if custom_sender_kms_key is not None:
            self._values["custom_sender_kms_key"] = custom_sender_kms_key
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if device_tracking is not None:
            self._values["device_tracking"] = device_tracking
        if email is not None:
            self._values["email"] = email
        if enable_sms_role is not None:
            self._values["enable_sms_role"] = enable_sms_role
        if keep_original is not None:
            self._values["keep_original"] = keep_original
        if lambda_triggers is not None:
            self._values["lambda_triggers"] = lambda_triggers
        if mfa is not None:
            self._values["mfa"] = mfa
        if mfa_message is not None:
            self._values["mfa_message"] = mfa_message
        if mfa_second_factor is not None:
            self._values["mfa_second_factor"] = mfa_second_factor
        if password_policy is not None:
            self._values["password_policy"] = password_policy
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if self_sign_up_enabled is not None:
            self._values["self_sign_up_enabled"] = self_sign_up_enabled
        if sign_in_aliases is not None:
            self._values["sign_in_aliases"] = sign_in_aliases
        if sign_in_case_sensitive is not None:
            self._values["sign_in_case_sensitive"] = sign_in_case_sensitive
        if sms_role is not None:
            self._values["sms_role"] = sms_role
        if sms_role_external_id is not None:
            self._values["sms_role_external_id"] = sms_role_external_id
        if sns_region is not None:
            self._values["sns_region"] = sns_region
        if standard_attributes is not None:
            self._values["standard_attributes"] = standard_attributes
        if user_invitation is not None:
            self._values["user_invitation"] = user_invitation
        if user_pool_name is not None:
            self._values["user_pool_name"] = user_pool_name
        if user_verification is not None:
            self._values["user_verification"] = user_verification

    @builtins.property
    def account_recovery(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AccountRecovery]:
        '''How will a user be able to recover their account?

        :default: AccountRecovery.PHONE_WITHOUT_MFA_AND_EMAIL
        '''
        result = self._values.get("account_recovery")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AccountRecovery], result)

    @builtins.property
    def advanced_security_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AdvancedSecurityMode]:
        '''The user pool's Advanced Security Mode.

        :default: - no value
        '''
        result = self._values.get("advanced_security_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AdvancedSecurityMode], result)

    @builtins.property
    def auto_verify(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AutoVerifiedAttrs]:
        '''Attributes which Cognito will look to verify automatically upon user sign up.

        EMAIL and PHONE are the only available options.

        :default:

        - If ``signInAlias`` includes email and/or phone, they will be included in ``autoVerifiedAttributes`` by default.
        If absent, no attributes will be auto-verified.
        '''
        result = self._values.get("auto_verify")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AutoVerifiedAttrs], result)

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cognito_ceddda9d.ICustomAttribute]]:
        '''Define a set of custom attributes that can be configured for each user in the user pool.

        :default: - No custom attributes.
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cognito_ceddda9d.ICustomAttribute]], result)

    @builtins.property
    def custom_sender_kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''This key will be used to encrypt temporary passwords and authorization codes that Amazon Cognito generates.

        :default: - no key ID configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-custom-sender-triggers.html
        '''
        result = self._values.get("custom_sender_kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the user pool should have deletion protection enabled.

        :default: false
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def device_tracking(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.DeviceTracking]:
        '''Device tracking settings.

        :default: - see defaults on each property of DeviceTracking.
        '''
        result = self._values.get("device_tracking")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.DeviceTracking], result)

    @builtins.property
    def email(self) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolEmail]:
        '''Email settings for a user pool.

        :default: - cognito will use the default email configuration
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolEmail], result)

    @builtins.property
    def enable_sms_role(self) -> typing.Optional[builtins.bool]:
        '''Setting this would explicitly enable or disable SMS role creation.

        When left unspecified, CDK will determine based on other properties if a role is needed or not.

        :default: - CDK will determine based on other properties of the user pool if an SMS role should be created or not.
        '''
        result = self._values.get("enable_sms_role")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def keep_original(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.KeepOriginalAttrs]:
        '''Attributes which Cognito will look to handle changes to the value of your users' email address and phone number attributes.

        EMAIL and PHONE are the only available options.

        :default: - Nothing is kept.
        '''
        result = self._values.get("keep_original")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.KeepOriginalAttrs], result)

    @builtins.property
    def lambda_triggers(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolTriggers]:
        '''Lambda functions to use for supported Cognito triggers.

        :default: - No Lambda triggers.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
        '''
        result = self._values.get("lambda_triggers")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolTriggers], result)

    @builtins.property
    def mfa(self) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.Mfa]:
        '''Configure whether users of this user pool can or are required use MFA to sign in.

        :default: Mfa.OFF
        '''
        result = self._values.get("mfa")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.Mfa], result)

    @builtins.property
    def mfa_message(self) -> typing.Optional[builtins.str]:
        '''The SMS message template sent during MFA verification.

        Use '{####}' in the template where Cognito should insert the verification code.

        :default: 'Your authentication code is {####}.'
        '''
        result = self._values.get("mfa_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mfa_second_factor(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.MfaSecondFactor]:
        '''Configure the MFA types that users can use in this user pool.

        Ignored if ``mfa`` is set to ``OFF``.

        :default:

        - { sms: true, otp: false }, if ``mfa`` is set to ``OPTIONAL`` or ``REQUIRED``.
        { sms: false, otp: false }, otherwise
        '''
        result = self._values.get("mfa_second_factor")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.MfaSecondFactor], result)

    @builtins.property
    def password_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.PasswordPolicy]:
        '''Password policy for this user pool.

        :default: - see defaults on each property of PasswordPolicy.
        '''
        result = self._values.get("password_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.PasswordPolicy], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Policy to apply when the user pool is removed from the stack.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def self_sign_up_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether self sign-up should be enabled.

        To configure self sign-up configuration use the ``userVerification`` property.

        :default: - false
        '''
        result = self._values.get("self_sign_up_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sign_in_aliases(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.SignInAliases]:
        '''Methods in which a user registers or signs in to a user pool.

        Allows either username with aliases OR sign in with email, phone, or both.

        Read the sections on usernames and aliases to learn more -
        https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html

        To match with 'Option 1' in the above link, with a verified email, this property should be set to
        ``{ username: true, email: true }``. To match with 'Option 2' in the above link with both a verified email and phone
        number, this property should be set to ``{ email: true, phone: true }``.

        :default: { username: true }
        '''
        result = self._values.get("sign_in_aliases")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.SignInAliases], result)

    @builtins.property
    def sign_in_case_sensitive(self) -> typing.Optional[builtins.bool]:
        '''Whether sign-in aliases should be evaluated with case sensitivity.

        For example, when this option is set to false, users will be able to sign in using either ``MyUsername`` or ``myusername``.

        :default: true
        '''
        result = self._values.get("sign_in_case_sensitive")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sms_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The IAM role that Cognito will assume while sending SMS messages.

        :default: - a new IAM role is created.
        '''
        result = self._values.get("sms_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def sms_role_external_id(self) -> typing.Optional[builtins.str]:
        '''The 'ExternalId' that Cognito service must be using when assuming the ``smsRole``, if the role is restricted with an 'sts:ExternalId' conditional.

        Learn more about ExternalId here - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html

        This property will be ignored if ``smsRole`` is not specified.

        :default: - No external id will be configured.
        '''
        result = self._values.get("sms_role_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_region(self) -> typing.Optional[builtins.str]:
        '''The region to integrate with SNS to send SMS messages.

        This property will do nothing if SMS configuration is not configured.

        :default: - The same region as the user pool, with a few exceptions - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html#user-pool-sms-settings-first-time
        '''
        result = self._values.get("sns_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standard_attributes(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.StandardAttributes]:
        '''The set of attributes that are required for every user in the user pool.

        Read more on attributes here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html

        :default: - All standard attributes are optional and mutable.
        '''
        result = self._values.get("standard_attributes")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.StandardAttributes], result)

    @builtins.property
    def user_invitation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserInvitationConfig]:
        '''Configuration around admins signing up users into a user pool.

        :default: - see defaults in UserInvitationConfig.
        '''
        result = self._values.get("user_invitation")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserInvitationConfig], result)

    @builtins.property
    def user_pool_name(self) -> typing.Optional[builtins.str]:
        '''Name of the user pool.

        :default: - automatically generated name by CloudFormation at deploy time.
        '''
        result = self._values.get("user_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_verification(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserVerificationConfig]:
        '''Configuration around users signing themselves up to the user pool.

        Enable or disable self sign-up via the ``selfSignUpEnabled`` property.

        :default: - see defaults in UserVerificationConfig.
        '''
        result = self._values.get("user_verification")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserVerificationConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolWithMfaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "UserIdentity",
    "UserIdentityProps",
    "UserPoolWithMfa",
    "UserPoolWithMfaProps",
]

publication.publish()

def _typecheckingstub__3dda65570bf25bbaff83417268c7c0a7e08163811a20c7a7401e4a59fb1b444b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allow_signup: typing.Optional[builtins.bool] = None,
    identity_pool_options: typing.Optional[typing.Union[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222a3b2caa10c1bfa3835077067d8216decf681bd0f8bec700ca69ceace9e3e8(
    *,
    allow_signup: typing.Optional[builtins.bool] = None,
    identity_pool_options: typing.Optional[typing.Union[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa66be073edba83d19edc44f0da937d528deb57625d13c7719a5f653bf5482b8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_recovery: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AccountRecovery] = None,
    advanced_security_mode: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AdvancedSecurityMode] = None,
    auto_verify: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.AutoVerifiedAttrs, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cognito_ceddda9d.ICustomAttribute]] = None,
    custom_sender_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    device_tracking: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.DeviceTracking, typing.Dict[builtins.str, typing.Any]]] = None,
    email: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolEmail] = None,
    enable_sms_role: typing.Optional[builtins.bool] = None,
    keep_original: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.KeepOriginalAttrs, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_triggers: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserPoolTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
    mfa: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.Mfa] = None,
    mfa_message: typing.Optional[builtins.str] = None,
    mfa_second_factor: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.MfaSecondFactor, typing.Dict[builtins.str, typing.Any]]] = None,
    password_policy: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.PasswordPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    self_sign_up_enabled: typing.Optional[builtins.bool] = None,
    sign_in_aliases: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.SignInAliases, typing.Dict[builtins.str, typing.Any]]] = None,
    sign_in_case_sensitive: typing.Optional[builtins.bool] = None,
    sms_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    sms_role_external_id: typing.Optional[builtins.str] = None,
    sns_region: typing.Optional[builtins.str] = None,
    standard_attributes: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.StandardAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    user_invitation: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserInvitationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool_name: typing.Optional[builtins.str] = None,
    user_verification: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserVerificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e225bd23db65e1b9bdf7a2e58c785a8fc5274a7f7eefd8ff5e9901dab81ff5(
    *,
    account_recovery: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AccountRecovery] = None,
    advanced_security_mode: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.AdvancedSecurityMode] = None,
    auto_verify: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.AutoVerifiedAttrs, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cognito_ceddda9d.ICustomAttribute]] = None,
    custom_sender_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    device_tracking: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.DeviceTracking, typing.Dict[builtins.str, typing.Any]]] = None,
    email: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolEmail] = None,
    enable_sms_role: typing.Optional[builtins.bool] = None,
    keep_original: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.KeepOriginalAttrs, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_triggers: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserPoolTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
    mfa: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.Mfa] = None,
    mfa_message: typing.Optional[builtins.str] = None,
    mfa_second_factor: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.MfaSecondFactor, typing.Dict[builtins.str, typing.Any]]] = None,
    password_policy: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.PasswordPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    self_sign_up_enabled: typing.Optional[builtins.bool] = None,
    sign_in_aliases: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.SignInAliases, typing.Dict[builtins.str, typing.Any]]] = None,
    sign_in_case_sensitive: typing.Optional[builtins.bool] = None,
    sms_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    sms_role_external_id: typing.Optional[builtins.str] = None,
    sns_region: typing.Optional[builtins.str] = None,
    standard_attributes: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.StandardAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    user_invitation: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserInvitationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool_name: typing.Optional[builtins.str] = None,
    user_verification: typing.Optional[typing.Union[_aws_cdk_aws_cognito_ceddda9d.UserVerificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
