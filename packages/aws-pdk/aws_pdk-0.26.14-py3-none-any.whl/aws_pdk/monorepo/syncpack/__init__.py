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

from ..._jsii import *

from .custom_type_config import (
    NameAndVersionProps as _NameAndVersionProps_24403af6,
    NamedVersionString as _NamedVersionString_3bf188be,
    UnnamedVersionString as _UnnamedVersionString_b2b8403e,
    VersionsByName as _VersionsByName_1c190b74,
)
from .semver_group_config import (
    Disabled as _Disabled_e47b7b80,
    Ignored as _Ignored_c00736b0,
    WithRange as _WithRange_5c9a8aff,
)
from .version_group_config import (
    Banned as _Banned_d684f005,
    Ignored as _Ignored_7ebad223,
    Pinned as _Pinned_0b9cc84e,
    SameRange as _SameRange_2cff5247,
    SnappedTo as _SnappedTo_3347d5ad,
    Standard as _Standard_f8437087,
)


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.CliConfig",
    jsii_struct_bases=[],
    name_mapping={
        "filter": "filter",
        "indent": "indent",
        "source": "source",
        "specs": "specs",
        "types": "types",
        "config_path": "configPath",
    },
)
class CliConfig:
    def __init__(
        self,
        *,
        filter: builtins.str,
        indent: builtins.str,
        source: typing.Sequence[builtins.str],
        specs: builtins.str,
        types: builtins.str,
        config_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter: 
        :param indent: 
        :param source: 
        :param specs: 
        :param types: 
        :param config_path: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c95dfa5cb9060b85d0ddf6297893e1bc2c5b48787cf239c9d2b9bd81046c919)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument indent", value=indent, expected_type=type_hints["indent"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument specs", value=specs, expected_type=type_hints["specs"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            check_type(argname="argument config_path", value=config_path, expected_type=type_hints["config_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
            "indent": indent,
            "source": source,
            "specs": specs,
            "types": types,
        }
        if config_path is not None:
            self._values["config_path"] = config_path

    @builtins.property
    def filter(self) -> builtins.str:
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def indent(self) -> builtins.str:
        result = self._values.get("indent")
        assert result is not None, "Required property 'indent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> typing.List[builtins.str]:
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def specs(self) -> builtins.str:
        result = self._values.get("specs")
        assert result is not None, "Required property 'specs' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def types(self) -> builtins.str:
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("config_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CliConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Syncpack.SyncpackConfig",
    jsii_struct_bases=[],
    name_mapping={
        "custom_types": "customTypes",
        "dependency_types": "dependencyTypes",
        "filter": "filter",
        "format_bugs": "formatBugs",
        "format_repository": "formatRepository",
        "indent": "indent",
        "lint_formatting": "lintFormatting",
        "lint_semver_ranges": "lintSemverRanges",
        "lint_versions": "lintVersions",
        "semver_groups": "semverGroups",
        "sort_az": "sortAz",
        "sort_exports": "sortExports",
        "sort_first": "sortFirst",
        "sort_packages": "sortPackages",
        "source": "source",
        "specifier_types": "specifierTypes",
        "version_groups": "versionGroups",
    },
)
class SyncpackConfig:
    def __init__(
        self,
        *,
        custom_types: typing.Optional[typing.Mapping[builtins.str, typing.Union[typing.Union[_NameAndVersionProps_24403af6, typing.Dict[builtins.str, typing.Any]], typing.Union[_NamedVersionString_3bf188be, typing.Dict[builtins.str, typing.Any]], typing.Union[_UnnamedVersionString_b2b8403e, typing.Dict[builtins.str, typing.Any]], typing.Union[_VersionsByName_1c190b74, typing.Dict[builtins.str, typing.Any]]]]] = None,
        dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        filter: typing.Optional[builtins.str] = None,
        format_bugs: typing.Optional[builtins.bool] = None,
        format_repository: typing.Optional[builtins.bool] = None,
        indent: typing.Optional[builtins.str] = None,
        lint_formatting: typing.Optional[builtins.bool] = None,
        lint_semver_ranges: typing.Optional[builtins.bool] = None,
        lint_versions: typing.Optional[builtins.bool] = None,
        semver_groups: typing.Optional[typing.Sequence[typing.Union[typing.Union[_Disabled_e47b7b80, typing.Dict[builtins.str, typing.Any]], typing.Union[_Ignored_c00736b0, typing.Dict[builtins.str, typing.Any]], typing.Union[_WithRange_5c9a8aff, typing.Dict[builtins.str, typing.Any]]]]] = None,
        sort_az: typing.Optional[typing.Sequence[builtins.str]] = None,
        sort_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        sort_first: typing.Optional[typing.Sequence[builtins.str]] = None,
        sort_packages: typing.Optional[builtins.bool] = None,
        source: typing.Optional[typing.Sequence[builtins.str]] = None,
        specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        version_groups: typing.Optional[typing.Sequence[typing.Union[typing.Union[_Banned_d684f005, typing.Dict[builtins.str, typing.Any]], typing.Union[_Ignored_7ebad223, typing.Dict[builtins.str, typing.Any]], typing.Union[_Pinned_0b9cc84e, typing.Dict[builtins.str, typing.Any]], typing.Union[_SnappedTo_3347d5ad, typing.Dict[builtins.str, typing.Any]], typing.Union[_SameRange_2cff5247, typing.Dict[builtins.str, typing.Any]], typing.Union[_Standard_f8437087, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Configuration for Syncpack.

        :param custom_types: 
        :param dependency_types: 
        :param filter: 
        :param format_bugs: 
        :param format_repository: 
        :param indent: 
        :param lint_formatting: 
        :param lint_semver_ranges: 
        :param lint_versions: 
        :param semver_groups: 
        :param sort_az: 
        :param sort_exports: 
        :param sort_first: 
        :param sort_packages: 
        :param source: 
        :param specifier_types: 
        :param version_groups: 

        :see: https://jamiemason.github.io/syncpack
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f876284f102219bc3c8a77a28983d485f44704e2cbc7da1c21b97df1541724c7)
            check_type(argname="argument custom_types", value=custom_types, expected_type=type_hints["custom_types"])
            check_type(argname="argument dependency_types", value=dependency_types, expected_type=type_hints["dependency_types"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument format_bugs", value=format_bugs, expected_type=type_hints["format_bugs"])
            check_type(argname="argument format_repository", value=format_repository, expected_type=type_hints["format_repository"])
            check_type(argname="argument indent", value=indent, expected_type=type_hints["indent"])
            check_type(argname="argument lint_formatting", value=lint_formatting, expected_type=type_hints["lint_formatting"])
            check_type(argname="argument lint_semver_ranges", value=lint_semver_ranges, expected_type=type_hints["lint_semver_ranges"])
            check_type(argname="argument lint_versions", value=lint_versions, expected_type=type_hints["lint_versions"])
            check_type(argname="argument semver_groups", value=semver_groups, expected_type=type_hints["semver_groups"])
            check_type(argname="argument sort_az", value=sort_az, expected_type=type_hints["sort_az"])
            check_type(argname="argument sort_exports", value=sort_exports, expected_type=type_hints["sort_exports"])
            check_type(argname="argument sort_first", value=sort_first, expected_type=type_hints["sort_first"])
            check_type(argname="argument sort_packages", value=sort_packages, expected_type=type_hints["sort_packages"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument specifier_types", value=specifier_types, expected_type=type_hints["specifier_types"])
            check_type(argname="argument version_groups", value=version_groups, expected_type=type_hints["version_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_types is not None:
            self._values["custom_types"] = custom_types
        if dependency_types is not None:
            self._values["dependency_types"] = dependency_types
        if filter is not None:
            self._values["filter"] = filter
        if format_bugs is not None:
            self._values["format_bugs"] = format_bugs
        if format_repository is not None:
            self._values["format_repository"] = format_repository
        if indent is not None:
            self._values["indent"] = indent
        if lint_formatting is not None:
            self._values["lint_formatting"] = lint_formatting
        if lint_semver_ranges is not None:
            self._values["lint_semver_ranges"] = lint_semver_ranges
        if lint_versions is not None:
            self._values["lint_versions"] = lint_versions
        if semver_groups is not None:
            self._values["semver_groups"] = semver_groups
        if sort_az is not None:
            self._values["sort_az"] = sort_az
        if sort_exports is not None:
            self._values["sort_exports"] = sort_exports
        if sort_first is not None:
            self._values["sort_first"] = sort_first
        if sort_packages is not None:
            self._values["sort_packages"] = sort_packages
        if source is not None:
            self._values["source"] = source
        if specifier_types is not None:
            self._values["specifier_types"] = specifier_types
        if version_groups is not None:
            self._values["version_groups"] = version_groups

    @builtins.property
    def custom_types(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[_NameAndVersionProps_24403af6, _NamedVersionString_3bf188be, _UnnamedVersionString_b2b8403e, _VersionsByName_1c190b74]]]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/custom-types
        '''
        result = self._values.get("custom_types")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[_NameAndVersionProps_24403af6, _NamedVersionString_3bf188be, _UnnamedVersionString_b2b8403e, _VersionsByName_1c190b74]]], result)

    @builtins.property
    def dependency_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/dependency-types
        '''
        result = self._values.get("dependency_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/filter
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format_bugs(self) -> typing.Optional[builtins.bool]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/format-bugs
        '''
        result = self._values.get("format_bugs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def format_repository(self) -> typing.Optional[builtins.bool]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/format-repository
        '''
        result = self._values.get("format_repository")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent(self) -> typing.Optional[builtins.str]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/indent
        '''
        result = self._values.get("indent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lint_formatting(self) -> typing.Optional[builtins.bool]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/lint-formatting
        '''
        result = self._values.get("lint_formatting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lint_semver_ranges(self) -> typing.Optional[builtins.bool]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/lint-semver-ranges
        '''
        result = self._values.get("lint_semver_ranges")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lint_versions(self) -> typing.Optional[builtins.bool]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/lint-versions
        '''
        result = self._values.get("lint_versions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def semver_groups(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_Disabled_e47b7b80, _Ignored_c00736b0, _WithRange_5c9a8aff]]]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/semver-groups
        '''
        result = self._values.get("semver_groups")
        return typing.cast(typing.Optional[typing.List[typing.Union[_Disabled_e47b7b80, _Ignored_c00736b0, _WithRange_5c9a8aff]]], result)

    @builtins.property
    def sort_az(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/sort-az
        '''
        result = self._values.get("sort_az")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sort_exports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/sort-exports
        '''
        result = self._values.get("sort_exports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sort_first(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/sort-first
        '''
        result = self._values.get("sort_first")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sort_packages(self) -> typing.Optional[builtins.bool]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/sort-packages
        '''
        result = self._values.get("sort_packages")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def specifier_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/specifier-types
        '''
        result = self._values.get("specifier_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def version_groups(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_Banned_d684f005, _Ignored_7ebad223, _Pinned_0b9cc84e, _SnappedTo_3347d5ad, _SameRange_2cff5247, _Standard_f8437087]]]:
        '''
        :see: https://jamiemason.github.io/syncpack/config/version-groups
        '''
        result = self._values.get("version_groups")
        return typing.cast(typing.Optional[typing.List[typing.Union[_Banned_d684f005, _Ignored_7ebad223, _Pinned_0b9cc84e, _SnappedTo_3347d5ad, _SameRange_2cff5247, _Standard_f8437087]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyncpackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CliConfig",
    "SyncpackConfig",
    "base_group_config",
    "custom_type_config",
    "semver_group_config",
    "version_group_config",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import base_group_config
from . import custom_type_config
from . import semver_group_config
from . import version_group_config

def _typecheckingstub__6c95dfa5cb9060b85d0ddf6297893e1bc2c5b48787cf239c9d2b9bd81046c919(
    *,
    filter: builtins.str,
    indent: builtins.str,
    source: typing.Sequence[builtins.str],
    specs: builtins.str,
    types: builtins.str,
    config_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f876284f102219bc3c8a77a28983d485f44704e2cbc7da1c21b97df1541724c7(
    *,
    custom_types: typing.Optional[typing.Mapping[builtins.str, typing.Union[typing.Union[_NameAndVersionProps_24403af6, typing.Dict[builtins.str, typing.Any]], typing.Union[_NamedVersionString_3bf188be, typing.Dict[builtins.str, typing.Any]], typing.Union[_UnnamedVersionString_b2b8403e, typing.Dict[builtins.str, typing.Any]], typing.Union[_VersionsByName_1c190b74, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dependency_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    filter: typing.Optional[builtins.str] = None,
    format_bugs: typing.Optional[builtins.bool] = None,
    format_repository: typing.Optional[builtins.bool] = None,
    indent: typing.Optional[builtins.str] = None,
    lint_formatting: typing.Optional[builtins.bool] = None,
    lint_semver_ranges: typing.Optional[builtins.bool] = None,
    lint_versions: typing.Optional[builtins.bool] = None,
    semver_groups: typing.Optional[typing.Sequence[typing.Union[typing.Union[_Disabled_e47b7b80, typing.Dict[builtins.str, typing.Any]], typing.Union[_Ignored_c00736b0, typing.Dict[builtins.str, typing.Any]], typing.Union[_WithRange_5c9a8aff, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sort_az: typing.Optional[typing.Sequence[builtins.str]] = None,
    sort_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    sort_first: typing.Optional[typing.Sequence[builtins.str]] = None,
    sort_packages: typing.Optional[builtins.bool] = None,
    source: typing.Optional[typing.Sequence[builtins.str]] = None,
    specifier_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_groups: typing.Optional[typing.Sequence[typing.Union[typing.Union[_Banned_d684f005, typing.Dict[builtins.str, typing.Any]], typing.Union[_Ignored_7ebad223, typing.Dict[builtins.str, typing.Any]], typing.Union[_Pinned_0b9cc84e, typing.Dict[builtins.str, typing.Any]], typing.Union[_SnappedTo_3347d5ad, typing.Dict[builtins.str, typing.Any]], typing.Union[_SameRange_2cff5247, typing.Dict[builtins.str, typing.Any]], typing.Union[_Standard_f8437087, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
