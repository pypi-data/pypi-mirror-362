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


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.BaseGroupConfig.GroupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dependencies": "dependencies",
        "dependency_types": "dependencyTypes",
        "label": "label",
        "packages": "packages",
        "specifier_types": "specifierTypes",
    },
)
class GroupConfig:
    def __init__(
        self,
        *,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dependencies: 
        :param dependency_types: 
        :param label: 
        :param packages: 
        :param specifier_types: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9780f7d5dd351fa9ddc07c612d0244b1f227a1df01b10315a4864187579c3ea8)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GroupConfig",
]

publication.publish()

def _typecheckingstub__9780f7d5dd351fa9ddc07c612d0244b1f227a1df01b10315a4864187579c3ea8(
    *,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
