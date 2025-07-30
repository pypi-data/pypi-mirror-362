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

import projen as _projen_04054675
import projen.github as _projen_github_04054675
import projen.github.workflows as _projen_github_workflows_04054675
import projen.java as _projen_java_04054675
import projen.javascript as _projen_javascript_04054675
import projen.python as _projen_python_04054675
import projen.release as _projen_release_04054675
import projen.typescript as _projen_typescript_04054675
from .nx import (
    IInput as _IInput_534968b7,
    INxAffectedConfig as _INxAffectedConfig_1a5bb1a8,
    IProjectTarget as _IProjectTarget_184fbc33,
    IWorkspaceLayout as _IWorkspaceLayout_a55c7d5d,
    ProjectConfig as _ProjectConfig_68a5168c,
    RunManyOptions as _RunManyOptions_f0e930ea,
)
from .syncpack import SyncpackConfig as _SyncpackConfig_9a7845d7


@jsii.interface(jsii_type="@aws/pdk.monorepo.INxProjectCore")
class INxProjectCore(typing_extensions.Protocol):
    '''Interface that all NXProject implementations should implement.'''

    @builtins.property
    @jsii.member(jsii_name="nx")
    def nx(self) -> "NxWorkspace":
        '''Return the NxWorkspace instance.

        This should be implemented using a getter.
        '''
        ...

    @jsii.member(jsii_name="addImplicitDependency")
    def add_implicit_dependency(
        self,
        dependent: _projen_04054675.Project,
        dependee: typing.Union[builtins.str, _projen_04054675.Project],
    ) -> None:
        '''Create an implicit dependency between two Projects.

        This is typically
        used in polygot repos where a Typescript project wants a build dependency
        on a Python project as an example.

        :param dependent: project you want to have the dependency.
        :param dependee: project you wish to depend on.

        :throws: error if this is called on a dependent which does not have a NXProject component attached.
        '''
        ...

    @jsii.member(jsii_name="addJavaDependency")
    def add_java_dependency(
        self,
        dependent: _projen_java_04054675.JavaProject,
        dependee: _projen_java_04054675.JavaProject,
    ) -> None:
        '''Adds a dependency between two Java Projects in the monorepo.

        :param dependent: project you want to have the dependency.
        :param dependee: project you wish to depend on.
        '''
        ...

    @jsii.member(jsii_name="addNxRunManyTask")
    def add_nx_run_many_task(
        self,
        name: builtins.str,
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
    ) -> _projen_04054675.Task:
        '''Add project task that executes ``npx nx run-many ...`` style command.

        :param name: task name.
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
        '''
        ...

    @jsii.member(jsii_name="addPythonPoetryDependency")
    def add_python_poetry_dependency(
        self,
        dependent: _projen_python_04054675.PythonProject,
        dependee: _projen_python_04054675.PythonProject,
    ) -> None:
        '''Adds a dependency between two Python Projects in the monorepo.

        The dependent must have Poetry enabled.

        :param dependent: project you want to have the dependency (must be a Poetry Python Project).
        :param dependee: project you wish to depend on.

        :throws: error if the dependent does not have Poetry enabled
        '''
        ...

    @jsii.member(jsii_name="composeNxRunManyCommand")
    def compose_nx_run_many_command(
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
    ) -> typing.List[builtins.str]:
        '''Helper to format ``npx nx run-many ...`` style command.

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
        '''
        ...

    @jsii.member(jsii_name="execNxRunManyCommand")
    def exec_nx_run_many_command(
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
    ) -> builtins.str:
        '''Helper to format ``npx nx run-many ...`` style command execution in package manager.

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
        '''
        ...


