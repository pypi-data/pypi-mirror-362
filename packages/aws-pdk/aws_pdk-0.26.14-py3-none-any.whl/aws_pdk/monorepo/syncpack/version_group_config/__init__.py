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
    jsii_type="@aws/pdk.monorepo.Syncpack.VersionGroupConfig.Banned",
    jsii_struct_bases=[_GroupConfig_a50a33b0],
    name_mapping={
        "dependencies": "dependencies",
        "dependency_types": "dependencyTypes",
        "label": "label",
        "packages": "packages",
        "specifier_types": "specifierTypes",
        "is_banned": "isBanned",
    },
)
class Banned(_GroupConfig_a50a33b0):
    def __init__(
        self,
        *,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_banned: builtins.bool,
    ) -> None:
        '''
        :param dependencies: 
        :param dependency_types: 
        :param label: 
        :param packages: 
        :param specifier_types: 
        :param is_banned: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1f53299a7d9f63a6d97ffe2b4ecbaf045f12e19d0647e17d86f64ddf126f2d)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
            check_type(argname="argument is_banned", value=is_banned, expected_type=type_hints["is_banned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_banned": is_banned,
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
    def is_banned(self) -> builtins.bool:
        result = self._values.get("is_banned")
        assert result is not None, "Required property 'is_banned' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Banned(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.VersionGroupConfig.Ignored",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62d3ef917d50d34451f7fb4bf5272e9eab337c618f89c3f473bfb7769f337f5a)
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
    jsii_type="@aws/pdk.monorepo.Syncpack.VersionGroupConfig.Pinned",
    jsii_struct_bases=[_GroupConfig_a50a33b0],
    name_mapping={
        "dependencies": "dependencies",
        "dependency_types": "dependencyTypes",
        "label": "label",
        "packages": "packages",
        "specifier_types": "specifierTypes",
        "pin_version": "pinVersion",
    },
)
class Pinned(_GroupConfig_a50a33b0):
    def __init__(
        self,
        *,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        pin_version: builtins.str,
    ) -> None:
        '''
        :param dependencies: 
        :param dependency_types: 
        :param label: 
        :param packages: 
        :param specifier_types: 
        :param pin_version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ae41e45d9c19db7906a4f71a1efa0677e7b8993280036aa9b8a398ac1842e6)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
            check_type(argname="argument pin_version", value=pin_version, expected_type=type_hints["pin_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pin_version": pin_version,
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
    def pin_version(self) -> builtins.str:
        result = self._values.get("pin_version")
        assert result is not None, "Required property 'pin_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Pinned(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.VersionGroupConfig.SameRange",
    jsii_struct_bases=[_GroupConfig_a50a33b0],
    name_mapping={
        "dependencies": "dependencies",
        "dependency_types": "dependencyTypes",
        "label": "label",
        "packages": "packages",
        "specifier_types": "specifierTypes",
        "policy": "policy",
    },
)
class SameRange(_GroupConfig_a50a33b0):
    def __init__(
        self,
        *,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        policy: builtins.str,
    ) -> None:
        '''
        :param dependencies: 
        :param dependency_types: 
        :param label: 
        :param packages: 
        :param specifier_types: 
        :param policy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9398af03e128e98d2b8ee35307bf7227c5f58a71582d5084203bd40bcaf25c9e)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
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
    def policy(self) -> builtins.str:
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SameRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.VersionGroupConfig.SnappedTo",
    jsii_struct_bases=[_GroupConfig_a50a33b0],
    name_mapping={
        "dependencies": "dependencies",
        "dependency_types": "dependencyTypes",
        "label": "label",
        "packages": "packages",
        "specifier_types": "specifierTypes",
        "snap_to": "snapTo",
    },
)
class SnappedTo(_GroupConfig_a50a33b0):
    def __init__(
        self,
        *,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        snap_to: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param dependencies: 
        :param dependency_types: 
        :param label: 
        :param packages: 
        :param specifier_types: 
        :param snap_to: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5597564c05b3ac31df8c26276c3ced91d04f09ee23a89decbaeaa73b9b38d9d3)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
            check_type(argname="argument snap_to", value=snap_to, expected_type=type_hints["snap_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "snap_to": snap_to,
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
    def snap_to(self) -> typing.List[builtins.str]:
        result = self._values.get("snap_to")
        assert result is not None, "Required property 'snap_to' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnappedTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.VersionGroupConfig.Standard",
    jsii_struct_bases=[_GroupConfig_a50a33b0],
    name_mapping={
        "dependencies": "dependencies",
        "dependency_types": "dependencyTypes",
        "label": "label",
        "packages": "packages",
        "specifier_types": "specifierTypes",
        "prefer_version": "preferVersion",
    },
)
class Standard(_GroupConfig_a50a33b0):
    def __init__(
        self,
        *,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefer_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dependencies: 
        :param dependency_types: 
        :param label: 
        :param packages: 
        :param specifier_types: 
        :param prefer_version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0425c02e8891bab22137f821ac48ffc5d54c5bc2ffc9929b81caeb36f42342)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
            check_type(argname="argument prefer_version", value=prefer_version, expected_type=type_hints["prefer_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if prefer_version is not None:
            self._values["prefer_version"] = prefer_version

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
    def prefer_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("prefer_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Standard(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Banned",
    "Ignored",
    "Pinned",
    "SameRange",
    "SnappedTo",
    "Standard",
]

publication.publish()

def _typecheckingstub__bc1f53299a7d9f63a6d97ffe2b4ecbaf045f12e19d0647e17d86f64ddf126f2d(
    *,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_banned: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d3ef917d50d34451f7fb4bf5272e9eab337c618f89c3f473bfb7769f337f5a(
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

def _typecheckingstub__f4ae41e45d9c19db7906a4f71a1efa0677e7b8993280036aa9b8a398ac1842e6(
    *,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    pin_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9398af03e128e98d2b8ee35307bf7227c5f58a71582d5084203bd40bcaf25c9e(
    *,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5597564c05b3ac31df8c26276c3ced91d04f09ee23a89decbaeaa73b9b38d9d3(
    *,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    snap_to: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0425c02e8891bab22137f821ac48ffc5d54c5bc2ffc9929b81caeb36f42342(
    *,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefer_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
