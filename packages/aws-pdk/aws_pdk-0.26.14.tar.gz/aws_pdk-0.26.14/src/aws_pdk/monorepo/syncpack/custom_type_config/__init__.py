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
    jsii_type="@aws/pdk.monorepo.Syncpack.CustomTypeConfig.NameAndVersionProps",
    jsii_struct_bases=[],
    name_mapping={"name_path": "namePath", "path": "path", "strategy": "strategy"},
)
class NameAndVersionProps:
    def __init__(
        self,
        *,
        name_path: builtins.str,
        path: builtins.str,
        strategy: builtins.str,
    ) -> None:
        '''
        :param name_path: 
        :param path: 
        :param strategy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9cfc507d9098e6ab86d76a4f7c32d6268201383cae15c9ef9064bf75f545dbf)
            check_type(argname="argument name_path", value=name_path, expected_type=type_hints["name_path"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name_path": name_path,
            "path": path,
            "strategy": strategy,
        }

    @builtins.property
    def name_path(self) -> builtins.str:
        result = self._values.get("name_path")
        assert result is not None, "Required property 'name_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def strategy(self) -> builtins.str:
        result = self._values.get("strategy")
        assert result is not None, "Required property 'strategy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NameAndVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.CustomTypeConfig.NamedVersionString",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "strategy": "strategy"},
)
class NamedVersionString:
    def __init__(self, *, path: builtins.str, strategy: builtins.str) -> None:
        '''
        :param path: 
        :param strategy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3449dfa9f2b1f059cfca505c8b3a8fc495406b65f329c6e385f381d712d386)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "strategy": strategy,
        }

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def strategy(self) -> builtins.str:
        result = self._values.get("strategy")
        assert result is not None, "Required property 'strategy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamedVersionString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.CustomTypeConfig.UnnamedVersionString",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "strategy": "strategy"},
)
class UnnamedVersionString:
    def __init__(self, *, path: builtins.str, strategy: builtins.str) -> None:
        '''
        :param path: 
        :param strategy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41612a3ace5666a392b80855d1b8d8a17138670259647990048da6a2987293b)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "strategy": strategy,
        }

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def strategy(self) -> builtins.str:
        result = self._values.get("strategy")
        assert result is not None, "Required property 'strategy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UnnamedVersionString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.CustomTypeConfig.VersionsByName",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "strategy": "strategy"},
)
class VersionsByName:
    def __init__(self, *, path: builtins.str, strategy: builtins.str) -> None:
        '''
        :param path: 
        :param strategy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfeb7945bcdad5f8903ff7a04f1b2ab6c27e7c5b0cdbc13ac69c53489c8b289b)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "strategy": strategy,
        }

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def strategy(self) -> builtins.str:
        result = self._values.get("strategy")
        assert result is not None, "Required property 'strategy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VersionsByName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NameAndVersionProps",
    "NamedVersionString",
    "UnnamedVersionString",
    "VersionsByName",
]

publication.publish()

def _typecheckingstub__c9cfc507d9098e6ab86d76a4f7c32d6268201383cae15c9ef9064bf75f545dbf(
    *,
    name_path: builtins.str,
    path: builtins.str,
    strategy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3449dfa9f2b1f059cfca505c8b3a8fc495406b65f329c6e385f381d712d386(
    *,
    path: builtins.str,
    strategy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41612a3ace5666a392b80855d1b8d8a17138670259647990048da6a2987293b(
    *,
    path: builtins.str,
    strategy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfeb7945bcdad5f8903ff7a04f1b2ab6c27e7c5b0cdbc13ac69c53489c8b289b(
    *,
    path: builtins.str,
    strategy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