class _INxProjectCoreProxy:
    '''Interface that all NXProject implementations should implement.'''

    __jsii_type__: typing.ClassVar[str] = "@aws/pdk.monorepo.INxProjectCore"

    @builtins.property
    @jsii.member(jsii_name="nx")
    def nx(self) -> "NxWorkspace":
        '''Return the NxWorkspace instance.

        This should be implemented using a getter.
        '''
        return typing.cast("NxWorkspace", jsii.get(self, "nx"))

    @jsii.member(jsii_name="addImplicitDependency")
    def add_implicit_dependency(
        self,
        dependent: _projen_04054675.Project,
        dependee: typing.Union[builtins.str, _projen_04054675.Project],
    ) -> None:
        '''Create an implicit dependency between two Projects.

        This is typically
        used in polygot repos where a Typescript project wants a build dependency
        on a Python project as an example.

        :param dependent: project you want to have the dependency.
        :param dependee: project you wish to depend on.

        :throws: error if this is called on a dependent which does not have a NXProject component attached.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d17d0395607a531a6a544f5d56974b8bc1c407aa3f529989f0f211bfd9dd0ae)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addImplicitDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addJavaDependency")
    def add_java_dependency(
        self,
        dependent: _projen_java_04054675.JavaProject,
        dependee: _projen_java_04054675.JavaProject,
    ) -> None:
        '''Adds a dependency between two Java Projects in the monorepo.

        :param dependent: project you want to have the dependency.
        :param dependee: project you wish to depend on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__019288be6d00cb0f50fecb03c9899b4be7e0d96cfbe3c6418d968f711f8e5b7e)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addJavaDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addNxRunManyTask")
    def add_nx_run_many_task(
        self,
        name: builtins.str,
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
    ) -> _projen_04054675.Task:
        '''Add project task that executes ``npx nx run-many ...`` style command.

        :param name: task name.
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
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87d10ada82211d80097025dafcee32a3ce09f98f19161788434f127287f92b6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(_projen_04054675.Task, jsii.invoke(self, "addNxRunManyTask", [name, options]))

    @jsii.member(jsii_name="addPythonPoetryDependency")
    def add_python_poetry_dependency(
        self,
        dependent: _projen_python_04054675.PythonProject,
        dependee: _projen_python_04054675.PythonProject,
    ) -> None:
        '''Adds a dependency between two Python Projects in the monorepo.

        The dependent must have Poetry enabled.

        :param dependent: project you want to have the dependency (must be a Poetry Python Project).
        :param dependee: project you wish to depend on.

        :throws: error if the dependent does not have Poetry enabled
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ae302715da724dc812c351b20ae831900e149ba1f9602fdd8e6d794257ea11)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addPythonPoetryDependency", [dependent, dependee]))

    @jsii.member(jsii_name="composeNxRunManyCommand")
    def compose_nx_run_many_command(
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
    ) -> typing.List[builtins.str]:
        '''Helper to format ``npx nx run-many ...`` style command.

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
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "composeNxRunManyCommand", [options]))

    @jsii.member(jsii_name="execNxRunManyCommand")
    def exec_nx_run_many_command(
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
    ) -> builtins.str:
        '''Helper to format ``npx nx run-many ...`` style command execution in package manager.

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
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "execNxRunManyCommand", [options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INxProjectCore).__jsii_proxy_class__ = lambda : _INxProjectCoreProxy


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.JavaProjectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "artifact_id": "artifactId",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "clobber": "clobber",
        "commit_generated": "commitGenerated",
        "compile_options": "compileOptions",
        "deps": "deps",
        "description": "description",
        "dev_container": "devContainer",
        "distdir": "distdir",
        "github": "github",
        "github_options": "githubOptions",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "gitpod": "gitpod",
        "group_id": "groupId",
        "junit": "junit",
        "junit_options": "junitOptions",
        "logging": "logging",
        "mergify": "mergify",
        "mergify_options": "mergifyOptions",
        "outdir": "outdir",
        "packaging": "packaging",
        "packaging_options": "packagingOptions",
        "parent": "parent",
        "parent_pom": "parentPom",
        "project_type": "projectType",
        "projen_command": "projenCommand",
        "projen_credentials": "projenCredentials",
        "projenrc_java": "projenrcJava",
        "projenrc_java_options": "projenrcJavaOptions",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "projen_token_secret": "projenTokenSecret",
        "readme": "readme",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "sample": "sample",
        "sample_java_package": "sampleJavaPackage",
        "stale": "stale",
        "stale_options": "staleOptions",
        "test_deps": "testDeps",
        "url": "url",
        "version": "version",
        "vscode": "vscode",
    },
)
class JavaProjectOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        artifact_id: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        distdir: typing.Optional[builtins.str] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        group_id: typing.Optional[builtins.str] = None,
        junit: typing.Optional[builtins.bool] = None,
        junit_options: typing.Optional[typing.Union[_projen_java_04054675.JunitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        packaging: typing.Optional[builtins.str] = None,
        packaging_options: typing.Optional[typing.Union[_projen_java_04054675.MavenPackagingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        parent_pom: typing.Optional[typing.Union[_projen_java_04054675.ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_projen_04054675.ProjectType] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
        projenrc_java: typing.Optional[builtins.bool] = None,
        projenrc_java_options: typing.Optional[typing.Union[_projen_java_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        sample: typing.Optional[builtins.bool] = None,
        sample_java_package: typing.Optional[builtins.str] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''JavaProjectOptions.

        :param name: Default: $BASEDIR
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param compile_options: (experimental) Compile options. Default: - defaults
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param distdir: (experimental) Final artifact output directory. Default: "dist/java"
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param group_id: (experimental) This is generally unique amongst an organization or a project. For example, all core Maven artifacts do (well, should) live under the groupId org.apache.maven. Group ID's do not necessarily use the dot notation, for example, the junit project. Note that the dot-notated groupId does not have to correspond to the package structure that the project contains. It is, however, a good practice to follow. When stored within a repository, the group acts much like the Java packaging structure does in an operating system. The dots are replaced by OS specific directory separators (such as '/' in Unix) which becomes a relative directory structure from the base repository. In the example given, the org.codehaus.mojo group lives within the directory $M2_REPO/org/codehaus/mojo. Default: "org.acme"
        :param junit: (experimental) Include junit tests. Default: true
        :param junit_options: (experimental) junit options. Default: - defaults
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param packaging: (experimental) Project packaging format. Default: "jar"
        :param packaging_options: (experimental) Packaging options. Default: - defaults
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param parent_pom: (experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos. Default: undefined
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projenrc_java: (experimental) Use projenrc in java. This will install ``projen`` as a java dependency and will add a ``synth`` task which will compile & execute ``main()`` from ``src/main/java/projenrc.java``. Default: true
        :param projenrc_java_options: (experimental) Options related to projenrc in java. Default: - default options
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param sample_java_package: (experimental) The java package to use for the code sample. Default: "org.acme"
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param test_deps: (experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addTestDependency()``. Default: []
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        '''
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _projen_github_04054675.AutoApproveOptions(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _projen_github_04054675.AutoMergeOptions(**auto_merge_options)
        if isinstance(compile_options, dict):
            compile_options = _projen_java_04054675.MavenCompileOptions(**compile_options)
        if isinstance(github_options, dict):
            github_options = _projen_github_04054675.GitHubOptions(**github_options)
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _projen_04054675.IgnoreFileOptions(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _projen_04054675.GitOptions(**git_options)
        if isinstance(junit_options, dict):
            junit_options = _projen_java_04054675.JunitOptions(**junit_options)
        if isinstance(logging, dict):
            logging = _projen_04054675.LoggerOptions(**logging)
        if isinstance(mergify_options, dict):
            mergify_options = _projen_github_04054675.MergifyOptions(**mergify_options)
        if isinstance(packaging_options, dict):
            packaging_options = _projen_java_04054675.MavenPackagingOptions(**packaging_options)
        if isinstance(parent_pom, dict):
            parent_pom = _projen_java_04054675.ParentPom(**parent_pom)
        if isinstance(projenrc_java_options, dict):
            projenrc_java_options = _projen_java_04054675.ProjenrcOptions(**projenrc_java_options)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _projen_04054675.ProjenrcJsonOptions(**projenrc_json_options)
        if isinstance(readme, dict):
            readme = _projen_04054675.SampleReadmeProps(**readme)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _projen_04054675.RenovatebotOptions(**renovatebot_options)
        if isinstance(stale_options, dict):
            stale_options = _projen_github_04054675.StaleOptions(**stale_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beca0972d1a8f14d9fe916150a1fae4839c40298030f85894001f1fb5bdacf4d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument compile_options", value=compile_options, expected_type=type_hints["compile_options"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument distdir", value=distdir, expected_type=type_hints["distdir"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument junit", value=junit, expected_type=type_hints["junit"])
            check_type(argname="argument junit_options", value=junit_options, expected_type=type_hints["junit_options"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument mergify", value=mergify, expected_type=type_hints["mergify"])
            check_type(argname="argument mergify_options", value=mergify_options, expected_type=type_hints["mergify_options"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument packaging_options", value=packaging_options, expected_type=type_hints["packaging_options"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument parent_pom", value=parent_pom, expected_type=type_hints["parent_pom"])
            check_type(argname="argument project_type", value=project_type, expected_type=type_hints["project_type"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument projenrc_java", value=projenrc_java, expected_type=type_hints["projenrc_java"])
            check_type(argname="argument projenrc_java_options", value=projenrc_java_options, expected_type=type_hints["projenrc_java_options"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument projen_token_secret", value=projen_token_secret, expected_type=type_hints["projen_token_secret"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument sample_java_package", value=sample_java_package, expected_type=type_hints["sample_java_package"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument test_deps", value=test_deps, expected_type=type_hints["test_deps"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if artifact_id is not None:
            self._values["artifact_id"] = artifact_id
        if auto_approve_options is not None:
            self._values["auto_approve_options"] = auto_approve_options
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if auto_merge_options is not None:
            self._values["auto_merge_options"] = auto_merge_options
        if clobber is not None:
            self._values["clobber"] = clobber
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if compile_options is not None:
            self._values["compile_options"] = compile_options
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if distdir is not None:
            self._values["distdir"] = distdir
        if github is not None:
            self._values["github"] = github
        if github_options is not None:
            self._values["github_options"] = github_options
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if gitpod is not None:
            self._values["gitpod"] = gitpod
        if group_id is not None:
            self._values["group_id"] = group_id
        if junit is not None:
            self._values["junit"] = junit
        if junit_options is not None:
            self._values["junit_options"] = junit_options
        if logging is not None:
            self._values["logging"] = logging
        if mergify is not None:
            self._values["mergify"] = mergify
        if mergify_options is not None:
            self._values["mergify_options"] = mergify_options
        if outdir is not None:
            self._values["outdir"] = outdir
        if packaging is not None:
            self._values["packaging"] = packaging
        if packaging_options is not None:
            self._values["packaging_options"] = packaging_options
        if parent is not None:
            self._values["parent"] = parent
        if parent_pom is not None:
            self._values["parent_pom"] = parent_pom
        if project_type is not None:
            self._values["project_type"] = project_type
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if projenrc_java is not None:
            self._values["projenrc_java"] = projenrc_java
        if projenrc_java_options is not None:
            self._values["projenrc_java_options"] = projenrc_java_options
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if projen_token_secret is not None:
            self._values["projen_token_secret"] = projen_token_secret
        if readme is not None:
            self._values["readme"] = readme
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if sample is not None:
            self._values["sample"] = sample
        if sample_java_package is not None:
            self._values["sample_java_package"] = sample_java_package
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if test_deps is not None:
            self._values["test_deps"] = test_deps
        if url is not None:
            self._values["url"] = url
        if version is not None:
            self._values["version"] = version
        if vscode is not None:
            self._values["vscode"] = vscode

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :default: $BASEDIR
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifact_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The artifactId is generally the name that the project is known by.

        Although
        the groupId is important, people within the group will rarely mention the
        groupId in discussion (they are often all be the same ID, such as the
        MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId,
        creates a key that separates this project from every other project in the
        world (at least, it should :) ). Along with the groupId, the artifactId
        fully defines the artifact's living quarters within the repository. In the
        case of the above project, my-project lives in
        $M2_REPO/org/codehaus/mojo/my-project.

        :default: "my-app"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_approve_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoApproveOptions]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoApproveOptions], result)

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable automatic merging on GitHub.

        Has no effect if ``github.mergify``
        is set to false.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoMergeOptions]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoMergeOptions], result)

    @builtins.property
    def clobber(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a ``clobber`` task which resets the repo to origin.

        :default: - true, but false for subprojects

        :stability: experimental
        '''
        result = self._values.get("clobber")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def compile_options(
        self,
    ) -> typing.Optional[_projen_java_04054675.MavenCompileOptions]:
        '''(experimental) Compile options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("compile_options")
        return typing.cast(typing.Optional[_projen_java_04054675.MavenCompileOptions], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``.

        Additional dependencies can be added via ``project.addDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of a project is always good.

        Although this should not replace
        formal documentation, a quick comment to any readers of the POM is always
        helpful.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dev_container(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a VSCode development environment (used for GitHub Codespaces).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dev_container")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def distdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Final artifact output directory.

        :default: "dist/java"

        :stability: experimental
        '''
        result = self._values.get("distdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable GitHub integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github_options(self) -> typing.Optional[_projen_github_04054675.GitHubOptions]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional[_projen_github_04054675.GitHubOptions], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_projen_04054675.IgnoreFileOptions]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_projen_04054675.IgnoreFileOptions], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_projen_04054675.GitOptions]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_projen_04054675.GitOptions], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) This is generally unique amongst an organization or a project.

        For example,
        all core Maven artifacts do (well, should) live under the groupId
        org.apache.maven. Group ID's do not necessarily use the dot notation, for
        example, the junit project. Note that the dot-notated groupId does not have
        to correspond to the package structure that the project contains. It is,
        however, a good practice to follow. When stored within a repository, the
        group acts much like the Java packaging structure does in an operating
        system. The dots are replaced by OS specific directory separators (such as
        '/' in Unix) which becomes a relative directory structure from the base
        repository. In the example given, the org.codehaus.mojo group lives within
        the directory $M2_REPO/org/codehaus/mojo.

        :default: "org.acme"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def junit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include junit tests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("junit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def junit_options(self) -> typing.Optional[_projen_java_04054675.JunitOptions]:
        '''(experimental) junit options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("junit_options")
        return typing.cast(typing.Optional[_projen_java_04054675.JunitOptions], result)

    @builtins.property
    def logging(self) -> typing.Optional[_projen_04054675.LoggerOptions]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_projen_04054675.LoggerOptions], result)

    @builtins.property
    def mergify(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether mergify should be enabled on this repository or not.

        :default: true

        :deprecated: use ``githubOptions.mergify`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.MergifyOptions]:
        '''(deprecated) Options for mergify.

        :default: - default options

        :deprecated: use ``githubOptions.mergifyOptions`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify_options")
        return typing.cast(typing.Optional[_projen_github_04054675.MergifyOptions], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project. Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packaging(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project packaging format.

        :default: "jar"

        :stability: experimental
        '''
        result = self._values.get("packaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packaging_options(
        self,
    ) -> typing.Optional[_projen_java_04054675.MavenPackagingOptions]:
        '''(experimental) Packaging options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("packaging_options")
        return typing.cast(typing.Optional[_projen_java_04054675.MavenPackagingOptions], result)

    @builtins.property
    def parent(self) -> typing.Optional[_projen_04054675.Project]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_projen_04054675.Project], result)

    @builtins.property
    def parent_pom(self) -> typing.Optional[_projen_java_04054675.ParentPom]:
        '''(experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("parent_pom")
        return typing.cast(typing.Optional[_projen_java_04054675.ParentPom], result)

    @builtins.property
    def project_type(self) -> typing.Optional[_projen_04054675.ProjectType]:
        '''(deprecated) Which type of project this is (library/app).

        :default: ProjectType.UNKNOWN

        :deprecated: no longer supported at the base project level

        :stability: deprecated
        '''
        result = self._values.get("project_type")
        return typing.cast(typing.Optional[_projen_04054675.ProjectType], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projen_credentials(
        self,
    ) -> typing.Optional[_projen_github_04054675.GithubCredentials]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_projen_github_04054675.GithubCredentials], result)

    @builtins.property
    def projenrc_java(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use projenrc in java.

        This will install ``projen`` as a java dependency and will add a ``synth`` task which
        will compile & execute ``main()`` from ``src/main/java/projenrc.java``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("projenrc_java")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_java_options(
        self,
    ) -> typing.Optional[_projen_java_04054675.ProjenrcOptions]:
        '''(experimental) Options related to projenrc in java.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_java_options")
        return typing.cast(typing.Optional[_projen_java_04054675.ProjenrcOptions], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(
        self,
    ) -> typing.Optional[_projen_04054675.ProjenrcJsonOptions]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_projen_04054675.ProjenrcJsonOptions], result)

    @builtins.property
    def projen_token_secret(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows.

        This token needs to have the ``repo``, ``workflows``
        and ``packages`` scope.

        :default: "PROJEN_GITHUB_TOKEN"

        :deprecated: use ``projenCredentials``

        :stability: deprecated
        '''
        result = self._values.get("projen_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme(self) -> typing.Optional[_projen_04054675.SampleReadmeProps]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[_projen_04054675.SampleReadmeProps], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(
        self,
    ) -> typing.Optional[_projen_04054675.RenovatebotOptions]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_projen_04054675.RenovatebotOptions], result)

    @builtins.property
    def sample(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include sample code and test if the relevant directories don't exist.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sample")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sample_java_package(self) -> typing.Optional[builtins.str]:
        '''(experimental) The java package to use for the code sample.

        :default: "org.acme"

        :stability: experimental
        '''
        result = self._values.get("sample_java_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stale(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Auto-close of stale issues and pull request.

        See ``staleOptions`` for options.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stale")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale_options(self) -> typing.Optional[_projen_github_04054675.StaleOptions]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional[_projen_github_04054675.StaleOptions], result)

    @builtins.property
    def test_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``.

        Additional dependencies can be added via ``project.addTestDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("test_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL, like the name, is not required.

        This is a nice gesture for
        projects users, however, so that they know where the project lives.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) This is the last piece of the naming puzzle.

        groupId:artifactId denotes a
        single project but they cannot delineate which incarnation of that project
        we are talking about. Do we want the junit:junit of 2018 (version 4.12), or
        of 2007 (version 3.8.2)? In short: code changes, those changes should be
        versioned, and this element keeps those versions in line. It is also used
        within an artifact's repository to separate versions from each other.
        my-project version 1.0 files live in the directory structure
        $M2_REPO/org/codehaus/mojo/my-project/1.0.

        :default: "0.1.0"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vscode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable VSCode integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("vscode")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JavaProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.LicenseOptions",
    jsii_struct_bases=[],
    name_mapping={
        "copyright_owner": "copyrightOwner",
        "disable_default_licenses": "disableDefaultLicenses",
        "license_text": "licenseText",
        "spdx": "spdx",
    },
)
class LicenseOptions:
    def __init__(
        self,
        *,
        copyright_owner: typing.Optional[builtins.str] = None,
        disable_default_licenses: typing.Optional[builtins.bool] = None,
        license_text: typing.Optional[builtins.str] = None,
        spdx: typing.Optional[builtins.str] = None,
    ) -> None:
        '''License options.

        :param copyright_owner: Copyright owner. If the license text for the given spdx has $copyright_owner, this option must be specified.
        :param disable_default_licenses: Whether to disable the generation of default licenses. Default: false
        :param license_text: Arbitrary license text.
        :param spdx: License type (SPDX).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__403eb7d3ab3dddebf764ebe76e5c135d2e4370a0158d3a2e1e7e417879222876)
            check_type(argname="argument copyright_owner", value=copyright_owner, expected_type=type_hints["copyright_owner"])
            check_type(argname="argument disable_default_licenses", value=disable_default_licenses, expected_type=type_hints["disable_default_licenses"])
            check_type(argname="argument license_text", value=license_text, expected_type=type_hints["license_text"])
            check_type(argname="argument spdx", value=spdx, expected_type=type_hints["spdx"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if copyright_owner is not None:
            self._values["copyright_owner"] = copyright_owner
        if disable_default_licenses is not None:
            self._values["disable_default_licenses"] = disable_default_licenses
        if license_text is not None:
            self._values["license_text"] = license_text
        if spdx is not None:
            self._values["spdx"] = spdx

    @builtins.property
    def copyright_owner(self) -> typing.Optional[builtins.str]:
        '''Copyright owner.

        If the license text for the given spdx has $copyright_owner, this option must be specified.
        '''
        result = self._values.get("copyright_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_default_licenses(self) -> typing.Optional[builtins.bool]:
        '''Whether to disable the generation of default licenses.

        :default: false
        '''
        result = self._values.get("disable_default_licenses")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def license_text(self) -> typing.Optional[builtins.str]:
        '''Arbitrary license text.'''
        result = self._values.get("license_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spdx(self) -> typing.Optional[builtins.str]:
        '''License type (SPDX).

        :see: https://github.com/projen/projen/tree/main/license-text for list of supported licenses
        '''
        result = self._values.get("spdx")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LicenseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.MonorepoJavaOptions",
    jsii_struct_bases=[JavaProjectOptions],
    name_mapping={
        "name": "name",
        "artifact_id": "artifactId",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "clobber": "clobber",
        "commit_generated": "commitGenerated",
        "compile_options": "compileOptions",
        "deps": "deps",
        "description": "description",
        "dev_container": "devContainer",
        "distdir": "distdir",
        "github": "github",
        "github_options": "githubOptions",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "gitpod": "gitpod",
        "group_id": "groupId",
        "junit": "junit",
        "junit_options": "junitOptions",
        "logging": "logging",
        "mergify": "mergify",
        "mergify_options": "mergifyOptions",
        "outdir": "outdir",
        "packaging": "packaging",
        "packaging_options": "packagingOptions",
        "parent": "parent",
        "parent_pom": "parentPom",
        "project_type": "projectType",
        "projen_command": "projenCommand",
        "projen_credentials": "projenCredentials",
        "projenrc_java": "projenrcJava",
        "projenrc_java_options": "projenrcJavaOptions",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "projen_token_secret": "projenTokenSecret",
        "readme": "readme",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "sample": "sample",
        "sample_java_package": "sampleJavaPackage",
        "stale": "stale",
        "stale_options": "staleOptions",
        "test_deps": "testDeps",
        "url": "url",
        "version": "version",
        "vscode": "vscode",
        "default_release_branch": "defaultReleaseBranch",
        "disable_default_licenses": "disableDefaultLicenses",
    },
)
class MonorepoJavaOptions(JavaProjectOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        artifact_id: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        distdir: typing.Optional[builtins.str] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        group_id: typing.Optional[builtins.str] = None,
        junit: typing.Optional[builtins.bool] = None,
        junit_options: typing.Optional[typing.Union[_projen_java_04054675.JunitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        packaging: typing.Optional[builtins.str] = None,
        packaging_options: typing.Optional[typing.Union[_projen_java_04054675.MavenPackagingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        parent_pom: typing.Optional[typing.Union[_projen_java_04054675.ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_projen_04054675.ProjectType] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
        projenrc_java: typing.Optional[builtins.bool] = None,
        projenrc_java_options: typing.Optional[typing.Union[_projen_java_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        sample: typing.Optional[builtins.bool] = None,
        sample_java_package: typing.Optional[builtins.str] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
        default_release_branch: typing.Optional[builtins.str] = None,
        disable_default_licenses: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Configuration options for the NxMonorepoJavaProject.

        :param name: Default: $BASEDIR
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param compile_options: (experimental) Compile options. Default: - defaults
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param distdir: (experimental) Final artifact output directory. Default: "dist/java"
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param group_id: (experimental) This is generally unique amongst an organization or a project. For example, all core Maven artifacts do (well, should) live under the groupId org.apache.maven. Group ID's do not necessarily use the dot notation, for example, the junit project. Note that the dot-notated groupId does not have to correspond to the package structure that the project contains. It is, however, a good practice to follow. When stored within a repository, the group acts much like the Java packaging structure does in an operating system. The dots are replaced by OS specific directory separators (such as '/' in Unix) which becomes a relative directory structure from the base repository. In the example given, the org.codehaus.mojo group lives within the directory $M2_REPO/org/codehaus/mojo. Default: "org.acme"
        :param junit: (experimental) Include junit tests. Default: true
        :param junit_options: (experimental) junit options. Default: - defaults
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param packaging: (experimental) Project packaging format. Default: "jar"
        :param packaging_options: (experimental) Packaging options. Default: - defaults
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param parent_pom: (experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos. Default: undefined
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projenrc_java: (experimental) Use projenrc in java. This will install ``projen`` as a java dependency and will add a ``synth`` task which will compile & execute ``main()`` from ``src/main/java/projenrc.java``. Default: true
        :param projenrc_java_options: (experimental) Options related to projenrc in java. Default: - default options
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param sample_java_package: (experimental) The java package to use for the code sample. Default: "org.acme"
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param test_deps: (experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addTestDependency()``. Default: []
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param default_release_branch: 
        :param disable_default_licenses: Whether to disable the generation of default licenses. Default: false
        '''
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _projen_github_04054675.AutoApproveOptions(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _projen_github_04054675.AutoMergeOptions(**auto_merge_options)
        if isinstance(compile_options, dict):
            compile_options = _projen_java_04054675.MavenCompileOptions(**compile_options)
        if isinstance(github_options, dict):
            github_options = _projen_github_04054675.GitHubOptions(**github_options)
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _projen_04054675.IgnoreFileOptions(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _projen_04054675.GitOptions(**git_options)
        if isinstance(junit_options, dict):
            junit_options = _projen_java_04054675.JunitOptions(**junit_options)
        if isinstance(logging, dict):
            logging = _projen_04054675.LoggerOptions(**logging)
        if isinstance(mergify_options, dict):
            mergify_options = _projen_github_04054675.MergifyOptions(**mergify_options)
        if isinstance(packaging_options, dict):
            packaging_options = _projen_java_04054675.MavenPackagingOptions(**packaging_options)
        if isinstance(parent_pom, dict):
            parent_pom = _projen_java_04054675.ParentPom(**parent_pom)
        if isinstance(projenrc_java_options, dict):
            projenrc_java_options = _projen_java_04054675.ProjenrcOptions(**projenrc_java_options)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _projen_04054675.ProjenrcJsonOptions(**projenrc_json_options)
        if isinstance(readme, dict):
            readme = _projen_04054675.SampleReadmeProps(**readme)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _projen_04054675.RenovatebotOptions(**renovatebot_options)
        if isinstance(stale_options, dict):
            stale_options = _projen_github_04054675.StaleOptions(**stale_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688b1b698e0603390e1cd961c8c727da10bed7e457c04f86d923d08ac347d491)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument compile_options", value=compile_options, expected_type=type_hints["compile_options"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument distdir", value=distdir, expected_type=type_hints["distdir"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument junit", value=junit, expected_type=type_hints["junit"])
            check_type(argname="argument junit_options", value=junit_options, expected_type=type_hints["junit_options"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument mergify", value=mergify, expected_type=type_hints["mergify"])
            check_type(argname="argument mergify_options", value=mergify_options, expected_type=type_hints["mergify_options"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument packaging_options", value=packaging_options, expected_type=type_hints["packaging_options"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument parent_pom", value=parent_pom, expected_type=type_hints["parent_pom"])
            check_type(argname="argument project_type", value=project_type, expected_type=type_hints["project_type"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument projenrc_java", value=projenrc_java, expected_type=type_hints["projenrc_java"])
            check_type(argname="argument projenrc_java_options", value=projenrc_java_options, expected_type=type_hints["projenrc_java_options"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument projen_token_secret", value=projen_token_secret, expected_type=type_hints["projen_token_secret"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument sample_java_package", value=sample_java_package, expected_type=type_hints["sample_java_package"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument test_deps", value=test_deps, expected_type=type_hints["test_deps"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument default_release_branch", value=default_release_branch, expected_type=type_hints["default_release_branch"])
            check_type(argname="argument disable_default_licenses", value=disable_default_licenses, expected_type=type_hints["disable_default_licenses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if artifact_id is not None:
            self._values["artifact_id"] = artifact_id
        if auto_approve_options is not None:
            self._values["auto_approve_options"] = auto_approve_options
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if auto_merge_options is not None:
            self._values["auto_merge_options"] = auto_merge_options
        if clobber is not None:
            self._values["clobber"] = clobber
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if compile_options is not None:
            self._values["compile_options"] = compile_options
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if distdir is not None:
            self._values["distdir"] = distdir
        if github is not None:
            self._values["github"] = github
        if github_options is not None:
            self._values["github_options"] = github_options
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if gitpod is not None:
            self._values["gitpod"] = gitpod
        if group_id is not None:
            self._values["group_id"] = group_id
        if junit is not None:
            self._values["junit"] = junit
        if junit_options is not None:
            self._values["junit_options"] = junit_options
        if logging is not None:
            self._values["logging"] = logging
        if mergify is not None:
            self._values["mergify"] = mergify
        if mergify_options is not None:
            self._values["mergify_options"] = mergify_options
        if outdir is not None:
            self._values["outdir"] = outdir
        if packaging is not None:
            self._values["packaging"] = packaging
        if packaging_options is not None:
            self._values["packaging_options"] = packaging_options
        if parent is not None:
            self._values["parent"] = parent
        if parent_pom is not None:
            self._values["parent_pom"] = parent_pom
        if project_type is not None:
            self._values["project_type"] = project_type
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if projenrc_java is not None:
            self._values["projenrc_java"] = projenrc_java
        if projenrc_java_options is not None:
            self._values["projenrc_java_options"] = projenrc_java_options
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if projen_token_secret is not None:
            self._values["projen_token_secret"] = projen_token_secret
        if readme is not None:
            self._values["readme"] = readme
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if sample is not None:
            self._values["sample"] = sample
        if sample_java_package is not None:
            self._values["sample_java_package"] = sample_java_package
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if test_deps is not None:
            self._values["test_deps"] = test_deps
        if url is not None:
            self._values["url"] = url
        if version is not None:
            self._values["version"] = version
        if vscode is not None:
            self._values["vscode"] = vscode
        if default_release_branch is not None:
            self._values["default_release_branch"] = default_release_branch
        if disable_default_licenses is not None:
            self._values["disable_default_licenses"] = disable_default_licenses

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :default: $BASEDIR
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifact_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The artifactId is generally the name that the project is known by.

        Although
        the groupId is important, people within the group will rarely mention the
        groupId in discussion (they are often all be the same ID, such as the
        MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId,
        creates a key that separates this project from every other project in the
        world (at least, it should :) ). Along with the groupId, the artifactId
        fully defines the artifact's living quarters within the repository. In the
        case of the above project, my-project lives in
        $M2_REPO/org/codehaus/mojo/my-project.

        :default: "my-app"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_approve_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoApproveOptions]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoApproveOptions], result)

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable automatic merging on GitHub.

        Has no effect if ``github.mergify``
        is set to false.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoMergeOptions]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoMergeOptions], result)

    @builtins.property
    def clobber(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a ``clobber`` task which resets the repo to origin.

        :default: - true, but false for subprojects

        :stability: experimental
        '''
        result = self._values.get("clobber")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def compile_options(
        self,
    ) -> typing.Optional[_projen_java_04054675.MavenCompileOptions]:
        '''(experimental) Compile options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("compile_options")
        return typing.cast(typing.Optional[_projen_java_04054675.MavenCompileOptions], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``.

        Additional dependencies can be added via ``project.addDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of a project is always good.

        Although this should not replace
        formal documentation, a quick comment to any readers of the POM is always
        helpful.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dev_container(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a VSCode development environment (used for GitHub Codespaces).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dev_container")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def distdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Final artifact output directory.

        :default: "dist/java"

        :stability: experimental
        '''
        result = self._values.get("distdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable GitHub integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github_options(self) -> typing.Optional[_projen_github_04054675.GitHubOptions]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional[_projen_github_04054675.GitHubOptions], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_projen_04054675.IgnoreFileOptions]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_projen_04054675.IgnoreFileOptions], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_projen_04054675.GitOptions]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_projen_04054675.GitOptions], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) This is generally unique amongst an organization or a project.

        For example,
        all core Maven artifacts do (well, should) live under the groupId
        org.apache.maven. Group ID's do not necessarily use the dot notation, for
        example, the junit project. Note that the dot-notated groupId does not have
        to correspond to the package structure that the project contains. It is,
        however, a good practice to follow. When stored within a repository, the
        group acts much like the Java packaging structure does in an operating
        system. The dots are replaced by OS specific directory separators (such as
        '/' in Unix) which becomes a relative directory structure from the base
        repository. In the example given, the org.codehaus.mojo group lives within
        the directory $M2_REPO/org/codehaus/mojo.

        :default: "org.acme"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def junit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include junit tests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("junit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def junit_options(self) -> typing.Optional[_projen_java_04054675.JunitOptions]:
        '''(experimental) junit options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("junit_options")
        return typing.cast(typing.Optional[_projen_java_04054675.JunitOptions], result)

    @builtins.property
    def logging(self) -> typing.Optional[_projen_04054675.LoggerOptions]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_projen_04054675.LoggerOptions], result)

    @builtins.property
    def mergify(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether mergify should be enabled on this repository or not.

        :default: true

        :deprecated: use ``githubOptions.mergify`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.MergifyOptions]:
        '''(deprecated) Options for mergify.

        :default: - default options

        :deprecated: use ``githubOptions.mergifyOptions`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify_options")
        return typing.cast(typing.Optional[_projen_github_04054675.MergifyOptions], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project. Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packaging(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project packaging format.

        :default: "jar"

        :stability: experimental
        '''
        result = self._values.get("packaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packaging_options(
        self,
    ) -> typing.Optional[_projen_java_04054675.MavenPackagingOptions]:
        '''(experimental) Packaging options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("packaging_options")
        return typing.cast(typing.Optional[_projen_java_04054675.MavenPackagingOptions], result)

    @builtins.property
    def parent(self) -> typing.Optional[_projen_04054675.Project]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_projen_04054675.Project], result)

    @builtins.property
    def parent_pom(self) -> typing.Optional[_projen_java_04054675.ParentPom]:
        '''(experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("parent_pom")
        return typing.cast(typing.Optional[_projen_java_04054675.ParentPom], result)

    @builtins.property
    def project_type(self) -> typing.Optional[_projen_04054675.ProjectType]:
        '''(deprecated) Which type of project this is (library/app).

        :default: ProjectType.UNKNOWN

        :deprecated: no longer supported at the base project level

        :stability: deprecated
        '''
        result = self._values.get("project_type")
        return typing.cast(typing.Optional[_projen_04054675.ProjectType], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projen_credentials(
        self,
    ) -> typing.Optional[_projen_github_04054675.GithubCredentials]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_projen_github_04054675.GithubCredentials], result)

    @builtins.property
    def projenrc_java(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use projenrc in java.

        This will install ``projen`` as a java dependency and will add a ``synth`` task which
        will compile & execute ``main()`` from ``src/main/java/projenrc.java``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("projenrc_java")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_java_options(
        self,
    ) -> typing.Optional[_projen_java_04054675.ProjenrcOptions]:
        '''(experimental) Options related to projenrc in java.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_java_options")
        return typing.cast(typing.Optional[_projen_java_04054675.ProjenrcOptions], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(
        self,
    ) -> typing.Optional[_projen_04054675.ProjenrcJsonOptions]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_projen_04054675.ProjenrcJsonOptions], result)

    @builtins.property
    def projen_token_secret(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows.

        This token needs to have the ``repo``, ``workflows``
        and ``packages`` scope.

        :default: "PROJEN_GITHUB_TOKEN"

        :deprecated: use ``projenCredentials``

        :stability: deprecated
        '''
        result = self._values.get("projen_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme(self) -> typing.Optional[_projen_04054675.SampleReadmeProps]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[_projen_04054675.SampleReadmeProps], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(
        self,
    ) -> typing.Optional[_projen_04054675.RenovatebotOptions]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_projen_04054675.RenovatebotOptions], result)

    @builtins.property
    def sample(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include sample code and test if the relevant directories don't exist.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sample")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sample_java_package(self) -> typing.Optional[builtins.str]:
        '''(experimental) The java package to use for the code sample.

        :default: "org.acme"

        :stability: experimental
        '''
        result = self._values.get("sample_java_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stale(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Auto-close of stale issues and pull request.

        See ``staleOptions`` for options.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stale")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale_options(self) -> typing.Optional[_projen_github_04054675.StaleOptions]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional[_projen_github_04054675.StaleOptions], result)

    @builtins.property
    def test_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``.

        Additional dependencies can be added via ``project.addTestDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("test_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL, like the name, is not required.

        This is a nice gesture for
        projects users, however, so that they know where the project lives.

        :default: undefined

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) This is the last piece of the naming puzzle.

        groupId:artifactId denotes a
        single project but they cannot delineate which incarnation of that project
        we are talking about. Do we want the junit:junit of 2018 (version 4.12), or
        of 2007 (version 3.8.2)? In short: code changes, those changes should be
        versioned, and this element keeps those versions in line. It is also used
        within an artifact's repository to separate versions from each other.
        my-project version 1.0 files live in the directory structure
        $M2_REPO/org/codehaus/mojo/my-project/1.0.

        :default: "0.1.0"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vscode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable VSCode integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("vscode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default_release_branch(self) -> typing.Optional[builtins.str]:
        result = self._values.get("default_release_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_default_licenses(self) -> typing.Optional[builtins.bool]:
        '''Whether to disable the generation of default licenses.

        :default: false
        '''
        result = self._values.get("disable_default_licenses")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonorepoJavaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INxProjectCore)
class MonorepoJavaProject(
    _projen_java_04054675.JavaProject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.monorepo.MonorepoJavaProject",
):
    '''This project type will bootstrap a NX based monorepo with support for polygot builds, build caching, dependency graph visualization and much more.

    :pjid: monorepo-java
    '''

    def __init__(
        self,
        *,
        default_release_branch: typing.Optional[builtins.str] = None,
        disable_default_licenses: typing.Optional[builtins.bool] = None,
        name: builtins.str,
        artifact_id: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        distdir: typing.Optional[builtins.str] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        group_id: typing.Optional[builtins.str] = None,
        junit: typing.Optional[builtins.bool] = None,
        junit_options: typing.Optional[typing.Union[_projen_java_04054675.JunitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        packaging: typing.Optional[builtins.str] = None,
        packaging_options: typing.Optional[typing.Union[_projen_java_04054675.MavenPackagingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        parent_pom: typing.Optional[typing.Union[_projen_java_04054675.ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_projen_04054675.ProjectType] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
        projenrc_java: typing.Optional[builtins.bool] = None,
        projenrc_java_options: typing.Optional[typing.Union[_projen_java_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        sample: typing.Optional[builtins.bool] = None,
        sample_java_package: typing.Optional[builtins.str] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param default_release_branch: 
        :param disable_default_licenses: Whether to disable the generation of default licenses. Default: false
        :param name: Default: $BASEDIR
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param compile_options: (experimental) Compile options. Default: - defaults
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param distdir: (experimental) Final artifact output directory. Default: "dist/java"
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param group_id: (experimental) This is generally unique amongst an organization or a project. For example, all core Maven artifacts do (well, should) live under the groupId org.apache.maven. Group ID's do not necessarily use the dot notation, for example, the junit project. Note that the dot-notated groupId does not have to correspond to the package structure that the project contains. It is, however, a good practice to follow. When stored within a repository, the group acts much like the Java packaging structure does in an operating system. The dots are replaced by OS specific directory separators (such as '/' in Unix) which becomes a relative directory structure from the base repository. In the example given, the org.codehaus.mojo group lives within the directory $M2_REPO/org/codehaus/mojo. Default: "org.acme"
        :param junit: (experimental) Include junit tests. Default: true
        :param junit_options: (experimental) junit options. Default: - defaults
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param packaging: (experimental) Project packaging format. Default: "jar"
        :param packaging_options: (experimental) Packaging options. Default: - defaults
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param parent_pom: (experimental) A Parent Pom can be used to have a child project inherit properties/plugins/ect in order to reduce duplication and keep standards across a large amount of repos. Default: undefined
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projenrc_java: (experimental) Use projenrc in java. This will install ``projen`` as a java dependency and will add a ``synth`` task which will compile & execute ``main()`` from ``src/main/java/projenrc.java``. Default: true
        :param projenrc_java_options: (experimental) Options related to projenrc in java. Default: - default options
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param sample_java_package: (experimental) The java package to use for the code sample. Default: "org.acme"
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param test_deps: (experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addTestDependency()``. Default: []
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        '''
        options = MonorepoJavaOptions(
            default_release_branch=default_release_branch,
            disable_default_licenses=disable_default_licenses,
            name=name,
            artifact_id=artifact_id,
            auto_approve_options=auto_approve_options,
            auto_merge=auto_merge,
            auto_merge_options=auto_merge_options,
            clobber=clobber,
            commit_generated=commit_generated,
            compile_options=compile_options,
            deps=deps,
            description=description,
            dev_container=dev_container,
            distdir=distdir,
            github=github,
            github_options=github_options,
            git_ignore_options=git_ignore_options,
            git_options=git_options,
            gitpod=gitpod,
            group_id=group_id,
            junit=junit,
            junit_options=junit_options,
            logging=logging,
            mergify=mergify,
            mergify_options=mergify_options,
            outdir=outdir,
            packaging=packaging,
            packaging_options=packaging_options,
            parent=parent,
            parent_pom=parent_pom,
            project_type=project_type,
            projen_command=projen_command,
            projen_credentials=projen_credentials,
            projenrc_java=projenrc_java,
            projenrc_java_options=projenrc_java_options,
            projenrc_json=projenrc_json,
            projenrc_json_options=projenrc_json_options,
            projen_token_secret=projen_token_secret,
            readme=readme,
            renovatebot=renovatebot,
            renovatebot_options=renovatebot_options,
            sample=sample,
            sample_java_package=sample_java_package,
            stale=stale,
            stale_options=stale_options,
            test_deps=test_deps,
            url=url,
            version=version,
            vscode=vscode,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addImplicitDependency")
    def add_implicit_dependency(
        self,
        dependent: _projen_04054675.Project,
        dependee: typing.Union[builtins.str, _projen_04054675.Project],
    ) -> None:
        '''Create an implicit dependency between two Projects.

        This is typically
        used in polygot repos where a Typescript project wants a build dependency
        on a Python project as an example.

        :param dependent: -
        :param dependee: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682830f1683b2735615a32e11be70033ae0868bfb3cc36d516befc9cdfef58c2)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addImplicitDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addJavaDependency")
    def add_java_dependency(
        self,
        dependent: _projen_java_04054675.JavaProject,
        dependee: _projen_java_04054675.JavaProject,
    ) -> None:
        '''Adds a dependency between two Java Projects in the monorepo.

        :param dependent: -
        :param dependee: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df53f208f195928611c6206487d14e22d8883a812b62159391dd91389c9c2e15)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addJavaDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addNxRunManyTask")
    def add_nx_run_many_task(
        self,
        name: builtins.str,
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
    ) -> _projen_04054675.Task:
        '''Add project task that executes ``npx nx run-many ...`` style command.

        :param name: -
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

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b3ad8588c14991da810bc28684e6ad2df1494945d81d2b318de4f318874505)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(_projen_04054675.Task, jsii.invoke(self, "addNxRunManyTask", [name, options]))

    @jsii.member(jsii_name="addPythonPoetryDependency")
    def add_python_poetry_dependency(
        self,
        dependent: _projen_python_04054675.PythonProject,
        dependee: _projen_python_04054675.PythonProject,
    ) -> None:
        '''Adds a dependency between two Python Projects in the monorepo.

        The dependent must have Poetry enabled.

        :param dependent: -
        :param dependee: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__064e49db934492bfa2ed35bd60a9fa5b97c2242d05f3a08312676ae30bfbfac8)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addPythonPoetryDependency", [dependent, dependee]))

    @jsii.member(jsii_name="composeNxRunManyCommand")
    def compose_nx_run_many_command(
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
    ) -> typing.List[builtins.str]:
        '''Helper to format ``npx nx run-many ...`` style command.

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

        :inheritdoc: true
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "composeNxRunManyCommand", [options]))

    @jsii.member(jsii_name="execNxRunManyCommand")
    def exec_nx_run_many_command(
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
    ) -> builtins.str:
        '''Helper to format ``npx nx run-many ...`` style command execution in package manager.

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

        :inheritdoc: true
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "execNxRunManyCommand", [options]))

    @jsii.member(jsii_name="postSynthesize")
    def post_synthesize(self) -> None:
        '''Called after all components are synthesized.

        Order is *not* guaranteed.
        '''
        return typing.cast(None, jsii.invoke(self, "postSynthesize", []))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''Called before all components are synthesized.

        :inheritdoc: true
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        '''Synthesize all project files into ``outdir``.

        1. Call "this.preSynthesize()"
        2. Delete all generated files
        3. Synthesize all subprojects
        4. Synthesize all components of this project
        5. Call "postSynthesize()" for all components of this project
        6. Call "this.postSynthesize()"

        :inheritDoc: true
        '''
        return typing.cast(None, jsii.invoke(self, "synth", []))

    @builtins.property
    @jsii.member(jsii_name="nx")
    def nx(self) -> "NxWorkspace":
        '''Return the NxWorkspace instance.

        This should be implemented using a getter.

        :inheritdoc: true
        '''
        return typing.cast("NxWorkspace", jsii.get(self, "nx"))

    @builtins.property
    @jsii.member(jsii_name="nxConfigurator")
    def nx_configurator(self) -> "NxConfigurator":
        return typing.cast("NxConfigurator", jsii.get(self, "nxConfigurator"))


@jsii.implements(INxProjectCore)
class MonorepoPythonProject(
    _projen_python_04054675.PythonProject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.monorepo.MonorepoPythonProject",
):
    '''This project type will bootstrap a NX based monorepo with support for polygot builds, build caching, dependency graph visualization and much more.

    :pjid: monorepo-py
    '''

    def __init__(
        self,
        *,
        default_release_branch: typing.Optional[builtins.str] = None,
        license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        module_name: builtins.str,
        name: builtins.str,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        package_name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        poetry_options: typing.Optional[typing.Union[_projen_python_04054675.PoetryPyprojectOptionsWithoutDeps, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_projen_04054675.ProjectType] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_python_options: typing.Optional[typing.Union[_projen_python_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        pytest: typing.Optional[builtins.bool] = None,
        pytest_options: typing.Optional[typing.Union[_projen_python_04054675.PytestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        python_exec: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        sample: typing.Optional[builtins.bool] = None,
        setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        setuptools: typing.Optional[builtins.bool] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param default_release_branch: 
        :param license_options: Default license to apply to all PDK managed packages. Default: Apache-2.0
        :param module_name: Default: $PYTHON_MODULE_NAME
        :param name: Default: $BASEDIR
        :param author_email: (experimental) Author's e-mail. Default: $GIT_USER_EMAIL
        :param author_name: (experimental) Author's name. Default: $GIT_USER_NAME
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param classifiers: (experimental) A list of PyPI trove classifiers that describe the project.
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) A short description of the package.
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param dev_deps: (experimental) List of dev dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDevDependency()``. Default: []
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param homepage: (experimental) A URL to the website of the project.
        :param license: (experimental) License of this package as an SPDX identifier.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param package_name: (experimental) Package name.
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param poetry_options: (experimental) Additional options to set for poetry if using poetry.
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param projenrc_python_options: (experimental) Options related to projenrc in python. Default: - default options
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param pytest: (experimental) Include pytest tests. Default: true
        :param pytest_options: (experimental) pytest options. Default: - defaults
        :param python_exec: (experimental) Path to the python executable to use. Default: "python"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param setup_config: (experimental) Additional fields to pass in the setup() function if using setuptools.
        :param setuptools: (experimental) Use setuptools with a setup.py script for packaging and publishing. Default: - true, unless poetry is true, then false
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param version: (experimental) Version of the package. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        '''
        options = MonorepoPythonProjectOptions(
            default_release_branch=default_release_branch,
            license_options=license_options,
            module_name=module_name,
            name=name,
            author_email=author_email,
            author_name=author_name,
            auto_approve_options=auto_approve_options,
            auto_merge=auto_merge,
            auto_merge_options=auto_merge_options,
            classifiers=classifiers,
            clobber=clobber,
            commit_generated=commit_generated,
            deps=deps,
            description=description,
            dev_container=dev_container,
            dev_deps=dev_deps,
            github=github,
            github_options=github_options,
            git_ignore_options=git_ignore_options,
            git_options=git_options,
            gitpod=gitpod,
            homepage=homepage,
            license=license,
            logging=logging,
            mergify=mergify,
            mergify_options=mergify_options,
            outdir=outdir,
            package_name=package_name,
            parent=parent,
            poetry_options=poetry_options,
            project_type=project_type,
            projen_command=projen_command,
            projen_credentials=projen_credentials,
            projenrc_json=projenrc_json,
            projenrc_json_options=projenrc_json_options,
            projenrc_python_options=projenrc_python_options,
            projen_token_secret=projen_token_secret,
            pytest=pytest,
            pytest_options=pytest_options,
            python_exec=python_exec,
            readme=readme,
            renovatebot=renovatebot,
            renovatebot_options=renovatebot_options,
            sample=sample,
            setup_config=setup_config,
            setuptools=setuptools,
            stale=stale,
            stale_options=stale_options,
            version=version,
            vscode=vscode,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addImplicitDependency")
    def add_implicit_dependency(
        self,
        dependent: _projen_04054675.Project,
        dependee: typing.Union[builtins.str, _projen_04054675.Project],
    ) -> None:
        '''Create an implicit dependency between two Projects.

        This is typically
        used in polygot repos where a Typescript project wants a build dependency
        on a Python project as an example.

        :param dependent: -
        :param dependee: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c886f4ab8dd9ee1d320a6473c4742e3d18b1f0c1c86d73cca3420ea7c19ee00)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addImplicitDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addJavaDependency")
    def add_java_dependency(
        self,
        dependent: _projen_java_04054675.JavaProject,
        dependee: _projen_java_04054675.JavaProject,
    ) -> None:
        '''Adds a dependency between two Java Projects in the monorepo.

        :param dependent: -
        :param dependee: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea38efa6f69de4704088112a006c41ca3887f1bb1c5ab6afe85c1e1975a3930a)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addJavaDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addNxRunManyTask")
    def add_nx_run_many_task(
        self,
        name: builtins.str,
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
    ) -> _projen_04054675.Task:
        '''Add project task that executes ``npx nx run-many ...`` style command.

        :param name: -
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

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee599bc4aadc41024c7991894dcc12951d573665b01127355bca175810feca2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(_projen_04054675.Task, jsii.invoke(self, "addNxRunManyTask", [name, options]))

    @jsii.member(jsii_name="addPythonPoetryDependency")
    def add_python_poetry_dependency(
        self,
        dependent: _projen_python_04054675.PythonProject,
        dependee: _projen_python_04054675.PythonProject,
    ) -> None:
        '''Adds a dependency between two Python Projects in the monorepo.

        The dependent must have Poetry enabled.

        :param dependent: -
        :param dependee: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa90809879df9155778f3dd8ecee1ed68af72c551df6d1f25f71fd0d896f4e7)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addPythonPoetryDependency", [dependent, dependee]))

    @jsii.member(jsii_name="composeNxRunManyCommand")
    def compose_nx_run_many_command(
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
    ) -> typing.List[builtins.str]:
        '''Helper to format ``npx nx run-many ...`` style command.

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

        :inheritdoc: true
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "composeNxRunManyCommand", [options]))

    @jsii.member(jsii_name="execNxRunManyCommand")
    def exec_nx_run_many_command(
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
    ) -> builtins.str:
        '''Helper to format ``npx nx run-many ...`` style command execution in package manager.

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

        :inheritdoc: true
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "execNxRunManyCommand", [options]))

    @jsii.member(jsii_name="postSynthesize")
    def post_synthesize(self) -> None:
        '''Called after all components are synthesized.

        Order is *not* guaranteed.
        NOTE: Be sure to ensure the VIRTUAL_ENV is unset during postSynthesize as the individual poetry envs will only be created if a existing VIRTUAL_ENV cannot be found.

        :inheritdoc: NOTE: Be sure to ensure the VIRTUAL_ENV is unset during postSynthesize as the individual poetry envs will only be created if a existing VIRTUAL_ENV cannot be found.
        '''
        return typing.cast(None, jsii.invoke(self, "postSynthesize", []))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''Called before all components are synthesized.

        :inheritdoc: true
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        '''Synthesize all project files into ``outdir``.

        1. Call "this.preSynthesize()"
        2. Delete all generated files
        3. Synthesize all subprojects
        4. Synthesize all components of this project
        5. Call "postSynthesize()" for all components of this project
        6. Call "this.postSynthesize()"

        :inheritDoc: true
        '''
        return typing.cast(None, jsii.invoke(self, "synth", []))

    @builtins.property
    @jsii.member(jsii_name="nx")
    def nx(self) -> "NxWorkspace":
        '''Return the NxWorkspace instance.

        This should be implemented using a getter.

        :inheritdoc: true
        '''
        return typing.cast("NxWorkspace", jsii.get(self, "nx"))

    @builtins.property
    @jsii.member(jsii_name="nxConfigurator")
    def nx_configurator(self) -> "NxConfigurator":
        return typing.cast("NxConfigurator", jsii.get(self, "nxConfigurator"))


@jsii.implements(INxProjectCore)
class MonorepoTsProject(
    _projen_typescript_04054675.TypeScriptProject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.monorepo.MonorepoTsProject",
):
    '''This project type will bootstrap a monorepo with support for polygot builds, build caching, dependency graph visualization and much more.

    :pjid: monorepo-ts
    '''

    def __init__(
        self,
        *,
        disable_node_warnings: typing.Optional[builtins.bool] = None,
        license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        monorepo_upgrade_deps: typing.Optional[builtins.bool] = None,
        monorepo_upgrade_deps_options: typing.Optional[typing.Union["MonorepoUpgradeDepsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_config: typing.Optional[typing.Union["WorkspaceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: builtins.str,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        artifacts_directory: typing.Optional[builtins.str] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        author_organization: typing.Optional[builtins.bool] = None,
        author_url: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_approve_upgrades: typing.Optional[builtins.bool] = None,
        auto_detect_bin: typing.Optional[builtins.bool] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bugs_email: typing.Optional[builtins.str] = None,
        bugs_url: typing.Optional[builtins.str] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        copyright_owner: typing.Optional[builtins.str] = None,
        copyright_period: typing.Optional[builtins.str] = None,
        default_release_branch: typing.Optional[builtins.str] = None,
        dependabot: typing.Optional[builtins.bool] = None,
        dependabot_options: typing.Optional[typing.Union[_projen_github_04054675.DependabotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        deps_upgrade: typing.Optional[builtins.bool] = None,
        deps_upgrade_options: typing.Optional[typing.Union[_projen_javascript_04054675.UpgradeDependenciesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        disable_tsconfig: typing.Optional[builtins.bool] = None,
        disable_tsconfig_dev: typing.Optional[builtins.bool] = None,
        docgen: typing.Optional[builtins.bool] = None,
        docs_directory: typing.Optional[builtins.str] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        entrypoint_types: typing.Optional[builtins.str] = None,
        eslint: typing.Optional[builtins.bool] = None,
        eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        libdir: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        licensed: typing.Optional[builtins.bool] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        major_version: typing.Optional[jsii.Number] = None,
        max_node_version: typing.Optional[builtins.str] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        min_node_version: typing.Optional[builtins.str] = None,
        mutable_build: typing.Optional[builtins.bool] = None,
        npm_access: typing.Optional[_projen_javascript_04054675.NpmAccess] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        npmignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        npmignore_enabled: typing.Optional[builtins.bool] = None,
        npm_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        npm_provenance: typing.Optional[builtins.bool] = None,
        npm_registry: typing.Optional[builtins.str] = None,
        npm_registry_url: typing.Optional[builtins.str] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        outdir: typing.Optional[builtins.str] = None,
        package: typing.Optional[builtins.bool] = None,
        package_manager: typing.Optional[_projen_javascript_04054675.NodePackageManager] = None,
        package_name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        peer_dependency_options: typing.Optional[typing.Union[_projen_javascript_04054675.PeerDependencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        pnpm_version: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        prettier: typing.Optional[builtins.bool] = None,
        prettier_options: typing.Optional[typing.Union[_projen_javascript_04054675.PrettierOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_projen_04054675.ProjectType] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
        projen_dev_dependency: typing.Optional[builtins.bool] = None,
        projenrc_js: typing.Optional[builtins.bool] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_js_options: typing.Optional[typing.Union[_projen_javascript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_ts: typing.Optional[builtins.bool] = None,
        projenrc_ts_options: typing.Optional[typing.Union[_projen_typescript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        projen_version: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        pull_request_template: typing.Optional[builtins.bool] = None,
        pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
        releasable_commits: typing.Optional[_projen_04054675.ReleasableCommits] = None,
        release: typing.Optional[builtins.bool] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[_projen_release_04054675.BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_to_npm: typing.Optional[builtins.bool] = None,
        release_trigger: typing.Optional[_projen_release_04054675.ReleaseTrigger] = None,
        release_workflow: typing.Optional[builtins.bool] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_directory: typing.Optional[builtins.str] = None,
        sample_code: typing.Optional[builtins.bool] = None,
        scoped_packages_options: typing.Optional[typing.Sequence[typing.Union[_projen_javascript_04054675.ScopedPackagesOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        srcdir: typing.Optional[builtins.str] = None,
        stability: typing.Optional[builtins.str] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        testdir: typing.Optional[builtins.str] = None,
        tsconfig: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev_file: typing.Optional[builtins.str] = None,
        ts_jest_options: typing.Optional[typing.Union[_projen_typescript_04054675.TsJestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        typescript_version: typing.Optional[builtins.str] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_git_identity: typing.Optional[typing.Union[_projen_github_04054675.GitIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_package_cache: typing.Optional[builtins.bool] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_projen_04054675.GroupRunnerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        yarn_berry_options: typing.Optional[typing.Union[_projen_javascript_04054675.YarnBerryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param disable_node_warnings: Disable node warnings from being emitted during build tasks. Default: false
        :param license_options: Default license to apply to all PDK managed packages. Default: Apache-2.0
        :param monorepo_upgrade_deps: Whether to include an upgrade-deps task at the root of the monorepo which will upgrade all dependencies. Default: true
        :param monorepo_upgrade_deps_options: Monorepo Upgrade Deps options. This is only used if monorepoUpgradeDeps is true. Default: undefined
        :param workspace_config: Configuration for workspace.
        :param name: Default: $BASEDIR
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param artifacts_directory: (experimental) A directory which will contain build artifacts. Default: "dist"
        :param author_email: (experimental) Author's e-mail.
        :param author_name: (experimental) Author's name.
        :param author_organization: (experimental) Is the author an organization.
        :param author_url: (experimental) Author's URL / Website.
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_approve_upgrades: (experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configued). Throw if set to true but ``autoApproveOptions`` are not defined. Default: - true
        :param auto_detect_bin: (experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section. Default: true
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param bin: (experimental) Binary programs vended with your module. You can use this option to add/customize how binaries are represented in your ``package.json``, but unless ``autoDetectBin`` is ``false``, every executable file under ``bin`` will automatically be added to this section.
        :param bugs_email: (experimental) The email address to which issues should be reported.
        :param bugs_url: (experimental) The url to your project's issue tracker.
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_options: (experimental) Options for PR build workflow.
        :param build_workflow_triggers: (deprecated) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param check_licenses: (experimental) Configure which licenses should be deemed acceptable for use by dependencies. This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered. Default: - no license checks are run during the build and all licenses will be accepted
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v4 A secret is required for private repos. Configured with ``@codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories. Default: - if this option is not specified, only public repositories are supported
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param copyright_owner: (experimental) License copyright owner. Default: - defaults to the value of authorName or "" if ``authorName`` is undefined.
        :param copyright_period: (experimental) The copyright years to put in the LICENSE file. Default: - current year
        :param default_release_branch: (experimental) The name of the main release branch. Default: "main"
        :param dependabot: (experimental) Use dependabot to handle dependency upgrades. Cannot be used in conjunction with ``depsUpgrade``. Default: false
        :param dependabot_options: (experimental) Options for dependabot. Default: - default options
        :param deps: (experimental) Runtime dependencies of this module. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param deps_upgrade: (experimental) Use tasks and github workflows to handle dependency upgrades. Cannot be used in conjunction with ``dependabot``. Default: true
        :param deps_upgrade_options: (experimental) Options for ``UpgradeDependencies``. Default: - default options
        :param description: (experimental) The description is just a string that helps people understand the purpose of the package. It can be used when searching for packages in a package manager as well. See https://classic.yarnpkg.com/en/docs/package-json/#toc-description
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param dev_deps: (experimental) Build dependencies for this module. These dependencies will only be available in your build environment but will not be fetched when this module is consumed. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param disable_tsconfig: (experimental) Do not generate a ``tsconfig.json`` file (used by jsii projects since tsconfig.json is generated by the jsii compiler). Default: false
        :param disable_tsconfig_dev: (experimental) Do not generate a ``tsconfig.dev.json`` file. Default: false
        :param docgen: (experimental) Docgen by Typedoc. Default: false
        :param docs_directory: (experimental) Docs directory. Default: "docs"
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json. Default: "lib/index.js"
        :param entrypoint_types: (experimental) The .d.ts file that includes the type declarations for this module. Default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)
        :param eslint: (experimental) Setup eslint. Default: true
        :param eslint_options: (experimental) Eslint options. Default: - opinionated default options
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param homepage: (experimental) Package's Homepage / Website.
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param libdir: (experimental) Typescript artifacts output directory. Default: "lib"
        :param license: (experimental) License's SPDX identifier. See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses. Use the ``licensed`` option if you want to no license to be specified. Default: "Apache-2.0"
        :param licensed: (experimental) Indicates if a license should be added. Default: true
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param max_node_version: (experimental) Minimum node.js version to require via ``engines`` (inclusive). Default: - no max
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param min_node_version: (experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive). Default: - no "engines" specified
        :param mutable_build: (deprecated) Automatically update files modified during builds to pull-request branches. This means that any files synthesized by projen or e.g. test snapshots will always be up-to-date before a PR is merged. Implies that PR builds do not have anti-tamper checks. Default: true
        :param npm_access: (experimental) Access level of the npm package. Default: - for scoped packages (e.g. ``foo@bar``), the default is ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is ``NpmAccess.PUBLIC``.
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param npmignore: (deprecated) Additional entries to .npmignore.
        :param npmignore_enabled: (experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs. Default: true
        :param npm_ignore_options: (experimental) Configuration options for .npmignore file.
        :param npm_provenance: (experimental) Should provenance statements be generated when the package is published. A supported package manager is required to publish a package with npm provenance statements and you will need to use a supported CI/CD provider. Note that the projen ``Release`` and ``Publisher`` components are using ``publib`` to publish packages, which is using npm internally and supports provenance statements independently of the package manager used. Default: - true for public packages, false otherwise
        :param npm_registry: (deprecated) The host name of the npm registry to publish to. Cannot be set together with ``npmRegistryUrl``.
        :param npm_registry_url: (experimental) The base URL of the npm package registry. Must be a URL (e.g. start with "https://" or "http://") Default: "https://registry.npmjs.org"
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: "NPM_TOKEN"
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param package: (experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``). Default: true
        :param package_manager: (experimental) The Node Package Manager used to execute scripts. Default: NodePackageManager.YARN_CLASSIC
        :param package_name: (experimental) The "name" in package.json. Default: - defaults to project name
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param peer_dependency_options: (experimental) Options for ``peerDeps``.
        :param peer_deps: (experimental) Peer dependencies for this module. Dependencies listed here are required to be installed (and satisfied) by the *consumer* of this library. Using peer dependencies allows you to ensure that only a single module of a certain library exists in the ``node_modules`` tree of your consumers. Note that prior to npm@7, peer dependencies are *not* automatically installed, which means that adding peer dependencies to a library will be a breaking change for your customers. Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is enabled by default), projen will automatically add a dev dependency with a pinned version for each peer dependency. This will ensure that you build & test your module against the lowest peer version required. Default: []
        :param pnpm_version: (experimental) The version of PNPM to use if using PNPM as a package manager. Default: "7"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param prettier: (experimental) Setup prettier. Default: false
        :param prettier_options: (experimental) Prettier options. Default: - default options
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projen_dev_dependency: (experimental) Indicates of "projen" should be installed as a devDependency. Default: - true if not a subproject
        :param projenrc_js: (experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation. Default: - true if projenrcJson is false
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param projenrc_js_options: (experimental) Options for .projenrc.js. Default: - default options
        :param projenrc_ts: (experimental) Use TypeScript for your projenrc file (``.projenrc.ts``). Default: false
        :param projenrc_ts_options: (experimental) Options for .projenrc.ts.
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param projen_version: (experimental) Version of projen to install. Default: - Defaults to the latest version.
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param pull_request_template: (experimental) Include a GitHub pull request template. Default: true
        :param pull_request_template_contents: (experimental) The contents of the pull request template. Default: - default content
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release: (experimental) Add release management to this project. Default: - true (false for subprojects)
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_every_commit: (deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_schedule: (deprecated) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_to_npm: (experimental) Automatically release to npm when new versions are introduced. Default: false
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow: (deprecated) DEPRECATED: renamed to ``release``. Default: - true if not a subproject
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param repository: (experimental) The repository is the location where the actual code for your package lives. See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository
        :param repository_directory: (experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.
        :param sample_code: (experimental) Generate one-time sample in ``src/`` and ``test/`` if there are no files there. Default: true
        :param scoped_packages_options: (experimental) Options for privately hosted scoped packages. Default: - fetch all scoped packages from the public npm registry
        :param scripts: (deprecated) npm scripts to include. If a script has the same name as a standard script, the standard script will be overwritten. Also adds the script as a task. Default: {}
        :param srcdir: (experimental) Typescript sources directory. Default: "src"
        :param stability: (experimental) Package's Stability.
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param testdir: (experimental) Jest tests directory. Tests files should be named ``xxx.test.ts``. If this directory is under ``srcdir`` (e.g. ``src/test``, ``src/__tests__``), then tests are going to be compiled into ``lib/`` and executed as javascript. If the test directory is outside of ``src``, then we configure jest to compile the code in-memory. Default: "test"
        :param tsconfig: (experimental) Custom TSConfig. Default: - default options
        :param tsconfig_dev: (experimental) Custom tsconfig options for the development tsconfig.json file (used for testing). Default: - use the production tsconfig options
        :param tsconfig_dev_file: (experimental) The name of the development tsconfig.json file. Default: "tsconfig.dev.json"
        :param ts_jest_options: (experimental) Options for ts-jest.
        :param typescript_version: (experimental) TypeScript version to use. NOTE: Typescript is not semantically versioned and should remain on the same minor, so we recommend using a ``~`` dependency (e.g. ``~1.2.3``). Default: "latest"
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with standard-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param workflow_bootstrap_steps: (experimental) Workflow steps to use in order to bootstrap this repo. Default: "yarn install --frozen-lockfile && yarn projen"
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_git_identity: (experimental) The git identity to use in workflows. Default: - GitHub Actions
        :param workflow_node_version: (experimental) The node version to use in GitHub workflows. Default: - same as ``minNodeVersion``
        :param workflow_package_cache: (experimental) Enable Node.js package cache in GitHub workflows. Default: false
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param yarn_berry_options: (experimental) Options for Yarn Berry. Default: - Yarn Berry v4 with all default options
        '''
        options = MonorepoTsProjectOptions(
            disable_node_warnings=disable_node_warnings,
            license_options=license_options,
            monorepo_upgrade_deps=monorepo_upgrade_deps,
            monorepo_upgrade_deps_options=monorepo_upgrade_deps_options,
            workspace_config=workspace_config,
            name=name,
            allow_library_dependencies=allow_library_dependencies,
            artifacts_directory=artifacts_directory,
            author_email=author_email,
            author_name=author_name,
            author_organization=author_organization,
            author_url=author_url,
            auto_approve_options=auto_approve_options,
            auto_approve_upgrades=auto_approve_upgrades,
            auto_detect_bin=auto_detect_bin,
            auto_merge=auto_merge,
            auto_merge_options=auto_merge_options,
            bin=bin,
            bugs_email=bugs_email,
            bugs_url=bugs_url,
            build_workflow=build_workflow,
            build_workflow_options=build_workflow_options,
            build_workflow_triggers=build_workflow_triggers,
            bundled_deps=bundled_deps,
            bundler_options=bundler_options,
            check_licenses=check_licenses,
            clobber=clobber,
            code_artifact_options=code_artifact_options,
            code_cov=code_cov,
            code_cov_token_secret=code_cov_token_secret,
            commit_generated=commit_generated,
            copyright_owner=copyright_owner,
            copyright_period=copyright_period,
            default_release_branch=default_release_branch,
            dependabot=dependabot,
            dependabot_options=dependabot_options,
            deps=deps,
            deps_upgrade=deps_upgrade,
            deps_upgrade_options=deps_upgrade_options,
            description=description,
            dev_container=dev_container,
            dev_deps=dev_deps,
            disable_tsconfig=disable_tsconfig,
            disable_tsconfig_dev=disable_tsconfig_dev,
            docgen=docgen,
            docs_directory=docs_directory,
            entrypoint=entrypoint,
            entrypoint_types=entrypoint_types,
            eslint=eslint,
            eslint_options=eslint_options,
            github=github,
            github_options=github_options,
            gitignore=gitignore,
            git_ignore_options=git_ignore_options,
            git_options=git_options,
            gitpod=gitpod,
            homepage=homepage,
            jest=jest,
            jest_options=jest_options,
            jsii_release_version=jsii_release_version,
            keywords=keywords,
            libdir=libdir,
            license=license,
            licensed=licensed,
            logging=logging,
            major_version=major_version,
            max_node_version=max_node_version,
            mergify=mergify,
            mergify_options=mergify_options,
            min_major_version=min_major_version,
            min_node_version=min_node_version,
            mutable_build=mutable_build,
            npm_access=npm_access,
            npm_dist_tag=npm_dist_tag,
            npmignore=npmignore,
            npmignore_enabled=npmignore_enabled,
            npm_ignore_options=npm_ignore_options,
            npm_provenance=npm_provenance,
            npm_registry=npm_registry,
            npm_registry_url=npm_registry_url,
            npm_token_secret=npm_token_secret,
            outdir=outdir,
            package=package,
            package_manager=package_manager,
            package_name=package_name,
            parent=parent,
            peer_dependency_options=peer_dependency_options,
            peer_deps=peer_deps,
            pnpm_version=pnpm_version,
            post_build_steps=post_build_steps,
            prerelease=prerelease,
            prettier=prettier,
            prettier_options=prettier_options,
            project_type=project_type,
            projen_command=projen_command,
            projen_credentials=projen_credentials,
            projen_dev_dependency=projen_dev_dependency,
            projenrc_js=projenrc_js,
            projenrc_json=projenrc_json,
            projenrc_json_options=projenrc_json_options,
            projenrc_js_options=projenrc_js_options,
            projenrc_ts=projenrc_ts,
            projenrc_ts_options=projenrc_ts_options,
            projen_token_secret=projen_token_secret,
            projen_version=projen_version,
            publish_dry_run=publish_dry_run,
            publish_tasks=publish_tasks,
            pull_request_template=pull_request_template,
            pull_request_template_contents=pull_request_template_contents,
            readme=readme,
            releasable_commits=releasable_commits,
            release=release,
            release_branches=release_branches,
            release_every_commit=release_every_commit,
            release_failure_issue=release_failure_issue,
            release_failure_issue_label=release_failure_issue_label,
            release_schedule=release_schedule,
            release_tag_prefix=release_tag_prefix,
            release_to_npm=release_to_npm,
            release_trigger=release_trigger,
            release_workflow=release_workflow,
            release_workflow_name=release_workflow_name,
            release_workflow_setup_steps=release_workflow_setup_steps,
            renovatebot=renovatebot,
            renovatebot_options=renovatebot_options,
            repository=repository,
            repository_directory=repository_directory,
            sample_code=sample_code,
            scoped_packages_options=scoped_packages_options,
            scripts=scripts,
            srcdir=srcdir,
            stability=stability,
            stale=stale,
            stale_options=stale_options,
            testdir=testdir,
            tsconfig=tsconfig,
            tsconfig_dev=tsconfig_dev,
            tsconfig_dev_file=tsconfig_dev_file,
            ts_jest_options=ts_jest_options,
            typescript_version=typescript_version,
            versionrc_options=versionrc_options,
            vscode=vscode,
            workflow_bootstrap_steps=workflow_bootstrap_steps,
            workflow_container_image=workflow_container_image,
            workflow_git_identity=workflow_git_identity,
            workflow_node_version=workflow_node_version,
            workflow_package_cache=workflow_package_cache,
            workflow_runs_on=workflow_runs_on,
            workflow_runs_on_group=workflow_runs_on_group,
            yarn_berry_options=yarn_berry_options,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addImplicitDependency")
    def add_implicit_dependency(
        self,
        dependent: _projen_04054675.Project,
        dependee: typing.Union[builtins.str, _projen_04054675.Project],
    ) -> None:
        '''Create an implicit dependency between two Projects.

        This is typically
        used in polygot repos where a Typescript project wants a build dependency
        on a Python project as an example.

        :param dependent: -
        :param dependee: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f49e2643fb6a6e113433d8379fa180cdfdb081b793f3cb0cdeb2c5f54cfdb81)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addImplicitDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addJavaDependency")
    def add_java_dependency(
        self,
        dependent: _projen_java_04054675.JavaProject,
        dependee: _projen_java_04054675.JavaProject,
    ) -> None:
        '''Adds a dependency between two Java Projects in the monorepo.

        :param dependent: -
        :param dependee: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__587e8033cb232120a1633228165099505bb32f21d31d2ecd6bdc8079e8a30ea9)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addJavaDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addNxRunManyTask")
    def add_nx_run_many_task(
        self,
        name: builtins.str,
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
    ) -> _projen_04054675.Task:
        '''Add project task that executes ``npx nx run-many ...`` style command.

        :param name: -
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

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1b5b8e0649aced11a695b1f6bc308ba2c715409b4d356fa846a5a1bce391c1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(_projen_04054675.Task, jsii.invoke(self, "addNxRunManyTask", [name, options]))

    @jsii.member(jsii_name="addPythonPoetryDependency")
    def add_python_poetry_dependency(
        self,
        dependent: _projen_python_04054675.PythonProject,
        dependee: _projen_python_04054675.PythonProject,
    ) -> None:
        '''Adds a dependency between two Python Projects in the monorepo.

        The dependent must have Poetry enabled.

        :param dependent: -
        :param dependee: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c463ab04e7a6ec06c7487d0639443405d7f1792e5bd42c2ac18a70edd5d9c823)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addPythonPoetryDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addWorkspacePackages")
    def add_workspace_packages(self, *package_globs: builtins.str) -> None:
        '''Add one or more additional package globs to the workspace.

        :param package_globs: paths to the package to include in the workspace (for example packages/my-package).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b95f98f7a6ffd6e29650a109c377dc135f7bd57a0639f9f720e2f86a61a09cc)
            check_type(argname="argument package_globs", value=package_globs, expected_type=typing.Tuple[type_hints["package_globs"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addWorkspacePackages", [*package_globs]))

    @jsii.member(jsii_name="composeNxRunManyCommand")
    def compose_nx_run_many_command(
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
    ) -> typing.List[builtins.str]:
        '''Helper to format ``npx nx run-many ...`` style command.

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

        :inheritdoc: true
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "composeNxRunManyCommand", [options]))

    @jsii.member(jsii_name="execNxRunManyCommand")
    def exec_nx_run_many_command(
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
    ) -> builtins.str:
        '''Helper to format ``npx nx run-many ...`` style command execution in package manager.

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

        :inheritdoc: true
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "execNxRunManyCommand", [options]))

    @jsii.member(jsii_name="linkLocalWorkspaceBins")
    def _link_local_workspace_bins(self) -> None:
        '''Create symbolic links to all local workspace bins.

        This enables the usage of bins the same
        way as consumers of the packages have when installing from the registry.
        '''
        return typing.cast(None, jsii.invoke(self, "linkLocalWorkspaceBins", []))

    @jsii.member(jsii_name="postSynthesize")
    def post_synthesize(self) -> None:
        '''Called after all components are synthesized.

        Order is *not* guaranteed.

        :inheritDoc: true
        '''
        return typing.cast(None, jsii.invoke(self, "postSynthesize", []))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''Called before all components are synthesized.'''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        '''Synthesize all project files into ``outdir``.

        1. Call "this.preSynthesize()"
        2. Delete all generated files
        3. Synthesize all subprojects
        4. Synthesize all components of this project
        5. Call "postSynthesize()" for all components of this project
        6. Call "this.postSynthesize()"

        :inheritDoc: true
        '''
        return typing.cast(None, jsii.invoke(self, "synth", []))

    @builtins.property
    @jsii.member(jsii_name="nx")
    def nx(self) -> "NxWorkspace":
        '''Return the NxWorkspace instance.

        This should be implemented using a getter.

        :inheritdoc: true
        '''
        return typing.cast("NxWorkspace", jsii.get(self, "nx"))

    @builtins.property
    @jsii.member(jsii_name="nxConfigurator")
    def nx_configurator(self) -> "NxConfigurator":
        return typing.cast("NxConfigurator", jsii.get(self, "nxConfigurator"))

    @builtins.property
    @jsii.member(jsii_name="sortedSubProjects")
    def sorted_sub_projects(self) -> typing.List[_projen_04054675.Project]:
        '''Get consistently sorted list of subprojects.'''
        return typing.cast(typing.List[_projen_04054675.Project], jsii.get(self, "sortedSubProjects"))


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.MonorepoUpgradeDepsOptions",
    jsii_struct_bases=[],
    name_mapping={"syncpack_config": "syncpackConfig", "task_name": "taskName"},
)
class MonorepoUpgradeDepsOptions:
    def __init__(
        self,
        *,
        syncpack_config: typing.Optional[typing.Union[_SyncpackConfig_9a7845d7, typing.Dict[builtins.str, typing.Any]]] = None,
        task_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for Monorepo Upgrade Deps task.

        :param syncpack_config: Syncpack configuration. No merging is performed and as such a complete syncpackConfig is required if supplied. Default: Syncpack.DEFAULT_CONFIG
        :param task_name: Name of the task to create. Default: upgrade-deps
        '''
        if isinstance(syncpack_config, dict):
            syncpack_config = _SyncpackConfig_9a7845d7(**syncpack_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390b0ad8efb140cce70e5df8c9a74d9aec5812aa35f52dd45fc8cbc95cededcd)
            check_type(argname="argument syncpack_config", value=syncpack_config, expected_type=type_hints["syncpack_config"])
            check_type(argname="argument task_name", value=task_name, expected_type=type_hints["task_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if syncpack_config is not None:
            self._values["syncpack_config"] = syncpack_config
        if task_name is not None:
            self._values["task_name"] = task_name

    @builtins.property
    def syncpack_config(self) -> typing.Optional[_SyncpackConfig_9a7845d7]:
        '''Syncpack configuration.

        No merging is performed and as such a complete syncpackConfig is required if supplied.

        :default: Syncpack.DEFAULT_CONFIG
        '''
        result = self._values.get("syncpack_config")
        return typing.cast(typing.Optional[_SyncpackConfig_9a7845d7], result)

    @builtins.property
    def task_name(self) -> typing.Optional[builtins.str]:
        '''Name of the task to create.

        :default: upgrade-deps
        '''
        result = self._values.get("task_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonorepoUpgradeDepsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INxProjectCore)
class NxConfigurator(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.monorepo.NxConfigurator",
):
    '''Configues common NX related tasks and methods.'''

    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        default_release_branch: typing.Optional[builtins.str] = None,
        license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param project: -
        :param default_release_branch: Branch that NX affected should run against.
        :param license_options: Default package license config. If nothing is specified, all packages will default to Apache-2.0 (unless they have their own License component).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed97476ef032e66c8f1f7ade48175ebbb06749d0ebf5e88945694da059348811)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = NxConfiguratorOptions(
            default_release_branch=default_release_branch,
            license_options=license_options,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addImplicitDependency")
    def add_implicit_dependency(
        self,
        dependent: _projen_04054675.Project,
        dependee: typing.Union[builtins.str, _projen_04054675.Project],
    ) -> None:
        '''Create an implicit dependency between two Projects.

        This is typically
        used in polygot repos where a Typescript project wants a build dependency
        on a Python project as an example.

        :param dependent: project you want to have the dependency.
        :param dependee: project you wish to depend on.

        :throws: error if this is called on a dependent which does not have a NXProject component attached.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44572c825aad4ac4e8118dff282e1942ba8aa1d9791852aae1ca46eb5d92710)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addImplicitDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addJavaDependency")
    def add_java_dependency(
        self,
        dependent: _projen_java_04054675.JavaProject,
        dependee: _projen_java_04054675.JavaProject,
    ) -> None:
        '''Adds a dependency between two Java Projects in the monorepo.

        :param dependent: project you want to have the dependency.
        :param dependee: project you wish to depend on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a0c582c7d2cfd66500b537a5cb0d287914102a80a6ef7f3268e2e6dc12e6d1)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addJavaDependency", [dependent, dependee]))

    @jsii.member(jsii_name="addNxRunManyTask")
    def add_nx_run_many_task(
        self,
        name: builtins.str,
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
    ) -> _projen_04054675.Task:
        '''Add project task that executes ``npx nx run-many ...`` style command.

        :param name: -
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
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4108c14007a7e79adfc367f7a8b55b09914490f0608987bb9585099775e10597)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(_projen_04054675.Task, jsii.invoke(self, "addNxRunManyTask", [name, options]))

    @jsii.member(jsii_name="addPythonPoetryDependency")
    def add_python_poetry_dependency(
        self,
        dependent: _projen_python_04054675.PythonProject,
        dependee: _projen_python_04054675.PythonProject,
    ) -> None:
        '''Adds a dependency between two Python Projects in the monorepo.

        The dependent must have Poetry enabled.

        :param dependent: project you want to have the dependency (must be a Poetry Python Project).
        :param dependee: project you wish to depend on.

        :throws: error if the dependent does not have Poetry enabled
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604e9c9a16fff068e5abd17ce8ba57f3807cf6e12bda0e6812589bbd2574cb37)
            check_type(argname="argument dependent", value=dependent, expected_type=type_hints["dependent"])
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addPythonPoetryDependency", [dependent, dependee]))

    @jsii.member(jsii_name="composeNxRunManyCommand")
    def compose_nx_run_many_command(
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
    ) -> typing.List[builtins.str]:
        '''Helper to format ``npx nx run-many ...`` style command.

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
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "composeNxRunManyCommand", [options]))

    @jsii.member(jsii_name="ensureNxInstallTask")
    def ensure_nx_install_task(
        self,
        nx_plugins: typing.Mapping[builtins.str, builtins.str],
    ) -> _projen_04054675.Task:
        '''Returns the install task or creates one with nx installation command added.

        Note: this should only be called from non-node projects

        :param nx_plugins: additional plugins to install.

        :return: install task
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f753c02716795922069d0101ef32fde087d3562a0ff1c5abbba92d300d72d77d)
            check_type(argname="argument nx_plugins", value=nx_plugins, expected_type=type_hints["nx_plugins"])
        return typing.cast(_projen_04054675.Task, jsii.invoke(self, "ensureNxInstallTask", [nx_plugins]))

    @jsii.member(jsii_name="execNxRunManyCommand")
    def exec_nx_run_many_command(
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
    ) -> builtins.str:
        '''Helper to format ``npx nx run-many ...`` style command execution in package manager.

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
        '''
        options = _RunManyOptions_f0e930ea(
            target=target,
            configuration=configuration,
            exclude=exclude,
            ignore_cycles=ignore_cycles,
            no_bail=no_bail,
            output_style=output_style,
            parallel=parallel,
            projects=projects,
            runner=runner,
            skip_cache=skip_cache,
            verbose=verbose,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "execNxRunManyCommand", [options]))

    @jsii.member(jsii_name="patchPoetryEnv")
    def patch_poetry_env(self, project: _projen_python_04054675.PythonProject) -> None:
        '''
        :param project: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41cdd8e56554c5bf2880bef86a2d8e3b6b1748bc19b96dce2a6b7bb3bebf765)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast(None, jsii.invoke(self, "patchPoetryEnv", [project]))

    @jsii.member(jsii_name="patchPythonProjects")
    def patch_python_projects(
        self,
        projects: typing.Sequence[_projen_04054675.Project],
    ) -> None:
        '''
        :param projects: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908936f24e27696f73dca58c8f0b5a868023a700925f4d2b30e8a22a06c80a54)
            check_type(argname="argument projects", value=projects, expected_type=type_hints["projects"])
        return typing.cast(None, jsii.invoke(self, "patchPythonProjects", [projects]))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''Called before synthesis.'''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        '''
        :inheritDoc: true
        '''
        return typing.cast(None, jsii.invoke(self, "synth", []))

    @builtins.property
    @jsii.member(jsii_name="nx")
    def nx(self) -> "NxWorkspace":
        '''Return the NxWorkspace instance.

        This should be implemented using a getter.
        '''
        return typing.cast("NxWorkspace", jsii.get(self, "nx"))


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.NxConfiguratorOptions",
    jsii_struct_bases=[],
    name_mapping={
        "default_release_branch": "defaultReleaseBranch",
        "license_options": "licenseOptions",
    },
)
class NxConfiguratorOptions:
    def __init__(
        self,
        *,
        default_release_branch: typing.Optional[builtins.str] = None,
        license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''NXConfigurator options.

        :param default_release_branch: Branch that NX affected should run against.
        :param license_options: Default package license config. If nothing is specified, all packages will default to Apache-2.0 (unless they have their own License component).
        '''
        if isinstance(license_options, dict):
            license_options = LicenseOptions(**license_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50950bf833fa298e21fe264d1d1b4bb04ced38d0e70d57190d06e13137f1f35a)
            check_type(argname="argument default_release_branch", value=default_release_branch, expected_type=type_hints["default_release_branch"])
            check_type(argname="argument license_options", value=license_options, expected_type=type_hints["license_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_release_branch is not None:
            self._values["default_release_branch"] = default_release_branch
        if license_options is not None:
            self._values["license_options"] = license_options

    @builtins.property
    def default_release_branch(self) -> typing.Optional[builtins.str]:
        '''Branch that NX affected should run against.'''
        result = self._values.get("default_release_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_options(self) -> typing.Optional[LicenseOptions]:
        '''Default package license config.

        If nothing is specified, all packages will default to Apache-2.0 (unless they have their own License component).
        '''
        result = self._values.get("license_options")
        return typing.cast(typing.Optional[LicenseOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NxConfiguratorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NxProject(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.monorepo.NxProject",
):
    '''(experimental) Component which manages the project specific NX Config and is added to all NXMonorepo subprojects.

    :stability: experimental
    '''

    def __init__(self, project: _projen_04054675.Project) -> None:
        '''
        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30366b89fa356cef1088329b5c0c6a1f2f3e674384574b5150983c2b20eb7283)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        jsii.create(self.__class__, self, [project])

    @jsii.member(jsii_name="ensure")
    @builtins.classmethod
    def ensure(cls, project: _projen_04054675.Project) -> "NxProject":
        '''(experimental) Retrieves an instance of NXProject if one is associated to the given project, otherwise created a NXProject instance for the project.

        :param project: project instance.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68513bdb1fb452405f6d9f95bcf81604c365d0abc3a3a4fe7378a36980b69d4d)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast("NxProject", jsii.sinvoke(cls, "ensure", [project]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, project: _projen_04054675.Project) -> typing.Optional["NxProject"]:
        '''(experimental) Retrieves an instance of NXProject if one is associated to the given project.

        :param project: project instance.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8577e9bef1e574cf8576f2a57b1728567ff89778f21ba4b68b9592063d7461)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast(typing.Optional["NxProject"], jsii.sinvoke(cls, "of", [project]))

    @jsii.member(jsii_name="addBuildTargetFiles")
    def add_build_target_files(
        self,
        inputs: typing.Optional[typing.Sequence[typing.Union[builtins.str, _IInput_534968b7]]] = None,
        outputs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Add input and output files to build target.

        :param inputs: Input files.
        :param outputs: Output files.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aad1e6d4ec0e879610ac5c5ede31cce5555f4d78b294ac87e7783c34ca6729d)
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
        return typing.cast(None, jsii.invoke(self, "addBuildTargetFiles", [inputs, outputs]))

    @jsii.member(jsii_name="addImplicitDependency")
    def add_implicit_dependency(
        self,
        *dependee: typing.Union[builtins.str, _projen_04054675.Project],
    ) -> None:
        '''(experimental) Adds an implicit dependency between the dependant (this project) and dependee.

        :param dependee: project to add the implicit dependency on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46a28aab116cd2273c3fb4bbb74c5f585f1edd073fd1f0b1efe223f1484317e)
            check_type(argname="argument dependee", value=dependee, expected_type=typing.Tuple[type_hints["dependee"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addImplicitDependency", [*dependee]))

    @jsii.member(jsii_name="addJavaDependency")
    def add_java_dependency(self, dependee: _projen_java_04054675.JavaProject) -> None:
        '''(experimental) Adds a dependency between two Java Projects in the monorepo.

        :param dependee: project you wish to depend on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5423fe6bc91d6737402b53c8d859130edbe0e82998bfb339ec9f7b0c12e0e5c)
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addJavaDependency", [dependee]))

    @jsii.member(jsii_name="addPythonPoetryDependency")
    def add_python_poetry_dependency(
        self,
        dependee: _projen_python_04054675.PythonProject,
    ) -> None:
        '''(experimental) Adds a dependency between two Python Projects in the monorepo.

        The dependent must have Poetry enabled.

        :param dependee: project you wish to depend on.

        :stability: experimental
        :throws: error if the dependent does not have Poetry enabled
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a8d5b45a6a468d432d8123028e6ea2c55ea1cdeb927fee35edea8b28a28f99)
            check_type(argname="argument dependee", value=dependee, expected_type=type_hints["dependee"])
        return typing.cast(None, jsii.invoke(self, "addPythonPoetryDependency", [dependee]))

    @jsii.member(jsii_name="addTag")
    def add_tag(self, *tags: builtins.str) -> None:
        '''(experimental) Add tag.

        :param tags: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d82461f56f01fff7e9c3fb53766cef8a655d75c33d2d824810eae12053df898)
            check_type(argname="argument tags", value=tags, expected_type=typing.Tuple[type_hints["tags"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addTag", [*tags]))

    @jsii.member(jsii_name="inferTargets")
    def infer_targets(self) -> None:
        '''(experimental) Automatically infer targets based on project type.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inferTargets", []))

    @jsii.member(jsii_name="merge")
    def merge(
        self,
        *,
        implicit_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        named_inputs: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        root: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        targets: typing.Optional[typing.Mapping[builtins.str, _IProjectTarget_184fbc33]] = None,
    ) -> None:
        '''(experimental) Merge configuration into existing config.

        :param implicit_dependencies: Implicit dependencies.
        :param included_scripts: Explicit list of scripts for Nx to include.
        :param name: Name of project.
        :param named_inputs: Named inputs.
        :param root: Project root dir path relative to workspace.
        :param tags: Project tag annotations.
        :param targets: Targets configuration.

        :stability: experimental
        '''
        config = _ProjectConfig_68a5168c(
            implicit_dependencies=implicit_dependencies,
            included_scripts=included_scripts,
            name=name,
            named_inputs=named_inputs,
            root=root,
            tags=tags,
            targets=targets,
        )

        return typing.cast(None, jsii.invoke(self, "merge", [config]))

    @jsii.member(jsii_name="setNamedInput")
    def set_named_input(
        self,
        name: builtins.str,
        inputs: typing.Sequence[builtins.str],
    ) -> None:
        '''(experimental) Set ``namedInputs`` helper.

        :param name: -
        :param inputs: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3ef7a57a97cc41beefab833fb4a8e43590ffdb00d966f84a9a39e82e8be96f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
        return typing.cast(None, jsii.invoke(self, "setNamedInput", [name, inputs]))

    @jsii.member(jsii_name="setTarget")
    def set_target(
        self,
        name: builtins.str,
        target: _IProjectTarget_184fbc33,
        include_defaults: typing.Optional[typing.Union[builtins.str, builtins.bool]] = None,
    ) -> None:
        '''(experimental) Set ``targets`` helper.

        :param name: -
        :param target: -
        :param include_defaults: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee830648fb433c27179f69b5e9b4018341cfa6bcffd1fe11d399b4879a4dbb52)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument include_defaults", value=include_defaults, expected_type=type_hints["include_defaults"])
        return typing.cast(None, jsii.invoke(self, "setTarget", [name, target, include_defaults]))

    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> None:
        '''(experimental) Synthesizes files to the project output directory.

        :stability: experimental
        :interface: true
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", []))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> _projen_04054675.JsonFile:
        '''(experimental) Raw json file.

        **Attention:** any overrides applied here will not be visible
        in the properties and only included in final synthesized output,
        and likely to override native handling.

        :stability: experimental
        :advanced: true
        '''
        return typing.cast(_projen_04054675.JsonFile, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="implicitDependencies")
    def implicit_dependencies(self) -> typing.List[builtins.str]:
        '''(experimental) Implicit dependencies.

        :see: https://nx.dev/reference/project-configuration#implicitdependencies
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "implicitDependencies"))

    @implicit_dependencies.setter
    def implicit_dependencies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__521e1d57d19197ff9932b7cbb0d3f8ad65c6f1a3fe4ee5be040a6fd02e27507c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "implicitDependencies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedScripts")
    def included_scripts(self) -> typing.List[builtins.str]:
        '''(experimental) Explicit list of scripts for Nx to include.

        :see: https://nx.dev/reference/project-configuration#ignoring-package.json-scripts
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedScripts"))

    @included_scripts.setter
    def included_scripts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3921b3c5d8fb8c7534254d3f7c6573f2ae66663bcea2bbd47e9b9d530dfa450b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedScripts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namedInputs")
    def named_inputs(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Named inputs.

        :see: https://nx.dev/reference/nx-json#inputs-&-namedinputs
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "namedInputs"))

    @named_inputs.setter
    def named_inputs(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c586a10031c8b671142a6bc8dc1d7e01d95f371904d5fdf7ee4bb22cb220beb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namedInputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        '''(experimental) Project tag annotations.

        :see: https://nx.dev/reference/project-configuration#tags
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11991d92880e09cad77e85bc1d0ab510767e1d3c7eff2d101478fc53d97148ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Targets configuration.

        :see: https://nx.dev/reference/project-configuration
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "targets"))

    @targets.setter
    def targets(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df666c2903109c294a10bae5f5b40da1eec0b2b2d40b72a3a209bf6bc599516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targets", value) # pyright: ignore[reportArgumentType]


class NxWorkspace(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.monorepo.NxWorkspace",
):
    '''(experimental) Component which manages the workspace specific NX Config for the root monorepo.

    :stability: experimental
    '''

    def __init__(self, project: _projen_04054675.Project) -> None:
        '''
        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250320810381bea13f650f8c6f9f01fa648ee521ead1bc8938c9476f9f4a6721)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        jsii.create(self.__class__, self, [project])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, scope: _projen_04054675.Project) -> typing.Optional["NxWorkspace"]:
        '''(experimental) Retrieves the singleton instance associated with project root.

        :param scope: project instance.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__064f95290b0f6b4cae88e9826662904872e694faf9474327ac6a207c88011fdf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.Optional["NxWorkspace"], jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''(experimental) Called before synthesis.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.member(jsii_name="setNamedInput")
    def set_named_input(
        self,
        name: builtins.str,
        inputs: typing.Sequence[builtins.str],
    ) -> None:
        '''(experimental) Set ``namedInput`` value helper.

        :param name: -
        :param inputs: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5eb856c65a0556913799999bf6028bc7aca48d46fa4de8eef5360c80edce220)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
        return typing.cast(None, jsii.invoke(self, "setNamedInput", [name, inputs]))

    @jsii.member(jsii_name="setTargetDefault")
    def set_target_default(
        self,
        name: builtins.str,
        target: _IProjectTarget_184fbc33,
        merge: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Set ``targetDefaults`` helper.

        :param name: -
        :param target: -
        :param merge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3dc483725d5b9f059f8bf44f1751d403efb32be822822ee6f139a0ad701d181)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument merge", value=merge, expected_type=type_hints["merge"])
        return typing.cast(None, jsii.invoke(self, "setTargetDefault", [name, target, merge]))

    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> None:
        '''(experimental) Synthesizes files to the project output directory.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", []))

    @jsii.member(jsii_name="useNxCloud")
    def use_nx_cloud(self, read_only_access_token: builtins.str) -> None:
        '''(experimental) Setup workspace to use nx-cloud.

        :param read_only_access_token: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f44402e5722b71268d11def844203c58a812944e360f7871eef5f4f94b29fc)
            check_type(argname="argument read_only_access_token", value=read_only_access_token, expected_type=type_hints["read_only_access_token"])
        return typing.cast(None, jsii.invoke(self, "useNxCloud", [read_only_access_token]))

    @builtins.property
    @jsii.member(jsii_name="nxIgnore")
    def nx_ignore(self) -> _projen_04054675.IgnoreFile:
        '''(experimental) .nxignore file.

        :stability: experimental
        '''
        return typing.cast(_projen_04054675.IgnoreFile, jsii.get(self, "nxIgnore"))

    @builtins.property
    @jsii.member(jsii_name="nxJson")
    def nx_json(self) -> _projen_04054675.JsonFile:
        '''(experimental) Raw nx.json file to support overrides that aren't handled directly.

        **Attention:** any overrides applied here will not be visible
        in the properties and only included in final synthesized output,
        and likely to override native handling.

        :stability: experimental
        :advanced: true
        '''
        return typing.cast(_projen_04054675.JsonFile, jsii.get(self, "nxJson"))

    @builtins.property
    @jsii.member(jsii_name="affected")
    def affected(self) -> _INxAffectedConfig_1a5bb1a8:
        '''(experimental) Default options for ``nx affected``.

        :stability: experimental
        '''
        return typing.cast(_INxAffectedConfig_1a5bb1a8, jsii.get(self, "affected"))

    @affected.setter
    def affected(self, value: _INxAffectedConfig_1a5bb1a8) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e54016533c964b96af2a7b8bf071f49b3c089cb3d855dbc51610ab1d0ac6ab00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "affected", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoInferProjectTargets")
    def auto_infer_project_targets(self) -> builtins.bool:
        '''(experimental) Automatically infer NxProject targets based on project type.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoInferProjectTargets"))

    @auto_infer_project_targets.setter
    def auto_infer_project_targets(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b038cb7d50d63894109da223dd2be8afe54c04d86d75602e7bd5ff00849a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoInferProjectTargets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheableOperations")
    def cacheable_operations(self) -> typing.List[builtins.str]:
        '''(experimental) List of cacheable operations.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cacheableOperations"))

    @cacheable_operations.setter
    def cacheable_operations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e976737e7f0db4a1d471c9d5b1855bb11e1cad1f9d421b29f887b7fef79fa7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheableOperations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTaskRunner")
    def default_task_runner(self) -> builtins.str:
        '''(experimental) Default task runner.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "defaultTaskRunner"))

    @default_task_runner.setter
    def default_task_runner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bac317426eae1f61a1ba6a1e6c66459b3a9baf6cf42b408d71a1912de53dabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTaskRunner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTaskRunnerOptions")
    def default_task_runner_options(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Default task runner options.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "defaultTaskRunnerOptions"))

    @default_task_runner_options.setter
    def default_task_runner_options(
        self,
        value: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cfd26bb5bdea0e58e11387d6df1f04ed49b58a9b857c3fe7aeaded9d3465a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTaskRunnerOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extends")
    def extends(self) -> builtins.str:
        '''(experimental) Some presets use the extends property to hide some default options in a separate json file.

        The json file specified in the extends property is located in your node_modules folder.
        The Nx preset files are specified in the nx package.

        :default: "nx/presets/npm.json"

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "extends"))

    @extends.setter
    def extends(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378acf007bb83eafc4c015ebd56148e9dea19a74b354e37c86cd55e0de9381e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extends", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namedInputs")
    def named_inputs(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''(experimental) Named inputs.

        :see: https://nx.dev/reference/nx-json#inputs-&-namedinputs
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.get(self, "namedInputs"))

    @named_inputs.setter
    def named_inputs(
        self,
        value: typing.Mapping[builtins.str, typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75325b7fa3abd85be92f4989a7916a9eda1bfabd263503e4f7abd28b49ae4a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namedInputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonNativeHasher")
    def non_native_hasher(self) -> builtins.bool:
        '''(experimental) Indicates if non-native nx hasher will be used.

        If true, the NX_NON_NATIVE_HASHER env var will be set
        to true for all project tasks.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "nonNativeHasher"))

    @non_native_hasher.setter
    def non_native_hasher(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c472f77cac71dd224f94cc3986df1bc2a615fb92cc14ca465d92280db9046993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonNativeHasher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="npmScope")
    def npm_scope(self) -> builtins.str:
        '''(experimental) Tells Nx what prefix to use when generating library imports.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "npmScope"))

    @npm_scope.setter
    def npm_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4aac2c6d47cc61b849934cf500d4f16438fb2e777fb3713219e2f97c6961212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "npmScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="plugins")
    def plugins(self) -> typing.List[builtins.str]:
        '''(experimental) Plugins for extending the project graph.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "plugins"))

    @plugins.setter
    def plugins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff3c185bc8e64404880e59de3dc657fa70213a6a2bfea00a74ea72044afdc93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plugins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginsConfig")
    def plugins_config(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Configuration for Nx Plugins.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "pluginsConfig"))

    @plugins_config.setter
    def plugins_config(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa837bf24c35c1fa31f1b7fd7f8aea9c91b2d274052e1eea6537c3c75ee6215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginsConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDefaults")
    def target_defaults(self) -> typing.Mapping[builtins.str, _IProjectTarget_184fbc33]:
        '''(experimental) Dependencies between different target names across all projects.

        :see: https://nx.dev/reference/nx-json#target-defaults
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, _IProjectTarget_184fbc33], jsii.get(self, "targetDefaults"))

    @target_defaults.setter
    def target_defaults(
        self,
        value: typing.Mapping[builtins.str, _IProjectTarget_184fbc33],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5cc18c3c7ffba2551af8a12b054360893e77b5599b4a93cdaa1e61a1330e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDefaults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tasksRunnerOptions")
    def tasks_runner_options(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Task runner options.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "tasksRunnerOptions"))

    @tasks_runner_options.setter
    def tasks_runner_options(
        self,
        value: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da6ba6112c3ca1a750676caab4f0662dc60225c78861f53b73f89a639f89793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tasksRunnerOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheDirectory")
    def cache_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Override the default nx cacheDirectory.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheDirectory"))

    @cache_directory.setter
    def cache_directory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d06e29986d52b7f0721c57b558ba202ba1133ceaabf1bfb61c7ce380417a0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceLayout")
    def workspace_layout(self) -> typing.Optional[_IWorkspaceLayout_a55c7d5d]:
        '''(experimental) Where new apps + libs should be placed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IWorkspaceLayout_a55c7d5d], jsii.get(self, "workspaceLayout"))

    @workspace_layout.setter
    def workspace_layout(
        self,
        value: typing.Optional[_IWorkspaceLayout_a55c7d5d],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9764b0d2301aef01e8a7ed83b46e43cd406eb0878be317b9c6a68c66803d12a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceLayout", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.PythonProjectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "module_name": "moduleName",
        "name": "name",
        "author_email": "authorEmail",
        "author_name": "authorName",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "classifiers": "classifiers",
        "clobber": "clobber",
        "commit_generated": "commitGenerated",
        "deps": "deps",
        "description": "description",
        "dev_container": "devContainer",
        "dev_deps": "devDeps",
        "github": "github",
        "github_options": "githubOptions",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "gitpod": "gitpod",
        "homepage": "homepage",
        "license": "license",
        "logging": "logging",
        "mergify": "mergify",
        "mergify_options": "mergifyOptions",
        "outdir": "outdir",
        "package_name": "packageName",
        "parent": "parent",
        "poetry_options": "poetryOptions",
        "project_type": "projectType",
        "projen_command": "projenCommand",
        "projen_credentials": "projenCredentials",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "projenrc_python_options": "projenrcPythonOptions",
        "projen_token_secret": "projenTokenSecret",
        "pytest": "pytest",
        "pytest_options": "pytestOptions",
        "python_exec": "pythonExec",
        "readme": "readme",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "sample": "sample",
        "setup_config": "setupConfig",
        "setuptools": "setuptools",
        "stale": "stale",
        "stale_options": "staleOptions",
        "version": "version",
        "vscode": "vscode",
    },
)
class PythonProjectOptions:
    def __init__(
        self,
        *,
        module_name: builtins.str,
        name: builtins.str,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        package_name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        poetry_options: typing.Optional[typing.Union[_projen_python_04054675.PoetryPyprojectOptionsWithoutDeps, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_projen_04054675.ProjectType] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_python_options: typing.Optional[typing.Union[_projen_python_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        pytest: typing.Optional[builtins.bool] = None,
        pytest_options: typing.Optional[typing.Union[_projen_python_04054675.PytestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        python_exec: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        sample: typing.Optional[builtins.bool] = None,
        setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        setuptools: typing.Optional[builtins.bool] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''PythonProjectOptions.

        :param module_name: Default: $PYTHON_MODULE_NAME
        :param name: Default: $BASEDIR
        :param author_email: (experimental) Author's e-mail. Default: $GIT_USER_EMAIL
        :param author_name: (experimental) Author's name. Default: $GIT_USER_NAME
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param classifiers: (experimental) A list of PyPI trove classifiers that describe the project.
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) A short description of the package.
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param dev_deps: (experimental) List of dev dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDevDependency()``. Default: []
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param homepage: (experimental) A URL to the website of the project.
        :param license: (experimental) License of this package as an SPDX identifier.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param package_name: (experimental) Package name.
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param poetry_options: (experimental) Additional options to set for poetry if using poetry.
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param projenrc_python_options: (experimental) Options related to projenrc in python. Default: - default options
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param pytest: (experimental) Include pytest tests. Default: true
        :param pytest_options: (experimental) pytest options. Default: - defaults
        :param python_exec: (experimental) Path to the python executable to use. Default: "python"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param setup_config: (experimental) Additional fields to pass in the setup() function if using setuptools.
        :param setuptools: (experimental) Use setuptools with a setup.py script for packaging and publishing. Default: - true, unless poetry is true, then false
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param version: (experimental) Version of the package. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        '''
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _projen_github_04054675.AutoApproveOptions(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _projen_github_04054675.AutoMergeOptions(**auto_merge_options)
        if isinstance(github_options, dict):
            github_options = _projen_github_04054675.GitHubOptions(**github_options)
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _projen_04054675.IgnoreFileOptions(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _projen_04054675.GitOptions(**git_options)
        if isinstance(logging, dict):
            logging = _projen_04054675.LoggerOptions(**logging)
        if isinstance(mergify_options, dict):
            mergify_options = _projen_github_04054675.MergifyOptions(**mergify_options)
        if isinstance(poetry_options, dict):
            poetry_options = _projen_python_04054675.PoetryPyprojectOptionsWithoutDeps(**poetry_options)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _projen_04054675.ProjenrcJsonOptions(**projenrc_json_options)
        if isinstance(projenrc_python_options, dict):
            projenrc_python_options = _projen_python_04054675.ProjenrcOptions(**projenrc_python_options)
        if isinstance(pytest_options, dict):
            pytest_options = _projen_python_04054675.PytestOptions(**pytest_options)
        if isinstance(readme, dict):
            readme = _projen_04054675.SampleReadmeProps(**readme)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _projen_04054675.RenovatebotOptions(**renovatebot_options)
        if isinstance(stale_options, dict):
            stale_options = _projen_github_04054675.StaleOptions(**stale_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d87ff8ff85bcdc19da74931d63e3c517add273af9807c138f0ca06c07a1dbd)
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument mergify", value=mergify, expected_type=type_hints["mergify"])
            check_type(argname="argument mergify_options", value=mergify_options, expected_type=type_hints["mergify_options"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument poetry_options", value=poetry_options, expected_type=type_hints["poetry_options"])
            check_type(argname="argument project_type", value=project_type, expected_type=type_hints["project_type"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument projenrc_python_options", value=projenrc_python_options, expected_type=type_hints["projenrc_python_options"])
            check_type(argname="argument projen_token_secret", value=projen_token_secret, expected_type=type_hints["projen_token_secret"])
            check_type(argname="argument pytest", value=pytest, expected_type=type_hints["pytest"])
            check_type(argname="argument pytest_options", value=pytest_options, expected_type=type_hints["pytest_options"])
            check_type(argname="argument python_exec", value=python_exec, expected_type=type_hints["python_exec"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument setup_config", value=setup_config, expected_type=type_hints["setup_config"])
            check_type(argname="argument setuptools", value=setuptools, expected_type=type_hints["setuptools"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "module_name": module_name,
            "name": name,
        }
        if author_email is not None:
            self._values["author_email"] = author_email
        if author_name is not None:
            self._values["author_name"] = author_name
        if auto_approve_options is not None:
            self._values["auto_approve_options"] = auto_approve_options
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if auto_merge_options is not None:
            self._values["auto_merge_options"] = auto_merge_options
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if clobber is not None:
            self._values["clobber"] = clobber
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if github is not None:
            self._values["github"] = github
        if github_options is not None:
            self._values["github_options"] = github_options
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if gitpod is not None:
            self._values["gitpod"] = gitpod
        if homepage is not None:
            self._values["homepage"] = homepage
        if license is not None:
            self._values["license"] = license
        if logging is not None:
            self._values["logging"] = logging
        if mergify is not None:
            self._values["mergify"] = mergify
        if mergify_options is not None:
            self._values["mergify_options"] = mergify_options
        if outdir is not None:
            self._values["outdir"] = outdir
        if package_name is not None:
            self._values["package_name"] = package_name
        if parent is not None:
            self._values["parent"] = parent
        if poetry_options is not None:
            self._values["poetry_options"] = poetry_options
        if project_type is not None:
            self._values["project_type"] = project_type
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if projenrc_python_options is not None:
            self._values["projenrc_python_options"] = projenrc_python_options
        if projen_token_secret is not None:
            self._values["projen_token_secret"] = projen_token_secret
        if pytest is not None:
            self._values["pytest"] = pytest
        if pytest_options is not None:
            self._values["pytest_options"] = pytest_options
        if python_exec is not None:
            self._values["python_exec"] = python_exec
        if readme is not None:
            self._values["readme"] = readme
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if sample is not None:
            self._values["sample"] = sample
        if setup_config is not None:
            self._values["setup_config"] = setup_config
        if setuptools is not None:
            self._values["setuptools"] = setuptools
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if version is not None:
            self._values["version"] = version
        if vscode is not None:
            self._values["vscode"] = vscode

    @builtins.property
    def module_name(self) -> builtins.str:
        '''
        :default: $PYTHON_MODULE_NAME
        '''
        result = self._values.get("module_name")
        assert result is not None, "Required property 'module_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :default: $BASEDIR
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def author_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's e-mail.

        :default: $GIT_USER_EMAIL

        :stability: experimental
        '''
        result = self._values.get("author_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's name.

        :default: $GIT_USER_NAME

        :stability: experimental
        '''
        result = self._values.get("author_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_approve_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoApproveOptions]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoApproveOptions], result)

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable automatic merging on GitHub.

        Has no effect if ``github.mergify``
        is set to false.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoMergeOptions]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoMergeOptions], result)

    @builtins.property
    def classifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of PyPI trove classifiers that describe the project.

        :stability: experimental
        '''
        result = self._values.get("classifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def clobber(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a ``clobber`` task which resets the repo to origin.

        :default: - true, but false for subprojects

        :stability: experimental
        '''
        result = self._values.get("clobber")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of runtime dependencies for this project. Dependencies use the format: ``<module>@<semver>``.

        Additional dependencies can be added via ``project.addDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A short description of the package.

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dev_container(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a VSCode development environment (used for GitHub Codespaces).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dev_container")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dev_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of dev dependencies for this project. Dependencies use the format: ``<module>@<semver>``.

        Additional dependencies can be added via ``project.addDevDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("dev_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def github(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable GitHub integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github_options(self) -> typing.Optional[_projen_github_04054675.GitHubOptions]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional[_projen_github_04054675.GitHubOptions], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_projen_04054675.IgnoreFileOptions]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_projen_04054675.IgnoreFileOptions], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_projen_04054675.GitOptions]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_projen_04054675.GitOptions], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''(experimental) A URL to the website of the project.

        :stability: experimental
        '''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''(experimental) License of this package as an SPDX identifier.

        :stability: experimental
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(self) -> typing.Optional[_projen_04054675.LoggerOptions]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_projen_04054675.LoggerOptions], result)

    @builtins.property
    def mergify(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether mergify should be enabled on this repository or not.

        :default: true

        :deprecated: use ``githubOptions.mergify`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.MergifyOptions]:
        '''(deprecated) Options for mergify.

        :default: - default options

        :deprecated: use ``githubOptions.mergifyOptions`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify_options")
        return typing.cast(typing.Optional[_projen_github_04054675.MergifyOptions], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project. Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package name.

        :stability: experimental
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[_projen_04054675.Project]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_projen_04054675.Project], result)

    @builtins.property
    def poetry_options(
        self,
    ) -> typing.Optional[_projen_python_04054675.PoetryPyprojectOptionsWithoutDeps]:
        '''(experimental) Additional options to set for poetry if using poetry.

        :stability: experimental
        '''
        result = self._values.get("poetry_options")
        return typing.cast(typing.Optional[_projen_python_04054675.PoetryPyprojectOptionsWithoutDeps], result)

    @builtins.property
    def project_type(self) -> typing.Optional[_projen_04054675.ProjectType]:
        '''(deprecated) Which type of project this is (library/app).

        :default: ProjectType.UNKNOWN

        :deprecated: no longer supported at the base project level

        :stability: deprecated
        '''
        result = self._values.get("project_type")
        return typing.cast(typing.Optional[_projen_04054675.ProjectType], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projen_credentials(
        self,
    ) -> typing.Optional[_projen_github_04054675.GithubCredentials]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_projen_github_04054675.GithubCredentials], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(
        self,
    ) -> typing.Optional[_projen_04054675.ProjenrcJsonOptions]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_projen_04054675.ProjenrcJsonOptions], result)

    @builtins.property
    def projenrc_python_options(
        self,
    ) -> typing.Optional[_projen_python_04054675.ProjenrcOptions]:
        '''(experimental) Options related to projenrc in python.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_python_options")
        return typing.cast(typing.Optional[_projen_python_04054675.ProjenrcOptions], result)

    @builtins.property
    def projen_token_secret(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows.

        This token needs to have the ``repo``, ``workflows``
        and ``packages`` scope.

        :default: "PROJEN_GITHUB_TOKEN"

        :deprecated: use ``projenCredentials``

        :stability: deprecated
        '''
        result = self._values.get("projen_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pytest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include pytest tests.

        :default: true

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("pytest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pytest_options(self) -> typing.Optional[_projen_python_04054675.PytestOptions]:
        '''(experimental) pytest options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("pytest_options")
        return typing.cast(typing.Optional[_projen_python_04054675.PytestOptions], result)

    @builtins.property
    def python_exec(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the python executable to use.

        :default: "python"

        :stability: experimental
        '''
        result = self._values.get("python_exec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme(self) -> typing.Optional[_projen_04054675.SampleReadmeProps]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[_projen_04054675.SampleReadmeProps], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(
        self,
    ) -> typing.Optional[_projen_04054675.RenovatebotOptions]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_projen_04054675.RenovatebotOptions], result)

    @builtins.property
    def sample(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include sample code and test if the relevant directories don't exist.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sample")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def setup_config(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional fields to pass in the setup() function if using setuptools.

        :stability: experimental
        '''
        result = self._values.get("setup_config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def setuptools(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use setuptools with a setup.py script for packaging and publishing.

        :default: - true, unless poetry is true, then false

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("setuptools")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Auto-close of stale issues and pull request.

        See ``staleOptions`` for options.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stale")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale_options(self) -> typing.Optional[_projen_github_04054675.StaleOptions]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional[_projen_github_04054675.StaleOptions], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of the package.

        :default: "0.1.0"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vscode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable VSCode integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("vscode")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.TypeScriptProjectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_library_dependencies": "allowLibraryDependencies",
        "artifacts_directory": "artifactsDirectory",
        "author_email": "authorEmail",
        "author_name": "authorName",
        "author_organization": "authorOrganization",
        "author_url": "authorUrl",
        "auto_approve_options": "autoApproveOptions",
        "auto_approve_upgrades": "autoApproveUpgrades",
        "auto_detect_bin": "autoDetectBin",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "bin": "bin",
        "bugs_email": "bugsEmail",
        "bugs_url": "bugsUrl",
        "build_workflow": "buildWorkflow",
        "build_workflow_options": "buildWorkflowOptions",
        "build_workflow_triggers": "buildWorkflowTriggers",
        "bundled_deps": "bundledDeps",
        "bundler_options": "bundlerOptions",
        "check_licenses": "checkLicenses",
        "clobber": "clobber",
        "code_artifact_options": "codeArtifactOptions",
        "code_cov": "codeCov",
        "code_cov_token_secret": "codeCovTokenSecret",
        "commit_generated": "commitGenerated",
        "copyright_owner": "copyrightOwner",
        "copyright_period": "copyrightPeriod",
        "default_release_branch": "defaultReleaseBranch",
        "dependabot": "dependabot",
        "dependabot_options": "dependabotOptions",
        "deps": "deps",
        "deps_upgrade": "depsUpgrade",
        "deps_upgrade_options": "depsUpgradeOptions",
        "description": "description",
        "dev_container": "devContainer",
        "dev_deps": "devDeps",
        "disable_tsconfig": "disableTsconfig",
        "disable_tsconfig_dev": "disableTsconfigDev",
        "docgen": "docgen",
        "docs_directory": "docsDirectory",
        "entrypoint": "entrypoint",
        "entrypoint_types": "entrypointTypes",
        "eslint": "eslint",
        "eslint_options": "eslintOptions",
        "github": "github",
        "github_options": "githubOptions",
        "gitignore": "gitignore",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "gitpod": "gitpod",
        "homepage": "homepage",
        "jest": "jest",
        "jest_options": "jestOptions",
        "jsii_release_version": "jsiiReleaseVersion",
        "keywords": "keywords",
        "libdir": "libdir",
        "license": "license",
        "licensed": "licensed",
        "logging": "logging",
        "major_version": "majorVersion",
        "max_node_version": "maxNodeVersion",
        "mergify": "mergify",
        "mergify_options": "mergifyOptions",
        "min_major_version": "minMajorVersion",
        "min_node_version": "minNodeVersion",
        "mutable_build": "mutableBuild",
        "npm_access": "npmAccess",
        "npm_dist_tag": "npmDistTag",
        "npmignore": "npmignore",
        "npmignore_enabled": "npmignoreEnabled",
        "npm_ignore_options": "npmIgnoreOptions",
        "npm_provenance": "npmProvenance",
        "npm_registry": "npmRegistry",
        "npm_registry_url": "npmRegistryUrl",
        "npm_token_secret": "npmTokenSecret",
        "outdir": "outdir",
        "package": "package",
        "package_manager": "packageManager",
        "package_name": "packageName",
        "parent": "parent",
        "peer_dependency_options": "peerDependencyOptions",
        "peer_deps": "peerDeps",
        "pnpm_version": "pnpmVersion",
        "post_build_steps": "postBuildSteps",
        "prerelease": "prerelease",
        "prettier": "prettier",
        "prettier_options": "prettierOptions",
        "project_type": "projectType",
        "projen_command": "projenCommand",
        "projen_credentials": "projenCredentials",
        "projen_dev_dependency": "projenDevDependency",
        "projenrc_js": "projenrcJs",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "projenrc_js_options": "projenrcJsOptions",
        "projenrc_ts": "projenrcTs",
        "projenrc_ts_options": "projenrcTsOptions",
        "projen_token_secret": "projenTokenSecret",
        "projen_version": "projenVersion",
        "publish_dry_run": "publishDryRun",
        "publish_tasks": "publishTasks",
        "pull_request_template": "pullRequestTemplate",
        "pull_request_template_contents": "pullRequestTemplateContents",
        "readme": "readme",
        "releasable_commits": "releasableCommits",
        "release": "release",
        "release_branches": "releaseBranches",
        "release_every_commit": "releaseEveryCommit",
        "release_failure_issue": "releaseFailureIssue",
        "release_failure_issue_label": "releaseFailureIssueLabel",
        "release_schedule": "releaseSchedule",
        "release_tag_prefix": "releaseTagPrefix",
        "release_to_npm": "releaseToNpm",
        "release_trigger": "releaseTrigger",
        "release_workflow": "releaseWorkflow",
        "release_workflow_name": "releaseWorkflowName",
        "release_workflow_setup_steps": "releaseWorkflowSetupSteps",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "repository": "repository",
        "repository_directory": "repositoryDirectory",
        "sample_code": "sampleCode",
        "scoped_packages_options": "scopedPackagesOptions",
        "scripts": "scripts",
        "srcdir": "srcdir",
        "stability": "stability",
        "stale": "stale",
        "stale_options": "staleOptions",
        "testdir": "testdir",
        "tsconfig": "tsconfig",
        "tsconfig_dev": "tsconfigDev",
        "tsconfig_dev_file": "tsconfigDevFile",
        "ts_jest_options": "tsJestOptions",
        "typescript_version": "typescriptVersion",
        "versionrc_options": "versionrcOptions",
        "vscode": "vscode",
        "workflow_bootstrap_steps": "workflowBootstrapSteps",
        "workflow_container_image": "workflowContainerImage",
        "workflow_git_identity": "workflowGitIdentity",
        "workflow_node_version": "workflowNodeVersion",
        "workflow_package_cache": "workflowPackageCache",
        "workflow_runs_on": "workflowRunsOn",
        "workflow_runs_on_group": "workflowRunsOnGroup",
        "yarn_berry_options": "yarnBerryOptions",
    },
)
class TypeScriptProjectOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        artifacts_directory: typing.Optional[builtins.str] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        author_organization: typing.Optional[builtins.bool] = None,
        author_url: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_approve_upgrades: typing.Optional[builtins.bool] = None,
        auto_detect_bin: typing.Optional[builtins.bool] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bugs_email: typing.Optional[builtins.str] = None,
        bugs_url: typing.Optional[builtins.str] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        copyright_owner: typing.Optional[builtins.str] = None,
        copyright_period: typing.Optional[builtins.str] = None,
        default_release_branch: typing.Optional[builtins.str] = None,
        dependabot: typing.Optional[builtins.bool] = None,
        dependabot_options: typing.Optional[typing.Union[_projen_github_04054675.DependabotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        deps_upgrade: typing.Optional[builtins.bool] = None,
        deps_upgrade_options: typing.Optional[typing.Union[_projen_javascript_04054675.UpgradeDependenciesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        disable_tsconfig: typing.Optional[builtins.bool] = None,
        disable_tsconfig_dev: typing.Optional[builtins.bool] = None,
        docgen: typing.Optional[builtins.bool] = None,
        docs_directory: typing.Optional[builtins.str] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        entrypoint_types: typing.Optional[builtins.str] = None,
        eslint: typing.Optional[builtins.bool] = None,
        eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        libdir: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        licensed: typing.Optional[builtins.bool] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        major_version: typing.Optional[jsii.Number] = None,
        max_node_version: typing.Optional[builtins.str] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        min_node_version: typing.Optional[builtins.str] = None,
        mutable_build: typing.Optional[builtins.bool] = None,
        npm_access: typing.Optional[_projen_javascript_04054675.NpmAccess] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        npmignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        npmignore_enabled: typing.Optional[builtins.bool] = None,
        npm_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        npm_provenance: typing.Optional[builtins.bool] = None,
        npm_registry: typing.Optional[builtins.str] = None,
        npm_registry_url: typing.Optional[builtins.str] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        outdir: typing.Optional[builtins.str] = None,
        package: typing.Optional[builtins.bool] = None,
        package_manager: typing.Optional[_projen_javascript_04054675.NodePackageManager] = None,
        package_name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        peer_dependency_options: typing.Optional[typing.Union[_projen_javascript_04054675.PeerDependencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        pnpm_version: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        prettier: typing.Optional[builtins.bool] = None,
        prettier_options: typing.Optional[typing.Union[_projen_javascript_04054675.PrettierOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_projen_04054675.ProjectType] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
        projen_dev_dependency: typing.Optional[builtins.bool] = None,
        projenrc_js: typing.Optional[builtins.bool] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_js_options: typing.Optional[typing.Union[_projen_javascript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_ts: typing.Optional[builtins.bool] = None,
        projenrc_ts_options: typing.Optional[typing.Union[_projen_typescript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        projen_version: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        pull_request_template: typing.Optional[builtins.bool] = None,
        pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
        releasable_commits: typing.Optional[_projen_04054675.ReleasableCommits] = None,
        release: typing.Optional[builtins.bool] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[_projen_release_04054675.BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_to_npm: typing.Optional[builtins.bool] = None,
        release_trigger: typing.Optional[_projen_release_04054675.ReleaseTrigger] = None,
        release_workflow: typing.Optional[builtins.bool] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_directory: typing.Optional[builtins.str] = None,
        sample_code: typing.Optional[builtins.bool] = None,
        scoped_packages_options: typing.Optional[typing.Sequence[typing.Union[_projen_javascript_04054675.ScopedPackagesOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        srcdir: typing.Optional[builtins.str] = None,
        stability: typing.Optional[builtins.str] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        testdir: typing.Optional[builtins.str] = None,
        tsconfig: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev_file: typing.Optional[builtins.str] = None,
        ts_jest_options: typing.Optional[typing.Union[_projen_typescript_04054675.TsJestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        typescript_version: typing.Optional[builtins.str] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_git_identity: typing.Optional[typing.Union[_projen_github_04054675.GitIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_package_cache: typing.Optional[builtins.bool] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_projen_04054675.GroupRunnerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        yarn_berry_options: typing.Optional[typing.Union[_projen_javascript_04054675.YarnBerryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''TypeScriptProjectOptions.

        :param name: Default: $BASEDIR
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param artifacts_directory: (experimental) A directory which will contain build artifacts. Default: "dist"
        :param author_email: (experimental) Author's e-mail.
        :param author_name: (experimental) Author's name.
        :param author_organization: (experimental) Is the author an organization.
        :param author_url: (experimental) Author's URL / Website.
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_approve_upgrades: (experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configued). Throw if set to true but ``autoApproveOptions`` are not defined. Default: - true
        :param auto_detect_bin: (experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section. Default: true
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param bin: (experimental) Binary programs vended with your module. You can use this option to add/customize how binaries are represented in your ``package.json``, but unless ``autoDetectBin`` is ``false``, every executable file under ``bin`` will automatically be added to this section.
        :param bugs_email: (experimental) The email address to which issues should be reported.
        :param bugs_url: (experimental) The url to your project's issue tracker.
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_options: (experimental) Options for PR build workflow.
        :param build_workflow_triggers: (deprecated) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param check_licenses: (experimental) Configure which licenses should be deemed acceptable for use by dependencies. This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered. Default: - no license checks are run during the build and all licenses will be accepted
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v4 A secret is required for private repos. Configured with ``@codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories. Default: - if this option is not specified, only public repositories are supported
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param copyright_owner: (experimental) License copyright owner. Default: - defaults to the value of authorName or "" if ``authorName`` is undefined.
        :param copyright_period: (experimental) The copyright years to put in the LICENSE file. Default: - current year
        :param default_release_branch: (experimental) The name of the main release branch. Default: "main"
        :param dependabot: (experimental) Use dependabot to handle dependency upgrades. Cannot be used in conjunction with ``depsUpgrade``. Default: false
        :param dependabot_options: (experimental) Options for dependabot. Default: - default options
        :param deps: (experimental) Runtime dependencies of this module. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param deps_upgrade: (experimental) Use tasks and github workflows to handle dependency upgrades. Cannot be used in conjunction with ``dependabot``. Default: true
        :param deps_upgrade_options: (experimental) Options for ``UpgradeDependencies``. Default: - default options
        :param description: (experimental) The description is just a string that helps people understand the purpose of the package. It can be used when searching for packages in a package manager as well. See https://classic.yarnpkg.com/en/docs/package-json/#toc-description
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param dev_deps: (experimental) Build dependencies for this module. These dependencies will only be available in your build environment but will not be fetched when this module is consumed. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param disable_tsconfig: (experimental) Do not generate a ``tsconfig.json`` file (used by jsii projects since tsconfig.json is generated by the jsii compiler). Default: false
        :param disable_tsconfig_dev: (experimental) Do not generate a ``tsconfig.dev.json`` file. Default: false
        :param docgen: (experimental) Docgen by Typedoc. Default: false
        :param docs_directory: (experimental) Docs directory. Default: "docs"
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json. Default: "lib/index.js"
        :param entrypoint_types: (experimental) The .d.ts file that includes the type declarations for this module. Default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)
        :param eslint: (experimental) Setup eslint. Default: true
        :param eslint_options: (experimental) Eslint options. Default: - opinionated default options
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param homepage: (experimental) Package's Homepage / Website.
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param libdir: (experimental) Typescript artifacts output directory. Default: "lib"
        :param license: (experimental) License's SPDX identifier. See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses. Use the ``licensed`` option if you want to no license to be specified. Default: "Apache-2.0"
        :param licensed: (experimental) Indicates if a license should be added. Default: true
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param max_node_version: (experimental) Minimum node.js version to require via ``engines`` (inclusive). Default: - no max
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param min_node_version: (experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive). Default: - no "engines" specified
        :param mutable_build: (deprecated) Automatically update files modified during builds to pull-request branches. This means that any files synthesized by projen or e.g. test snapshots will always be up-to-date before a PR is merged. Implies that PR builds do not have anti-tamper checks. Default: true
        :param npm_access: (experimental) Access level of the npm package. Default: - for scoped packages (e.g. ``foo@bar``), the default is ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is ``NpmAccess.PUBLIC``.
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param npmignore: (deprecated) Additional entries to .npmignore.
        :param npmignore_enabled: (experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs. Default: true
        :param npm_ignore_options: (experimental) Configuration options for .npmignore file.
        :param npm_provenance: (experimental) Should provenance statements be generated when the package is published. A supported package manager is required to publish a package with npm provenance statements and you will need to use a supported CI/CD provider. Note that the projen ``Release`` and ``Publisher`` components are using ``publib`` to publish packages, which is using npm internally and supports provenance statements independently of the package manager used. Default: - true for public packages, false otherwise
        :param npm_registry: (deprecated) The host name of the npm registry to publish to. Cannot be set together with ``npmRegistryUrl``.
        :param npm_registry_url: (experimental) The base URL of the npm package registry. Must be a URL (e.g. start with "https://" or "http://") Default: "https://registry.npmjs.org"
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: "NPM_TOKEN"
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param package: (experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``). Default: true
        :param package_manager: (experimental) The Node Package Manager used to execute scripts. Default: NodePackageManager.YARN_CLASSIC
        :param package_name: (experimental) The "name" in package.json. Default: - defaults to project name
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param peer_dependency_options: (experimental) Options for ``peerDeps``.
        :param peer_deps: (experimental) Peer dependencies for this module. Dependencies listed here are required to be installed (and satisfied) by the *consumer* of this library. Using peer dependencies allows you to ensure that only a single module of a certain library exists in the ``node_modules`` tree of your consumers. Note that prior to npm@7, peer dependencies are *not* automatically installed, which means that adding peer dependencies to a library will be a breaking change for your customers. Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is enabled by default), projen will automatically add a dev dependency with a pinned version for each peer dependency. This will ensure that you build & test your module against the lowest peer version required. Default: []
        :param pnpm_version: (experimental) The version of PNPM to use if using PNPM as a package manager. Default: "7"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param prettier: (experimental) Setup prettier. Default: false
        :param prettier_options: (experimental) Prettier options. Default: - default options
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projen_dev_dependency: (experimental) Indicates of "projen" should be installed as a devDependency. Default: - true if not a subproject
        :param projenrc_js: (experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation. Default: - true if projenrcJson is false
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param projenrc_js_options: (experimental) Options for .projenrc.js. Default: - default options
        :param projenrc_ts: (experimental) Use TypeScript for your projenrc file (``.projenrc.ts``). Default: false
        :param projenrc_ts_options: (experimental) Options for .projenrc.ts.
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param projen_version: (experimental) Version of projen to install. Default: - Defaults to the latest version.
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param pull_request_template: (experimental) Include a GitHub pull request template. Default: true
        :param pull_request_template_contents: (experimental) The contents of the pull request template. Default: - default content
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release: (experimental) Add release management to this project. Default: - true (false for subprojects)
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_every_commit: (deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_schedule: (deprecated) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_to_npm: (experimental) Automatically release to npm when new versions are introduced. Default: false
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow: (deprecated) DEPRECATED: renamed to ``release``. Default: - true if not a subproject
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param repository: (experimental) The repository is the location where the actual code for your package lives. See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository
        :param repository_directory: (experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.
        :param sample_code: (experimental) Generate one-time sample in ``src/`` and ``test/`` if there are no files there. Default: true
        :param scoped_packages_options: (experimental) Options for privately hosted scoped packages. Default: - fetch all scoped packages from the public npm registry
        :param scripts: (deprecated) npm scripts to include. If a script has the same name as a standard script, the standard script will be overwritten. Also adds the script as a task. Default: {}
        :param srcdir: (experimental) Typescript sources directory. Default: "src"
        :param stability: (experimental) Package's Stability.
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param testdir: (experimental) Jest tests directory. Tests files should be named ``xxx.test.ts``. If this directory is under ``srcdir`` (e.g. ``src/test``, ``src/__tests__``), then tests are going to be compiled into ``lib/`` and executed as javascript. If the test directory is outside of ``src``, then we configure jest to compile the code in-memory. Default: "test"
        :param tsconfig: (experimental) Custom TSConfig. Default: - default options
        :param tsconfig_dev: (experimental) Custom tsconfig options for the development tsconfig.json file (used for testing). Default: - use the production tsconfig options
        :param tsconfig_dev_file: (experimental) The name of the development tsconfig.json file. Default: "tsconfig.dev.json"
        :param ts_jest_options: (experimental) Options for ts-jest.
        :param typescript_version: (experimental) TypeScript version to use. NOTE: Typescript is not semantically versioned and should remain on the same minor, so we recommend using a ``~`` dependency (e.g. ``~1.2.3``). Default: "latest"
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with standard-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param workflow_bootstrap_steps: (experimental) Workflow steps to use in order to bootstrap this repo. Default: "yarn install --frozen-lockfile && yarn projen"
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_git_identity: (experimental) The git identity to use in workflows. Default: - GitHub Actions
        :param workflow_node_version: (experimental) The node version to use in GitHub workflows. Default: - same as ``minNodeVersion``
        :param workflow_package_cache: (experimental) Enable Node.js package cache in GitHub workflows. Default: false
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param yarn_berry_options: (experimental) Options for Yarn Berry. Default: - Yarn Berry v4 with all default options
        '''
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _projen_github_04054675.AutoApproveOptions(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _projen_github_04054675.AutoMergeOptions(**auto_merge_options)
        if isinstance(build_workflow_options, dict):
            build_workflow_options = _projen_javascript_04054675.BuildWorkflowOptions(**build_workflow_options)
        if isinstance(build_workflow_triggers, dict):
            build_workflow_triggers = _projen_github_workflows_04054675.Triggers(**build_workflow_triggers)
        if isinstance(bundler_options, dict):
            bundler_options = _projen_javascript_04054675.BundlerOptions(**bundler_options)
        if isinstance(check_licenses, dict):
            check_licenses = _projen_javascript_04054675.LicenseCheckerOptions(**check_licenses)
        if isinstance(code_artifact_options, dict):
            code_artifact_options = _projen_javascript_04054675.CodeArtifactOptions(**code_artifact_options)
        if isinstance(dependabot_options, dict):
            dependabot_options = _projen_github_04054675.DependabotOptions(**dependabot_options)
        if isinstance(deps_upgrade_options, dict):
            deps_upgrade_options = _projen_javascript_04054675.UpgradeDependenciesOptions(**deps_upgrade_options)
        if isinstance(eslint_options, dict):
            eslint_options = _projen_javascript_04054675.EslintOptions(**eslint_options)
        if isinstance(github_options, dict):
            github_options = _projen_github_04054675.GitHubOptions(**github_options)
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _projen_04054675.IgnoreFileOptions(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _projen_04054675.GitOptions(**git_options)
        if isinstance(jest_options, dict):
            jest_options = _projen_javascript_04054675.JestOptions(**jest_options)
        if isinstance(logging, dict):
            logging = _projen_04054675.LoggerOptions(**logging)
        if isinstance(mergify_options, dict):
            mergify_options = _projen_github_04054675.MergifyOptions(**mergify_options)
        if isinstance(npm_ignore_options, dict):
            npm_ignore_options = _projen_04054675.IgnoreFileOptions(**npm_ignore_options)
        if isinstance(peer_dependency_options, dict):
            peer_dependency_options = _projen_javascript_04054675.PeerDependencyOptions(**peer_dependency_options)
        if isinstance(prettier_options, dict):
            prettier_options = _projen_javascript_04054675.PrettierOptions(**prettier_options)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _projen_04054675.ProjenrcJsonOptions(**projenrc_json_options)
        if isinstance(projenrc_js_options, dict):
            projenrc_js_options = _projen_javascript_04054675.ProjenrcOptions(**projenrc_js_options)
        if isinstance(projenrc_ts_options, dict):
            projenrc_ts_options = _projen_typescript_04054675.ProjenrcOptions(**projenrc_ts_options)
        if isinstance(readme, dict):
            readme = _projen_04054675.SampleReadmeProps(**readme)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _projen_04054675.RenovatebotOptions(**renovatebot_options)
        if isinstance(stale_options, dict):
            stale_options = _projen_github_04054675.StaleOptions(**stale_options)
        if isinstance(tsconfig, dict):
            tsconfig = _projen_javascript_04054675.TypescriptConfigOptions(**tsconfig)
        if isinstance(tsconfig_dev, dict):
            tsconfig_dev = _projen_javascript_04054675.TypescriptConfigOptions(**tsconfig_dev)
        if isinstance(ts_jest_options, dict):
            ts_jest_options = _projen_typescript_04054675.TsJestOptions(**ts_jest_options)
        if isinstance(workflow_git_identity, dict):
            workflow_git_identity = _projen_github_04054675.GitIdentity(**workflow_git_identity)
        if isinstance(workflow_runs_on_group, dict):
            workflow_runs_on_group = _projen_04054675.GroupRunnerOptions(**workflow_runs_on_group)
        if isinstance(yarn_berry_options, dict):
            yarn_berry_options = _projen_javascript_04054675.YarnBerryOptions(**yarn_berry_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb99db9d3225c4cdd0c347616408142d71a340a8c808142cc5f3d813a6f71ec)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_library_dependencies", value=allow_library_dependencies, expected_type=type_hints["allow_library_dependencies"])
            check_type(argname="argument artifacts_directory", value=artifacts_directory, expected_type=type_hints["artifacts_directory"])
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument author_organization", value=author_organization, expected_type=type_hints["author_organization"])
            check_type(argname="argument author_url", value=author_url, expected_type=type_hints["author_url"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_approve_upgrades", value=auto_approve_upgrades, expected_type=type_hints["auto_approve_upgrades"])
            check_type(argname="argument auto_detect_bin", value=auto_detect_bin, expected_type=type_hints["auto_detect_bin"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument bin", value=bin, expected_type=type_hints["bin"])
            check_type(argname="argument bugs_email", value=bugs_email, expected_type=type_hints["bugs_email"])
            check_type(argname="argument bugs_url", value=bugs_url, expected_type=type_hints["bugs_url"])
            check_type(argname="argument build_workflow", value=build_workflow, expected_type=type_hints["build_workflow"])
            check_type(argname="argument build_workflow_options", value=build_workflow_options, expected_type=type_hints["build_workflow_options"])
            check_type(argname="argument build_workflow_triggers", value=build_workflow_triggers, expected_type=type_hints["build_workflow_triggers"])
            check_type(argname="argument bundled_deps", value=bundled_deps, expected_type=type_hints["bundled_deps"])
            check_type(argname="argument bundler_options", value=bundler_options, expected_type=type_hints["bundler_options"])
            check_type(argname="argument check_licenses", value=check_licenses, expected_type=type_hints["check_licenses"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument code_cov", value=code_cov, expected_type=type_hints["code_cov"])
            check_type(argname="argument code_cov_token_secret", value=code_cov_token_secret, expected_type=type_hints["code_cov_token_secret"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument copyright_owner", value=copyright_owner, expected_type=type_hints["copyright_owner"])
            check_type(argname="argument copyright_period", value=copyright_period, expected_type=type_hints["copyright_period"])
            check_type(argname="argument default_release_branch", value=default_release_branch, expected_type=type_hints["default_release_branch"])
            check_type(argname="argument dependabot", value=dependabot, expected_type=type_hints["dependabot"])
            check_type(argname="argument dependabot_options", value=dependabot_options, expected_type=type_hints["dependabot_options"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument deps_upgrade", value=deps_upgrade, expected_type=type_hints["deps_upgrade"])
            check_type(argname="argument deps_upgrade_options", value=deps_upgrade_options, expected_type=type_hints["deps_upgrade_options"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument disable_tsconfig", value=disable_tsconfig, expected_type=type_hints["disable_tsconfig"])
            check_type(argname="argument disable_tsconfig_dev", value=disable_tsconfig_dev, expected_type=type_hints["disable_tsconfig_dev"])
            check_type(argname="argument docgen", value=docgen, expected_type=type_hints["docgen"])
            check_type(argname="argument docs_directory", value=docs_directory, expected_type=type_hints["docs_directory"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument entrypoint_types", value=entrypoint_types, expected_type=type_hints["entrypoint_types"])
            check_type(argname="argument eslint", value=eslint, expected_type=type_hints["eslint"])
            check_type(argname="argument eslint_options", value=eslint_options, expected_type=type_hints["eslint_options"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument gitignore", value=gitignore, expected_type=type_hints["gitignore"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument jest", value=jest, expected_type=type_hints["jest"])
            check_type(argname="argument jest_options", value=jest_options, expected_type=type_hints["jest_options"])
            check_type(argname="argument jsii_release_version", value=jsii_release_version, expected_type=type_hints["jsii_release_version"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument libdir", value=libdir, expected_type=type_hints["libdir"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument licensed", value=licensed, expected_type=type_hints["licensed"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument max_node_version", value=max_node_version, expected_type=type_hints["max_node_version"])
            check_type(argname="argument mergify", value=mergify, expected_type=type_hints["mergify"])
            check_type(argname="argument mergify_options", value=mergify_options, expected_type=type_hints["mergify_options"])
            check_type(argname="argument min_major_version", value=min_major_version, expected_type=type_hints["min_major_version"])
            check_type(argname="argument min_node_version", value=min_node_version, expected_type=type_hints["min_node_version"])
            check_type(argname="argument mutable_build", value=mutable_build, expected_type=type_hints["mutable_build"])
            check_type(argname="argument npm_access", value=npm_access, expected_type=type_hints["npm_access"])
            check_type(argname="argument npm_dist_tag", value=npm_dist_tag, expected_type=type_hints["npm_dist_tag"])
            check_type(argname="argument npmignore", value=npmignore, expected_type=type_hints["npmignore"])
            check_type(argname="argument npmignore_enabled", value=npmignore_enabled, expected_type=type_hints["npmignore_enabled"])
            check_type(argname="argument npm_ignore_options", value=npm_ignore_options, expected_type=type_hints["npm_ignore_options"])
            check_type(argname="argument npm_provenance", value=npm_provenance, expected_type=type_hints["npm_provenance"])
            check_type(argname="argument npm_registry", value=npm_registry, expected_type=type_hints["npm_registry"])
            check_type(argname="argument npm_registry_url", value=npm_registry_url, expected_type=type_hints["npm_registry_url"])
            check_type(argname="argument npm_token_secret", value=npm_token_secret, expected_type=type_hints["npm_token_secret"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument package", value=package, expected_type=type_hints["package"])
            check_type(argname="argument package_manager", value=package_manager, expected_type=type_hints["package_manager"])
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument peer_dependency_options", value=peer_dependency_options, expected_type=type_hints["peer_dependency_options"])
            check_type(argname="argument peer_deps", value=peer_deps, expected_type=type_hints["peer_deps"])
            check_type(argname="argument pnpm_version", value=pnpm_version, expected_type=type_hints["pnpm_version"])
            check_type(argname="argument post_build_steps", value=post_build_steps, expected_type=type_hints["post_build_steps"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument prettier", value=prettier, expected_type=type_hints["prettier"])
            check_type(argname="argument prettier_options", value=prettier_options, expected_type=type_hints["prettier_options"])
            check_type(argname="argument project_type", value=project_type, expected_type=type_hints["project_type"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument projen_dev_dependency", value=projen_dev_dependency, expected_type=type_hints["projen_dev_dependency"])
            check_type(argname="argument projenrc_js", value=projenrc_js, expected_type=type_hints["projenrc_js"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument projenrc_js_options", value=projenrc_js_options, expected_type=type_hints["projenrc_js_options"])
            check_type(argname="argument projenrc_ts", value=projenrc_ts, expected_type=type_hints["projenrc_ts"])
            check_type(argname="argument projenrc_ts_options", value=projenrc_ts_options, expected_type=type_hints["projenrc_ts_options"])
            check_type(argname="argument projen_token_secret", value=projen_token_secret, expected_type=type_hints["projen_token_secret"])
            check_type(argname="argument projen_version", value=projen_version, expected_type=type_hints["projen_version"])
            check_type(argname="argument publish_dry_run", value=publish_dry_run, expected_type=type_hints["publish_dry_run"])
            check_type(argname="argument publish_tasks", value=publish_tasks, expected_type=type_hints["publish_tasks"])
            check_type(argname="argument pull_request_template", value=pull_request_template, expected_type=type_hints["pull_request_template"])
            check_type(argname="argument pull_request_template_contents", value=pull_request_template_contents, expected_type=type_hints["pull_request_template_contents"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument releasable_commits", value=releasable_commits, expected_type=type_hints["releasable_commits"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument release_branches", value=release_branches, expected_type=type_hints["release_branches"])
            check_type(argname="argument release_every_commit", value=release_every_commit, expected_type=type_hints["release_every_commit"])
            check_type(argname="argument release_failure_issue", value=release_failure_issue, expected_type=type_hints["release_failure_issue"])
            check_type(argname="argument release_failure_issue_label", value=release_failure_issue_label, expected_type=type_hints["release_failure_issue_label"])
            check_type(argname="argument release_schedule", value=release_schedule, expected_type=type_hints["release_schedule"])
            check_type(argname="argument release_tag_prefix", value=release_tag_prefix, expected_type=type_hints["release_tag_prefix"])
            check_type(argname="argument release_to_npm", value=release_to_npm, expected_type=type_hints["release_to_npm"])
            check_type(argname="argument release_trigger", value=release_trigger, expected_type=type_hints["release_trigger"])
            check_type(argname="argument release_workflow", value=release_workflow, expected_type=type_hints["release_workflow"])
            check_type(argname="argument release_workflow_name", value=release_workflow_name, expected_type=type_hints["release_workflow_name"])
            check_type(argname="argument release_workflow_setup_steps", value=release_workflow_setup_steps, expected_type=type_hints["release_workflow_setup_steps"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument repository_directory", value=repository_directory, expected_type=type_hints["repository_directory"])
            check_type(argname="argument sample_code", value=sample_code, expected_type=type_hints["sample_code"])
            check_type(argname="argument scoped_packages_options", value=scoped_packages_options, expected_type=type_hints["scoped_packages_options"])
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
            check_type(argname="argument srcdir", value=srcdir, expected_type=type_hints["srcdir"])
            check_type(argname="argument stability", value=stability, expected_type=type_hints["stability"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument testdir", value=testdir, expected_type=type_hints["testdir"])
            check_type(argname="argument tsconfig", value=tsconfig, expected_type=type_hints["tsconfig"])
            check_type(argname="argument tsconfig_dev", value=tsconfig_dev, expected_type=type_hints["tsconfig_dev"])
            check_type(argname="argument tsconfig_dev_file", value=tsconfig_dev_file, expected_type=type_hints["tsconfig_dev_file"])
            check_type(argname="argument ts_jest_options", value=ts_jest_options, expected_type=type_hints["ts_jest_options"])
            check_type(argname="argument typescript_version", value=typescript_version, expected_type=type_hints["typescript_version"])
            check_type(argname="argument versionrc_options", value=versionrc_options, expected_type=type_hints["versionrc_options"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument workflow_bootstrap_steps", value=workflow_bootstrap_steps, expected_type=type_hints["workflow_bootstrap_steps"])
            check_type(argname="argument workflow_container_image", value=workflow_container_image, expected_type=type_hints["workflow_container_image"])
            check_type(argname="argument workflow_git_identity", value=workflow_git_identity, expected_type=type_hints["workflow_git_identity"])
            check_type(argname="argument workflow_node_version", value=workflow_node_version, expected_type=type_hints["workflow_node_version"])
            check_type(argname="argument workflow_package_cache", value=workflow_package_cache, expected_type=type_hints["workflow_package_cache"])
            check_type(argname="argument workflow_runs_on", value=workflow_runs_on, expected_type=type_hints["workflow_runs_on"])
            check_type(argname="argument workflow_runs_on_group", value=workflow_runs_on_group, expected_type=type_hints["workflow_runs_on_group"])
            check_type(argname="argument yarn_berry_options", value=yarn_berry_options, expected_type=type_hints["yarn_berry_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_library_dependencies is not None:
            self._values["allow_library_dependencies"] = allow_library_dependencies
        if artifacts_directory is not None:
            self._values["artifacts_directory"] = artifacts_directory
        if author_email is not None:
            self._values["author_email"] = author_email
        if author_name is not None:
            self._values["author_name"] = author_name
        if author_organization is not None:
            self._values["author_organization"] = author_organization
        if author_url is not None:
            self._values["author_url"] = author_url
        if auto_approve_options is not None:
            self._values["auto_approve_options"] = auto_approve_options
        if auto_approve_upgrades is not None:
            self._values["auto_approve_upgrades"] = auto_approve_upgrades
        if auto_detect_bin is not None:
            self._values["auto_detect_bin"] = auto_detect_bin
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if auto_merge_options is not None:
            self._values["auto_merge_options"] = auto_merge_options
        if bin is not None:
            self._values["bin"] = bin
        if bugs_email is not None:
            self._values["bugs_email"] = bugs_email
        if bugs_url is not None:
            self._values["bugs_url"] = bugs_url
        if build_workflow is not None:
            self._values["build_workflow"] = build_workflow
        if build_workflow_options is not None:
            self._values["build_workflow_options"] = build_workflow_options
        if build_workflow_triggers is not None:
            self._values["build_workflow_triggers"] = build_workflow_triggers
        if bundled_deps is not None:
            self._values["bundled_deps"] = bundled_deps
        if bundler_options is not None:
            self._values["bundler_options"] = bundler_options
        if check_licenses is not None:
            self._values["check_licenses"] = check_licenses
        if clobber is not None:
            self._values["clobber"] = clobber
        if code_artifact_options is not None:
            self._values["code_artifact_options"] = code_artifact_options
        if code_cov is not None:
            self._values["code_cov"] = code_cov
        if code_cov_token_secret is not None:
            self._values["code_cov_token_secret"] = code_cov_token_secret
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if copyright_owner is not None:
            self._values["copyright_owner"] = copyright_owner
        if copyright_period is not None:
            self._values["copyright_period"] = copyright_period
        if default_release_branch is not None:
            self._values["default_release_branch"] = default_release_branch
        if dependabot is not None:
            self._values["dependabot"] = dependabot
        if dependabot_options is not None:
            self._values["dependabot_options"] = dependabot_options
        if deps is not None:
            self._values["deps"] = deps
        if deps_upgrade is not None:
            self._values["deps_upgrade"] = deps_upgrade
        if deps_upgrade_options is not None:
            self._values["deps_upgrade_options"] = deps_upgrade_options
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if disable_tsconfig is not None:
            self._values["disable_tsconfig"] = disable_tsconfig
        if disable_tsconfig_dev is not None:
            self._values["disable_tsconfig_dev"] = disable_tsconfig_dev
        if docgen is not None:
            self._values["docgen"] = docgen
        if docs_directory is not None:
            self._values["docs_directory"] = docs_directory
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if entrypoint_types is not None:
            self._values["entrypoint_types"] = entrypoint_types
        if eslint is not None:
            self._values["eslint"] = eslint
        if eslint_options is not None:
            self._values["eslint_options"] = eslint_options
        if github is not None:
            self._values["github"] = github
        if github_options is not None:
            self._values["github_options"] = github_options
        if gitignore is not None:
            self._values["gitignore"] = gitignore
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if gitpod is not None:
            self._values["gitpod"] = gitpod
        if homepage is not None:
            self._values["homepage"] = homepage
        if jest is not None:
            self._values["jest"] = jest
        if jest_options is not None:
            self._values["jest_options"] = jest_options
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if keywords is not None:
            self._values["keywords"] = keywords
        if libdir is not None:
            self._values["libdir"] = libdir
        if license is not None:
            self._values["license"] = license
        if licensed is not None:
            self._values["licensed"] = licensed
        if logging is not None:
            self._values["logging"] = logging
        if major_version is not None:
            self._values["major_version"] = major_version
        if max_node_version is not None:
            self._values["max_node_version"] = max_node_version
        if mergify is not None:
            self._values["mergify"] = mergify
        if mergify_options is not None:
            self._values["mergify_options"] = mergify_options
        if min_major_version is not None:
            self._values["min_major_version"] = min_major_version
        if min_node_version is not None:
            self._values["min_node_version"] = min_node_version
        if mutable_build is not None:
            self._values["mutable_build"] = mutable_build
        if npm_access is not None:
            self._values["npm_access"] = npm_access
        if npm_dist_tag is not None:
            self._values["npm_dist_tag"] = npm_dist_tag
        if npmignore is not None:
            self._values["npmignore"] = npmignore
        if npmignore_enabled is not None:
            self._values["npmignore_enabled"] = npmignore_enabled
        if npm_ignore_options is not None:
            self._values["npm_ignore_options"] = npm_ignore_options
        if npm_provenance is not None:
            self._values["npm_provenance"] = npm_provenance
        if npm_registry is not None:
            self._values["npm_registry"] = npm_registry
        if npm_registry_url is not None:
            self._values["npm_registry_url"] = npm_registry_url
        if npm_token_secret is not None:
            self._values["npm_token_secret"] = npm_token_secret
        if outdir is not None:
            self._values["outdir"] = outdir
        if package is not None:
            self._values["package"] = package
        if package_manager is not None:
            self._values["package_manager"] = package_manager
        if package_name is not None:
            self._values["package_name"] = package_name
        if parent is not None:
            self._values["parent"] = parent
        if peer_dependency_options is not None:
            self._values["peer_dependency_options"] = peer_dependency_options
        if peer_deps is not None:
            self._values["peer_deps"] = peer_deps
        if pnpm_version is not None:
            self._values["pnpm_version"] = pnpm_version
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if prettier is not None:
            self._values["prettier"] = prettier
        if prettier_options is not None:
            self._values["prettier_options"] = prettier_options
        if project_type is not None:
            self._values["project_type"] = project_type
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if projen_dev_dependency is not None:
            self._values["projen_dev_dependency"] = projen_dev_dependency
        if projenrc_js is not None:
            self._values["projenrc_js"] = projenrc_js
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if projenrc_js_options is not None:
            self._values["projenrc_js_options"] = projenrc_js_options
        if projenrc_ts is not None:
            self._values["projenrc_ts"] = projenrc_ts
        if projenrc_ts_options is not None:
            self._values["projenrc_ts_options"] = projenrc_ts_options
        if projen_token_secret is not None:
            self._values["projen_token_secret"] = projen_token_secret
        if projen_version is not None:
            self._values["projen_version"] = projen_version
        if publish_dry_run is not None:
            self._values["publish_dry_run"] = publish_dry_run
        if publish_tasks is not None:
            self._values["publish_tasks"] = publish_tasks
        if pull_request_template is not None:
            self._values["pull_request_template"] = pull_request_template
        if pull_request_template_contents is not None:
            self._values["pull_request_template_contents"] = pull_request_template_contents
        if readme is not None:
            self._values["readme"] = readme
        if releasable_commits is not None:
            self._values["releasable_commits"] = releasable_commits
        if release is not None:
            self._values["release"] = release
        if release_branches is not None:
            self._values["release_branches"] = release_branches
        if release_every_commit is not None:
            self._values["release_every_commit"] = release_every_commit
        if release_failure_issue is not None:
            self._values["release_failure_issue"] = release_failure_issue
        if release_failure_issue_label is not None:
            self._values["release_failure_issue_label"] = release_failure_issue_label
        if release_schedule is not None:
            self._values["release_schedule"] = release_schedule
        if release_tag_prefix is not None:
            self._values["release_tag_prefix"] = release_tag_prefix
        if release_to_npm is not None:
            self._values["release_to_npm"] = release_to_npm
        if release_trigger is not None:
            self._values["release_trigger"] = release_trigger
        if release_workflow is not None:
            self._values["release_workflow"] = release_workflow
        if release_workflow_name is not None:
            self._values["release_workflow_name"] = release_workflow_name
        if release_workflow_setup_steps is not None:
            self._values["release_workflow_setup_steps"] = release_workflow_setup_steps
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if repository is not None:
            self._values["repository"] = repository
        if repository_directory is not None:
            self._values["repository_directory"] = repository_directory
        if sample_code is not None:
            self._values["sample_code"] = sample_code
        if scoped_packages_options is not None:
            self._values["scoped_packages_options"] = scoped_packages_options
        if scripts is not None:
            self._values["scripts"] = scripts
        if srcdir is not None:
            self._values["srcdir"] = srcdir
        if stability is not None:
            self._values["stability"] = stability
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if testdir is not None:
            self._values["testdir"] = testdir
        if tsconfig is not None:
            self._values["tsconfig"] = tsconfig
        if tsconfig_dev is not None:
            self._values["tsconfig_dev"] = tsconfig_dev
        if tsconfig_dev_file is not None:
            self._values["tsconfig_dev_file"] = tsconfig_dev_file
        if ts_jest_options is not None:
            self._values["ts_jest_options"] = ts_jest_options
        if typescript_version is not None:
            self._values["typescript_version"] = typescript_version
        if versionrc_options is not None:
            self._values["versionrc_options"] = versionrc_options
        if vscode is not None:
            self._values["vscode"] = vscode
        if workflow_bootstrap_steps is not None:
            self._values["workflow_bootstrap_steps"] = workflow_bootstrap_steps
        if workflow_container_image is not None:
            self._values["workflow_container_image"] = workflow_container_image
        if workflow_git_identity is not None:
            self._values["workflow_git_identity"] = workflow_git_identity
        if workflow_node_version is not None:
            self._values["workflow_node_version"] = workflow_node_version
        if workflow_package_cache is not None:
            self._values["workflow_package_cache"] = workflow_package_cache
        if workflow_runs_on is not None:
            self._values["workflow_runs_on"] = workflow_runs_on
        if workflow_runs_on_group is not None:
            self._values["workflow_runs_on_group"] = workflow_runs_on_group
        if yarn_berry_options is not None:
            self._values["yarn_berry_options"] = yarn_berry_options

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :default: $BASEDIR
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_library_dependencies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``.

        This is normally only allowed for libraries. For apps, there's no meaning
        for specifying these.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("allow_library_dependencies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def artifacts_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) A directory which will contain build artifacts.

        :default: "dist"

        :stability: experimental
        '''
        result = self._values.get("artifacts_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's e-mail.

        :stability: experimental
        '''
        result = self._values.get("author_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's name.

        :stability: experimental
        '''
        result = self._values.get("author_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_organization(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Is the author an organization.

        :stability: experimental
        '''
        result = self._values.get("author_organization")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def author_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's URL / Website.

        :stability: experimental
        '''
        result = self._values.get("author_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_approve_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoApproveOptions]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoApproveOptions], result)

    @builtins.property
    def auto_approve_upgrades(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configued).

        Throw if set to true but ``autoApproveOptions`` are not defined.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("auto_approve_upgrades")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_detect_bin(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_detect_bin")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable automatic merging on GitHub.

        Has no effect if ``github.mergify``
        is set to false.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoMergeOptions]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoMergeOptions], result)

    @builtins.property
    def bin(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Binary programs vended with your module.

        You can use this option to add/customize how binaries are represented in
        your ``package.json``, but unless ``autoDetectBin`` is ``false``, every
        executable file under ``bin`` will automatically be added to this section.

        :stability: experimental
        '''
        result = self._values.get("bin")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bugs_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) The email address to which issues should be reported.

        :stability: experimental
        '''
        result = self._values.get("bugs_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bugs_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The url to your project's issue tracker.

        :stability: experimental
        '''
        result = self._values.get("bugs_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define a GitHub workflow for building PRs.

        :default: - true if not a subproject

        :stability: experimental
        '''
        result = self._values.get("build_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def build_workflow_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.BuildWorkflowOptions]:
        '''(experimental) Options for PR build workflow.

        :stability: experimental
        '''
        result = self._values.get("build_workflow_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.BuildWorkflowOptions], result)

    @builtins.property
    def build_workflow_triggers(
        self,
    ) -> typing.Optional[_projen_github_workflows_04054675.Triggers]:
        '''(deprecated) Build workflow triggers.

        :default: "{ pullRequest: {}, workflowDispatch: {} }"

        :deprecated: - Use ``buildWorkflowOptions.workflowTriggers``

        :stability: deprecated
        '''
        result = self._values.get("build_workflow_triggers")
        return typing.cast(typing.Optional[_projen_github_workflows_04054675.Triggers], result)

    @builtins.property
    def bundled_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of dependencies to bundle into this module.

        These modules will be
        added both to the ``dependencies`` section and ``bundledDependencies`` section of
        your ``package.json``.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :stability: experimental
        '''
        result = self._values.get("bundled_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bundler_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.BundlerOptions]:
        '''(experimental) Options for ``Bundler``.

        :stability: experimental
        '''
        result = self._values.get("bundler_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.BundlerOptions], result)

    @builtins.property
    def check_licenses(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.LicenseCheckerOptions]:
        '''(experimental) Configure which licenses should be deemed acceptable for use by dependencies.

        This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered.

        :default: - no license checks are run during the build and all licenses will be accepted

        :stability: experimental
        '''
        result = self._values.get("check_licenses")
        return typing.cast(typing.Optional[_projen_javascript_04054675.LicenseCheckerOptions], result)

    @builtins.property
    def clobber(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a ``clobber`` task which resets the repo to origin.

        :default: - true, but false for subprojects

        :stability: experimental
        '''
        result = self._values.get("clobber")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def code_artifact_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.CodeArtifactOptions]:
        '''(experimental) Options for npm packages using AWS CodeArtifact.

        This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("code_artifact_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.CodeArtifactOptions], result)

    @builtins.property
    def code_cov(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v4 A secret is required for private repos. Configured with ``@codeCovTokenSecret``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("code_cov")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def code_cov_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories.

        :default: - if this option is not specified, only public repositories are supported

        :stability: experimental
        '''
        result = self._values.get("code_cov_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def copyright_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) License copyright owner.

        :default: - defaults to the value of authorName or "" if ``authorName`` is undefined.

        :stability: experimental
        '''
        result = self._values.get("copyright_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copyright_period(self) -> typing.Optional[builtins.str]:
        '''(experimental) The copyright years to put in the LICENSE file.

        :default: - current year

        :stability: experimental
        '''
        result = self._values.get("copyright_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_release_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the main release branch.

        :default: "main"

        :stability: experimental
        '''
        result = self._values.get("default_release_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependabot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use dependabot to handle dependency upgrades.

        Cannot be used in conjunction with ``depsUpgrade``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dependabot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dependabot_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.DependabotOptions]:
        '''(experimental) Options for dependabot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("dependabot_options")
        return typing.cast(typing.Optional[_projen_github_04054675.DependabotOptions], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Runtime dependencies of this module.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: false
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deps_upgrade(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use tasks and github workflows to handle dependency upgrades.

        Cannot be used in conjunction with ``dependabot``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("deps_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deps_upgrade_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.UpgradeDependenciesOptions]:
        '''(experimental) Options for ``UpgradeDependencies``.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("deps_upgrade_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.UpgradeDependenciesOptions], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description is just a string that helps people understand the purpose of the package.

        It can be used when searching for packages in a package manager as well.
        See https://classic.yarnpkg.com/en/docs/package-json/#toc-description

        :stability: experimental
        :featured: false
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dev_container(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a VSCode development environment (used for GitHub Codespaces).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dev_container")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dev_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Build dependencies for this module.

        These dependencies will only be
        available in your build environment but will not be fetched when this
        module is consumed.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("dev_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disable_tsconfig(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not generate a ``tsconfig.json`` file (used by jsii projects since tsconfig.json is generated by the jsii compiler).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disable_tsconfig")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def disable_tsconfig_dev(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not generate a ``tsconfig.dev.json`` file.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disable_tsconfig_dev")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docgen(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Docgen by Typedoc.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("docgen")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docs_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs directory.

        :default: "docs"

        :stability: experimental
        '''
        result = self._values.get("docs_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json.

        :default: "lib/index.js"

        :stability: experimental
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint_types(self) -> typing.Optional[builtins.str]:
        '''(experimental) The .d.ts file that includes the type declarations for this module.

        :default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)

        :stability: experimental
        '''
        result = self._values.get("entrypoint_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eslint(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup eslint.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("eslint")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def eslint_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.EslintOptions]:
        '''(experimental) Eslint options.

        :default: - opinionated default options

        :stability: experimental
        '''
        result = self._values.get("eslint_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.EslintOptions], result)

    @builtins.property
    def github(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable GitHub integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github_options(self) -> typing.Optional[_projen_github_04054675.GitHubOptions]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional[_projen_github_04054675.GitHubOptions], result)

    @builtins.property
    def gitignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional entries to .gitignore.

        :stability: experimental
        '''
        result = self._values.get("gitignore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_projen_04054675.IgnoreFileOptions]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_projen_04054675.IgnoreFileOptions], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_projen_04054675.GitOptions]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_projen_04054675.GitOptions], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Homepage / Website.

        :stability: experimental
        '''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup jest unit tests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("jest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jest_options(self) -> typing.Optional[_projen_javascript_04054675.JestOptions]:
        '''(experimental) Jest options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("jest_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.JestOptions], result)

    @builtins.property
    def jsii_release_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version requirement of ``publib`` which is used to publish modules to npm.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("jsii_release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keywords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Keywords to include in ``package.json``.

        :stability: experimental
        '''
        result = self._values.get("keywords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def libdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Typescript  artifacts output directory.

        :default: "lib"

        :stability: experimental
        '''
        result = self._values.get("libdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''(experimental) License's SPDX identifier.

        See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses.
        Use the ``licensed`` option if you want to no license to be specified.

        :default: "Apache-2.0"

        :stability: experimental
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def licensed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if a license should be added.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("licensed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def logging(self) -> typing.Optional[_projen_04054675.LoggerOptions]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_projen_04054675.LoggerOptions], result)

    @builtins.property
    def major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Major version to release from the default branch.

        If this is specified, we bump the latest version of this major version line.
        If not specified, we bump the global latest version.

        :default: - Major version is not enforced.

        :stability: experimental
        '''
        result = self._values.get("major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum node.js version to require via ``engines`` (inclusive).

        :default: - no max

        :stability: experimental
        '''
        result = self._values.get("max_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mergify(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether mergify should be enabled on this repository or not.

        :default: true

        :deprecated: use ``githubOptions.mergify`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.MergifyOptions]:
        '''(deprecated) Options for mergify.

        :default: - default options

        :deprecated: use ``githubOptions.mergifyOptions`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify_options")
        return typing.cast(typing.Optional[_projen_github_04054675.MergifyOptions], result)

    @builtins.property
    def min_major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Minimal Major version to release.

        This can be useful to set to 1, as breaking changes before the 1.x major
        release are not incrementing the major version number.

        Can not be set together with ``majorVersion``.

        :default: - No minimum version is being enforced

        :stability: experimental
        '''
        result = self._values.get("min_major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive).

        :default: - no "engines" specified

        :stability: experimental
        '''
        result = self._values.get("min_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mutable_build(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Automatically update files modified during builds to pull-request branches.

        This means
        that any files synthesized by projen or e.g. test snapshots will always be up-to-date
        before a PR is merged.

        Implies that PR builds do not have anti-tamper checks.

        :default: true

        :deprecated: - Use ``buildWorkflowOptions.mutableBuild``

        :stability: deprecated
        '''
        result = self._values.get("mutable_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_access(self) -> typing.Optional[_projen_javascript_04054675.NpmAccess]:
        '''(experimental) Access level of the npm package.

        :default:

        - for scoped packages (e.g. ``foo@bar``), the default is
        ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is
        ``NpmAccess.PUBLIC``.

        :stability: experimental
        '''
        result = self._values.get("npm_access")
        return typing.cast(typing.Optional[_projen_javascript_04054675.NpmAccess], result)

    @builtins.property
    def npm_dist_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The npmDistTag to use when publishing from the default branch.

        To set the npm dist-tag for release branches, set the ``npmDistTag`` property
        for each branch.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("npm_dist_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npmignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Additional entries to .npmignore.

        :deprecated: - use ``project.addPackageIgnore``

        :stability: deprecated
        '''
        result = self._values.get("npmignore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def npmignore_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("npmignore_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_ignore_options(self) -> typing.Optional[_projen_04054675.IgnoreFileOptions]:
        '''(experimental) Configuration options for .npmignore file.

        :stability: experimental
        '''
        result = self._values.get("npm_ignore_options")
        return typing.cast(typing.Optional[_projen_04054675.IgnoreFileOptions], result)

    @builtins.property
    def npm_provenance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should provenance statements be generated when the package is published.

        A supported package manager is required to publish a package with npm provenance statements and
        you will need to use a supported CI/CD provider.

        Note that the projen ``Release`` and ``Publisher`` components are using ``publib`` to publish packages,
        which is using npm internally and supports provenance statements independently of the package manager used.

        :default: - true for public packages, false otherwise

        :stability: experimental
        '''
        result = self._values.get("npm_provenance")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_registry(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The host name of the npm registry to publish to.

        Cannot be set together with ``npmRegistryUrl``.

        :deprecated: use ``npmRegistryUrl`` instead

        :stability: deprecated
        '''
        result = self._values.get("npm_registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_registry_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The base URL of the npm package registry.

        Must be a URL (e.g. start with "https://" or "http://")

        :default: "https://registry.npmjs.org"

        :stability: experimental
        '''
        result = self._values.get("npm_registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the NPM token to use when publishing packages.

        :default: "NPM_TOKEN"

        :stability: experimental
        '''
        result = self._values.get("npm_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project. Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``).

        :default: true

        :stability: experimental
        '''
        result = self._values.get("package")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def package_manager(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.NodePackageManager]:
        '''(experimental) The Node Package Manager used to execute scripts.

        :default: NodePackageManager.YARN_CLASSIC

        :stability: experimental
        '''
        result = self._values.get("package_manager")
        return typing.cast(typing.Optional[_projen_javascript_04054675.NodePackageManager], result)

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The "name" in package.json.

        :default: - defaults to project name

        :stability: experimental
        :featured: false
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[_projen_04054675.Project]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_projen_04054675.Project], result)

    @builtins.property
    def peer_dependency_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.PeerDependencyOptions]:
        '''(experimental) Options for ``peerDeps``.

        :stability: experimental
        '''
        result = self._values.get("peer_dependency_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.PeerDependencyOptions], result)

    @builtins.property
    def peer_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Peer dependencies for this module.

        Dependencies listed here are required to
        be installed (and satisfied) by the *consumer* of this library. Using peer
        dependencies allows you to ensure that only a single module of a certain
        library exists in the ``node_modules`` tree of your consumers.

        Note that prior to npm@7, peer dependencies are *not* automatically
        installed, which means that adding peer dependencies to a library will be a
        breaking change for your customers.

        Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is
        enabled by default), projen will automatically add a dev dependency with a
        pinned version for each peer dependency. This will ensure that you build &
        test your module against the lowest peer version required.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("peer_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pnpm_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of PNPM to use if using PNPM as a package manager.

        :default: "7"

        :stability: experimental
        '''
        result = self._values.get("pnpm_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_build_steps(
        self,
    ) -> typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]]:
        '''(experimental) Steps to execute after build as part of the release workflow.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre").

        :default: - normal semantic versions

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prettier(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup prettier.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("prettier")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prettier_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.PrettierOptions]:
        '''(experimental) Prettier options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("prettier_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.PrettierOptions], result)

    @builtins.property
    def project_type(self) -> typing.Optional[_projen_04054675.ProjectType]:
        '''(deprecated) Which type of project this is (library/app).

        :default: ProjectType.UNKNOWN

        :deprecated: no longer supported at the base project level

        :stability: deprecated
        '''
        result = self._values.get("project_type")
        return typing.cast(typing.Optional[_projen_04054675.ProjectType], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projen_credentials(
        self,
    ) -> typing.Optional[_projen_github_04054675.GithubCredentials]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_projen_github_04054675.GithubCredentials], result)

    @builtins.property
    def projen_dev_dependency(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates of "projen" should be installed as a devDependency.

        :default: - true if not a subproject

        :stability: experimental
        '''
        result = self._values.get("projen_dev_dependency")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_js(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation.

        :default: - true if projenrcJson is false

        :stability: experimental
        '''
        result = self._values.get("projenrc_js")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(
        self,
    ) -> typing.Optional[_projen_04054675.ProjenrcJsonOptions]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_projen_04054675.ProjenrcJsonOptions], result)

    @builtins.property
    def projenrc_js_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.ProjenrcOptions]:
        '''(experimental) Options for .projenrc.js.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_js_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.ProjenrcOptions], result)

    @builtins.property
    def projenrc_ts(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use TypeScript for your projenrc file (``.projenrc.ts``).

        :default: false

        :stability: experimental
        :pjnew: true
        '''
        result = self._values.get("projenrc_ts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_ts_options(
        self,
    ) -> typing.Optional[_projen_typescript_04054675.ProjenrcOptions]:
        '''(experimental) Options for .projenrc.ts.

        :stability: experimental
        '''
        result = self._values.get("projenrc_ts_options")
        return typing.cast(typing.Optional[_projen_typescript_04054675.ProjenrcOptions], result)

    @builtins.property
    def projen_token_secret(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows.

        This token needs to have the ``repo``, ``workflows``
        and ``packages`` scope.

        :default: "PROJEN_GITHUB_TOKEN"

        :deprecated: use ``projenCredentials``

        :stability: deprecated
        '''
        result = self._values.get("projen_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projen_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of projen to install.

        :default: - Defaults to the latest version.

        :stability: experimental
        '''
        result = self._values.get("projen_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_dry_run(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Instead of actually publishing to package managers, just print the publishing command.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_tasks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define publishing tasks that can be executed manually as well as workflows.

        Normally, publishing only happens within automated workflows. Enable this
        in order to create a publishing task for each publishing activity.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_tasks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_template(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a GitHub pull request template.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_template")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_template_contents(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The contents of the pull request template.

        :default: - default content

        :stability: experimental
        '''
        result = self._values.get("pull_request_template_contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def readme(self) -> typing.Optional[_projen_04054675.SampleReadmeProps]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[_projen_04054675.SampleReadmeProps], result)

    @builtins.property
    def releasable_commits(self) -> typing.Optional[_projen_04054675.ReleasableCommits]:
        '''(experimental) Find commits that should be considered releasable Used to decide if a release is required.

        :default: ReleasableCommits.everyCommit()

        :stability: experimental
        '''
        result = self._values.get("releasable_commits")
        return typing.cast(typing.Optional[_projen_04054675.ReleasableCommits], result)

    @builtins.property
    def release(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add release management to this project.

        :default: - true (false for subprojects)

        :stability: experimental
        '''
        result = self._values.get("release")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_branches(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _projen_release_04054675.BranchOptions]]:
        '''(experimental) Defines additional release branches.

        A workflow will be created for each
        release branch which will publish releases from commits in this branch.
        Each release branch *must* be assigned a major version number which is used
        to enforce that versions published from that branch always use that major
        version. If multiple branches are used, the ``majorVersion`` field must also
        be provided for the default branch.

        :default:

        - no additional branches are used for release. you can use
        ``addBranch()`` to add additional branches.

        :stability: experimental
        '''
        result = self._values.get("release_branches")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _projen_release_04054675.BranchOptions]], result)

    @builtins.property
    def release_every_commit(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``.

        :default: true

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.continuous()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_every_commit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create a github issue on every failed publishing task.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue_label(self) -> typing.Optional[builtins.str]:
        '''(experimental) The label to apply to issues indicating publish failures.

        Only applies if ``releaseFailureIssue`` is true.

        :default: "failed-release"

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_schedule(self) -> typing.Optional[builtins.str]:
        '''(deprecated) CRON schedule to trigger new releases.

        :default: - no scheduled releases

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.scheduled()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_tag_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Automatically add the given prefix to release tags.

        Useful if you are releasing on multiple branches with overlapping version numbers.
        Note: this prefix is used to detect the latest tagged version
        when bumping, so if you change this on a project with an existing version
        history, you may need to manually tag your latest release
        with the new prefix.

        :default: "v"

        :stability: experimental
        '''
        result = self._values.get("release_tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_to_npm(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically release to npm when new versions are introduced.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_to_npm")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_trigger(
        self,
    ) -> typing.Optional[_projen_release_04054675.ReleaseTrigger]:
        '''(experimental) The release trigger to use.

        :default: - Continuous releases (``ReleaseTrigger.continuous()``)

        :stability: experimental
        '''
        result = self._values.get("release_trigger")
        return typing.cast(typing.Optional[_projen_release_04054675.ReleaseTrigger], result)

    @builtins.property
    def release_workflow(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) DEPRECATED: renamed to ``release``.

        :default: - true if not a subproject

        :deprecated: see ``release``.

        :stability: deprecated
        '''
        result = self._values.get("release_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the default release workflow.

        :default: "release"

        :stability: experimental
        '''
        result = self._values.get("release_workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_workflow_setup_steps(
        self,
    ) -> typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]]:
        '''(experimental) A set of workflow steps to execute in order to setup the workflow container.

        :stability: experimental
        '''
        result = self._values.get("release_workflow_setup_steps")
        return typing.cast(typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(
        self,
    ) -> typing.Optional[_projen_04054675.RenovatebotOptions]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_projen_04054675.RenovatebotOptions], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''(experimental) The repository is the location where the actual code for your package lives.

        See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository

        :stability: experimental
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.

        :stability: experimental
        '''
        result = self._values.get("repository_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_code(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate one-time sample in ``src/`` and ``test/`` if there are no files there.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sample_code")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def scoped_packages_options(
        self,
    ) -> typing.Optional[typing.List[_projen_javascript_04054675.ScopedPackagesOptions]]:
        '''(experimental) Options for privately hosted scoped packages.

        :default: - fetch all scoped packages from the public npm registry

        :stability: experimental
        '''
        result = self._values.get("scoped_packages_options")
        return typing.cast(typing.Optional[typing.List[_projen_javascript_04054675.ScopedPackagesOptions]], result)

    @builtins.property
    def scripts(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(deprecated) npm scripts to include.

        If a script has the same name as a standard script,
        the standard script will be overwritten.
        Also adds the script as a task.

        :default: {}

        :deprecated: use ``project.addTask()`` or ``package.setScript()``

        :stability: deprecated
        '''
        result = self._values.get("scripts")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def srcdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Typescript sources directory.

        :default: "src"

        :stability: experimental
        '''
        result = self._values.get("srcdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stability(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Stability.

        :stability: experimental
        '''
        result = self._values.get("stability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stale(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Auto-close of stale issues and pull request.

        See ``staleOptions`` for options.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stale")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale_options(self) -> typing.Optional[_projen_github_04054675.StaleOptions]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional[_projen_github_04054675.StaleOptions], result)

    @builtins.property
    def testdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Jest tests directory.

        Tests files should be named ``xxx.test.ts``.
        If this directory is under ``srcdir`` (e.g. ``src/test``, ``src/__tests__``),
        then tests are going to be compiled into ``lib/`` and executed as javascript.
        If the test directory is outside of ``src``, then we configure jest to
        compile the code in-memory.

        :default: "test"

        :stability: experimental
        '''
        result = self._values.get("testdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tsconfig(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.TypescriptConfigOptions]:
        '''(experimental) Custom TSConfig.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("tsconfig")
        return typing.cast(typing.Optional[_projen_javascript_04054675.TypescriptConfigOptions], result)

    @builtins.property
    def tsconfig_dev(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.TypescriptConfigOptions]:
        '''(experimental) Custom tsconfig options for the development tsconfig.json file (used for testing).

        :default: - use the production tsconfig options

        :stability: experimental
        '''
        result = self._values.get("tsconfig_dev")
        return typing.cast(typing.Optional[_projen_javascript_04054675.TypescriptConfigOptions], result)

    @builtins.property
    def tsconfig_dev_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the development tsconfig.json file.

        :default: "tsconfig.dev.json"

        :stability: experimental
        '''
        result = self._values.get("tsconfig_dev_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ts_jest_options(
        self,
    ) -> typing.Optional[_projen_typescript_04054675.TsJestOptions]:
        '''(experimental) Options for ts-jest.

        :stability: experimental
        '''
        result = self._values.get("ts_jest_options")
        return typing.cast(typing.Optional[_projen_typescript_04054675.TsJestOptions], result)

    @builtins.property
    def typescript_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) TypeScript version to use.

        NOTE: Typescript is not semantically versioned and should remain on the
        same minor, so we recommend using a ``~`` dependency (e.g. ``~1.2.3``).

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("typescript_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def versionrc_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Custom configuration used when creating changelog with standard-version package.

        Given values either append to default configuration or overwrite values in it.

        :default: - standard configuration applicable for GitHub repositories

        :stability: experimental
        '''
        result = self._values.get("versionrc_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def vscode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable VSCode integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("vscode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow_bootstrap_steps(
        self,
    ) -> typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]]:
        '''(experimental) Workflow steps to use in order to bootstrap this repo.

        :default: "yarn install --frozen-lockfile && yarn projen"

        :stability: experimental
        '''
        result = self._values.get("workflow_bootstrap_steps")
        return typing.cast(typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]], result)

    @builtins.property
    def workflow_container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Container image to use for GitHub workflows.

        :default: - default image

        :stability: experimental
        '''
        result = self._values.get("workflow_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_git_identity(
        self,
    ) -> typing.Optional[_projen_github_04054675.GitIdentity]:
        '''(experimental) The git identity to use in workflows.

        :default: - GitHub Actions

        :stability: experimental
        '''
        result = self._values.get("workflow_git_identity")
        return typing.cast(typing.Optional[_projen_github_04054675.GitIdentity], result)

    @builtins.property
    def workflow_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The node version to use in GitHub workflows.

        :default: - same as ``minNodeVersion``

        :stability: experimental
        '''
        result = self._values.get("workflow_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_package_cache(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable Node.js package cache in GitHub workflows.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("workflow_package_cache")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow_runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workflow_runs_on_group(
        self,
    ) -> typing.Optional[_projen_04054675.GroupRunnerOptions]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on_group")
        return typing.cast(typing.Optional[_projen_04054675.GroupRunnerOptions], result)

    @builtins.property
    def yarn_berry_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.YarnBerryOptions]:
        '''(experimental) Options for Yarn Berry.

        :default: - Yarn Berry v4 with all default options

        :stability: experimental
        '''
        result = self._values.get("yarn_berry_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.YarnBerryOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TypeScriptProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.WorkspaceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "additional_packages": "additionalPackages",
        "link_local_workspace_bins": "linkLocalWorkspaceBins",
        "yarn": "yarn",
    },
)
class WorkspaceConfig:
    def __init__(
        self,
        *,
        additional_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        link_local_workspace_bins: typing.Optional[builtins.bool] = None,
        yarn: typing.Optional[typing.Union["YarnWorkspaceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Workspace configurations.

        :param additional_packages: List of additional package globs to include in the workspace. All packages which are parented by the monorepo are automatically added to the workspace, but you can use this property to specify any additional paths to packages which may not be managed by projen.
        :param link_local_workspace_bins: Links all local workspace project bins so they can be used for local development. Package bins are only linked when installed from the registry, however it is very useful for monorepo development to also utilize these bin scripts. When enabled, this flag will recursively link all bins from packages.json files to the root node_modules/.bin.
        :param yarn: Yarn workspace config.

        :see: https://classic.yarnpkg.com/lang/en/docs/workspaces/
        '''
        if isinstance(yarn, dict):
            yarn = YarnWorkspaceConfig(**yarn)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b872fab3c01261b61bb1ba4e216c6063540ecf4ca12c8b063f16badde10abf)
            check_type(argname="argument additional_packages", value=additional_packages, expected_type=type_hints["additional_packages"])
            check_type(argname="argument link_local_workspace_bins", value=link_local_workspace_bins, expected_type=type_hints["link_local_workspace_bins"])
            check_type(argname="argument yarn", value=yarn, expected_type=type_hints["yarn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_packages is not None:
            self._values["additional_packages"] = additional_packages
        if link_local_workspace_bins is not None:
            self._values["link_local_workspace_bins"] = link_local_workspace_bins
        if yarn is not None:
            self._values["yarn"] = yarn

    @builtins.property
    def additional_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of additional package globs to include in the workspace.

        All packages which are parented by the monorepo are automatically added to the workspace, but you can use this
        property to specify any additional paths to packages which may not be managed by projen.
        '''
        result = self._values.get("additional_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def link_local_workspace_bins(self) -> typing.Optional[builtins.bool]:
        '''Links all local workspace project bins so they can be used for local development.

        Package bins are only linked when installed from the registry, however it is very useful
        for monorepo development to also utilize these bin scripts. When enabled, this flag will
        recursively link all bins from packages.json files to the root node_modules/.bin.
        '''
        result = self._values.get("link_local_workspace_bins")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def yarn(self) -> typing.Optional["YarnWorkspaceConfig"]:
        '''Yarn workspace config.'''
        result = self._values.get("yarn")
        return typing.cast(typing.Optional["YarnWorkspaceConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.YarnWorkspaceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disable_no_hoist_bundled": "disableNoHoistBundled",
        "no_hoist": "noHoist",
    },
)
class YarnWorkspaceConfig:
    def __init__(
        self,
        *,
        disable_no_hoist_bundled: typing.Optional[builtins.bool] = None,
        no_hoist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Yarn related workspace config.

        :param disable_no_hoist_bundled: Disable automatically applying ``noHoist`` logic for all sub-project "bundledDependencies". Default: false
        :param no_hoist: List of package globs to exclude from hoisting in the workspace.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df49722742021b2cc598380915e034283683e99ee86edaeca83859f793d616ea)
            check_type(argname="argument disable_no_hoist_bundled", value=disable_no_hoist_bundled, expected_type=type_hints["disable_no_hoist_bundled"])
            check_type(argname="argument no_hoist", value=no_hoist, expected_type=type_hints["no_hoist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_no_hoist_bundled is not None:
            self._values["disable_no_hoist_bundled"] = disable_no_hoist_bundled
        if no_hoist is not None:
            self._values["no_hoist"] = no_hoist

    @builtins.property
    def disable_no_hoist_bundled(self) -> typing.Optional[builtins.bool]:
        '''Disable automatically applying ``noHoist`` logic for all sub-project "bundledDependencies".

        :default: false
        '''
        result = self._values.get("disable_no_hoist_bundled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_hoist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of package globs to exclude from hoisting in the workspace.

        :see: https://classic.yarnpkg.com/blog/2018/02/15/nohoist/
        '''
        result = self._values.get("no_hoist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YarnWorkspaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.MonorepoPythonProjectOptions",
    jsii_struct_bases=[PythonProjectOptions],
    name_mapping={
        "module_name": "moduleName",
        "name": "name",
        "author_email": "authorEmail",
        "author_name": "authorName",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "classifiers": "classifiers",
        "clobber": "clobber",
        "commit_generated": "commitGenerated",
        "deps": "deps",
        "description": "description",
        "dev_container": "devContainer",
        "dev_deps": "devDeps",
        "github": "github",
        "github_options": "githubOptions",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "gitpod": "gitpod",
        "homepage": "homepage",
        "license": "license",
        "logging": "logging",
        "mergify": "mergify",
        "mergify_options": "mergifyOptions",
        "outdir": "outdir",
        "package_name": "packageName",
        "parent": "parent",
        "poetry_options": "poetryOptions",
        "project_type": "projectType",
        "projen_command": "projenCommand",
        "projen_credentials": "projenCredentials",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "projenrc_python_options": "projenrcPythonOptions",
        "projen_token_secret": "projenTokenSecret",
        "pytest": "pytest",
        "pytest_options": "pytestOptions",
        "python_exec": "pythonExec",
        "readme": "readme",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "sample": "sample",
        "setup_config": "setupConfig",
        "setuptools": "setuptools",
        "stale": "stale",
        "stale_options": "staleOptions",
        "version": "version",
        "vscode": "vscode",
        "default_release_branch": "defaultReleaseBranch",
        "license_options": "licenseOptions",
    },
)
class MonorepoPythonProjectOptions(PythonProjectOptions):
    def __init__(
        self,
        *,
        module_name: builtins.str,
        name: builtins.str,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        package_name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        poetry_options: typing.Optional[typing.Union[_projen_python_04054675.PoetryPyprojectOptionsWithoutDeps, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_projen_04054675.ProjectType] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_python_options: typing.Optional[typing.Union[_projen_python_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        pytest: typing.Optional[builtins.bool] = None,
        pytest_options: typing.Optional[typing.Union[_projen_python_04054675.PytestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        python_exec: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        sample: typing.Optional[builtins.bool] = None,
        setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        setuptools: typing.Optional[builtins.bool] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
        default_release_branch: typing.Optional[builtins.str] = None,
        license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Configuration options for the NxMonorepoPythonProject.

        :param module_name: Default: $PYTHON_MODULE_NAME
        :param name: Default: $BASEDIR
        :param author_email: (experimental) Author's e-mail. Default: $GIT_USER_EMAIL
        :param author_name: (experimental) Author's name. Default: $GIT_USER_NAME
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param classifiers: (experimental) A list of PyPI trove classifiers that describe the project.
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) A short description of the package.
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param dev_deps: (experimental) List of dev dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDevDependency()``. Default: []
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param homepage: (experimental) A URL to the website of the project.
        :param license: (experimental) License of this package as an SPDX identifier.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param package_name: (experimental) Package name.
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param poetry_options: (experimental) Additional options to set for poetry if using poetry.
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param projenrc_python_options: (experimental) Options related to projenrc in python. Default: - default options
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param pytest: (experimental) Include pytest tests. Default: true
        :param pytest_options: (experimental) pytest options. Default: - defaults
        :param python_exec: (experimental) Path to the python executable to use. Default: "python"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param setup_config: (experimental) Additional fields to pass in the setup() function if using setuptools.
        :param setuptools: (experimental) Use setuptools with a setup.py script for packaging and publishing. Default: - true, unless poetry is true, then false
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param version: (experimental) Version of the package. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param default_release_branch: 
        :param license_options: Default license to apply to all PDK managed packages. Default: Apache-2.0
        '''
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _projen_github_04054675.AutoApproveOptions(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _projen_github_04054675.AutoMergeOptions(**auto_merge_options)
        if isinstance(github_options, dict):
            github_options = _projen_github_04054675.GitHubOptions(**github_options)
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _projen_04054675.IgnoreFileOptions(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _projen_04054675.GitOptions(**git_options)
        if isinstance(logging, dict):
            logging = _projen_04054675.LoggerOptions(**logging)
        if isinstance(mergify_options, dict):
            mergify_options = _projen_github_04054675.MergifyOptions(**mergify_options)
        if isinstance(poetry_options, dict):
            poetry_options = _projen_python_04054675.PoetryPyprojectOptionsWithoutDeps(**poetry_options)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _projen_04054675.ProjenrcJsonOptions(**projenrc_json_options)
        if isinstance(projenrc_python_options, dict):
            projenrc_python_options = _projen_python_04054675.ProjenrcOptions(**projenrc_python_options)
        if isinstance(pytest_options, dict):
            pytest_options = _projen_python_04054675.PytestOptions(**pytest_options)
        if isinstance(readme, dict):
            readme = _projen_04054675.SampleReadmeProps(**readme)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _projen_04054675.RenovatebotOptions(**renovatebot_options)
        if isinstance(stale_options, dict):
            stale_options = _projen_github_04054675.StaleOptions(**stale_options)
        if isinstance(license_options, dict):
            license_options = LicenseOptions(**license_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea87dc3723259fcfab289a5ee69cc3ffb4716eafa280a8abe4df20c5b147630)
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument mergify", value=mergify, expected_type=type_hints["mergify"])
            check_type(argname="argument mergify_options", value=mergify_options, expected_type=type_hints["mergify_options"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument poetry_options", value=poetry_options, expected_type=type_hints["poetry_options"])
            check_type(argname="argument project_type", value=project_type, expected_type=type_hints["project_type"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument projenrc_python_options", value=projenrc_python_options, expected_type=type_hints["projenrc_python_options"])
            check_type(argname="argument projen_token_secret", value=projen_token_secret, expected_type=type_hints["projen_token_secret"])
            check_type(argname="argument pytest", value=pytest, expected_type=type_hints["pytest"])
            check_type(argname="argument pytest_options", value=pytest_options, expected_type=type_hints["pytest_options"])
            check_type(argname="argument python_exec", value=python_exec, expected_type=type_hints["python_exec"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument setup_config", value=setup_config, expected_type=type_hints["setup_config"])
            check_type(argname="argument setuptools", value=setuptools, expected_type=type_hints["setuptools"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument default_release_branch", value=default_release_branch, expected_type=type_hints["default_release_branch"])
            check_type(argname="argument license_options", value=license_options, expected_type=type_hints["license_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "module_name": module_name,
            "name": name,
        }
        if author_email is not None:
            self._values["author_email"] = author_email
        if author_name is not None:
            self._values["author_name"] = author_name
        if auto_approve_options is not None:
            self._values["auto_approve_options"] = auto_approve_options
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if auto_merge_options is not None:
            self._values["auto_merge_options"] = auto_merge_options
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if clobber is not None:
            self._values["clobber"] = clobber
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if github is not None:
            self._values["github"] = github
        if github_options is not None:
            self._values["github_options"] = github_options
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if gitpod is not None:
            self._values["gitpod"] = gitpod
        if homepage is not None:
            self._values["homepage"] = homepage
        if license is not None:
            self._values["license"] = license
        if logging is not None:
            self._values["logging"] = logging
        if mergify is not None:
            self._values["mergify"] = mergify
        if mergify_options is not None:
            self._values["mergify_options"] = mergify_options
        if outdir is not None:
            self._values["outdir"] = outdir
        if package_name is not None:
            self._values["package_name"] = package_name
        if parent is not None:
            self._values["parent"] = parent
        if poetry_options is not None:
            self._values["poetry_options"] = poetry_options
        if project_type is not None:
            self._values["project_type"] = project_type
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if projenrc_python_options is not None:
            self._values["projenrc_python_options"] = projenrc_python_options
        if projen_token_secret is not None:
            self._values["projen_token_secret"] = projen_token_secret
        if pytest is not None:
            self._values["pytest"] = pytest
        if pytest_options is not None:
            self._values["pytest_options"] = pytest_options
        if python_exec is not None:
            self._values["python_exec"] = python_exec
        if readme is not None:
            self._values["readme"] = readme
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if sample is not None:
            self._values["sample"] = sample
        if setup_config is not None:
            self._values["setup_config"] = setup_config
        if setuptools is not None:
            self._values["setuptools"] = setuptools
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if version is not None:
            self._values["version"] = version
        if vscode is not None:
            self._values["vscode"] = vscode
        if default_release_branch is not None:
            self._values["default_release_branch"] = default_release_branch
        if license_options is not None:
            self._values["license_options"] = license_options

    @builtins.property
    def module_name(self) -> builtins.str:
        '''
        :default: $PYTHON_MODULE_NAME
        '''
        result = self._values.get("module_name")
        assert result is not None, "Required property 'module_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :default: $BASEDIR
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def author_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's e-mail.

        :default: $GIT_USER_EMAIL

        :stability: experimental
        '''
        result = self._values.get("author_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's name.

        :default: $GIT_USER_NAME

        :stability: experimental
        '''
        result = self._values.get("author_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_approve_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoApproveOptions]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoApproveOptions], result)

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable automatic merging on GitHub.

        Has no effect if ``github.mergify``
        is set to false.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoMergeOptions]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoMergeOptions], result)

    @builtins.property
    def classifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of PyPI trove classifiers that describe the project.

        :stability: experimental
        '''
        result = self._values.get("classifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def clobber(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a ``clobber`` task which resets the repo to origin.

        :default: - true, but false for subprojects

        :stability: experimental
        '''
        result = self._values.get("clobber")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of runtime dependencies for this project. Dependencies use the format: ``<module>@<semver>``.

        Additional dependencies can be added via ``project.addDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A short description of the package.

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dev_container(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a VSCode development environment (used for GitHub Codespaces).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dev_container")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dev_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of dev dependencies for this project. Dependencies use the format: ``<module>@<semver>``.

        Additional dependencies can be added via ``project.addDevDependency()``.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("dev_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def github(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable GitHub integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github_options(self) -> typing.Optional[_projen_github_04054675.GitHubOptions]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional[_projen_github_04054675.GitHubOptions], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_projen_04054675.IgnoreFileOptions]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_projen_04054675.IgnoreFileOptions], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_projen_04054675.GitOptions]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_projen_04054675.GitOptions], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''(experimental) A URL to the website of the project.

        :stability: experimental
        '''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''(experimental) License of this package as an SPDX identifier.

        :stability: experimental
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(self) -> typing.Optional[_projen_04054675.LoggerOptions]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_projen_04054675.LoggerOptions], result)

    @builtins.property
    def mergify(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether mergify should be enabled on this repository or not.

        :default: true

        :deprecated: use ``githubOptions.mergify`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.MergifyOptions]:
        '''(deprecated) Options for mergify.

        :default: - default options

        :deprecated: use ``githubOptions.mergifyOptions`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify_options")
        return typing.cast(typing.Optional[_projen_github_04054675.MergifyOptions], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project. Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package name.

        :stability: experimental
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[_projen_04054675.Project]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_projen_04054675.Project], result)

    @builtins.property
    def poetry_options(
        self,
    ) -> typing.Optional[_projen_python_04054675.PoetryPyprojectOptionsWithoutDeps]:
        '''(experimental) Additional options to set for poetry if using poetry.

        :stability: experimental
        '''
        result = self._values.get("poetry_options")
        return typing.cast(typing.Optional[_projen_python_04054675.PoetryPyprojectOptionsWithoutDeps], result)

    @builtins.property
    def project_type(self) -> typing.Optional[_projen_04054675.ProjectType]:
        '''(deprecated) Which type of project this is (library/app).

        :default: ProjectType.UNKNOWN

        :deprecated: no longer supported at the base project level

        :stability: deprecated
        '''
        result = self._values.get("project_type")
        return typing.cast(typing.Optional[_projen_04054675.ProjectType], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projen_credentials(
        self,
    ) -> typing.Optional[_projen_github_04054675.GithubCredentials]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_projen_github_04054675.GithubCredentials], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(
        self,
    ) -> typing.Optional[_projen_04054675.ProjenrcJsonOptions]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_projen_04054675.ProjenrcJsonOptions], result)

    @builtins.property
    def projenrc_python_options(
        self,
    ) -> typing.Optional[_projen_python_04054675.ProjenrcOptions]:
        '''(experimental) Options related to projenrc in python.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_python_options")
        return typing.cast(typing.Optional[_projen_python_04054675.ProjenrcOptions], result)

    @builtins.property
    def projen_token_secret(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows.

        This token needs to have the ``repo``, ``workflows``
        and ``packages`` scope.

        :default: "PROJEN_GITHUB_TOKEN"

        :deprecated: use ``projenCredentials``

        :stability: deprecated
        '''
        result = self._values.get("projen_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pytest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include pytest tests.

        :default: true

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("pytest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pytest_options(self) -> typing.Optional[_projen_python_04054675.PytestOptions]:
        '''(experimental) pytest options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("pytest_options")
        return typing.cast(typing.Optional[_projen_python_04054675.PytestOptions], result)

    @builtins.property
    def python_exec(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the python executable to use.

        :default: "python"

        :stability: experimental
        '''
        result = self._values.get("python_exec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme(self) -> typing.Optional[_projen_04054675.SampleReadmeProps]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[_projen_04054675.SampleReadmeProps], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(
        self,
    ) -> typing.Optional[_projen_04054675.RenovatebotOptions]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_projen_04054675.RenovatebotOptions], result)

    @builtins.property
    def sample(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include sample code and test if the relevant directories don't exist.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sample")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def setup_config(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional fields to pass in the setup() function if using setuptools.

        :stability: experimental
        '''
        result = self._values.get("setup_config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def setuptools(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use setuptools with a setup.py script for packaging and publishing.

        :default: - true, unless poetry is true, then false

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("setuptools")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Auto-close of stale issues and pull request.

        See ``staleOptions`` for options.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stale")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale_options(self) -> typing.Optional[_projen_github_04054675.StaleOptions]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional[_projen_github_04054675.StaleOptions], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of the package.

        :default: "0.1.0"

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vscode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable VSCode integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("vscode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default_release_branch(self) -> typing.Optional[builtins.str]:
        result = self._values.get("default_release_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_options(self) -> typing.Optional[LicenseOptions]:
        '''Default license to apply to all PDK managed packages.

        :default: Apache-2.0
        '''
        result = self._values.get("license_options")
        return typing.cast(typing.Optional[LicenseOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonorepoPythonProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.monorepo.MonorepoTsProjectOptions",
    jsii_struct_bases=[TypeScriptProjectOptions],
    name_mapping={
        "name": "name",
        "allow_library_dependencies": "allowLibraryDependencies",
        "artifacts_directory": "artifactsDirectory",
        "author_email": "authorEmail",
        "author_name": "authorName",
        "author_organization": "authorOrganization",
        "author_url": "authorUrl",
        "auto_approve_options": "autoApproveOptions",
        "auto_approve_upgrades": "autoApproveUpgrades",
        "auto_detect_bin": "autoDetectBin",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "bin": "bin",
        "bugs_email": "bugsEmail",
        "bugs_url": "bugsUrl",
        "build_workflow": "buildWorkflow",
        "build_workflow_options": "buildWorkflowOptions",
        "build_workflow_triggers": "buildWorkflowTriggers",
        "bundled_deps": "bundledDeps",
        "bundler_options": "bundlerOptions",
        "check_licenses": "checkLicenses",
        "clobber": "clobber",
        "code_artifact_options": "codeArtifactOptions",
        "code_cov": "codeCov",
        "code_cov_token_secret": "codeCovTokenSecret",
        "commit_generated": "commitGenerated",
        "copyright_owner": "copyrightOwner",
        "copyright_period": "copyrightPeriod",
        "default_release_branch": "defaultReleaseBranch",
        "dependabot": "dependabot",
        "dependabot_options": "dependabotOptions",
        "deps": "deps",
        "deps_upgrade": "depsUpgrade",
        "deps_upgrade_options": "depsUpgradeOptions",
        "description": "description",
        "dev_container": "devContainer",
        "dev_deps": "devDeps",
        "disable_tsconfig": "disableTsconfig",
        "disable_tsconfig_dev": "disableTsconfigDev",
        "docgen": "docgen",
        "docs_directory": "docsDirectory",
        "entrypoint": "entrypoint",
        "entrypoint_types": "entrypointTypes",
        "eslint": "eslint",
        "eslint_options": "eslintOptions",
        "github": "github",
        "github_options": "githubOptions",
        "gitignore": "gitignore",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "gitpod": "gitpod",
        "homepage": "homepage",
        "jest": "jest",
        "jest_options": "jestOptions",
        "jsii_release_version": "jsiiReleaseVersion",
        "keywords": "keywords",
        "libdir": "libdir",
        "license": "license",
        "licensed": "licensed",
        "logging": "logging",
        "major_version": "majorVersion",
        "max_node_version": "maxNodeVersion",
        "mergify": "mergify",
        "mergify_options": "mergifyOptions",
        "min_major_version": "minMajorVersion",
        "min_node_version": "minNodeVersion",
        "mutable_build": "mutableBuild",
        "npm_access": "npmAccess",
        "npm_dist_tag": "npmDistTag",
        "npmignore": "npmignore",
        "npmignore_enabled": "npmignoreEnabled",
        "npm_ignore_options": "npmIgnoreOptions",
        "npm_provenance": "npmProvenance",
        "npm_registry": "npmRegistry",
        "npm_registry_url": "npmRegistryUrl",
        "npm_token_secret": "npmTokenSecret",
        "outdir": "outdir",
        "package": "package",
        "package_manager": "packageManager",
        "package_name": "packageName",
        "parent": "parent",
        "peer_dependency_options": "peerDependencyOptions",
        "peer_deps": "peerDeps",
        "pnpm_version": "pnpmVersion",
        "post_build_steps": "postBuildSteps",
        "prerelease": "prerelease",
        "prettier": "prettier",
        "prettier_options": "prettierOptions",
        "project_type": "projectType",
        "projen_command": "projenCommand",
        "projen_credentials": "projenCredentials",
        "projen_dev_dependency": "projenDevDependency",
        "projenrc_js": "projenrcJs",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "projenrc_js_options": "projenrcJsOptions",
        "projenrc_ts": "projenrcTs",
        "projenrc_ts_options": "projenrcTsOptions",
        "projen_token_secret": "projenTokenSecret",
        "projen_version": "projenVersion",
        "publish_dry_run": "publishDryRun",
        "publish_tasks": "publishTasks",
        "pull_request_template": "pullRequestTemplate",
        "pull_request_template_contents": "pullRequestTemplateContents",
        "readme": "readme",
        "releasable_commits": "releasableCommits",
        "release": "release",
        "release_branches": "releaseBranches",
        "release_every_commit": "releaseEveryCommit",
        "release_failure_issue": "releaseFailureIssue",
        "release_failure_issue_label": "releaseFailureIssueLabel",
        "release_schedule": "releaseSchedule",
        "release_tag_prefix": "releaseTagPrefix",
        "release_to_npm": "releaseToNpm",
        "release_trigger": "releaseTrigger",
        "release_workflow": "releaseWorkflow",
        "release_workflow_name": "releaseWorkflowName",
        "release_workflow_setup_steps": "releaseWorkflowSetupSteps",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "repository": "repository",
        "repository_directory": "repositoryDirectory",
        "sample_code": "sampleCode",
        "scoped_packages_options": "scopedPackagesOptions",
        "scripts": "scripts",
        "srcdir": "srcdir",
        "stability": "stability",
        "stale": "stale",
        "stale_options": "staleOptions",
        "testdir": "testdir",
        "tsconfig": "tsconfig",
        "tsconfig_dev": "tsconfigDev",
        "tsconfig_dev_file": "tsconfigDevFile",
        "ts_jest_options": "tsJestOptions",
        "typescript_version": "typescriptVersion",
        "versionrc_options": "versionrcOptions",
        "vscode": "vscode",
        "workflow_bootstrap_steps": "workflowBootstrapSteps",
        "workflow_container_image": "workflowContainerImage",
        "workflow_git_identity": "workflowGitIdentity",
        "workflow_node_version": "workflowNodeVersion",
        "workflow_package_cache": "workflowPackageCache",
        "workflow_runs_on": "workflowRunsOn",
        "workflow_runs_on_group": "workflowRunsOnGroup",
        "yarn_berry_options": "yarnBerryOptions",
        "disable_node_warnings": "disableNodeWarnings",
        "license_options": "licenseOptions",
        "monorepo_upgrade_deps": "monorepoUpgradeDeps",
        "monorepo_upgrade_deps_options": "monorepoUpgradeDepsOptions",
        "workspace_config": "workspaceConfig",
    },
)
class MonorepoTsProjectOptions(TypeScriptProjectOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        artifacts_directory: typing.Optional[builtins.str] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        author_organization: typing.Optional[builtins.bool] = None,
        author_url: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_approve_upgrades: typing.Optional[builtins.bool] = None,
        auto_detect_bin: typing.Optional[builtins.bool] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bugs_email: typing.Optional[builtins.str] = None,
        bugs_url: typing.Optional[builtins.str] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        copyright_owner: typing.Optional[builtins.str] = None,
        copyright_period: typing.Optional[builtins.str] = None,
        default_release_branch: typing.Optional[builtins.str] = None,
        dependabot: typing.Optional[builtins.bool] = None,
        dependabot_options: typing.Optional[typing.Union[_projen_github_04054675.DependabotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        deps_upgrade: typing.Optional[builtins.bool] = None,
        deps_upgrade_options: typing.Optional[typing.Union[_projen_javascript_04054675.UpgradeDependenciesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        disable_tsconfig: typing.Optional[builtins.bool] = None,
        disable_tsconfig_dev: typing.Optional[builtins.bool] = None,
        docgen: typing.Optional[builtins.bool] = None,
        docs_directory: typing.Optional[builtins.str] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        entrypoint_types: typing.Optional[builtins.str] = None,
        eslint: typing.Optional[builtins.bool] = None,
        eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        libdir: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        licensed: typing.Optional[builtins.bool] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        major_version: typing.Optional[jsii.Number] = None,
        max_node_version: typing.Optional[builtins.str] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        min_node_version: typing.Optional[builtins.str] = None,
        mutable_build: typing.Optional[builtins.bool] = None,
        npm_access: typing.Optional[_projen_javascript_04054675.NpmAccess] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        npmignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        npmignore_enabled: typing.Optional[builtins.bool] = None,
        npm_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        npm_provenance: typing.Optional[builtins.bool] = None,
        npm_registry: typing.Optional[builtins.str] = None,
        npm_registry_url: typing.Optional[builtins.str] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        outdir: typing.Optional[builtins.str] = None,
        package: typing.Optional[builtins.bool] = None,
        package_manager: typing.Optional[_projen_javascript_04054675.NodePackageManager] = None,
        package_name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        peer_dependency_options: typing.Optional[typing.Union[_projen_javascript_04054675.PeerDependencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        pnpm_version: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        prettier: typing.Optional[builtins.bool] = None,
        prettier_options: typing.Optional[typing.Union[_projen_javascript_04054675.PrettierOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_projen_04054675.ProjectType] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
        projen_dev_dependency: typing.Optional[builtins.bool] = None,
        projenrc_js: typing.Optional[builtins.bool] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_js_options: typing.Optional[typing.Union[_projen_javascript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projenrc_ts: typing.Optional[builtins.bool] = None,
        projenrc_ts_options: typing.Optional[typing.Union[_projen_typescript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        projen_version: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        pull_request_template: typing.Optional[builtins.bool] = None,
        pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
        releasable_commits: typing.Optional[_projen_04054675.ReleasableCommits] = None,
        release: typing.Optional[builtins.bool] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[_projen_release_04054675.BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_to_npm: typing.Optional[builtins.bool] = None,
        release_trigger: typing.Optional[_projen_release_04054675.ReleaseTrigger] = None,
        release_workflow: typing.Optional[builtins.bool] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_directory: typing.Optional[builtins.str] = None,
        sample_code: typing.Optional[builtins.bool] = None,
        scoped_packages_options: typing.Optional[typing.Sequence[typing.Union[_projen_javascript_04054675.ScopedPackagesOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        srcdir: typing.Optional[builtins.str] = None,
        stability: typing.Optional[builtins.str] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        testdir: typing.Optional[builtins.str] = None,
        tsconfig: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        tsconfig_dev_file: typing.Optional[builtins.str] = None,
        ts_jest_options: typing.Optional[typing.Union[_projen_typescript_04054675.TsJestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        typescript_version: typing.Optional[builtins.str] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_git_identity: typing.Optional[typing.Union[_projen_github_04054675.GitIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_package_cache: typing.Optional[builtins.bool] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_projen_04054675.GroupRunnerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        yarn_berry_options: typing.Optional[typing.Union[_projen_javascript_04054675.YarnBerryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        disable_node_warnings: typing.Optional[builtins.bool] = None,
        license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        monorepo_upgrade_deps: typing.Optional[builtins.bool] = None,
        monorepo_upgrade_deps_options: typing.Optional[typing.Union[MonorepoUpgradeDepsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_config: typing.Optional[typing.Union[WorkspaceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Configuration options for the MonorepoTsProject.

        :param name: Default: $BASEDIR
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param artifacts_directory: (experimental) A directory which will contain build artifacts. Default: "dist"
        :param author_email: (experimental) Author's e-mail.
        :param author_name: (experimental) Author's name.
        :param author_organization: (experimental) Is the author an organization.
        :param author_url: (experimental) Author's URL / Website.
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_approve_upgrades: (experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configued). Throw if set to true but ``autoApproveOptions`` are not defined. Default: - true
        :param auto_detect_bin: (experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section. Default: true
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param bin: (experimental) Binary programs vended with your module. You can use this option to add/customize how binaries are represented in your ``package.json``, but unless ``autoDetectBin`` is ``false``, every executable file under ``bin`` will automatically be added to this section.
        :param bugs_email: (experimental) The email address to which issues should be reported.
        :param bugs_url: (experimental) The url to your project's issue tracker.
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_options: (experimental) Options for PR build workflow.
        :param build_workflow_triggers: (deprecated) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param check_licenses: (experimental) Configure which licenses should be deemed acceptable for use by dependencies. This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered. Default: - no license checks are run during the build and all licenses will be accepted
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v4 A secret is required for private repos. Configured with ``@codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories. Default: - if this option is not specified, only public repositories are supported
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param copyright_owner: (experimental) License copyright owner. Default: - defaults to the value of authorName or "" if ``authorName`` is undefined.
        :param copyright_period: (experimental) The copyright years to put in the LICENSE file. Default: - current year
        :param default_release_branch: (experimental) The name of the main release branch. Default: "main"
        :param dependabot: (experimental) Use dependabot to handle dependency upgrades. Cannot be used in conjunction with ``depsUpgrade``. Default: false
        :param dependabot_options: (experimental) Options for dependabot. Default: - default options
        :param deps: (experimental) Runtime dependencies of this module. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param deps_upgrade: (experimental) Use tasks and github workflows to handle dependency upgrades. Cannot be used in conjunction with ``dependabot``. Default: true
        :param deps_upgrade_options: (experimental) Options for ``UpgradeDependencies``. Default: - default options
        :param description: (experimental) The description is just a string that helps people understand the purpose of the package. It can be used when searching for packages in a package manager as well. See https://classic.yarnpkg.com/en/docs/package-json/#toc-description
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param dev_deps: (experimental) Build dependencies for this module. These dependencies will only be available in your build environment but will not be fetched when this module is consumed. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param disable_tsconfig: (experimental) Do not generate a ``tsconfig.json`` file (used by jsii projects since tsconfig.json is generated by the jsii compiler). Default: false
        :param disable_tsconfig_dev: (experimental) Do not generate a ``tsconfig.dev.json`` file. Default: false
        :param docgen: (experimental) Docgen by Typedoc. Default: false
        :param docs_directory: (experimental) Docs directory. Default: "docs"
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json. Default: "lib/index.js"
        :param entrypoint_types: (experimental) The .d.ts file that includes the type declarations for this module. Default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)
        :param eslint: (experimental) Setup eslint. Default: true
        :param eslint_options: (experimental) Eslint options. Default: - opinionated default options
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param homepage: (experimental) Package's Homepage / Website.
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param libdir: (experimental) Typescript artifacts output directory. Default: "lib"
        :param license: (experimental) License's SPDX identifier. See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses. Use the ``licensed`` option if you want to no license to be specified. Default: "Apache-2.0"
        :param licensed: (experimental) Indicates if a license should be added. Default: true
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param max_node_version: (experimental) Minimum node.js version to require via ``engines`` (inclusive). Default: - no max
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param min_node_version: (experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive). Default: - no "engines" specified
        :param mutable_build: (deprecated) Automatically update files modified during builds to pull-request branches. This means that any files synthesized by projen or e.g. test snapshots will always be up-to-date before a PR is merged. Implies that PR builds do not have anti-tamper checks. Default: true
        :param npm_access: (experimental) Access level of the npm package. Default: - for scoped packages (e.g. ``foo@bar``), the default is ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is ``NpmAccess.PUBLIC``.
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param npmignore: (deprecated) Additional entries to .npmignore.
        :param npmignore_enabled: (experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs. Default: true
        :param npm_ignore_options: (experimental) Configuration options for .npmignore file.
        :param npm_provenance: (experimental) Should provenance statements be generated when the package is published. A supported package manager is required to publish a package with npm provenance statements and you will need to use a supported CI/CD provider. Note that the projen ``Release`` and ``Publisher`` components are using ``publib`` to publish packages, which is using npm internally and supports provenance statements independently of the package manager used. Default: - true for public packages, false otherwise
        :param npm_registry: (deprecated) The host name of the npm registry to publish to. Cannot be set together with ``npmRegistryUrl``.
        :param npm_registry_url: (experimental) The base URL of the npm package registry. Must be a URL (e.g. start with "https://" or "http://") Default: "https://registry.npmjs.org"
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: "NPM_TOKEN"
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param package: (experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``). Default: true
        :param package_manager: (experimental) The Node Package Manager used to execute scripts. Default: NodePackageManager.YARN_CLASSIC
        :param package_name: (experimental) The "name" in package.json. Default: - defaults to project name
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param peer_dependency_options: (experimental) Options for ``peerDeps``.
        :param peer_deps: (experimental) Peer dependencies for this module. Dependencies listed here are required to be installed (and satisfied) by the *consumer* of this library. Using peer dependencies allows you to ensure that only a single module of a certain library exists in the ``node_modules`` tree of your consumers. Note that prior to npm@7, peer dependencies are *not* automatically installed, which means that adding peer dependencies to a library will be a breaking change for your customers. Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is enabled by default), projen will automatically add a dev dependency with a pinned version for each peer dependency. This will ensure that you build & test your module against the lowest peer version required. Default: []
        :param pnpm_version: (experimental) The version of PNPM to use if using PNPM as a package manager. Default: "7"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param prettier: (experimental) Setup prettier. Default: false
        :param prettier_options: (experimental) Prettier options. Default: - default options
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projen_dev_dependency: (experimental) Indicates of "projen" should be installed as a devDependency. Default: - true if not a subproject
        :param projenrc_js: (experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation. Default: - true if projenrcJson is false
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param projenrc_js_options: (experimental) Options for .projenrc.js. Default: - default options
        :param projenrc_ts: (experimental) Use TypeScript for your projenrc file (``.projenrc.ts``). Default: false
        :param projenrc_ts_options: (experimental) Options for .projenrc.ts.
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param projen_version: (experimental) Version of projen to install. Default: - Defaults to the latest version.
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param pull_request_template: (experimental) Include a GitHub pull request template. Default: true
        :param pull_request_template_contents: (experimental) The contents of the pull request template. Default: - default content
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release: (experimental) Add release management to this project. Default: - true (false for subprojects)
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_every_commit: (deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_schedule: (deprecated) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_to_npm: (experimental) Automatically release to npm when new versions are introduced. Default: false
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow: (deprecated) DEPRECATED: renamed to ``release``. Default: - true if not a subproject
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param repository: (experimental) The repository is the location where the actual code for your package lives. See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository
        :param repository_directory: (experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.
        :param sample_code: (experimental) Generate one-time sample in ``src/`` and ``test/`` if there are no files there. Default: true
        :param scoped_packages_options: (experimental) Options for privately hosted scoped packages. Default: - fetch all scoped packages from the public npm registry
        :param scripts: (deprecated) npm scripts to include. If a script has the same name as a standard script, the standard script will be overwritten. Also adds the script as a task. Default: {}
        :param srcdir: (experimental) Typescript sources directory. Default: "src"
        :param stability: (experimental) Package's Stability.
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param testdir: (experimental) Jest tests directory. Tests files should be named ``xxx.test.ts``. If this directory is under ``srcdir`` (e.g. ``src/test``, ``src/__tests__``), then tests are going to be compiled into ``lib/`` and executed as javascript. If the test directory is outside of ``src``, then we configure jest to compile the code in-memory. Default: "test"
        :param tsconfig: (experimental) Custom TSConfig. Default: - default options
        :param tsconfig_dev: (experimental) Custom tsconfig options for the development tsconfig.json file (used for testing). Default: - use the production tsconfig options
        :param tsconfig_dev_file: (experimental) The name of the development tsconfig.json file. Default: "tsconfig.dev.json"
        :param ts_jest_options: (experimental) Options for ts-jest.
        :param typescript_version: (experimental) TypeScript version to use. NOTE: Typescript is not semantically versioned and should remain on the same minor, so we recommend using a ``~`` dependency (e.g. ``~1.2.3``). Default: "latest"
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with standard-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param workflow_bootstrap_steps: (experimental) Workflow steps to use in order to bootstrap this repo. Default: "yarn install --frozen-lockfile && yarn projen"
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_git_identity: (experimental) The git identity to use in workflows. Default: - GitHub Actions
        :param workflow_node_version: (experimental) The node version to use in GitHub workflows. Default: - same as ``minNodeVersion``
        :param workflow_package_cache: (experimental) Enable Node.js package cache in GitHub workflows. Default: false
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param yarn_berry_options: (experimental) Options for Yarn Berry. Default: - Yarn Berry v4 with all default options
        :param disable_node_warnings: Disable node warnings from being emitted during build tasks. Default: false
        :param license_options: Default license to apply to all PDK managed packages. Default: Apache-2.0
        :param monorepo_upgrade_deps: Whether to include an upgrade-deps task at the root of the monorepo which will upgrade all dependencies. Default: true
        :param monorepo_upgrade_deps_options: Monorepo Upgrade Deps options. This is only used if monorepoUpgradeDeps is true. Default: undefined
        :param workspace_config: Configuration for workspace.
        '''
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _projen_github_04054675.AutoApproveOptions(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _projen_github_04054675.AutoMergeOptions(**auto_merge_options)
        if isinstance(build_workflow_options, dict):
            build_workflow_options = _projen_javascript_04054675.BuildWorkflowOptions(**build_workflow_options)
        if isinstance(build_workflow_triggers, dict):
            build_workflow_triggers = _projen_github_workflows_04054675.Triggers(**build_workflow_triggers)
        if isinstance(bundler_options, dict):
            bundler_options = _projen_javascript_04054675.BundlerOptions(**bundler_options)
        if isinstance(check_licenses, dict):
            check_licenses = _projen_javascript_04054675.LicenseCheckerOptions(**check_licenses)
        if isinstance(code_artifact_options, dict):
            code_artifact_options = _projen_javascript_04054675.CodeArtifactOptions(**code_artifact_options)
        if isinstance(dependabot_options, dict):
            dependabot_options = _projen_github_04054675.DependabotOptions(**dependabot_options)
        if isinstance(deps_upgrade_options, dict):
            deps_upgrade_options = _projen_javascript_04054675.UpgradeDependenciesOptions(**deps_upgrade_options)
        if isinstance(eslint_options, dict):
            eslint_options = _projen_javascript_04054675.EslintOptions(**eslint_options)
        if isinstance(github_options, dict):
            github_options = _projen_github_04054675.GitHubOptions(**github_options)
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _projen_04054675.IgnoreFileOptions(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _projen_04054675.GitOptions(**git_options)
        if isinstance(jest_options, dict):
            jest_options = _projen_javascript_04054675.JestOptions(**jest_options)
        if isinstance(logging, dict):
            logging = _projen_04054675.LoggerOptions(**logging)
        if isinstance(mergify_options, dict):
            mergify_options = _projen_github_04054675.MergifyOptions(**mergify_options)
        if isinstance(npm_ignore_options, dict):
            npm_ignore_options = _projen_04054675.IgnoreFileOptions(**npm_ignore_options)
        if isinstance(peer_dependency_options, dict):
            peer_dependency_options = _projen_javascript_04054675.PeerDependencyOptions(**peer_dependency_options)
        if isinstance(prettier_options, dict):
            prettier_options = _projen_javascript_04054675.PrettierOptions(**prettier_options)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _projen_04054675.ProjenrcJsonOptions(**projenrc_json_options)
        if isinstance(projenrc_js_options, dict):
            projenrc_js_options = _projen_javascript_04054675.ProjenrcOptions(**projenrc_js_options)
        if isinstance(projenrc_ts_options, dict):
            projenrc_ts_options = _projen_typescript_04054675.ProjenrcOptions(**projenrc_ts_options)
        if isinstance(readme, dict):
            readme = _projen_04054675.SampleReadmeProps(**readme)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _projen_04054675.RenovatebotOptions(**renovatebot_options)
        if isinstance(stale_options, dict):
            stale_options = _projen_github_04054675.StaleOptions(**stale_options)
        if isinstance(tsconfig, dict):
            tsconfig = _projen_javascript_04054675.TypescriptConfigOptions(**tsconfig)
        if isinstance(tsconfig_dev, dict):
            tsconfig_dev = _projen_javascript_04054675.TypescriptConfigOptions(**tsconfig_dev)
        if isinstance(ts_jest_options, dict):
            ts_jest_options = _projen_typescript_04054675.TsJestOptions(**ts_jest_options)
        if isinstance(workflow_git_identity, dict):
            workflow_git_identity = _projen_github_04054675.GitIdentity(**workflow_git_identity)
        if isinstance(workflow_runs_on_group, dict):
            workflow_runs_on_group = _projen_04054675.GroupRunnerOptions(**workflow_runs_on_group)
        if isinstance(yarn_berry_options, dict):
            yarn_berry_options = _projen_javascript_04054675.YarnBerryOptions(**yarn_berry_options)
        if isinstance(license_options, dict):
            license_options = LicenseOptions(**license_options)
        if isinstance(monorepo_upgrade_deps_options, dict):
            monorepo_upgrade_deps_options = MonorepoUpgradeDepsOptions(**monorepo_upgrade_deps_options)
        if isinstance(workspace_config, dict):
            workspace_config = WorkspaceConfig(**workspace_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd6505f1b256e8137d338ed4a05a0fefbc62ac331551c10781a424be0bb1d4c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_library_dependencies", value=allow_library_dependencies, expected_type=type_hints["allow_library_dependencies"])
            check_type(argname="argument artifacts_directory", value=artifacts_directory, expected_type=type_hints["artifacts_directory"])
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument author_organization", value=author_organization, expected_type=type_hints["author_organization"])
            check_type(argname="argument author_url", value=author_url, expected_type=type_hints["author_url"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_approve_upgrades", value=auto_approve_upgrades, expected_type=type_hints["auto_approve_upgrades"])
            check_type(argname="argument auto_detect_bin", value=auto_detect_bin, expected_type=type_hints["auto_detect_bin"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument bin", value=bin, expected_type=type_hints["bin"])
            check_type(argname="argument bugs_email", value=bugs_email, expected_type=type_hints["bugs_email"])
            check_type(argname="argument bugs_url", value=bugs_url, expected_type=type_hints["bugs_url"])
            check_type(argname="argument build_workflow", value=build_workflow, expected_type=type_hints["build_workflow"])
            check_type(argname="argument build_workflow_options", value=build_workflow_options, expected_type=type_hints["build_workflow_options"])
            check_type(argname="argument build_workflow_triggers", value=build_workflow_triggers, expected_type=type_hints["build_workflow_triggers"])
            check_type(argname="argument bundled_deps", value=bundled_deps, expected_type=type_hints["bundled_deps"])
            check_type(argname="argument bundler_options", value=bundler_options, expected_type=type_hints["bundler_options"])
            check_type(argname="argument check_licenses", value=check_licenses, expected_type=type_hints["check_licenses"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument code_cov", value=code_cov, expected_type=type_hints["code_cov"])
            check_type(argname="argument code_cov_token_secret", value=code_cov_token_secret, expected_type=type_hints["code_cov_token_secret"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument copyright_owner", value=copyright_owner, expected_type=type_hints["copyright_owner"])
            check_type(argname="argument copyright_period", value=copyright_period, expected_type=type_hints["copyright_period"])
            check_type(argname="argument default_release_branch", value=default_release_branch, expected_type=type_hints["default_release_branch"])
            check_type(argname="argument dependabot", value=dependabot, expected_type=type_hints["dependabot"])
            check_type(argname="argument dependabot_options", value=dependabot_options, expected_type=type_hints["dependabot_options"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument deps_upgrade", value=deps_upgrade, expected_type=type_hints["deps_upgrade"])
            check_type(argname="argument deps_upgrade_options", value=deps_upgrade_options, expected_type=type_hints["deps_upgrade_options"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument disable_tsconfig", value=disable_tsconfig, expected_type=type_hints["disable_tsconfig"])
            check_type(argname="argument disable_tsconfig_dev", value=disable_tsconfig_dev, expected_type=type_hints["disable_tsconfig_dev"])
            check_type(argname="argument docgen", value=docgen, expected_type=type_hints["docgen"])
            check_type(argname="argument docs_directory", value=docs_directory, expected_type=type_hints["docs_directory"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument entrypoint_types", value=entrypoint_types, expected_type=type_hints["entrypoint_types"])
            check_type(argname="argument eslint", value=eslint, expected_type=type_hints["eslint"])
            check_type(argname="argument eslint_options", value=eslint_options, expected_type=type_hints["eslint_options"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument gitignore", value=gitignore, expected_type=type_hints["gitignore"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument jest", value=jest, expected_type=type_hints["jest"])
            check_type(argname="argument jest_options", value=jest_options, expected_type=type_hints["jest_options"])
            check_type(argname="argument jsii_release_version", value=jsii_release_version, expected_type=type_hints["jsii_release_version"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument libdir", value=libdir, expected_type=type_hints["libdir"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument licensed", value=licensed, expected_type=type_hints["licensed"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument max_node_version", value=max_node_version, expected_type=type_hints["max_node_version"])
            check_type(argname="argument mergify", value=mergify, expected_type=type_hints["mergify"])
            check_type(argname="argument mergify_options", value=mergify_options, expected_type=type_hints["mergify_options"])
            check_type(argname="argument min_major_version", value=min_major_version, expected_type=type_hints["min_major_version"])
            check_type(argname="argument min_node_version", value=min_node_version, expected_type=type_hints["min_node_version"])
            check_type(argname="argument mutable_build", value=mutable_build, expected_type=type_hints["mutable_build"])
            check_type(argname="argument npm_access", value=npm_access, expected_type=type_hints["npm_access"])
            check_type(argname="argument npm_dist_tag", value=npm_dist_tag, expected_type=type_hints["npm_dist_tag"])
            check_type(argname="argument npmignore", value=npmignore, expected_type=type_hints["npmignore"])
            check_type(argname="argument npmignore_enabled", value=npmignore_enabled, expected_type=type_hints["npmignore_enabled"])
            check_type(argname="argument npm_ignore_options", value=npm_ignore_options, expected_type=type_hints["npm_ignore_options"])
            check_type(argname="argument npm_provenance", value=npm_provenance, expected_type=type_hints["npm_provenance"])
            check_type(argname="argument npm_registry", value=npm_registry, expected_type=type_hints["npm_registry"])
            check_type(argname="argument npm_registry_url", value=npm_registry_url, expected_type=type_hints["npm_registry_url"])
            check_type(argname="argument npm_token_secret", value=npm_token_secret, expected_type=type_hints["npm_token_secret"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument package", value=package, expected_type=type_hints["package"])
            check_type(argname="argument package_manager", value=package_manager, expected_type=type_hints["package_manager"])
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument peer_dependency_options", value=peer_dependency_options, expected_type=type_hints["peer_dependency_options"])
            check_type(argname="argument peer_deps", value=peer_deps, expected_type=type_hints["peer_deps"])
            check_type(argname="argument pnpm_version", value=pnpm_version, expected_type=type_hints["pnpm_version"])
            check_type(argname="argument post_build_steps", value=post_build_steps, expected_type=type_hints["post_build_steps"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument prettier", value=prettier, expected_type=type_hints["prettier"])
            check_type(argname="argument prettier_options", value=prettier_options, expected_type=type_hints["prettier_options"])
            check_type(argname="argument project_type", value=project_type, expected_type=type_hints["project_type"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument projen_dev_dependency", value=projen_dev_dependency, expected_type=type_hints["projen_dev_dependency"])
            check_type(argname="argument projenrc_js", value=projenrc_js, expected_type=type_hints["projenrc_js"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument projenrc_js_options", value=projenrc_js_options, expected_type=type_hints["projenrc_js_options"])
            check_type(argname="argument projenrc_ts", value=projenrc_ts, expected_type=type_hints["projenrc_ts"])
            check_type(argname="argument projenrc_ts_options", value=projenrc_ts_options, expected_type=type_hints["projenrc_ts_options"])
            check_type(argname="argument projen_token_secret", value=projen_token_secret, expected_type=type_hints["projen_token_secret"])
            check_type(argname="argument projen_version", value=projen_version, expected_type=type_hints["projen_version"])
            check_type(argname="argument publish_dry_run", value=publish_dry_run, expected_type=type_hints["publish_dry_run"])
            check_type(argname="argument publish_tasks", value=publish_tasks, expected_type=type_hints["publish_tasks"])
            check_type(argname="argument pull_request_template", value=pull_request_template, expected_type=type_hints["pull_request_template"])
            check_type(argname="argument pull_request_template_contents", value=pull_request_template_contents, expected_type=type_hints["pull_request_template_contents"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument releasable_commits", value=releasable_commits, expected_type=type_hints["releasable_commits"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument release_branches", value=release_branches, expected_type=type_hints["release_branches"])
            check_type(argname="argument release_every_commit", value=release_every_commit, expected_type=type_hints["release_every_commit"])
            check_type(argname="argument release_failure_issue", value=release_failure_issue, expected_type=type_hints["release_failure_issue"])
            check_type(argname="argument release_failure_issue_label", value=release_failure_issue_label, expected_type=type_hints["release_failure_issue_label"])
            check_type(argname="argument release_schedule", value=release_schedule, expected_type=type_hints["release_schedule"])
            check_type(argname="argument release_tag_prefix", value=release_tag_prefix, expected_type=type_hints["release_tag_prefix"])
            check_type(argname="argument release_to_npm", value=release_to_npm, expected_type=type_hints["release_to_npm"])
            check_type(argname="argument release_trigger", value=release_trigger, expected_type=type_hints["release_trigger"])
            check_type(argname="argument release_workflow", value=release_workflow, expected_type=type_hints["release_workflow"])
            check_type(argname="argument release_workflow_name", value=release_workflow_name, expected_type=type_hints["release_workflow_name"])
            check_type(argname="argument release_workflow_setup_steps", value=release_workflow_setup_steps, expected_type=type_hints["release_workflow_setup_steps"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument repository_directory", value=repository_directory, expected_type=type_hints["repository_directory"])
            check_type(argname="argument sample_code", value=sample_code, expected_type=type_hints["sample_code"])
            check_type(argname="argument scoped_packages_options", value=scoped_packages_options, expected_type=type_hints["scoped_packages_options"])
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
            check_type(argname="argument srcdir", value=srcdir, expected_type=type_hints["srcdir"])
            check_type(argname="argument stability", value=stability, expected_type=type_hints["stability"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument testdir", value=testdir, expected_type=type_hints["testdir"])
            check_type(argname="argument tsconfig", value=tsconfig, expected_type=type_hints["tsconfig"])
            check_type(argname="argument tsconfig_dev", value=tsconfig_dev, expected_type=type_hints["tsconfig_dev"])
            check_type(argname="argument tsconfig_dev_file", value=tsconfig_dev_file, expected_type=type_hints["tsconfig_dev_file"])
            check_type(argname="argument ts_jest_options", value=ts_jest_options, expected_type=type_hints["ts_jest_options"])
            check_type(argname="argument typescript_version", value=typescript_version, expected_type=type_hints["typescript_version"])
            check_type(argname="argument versionrc_options", value=versionrc_options, expected_type=type_hints["versionrc_options"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument workflow_bootstrap_steps", value=workflow_bootstrap_steps, expected_type=type_hints["workflow_bootstrap_steps"])
            check_type(argname="argument workflow_container_image", value=workflow_container_image, expected_type=type_hints["workflow_container_image"])
            check_type(argname="argument workflow_git_identity", value=workflow_git_identity, expected_type=type_hints["workflow_git_identity"])
            check_type(argname="argument workflow_node_version", value=workflow_node_version, expected_type=type_hints["workflow_node_version"])
            check_type(argname="argument workflow_package_cache", value=workflow_package_cache, expected_type=type_hints["workflow_package_cache"])
            check_type(argname="argument workflow_runs_on", value=workflow_runs_on, expected_type=type_hints["workflow_runs_on"])
            check_type(argname="argument workflow_runs_on_group", value=workflow_runs_on_group, expected_type=type_hints["workflow_runs_on_group"])
            check_type(argname="argument yarn_berry_options", value=yarn_berry_options, expected_type=type_hints["yarn_berry_options"])
            check_type(argname="argument disable_node_warnings", value=disable_node_warnings, expected_type=type_hints["disable_node_warnings"])
            check_type(argname="argument license_options", value=license_options, expected_type=type_hints["license_options"])
            check_type(argname="argument monorepo_upgrade_deps", value=monorepo_upgrade_deps, expected_type=type_hints["monorepo_upgrade_deps"])
            check_type(argname="argument monorepo_upgrade_deps_options", value=monorepo_upgrade_deps_options, expected_type=type_hints["monorepo_upgrade_deps_options"])
            check_type(argname="argument workspace_config", value=workspace_config, expected_type=type_hints["workspace_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_library_dependencies is not None:
            self._values["allow_library_dependencies"] = allow_library_dependencies
        if artifacts_directory is not None:
            self._values["artifacts_directory"] = artifacts_directory
        if author_email is not None:
            self._values["author_email"] = author_email
        if author_name is not None:
            self._values["author_name"] = author_name
        if author_organization is not None:
            self._values["author_organization"] = author_organization
        if author_url is not None:
            self._values["author_url"] = author_url
        if auto_approve_options is not None:
            self._values["auto_approve_options"] = auto_approve_options
        if auto_approve_upgrades is not None:
            self._values["auto_approve_upgrades"] = auto_approve_upgrades
        if auto_detect_bin is not None:
            self._values["auto_detect_bin"] = auto_detect_bin
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if auto_merge_options is not None:
            self._values["auto_merge_options"] = auto_merge_options
        if bin is not None:
            self._values["bin"] = bin
        if bugs_email is not None:
            self._values["bugs_email"] = bugs_email
        if bugs_url is not None:
            self._values["bugs_url"] = bugs_url
        if build_workflow is not None:
            self._values["build_workflow"] = build_workflow
        if build_workflow_options is not None:
            self._values["build_workflow_options"] = build_workflow_options
        if build_workflow_triggers is not None:
            self._values["build_workflow_triggers"] = build_workflow_triggers
        if bundled_deps is not None:
            self._values["bundled_deps"] = bundled_deps
        if bundler_options is not None:
            self._values["bundler_options"] = bundler_options
        if check_licenses is not None:
            self._values["check_licenses"] = check_licenses
        if clobber is not None:
            self._values["clobber"] = clobber
        if code_artifact_options is not None:
            self._values["code_artifact_options"] = code_artifact_options
        if code_cov is not None:
            self._values["code_cov"] = code_cov
        if code_cov_token_secret is not None:
            self._values["code_cov_token_secret"] = code_cov_token_secret
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if copyright_owner is not None:
            self._values["copyright_owner"] = copyright_owner
        if copyright_period is not None:
            self._values["copyright_period"] = copyright_period
        if default_release_branch is not None:
            self._values["default_release_branch"] = default_release_branch
        if dependabot is not None:
            self._values["dependabot"] = dependabot
        if dependabot_options is not None:
            self._values["dependabot_options"] = dependabot_options
        if deps is not None:
            self._values["deps"] = deps
        if deps_upgrade is not None:
            self._values["deps_upgrade"] = deps_upgrade
        if deps_upgrade_options is not None:
            self._values["deps_upgrade_options"] = deps_upgrade_options
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if disable_tsconfig is not None:
            self._values["disable_tsconfig"] = disable_tsconfig
        if disable_tsconfig_dev is not None:
            self._values["disable_tsconfig_dev"] = disable_tsconfig_dev
        if docgen is not None:
            self._values["docgen"] = docgen
        if docs_directory is not None:
            self._values["docs_directory"] = docs_directory
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if entrypoint_types is not None:
            self._values["entrypoint_types"] = entrypoint_types
        if eslint is not None:
            self._values["eslint"] = eslint
        if eslint_options is not None:
            self._values["eslint_options"] = eslint_options
        if github is not None:
            self._values["github"] = github
        if github_options is not None:
            self._values["github_options"] = github_options
        if gitignore is not None:
            self._values["gitignore"] = gitignore
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if gitpod is not None:
            self._values["gitpod"] = gitpod
        if homepage is not None:
            self._values["homepage"] = homepage
        if jest is not None:
            self._values["jest"] = jest
        if jest_options is not None:
            self._values["jest_options"] = jest_options
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if keywords is not None:
            self._values["keywords"] = keywords
        if libdir is not None:
            self._values["libdir"] = libdir
        if license is not None:
            self._values["license"] = license
        if licensed is not None:
            self._values["licensed"] = licensed
        if logging is not None:
            self._values["logging"] = logging
        if major_version is not None:
            self._values["major_version"] = major_version
        if max_node_version is not None:
            self._values["max_node_version"] = max_node_version
        if mergify is not None:
            self._values["mergify"] = mergify
        if mergify_options is not None:
            self._values["mergify_options"] = mergify_options
        if min_major_version is not None:
            self._values["min_major_version"] = min_major_version
        if min_node_version is not None:
            self._values["min_node_version"] = min_node_version
        if mutable_build is not None:
            self._values["mutable_build"] = mutable_build
        if npm_access is not None:
            self._values["npm_access"] = npm_access
        if npm_dist_tag is not None:
            self._values["npm_dist_tag"] = npm_dist_tag
        if npmignore is not None:
            self._values["npmignore"] = npmignore
        if npmignore_enabled is not None:
            self._values["npmignore_enabled"] = npmignore_enabled
        if npm_ignore_options is not None:
            self._values["npm_ignore_options"] = npm_ignore_options
        if npm_provenance is not None:
            self._values["npm_provenance"] = npm_provenance
        if npm_registry is not None:
            self._values["npm_registry"] = npm_registry
        if npm_registry_url is not None:
            self._values["npm_registry_url"] = npm_registry_url
        if npm_token_secret is not None:
            self._values["npm_token_secret"] = npm_token_secret
        if outdir is not None:
            self._values["outdir"] = outdir
        if package is not None:
            self._values["package"] = package
        if package_manager is not None:
            self._values["package_manager"] = package_manager
        if package_name is not None:
            self._values["package_name"] = package_name
        if parent is not None:
            self._values["parent"] = parent
        if peer_dependency_options is not None:
            self._values["peer_dependency_options"] = peer_dependency_options
        if peer_deps is not None:
            self._values["peer_deps"] = peer_deps
        if pnpm_version is not None:
            self._values["pnpm_version"] = pnpm_version
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if prettier is not None:
            self._values["prettier"] = prettier
        if prettier_options is not None:
            self._values["prettier_options"] = prettier_options
        if project_type is not None:
            self._values["project_type"] = project_type
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if projen_dev_dependency is not None:
            self._values["projen_dev_dependency"] = projen_dev_dependency
        if projenrc_js is not None:
            self._values["projenrc_js"] = projenrc_js
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if projenrc_js_options is not None:
            self._values["projenrc_js_options"] = projenrc_js_options
        if projenrc_ts is not None:
            self._values["projenrc_ts"] = projenrc_ts
        if projenrc_ts_options is not None:
            self._values["projenrc_ts_options"] = projenrc_ts_options
        if projen_token_secret is not None:
            self._values["projen_token_secret"] = projen_token_secret
        if projen_version is not None:
            self._values["projen_version"] = projen_version
        if publish_dry_run is not None:
            self._values["publish_dry_run"] = publish_dry_run
        if publish_tasks is not None:
            self._values["publish_tasks"] = publish_tasks
        if pull_request_template is not None:
            self._values["pull_request_template"] = pull_request_template
        if pull_request_template_contents is not None:
            self._values["pull_request_template_contents"] = pull_request_template_contents
        if readme is not None:
            self._values["readme"] = readme
        if releasable_commits is not None:
            self._values["releasable_commits"] = releasable_commits
        if release is not None:
            self._values["release"] = release
        if release_branches is not None:
            self._values["release_branches"] = release_branches
        if release_every_commit is not None:
            self._values["release_every_commit"] = release_every_commit
        if release_failure_issue is not None:
            self._values["release_failure_issue"] = release_failure_issue
        if release_failure_issue_label is not None:
            self._values["release_failure_issue_label"] = release_failure_issue_label
        if release_schedule is not None:
            self._values["release_schedule"] = release_schedule
        if release_tag_prefix is not None:
            self._values["release_tag_prefix"] = release_tag_prefix
        if release_to_npm is not None:
            self._values["release_to_npm"] = release_to_npm
        if release_trigger is not None:
            self._values["release_trigger"] = release_trigger
        if release_workflow is not None:
            self._values["release_workflow"] = release_workflow
        if release_workflow_name is not None:
            self._values["release_workflow_name"] = release_workflow_name
        if release_workflow_setup_steps is not None:
            self._values["release_workflow_setup_steps"] = release_workflow_setup_steps
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if repository is not None:
            self._values["repository"] = repository
        if repository_directory is not None:
            self._values["repository_directory"] = repository_directory
        if sample_code is not None:
            self._values["sample_code"] = sample_code
        if scoped_packages_options is not None:
            self._values["scoped_packages_options"] = scoped_packages_options
        if scripts is not None:
            self._values["scripts"] = scripts
        if srcdir is not None:
            self._values["srcdir"] = srcdir
        if stability is not None:
            self._values["stability"] = stability
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if testdir is not None:
            self._values["testdir"] = testdir
        if tsconfig is not None:
            self._values["tsconfig"] = tsconfig
        if tsconfig_dev is not None:
            self._values["tsconfig_dev"] = tsconfig_dev
        if tsconfig_dev_file is not None:
            self._values["tsconfig_dev_file"] = tsconfig_dev_file
        if ts_jest_options is not None:
            self._values["ts_jest_options"] = ts_jest_options
        if typescript_version is not None:
            self._values["typescript_version"] = typescript_version
        if versionrc_options is not None:
            self._values["versionrc_options"] = versionrc_options
        if vscode is not None:
            self._values["vscode"] = vscode
        if workflow_bootstrap_steps is not None:
            self._values["workflow_bootstrap_steps"] = workflow_bootstrap_steps
        if workflow_container_image is not None:
            self._values["workflow_container_image"] = workflow_container_image
        if workflow_git_identity is not None:
            self._values["workflow_git_identity"] = workflow_git_identity
        if workflow_node_version is not None:
            self._values["workflow_node_version"] = workflow_node_version
        if workflow_package_cache is not None:
            self._values["workflow_package_cache"] = workflow_package_cache
        if workflow_runs_on is not None:
            self._values["workflow_runs_on"] = workflow_runs_on
        if workflow_runs_on_group is not None:
            self._values["workflow_runs_on_group"] = workflow_runs_on_group
        if yarn_berry_options is not None:
            self._values["yarn_berry_options"] = yarn_berry_options
        if disable_node_warnings is not None:
            self._values["disable_node_warnings"] = disable_node_warnings
        if license_options is not None:
            self._values["license_options"] = license_options
        if monorepo_upgrade_deps is not None:
            self._values["monorepo_upgrade_deps"] = monorepo_upgrade_deps
        if monorepo_upgrade_deps_options is not None:
            self._values["monorepo_upgrade_deps_options"] = monorepo_upgrade_deps_options
        if workspace_config is not None:
            self._values["workspace_config"] = workspace_config

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :default: $BASEDIR
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_library_dependencies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``.

        This is normally only allowed for libraries. For apps, there's no meaning
        for specifying these.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("allow_library_dependencies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def artifacts_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) A directory which will contain build artifacts.

        :default: "dist"

        :stability: experimental
        '''
        result = self._values.get("artifacts_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's e-mail.

        :stability: experimental
        '''
        result = self._values.get("author_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's name.

        :stability: experimental
        '''
        result = self._values.get("author_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_organization(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Is the author an organization.

        :stability: experimental
        '''
        result = self._values.get("author_organization")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def author_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's URL / Website.

        :stability: experimental
        '''
        result = self._values.get("author_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_approve_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoApproveOptions]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoApproveOptions], result)

    @builtins.property
    def auto_approve_upgrades(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configued).

        Throw if set to true but ``autoApproveOptions`` are not defined.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("auto_approve_upgrades")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_detect_bin(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_detect_bin")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable automatic merging on GitHub.

        Has no effect if ``github.mergify``
        is set to false.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.AutoMergeOptions]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional[_projen_github_04054675.AutoMergeOptions], result)

    @builtins.property
    def bin(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Binary programs vended with your module.

        You can use this option to add/customize how binaries are represented in
        your ``package.json``, but unless ``autoDetectBin`` is ``false``, every
        executable file under ``bin`` will automatically be added to this section.

        :stability: experimental
        '''
        result = self._values.get("bin")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bugs_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) The email address to which issues should be reported.

        :stability: experimental
        '''
        result = self._values.get("bugs_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bugs_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The url to your project's issue tracker.

        :stability: experimental
        '''
        result = self._values.get("bugs_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define a GitHub workflow for building PRs.

        :default: - true if not a subproject

        :stability: experimental
        '''
        result = self._values.get("build_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def build_workflow_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.BuildWorkflowOptions]:
        '''(experimental) Options for PR build workflow.

        :stability: experimental
        '''
        result = self._values.get("build_workflow_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.BuildWorkflowOptions], result)

    @builtins.property
    def build_workflow_triggers(
        self,
    ) -> typing.Optional[_projen_github_workflows_04054675.Triggers]:
        '''(deprecated) Build workflow triggers.

        :default: "{ pullRequest: {}, workflowDispatch: {} }"

        :deprecated: - Use ``buildWorkflowOptions.workflowTriggers``

        :stability: deprecated
        '''
        result = self._values.get("build_workflow_triggers")
        return typing.cast(typing.Optional[_projen_github_workflows_04054675.Triggers], result)

    @builtins.property
    def bundled_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of dependencies to bundle into this module.

        These modules will be
        added both to the ``dependencies`` section and ``bundledDependencies`` section of
        your ``package.json``.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :stability: experimental
        '''
        result = self._values.get("bundled_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bundler_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.BundlerOptions]:
        '''(experimental) Options for ``Bundler``.

        :stability: experimental
        '''
        result = self._values.get("bundler_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.BundlerOptions], result)

    @builtins.property
    def check_licenses(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.LicenseCheckerOptions]:
        '''(experimental) Configure which licenses should be deemed acceptable for use by dependencies.

        This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered.

        :default: - no license checks are run during the build and all licenses will be accepted

        :stability: experimental
        '''
        result = self._values.get("check_licenses")
        return typing.cast(typing.Optional[_projen_javascript_04054675.LicenseCheckerOptions], result)

    @builtins.property
    def clobber(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a ``clobber`` task which resets the repo to origin.

        :default: - true, but false for subprojects

        :stability: experimental
        '''
        result = self._values.get("clobber")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def code_artifact_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.CodeArtifactOptions]:
        '''(experimental) Options for npm packages using AWS CodeArtifact.

        This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("code_artifact_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.CodeArtifactOptions], result)

    @builtins.property
    def code_cov(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v4 A secret is required for private repos. Configured with ``@codeCovTokenSecret``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("code_cov")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def code_cov_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories.

        :default: - if this option is not specified, only public repositories are supported

        :stability: experimental
        '''
        result = self._values.get("code_cov_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def copyright_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) License copyright owner.

        :default: - defaults to the value of authorName or "" if ``authorName`` is undefined.

        :stability: experimental
        '''
        result = self._values.get("copyright_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copyright_period(self) -> typing.Optional[builtins.str]:
        '''(experimental) The copyright years to put in the LICENSE file.

        :default: - current year

        :stability: experimental
        '''
        result = self._values.get("copyright_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_release_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the main release branch.

        :default: "main"

        :stability: experimental
        '''
        result = self._values.get("default_release_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependabot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use dependabot to handle dependency upgrades.

        Cannot be used in conjunction with ``depsUpgrade``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dependabot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dependabot_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.DependabotOptions]:
        '''(experimental) Options for dependabot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("dependabot_options")
        return typing.cast(typing.Optional[_projen_github_04054675.DependabotOptions], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Runtime dependencies of this module.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: false
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deps_upgrade(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use tasks and github workflows to handle dependency upgrades.

        Cannot be used in conjunction with ``dependabot``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("deps_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deps_upgrade_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.UpgradeDependenciesOptions]:
        '''(experimental) Options for ``UpgradeDependencies``.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("deps_upgrade_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.UpgradeDependenciesOptions], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description is just a string that helps people understand the purpose of the package.

        It can be used when searching for packages in a package manager as well.
        See https://classic.yarnpkg.com/en/docs/package-json/#toc-description

        :stability: experimental
        :featured: false
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dev_container(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a VSCode development environment (used for GitHub Codespaces).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dev_container")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dev_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Build dependencies for this module.

        These dependencies will only be
        available in your build environment but will not be fetched when this
        module is consumed.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("dev_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disable_tsconfig(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not generate a ``tsconfig.json`` file (used by jsii projects since tsconfig.json is generated by the jsii compiler).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disable_tsconfig")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def disable_tsconfig_dev(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not generate a ``tsconfig.dev.json`` file.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disable_tsconfig_dev")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docgen(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Docgen by Typedoc.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("docgen")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docs_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs directory.

        :default: "docs"

        :stability: experimental
        '''
        result = self._values.get("docs_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json.

        :default: "lib/index.js"

        :stability: experimental
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint_types(self) -> typing.Optional[builtins.str]:
        '''(experimental) The .d.ts file that includes the type declarations for this module.

        :default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)

        :stability: experimental
        '''
        result = self._values.get("entrypoint_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eslint(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup eslint.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("eslint")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def eslint_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.EslintOptions]:
        '''(experimental) Eslint options.

        :default: - opinionated default options

        :stability: experimental
        '''
        result = self._values.get("eslint_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.EslintOptions], result)

    @builtins.property
    def github(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable GitHub integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github_options(self) -> typing.Optional[_projen_github_04054675.GitHubOptions]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional[_projen_github_04054675.GitHubOptions], result)

    @builtins.property
    def gitignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional entries to .gitignore.

        :stability: experimental
        '''
        result = self._values.get("gitignore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_projen_04054675.IgnoreFileOptions]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_projen_04054675.IgnoreFileOptions], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_projen_04054675.GitOptions]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_projen_04054675.GitOptions], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Homepage / Website.

        :stability: experimental
        '''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup jest unit tests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("jest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jest_options(self) -> typing.Optional[_projen_javascript_04054675.JestOptions]:
        '''(experimental) Jest options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("jest_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.JestOptions], result)

    @builtins.property
    def jsii_release_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version requirement of ``publib`` which is used to publish modules to npm.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("jsii_release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keywords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Keywords to include in ``package.json``.

        :stability: experimental
        '''
        result = self._values.get("keywords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def libdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Typescript  artifacts output directory.

        :default: "lib"

        :stability: experimental
        '''
        result = self._values.get("libdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''(experimental) License's SPDX identifier.

        See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses.
        Use the ``licensed`` option if you want to no license to be specified.

        :default: "Apache-2.0"

        :stability: experimental
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def licensed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if a license should be added.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("licensed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def logging(self) -> typing.Optional[_projen_04054675.LoggerOptions]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_projen_04054675.LoggerOptions], result)

    @builtins.property
    def major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Major version to release from the default branch.

        If this is specified, we bump the latest version of this major version line.
        If not specified, we bump the global latest version.

        :default: - Major version is not enforced.

        :stability: experimental
        '''
        result = self._values.get("major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum node.js version to require via ``engines`` (inclusive).

        :default: - no max

        :stability: experimental
        '''
        result = self._values.get("max_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mergify(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether mergify should be enabled on this repository or not.

        :default: true

        :deprecated: use ``githubOptions.mergify`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify_options(
        self,
    ) -> typing.Optional[_projen_github_04054675.MergifyOptions]:
        '''(deprecated) Options for mergify.

        :default: - default options

        :deprecated: use ``githubOptions.mergifyOptions`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify_options")
        return typing.cast(typing.Optional[_projen_github_04054675.MergifyOptions], result)

    @builtins.property
    def min_major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Minimal Major version to release.

        This can be useful to set to 1, as breaking changes before the 1.x major
        release are not incrementing the major version number.

        Can not be set together with ``majorVersion``.

        :default: - No minimum version is being enforced

        :stability: experimental
        '''
        result = self._values.get("min_major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive).

        :default: - no "engines" specified

        :stability: experimental
        '''
        result = self._values.get("min_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mutable_build(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Automatically update files modified during builds to pull-request branches.

        This means
        that any files synthesized by projen or e.g. test snapshots will always be up-to-date
        before a PR is merged.

        Implies that PR builds do not have anti-tamper checks.

        :default: true

        :deprecated: - Use ``buildWorkflowOptions.mutableBuild``

        :stability: deprecated
        '''
        result = self._values.get("mutable_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_access(self) -> typing.Optional[_projen_javascript_04054675.NpmAccess]:
        '''(experimental) Access level of the npm package.

        :default:

        - for scoped packages (e.g. ``foo@bar``), the default is
        ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is
        ``NpmAccess.PUBLIC``.

        :stability: experimental
        '''
        result = self._values.get("npm_access")
        return typing.cast(typing.Optional[_projen_javascript_04054675.NpmAccess], result)

    @builtins.property
    def npm_dist_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The npmDistTag to use when publishing from the default branch.

        To set the npm dist-tag for release branches, set the ``npmDistTag`` property
        for each branch.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("npm_dist_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npmignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Additional entries to .npmignore.

        :deprecated: - use ``project.addPackageIgnore``

        :stability: deprecated
        '''
        result = self._values.get("npmignore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def npmignore_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("npmignore_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_ignore_options(self) -> typing.Optional[_projen_04054675.IgnoreFileOptions]:
        '''(experimental) Configuration options for .npmignore file.

        :stability: experimental
        '''
        result = self._values.get("npm_ignore_options")
        return typing.cast(typing.Optional[_projen_04054675.IgnoreFileOptions], result)

    @builtins.property
    def npm_provenance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should provenance statements be generated when the package is published.

        A supported package manager is required to publish a package with npm provenance statements and
        you will need to use a supported CI/CD provider.

        Note that the projen ``Release`` and ``Publisher`` components are using ``publib`` to publish packages,
        which is using npm internally and supports provenance statements independently of the package manager used.

        :default: - true for public packages, false otherwise

        :stability: experimental
        '''
        result = self._values.get("npm_provenance")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_registry(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The host name of the npm registry to publish to.

        Cannot be set together with ``npmRegistryUrl``.

        :deprecated: use ``npmRegistryUrl`` instead

        :stability: deprecated
        '''
        result = self._values.get("npm_registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_registry_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The base URL of the npm package registry.

        Must be a URL (e.g. start with "https://" or "http://")

        :default: "https://registry.npmjs.org"

        :stability: experimental
        '''
        result = self._values.get("npm_registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the NPM token to use when publishing packages.

        :default: "NPM_TOKEN"

        :stability: experimental
        '''
        result = self._values.get("npm_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project. Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``).

        :default: true

        :stability: experimental
        '''
        result = self._values.get("package")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def package_manager(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.NodePackageManager]:
        '''(experimental) The Node Package Manager used to execute scripts.

        :default: NodePackageManager.YARN_CLASSIC

        :stability: experimental
        '''
        result = self._values.get("package_manager")
        return typing.cast(typing.Optional[_projen_javascript_04054675.NodePackageManager], result)

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The "name" in package.json.

        :default: - defaults to project name

        :stability: experimental
        :featured: false
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[_projen_04054675.Project]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_projen_04054675.Project], result)

    @builtins.property
    def peer_dependency_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.PeerDependencyOptions]:
        '''(experimental) Options for ``peerDeps``.

        :stability: experimental
        '''
        result = self._values.get("peer_dependency_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.PeerDependencyOptions], result)

    @builtins.property
    def peer_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Peer dependencies for this module.

        Dependencies listed here are required to
        be installed (and satisfied) by the *consumer* of this library. Using peer
        dependencies allows you to ensure that only a single module of a certain
        library exists in the ``node_modules`` tree of your consumers.

        Note that prior to npm@7, peer dependencies are *not* automatically
        installed, which means that adding peer dependencies to a library will be a
        breaking change for your customers.

        Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is
        enabled by default), projen will automatically add a dev dependency with a
        pinned version for each peer dependency. This will ensure that you build &
        test your module against the lowest peer version required.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("peer_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pnpm_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of PNPM to use if using PNPM as a package manager.

        :default: "7"

        :stability: experimental
        '''
        result = self._values.get("pnpm_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_build_steps(
        self,
    ) -> typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]]:
        '''(experimental) Steps to execute after build as part of the release workflow.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre").

        :default: - normal semantic versions

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prettier(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup prettier.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("prettier")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prettier_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.PrettierOptions]:
        '''(experimental) Prettier options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("prettier_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.PrettierOptions], result)

    @builtins.property
    def project_type(self) -> typing.Optional[_projen_04054675.ProjectType]:
        '''(deprecated) Which type of project this is (library/app).

        :default: ProjectType.UNKNOWN

        :deprecated: no longer supported at the base project level

        :stability: deprecated
        '''
        result = self._values.get("project_type")
        return typing.cast(typing.Optional[_projen_04054675.ProjectType], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projen_credentials(
        self,
    ) -> typing.Optional[_projen_github_04054675.GithubCredentials]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_projen_github_04054675.GithubCredentials], result)

    @builtins.property
    def projen_dev_dependency(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates of "projen" should be installed as a devDependency.

        :default: - true if not a subproject

        :stability: experimental
        '''
        result = self._values.get("projen_dev_dependency")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_js(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation.

        :default: - true if projenrcJson is false

        :stability: experimental
        '''
        result = self._values.get("projenrc_js")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(
        self,
    ) -> typing.Optional[_projen_04054675.ProjenrcJsonOptions]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_projen_04054675.ProjenrcJsonOptions], result)

    @builtins.property
    def projenrc_js_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.ProjenrcOptions]:
        '''(experimental) Options for .projenrc.js.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_js_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.ProjenrcOptions], result)

    @builtins.property
    def projenrc_ts(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use TypeScript for your projenrc file (``.projenrc.ts``).

        :default: false

        :stability: experimental
        :pjnew: true
        '''
        result = self._values.get("projenrc_ts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_ts_options(
        self,
    ) -> typing.Optional[_projen_typescript_04054675.ProjenrcOptions]:
        '''(experimental) Options for .projenrc.ts.

        :stability: experimental
        '''
        result = self._values.get("projenrc_ts_options")
        return typing.cast(typing.Optional[_projen_typescript_04054675.ProjenrcOptions], result)

    @builtins.property
    def projen_token_secret(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows.

        This token needs to have the ``repo``, ``workflows``
        and ``packages`` scope.

        :default: "PROJEN_GITHUB_TOKEN"

        :deprecated: use ``projenCredentials``

        :stability: deprecated
        '''
        result = self._values.get("projen_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projen_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of projen to install.

        :default: - Defaults to the latest version.

        :stability: experimental
        '''
        result = self._values.get("projen_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_dry_run(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Instead of actually publishing to package managers, just print the publishing command.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_tasks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define publishing tasks that can be executed manually as well as workflows.

        Normally, publishing only happens within automated workflows. Enable this
        in order to create a publishing task for each publishing activity.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_tasks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_template(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a GitHub pull request template.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_template")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_template_contents(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The contents of the pull request template.

        :default: - default content

        :stability: experimental
        '''
        result = self._values.get("pull_request_template_contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def readme(self) -> typing.Optional[_projen_04054675.SampleReadmeProps]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[_projen_04054675.SampleReadmeProps], result)

    @builtins.property
    def releasable_commits(self) -> typing.Optional[_projen_04054675.ReleasableCommits]:
        '''(experimental) Find commits that should be considered releasable Used to decide if a release is required.

        :default: ReleasableCommits.everyCommit()

        :stability: experimental
        '''
        result = self._values.get("releasable_commits")
        return typing.cast(typing.Optional[_projen_04054675.ReleasableCommits], result)

    @builtins.property
    def release(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add release management to this project.

        :default: - true (false for subprojects)

        :stability: experimental
        '''
        result = self._values.get("release")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_branches(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _projen_release_04054675.BranchOptions]]:
        '''(experimental) Defines additional release branches.

        A workflow will be created for each
        release branch which will publish releases from commits in this branch.
        Each release branch *must* be assigned a major version number which is used
        to enforce that versions published from that branch always use that major
        version. If multiple branches are used, the ``majorVersion`` field must also
        be provided for the default branch.

        :default:

        - no additional branches are used for release. you can use
        ``addBranch()`` to add additional branches.

        :stability: experimental
        '''
        result = self._values.get("release_branches")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _projen_release_04054675.BranchOptions]], result)

    @builtins.property
    def release_every_commit(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``.

        :default: true

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.continuous()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_every_commit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create a github issue on every failed publishing task.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue_label(self) -> typing.Optional[builtins.str]:
        '''(experimental) The label to apply to issues indicating publish failures.

        Only applies if ``releaseFailureIssue`` is true.

        :default: "failed-release"

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_schedule(self) -> typing.Optional[builtins.str]:
        '''(deprecated) CRON schedule to trigger new releases.

        :default: - no scheduled releases

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.scheduled()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_tag_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Automatically add the given prefix to release tags.

        Useful if you are releasing on multiple branches with overlapping version numbers.
        Note: this prefix is used to detect the latest tagged version
        when bumping, so if you change this on a project with an existing version
        history, you may need to manually tag your latest release
        with the new prefix.

        :default: "v"

        :stability: experimental
        '''
        result = self._values.get("release_tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_to_npm(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically release to npm when new versions are introduced.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_to_npm")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_trigger(
        self,
    ) -> typing.Optional[_projen_release_04054675.ReleaseTrigger]:
        '''(experimental) The release trigger to use.

        :default: - Continuous releases (``ReleaseTrigger.continuous()``)

        :stability: experimental
        '''
        result = self._values.get("release_trigger")
        return typing.cast(typing.Optional[_projen_release_04054675.ReleaseTrigger], result)

    @builtins.property
    def release_workflow(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) DEPRECATED: renamed to ``release``.

        :default: - true if not a subproject

        :deprecated: see ``release``.

        :stability: deprecated
        '''
        result = self._values.get("release_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the default release workflow.

        :default: "release"

        :stability: experimental
        '''
        result = self._values.get("release_workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_workflow_setup_steps(
        self,
    ) -> typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]]:
        '''(experimental) A set of workflow steps to execute in order to setup the workflow container.

        :stability: experimental
        '''
        result = self._values.get("release_workflow_setup_steps")
        return typing.cast(typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(
        self,
    ) -> typing.Optional[_projen_04054675.RenovatebotOptions]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_projen_04054675.RenovatebotOptions], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''(experimental) The repository is the location where the actual code for your package lives.

        See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository

        :stability: experimental
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.

        :stability: experimental
        '''
        result = self._values.get("repository_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_code(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate one-time sample in ``src/`` and ``test/`` if there are no files there.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sample_code")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def scoped_packages_options(
        self,
    ) -> typing.Optional[typing.List[_projen_javascript_04054675.ScopedPackagesOptions]]:
        '''(experimental) Options for privately hosted scoped packages.

        :default: - fetch all scoped packages from the public npm registry

        :stability: experimental
        '''
        result = self._values.get("scoped_packages_options")
        return typing.cast(typing.Optional[typing.List[_projen_javascript_04054675.ScopedPackagesOptions]], result)

    @builtins.property
    def scripts(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(deprecated) npm scripts to include.

        If a script has the same name as a standard script,
        the standard script will be overwritten.
        Also adds the script as a task.

        :default: {}

        :deprecated: use ``project.addTask()`` or ``package.setScript()``

        :stability: deprecated
        '''
        result = self._values.get("scripts")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def srcdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Typescript sources directory.

        :default: "src"

        :stability: experimental
        '''
        result = self._values.get("srcdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stability(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Stability.

        :stability: experimental
        '''
        result = self._values.get("stability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stale(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Auto-close of stale issues and pull request.

        See ``staleOptions`` for options.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stale")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale_options(self) -> typing.Optional[_projen_github_04054675.StaleOptions]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional[_projen_github_04054675.StaleOptions], result)

    @builtins.property
    def testdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Jest tests directory.

        Tests files should be named ``xxx.test.ts``.
        If this directory is under ``srcdir`` (e.g. ``src/test``, ``src/__tests__``),
        then tests are going to be compiled into ``lib/`` and executed as javascript.
        If the test directory is outside of ``src``, then we configure jest to
        compile the code in-memory.

        :default: "test"

        :stability: experimental
        '''
        result = self._values.get("testdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tsconfig(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.TypescriptConfigOptions]:
        '''(experimental) Custom TSConfig.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("tsconfig")
        return typing.cast(typing.Optional[_projen_javascript_04054675.TypescriptConfigOptions], result)

    @builtins.property
    def tsconfig_dev(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.TypescriptConfigOptions]:
        '''(experimental) Custom tsconfig options for the development tsconfig.json file (used for testing).

        :default: - use the production tsconfig options

        :stability: experimental
        '''
        result = self._values.get("tsconfig_dev")
        return typing.cast(typing.Optional[_projen_javascript_04054675.TypescriptConfigOptions], result)

    @builtins.property
    def tsconfig_dev_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the development tsconfig.json file.

        :default: "tsconfig.dev.json"

        :stability: experimental
        '''
        result = self._values.get("tsconfig_dev_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ts_jest_options(
        self,
    ) -> typing.Optional[_projen_typescript_04054675.TsJestOptions]:
        '''(experimental) Options for ts-jest.

        :stability: experimental
        '''
        result = self._values.get("ts_jest_options")
        return typing.cast(typing.Optional[_projen_typescript_04054675.TsJestOptions], result)

    @builtins.property
    def typescript_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) TypeScript version to use.

        NOTE: Typescript is not semantically versioned and should remain on the
        same minor, so we recommend using a ``~`` dependency (e.g. ``~1.2.3``).

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("typescript_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def versionrc_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Custom configuration used when creating changelog with standard-version package.

        Given values either append to default configuration or overwrite values in it.

        :default: - standard configuration applicable for GitHub repositories

        :stability: experimental
        '''
        result = self._values.get("versionrc_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def vscode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable VSCode integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("vscode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow_bootstrap_steps(
        self,
    ) -> typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]]:
        '''(experimental) Workflow steps to use in order to bootstrap this repo.

        :default: "yarn install --frozen-lockfile && yarn projen"

        :stability: experimental
        '''
        result = self._values.get("workflow_bootstrap_steps")
        return typing.cast(typing.Optional[typing.List[_projen_github_workflows_04054675.JobStep]], result)

    @builtins.property
    def workflow_container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Container image to use for GitHub workflows.

        :default: - default image

        :stability: experimental
        '''
        result = self._values.get("workflow_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_git_identity(
        self,
    ) -> typing.Optional[_projen_github_04054675.GitIdentity]:
        '''(experimental) The git identity to use in workflows.

        :default: - GitHub Actions

        :stability: experimental
        '''
        result = self._values.get("workflow_git_identity")
        return typing.cast(typing.Optional[_projen_github_04054675.GitIdentity], result)

    @builtins.property
    def workflow_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The node version to use in GitHub workflows.

        :default: - same as ``minNodeVersion``

        :stability: experimental
        '''
        result = self._values.get("workflow_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_package_cache(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable Node.js package cache in GitHub workflows.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("workflow_package_cache")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow_runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workflow_runs_on_group(
        self,
    ) -> typing.Optional[_projen_04054675.GroupRunnerOptions]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on_group")
        return typing.cast(typing.Optional[_projen_04054675.GroupRunnerOptions], result)

    @builtins.property
    def yarn_berry_options(
        self,
    ) -> typing.Optional[_projen_javascript_04054675.YarnBerryOptions]:
        '''(experimental) Options for Yarn Berry.

        :default: - Yarn Berry v4 with all default options

        :stability: experimental
        '''
        result = self._values.get("yarn_berry_options")
        return typing.cast(typing.Optional[_projen_javascript_04054675.YarnBerryOptions], result)

    @builtins.property
    def disable_node_warnings(self) -> typing.Optional[builtins.bool]:
        '''Disable node warnings from being emitted during build tasks.

        :default: false
        '''
        result = self._values.get("disable_node_warnings")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def license_options(self) -> typing.Optional[LicenseOptions]:
        '''Default license to apply to all PDK managed packages.

        :default: Apache-2.0
        '''
        result = self._values.get("license_options")
        return typing.cast(typing.Optional[LicenseOptions], result)

    @builtins.property
    def monorepo_upgrade_deps(self) -> typing.Optional[builtins.bool]:
        '''Whether to include an upgrade-deps task at the root of the monorepo which will upgrade all dependencies.

        :default: true
        '''
        result = self._values.get("monorepo_upgrade_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def monorepo_upgrade_deps_options(
        self,
    ) -> typing.Optional[MonorepoUpgradeDepsOptions]:
        '''Monorepo Upgrade Deps options.

        This is only used if monorepoUpgradeDeps is true.

        :default: undefined
        '''
        result = self._values.get("monorepo_upgrade_deps_options")
        return typing.cast(typing.Optional[MonorepoUpgradeDepsOptions], result)

    @builtins.property
    def workspace_config(self) -> typing.Optional[WorkspaceConfig]:
        '''Configuration for workspace.'''
        result = self._values.get("workspace_config")
        return typing.cast(typing.Optional[WorkspaceConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonorepoTsProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "INxProjectCore",
    "JavaProjectOptions",
    "LicenseOptions",
    "MonorepoJavaOptions",
    "MonorepoJavaProject",
    "MonorepoPythonProject",
    "MonorepoPythonProjectOptions",
    "MonorepoTsProject",
    "MonorepoTsProjectOptions",
    "MonorepoUpgradeDepsOptions",
    "NxConfigurator",
    "NxConfiguratorOptions",
    "NxProject",
    "NxWorkspace",
    "PythonProjectOptions",
    "TypeScriptProjectOptions",
    "WorkspaceConfig",
    "YarnWorkspaceConfig",
    "nx",
    "syncpack",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import nx
from . import syncpack

def _typecheckingstub__3d17d0395607a531a6a544f5d56974b8bc1c407aa3f529989f0f211bfd9dd0ae(
    dependent: _projen_04054675.Project,
    dependee: typing.Union[builtins.str, _projen_04054675.Project],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019288be6d00cb0f50fecb03c9899b4be7e0d96cfbe3c6418d968f711f8e5b7e(
    dependent: _projen_java_04054675.JavaProject,
    dependee: _projen_java_04054675.JavaProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87d10ada82211d80097025dafcee32a3ce09f98f19161788434f127287f92b6(
    name: builtins.str,
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

def _typecheckingstub__72ae302715da724dc812c351b20ae831900e149ba1f9602fdd8e6d794257ea11(
    dependent: _projen_python_04054675.PythonProject,
    dependee: _projen_python_04054675.PythonProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beca0972d1a8f14d9fe916150a1fae4839c40298030f85894001f1fb5bdacf4d(
    *,
    name: builtins.str,
    artifact_id: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    distdir: typing.Optional[builtins.str] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    group_id: typing.Optional[builtins.str] = None,
    junit: typing.Optional[builtins.bool] = None,
    junit_options: typing.Optional[typing.Union[_projen_java_04054675.JunitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    mergify: typing.Optional[builtins.bool] = None,
    mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    packaging: typing.Optional[builtins.str] = None,
    packaging_options: typing.Optional[typing.Union[_projen_java_04054675.MavenPackagingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[_projen_04054675.Project] = None,
    parent_pom: typing.Optional[typing.Union[_projen_java_04054675.ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
    project_type: typing.Optional[_projen_04054675.ProjectType] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
    projenrc_java: typing.Optional[builtins.bool] = None,
    projenrc_java_options: typing.Optional[typing.Union[_projen_java_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_token_secret: typing.Optional[builtins.str] = None,
    readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sample: typing.Optional[builtins.bool] = None,
    sample_java_package: typing.Optional[builtins.str] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    vscode: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403eb7d3ab3dddebf764ebe76e5c135d2e4370a0158d3a2e1e7e417879222876(
    *,
    copyright_owner: typing.Optional[builtins.str] = None,
    disable_default_licenses: typing.Optional[builtins.bool] = None,
    license_text: typing.Optional[builtins.str] = None,
    spdx: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688b1b698e0603390e1cd961c8c727da10bed7e457c04f86d923d08ac347d491(
    *,
    name: builtins.str,
    artifact_id: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    distdir: typing.Optional[builtins.str] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    group_id: typing.Optional[builtins.str] = None,
    junit: typing.Optional[builtins.bool] = None,
    junit_options: typing.Optional[typing.Union[_projen_java_04054675.JunitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    mergify: typing.Optional[builtins.bool] = None,
    mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    packaging: typing.Optional[builtins.str] = None,
    packaging_options: typing.Optional[typing.Union[_projen_java_04054675.MavenPackagingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[_projen_04054675.Project] = None,
    parent_pom: typing.Optional[typing.Union[_projen_java_04054675.ParentPom, typing.Dict[builtins.str, typing.Any]]] = None,
    project_type: typing.Optional[_projen_04054675.ProjectType] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
    projenrc_java: typing.Optional[builtins.bool] = None,
    projenrc_java_options: typing.Optional[typing.Union[_projen_java_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_token_secret: typing.Optional[builtins.str] = None,
    readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sample: typing.Optional[builtins.bool] = None,
    sample_java_package: typing.Optional[builtins.str] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    vscode: typing.Optional[builtins.bool] = None,
    default_release_branch: typing.Optional[builtins.str] = None,
    disable_default_licenses: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682830f1683b2735615a32e11be70033ae0868bfb3cc36d516befc9cdfef58c2(
    dependent: _projen_04054675.Project,
    dependee: typing.Union[builtins.str, _projen_04054675.Project],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df53f208f195928611c6206487d14e22d8883a812b62159391dd91389c9c2e15(
    dependent: _projen_java_04054675.JavaProject,
    dependee: _projen_java_04054675.JavaProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b3ad8588c14991da810bc28684e6ad2df1494945d81d2b318de4f318874505(
    name: builtins.str,
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

def _typecheckingstub__064e49db934492bfa2ed35bd60a9fa5b97c2242d05f3a08312676ae30bfbfac8(
    dependent: _projen_python_04054675.PythonProject,
    dependee: _projen_python_04054675.PythonProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c886f4ab8dd9ee1d320a6473c4742e3d18b1f0c1c86d73cca3420ea7c19ee00(
    dependent: _projen_04054675.Project,
    dependee: typing.Union[builtins.str, _projen_04054675.Project],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea38efa6f69de4704088112a006c41ca3887f1bb1c5ab6afe85c1e1975a3930a(
    dependent: _projen_java_04054675.JavaProject,
    dependee: _projen_java_04054675.JavaProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee599bc4aadc41024c7991894dcc12951d573665b01127355bca175810feca2(
    name: builtins.str,
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

def _typecheckingstub__1fa90809879df9155778f3dd8ecee1ed68af72c551df6d1f25f71fd0d896f4e7(
    dependent: _projen_python_04054675.PythonProject,
    dependee: _projen_python_04054675.PythonProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f49e2643fb6a6e113433d8379fa180cdfdb081b793f3cb0cdeb2c5f54cfdb81(
    dependent: _projen_04054675.Project,
    dependee: typing.Union[builtins.str, _projen_04054675.Project],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587e8033cb232120a1633228165099505bb32f21d31d2ecd6bdc8079e8a30ea9(
    dependent: _projen_java_04054675.JavaProject,
    dependee: _projen_java_04054675.JavaProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1b5b8e0649aced11a695b1f6bc308ba2c715409b4d356fa846a5a1bce391c1(
    name: builtins.str,
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

def _typecheckingstub__c463ab04e7a6ec06c7487d0639443405d7f1792e5bd42c2ac18a70edd5d9c823(
    dependent: _projen_python_04054675.PythonProject,
    dependee: _projen_python_04054675.PythonProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b95f98f7a6ffd6e29650a109c377dc135f7bd57a0639f9f720e2f86a61a09cc(
    *package_globs: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390b0ad8efb140cce70e5df8c9a74d9aec5812aa35f52dd45fc8cbc95cededcd(
    *,
    syncpack_config: typing.Optional[typing.Union[_SyncpackConfig_9a7845d7, typing.Dict[builtins.str, typing.Any]]] = None,
    task_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed97476ef032e66c8f1f7ade48175ebbb06749d0ebf5e88945694da059348811(
    project: _projen_04054675.Project,
    *,
    default_release_branch: typing.Optional[builtins.str] = None,
    license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44572c825aad4ac4e8118dff282e1942ba8aa1d9791852aae1ca46eb5d92710(
    dependent: _projen_04054675.Project,
    dependee: typing.Union[builtins.str, _projen_04054675.Project],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a0c582c7d2cfd66500b537a5cb0d287914102a80a6ef7f3268e2e6dc12e6d1(
    dependent: _projen_java_04054675.JavaProject,
    dependee: _projen_java_04054675.JavaProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4108c14007a7e79adfc367f7a8b55b09914490f0608987bb9585099775e10597(
    name: builtins.str,
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

def _typecheckingstub__604e9c9a16fff068e5abd17ce8ba57f3807cf6e12bda0e6812589bbd2574cb37(
    dependent: _projen_python_04054675.PythonProject,
    dependee: _projen_python_04054675.PythonProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f753c02716795922069d0101ef32fde087d3562a0ff1c5abbba92d300d72d77d(
    nx_plugins: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41cdd8e56554c5bf2880bef86a2d8e3b6b1748bc19b96dce2a6b7bb3bebf765(
    project: _projen_python_04054675.PythonProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908936f24e27696f73dca58c8f0b5a868023a700925f4d2b30e8a22a06c80a54(
    projects: typing.Sequence[_projen_04054675.Project],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50950bf833fa298e21fe264d1d1b4bb04ced38d0e70d57190d06e13137f1f35a(
    *,
    default_release_branch: typing.Optional[builtins.str] = None,
    license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30366b89fa356cef1088329b5c0c6a1f2f3e674384574b5150983c2b20eb7283(
    project: _projen_04054675.Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68513bdb1fb452405f6d9f95bcf81604c365d0abc3a3a4fe7378a36980b69d4d(
    project: _projen_04054675.Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8577e9bef1e574cf8576f2a57b1728567ff89778f21ba4b68b9592063d7461(
    project: _projen_04054675.Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aad1e6d4ec0e879610ac5c5ede31cce5555f4d78b294ac87e7783c34ca6729d(
    inputs: typing.Optional[typing.Sequence[typing.Union[builtins.str, _IInput_534968b7]]] = None,
    outputs: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46a28aab116cd2273c3fb4bbb74c5f585f1edd073fd1f0b1efe223f1484317e(
    *dependee: typing.Union[builtins.str, _projen_04054675.Project],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5423fe6bc91d6737402b53c8d859130edbe0e82998bfb339ec9f7b0c12e0e5c(
    dependee: _projen_java_04054675.JavaProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a8d5b45a6a468d432d8123028e6ea2c55ea1cdeb927fee35edea8b28a28f99(
    dependee: _projen_python_04054675.PythonProject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d82461f56f01fff7e9c3fb53766cef8a655d75c33d2d824810eae12053df898(
    *tags: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3ef7a57a97cc41beefab833fb4a8e43590ffdb00d966f84a9a39e82e8be96f(
    name: builtins.str,
    inputs: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee830648fb433c27179f69b5e9b4018341cfa6bcffd1fe11d399b4879a4dbb52(
    name: builtins.str,
    target: _IProjectTarget_184fbc33,
    include_defaults: typing.Optional[typing.Union[builtins.str, builtins.bool]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521e1d57d19197ff9932b7cbb0d3f8ad65c6f1a3fe4ee5be040a6fd02e27507c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3921b3c5d8fb8c7534254d3f7c6573f2ae66663bcea2bbd47e9b9d530dfa450b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c586a10031c8b671142a6bc8dc1d7e01d95f371904d5fdf7ee4bb22cb220beb8(
    value: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11991d92880e09cad77e85bc1d0ab510767e1d3c7eff2d101478fc53d97148ff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df666c2903109c294a10bae5f5b40da1eec0b2b2d40b72a3a209bf6bc599516(
    value: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250320810381bea13f650f8c6f9f01fa648ee521ead1bc8938c9476f9f4a6721(
    project: _projen_04054675.Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064f95290b0f6b4cae88e9826662904872e694faf9474327ac6a207c88011fdf(
    scope: _projen_04054675.Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5eb856c65a0556913799999bf6028bc7aca48d46fa4de8eef5360c80edce220(
    name: builtins.str,
    inputs: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3dc483725d5b9f059f8bf44f1751d403efb32be822822ee6f139a0ad701d181(
    name: builtins.str,
    target: _IProjectTarget_184fbc33,
    merge: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f44402e5722b71268d11def844203c58a812944e360f7871eef5f4f94b29fc(
    read_only_access_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54016533c964b96af2a7b8bf071f49b3c089cb3d855dbc51610ab1d0ac6ab00(
    value: _INxAffectedConfig_1a5bb1a8,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b038cb7d50d63894109da223dd2be8afe54c04d86d75602e7bd5ff00849a50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e976737e7f0db4a1d471c9d5b1855bb11e1cad1f9d421b29f887b7fef79fa7c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bac317426eae1f61a1ba6a1e6c66459b3a9baf6cf42b408d71a1912de53dabf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cfd26bb5bdea0e58e11387d6df1f04ed49b58a9b857c3fe7aeaded9d3465a22(
    value: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378acf007bb83eafc4c015ebd56148e9dea19a74b354e37c86cd55e0de9381e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75325b7fa3abd85be92f4989a7916a9eda1bfabd263503e4f7abd28b49ae4a39(
    value: typing.Mapping[builtins.str, typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c472f77cac71dd224f94cc3986df1bc2a615fb92cc14ca465d92280db9046993(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4aac2c6d47cc61b849934cf500d4f16438fb2e777fb3713219e2f97c6961212(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff3c185bc8e64404880e59de3dc657fa70213a6a2bfea00a74ea72044afdc93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa837bf24c35c1fa31f1b7fd7f8aea9c91b2d274052e1eea6537c3c75ee6215(
    value: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5cc18c3c7ffba2551af8a12b054360893e77b5599b4a93cdaa1e61a1330e3c(
    value: typing.Mapping[builtins.str, _IProjectTarget_184fbc33],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da6ba6112c3ca1a750676caab4f0662dc60225c78861f53b73f89a639f89793(
    value: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d06e29986d52b7f0721c57b558ba202ba1133ceaabf1bfb61c7ce380417a0d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9764b0d2301aef01e8a7ed83b46e43cd406eb0878be317b9c6a68c66803d12a5(
    value: typing.Optional[_IWorkspaceLayout_a55c7d5d],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d87ff8ff85bcdc19da74931d63e3c517add273af9807c138f0ca06c07a1dbd(
    *,
    module_name: builtins.str,
    name: builtins.str,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    homepage: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    mergify: typing.Optional[builtins.bool] = None,
    mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    package_name: typing.Optional[builtins.str] = None,
    parent: typing.Optional[_projen_04054675.Project] = None,
    poetry_options: typing.Optional[typing.Union[_projen_python_04054675.PoetryPyprojectOptionsWithoutDeps, typing.Dict[builtins.str, typing.Any]]] = None,
    project_type: typing.Optional[_projen_04054675.ProjectType] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_python_options: typing.Optional[typing.Union[_projen_python_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_token_secret: typing.Optional[builtins.str] = None,
    pytest: typing.Optional[builtins.bool] = None,
    pytest_options: typing.Optional[typing.Union[_projen_python_04054675.PytestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    python_exec: typing.Optional[builtins.str] = None,
    readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sample: typing.Optional[builtins.bool] = None,
    setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    setuptools: typing.Optional[builtins.bool] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    vscode: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb99db9d3225c4cdd0c347616408142d71a340a8c808142cc5f3d813a6f71ec(
    *,
    name: builtins.str,
    allow_library_dependencies: typing.Optional[builtins.bool] = None,
    artifacts_directory: typing.Optional[builtins.str] = None,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    author_organization: typing.Optional[builtins.bool] = None,
    author_url: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_approve_upgrades: typing.Optional[builtins.bool] = None,
    auto_detect_bin: typing.Optional[builtins.bool] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bugs_email: typing.Optional[builtins.str] = None,
    bugs_url: typing.Optional[builtins.str] = None,
    build_workflow: typing.Optional[builtins.bool] = None,
    build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
    bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_cov: typing.Optional[builtins.bool] = None,
    code_cov_token_secret: typing.Optional[builtins.str] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    copyright_owner: typing.Optional[builtins.str] = None,
    copyright_period: typing.Optional[builtins.str] = None,
    default_release_branch: typing.Optional[builtins.str] = None,
    dependabot: typing.Optional[builtins.bool] = None,
    dependabot_options: typing.Optional[typing.Union[_projen_github_04054675.DependabotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    deps_upgrade: typing.Optional[builtins.bool] = None,
    deps_upgrade_options: typing.Optional[typing.Union[_projen_javascript_04054675.UpgradeDependenciesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    disable_tsconfig: typing.Optional[builtins.bool] = None,
    disable_tsconfig_dev: typing.Optional[builtins.bool] = None,
    docgen: typing.Optional[builtins.bool] = None,
    docs_directory: typing.Optional[builtins.str] = None,
    entrypoint: typing.Optional[builtins.str] = None,
    entrypoint_types: typing.Optional[builtins.str] = None,
    eslint: typing.Optional[builtins.bool] = None,
    eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    homepage: typing.Optional[builtins.str] = None,
    jest: typing.Optional[builtins.bool] = None,
    jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    libdir: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    licensed: typing.Optional[builtins.bool] = None,
    logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    major_version: typing.Optional[jsii.Number] = None,
    max_node_version: typing.Optional[builtins.str] = None,
    mergify: typing.Optional[builtins.bool] = None,
    mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    min_major_version: typing.Optional[jsii.Number] = None,
    min_node_version: typing.Optional[builtins.str] = None,
    mutable_build: typing.Optional[builtins.bool] = None,
    npm_access: typing.Optional[_projen_javascript_04054675.NpmAccess] = None,
    npm_dist_tag: typing.Optional[builtins.str] = None,
    npmignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    npmignore_enabled: typing.Optional[builtins.bool] = None,
    npm_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    npm_provenance: typing.Optional[builtins.bool] = None,
    npm_registry: typing.Optional[builtins.str] = None,
    npm_registry_url: typing.Optional[builtins.str] = None,
    npm_token_secret: typing.Optional[builtins.str] = None,
    outdir: typing.Optional[builtins.str] = None,
    package: typing.Optional[builtins.bool] = None,
    package_manager: typing.Optional[_projen_javascript_04054675.NodePackageManager] = None,
    package_name: typing.Optional[builtins.str] = None,
    parent: typing.Optional[_projen_04054675.Project] = None,
    peer_dependency_options: typing.Optional[typing.Union[_projen_javascript_04054675.PeerDependencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    pnpm_version: typing.Optional[builtins.str] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    prerelease: typing.Optional[builtins.str] = None,
    prettier: typing.Optional[builtins.bool] = None,
    prettier_options: typing.Optional[typing.Union[_projen_javascript_04054675.PrettierOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_type: typing.Optional[_projen_04054675.ProjectType] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
    projen_dev_dependency: typing.Optional[builtins.bool] = None,
    projenrc_js: typing.Optional[builtins.bool] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_js_options: typing.Optional[typing.Union[_projen_javascript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_ts: typing.Optional[builtins.bool] = None,
    projenrc_ts_options: typing.Optional[typing.Union[_projen_typescript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_token_secret: typing.Optional[builtins.str] = None,
    projen_version: typing.Optional[builtins.str] = None,
    publish_dry_run: typing.Optional[builtins.bool] = None,
    publish_tasks: typing.Optional[builtins.bool] = None,
    pull_request_template: typing.Optional[builtins.bool] = None,
    pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    releasable_commits: typing.Optional[_projen_04054675.ReleasableCommits] = None,
    release: typing.Optional[builtins.bool] = None,
    release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[_projen_release_04054675.BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_every_commit: typing.Optional[builtins.bool] = None,
    release_failure_issue: typing.Optional[builtins.bool] = None,
    release_failure_issue_label: typing.Optional[builtins.str] = None,
    release_schedule: typing.Optional[builtins.str] = None,
    release_tag_prefix: typing.Optional[builtins.str] = None,
    release_to_npm: typing.Optional[builtins.bool] = None,
    release_trigger: typing.Optional[_projen_release_04054675.ReleaseTrigger] = None,
    release_workflow: typing.Optional[builtins.bool] = None,
    release_workflow_name: typing.Optional[builtins.str] = None,
    release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[builtins.str] = None,
    repository_directory: typing.Optional[builtins.str] = None,
    sample_code: typing.Optional[builtins.bool] = None,
    scoped_packages_options: typing.Optional[typing.Sequence[typing.Union[_projen_javascript_04054675.ScopedPackagesOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    srcdir: typing.Optional[builtins.str] = None,
    stability: typing.Optional[builtins.str] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    testdir: typing.Optional[builtins.str] = None,
    tsconfig: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tsconfig_dev: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tsconfig_dev_file: typing.Optional[builtins.str] = None,
    ts_jest_options: typing.Optional[typing.Union[_projen_typescript_04054675.TsJestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    typescript_version: typing.Optional[builtins.str] = None,
    versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    vscode: typing.Optional[builtins.bool] = None,
    workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_git_identity: typing.Optional[typing.Union[_projen_github_04054675.GitIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_node_version: typing.Optional[builtins.str] = None,
    workflow_package_cache: typing.Optional[builtins.bool] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_projen_04054675.GroupRunnerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    yarn_berry_options: typing.Optional[typing.Union[_projen_javascript_04054675.YarnBerryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b872fab3c01261b61bb1ba4e216c6063540ecf4ca12c8b063f16badde10abf(
    *,
    additional_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    link_local_workspace_bins: typing.Optional[builtins.bool] = None,
    yarn: typing.Optional[typing.Union[YarnWorkspaceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df49722742021b2cc598380915e034283683e99ee86edaeca83859f793d616ea(
    *,
    disable_no_hoist_bundled: typing.Optional[builtins.bool] = None,
    no_hoist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea87dc3723259fcfab289a5ee69cc3ffb4716eafa280a8abe4df20c5b147630(
    *,
    module_name: builtins.str,
    name: builtins.str,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    homepage: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    mergify: typing.Optional[builtins.bool] = None,
    mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    package_name: typing.Optional[builtins.str] = None,
    parent: typing.Optional[_projen_04054675.Project] = None,
    poetry_options: typing.Optional[typing.Union[_projen_python_04054675.PoetryPyprojectOptionsWithoutDeps, typing.Dict[builtins.str, typing.Any]]] = None,
    project_type: typing.Optional[_projen_04054675.ProjectType] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_python_options: typing.Optional[typing.Union[_projen_python_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_token_secret: typing.Optional[builtins.str] = None,
    pytest: typing.Optional[builtins.bool] = None,
    pytest_options: typing.Optional[typing.Union[_projen_python_04054675.PytestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    python_exec: typing.Optional[builtins.str] = None,
    readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sample: typing.Optional[builtins.bool] = None,
    setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    setuptools: typing.Optional[builtins.bool] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    vscode: typing.Optional[builtins.bool] = None,
    default_release_branch: typing.Optional[builtins.str] = None,
    license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd6505f1b256e8137d338ed4a05a0fefbc62ac331551c10781a424be0bb1d4c(
    *,
    name: builtins.str,
    allow_library_dependencies: typing.Optional[builtins.bool] = None,
    artifacts_directory: typing.Optional[builtins.str] = None,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    author_organization: typing.Optional[builtins.bool] = None,
    author_url: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_approve_upgrades: typing.Optional[builtins.bool] = None,
    auto_detect_bin: typing.Optional[builtins.bool] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bugs_email: typing.Optional[builtins.str] = None,
    bugs_url: typing.Optional[builtins.str] = None,
    build_workflow: typing.Optional[builtins.bool] = None,
    build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
    bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_cov: typing.Optional[builtins.bool] = None,
    code_cov_token_secret: typing.Optional[builtins.str] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    copyright_owner: typing.Optional[builtins.str] = None,
    copyright_period: typing.Optional[builtins.str] = None,
    default_release_branch: typing.Optional[builtins.str] = None,
    dependabot: typing.Optional[builtins.bool] = None,
    dependabot_options: typing.Optional[typing.Union[_projen_github_04054675.DependabotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    deps_upgrade: typing.Optional[builtins.bool] = None,
    deps_upgrade_options: typing.Optional[typing.Union[_projen_javascript_04054675.UpgradeDependenciesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    disable_tsconfig: typing.Optional[builtins.bool] = None,
    disable_tsconfig_dev: typing.Optional[builtins.bool] = None,
    docgen: typing.Optional[builtins.bool] = None,
    docs_directory: typing.Optional[builtins.str] = None,
    entrypoint: typing.Optional[builtins.str] = None,
    entrypoint_types: typing.Optional[builtins.str] = None,
    eslint: typing.Optional[builtins.bool] = None,
    eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    homepage: typing.Optional[builtins.str] = None,
    jest: typing.Optional[builtins.bool] = None,
    jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    libdir: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    licensed: typing.Optional[builtins.bool] = None,
    logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    major_version: typing.Optional[jsii.Number] = None,
    max_node_version: typing.Optional[builtins.str] = None,
    mergify: typing.Optional[builtins.bool] = None,
    mergify_options: typing.Optional[typing.Union[_projen_github_04054675.MergifyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    min_major_version: typing.Optional[jsii.Number] = None,
    min_node_version: typing.Optional[builtins.str] = None,
    mutable_build: typing.Optional[builtins.bool] = None,
    npm_access: typing.Optional[_projen_javascript_04054675.NpmAccess] = None,
    npm_dist_tag: typing.Optional[builtins.str] = None,
    npmignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    npmignore_enabled: typing.Optional[builtins.bool] = None,
    npm_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    npm_provenance: typing.Optional[builtins.bool] = None,
    npm_registry: typing.Optional[builtins.str] = None,
    npm_registry_url: typing.Optional[builtins.str] = None,
    npm_token_secret: typing.Optional[builtins.str] = None,
    outdir: typing.Optional[builtins.str] = None,
    package: typing.Optional[builtins.bool] = None,
    package_manager: typing.Optional[_projen_javascript_04054675.NodePackageManager] = None,
    package_name: typing.Optional[builtins.str] = None,
    parent: typing.Optional[_projen_04054675.Project] = None,
    peer_dependency_options: typing.Optional[typing.Union[_projen_javascript_04054675.PeerDependencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    pnpm_version: typing.Optional[builtins.str] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    prerelease: typing.Optional[builtins.str] = None,
    prettier: typing.Optional[builtins.bool] = None,
    prettier_options: typing.Optional[typing.Union[_projen_javascript_04054675.PrettierOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_type: typing.Optional[_projen_04054675.ProjectType] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projen_credentials: typing.Optional[_projen_github_04054675.GithubCredentials] = None,
    projen_dev_dependency: typing.Optional[builtins.bool] = None,
    projenrc_js: typing.Optional[builtins.bool] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_js_options: typing.Optional[typing.Union[_projen_javascript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projenrc_ts: typing.Optional[builtins.bool] = None,
    projenrc_ts_options: typing.Optional[typing.Union[_projen_typescript_04054675.ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_token_secret: typing.Optional[builtins.str] = None,
    projen_version: typing.Optional[builtins.str] = None,
    publish_dry_run: typing.Optional[builtins.bool] = None,
    publish_tasks: typing.Optional[builtins.bool] = None,
    pull_request_template: typing.Optional[builtins.bool] = None,
    pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    readme: typing.Optional[typing.Union[_projen_04054675.SampleReadmeProps, typing.Dict[builtins.str, typing.Any]]] = None,
    releasable_commits: typing.Optional[_projen_04054675.ReleasableCommits] = None,
    release: typing.Optional[builtins.bool] = None,
    release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[_projen_release_04054675.BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_every_commit: typing.Optional[builtins.bool] = None,
    release_failure_issue: typing.Optional[builtins.bool] = None,
    release_failure_issue_label: typing.Optional[builtins.str] = None,
    release_schedule: typing.Optional[builtins.str] = None,
    release_tag_prefix: typing.Optional[builtins.str] = None,
    release_to_npm: typing.Optional[builtins.bool] = None,
    release_trigger: typing.Optional[_projen_release_04054675.ReleaseTrigger] = None,
    release_workflow: typing.Optional[builtins.bool] = None,
    release_workflow_name: typing.Optional[builtins.str] = None,
    release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[builtins.str] = None,
    repository_directory: typing.Optional[builtins.str] = None,
    sample_code: typing.Optional[builtins.bool] = None,
    scoped_packages_options: typing.Optional[typing.Sequence[typing.Union[_projen_javascript_04054675.ScopedPackagesOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    srcdir: typing.Optional[builtins.str] = None,
    stability: typing.Optional[builtins.str] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    testdir: typing.Optional[builtins.str] = None,
    tsconfig: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tsconfig_dev: typing.Optional[typing.Union[_projen_javascript_04054675.TypescriptConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tsconfig_dev_file: typing.Optional[builtins.str] = None,
    ts_jest_options: typing.Optional[typing.Union[_projen_typescript_04054675.TsJestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    typescript_version: typing.Optional[builtins.str] = None,
    versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    vscode: typing.Optional[builtins.bool] = None,
    workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_git_identity: typing.Optional[typing.Union[_projen_github_04054675.GitIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_node_version: typing.Optional[builtins.str] = None,
    workflow_package_cache: typing.Optional[builtins.bool] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_projen_04054675.GroupRunnerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    yarn_berry_options: typing.Optional[typing.Union[_projen_javascript_04054675.YarnBerryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_node_warnings: typing.Optional[builtins.bool] = None,
    license_options: typing.Optional[typing.Union[LicenseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    monorepo_upgrade_deps: typing.Optional[builtins.bool] = None,
    monorepo_upgrade_deps_options: typing.Optional[typing.Union[MonorepoUpgradeDepsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_config: typing.Optional[typing.Union[WorkspaceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
