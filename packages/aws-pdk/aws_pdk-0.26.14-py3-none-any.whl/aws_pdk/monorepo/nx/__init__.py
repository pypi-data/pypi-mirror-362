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


@jsii.interface(jsii_type="@aws/pdk.monorepo.Nx.IInput")
class IInput(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[builtins.str]:
        ...

    @env.setter
    def env(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fileset")
    def fileset(self) -> typing.Optional[builtins.str]:
        ...

    @fileset.setter
    def fileset(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> typing.Optional[builtins.str]:
        ...

    @runtime.setter
    def runtime(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IInputProxy:
    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.monorepo.Nx.IInput"

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef17181cbd03403bf29ebca68eff5a8a35f4d949c96cc3fb46f3ea0a800907a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileset")
    def fileset(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileset"))

    @fileset.setter
    def fileset(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e40bf4664a9b85473f0cd5ddda585050d4d896dce836a6e5a3bdb3a69d50982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf7ed09213cbf9149b9c6bec9ae709ceed4fe24cc96793660a5facb6d0dfa3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInput).__jsii_proxy_class__ = lambda : _IInputProxy


@jsii.interface(jsii_type="@aws/pdk.monorepo.Nx.INxAffectedConfig")
class INxAffectedConfig(typing_extensions.Protocol):
    '''Default options for ``nx affected``.

    :see: https://github.com/nrwl/nx/blob/065477610605d5799babc3ba78f26cdfe8737250/packages/nx/src/config/nx-json.ts#L16
    '''

    @builtins.property
    @jsii.member(jsii_name="defaultBase")
    def default_base(self) -> typing.Optional[builtins.str]:
        '''Default based branch used by affected commands.'''
        ...

    @default_base.setter
    def default_base(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _INxAffectedConfigProxy:
    '''Default options for ``nx affected``.

    :see: https://github.com/nrwl/nx/blob/065477610605d5799babc3ba78f26cdfe8737250/packages/nx/src/config/nx-json.ts#L16
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.monorepo.Nx.INxAffectedConfig"

    @builtins.property
    @jsii.member(jsii_name="defaultBase")
    def default_base(self) -> typing.Optional[builtins.str]:
        '''Default based branch used by affected commands.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBase"))

    @default_base.setter
    def default_base(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de46fc8267401d9897d460c760bbe14b8b04ecd82004f1b6692619e9c2f93aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBase", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INxAffectedConfig).__jsii_proxy_class__ = lambda : _INxAffectedConfigProxy


@jsii.interface(jsii_type="@aws/pdk.monorepo.Nx.IProjectTarget")
class IProjectTarget(typing_extensions.Protocol):
    '''Project Target.'''

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[typing.Union[builtins.str, "ITargetDependency"]]]:
        '''List of Target Dependencies.'''
        ...

    @depends_on.setter
    def depends_on(
        self,
        value: typing.Optional[typing.List[typing.Union[builtins.str, "ITargetDependency"]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="executor")
    def executor(self) -> typing.Optional[builtins.str]:
        '''The function that Nx will invoke when you run this target.'''
        ...

    @executor.setter
    def executor(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(
        self,
    ) -> typing.Optional[typing.List[typing.Union[builtins.str, IInput]]]:
        '''List of inputs to hash for cache key, relative to the root of the monorepo.

        note: must start with leading /
        '''
        ...

    @inputs.setter
    def inputs(
        self,
        value: typing.Optional[typing.List[typing.Union[builtins.str, IInput]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Any:
        '''Contains whatever configuration properties the executor needs to run.'''
        ...

    @options.setter
    def options(self, value: typing.Any) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of outputs to cache, relative to the root of the monorepo.

        note: must start with leading /
        '''
        ...

    @outputs.setter
    def outputs(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...


class _IProjectTargetProxy:
    '''Project Target.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.monorepo.Nx.IProjectTarget"

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[typing.Union[builtins.str, "ITargetDependency"]]]:
        '''List of Target Dependencies.'''
        return typing.cast(typing.Optional[typing.List[typing.Union[builtins.str, "ITargetDependency"]]], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(
        self,
        value: typing.Optional[typing.List[typing.Union[builtins.str, "ITargetDependency"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bfe01eb9bba696fa0b998df6adfa073377b715413e574acdc20a445a74a157e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executor")
    def executor(self) -> typing.Optional[builtins.str]:
        '''The function that Nx will invoke when you run this target.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executor"))

    @executor.setter
    def executor(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc4539bf826901805777870720a4a4146f122a25e508dfddba2dd794183238b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(
        self,
    ) -> typing.Optional[typing.List[typing.Union[builtins.str, IInput]]]:
        '''List of inputs to hash for cache key, relative to the root of the monorepo.

        note: must start with leading /
        '''
        return typing.cast(typing.Optional[typing.List[typing.Union[builtins.str, IInput]]], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(
        self,
        value: typing.Optional[typing.List[typing.Union[builtins.str, IInput]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4cefac6efec82189278bbac22bc1a2a3940859701ac557425d807f26abacd32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Any:
        '''Contains whatever configuration properties the executor needs to run.'''
        return typing.cast(typing.Any, jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13f5eef9b35e94985234176670293b661d35e10803d59e5adb76ed143dd2084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of outputs to cache, relative to the root of the monorepo.

        note: must start with leading /
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outputs"))

    @outputs.setter
    def outputs(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6827bcd95ea658da76b5b2a114f94af095141e1cb32ee5afd83da4e2eb5611e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputs", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IProjectTarget).__jsii_proxy_class__ = lambda : _IProjectTargetProxy


@jsii.interface(jsii_type="@aws/pdk.monorepo.Nx.ITargetDependency")
class ITargetDependency(typing_extensions.Protocol):
    '''Represents an NX Target Dependency.'''

    @builtins.property
    @jsii.member(jsii_name="projects")
    def projects(self) -> "TargetDependencyProject":
        '''Target dependencies.'''
        ...

    @projects.setter
    def projects(self, value: "TargetDependencyProject") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        '''Projen target i.e: build, test, etc.'''
        ...

    @target.setter
    def target(self, value: builtins.str) -> None:
        ...


class _ITargetDependencyProxy:
    '''Represents an NX Target Dependency.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.monorepo.Nx.ITargetDependency"

    @builtins.property
    @jsii.member(jsii_name="projects")
    def projects(self) -> "TargetDependencyProject":
        '''Target dependencies.'''
        return typing.cast("TargetDependencyProject", jsii.get(self, "projects"))

    @projects.setter
    def projects(self, value: "TargetDependencyProject") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7202bcdf061c1b6995a66da3233b860f29bbae230a28871132e2ed4323c7a435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        '''Projen target i.e: build, test, etc.'''
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5ffe7aa483411b0d1926a1612516a83317c4d8aa90b4b2da85a4747d399586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITargetDependency).__jsii_proxy_class__ = lambda : _ITargetDependencyProxy


@jsii.interface(jsii_type="@aws/pdk.monorepo.Nx.IWorkspaceLayout")
class IWorkspaceLayout(typing_extensions.Protocol):
    '''Where new apps + libs should be placed.'''

    @builtins.property
    @jsii.member(jsii_name="appsDir")
    def apps_dir(self) -> builtins.str:
        ...

    @apps_dir.setter
    def apps_dir(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="libsDir")
    def libs_dir(self) -> builtins.str:
        ...

    @libs_dir.setter
    def libs_dir(self, value: builtins.str) -> None:
        ...


class _IWorkspaceLayoutProxy:
    '''Where new apps + libs should be placed.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.monorepo.Nx.IWorkspaceLayout"

    @builtins.property
    @jsii.member(jsii_name="appsDir")
    def apps_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appsDir"))

    @apps_dir.setter
    def apps_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0196b26e8b7979766500e7931dc16e4c303ff6d624692565c7de3fde156c74a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appsDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="libsDir")
    def libs_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "libsDir"))

    @libs_dir.setter
    def libs_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec58a06dd94ddc5179ffb0ec87eda35d59808e5a5fdf4e884031d7d286b3624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "libsDir", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWorkspaceLayout).__jsii_proxy_class__ = lambda : _IWorkspaceLayoutProxy


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Nx.NxJsonConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "affected": "affected",
        "default_project": "defaultProject",
        "extends": "extends",
        "named_inputs": "namedInputs",
        "npm_scope": "npmScope",
        "plugins": "plugins",
        "plugins_config": "pluginsConfig",
        "target_defaults": "targetDefaults",
        "tasks_runner_options": "tasksRunnerOptions",
        "workspace_layout": "workspaceLayout",
    },
)
class NxJsonConfiguration:
    def __init__(
        self,
        *,
        affected: typing.Optional[INxAffectedConfig] = None,
        default_project: typing.Optional[builtins.str] = None,
        extends: typing.Optional[builtins.str] = None,
        named_inputs: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        npm_scope: typing.Optional[builtins.str] = None,
        plugins: typing.Optional[typing.Sequence[builtins.str]] = None,
        plugins_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        target_defaults: typing.Optional[typing.Mapping[builtins.str, IProjectTarget]] = None,
        tasks_runner_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace_layout: typing.Optional[IWorkspaceLayout] = None,
    ) -> None:
        '''
        :param affected: Default options for ``nx affected``.
        :param default_project: Default project. When project isn't provided, the default project will be used. Convenient for small workspaces with one main application.
        :param extends: Some presets use the extends property to hide some default options in a separate json file. The json file specified in the extends property is located in your node_modules folder. The Nx preset files are specified in the nx package. Default: "nx/presets/npm.json"
        :param named_inputs: Named inputs.
        :param npm_scope: Tells Nx what prefix to use when generating library imports.
        :param plugins: Plugins for extending the project graph.
        :param plugins_config: Configuration for Nx Plugins.
        :param target_defaults: Dependencies between different target names across all projects.
        :param tasks_runner_options: Available Task Runners.
        :param workspace_layout: Where new apps + libs should be placed.

        :see: https://github.com/nrwl/nx/blob/master/packages/nx/src/config/nx-json.ts
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f097bdeca55fa6dd1561bdae3a1073ef8ee2066bc6aac49f304d7a3b3bde6ab5)
            check_type(argname="argument affected", value=affected, expected_type=type_hints["affected"])
            check_type(argname="argument default_project", value=default_project, expected_type=type_hints["default_project"])
            check_type(argname="argument extends", value=extends, expected_type=type_hints["extends"])
            check_type(argname="argument named_inputs", value=named_inputs, expected_type=type_hints["named_inputs"])
            check_type(argname="argument npm_scope", value=npm_scope, expected_type=type_hints["npm_scope"])
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
            check_type(argname="argument plugins_config", value=plugins_config, expected_type=type_hints["plugins_config"])
            check_type(argname="argument target_defaults", value=target_defaults, expected_type=type_hints["target_defaults"])
            check_type(argname="argument tasks_runner_options", value=tasks_runner_options, expected_type=type_hints["tasks_runner_options"])
            check_type(argname="argument workspace_layout", value=workspace_layout, expected_type=type_hints["workspace_layout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if affected is not None:
            self._values["affected"] = affected
        if default_project is not None:
            self._values["default_project"] = default_project
        if extends is not None:
            self._values["extends"] = extends
        if named_inputs is not None:
            self._values["named_inputs"] = named_inputs
        if npm_scope is not None:
            self._values["npm_scope"] = npm_scope
        if plugins is not None:
            self._values["plugins"] = plugins
        if plugins_config is not None:
            self._values["plugins_config"] = plugins_config
        if target_defaults is not None:
            self._values["target_defaults"] = target_defaults
        if tasks_runner_options is not None:
            self._values["tasks_runner_options"] = tasks_runner_options
        if workspace_layout is not None:
            self._values["workspace_layout"] = workspace_layout

    @builtins.property
    def affected(self) -> typing.Optional[INxAffectedConfig]:
        '''Default options for ``nx affected``.'''
        result = self._values.get("affected")
        return typing.cast(typing.Optional[INxAffectedConfig], result)

    @builtins.property
    def default_project(self) -> typing.Optional[builtins.str]:
        '''Default project.

        When project isn't provided, the default project
        will be used. Convenient for small workspaces with one main application.
        '''
        result = self._values.get("default_project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extends(self) -> typing.Optional[builtins.str]:
        '''Some presets use the extends property to hide some default options in a separate json file.

        The json file specified in the extends property is located in your node_modules folder.
        The Nx preset files are specified in the nx package.

        :default: "nx/presets/npm.json"
        '''
        result = self._values.get("extends")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def named_inputs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''Named inputs.

        :see: https://nx.dev/reference/nx-json#inputs-&-namedinputs
        '''
        result = self._values.get("named_inputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def npm_scope(self) -> typing.Optional[builtins.str]:
        '''Tells Nx what prefix to use when generating library imports.'''
        result = self._values.get("npm_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Plugins for extending the project graph.'''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def plugins_config(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Configuration for Nx Plugins.'''
        result = self._values.get("plugins_config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def target_defaults(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, IProjectTarget]]:
        '''Dependencies between different target names across all projects.

        :see: https://nx.dev/reference/nx-json#target-defaults
        '''
        result = self._values.get("target_defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, IProjectTarget]], result)

    @builtins.property
    def tasks_runner_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Available Task Runners.'''
        result = self._values.get("tasks_runner_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace_layout(self) -> typing.Optional[IWorkspaceLayout]:
        '''Where new apps + libs should be placed.'''
        result = self._values.get("workspace_layout")
        return typing.cast(typing.Optional[IWorkspaceLayout], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NxJsonConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Nx.ProjectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "implicit_dependencies": "implicitDependencies",
        "included_scripts": "includedScripts",
        "name": "name",
        "named_inputs": "namedInputs",
        "root": "root",
        "tags": "tags",
        "targets": "targets",
    },
)
class ProjectConfig:
    def __init__(
        self,
        *,
        implicit_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        named_inputs: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        root: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        targets: typing.Optional[typing.Mapping[builtins.str, IProjectTarget]] = None,
    ) -> None:
        '''
        :param implicit_dependencies: Implicit dependencies.
        :param included_scripts: Explicit list of scripts for Nx to include.
        :param name: Name of project.
        :param named_inputs: Named inputs.
        :param root: Project root dir path relative to workspace.
        :param tags: Project tag annotations.
        :param targets: Targets configuration.

        :see: https://github.com/nrwl/nx/blob/master/packages/nx/schemas/project-schema.json
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b894ce11981b2d0873a4df2ce3375e34619b3f450d074887336294e6e37b4290)
            check_type(argname="argument implicit_dependencies", value=implicit_dependencies, expected_type=type_hints["implicit_dependencies"])
            check_type(argname="argument included_scripts", value=included_scripts, expected_type=type_hints["included_scripts"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument named_inputs", value=named_inputs, expected_type=type_hints["named_inputs"])
            check_type(argname="argument root", value=root, expected_type=type_hints["root"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if implicit_dependencies is not None:
            self._values["implicit_dependencies"] = implicit_dependencies
        if included_scripts is not None:
            self._values["included_scripts"] = included_scripts
        if name is not None:
            self._values["name"] = name
        if named_inputs is not None:
            self._values["named_inputs"] = named_inputs
        if root is not None:
            self._values["root"] = root
        if tags is not None:
            self._values["tags"] = tags
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def implicit_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Implicit dependencies.

        :see: https://nx.dev/reference/project-configuration#implicitdependencies
        '''
        result = self._values.get("implicit_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_scripts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Explicit list of scripts for Nx to include.

        :see: https://nx.dev/reference/project-configuration#ignoring-package.json-scripts
        '''
        result = self._values.get("included_scripts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of project.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def named_inputs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''Named inputs.

        :see: https://nx.dev/reference/nx-json#inputs-&-namedinputs
        '''
        result = self._values.get("named_inputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def root(self) -> typing.Optional[builtins.str]:
        '''Project root dir path relative to workspace.'''
        result = self._values.get("root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Project tag annotations.

        :see: https://nx.dev/reference/project-configuration#tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.Mapping[builtins.str, IProjectTarget]]:
        '''Targets configuration.

        :see: https://nx.dev/reference/project-configuration
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, IProjectTarget]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Nx.RunManyOptions",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "configuration": "configuration",
        "exclude": "exclude",
        "ignore_cycles": "ignoreCycles",
        "no_bail": "noBail",
        "output_style": "outputStyle",
        "parallel": "parallel",
        "projects": "projects",
        "runner": "runner",
        "skip_cache": "skipCache",
        "verbose": "verbose",
    },
)
class RunManyOptions:
    def __init__(
        self,
        *,
        target: builtins.str,
        configuration: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[builtins.str] = None,
        ignore_cycles: typing.Optional[builtins.bool] = None,
        no_bail: typing.Optional[builtins.bool] = None,
        output_style: typing.Optional[builtins.str] = None,
        parallel: typing.Optional[jsii.Number] = None,
        projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner: typing.Optional[builtins.str] = None,
        skip_cache: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param target: Task to run for affected projects.
        :param configuration: This is the configuration to use when performing tasks on projects.
        :param exclude: Exclude certain projects from being processed.
        :param ignore_cycles: Ignore cycles in the task graph.
        :param no_bail: Do not stop command execution after the first failed task.
        :param output_style: Defines how Nx emits outputs tasks logs. Default: "stream"
        :param parallel: Max number of parallel processes. Default: 3
        :param projects: Project to run as list project names and/or patterns.
        :param runner: This is the name of the tasks runner configuration in nx.json.
        :param skip_cache: Rerun the tasks even when the results are available in the cache.
        :param verbose: Prints additional information about the commands (e.g. stack traces).

        :see: https://nx.dev/packages/nx/documents/run-many#options
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62900a384691230286bfc4f663bf4ccfb5d65cec1e65be45a63d10169b28b3f6)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument ignore_cycles", value=ignore_cycles, expected_type=type_hints["ignore_cycles"])
            check_type(argname="argument no_bail", value=no_bail, expected_type=type_hints["no_bail"])
            check_type(argname="argument output_style", value=output_style, expected_type=type_hints["output_style"])
            check_type(argname="argument parallel", value=parallel, expected_type=type_hints["parallel"])
            check_type(argname="argument projects", value=projects, expected_type=type_hints["projects"])
            check_type(argname="argument runner", value=runner, expected_type=type_hints["runner"])
            check_type(argname="argument skip_cache", value=skip_cache, expected_type=type_hints["skip_cache"])
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }
        if configuration is not None:
            self._values["configuration"] = configuration
        if exclude is not None:
            self._values["exclude"] = exclude
        if ignore_cycles is not None:
            self._values["ignore_cycles"] = ignore_cycles
        if no_bail is not None:
            self._values["no_bail"] = no_bail
        if output_style is not None:
            self._values["output_style"] = output_style
        if parallel is not None:
            self._values["parallel"] = parallel
        if projects is not None:
            self._values["projects"] = projects
        if runner is not None:
            self._values["runner"] = runner
        if skip_cache is not None:
            self._values["skip_cache"] = skip_cache
        if verbose is not None:
            self._values["verbose"] = verbose

    @builtins.property
    def target(self) -> builtins.str:
        '''Task to run for affected projects.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(self) -> typing.Optional[builtins.str]:
        '''This is the configuration to use when performing tasks on projects.'''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude(self) -> typing.Optional[builtins.str]:
        '''Exclude certain projects from being processed.'''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_cycles(self) -> typing.Optional[builtins.bool]:
        '''Ignore cycles in the task graph.'''
        result = self._values.get("ignore_cycles")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_bail(self) -> typing.Optional[builtins.bool]:
        '''Do not stop command execution after the first failed task.'''
        result = self._values.get("no_bail")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def output_style(self) -> typing.Optional[builtins.str]:
        '''Defines how Nx emits outputs tasks logs.

        :default: "stream"
        '''
        result = self._values.get("output_style")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallel(self) -> typing.Optional[jsii.Number]:
        '''Max number of parallel processes.

        :default: 3
        '''
        result = self._values.get("parallel")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Project to run as list project names and/or patterns.'''
        result = self._values.get("projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runner(self) -> typing.Optional[builtins.str]:
        '''This is the name of the tasks runner configuration in nx.json.'''
        result = self._values.get("runner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_cache(self) -> typing.Optional[builtins.bool]:
        '''Rerun the tasks even when the results are available in the cache.'''
        result = self._values.get("skip_cache")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''Prints additional information about the commands (e.g. stack traces).'''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunManyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws/pdk.monorepo.Nx.TargetDependencyProject")
class TargetDependencyProject(enum.Enum):
    '''Supported enums for a TargetDependency.'''

    SELF = "SELF"
    '''Only rely on the package where the target is called.

    This is usually done for test like targets where you only want to run unit
    tests on the target packages without testing all dependent packages.
    '''
    DEPENDENCIES = "DEPENDENCIES"
    '''Target relies on executing the target against all dependencies first.

    This is usually done for build like targets where you want to build all
    dependant projects first.
    '''


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.Nx.WorkspaceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cacheable_operations": "cacheableOperations",
        "default_build_outputs": "defaultBuildOutputs",
        "non_native_hasher": "nonNativeHasher",
        "nx_cloud_read_only_access_token": "nxCloudReadOnlyAccessToken",
        "nx_ignore": "nxIgnore",
    },
)
class WorkspaceConfig:
    def __init__(
        self,
        *,
        cacheable_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_build_outputs: typing.Optional[typing.Sequence[builtins.str]] = None,
        non_native_hasher: typing.Optional[builtins.bool] = None,
        nx_cloud_read_only_access_token: typing.Optional[builtins.str] = None,
        nx_ignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''NX workspace configurations.

        :param cacheable_operations: Defines the list of targets/operations that are cached by Nx. Default: ["build", "test"]
        :param default_build_outputs: 
        :param non_native_hasher: Use non-native hasher for nx tasks. Sets ``NX_NON_NATIVE_HASHER=true`` environment variable on nx based tasks.
        :param nx_cloud_read_only_access_token: Read only access token if enabling nx cloud.
        :param nx_ignore: List of patterns to include in the .nxignore file.

        :see: https://nx.dev/configuration/packagejson
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9a086d867c701af33e4eb61d60d96ca3ede7c489f9ca40e87770595819539c)
            check_type(argname="argument cacheable_operations", value=cacheable_operations, expected_type=type_hints["cacheable_operations"])
            check_type(argname="argument default_build_outputs", value=default_build_outputs, expected_type=type_hints["default_build_outputs"])
            check_type(argname="argument non_native_hasher", value=non_native_hasher, expected_type=type_hints["non_native_hasher"])
            check_type(argname="argument nx_cloud_read_only_access_token", value=nx_cloud_read_only_access_token, expected_type=type_hints["nx_cloud_read_only_access_token"])
            check_type(argname="argument nx_ignore", value=nx_ignore, expected_type=type_hints["nx_ignore"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cacheable_operations is not None:
            self._values["cacheable_operations"] = cacheable_operations
        if default_build_outputs is not None:
            self._values["default_build_outputs"] = default_build_outputs
        if non_native_hasher is not None:
            self._values["non_native_hasher"] = non_native_hasher
        if nx_cloud_read_only_access_token is not None:
            self._values["nx_cloud_read_only_access_token"] = nx_cloud_read_only_access_token
        if nx_ignore is not None:
            self._values["nx_ignore"] = nx_ignore

    @builtins.property
    def cacheable_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Defines the list of targets/operations that are cached by Nx.

        :default: ["build", "test"]

        :see: https://nx.dev/reference/nx-json#tasks-runner-options
        '''
        result = self._values.get("cacheable_operations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_build_outputs(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("default_build_outputs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def non_native_hasher(self) -> typing.Optional[builtins.bool]:
        '''Use non-native hasher for nx tasks.

        Sets ``NX_NON_NATIVE_HASHER=true`` environment variable on nx based tasks.

        :see: https://github.com/nrwl/nx/pull/15071
        '''
        result = self._values.get("non_native_hasher")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nx_cloud_read_only_access_token(self) -> typing.Optional[builtins.str]:
        '''Read only access token if enabling nx cloud.'''
        result = self._values.get("nx_cloud_read_only_access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nx_ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of patterns to include in the .nxignore file.

        :see: https://nx.dev/configuration/packagejson#nxignore
        '''
        result = self._values.get("nx_ignore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IInput",
    "INxAffectedConfig",
    "IProjectTarget",
    "ITargetDependency",
    "IWorkspaceLayout",
    "NxJsonConfiguration",
    "ProjectConfig",
    "RunManyOptions",
    "TargetDependencyProject",
    "WorkspaceConfig",
]

publication.publish()

def _typecheckingstub__1ef17181cbd03403bf29ebca68eff5a8a35f4d949c96cc3fb46f3ea0a800907a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e40bf4664a9b85473f0cd5ddda585050d4d896dce836a6e5a3bdb3a69d50982(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf7ed09213cbf9149b9c6bec9ae709ceed4fe24cc96793660a5facb6d0dfa3e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de46fc8267401d9897d460c760bbe14b8b04ecd82004f1b6692619e9c2f93aa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bfe01eb9bba696fa0b998df6adfa073377b715413e574acdc20a445a74a157e(
    value: typing.Optional[typing.List[typing.Union[builtins.str, ITargetDependency]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc4539bf826901805777870720a4a4146f122a25e508dfddba2dd794183238b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cefac6efec82189278bbac22bc1a2a3940859701ac557425d807f26abacd32(
    value: typing.Optional[typing.List[typing.Union[builtins.str, IInput]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13f5eef9b35e94985234176670293b661d35e10803d59e5adb76ed143dd2084(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6827bcd95ea658da76b5b2a114f94af095141e1cb32ee5afd83da4e2eb5611e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7202bcdf061c1b6995a66da3233b860f29bbae230a28871132e2ed4323c7a435(
    value: TargetDependencyProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5ffe7aa483411b0d1926a1612516a83317c4d8aa90b4b2da85a4747d399586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0196b26e8b7979766500e7931dc16e4c303ff6d624692565c7de3fde156c74a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec58a06dd94ddc5179ffb0ec87eda35d59808e5a5fdf4e884031d7d286b3624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f097bdeca55fa6dd1561bdae3a1073ef8ee2066bc6aac49f304d7a3b3bde6ab5(
    *,
    affected: typing.Optional[INxAffectedConfig] = None,
    default_project: typing.Optional[builtins.str] = None,
    extends: typing.Optional[builtins.str] = None,
    named_inputs: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    npm_scope: typing.Optional[builtins.str] = None,
    plugins: typing.Optional[typing.Sequence[builtins.str]] = None,
    plugins_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    target_defaults: typing.Optional[typing.Mapping[builtins.str, IProjectTarget]] = None,
    tasks_runner_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workspace_layout: typing.Optional[IWorkspaceLayout] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b894ce11981b2d0873a4df2ce3375e34619b3f450d074887336294e6e37b4290(
    *,
    implicit_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    named_inputs: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    root: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    targets: typing.Optional[typing.Mapping[builtins.str, IProjectTarget]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62900a384691230286bfc4f663bf4ccfb5d65cec1e65be45a63d10169b28b3f6(
    *,
    target: builtins.str,
    configuration: typing.Optional[builtins.str] = None,
    exclude: typing.Optional[builtins.str] = None,
    ignore_cycles: typing.Optional[builtins.bool] = None,
    no_bail: typing.Optional[builtins.bool] = None,
    output_style: typing.Optional[builtins.str] = None,
    parallel: typing.Optional[jsii.Number] = None,
    projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner: typing.Optional[builtins.str] = None,
    skip_cache: typing.Optional[builtins.bool] = None,
    verbose: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9a086d867c701af33e4eb61d60d96ca3ede7c489f9ca40e87770595819539c(
    *,
    cacheable_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_build_outputs: typing.Optional[typing.Sequence[builtins.str]] = None,
    non_native_hasher: typing.Optional[builtins.bool] = None,
    nx_cloud_read_only_access_token: typing.Optional[builtins.str] = None,
    nx_ignore: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
