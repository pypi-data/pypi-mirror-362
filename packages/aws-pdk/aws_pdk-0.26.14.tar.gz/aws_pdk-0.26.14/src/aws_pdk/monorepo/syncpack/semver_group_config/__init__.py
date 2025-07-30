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

from ...._jsii import *

from ..base_group_config import GroupConfig as _GroupConfig_a50a33b0


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.SemverGroupConfig.Disabled",
    jsii_struct_bases=[_GroupConfig_a50a33b0],
    name_mapping={
        "dependencies": "dependencies",
        "dependency_types": "dependencyTypes",
        "label": "label",
        "packages": "packages",
        "specifier_types": "specifierTypes",
        "is_disabled": "isDisabled",
    },
)
class Disabled(_GroupConfig_a50a33b0):
    def __init__(
        self,
        *,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_disabled: builtins.bool,
    ) -> None:
        '''
        :param dependencies: 
        :param dependency_types: 
        :param label: 
        :param packages: 
        :param specifier_types: 
        :param is_disabled: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4076dc19ccd57900e76d02db17bd4ea1b1791168bd4ff66289cffb60259dc01)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
            check_type(argname="argument is_disabled", value=is_disabled, expected_type=type_hints["is_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_disabled": is_disabled,
        }
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if dependency_types is not None:
            self._values["dependency_types"] = dependency_types
        if label is not None:
            self._values["label"] = label
        if packages is not None:
            self._values["packages"] = packages
        if specifier_types is not None:
            self._values["specifier_types"] = specifier_types

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dependency_types(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("dependency_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def specifier_types(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("specifier_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def is_disabled(self) -> builtins.bool:
        result = self._values.get("is_disabled")
        assert result is not None, "Required property 'is_disabled' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Disabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.SemverGroupConfig.Ignored",
    jsii_struct_bases=[_GroupConfig_a50a33b0],
    name_mapping={
        "dependencies": "dependencies",
        "dependency_types": "dependencyTypes",
        "label": "label",
        "packages": "packages",
        "specifier_types": "specifierTypes",
        "is_ignored": "isIgnored",
    },
)
class Ignored(_GroupConfig_a50a33b0):
    def __init__(
        self,
        *,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_ignored: builtins.bool,
    ) -> None:
        '''
        :param dependencies: 
        :param dependency_types: 
        :param label: 
        :param packages: 
        :param specifier_types: 
        :param is_ignored: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71eb511f36586f54284df7d4904595392eb839ec81bb6841353660f9f9a5f580)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
            check_type(argname="argument is_ignored", value=is_ignored, expected_type=type_hints["is_ignored"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_ignored": is_ignored,
        }
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if dependency_types is not None:
            self._values["dependency_types"] = dependency_types
        if label is not None:
            self._values["label"] = label
        if packages is not None:
            self._values["packages"] = packages
        if specifier_types is not None:
            self._values["specifier_types"] = specifier_types

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dependency_types(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("dependency_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def specifier_types(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("specifier_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def is_ignored(self) -> builtins.bool:
        result = self._values.get("is_ignored")
        assert result is not None, "Required property 'is_ignored' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ignored(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.SemverGroupConfig.WithRange",
    jsii_struct_bases=[_GroupConfig_a50a33b0],
    name_mapping={
        "dependencies": "dependencies",
        "dependency_types": "dependencyTypes",
        "label": "label",
        "packages": "packages",
        "specifier_types": "specifierTypes",
        "range": "range",
    },
)
class WithRange(_GroupConfig_a50a33b0):
    def __init__(
        self,
        *,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        range: builtins.str,
    ) -> None:
        '''
        :param dependencies: 
        :param dependency_types: 
        :param label: 
        :param packages: 
        :param specifier_types: 
        :param range: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d1e5d8596d56d8a0342d7c12dfc46ee9f0d7f843a3c2f9f71794141b076d4d)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range": range,
        }
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if dependency_types is not None:
            self._values["dependency_types"] = dependency_types
        if label is not None:
            self._values["label"] = label
        if packages is not None:
            self._values["packages"] = packages
        if specifier_types is not None:
            self._values["specifier_types"] = specifier_types

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dependency_types(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("dependency_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def specifier_types(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("specifier_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def range(self) -> builtins.str:
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WithRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Disabled",
    "Ignored",
    "WithRange",
]

publication.publish()

def _typecheckingstub__b4076dc19ccd57900e76d02db17bd4ea1b1791168bd4ff66289cffb60259dc01(
    *,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_disabled: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71eb511f36586f54284df7d4904595392eb839ec81bb6841353660f9f9a5f580(
    *,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_ignored: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d1e5d8596d56d8a0342d7c12dfc46ee9f0d7f843a3c2f9f71794141b076d4d(
    *,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    range: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
