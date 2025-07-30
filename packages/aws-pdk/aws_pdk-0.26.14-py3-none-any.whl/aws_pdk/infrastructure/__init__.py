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
import projen.awscdk as _projen_awscdk_04054675
import projen.github as _projen_github_04054675
import projen.github.workflows as _projen_github_workflows_04054675
import projen.java as _projen_java_04054675
import projen.javascript as _projen_javascript_04054675
import projen.python as _projen_python_04054675
import projen.release as _projen_release_04054675
import projen.typescript as _projen_typescript_04054675
from ..cloudscape_react_ts_website import (
    CloudscapeReactTsWebsiteProject as _CloudscapeReactTsWebsiteProject_ef2bfd2f
)
from ..type_safe_api import (
    TypeSafeApiProject as _TypeSafeApiProject_b9e4f1cf,
    TypeSafeWebSocketApiProject as _TypeSafeWebSocketApiProject_59b62fd2,
)


@jsii.data_type(
    jsii_type="@aws/pdk.infrastructure.AwsCdkJavaAppOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "artifact_id": "artifactId",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "build_command": "buildCommand",
        "cdk_assert": "cdkAssert",
        "cdk_assertions": "cdkAssertions",
        "cdk_dependencies": "cdkDependencies",
        "cdk_dependencies_as_deps": "cdkDependenciesAsDeps",
        "cdkout": "cdkout",
        "cdk_test_dependencies": "cdkTestDependencies",
        "cdk_version": "cdkVersion",
        "cdk_version_pinning": "cdkVersionPinning",
        "clobber": "clobber",
        "commit_generated": "commitGenerated",
        "compile_options": "compileOptions",
        "constructs_version": "constructsVersion",
        "context": "context",
        "deps": "deps",
        "description": "description",
        "dev_container": "devContainer",
        "distdir": "distdir",
        "feature_flags": "featureFlags",
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
        "require_approval": "requireApproval",
        "sample": "sample",
        "sample_java_package": "sampleJavaPackage",
        "stale": "stale",
        "stale_options": "staleOptions",
        "test_deps": "testDeps",
        "url": "url",
        "version": "version",
        "vscode": "vscode",
        "watch_excludes": "watchExcludes",
        "watch_includes": "watchIncludes",
    },
)
class AwsCdkJavaAppOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        artifact_id: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_command: typing.Optional[builtins.str] = None,
        cdk_assert: typing.Optional[builtins.bool] = None,
        cdk_assertions: typing.Optional[builtins.bool] = None,
        cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
        cdkout: typing.Optional[builtins.str] = None,
        cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_version: typing.Optional[builtins.str] = None,
        cdk_version_pinning: typing.Optional[builtins.bool] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        constructs_version: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        distdir: typing.Optional[builtins.str] = None,
        feature_flags: typing.Optional[builtins.bool] = None,
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
        require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
        sample: typing.Optional[builtins.bool] = None,
        sample_java_package: typing.Optional[builtins.str] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
        watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''AwsCdkJavaAppOptions.

        :param name: Default: $BASEDIR
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param build_command: (experimental) A command to execute before synthesis. This command will be called when running ``cdk synth`` or when ``cdk watch`` identifies a change in your source code before redeployment. Default: - no build command
        :param cdk_assert: (deprecated) Warning: NodeJS only. Install the Default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0
        :param cdk_assertions: (experimental) Install the assertions library? Only needed for CDK 1.x. If using CDK 2.x then assertions is already included in 'aws-cdk-lib' Default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0
        :param cdk_dependencies: (deprecated) Which AWS CDKv1 modules this project requires.
        :param cdk_dependencies_as_deps: (deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``). This is to ensure that downstream consumers actually have your CDK dependencies installed when using npm < 7 or yarn, where peer dependencies are not automatically installed. If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure they are present during development. Note: this setting only applies to construct library projects Default: true
        :param cdkout: (experimental) cdk.out directory. Default: "cdk.out"
        :param cdk_test_dependencies: (deprecated) AWS CDK modules required for testing.
        :param cdk_version: (experimental) Minimum version of the AWS CDK to depend on. Default: "2.1.0"
        :param cdk_version_pinning: (experimental) Use pinned version instead of caret version for CDK. You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates. If you use experimental features this will let you define the moment you include breaking changes.
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param compile_options: (experimental) Compile options. Default: - defaults
        :param constructs_version: (experimental) Minimum version of the ``constructs`` library to depend on. Default: - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is "10.0.5".
        :param context: (experimental) Additional context to include in ``cdk.json``. Default: - no additional context
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param distdir: (experimental) Final artifact output directory. Default: "dist/java"
        :param feature_flags: (experimental) Include all feature flags in cdk.json. Default: true
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
        :param require_approval: (experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them. Default: ApprovalLevel.BROADENING
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param sample_java_package: (experimental) The java package to use for the code sample. Default: "org.acme"
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param test_deps: (experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addTestDependency()``. Default: []
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param watch_excludes: (experimental) Glob patterns to exclude from ``cdk watch``. Default: []
        :param watch_includes: (experimental) Glob patterns to include in ``cdk watch``. Default: []
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ea975ed4c9a1918e26b02319faeb5e7df13050f92baf8b835320a1908ec9b73)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument cdk_assert", value=cdk_assert, expected_type=type_hints["cdk_assert"])
            check_type(argname="argument cdk_assertions", value=cdk_assertions, expected_type=type_hints["cdk_assertions"])
            check_type(argname="argument cdk_dependencies", value=cdk_dependencies, expected_type=type_hints["cdk_dependencies"])
            check_type(argname="argument cdk_dependencies_as_deps", value=cdk_dependencies_as_deps, expected_type=type_hints["cdk_dependencies_as_deps"])
            check_type(argname="argument cdkout", value=cdkout, expected_type=type_hints["cdkout"])
            check_type(argname="argument cdk_test_dependencies", value=cdk_test_dependencies, expected_type=type_hints["cdk_test_dependencies"])
            check_type(argname="argument cdk_version", value=cdk_version, expected_type=type_hints["cdk_version"])
            check_type(argname="argument cdk_version_pinning", value=cdk_version_pinning, expected_type=type_hints["cdk_version_pinning"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument compile_options", value=compile_options, expected_type=type_hints["compile_options"])
            check_type(argname="argument constructs_version", value=constructs_version, expected_type=type_hints["constructs_version"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument distdir", value=distdir, expected_type=type_hints["distdir"])
            check_type(argname="argument feature_flags", value=feature_flags, expected_type=type_hints["feature_flags"])
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
            check_type(argname="argument require_approval", value=require_approval, expected_type=type_hints["require_approval"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument sample_java_package", value=sample_java_package, expected_type=type_hints["sample_java_package"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument test_deps", value=test_deps, expected_type=type_hints["test_deps"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument watch_excludes", value=watch_excludes, expected_type=type_hints["watch_excludes"])
            check_type(argname="argument watch_includes", value=watch_includes, expected_type=type_hints["watch_includes"])
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
        if build_command is not None:
            self._values["build_command"] = build_command
        if cdk_assert is not None:
            self._values["cdk_assert"] = cdk_assert
        if cdk_assertions is not None:
            self._values["cdk_assertions"] = cdk_assertions
        if cdk_dependencies is not None:
            self._values["cdk_dependencies"] = cdk_dependencies
        if cdk_dependencies_as_deps is not None:
            self._values["cdk_dependencies_as_deps"] = cdk_dependencies_as_deps
        if cdkout is not None:
            self._values["cdkout"] = cdkout
        if cdk_test_dependencies is not None:
            self._values["cdk_test_dependencies"] = cdk_test_dependencies
        if cdk_version is not None:
            self._values["cdk_version"] = cdk_version
        if cdk_version_pinning is not None:
            self._values["cdk_version_pinning"] = cdk_version_pinning
        if clobber is not None:
            self._values["clobber"] = clobber
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if compile_options is not None:
            self._values["compile_options"] = compile_options
        if constructs_version is not None:
            self._values["constructs_version"] = constructs_version
        if context is not None:
            self._values["context"] = context
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if distdir is not None:
            self._values["distdir"] = distdir
        if feature_flags is not None:
            self._values["feature_flags"] = feature_flags
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
        if require_approval is not None:
            self._values["require_approval"] = require_approval
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
        if watch_excludes is not None:
            self._values["watch_excludes"] = watch_excludes
        if watch_includes is not None:
            self._values["watch_includes"] = watch_includes

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
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A command to execute before synthesis.

        This command will be called when
        running ``cdk synth`` or when ``cdk watch`` identifies a change in your source
        code before redeployment.

        :default: - no build command

        :stability: experimental
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_assert(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Warning: NodeJS only.

        Install the

        :default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0

        :deprecated: The

        :stability: deprecated
        :aws-cdk: /assertions (in V1) and included in ``aws-cdk-lib`` for V2.
        '''
        result = self._values.get("cdk_assert")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_assertions(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install the assertions library?

        Only needed for CDK 1.x. If using CDK 2.x then
        assertions is already included in 'aws-cdk-lib'

        :default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0

        :stability: experimental
        '''
        result = self._values.get("cdk_assertions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Which AWS CDKv1 modules this project requires.

        :deprecated: For CDK 2.x use "deps" instead. (or "peerDeps" if you're building a library)

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_dependencies_as_deps(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``).

        This is to ensure that downstream consumers actually have your CDK dependencies installed
        when using npm < 7 or yarn, where peer dependencies are not automatically installed.
        If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure
        they are present during development.

        Note: this setting only applies to construct library projects

        :default: true

        :deprecated: Not supported in CDK v2.

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies_as_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdkout(self) -> typing.Optional[builtins.str]:
        '''(experimental) cdk.out directory.

        :default: "cdk.out"

        :stability: experimental
        '''
        result = self._values.get("cdkout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_test_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) AWS CDK modules required for testing.

        :deprecated: For CDK 2.x use 'devDeps' (in node.js projects) or 'testDeps' (in java projects) instead

        :stability: deprecated
        '''
        result = self._values.get("cdk_test_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the AWS CDK to depend on.

        :default: "2.1.0"

        :stability: experimental
        '''
        result = self._values.get("cdk_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_version_pinning(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use pinned version instead of caret version for CDK.

        You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates.
        If you use experimental features this will let you define the moment you include breaking changes.

        :stability: experimental
        '''
        result = self._values.get("cdk_version_pinning")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def constructs_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the ``constructs`` library to depend on.

        :default:

        - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is
        "10.0.5".

        :stability: experimental
        '''
        result = self._values.get("constructs_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional context to include in ``cdk.json``.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

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
    def feature_flags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include all feature flags in cdk.json.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("feature_flags")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def require_approval(
        self,
    ) -> typing.Optional[_projen_awscdk_04054675.ApprovalLevel]:
        '''(experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them.

        :default: ApprovalLevel.BROADENING

        :stability: experimental
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[_projen_awscdk_04054675.ApprovalLevel], result)

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
    def watch_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to exclude from ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def watch_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to include in ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCdkJavaAppOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.infrastructure.AwsCdkPythonAppOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "author_email": "authorEmail",
        "author_name": "authorName",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "build_command": "buildCommand",
        "cdk_assert": "cdkAssert",
        "cdk_assertions": "cdkAssertions",
        "cdk_dependencies": "cdkDependencies",
        "cdk_dependencies_as_deps": "cdkDependenciesAsDeps",
        "cdkout": "cdkout",
        "cdk_test_dependencies": "cdkTestDependencies",
        "cdk_version": "cdkVersion",
        "cdk_version_pinning": "cdkVersionPinning",
        "classifiers": "classifiers",
        "clobber": "clobber",
        "commit_generated": "commitGenerated",
        "constructs_version": "constructsVersion",
        "context": "context",
        "deps": "deps",
        "description": "description",
        "dev_container": "devContainer",
        "dev_deps": "devDeps",
        "feature_flags": "featureFlags",
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
        "module_name": "moduleName",
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
        "require_approval": "requireApproval",
        "sample": "sample",
        "setup_config": "setupConfig",
        "setuptools": "setuptools",
        "stale": "stale",
        "stale_options": "staleOptions",
        "testdir": "testdir",
        "version": "version",
        "vscode": "vscode",
        "watch_excludes": "watchExcludes",
        "watch_includes": "watchIncludes",
    },
)
class AwsCdkPythonAppOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_command: typing.Optional[builtins.str] = None,
        cdk_assert: typing.Optional[builtins.bool] = None,
        cdk_assertions: typing.Optional[builtins.bool] = None,
        cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
        cdkout: typing.Optional[builtins.str] = None,
        cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_version: typing.Optional[builtins.str] = None,
        cdk_version_pinning: typing.Optional[builtins.bool] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        constructs_version: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        feature_flags: typing.Optional[builtins.bool] = None,
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
        module_name: typing.Optional[builtins.str] = None,
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
        require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
        sample: typing.Optional[builtins.bool] = None,
        setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        setuptools: typing.Optional[builtins.bool] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        testdir: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
        watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''AwsCdkPythonAppOptions.

        :param name: Default: $BASEDIR
        :param author_email: (experimental) Author's e-mail. Default: $GIT_USER_EMAIL
        :param author_name: (experimental) Author's name. Default: $GIT_USER_NAME
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param build_command: (experimental) A command to execute before synthesis. This command will be called when running ``cdk synth`` or when ``cdk watch`` identifies a change in your source code before redeployment. Default: - no build command
        :param cdk_assert: (deprecated) Warning: NodeJS only. Install the Default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0
        :param cdk_assertions: (experimental) Install the assertions library? Only needed for CDK 1.x. If using CDK 2.x then assertions is already included in 'aws-cdk-lib' Default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0
        :param cdk_dependencies: (deprecated) Which AWS CDKv1 modules this project requires.
        :param cdk_dependencies_as_deps: (deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``). This is to ensure that downstream consumers actually have your CDK dependencies installed when using npm < 7 or yarn, where peer dependencies are not automatically installed. If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure they are present during development. Note: this setting only applies to construct library projects Default: true
        :param cdkout: (experimental) cdk.out directory. Default: "cdk.out"
        :param cdk_test_dependencies: (deprecated) AWS CDK modules required for testing.
        :param cdk_version: (experimental) Minimum version of the AWS CDK to depend on. Default: "2.1.0"
        :param cdk_version_pinning: (experimental) Use pinned version instead of caret version for CDK. You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates. If you use experimental features this will let you define the moment you include breaking changes.
        :param classifiers: (experimental) A list of PyPI trove classifiers that describe the project.
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param constructs_version: (experimental) Minimum version of the ``constructs`` library to depend on. Default: - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is "10.0.5".
        :param context: (experimental) Additional context to include in ``cdk.json``. Default: - no additional context
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) A short description of the package.
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param dev_deps: (experimental) List of dev dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDevDependency()``. Default: []
        :param feature_flags: (experimental) Include all feature flags in cdk.json. Default: true
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
        :param module_name: (experimental) Name of the python package as used in imports and filenames. Must only consist of alphanumeric characters and underscores. Default: $PYTHON_MODULE_NAME
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
        :param require_approval: (experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them. Default: ApprovalLevel.BROADENING
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param setup_config: (experimental) Additional fields to pass in the setup() function if using setuptools.
        :param setuptools: (experimental) Use setuptools with a setup.py script for packaging and publishing. Default: - true, unless poetry is true, then false
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param testdir: (experimental) Python sources directory. Default: "tests"
        :param version: (experimental) Version of the package. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param watch_excludes: (experimental) Glob patterns to exclude from ``cdk watch``. Default: []
        :param watch_includes: (experimental) Glob patterns to include in ``cdk watch``. Default: []
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
            type_hints = typing.get_type_hints(_typecheckingstub__e05dda3da908a708305470f6c3db90baf552c1784e8fbb842f3a927f7577f28d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument cdk_assert", value=cdk_assert, expected_type=type_hints["cdk_assert"])
            check_type(argname="argument cdk_assertions", value=cdk_assertions, expected_type=type_hints["cdk_assertions"])
            check_type(argname="argument cdk_dependencies", value=cdk_dependencies, expected_type=type_hints["cdk_dependencies"])
            check_type(argname="argument cdk_dependencies_as_deps", value=cdk_dependencies_as_deps, expected_type=type_hints["cdk_dependencies_as_deps"])
            check_type(argname="argument cdkout", value=cdkout, expected_type=type_hints["cdkout"])
            check_type(argname="argument cdk_test_dependencies", value=cdk_test_dependencies, expected_type=type_hints["cdk_test_dependencies"])
            check_type(argname="argument cdk_version", value=cdk_version, expected_type=type_hints["cdk_version"])
            check_type(argname="argument cdk_version_pinning", value=cdk_version_pinning, expected_type=type_hints["cdk_version_pinning"])
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument constructs_version", value=constructs_version, expected_type=type_hints["constructs_version"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument feature_flags", value=feature_flags, expected_type=type_hints["feature_flags"])
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
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
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
            check_type(argname="argument require_approval", value=require_approval, expected_type=type_hints["require_approval"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument setup_config", value=setup_config, expected_type=type_hints["setup_config"])
            check_type(argname="argument setuptools", value=setuptools, expected_type=type_hints["setuptools"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument testdir", value=testdir, expected_type=type_hints["testdir"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument watch_excludes", value=watch_excludes, expected_type=type_hints["watch_excludes"])
            check_type(argname="argument watch_includes", value=watch_includes, expected_type=type_hints["watch_includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if build_command is not None:
            self._values["build_command"] = build_command
        if cdk_assert is not None:
            self._values["cdk_assert"] = cdk_assert
        if cdk_assertions is not None:
            self._values["cdk_assertions"] = cdk_assertions
        if cdk_dependencies is not None:
            self._values["cdk_dependencies"] = cdk_dependencies
        if cdk_dependencies_as_deps is not None:
            self._values["cdk_dependencies_as_deps"] = cdk_dependencies_as_deps
        if cdkout is not None:
            self._values["cdkout"] = cdkout
        if cdk_test_dependencies is not None:
            self._values["cdk_test_dependencies"] = cdk_test_dependencies
        if cdk_version is not None:
            self._values["cdk_version"] = cdk_version
        if cdk_version_pinning is not None:
            self._values["cdk_version_pinning"] = cdk_version_pinning
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if clobber is not None:
            self._values["clobber"] = clobber
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if constructs_version is not None:
            self._values["constructs_version"] = constructs_version
        if context is not None:
            self._values["context"] = context
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if feature_flags is not None:
            self._values["feature_flags"] = feature_flags
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
        if module_name is not None:
            self._values["module_name"] = module_name
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
        if require_approval is not None:
            self._values["require_approval"] = require_approval
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
        if testdir is not None:
            self._values["testdir"] = testdir
        if version is not None:
            self._values["version"] = version
        if vscode is not None:
            self._values["vscode"] = vscode
        if watch_excludes is not None:
            self._values["watch_excludes"] = watch_excludes
        if watch_includes is not None:
            self._values["watch_includes"] = watch_includes

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
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A command to execute before synthesis.

        This command will be called when
        running ``cdk synth`` or when ``cdk watch`` identifies a change in your source
        code before redeployment.

        :default: - no build command

        :stability: experimental
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_assert(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Warning: NodeJS only.

        Install the

        :default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0

        :deprecated: The

        :stability: deprecated
        :aws-cdk: /assertions (in V1) and included in ``aws-cdk-lib`` for V2.
        '''
        result = self._values.get("cdk_assert")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_assertions(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install the assertions library?

        Only needed for CDK 1.x. If using CDK 2.x then
        assertions is already included in 'aws-cdk-lib'

        :default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0

        :stability: experimental
        '''
        result = self._values.get("cdk_assertions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Which AWS CDKv1 modules this project requires.

        :deprecated: For CDK 2.x use "deps" instead. (or "peerDeps" if you're building a library)

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_dependencies_as_deps(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``).

        This is to ensure that downstream consumers actually have your CDK dependencies installed
        when using npm < 7 or yarn, where peer dependencies are not automatically installed.
        If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure
        they are present during development.

        Note: this setting only applies to construct library projects

        :default: true

        :deprecated: Not supported in CDK v2.

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies_as_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdkout(self) -> typing.Optional[builtins.str]:
        '''(experimental) cdk.out directory.

        :default: "cdk.out"

        :stability: experimental
        '''
        result = self._values.get("cdkout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_test_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) AWS CDK modules required for testing.

        :deprecated: For CDK 2.x use 'devDeps' (in node.js projects) or 'testDeps' (in java projects) instead

        :stability: deprecated
        '''
        result = self._values.get("cdk_test_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the AWS CDK to depend on.

        :default: "2.1.0"

        :stability: experimental
        '''
        result = self._values.get("cdk_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_version_pinning(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use pinned version instead of caret version for CDK.

        You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates.
        If you use experimental features this will let you define the moment you include breaking changes.

        :stability: experimental
        '''
        result = self._values.get("cdk_version_pinning")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def constructs_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the ``constructs`` library to depend on.

        :default:

        - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is
        "10.0.5".

        :stability: experimental
        '''
        result = self._values.get("constructs_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional context to include in ``cdk.json``.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

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
    def feature_flags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include all feature flags in cdk.json.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("feature_flags")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def module_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the python package as used in imports and filenames.

        Must only consist of alphanumeric characters and underscores.

        :default: $PYTHON_MODULE_NAME

        :stability: experimental
        '''
        result = self._values.get("module_name")
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
    def require_approval(
        self,
    ) -> typing.Optional[_projen_awscdk_04054675.ApprovalLevel]:
        '''(experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them.

        :default: ApprovalLevel.BROADENING

        :stability: experimental
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[_projen_awscdk_04054675.ApprovalLevel], result)

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
    def testdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Python sources directory.

        :default: "tests"

        :stability: experimental
        '''
        result = self._values.get("testdir")
        return typing.cast(typing.Optional[builtins.str], result)

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
    def watch_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to exclude from ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def watch_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to include in ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCdkPythonAppOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.infrastructure.AwsCdkTypeScriptAppOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_library_dependencies": "allowLibraryDependencies",
        "app_entrypoint": "appEntrypoint",
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
        "build_command": "buildCommand",
        "build_workflow": "buildWorkflow",
        "build_workflow_options": "buildWorkflowOptions",
        "build_workflow_triggers": "buildWorkflowTriggers",
        "bundled_deps": "bundledDeps",
        "bundler_options": "bundlerOptions",
        "cdk_assert": "cdkAssert",
        "cdk_assertions": "cdkAssertions",
        "cdk_dependencies": "cdkDependencies",
        "cdk_dependencies_as_deps": "cdkDependenciesAsDeps",
        "cdkout": "cdkout",
        "cdk_test_dependencies": "cdkTestDependencies",
        "cdk_version": "cdkVersion",
        "cdk_version_pinning": "cdkVersionPinning",
        "check_licenses": "checkLicenses",
        "clobber": "clobber",
        "code_artifact_options": "codeArtifactOptions",
        "code_cov": "codeCov",
        "code_cov_token_secret": "codeCovTokenSecret",
        "commit_generated": "commitGenerated",
        "constructs_version": "constructsVersion",
        "context": "context",
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
        "edge_lambda_auto_discover": "edgeLambdaAutoDiscover",
        "entrypoint": "entrypoint",
        "entrypoint_types": "entrypointTypes",
        "eslint": "eslint",
        "eslint_options": "eslintOptions",
        "experimental_integ_runner": "experimentalIntegRunner",
        "feature_flags": "featureFlags",
        "github": "github",
        "github_options": "githubOptions",
        "gitignore": "gitignore",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "gitpod": "gitpod",
        "homepage": "homepage",
        "integration_test_auto_discover": "integrationTestAutoDiscover",
        "jest": "jest",
        "jest_options": "jestOptions",
        "jsii_release_version": "jsiiReleaseVersion",
        "keywords": "keywords",
        "lambda_auto_discover": "lambdaAutoDiscover",
        "lambda_extension_auto_discover": "lambdaExtensionAutoDiscover",
        "lambda_options": "lambdaOptions",
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
        "require_approval": "requireApproval",
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
        "watch_excludes": "watchExcludes",
        "watch_includes": "watchIncludes",
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
class AwsCdkTypeScriptAppOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        app_entrypoint: typing.Optional[builtins.str] = None,
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
        build_command: typing.Optional[builtins.str] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cdk_assert: typing.Optional[builtins.bool] = None,
        cdk_assertions: typing.Optional[builtins.bool] = None,
        cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
        cdkout: typing.Optional[builtins.str] = None,
        cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_version: typing.Optional[builtins.str] = None,
        cdk_version_pinning: typing.Optional[builtins.bool] = None,
        check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        constructs_version: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
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
        edge_lambda_auto_discover: typing.Optional[builtins.bool] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        entrypoint_types: typing.Optional[builtins.str] = None,
        eslint: typing.Optional[builtins.bool] = None,
        eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        experimental_integ_runner: typing.Optional[builtins.bool] = None,
        feature_flags: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        integration_test_auto_discover: typing.Optional[builtins.bool] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_auto_discover: typing.Optional[builtins.bool] = None,
        lambda_extension_auto_discover: typing.Optional[builtins.bool] = None,
        lambda_options: typing.Optional[typing.Union[_projen_awscdk_04054675.LambdaFunctionCommonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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
        require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
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
        watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_git_identity: typing.Optional[typing.Union[_projen_github_04054675.GitIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_package_cache: typing.Optional[builtins.bool] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_projen_04054675.GroupRunnerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        yarn_berry_options: typing.Optional[typing.Union[_projen_javascript_04054675.YarnBerryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''AwsCdkTypeScriptAppOptions.

        :param name: Default: $BASEDIR
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param app_entrypoint: (experimental) The CDK app's entrypoint (relative to the source directory, which is "src" by default). Default: "main.ts"
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
        :param build_command: (experimental) A command to execute before synthesis. This command will be called when running ``cdk synth`` or when ``cdk watch`` identifies a change in your source code before redeployment. Default: - no build command
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_options: (experimental) Options for PR build workflow.
        :param build_workflow_triggers: (deprecated) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param cdk_assert: (deprecated) Warning: NodeJS only. Install the Default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0
        :param cdk_assertions: (experimental) Install the assertions library? Only needed for CDK 1.x. If using CDK 2.x then assertions is already included in 'aws-cdk-lib' Default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0
        :param cdk_dependencies: (deprecated) Which AWS CDKv1 modules this project requires.
        :param cdk_dependencies_as_deps: (deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``). This is to ensure that downstream consumers actually have your CDK dependencies installed when using npm < 7 or yarn, where peer dependencies are not automatically installed. If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure they are present during development. Note: this setting only applies to construct library projects Default: true
        :param cdkout: (experimental) cdk.out directory. Default: "cdk.out"
        :param cdk_test_dependencies: (deprecated) AWS CDK modules required for testing.
        :param cdk_version: (experimental) Minimum version of the AWS CDK to depend on. Default: "2.1.0"
        :param cdk_version_pinning: (experimental) Use pinned version instead of caret version for CDK. You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates. If you use experimental features this will let you define the moment you include breaking changes.
        :param check_licenses: (experimental) Configure which licenses should be deemed acceptable for use by dependencies. This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered. Default: - no license checks are run during the build and all licenses will be accepted
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v4 A secret is required for private repos. Configured with ``@codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories. Default: - if this option is not specified, only public repositories are supported
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param constructs_version: (experimental) Minimum version of the ``constructs`` library to depend on. Default: - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is "10.0.5".
        :param context: (experimental) Additional context to include in ``cdk.json``. Default: - no additional context
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
        :param edge_lambda_auto_discover: (experimental) Automatically adds an ``cloudfront.experimental.EdgeFunction`` for each ``.edge-lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project. Default: true
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json. Default: "lib/index.js"
        :param entrypoint_types: (experimental) The .d.ts file that includes the type declarations for this module. Default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)
        :param eslint: (experimental) Setup eslint. Default: true
        :param eslint_options: (experimental) Eslint options. Default: - opinionated default options
        :param experimental_integ_runner: (experimental) Enable experimental support for the AWS CDK integ-runner. Default: false
        :param feature_flags: (experimental) Include all feature flags in cdk.json. Default: true
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param homepage: (experimental) Package's Homepage / Website.
        :param integration_test_auto_discover: (experimental) Automatically discovers and creates integration tests for each ``.integ.ts`` file in under your test directory. Default: true
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param lambda_auto_discover: (experimental) Automatically adds an ``awscdk.LambdaFunction`` for each ``.lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project. Default: true
        :param lambda_extension_auto_discover: (experimental) Automatically adds an ``awscdk.LambdaExtension`` for each ``.lambda-extension.ts`` entrypoint in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project. Default: true
        :param lambda_options: (experimental) Common options for all AWS Lambda functions. Default: - default options
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
        :param require_approval: (experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them. Default: ApprovalLevel.BROADENING
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
        :param watch_excludes: (experimental) Glob patterns to exclude from ``cdk watch``. Default: []
        :param watch_includes: (experimental) Glob patterns to include in ``cdk watch``. Default: []
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
        if isinstance(lambda_options, dict):
            lambda_options = _projen_awscdk_04054675.LambdaFunctionCommonOptions(**lambda_options)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d18b26cb9f80927dee1642f1695c52ae992d3f492f97ff41c4a8baf4c9e5fd9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_library_dependencies", value=allow_library_dependencies, expected_type=type_hints["allow_library_dependencies"])
            check_type(argname="argument app_entrypoint", value=app_entrypoint, expected_type=type_hints["app_entrypoint"])
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
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_workflow", value=build_workflow, expected_type=type_hints["build_workflow"])
            check_type(argname="argument build_workflow_options", value=build_workflow_options, expected_type=type_hints["build_workflow_options"])
            check_type(argname="argument build_workflow_triggers", value=build_workflow_triggers, expected_type=type_hints["build_workflow_triggers"])
            check_type(argname="argument bundled_deps", value=bundled_deps, expected_type=type_hints["bundled_deps"])
            check_type(argname="argument bundler_options", value=bundler_options, expected_type=type_hints["bundler_options"])
            check_type(argname="argument cdk_assert", value=cdk_assert, expected_type=type_hints["cdk_assert"])
            check_type(argname="argument cdk_assertions", value=cdk_assertions, expected_type=type_hints["cdk_assertions"])
            check_type(argname="argument cdk_dependencies", value=cdk_dependencies, expected_type=type_hints["cdk_dependencies"])
            check_type(argname="argument cdk_dependencies_as_deps", value=cdk_dependencies_as_deps, expected_type=type_hints["cdk_dependencies_as_deps"])
            check_type(argname="argument cdkout", value=cdkout, expected_type=type_hints["cdkout"])
            check_type(argname="argument cdk_test_dependencies", value=cdk_test_dependencies, expected_type=type_hints["cdk_test_dependencies"])
            check_type(argname="argument cdk_version", value=cdk_version, expected_type=type_hints["cdk_version"])
            check_type(argname="argument cdk_version_pinning", value=cdk_version_pinning, expected_type=type_hints["cdk_version_pinning"])
            check_type(argname="argument check_licenses", value=check_licenses, expected_type=type_hints["check_licenses"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument code_cov", value=code_cov, expected_type=type_hints["code_cov"])
            check_type(argname="argument code_cov_token_secret", value=code_cov_token_secret, expected_type=type_hints["code_cov_token_secret"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument constructs_version", value=constructs_version, expected_type=type_hints["constructs_version"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
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
            check_type(argname="argument edge_lambda_auto_discover", value=edge_lambda_auto_discover, expected_type=type_hints["edge_lambda_auto_discover"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument entrypoint_types", value=entrypoint_types, expected_type=type_hints["entrypoint_types"])
            check_type(argname="argument eslint", value=eslint, expected_type=type_hints["eslint"])
            check_type(argname="argument eslint_options", value=eslint_options, expected_type=type_hints["eslint_options"])
            check_type(argname="argument experimental_integ_runner", value=experimental_integ_runner, expected_type=type_hints["experimental_integ_runner"])
            check_type(argname="argument feature_flags", value=feature_flags, expected_type=type_hints["feature_flags"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument gitignore", value=gitignore, expected_type=type_hints["gitignore"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument integration_test_auto_discover", value=integration_test_auto_discover, expected_type=type_hints["integration_test_auto_discover"])
            check_type(argname="argument jest", value=jest, expected_type=type_hints["jest"])
            check_type(argname="argument jest_options", value=jest_options, expected_type=type_hints["jest_options"])
            check_type(argname="argument jsii_release_version", value=jsii_release_version, expected_type=type_hints["jsii_release_version"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument lambda_auto_discover", value=lambda_auto_discover, expected_type=type_hints["lambda_auto_discover"])
            check_type(argname="argument lambda_extension_auto_discover", value=lambda_extension_auto_discover, expected_type=type_hints["lambda_extension_auto_discover"])
            check_type(argname="argument lambda_options", value=lambda_options, expected_type=type_hints["lambda_options"])
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
            check_type(argname="argument require_approval", value=require_approval, expected_type=type_hints["require_approval"])
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
            check_type(argname="argument watch_excludes", value=watch_excludes, expected_type=type_hints["watch_excludes"])
            check_type(argname="argument watch_includes", value=watch_includes, expected_type=type_hints["watch_includes"])
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
        if app_entrypoint is not None:
            self._values["app_entrypoint"] = app_entrypoint
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
        if build_command is not None:
            self._values["build_command"] = build_command
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
        if cdk_assert is not None:
            self._values["cdk_assert"] = cdk_assert
        if cdk_assertions is not None:
            self._values["cdk_assertions"] = cdk_assertions
        if cdk_dependencies is not None:
            self._values["cdk_dependencies"] = cdk_dependencies
        if cdk_dependencies_as_deps is not None:
            self._values["cdk_dependencies_as_deps"] = cdk_dependencies_as_deps
        if cdkout is not None:
            self._values["cdkout"] = cdkout
        if cdk_test_dependencies is not None:
            self._values["cdk_test_dependencies"] = cdk_test_dependencies
        if cdk_version is not None:
            self._values["cdk_version"] = cdk_version
        if cdk_version_pinning is not None:
            self._values["cdk_version_pinning"] = cdk_version_pinning
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
        if constructs_version is not None:
            self._values["constructs_version"] = constructs_version
        if context is not None:
            self._values["context"] = context
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
        if edge_lambda_auto_discover is not None:
            self._values["edge_lambda_auto_discover"] = edge_lambda_auto_discover
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if entrypoint_types is not None:
            self._values["entrypoint_types"] = entrypoint_types
        if eslint is not None:
            self._values["eslint"] = eslint
        if eslint_options is not None:
            self._values["eslint_options"] = eslint_options
        if experimental_integ_runner is not None:
            self._values["experimental_integ_runner"] = experimental_integ_runner
        if feature_flags is not None:
            self._values["feature_flags"] = feature_flags
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
        if integration_test_auto_discover is not None:
            self._values["integration_test_auto_discover"] = integration_test_auto_discover
        if jest is not None:
            self._values["jest"] = jest
        if jest_options is not None:
            self._values["jest_options"] = jest_options
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if keywords is not None:
            self._values["keywords"] = keywords
        if lambda_auto_discover is not None:
            self._values["lambda_auto_discover"] = lambda_auto_discover
        if lambda_extension_auto_discover is not None:
            self._values["lambda_extension_auto_discover"] = lambda_extension_auto_discover
        if lambda_options is not None:
            self._values["lambda_options"] = lambda_options
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
        if require_approval is not None:
            self._values["require_approval"] = require_approval
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
        if watch_excludes is not None:
            self._values["watch_excludes"] = watch_excludes
        if watch_includes is not None:
            self._values["watch_includes"] = watch_includes
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
    def app_entrypoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) The CDK app's entrypoint (relative to the source directory, which is "src" by default).

        :default: "main.ts"

        :stability: experimental
        '''
        result = self._values.get("app_entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

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
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A command to execute before synthesis.

        This command will be called when
        running ``cdk synth`` or when ``cdk watch`` identifies a change in your source
        code before redeployment.

        :default: - no build command

        :stability: experimental
        '''
        result = self._values.get("build_command")
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
    def cdk_assert(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Warning: NodeJS only.

        Install the

        :default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0

        :deprecated: The

        :stability: deprecated
        :aws-cdk: /assertions (in V1) and included in ``aws-cdk-lib`` for V2.
        '''
        result = self._values.get("cdk_assert")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_assertions(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install the assertions library?

        Only needed for CDK 1.x. If using CDK 2.x then
        assertions is already included in 'aws-cdk-lib'

        :default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0

        :stability: experimental
        '''
        result = self._values.get("cdk_assertions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Which AWS CDKv1 modules this project requires.

        :deprecated: For CDK 2.x use "deps" instead. (or "peerDeps" if you're building a library)

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_dependencies_as_deps(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``).

        This is to ensure that downstream consumers actually have your CDK dependencies installed
        when using npm < 7 or yarn, where peer dependencies are not automatically installed.
        If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure
        they are present during development.

        Note: this setting only applies to construct library projects

        :default: true

        :deprecated: Not supported in CDK v2.

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies_as_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdkout(self) -> typing.Optional[builtins.str]:
        '''(experimental) cdk.out directory.

        :default: "cdk.out"

        :stability: experimental
        '''
        result = self._values.get("cdkout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_test_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) AWS CDK modules required for testing.

        :deprecated: For CDK 2.x use 'devDeps' (in node.js projects) or 'testDeps' (in java projects) instead

        :stability: deprecated
        '''
        result = self._values.get("cdk_test_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the AWS CDK to depend on.

        :default: "2.1.0"

        :stability: experimental
        '''
        result = self._values.get("cdk_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_version_pinning(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use pinned version instead of caret version for CDK.

        You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates.
        If you use experimental features this will let you define the moment you include breaking changes.

        :stability: experimental
        '''
        result = self._values.get("cdk_version_pinning")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def constructs_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the ``constructs`` library to depend on.

        :default:

        - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is
        "10.0.5".

        :stability: experimental
        '''
        result = self._values.get("constructs_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional context to include in ``cdk.json``.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

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
        :featured: true
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
    def edge_lambda_auto_discover(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically adds an ``cloudfront.experimental.EdgeFunction`` for each ``.edge-lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edge_lambda_auto_discover")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def experimental_integ_runner(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable experimental support for the AWS CDK integ-runner.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("experimental_integ_runner")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def feature_flags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include all feature flags in cdk.json.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("feature_flags")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def integration_test_auto_discover(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically discovers and creates integration tests for each ``.integ.ts`` file in under your test directory.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("integration_test_auto_discover")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def lambda_auto_discover(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically adds an ``awscdk.LambdaFunction`` for each ``.lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("lambda_auto_discover")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lambda_extension_auto_discover(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically adds an ``awscdk.LambdaExtension`` for each ``.lambda-extension.ts`` entrypoint in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("lambda_extension_auto_discover")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lambda_options(
        self,
    ) -> typing.Optional[_projen_awscdk_04054675.LambdaFunctionCommonOptions]:
        '''(experimental) Common options for all AWS Lambda functions.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("lambda_options")
        return typing.cast(typing.Optional[_projen_awscdk_04054675.LambdaFunctionCommonOptions], result)

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
        :featured: true
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
    def require_approval(
        self,
    ) -> typing.Optional[_projen_awscdk_04054675.ApprovalLevel]:
        '''(experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them.

        :default: ApprovalLevel.BROADENING

        :stability: experimental
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[_projen_awscdk_04054675.ApprovalLevel], result)

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
    def watch_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to exclude from ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def watch_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to include in ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

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
        return "AwsCdkTypeScriptAppOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.infrastructure.DeploymentStage",
    jsii_struct_bases=[],
    name_mapping={"account": "account", "region": "region", "stage_name": "stageName"},
)
class DeploymentStage:
    def __init__(
        self,
        *,
        account: jsii.Number,
        region: builtins.str,
        stage_name: builtins.str,
    ) -> None:
        '''
        :param account: Account to deploy into.
        :param region: AWS region to deploy into.
        :param stage_name: Stage name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b730d5a9529973352ea249c46d5732448dd09ac35400ac252ba0be082864168)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "region": region,
            "stage_name": stage_name,
        }

    @builtins.property
    def account(self) -> jsii.Number:
        '''Account to deploy into.'''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''AWS region to deploy into.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''Stage name.'''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentStage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InfrastructureJavaProject(
    _projen_awscdk_04054675.AwsCdkJavaApp,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.infrastructure.InfrastructureJavaProject",
):
    '''Synthesizes a Infrastructure Java Project.'''

    def __init__(
        self,
        *,
        allow_signup: typing.Optional[builtins.bool] = None,
        cloudscape_react_ts_website: typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f] = None,
        cloudscape_react_ts_websites: typing.Optional[typing.Sequence[_CloudscapeReactTsWebsiteProject_ef2bfd2f]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[typing.Union[DeploymentStage, typing.Dict[builtins.str, typing.Any]]]] = None,
        type_safe_api: typing.Optional[_TypeSafeApiProject_b9e4f1cf] = None,
        type_safe_apis: typing.Optional[typing.Sequence[_TypeSafeApiProject_b9e4f1cf]] = None,
        name: builtins.str,
        artifact_id: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_command: typing.Optional[builtins.str] = None,
        cdk_assert: typing.Optional[builtins.bool] = None,
        cdk_assertions: typing.Optional[builtins.bool] = None,
        cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
        cdkout: typing.Optional[builtins.str] = None,
        cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_version: typing.Optional[builtins.str] = None,
        cdk_version_pinning: typing.Optional[builtins.bool] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        constructs_version: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        distdir: typing.Optional[builtins.str] = None,
        feature_flags: typing.Optional[builtins.bool] = None,
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
        require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
        sample: typing.Optional[builtins.bool] = None,
        sample_java_package: typing.Optional[builtins.str] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
        watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_signup: Allow self sign up for the UserIdentity construct. Default: - false
        :param cloudscape_react_ts_website: (deprecated) CloudscapeReactTsWebsiteProject instance to use when setting up the initial project sample code.
        :param cloudscape_react_ts_websites: CloudscapeReactTsWebsiteProject instances to use when setting up the initial project sample code.
        :param stack_name: Stack name. Default: infra-dev
        :param stages: List of deployment stages.
        :param type_safe_api: (deprecated) TypeSafeApi instance to use when setting up the initial project sample code.
        :param type_safe_apis: TypeSafeApi instances to use when setting up the initial project sample code.
        :param name: Default: $BASEDIR
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param build_command: (experimental) A command to execute before synthesis. This command will be called when running ``cdk synth`` or when ``cdk watch`` identifies a change in your source code before redeployment. Default: - no build command
        :param cdk_assert: (deprecated) Warning: NodeJS only. Install the Default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0
        :param cdk_assertions: (experimental) Install the assertions library? Only needed for CDK 1.x. If using CDK 2.x then assertions is already included in 'aws-cdk-lib' Default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0
        :param cdk_dependencies: (deprecated) Which AWS CDKv1 modules this project requires.
        :param cdk_dependencies_as_deps: (deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``). This is to ensure that downstream consumers actually have your CDK dependencies installed when using npm < 7 or yarn, where peer dependencies are not automatically installed. If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure they are present during development. Note: this setting only applies to construct library projects Default: true
        :param cdkout: (experimental) cdk.out directory. Default: "cdk.out"
        :param cdk_test_dependencies: (deprecated) AWS CDK modules required for testing.
        :param cdk_version: (experimental) Minimum version of the AWS CDK to depend on. Default: "2.1.0"
        :param cdk_version_pinning: (experimental) Use pinned version instead of caret version for CDK. You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates. If you use experimental features this will let you define the moment you include breaking changes.
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param compile_options: (experimental) Compile options. Default: - defaults
        :param constructs_version: (experimental) Minimum version of the ``constructs`` library to depend on. Default: - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is "10.0.5".
        :param context: (experimental) Additional context to include in ``cdk.json``. Default: - no additional context
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param distdir: (experimental) Final artifact output directory. Default: "dist/java"
        :param feature_flags: (experimental) Include all feature flags in cdk.json. Default: true
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
        :param require_approval: (experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them. Default: ApprovalLevel.BROADENING
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param sample_java_package: (experimental) The java package to use for the code sample. Default: "org.acme"
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param test_deps: (experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addTestDependency()``. Default: []
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param watch_excludes: (experimental) Glob patterns to exclude from ``cdk watch``. Default: []
        :param watch_includes: (experimental) Glob patterns to include in ``cdk watch``. Default: []
        '''
        options = InfrastructureJavaProjectOptions(
            allow_signup=allow_signup,
            cloudscape_react_ts_website=cloudscape_react_ts_website,
            cloudscape_react_ts_websites=cloudscape_react_ts_websites,
            stack_name=stack_name,
            stages=stages,
            type_safe_api=type_safe_api,
            type_safe_apis=type_safe_apis,
            name=name,
            artifact_id=artifact_id,
            auto_approve_options=auto_approve_options,
            auto_merge=auto_merge,
            auto_merge_options=auto_merge_options,
            build_command=build_command,
            cdk_assert=cdk_assert,
            cdk_assertions=cdk_assertions,
            cdk_dependencies=cdk_dependencies,
            cdk_dependencies_as_deps=cdk_dependencies_as_deps,
            cdkout=cdkout,
            cdk_test_dependencies=cdk_test_dependencies,
            cdk_version=cdk_version,
            cdk_version_pinning=cdk_version_pinning,
            clobber=clobber,
            commit_generated=commit_generated,
            compile_options=compile_options,
            constructs_version=constructs_version,
            context=context,
            deps=deps,
            description=description,
            dev_container=dev_container,
            distdir=distdir,
            feature_flags=feature_flags,
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
            require_approval=require_approval,
            sample=sample,
            sample_java_package=sample_java_package,
            stale=stale,
            stale_options=stale_options,
            test_deps=test_deps,
            url=url,
            version=version,
            vscode=vscode,
            watch_excludes=watch_excludes,
            watch_includes=watch_includes,
        )

        jsii.create(self.__class__, self, [options])


@jsii.data_type(
    jsii_type="@aws/pdk.infrastructure.InfrastructureJavaProjectOptions",
    jsii_struct_bases=[AwsCdkJavaAppOptions],
    name_mapping={
        "name": "name",
        "artifact_id": "artifactId",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "build_command": "buildCommand",
        "cdk_assert": "cdkAssert",
        "cdk_assertions": "cdkAssertions",
        "cdk_dependencies": "cdkDependencies",
        "cdk_dependencies_as_deps": "cdkDependenciesAsDeps",
        "cdkout": "cdkout",
        "cdk_test_dependencies": "cdkTestDependencies",
        "cdk_version": "cdkVersion",
        "cdk_version_pinning": "cdkVersionPinning",
        "clobber": "clobber",
        "commit_generated": "commitGenerated",
        "compile_options": "compileOptions",
        "constructs_version": "constructsVersion",
        "context": "context",
        "deps": "deps",
        "description": "description",
        "dev_container": "devContainer",
        "distdir": "distdir",
        "feature_flags": "featureFlags",
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
        "require_approval": "requireApproval",
        "sample": "sample",
        "sample_java_package": "sampleJavaPackage",
        "stale": "stale",
        "stale_options": "staleOptions",
        "test_deps": "testDeps",
        "url": "url",
        "version": "version",
        "vscode": "vscode",
        "watch_excludes": "watchExcludes",
        "watch_includes": "watchIncludes",
        "allow_signup": "allowSignup",
        "cloudscape_react_ts_website": "cloudscapeReactTsWebsite",
        "cloudscape_react_ts_websites": "cloudscapeReactTsWebsites",
        "stack_name": "stackName",
        "stages": "stages",
        "type_safe_api": "typeSafeApi",
        "type_safe_apis": "typeSafeApis",
    },
)
class InfrastructureJavaProjectOptions(AwsCdkJavaAppOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        artifact_id: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_command: typing.Optional[builtins.str] = None,
        cdk_assert: typing.Optional[builtins.bool] = None,
        cdk_assertions: typing.Optional[builtins.bool] = None,
        cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
        cdkout: typing.Optional[builtins.str] = None,
        cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_version: typing.Optional[builtins.str] = None,
        cdk_version_pinning: typing.Optional[builtins.bool] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        constructs_version: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        distdir: typing.Optional[builtins.str] = None,
        feature_flags: typing.Optional[builtins.bool] = None,
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
        require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
        sample: typing.Optional[builtins.bool] = None,
        sample_java_package: typing.Optional[builtins.str] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
        watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_signup: typing.Optional[builtins.bool] = None,
        cloudscape_react_ts_website: typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f] = None,
        cloudscape_react_ts_websites: typing.Optional[typing.Sequence[_CloudscapeReactTsWebsiteProject_ef2bfd2f]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[typing.Union[DeploymentStage, typing.Dict[builtins.str, typing.Any]]]] = None,
        type_safe_api: typing.Optional[_TypeSafeApiProject_b9e4f1cf] = None,
        type_safe_apis: typing.Optional[typing.Sequence[_TypeSafeApiProject_b9e4f1cf]] = None,
    ) -> None:
        '''Configuration options for the InfrastructureJavaProject.

        :param name: Default: $BASEDIR
        :param artifact_id: (experimental) The artifactId is generally the name that the project is known by. Although the groupId is important, people within the group will rarely mention the groupId in discussion (they are often all be the same ID, such as the MojoHaus project groupId: org.codehaus.mojo). It, along with the groupId, creates a key that separates this project from every other project in the world (at least, it should :) ). Along with the groupId, the artifactId fully defines the artifact's living quarters within the repository. In the case of the above project, my-project lives in $M2_REPO/org/codehaus/mojo/my-project. Default: "my-app"
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param build_command: (experimental) A command to execute before synthesis. This command will be called when running ``cdk synth`` or when ``cdk watch`` identifies a change in your source code before redeployment. Default: - no build command
        :param cdk_assert: (deprecated) Warning: NodeJS only. Install the Default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0
        :param cdk_assertions: (experimental) Install the assertions library? Only needed for CDK 1.x. If using CDK 2.x then assertions is already included in 'aws-cdk-lib' Default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0
        :param cdk_dependencies: (deprecated) Which AWS CDKv1 modules this project requires.
        :param cdk_dependencies_as_deps: (deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``). This is to ensure that downstream consumers actually have your CDK dependencies installed when using npm < 7 or yarn, where peer dependencies are not automatically installed. If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure they are present during development. Note: this setting only applies to construct library projects Default: true
        :param cdkout: (experimental) cdk.out directory. Default: "cdk.out"
        :param cdk_test_dependencies: (deprecated) AWS CDK modules required for testing.
        :param cdk_version: (experimental) Minimum version of the AWS CDK to depend on. Default: "2.1.0"
        :param cdk_version_pinning: (experimental) Use pinned version instead of caret version for CDK. You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates. If you use experimental features this will let you define the moment you include breaking changes.
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param compile_options: (experimental) Compile options. Default: - defaults
        :param constructs_version: (experimental) Minimum version of the ``constructs`` library to depend on. Default: - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is "10.0.5".
        :param context: (experimental) Additional context to include in ``cdk.json``. Default: - no additional context
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) Description of a project is always good. Although this should not replace formal documentation, a quick comment to any readers of the POM is always helpful. Default: undefined
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param distdir: (experimental) Final artifact output directory. Default: "dist/java"
        :param feature_flags: (experimental) Include all feature flags in cdk.json. Default: true
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
        :param require_approval: (experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them. Default: ApprovalLevel.BROADENING
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param sample_java_package: (experimental) The java package to use for the code sample. Default: "org.acme"
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param test_deps: (experimental) List of test dependencies for this project. Dependencies use the format: ``<groupId>/<artifactId>@<semver>``. Additional dependencies can be added via ``project.addTestDependency()``. Default: []
        :param url: (experimental) The URL, like the name, is not required. This is a nice gesture for projects users, however, so that they know where the project lives. Default: undefined
        :param version: (experimental) This is the last piece of the naming puzzle. groupId:artifactId denotes a single project but they cannot delineate which incarnation of that project we are talking about. Do we want the junit:junit of 2018 (version 4.12), or of 2007 (version 3.8.2)? In short: code changes, those changes should be versioned, and this element keeps those versions in line. It is also used within an artifact's repository to separate versions from each other. my-project version 1.0 files live in the directory structure $M2_REPO/org/codehaus/mojo/my-project/1.0. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param watch_excludes: (experimental) Glob patterns to exclude from ``cdk watch``. Default: []
        :param watch_includes: (experimental) Glob patterns to include in ``cdk watch``. Default: []
        :param allow_signup: Allow self sign up for the UserIdentity construct. Default: - false
        :param cloudscape_react_ts_website: (deprecated) CloudscapeReactTsWebsiteProject instance to use when setting up the initial project sample code.
        :param cloudscape_react_ts_websites: CloudscapeReactTsWebsiteProject instances to use when setting up the initial project sample code.
        :param stack_name: Stack name. Default: infra-dev
        :param stages: List of deployment stages.
        :param type_safe_api: (deprecated) TypeSafeApi instance to use when setting up the initial project sample code.
        :param type_safe_apis: TypeSafeApi instances to use when setting up the initial project sample code.
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d1710385bc23fdc48cd7d8c347c87ab551177038b183cf7fa1d2bac8ec9bd68)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument cdk_assert", value=cdk_assert, expected_type=type_hints["cdk_assert"])
            check_type(argname="argument cdk_assertions", value=cdk_assertions, expected_type=type_hints["cdk_assertions"])
            check_type(argname="argument cdk_dependencies", value=cdk_dependencies, expected_type=type_hints["cdk_dependencies"])
            check_type(argname="argument cdk_dependencies_as_deps", value=cdk_dependencies_as_deps, expected_type=type_hints["cdk_dependencies_as_deps"])
            check_type(argname="argument cdkout", value=cdkout, expected_type=type_hints["cdkout"])
            check_type(argname="argument cdk_test_dependencies", value=cdk_test_dependencies, expected_type=type_hints["cdk_test_dependencies"])
            check_type(argname="argument cdk_version", value=cdk_version, expected_type=type_hints["cdk_version"])
            check_type(argname="argument cdk_version_pinning", value=cdk_version_pinning, expected_type=type_hints["cdk_version_pinning"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument compile_options", value=compile_options, expected_type=type_hints["compile_options"])
            check_type(argname="argument constructs_version", value=constructs_version, expected_type=type_hints["constructs_version"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument distdir", value=distdir, expected_type=type_hints["distdir"])
            check_type(argname="argument feature_flags", value=feature_flags, expected_type=type_hints["feature_flags"])
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
            check_type(argname="argument require_approval", value=require_approval, expected_type=type_hints["require_approval"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument sample_java_package", value=sample_java_package, expected_type=type_hints["sample_java_package"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument test_deps", value=test_deps, expected_type=type_hints["test_deps"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument watch_excludes", value=watch_excludes, expected_type=type_hints["watch_excludes"])
            check_type(argname="argument watch_includes", value=watch_includes, expected_type=type_hints["watch_includes"])
            check_type(argname="argument allow_signup", value=allow_signup, expected_type=type_hints["allow_signup"])
            check_type(argname="argument cloudscape_react_ts_website", value=cloudscape_react_ts_website, expected_type=type_hints["cloudscape_react_ts_website"])
            check_type(argname="argument cloudscape_react_ts_websites", value=cloudscape_react_ts_websites, expected_type=type_hints["cloudscape_react_ts_websites"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
            check_type(argname="argument type_safe_api", value=type_safe_api, expected_type=type_hints["type_safe_api"])
            check_type(argname="argument type_safe_apis", value=type_safe_apis, expected_type=type_hints["type_safe_apis"])
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
        if build_command is not None:
            self._values["build_command"] = build_command
        if cdk_assert is not None:
            self._values["cdk_assert"] = cdk_assert
        if cdk_assertions is not None:
            self._values["cdk_assertions"] = cdk_assertions
        if cdk_dependencies is not None:
            self._values["cdk_dependencies"] = cdk_dependencies
        if cdk_dependencies_as_deps is not None:
            self._values["cdk_dependencies_as_deps"] = cdk_dependencies_as_deps
        if cdkout is not None:
            self._values["cdkout"] = cdkout
        if cdk_test_dependencies is not None:
            self._values["cdk_test_dependencies"] = cdk_test_dependencies
        if cdk_version is not None:
            self._values["cdk_version"] = cdk_version
        if cdk_version_pinning is not None:
            self._values["cdk_version_pinning"] = cdk_version_pinning
        if clobber is not None:
            self._values["clobber"] = clobber
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if compile_options is not None:
            self._values["compile_options"] = compile_options
        if constructs_version is not None:
            self._values["constructs_version"] = constructs_version
        if context is not None:
            self._values["context"] = context
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if distdir is not None:
            self._values["distdir"] = distdir
        if feature_flags is not None:
            self._values["feature_flags"] = feature_flags
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
        if require_approval is not None:
            self._values["require_approval"] = require_approval
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
        if watch_excludes is not None:
            self._values["watch_excludes"] = watch_excludes
        if watch_includes is not None:
            self._values["watch_includes"] = watch_includes
        if allow_signup is not None:
            self._values["allow_signup"] = allow_signup
        if cloudscape_react_ts_website is not None:
            self._values["cloudscape_react_ts_website"] = cloudscape_react_ts_website
        if cloudscape_react_ts_websites is not None:
            self._values["cloudscape_react_ts_websites"] = cloudscape_react_ts_websites
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if stages is not None:
            self._values["stages"] = stages
        if type_safe_api is not None:
            self._values["type_safe_api"] = type_safe_api
        if type_safe_apis is not None:
            self._values["type_safe_apis"] = type_safe_apis

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
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A command to execute before synthesis.

        This command will be called when
        running ``cdk synth`` or when ``cdk watch`` identifies a change in your source
        code before redeployment.

        :default: - no build command

        :stability: experimental
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_assert(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Warning: NodeJS only.

        Install the

        :default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0

        :deprecated: The

        :stability: deprecated
        :aws-cdk: /assertions (in V1) and included in ``aws-cdk-lib`` for V2.
        '''
        result = self._values.get("cdk_assert")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_assertions(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install the assertions library?

        Only needed for CDK 1.x. If using CDK 2.x then
        assertions is already included in 'aws-cdk-lib'

        :default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0

        :stability: experimental
        '''
        result = self._values.get("cdk_assertions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Which AWS CDKv1 modules this project requires.

        :deprecated: For CDK 2.x use "deps" instead. (or "peerDeps" if you're building a library)

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_dependencies_as_deps(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``).

        This is to ensure that downstream consumers actually have your CDK dependencies installed
        when using npm < 7 or yarn, where peer dependencies are not automatically installed.
        If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure
        they are present during development.

        Note: this setting only applies to construct library projects

        :default: true

        :deprecated: Not supported in CDK v2.

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies_as_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdkout(self) -> typing.Optional[builtins.str]:
        '''(experimental) cdk.out directory.

        :default: "cdk.out"

        :stability: experimental
        '''
        result = self._values.get("cdkout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_test_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) AWS CDK modules required for testing.

        :deprecated: For CDK 2.x use 'devDeps' (in node.js projects) or 'testDeps' (in java projects) instead

        :stability: deprecated
        '''
        result = self._values.get("cdk_test_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the AWS CDK to depend on.

        :default: "2.1.0"

        :stability: experimental
        '''
        result = self._values.get("cdk_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_version_pinning(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use pinned version instead of caret version for CDK.

        You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates.
        If you use experimental features this will let you define the moment you include breaking changes.

        :stability: experimental
        '''
        result = self._values.get("cdk_version_pinning")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def constructs_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the ``constructs`` library to depend on.

        :default:

        - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is
        "10.0.5".

        :stability: experimental
        '''
        result = self._values.get("constructs_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional context to include in ``cdk.json``.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

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
    def feature_flags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include all feature flags in cdk.json.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("feature_flags")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def require_approval(
        self,
    ) -> typing.Optional[_projen_awscdk_04054675.ApprovalLevel]:
        '''(experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them.

        :default: ApprovalLevel.BROADENING

        :stability: experimental
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[_projen_awscdk_04054675.ApprovalLevel], result)

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
    def watch_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to exclude from ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def watch_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to include in ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_signup(self) -> typing.Optional[builtins.bool]:
        '''Allow self sign up for the UserIdentity construct.

        :default: - false
        '''
        result = self._values.get("allow_signup")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cloudscape_react_ts_website(
        self,
    ) -> typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f]:
        '''(deprecated) CloudscapeReactTsWebsiteProject instance to use when setting up the initial project sample code.

        :deprecated: use cloudscapeReactTsWebsites

        :stability: deprecated
        '''
        result = self._values.get("cloudscape_react_ts_website")
        return typing.cast(typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f], result)

    @builtins.property
    def cloudscape_react_ts_websites(
        self,
    ) -> typing.Optional[typing.List[_CloudscapeReactTsWebsiteProject_ef2bfd2f]]:
        '''CloudscapeReactTsWebsiteProject instances to use when setting up the initial project sample code.'''
        result = self._values.get("cloudscape_react_ts_websites")
        return typing.cast(typing.Optional[typing.List[_CloudscapeReactTsWebsiteProject_ef2bfd2f]], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Stack name.

        :default: infra-dev
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stages(self) -> typing.Optional[typing.List[DeploymentStage]]:
        '''List of deployment stages.'''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.List[DeploymentStage]], result)

    @builtins.property
    def type_safe_api(self) -> typing.Optional[_TypeSafeApiProject_b9e4f1cf]:
        '''(deprecated) TypeSafeApi instance to use when setting up the initial project sample code.

        :deprecated: use typeSafeApis

        :stability: deprecated
        '''
        result = self._values.get("type_safe_api")
        return typing.cast(typing.Optional[_TypeSafeApiProject_b9e4f1cf], result)

    @builtins.property
    def type_safe_apis(
        self,
    ) -> typing.Optional[typing.List[_TypeSafeApiProject_b9e4f1cf]]:
        '''TypeSafeApi instances to use when setting up the initial project sample code.'''
        result = self._values.get("type_safe_apis")
        return typing.cast(typing.Optional[typing.List[_TypeSafeApiProject_b9e4f1cf]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfrastructureJavaProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InfrastructurePyProject(
    _projen_awscdk_04054675.AwsCdkPythonApp,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.infrastructure.InfrastructurePyProject",
):
    '''Synthesizes a Infrastructure Python Project.'''

    def __init__(
        self,
        *,
        allow_signup: typing.Optional[builtins.bool] = None,
        cloudscape_react_ts_website: typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f] = None,
        cloudscape_react_ts_websites: typing.Optional[typing.Sequence[_CloudscapeReactTsWebsiteProject_ef2bfd2f]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[typing.Union[DeploymentStage, typing.Dict[builtins.str, typing.Any]]]] = None,
        type_safe_api: typing.Optional[_TypeSafeApiProject_b9e4f1cf] = None,
        type_safe_apis: typing.Optional[typing.Sequence[_TypeSafeApiProject_b9e4f1cf]] = None,
        name: builtins.str,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_command: typing.Optional[builtins.str] = None,
        cdk_assert: typing.Optional[builtins.bool] = None,
        cdk_assertions: typing.Optional[builtins.bool] = None,
        cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
        cdkout: typing.Optional[builtins.str] = None,
        cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_version: typing.Optional[builtins.str] = None,
        cdk_version_pinning: typing.Optional[builtins.bool] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        constructs_version: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        feature_flags: typing.Optional[builtins.bool] = None,
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
        module_name: typing.Optional[builtins.str] = None,
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
        require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
        sample: typing.Optional[builtins.bool] = None,
        setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        setuptools: typing.Optional[builtins.bool] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        testdir: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
        watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_signup: Allow self sign up for the UserIdentity construct. Default: - false
        :param cloudscape_react_ts_website: (deprecated) CloudscapeReactTsWebsiteProject instance to use when setting up the initial project sample code.
        :param cloudscape_react_ts_websites: CloudscapeReactTsWebsiteProject instances to use when setting up the initial project sample code.
        :param stack_name: Stack name. Default: infra-dev
        :param stages: List of deployment stages.
        :param type_safe_api: (deprecated) TypeSafeApi instance to use when setting up the initial project sample code.
        :param type_safe_apis: TypeSafeApi instances to use when setting up the initial project sample code.
        :param name: Default: $BASEDIR
        :param author_email: (experimental) Author's e-mail. Default: $GIT_USER_EMAIL
        :param author_name: (experimental) Author's name. Default: $GIT_USER_NAME
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param build_command: (experimental) A command to execute before synthesis. This command will be called when running ``cdk synth`` or when ``cdk watch`` identifies a change in your source code before redeployment. Default: - no build command
        :param cdk_assert: (deprecated) Warning: NodeJS only. Install the Default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0
        :param cdk_assertions: (experimental) Install the assertions library? Only needed for CDK 1.x. If using CDK 2.x then assertions is already included in 'aws-cdk-lib' Default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0
        :param cdk_dependencies: (deprecated) Which AWS CDKv1 modules this project requires.
        :param cdk_dependencies_as_deps: (deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``). This is to ensure that downstream consumers actually have your CDK dependencies installed when using npm < 7 or yarn, where peer dependencies are not automatically installed. If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure they are present during development. Note: this setting only applies to construct library projects Default: true
        :param cdkout: (experimental) cdk.out directory. Default: "cdk.out"
        :param cdk_test_dependencies: (deprecated) AWS CDK modules required for testing.
        :param cdk_version: (experimental) Minimum version of the AWS CDK to depend on. Default: "2.1.0"
        :param cdk_version_pinning: (experimental) Use pinned version instead of caret version for CDK. You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates. If you use experimental features this will let you define the moment you include breaking changes.
        :param classifiers: (experimental) A list of PyPI trove classifiers that describe the project.
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param constructs_version: (experimental) Minimum version of the ``constructs`` library to depend on. Default: - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is "10.0.5".
        :param context: (experimental) Additional context to include in ``cdk.json``. Default: - no additional context
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) A short description of the package.
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param dev_deps: (experimental) List of dev dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDevDependency()``. Default: []
        :param feature_flags: (experimental) Include all feature flags in cdk.json. Default: true
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
        :param module_name: (experimental) Name of the python package as used in imports and filenames. Must only consist of alphanumeric characters and underscores. Default: $PYTHON_MODULE_NAME
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
        :param require_approval: (experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them. Default: ApprovalLevel.BROADENING
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param setup_config: (experimental) Additional fields to pass in the setup() function if using setuptools.
        :param setuptools: (experimental) Use setuptools with a setup.py script for packaging and publishing. Default: - true, unless poetry is true, then false
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param testdir: (experimental) Python sources directory. Default: "tests"
        :param version: (experimental) Version of the package. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param watch_excludes: (experimental) Glob patterns to exclude from ``cdk watch``. Default: []
        :param watch_includes: (experimental) Glob patterns to include in ``cdk watch``. Default: []
        '''
        options = InfrastructurePyProjectOptions(
            allow_signup=allow_signup,
            cloudscape_react_ts_website=cloudscape_react_ts_website,
            cloudscape_react_ts_websites=cloudscape_react_ts_websites,
            stack_name=stack_name,
            stages=stages,
            type_safe_api=type_safe_api,
            type_safe_apis=type_safe_apis,
            name=name,
            author_email=author_email,
            author_name=author_name,
            auto_approve_options=auto_approve_options,
            auto_merge=auto_merge,
            auto_merge_options=auto_merge_options,
            build_command=build_command,
            cdk_assert=cdk_assert,
            cdk_assertions=cdk_assertions,
            cdk_dependencies=cdk_dependencies,
            cdk_dependencies_as_deps=cdk_dependencies_as_deps,
            cdkout=cdkout,
            cdk_test_dependencies=cdk_test_dependencies,
            cdk_version=cdk_version,
            cdk_version_pinning=cdk_version_pinning,
            classifiers=classifiers,
            clobber=clobber,
            commit_generated=commit_generated,
            constructs_version=constructs_version,
            context=context,
            deps=deps,
            description=description,
            dev_container=dev_container,
            dev_deps=dev_deps,
            feature_flags=feature_flags,
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
            module_name=module_name,
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
            require_approval=require_approval,
            sample=sample,
            setup_config=setup_config,
            setuptools=setuptools,
            stale=stale,
            stale_options=stale_options,
            testdir=testdir,
            version=version,
            vscode=vscode,
            watch_excludes=watch_excludes,
            watch_includes=watch_includes,
        )

        jsii.create(self.__class__, self, [options])


@jsii.data_type(
    jsii_type="@aws/pdk.infrastructure.InfrastructurePyProjectOptions",
    jsii_struct_bases=[AwsCdkPythonAppOptions],
    name_mapping={
        "name": "name",
        "author_email": "authorEmail",
        "author_name": "authorName",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "build_command": "buildCommand",
        "cdk_assert": "cdkAssert",
        "cdk_assertions": "cdkAssertions",
        "cdk_dependencies": "cdkDependencies",
        "cdk_dependencies_as_deps": "cdkDependenciesAsDeps",
        "cdkout": "cdkout",
        "cdk_test_dependencies": "cdkTestDependencies",
        "cdk_version": "cdkVersion",
        "cdk_version_pinning": "cdkVersionPinning",
        "classifiers": "classifiers",
        "clobber": "clobber",
        "commit_generated": "commitGenerated",
        "constructs_version": "constructsVersion",
        "context": "context",
        "deps": "deps",
        "description": "description",
        "dev_container": "devContainer",
        "dev_deps": "devDeps",
        "feature_flags": "featureFlags",
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
        "module_name": "moduleName",
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
        "require_approval": "requireApproval",
        "sample": "sample",
        "setup_config": "setupConfig",
        "setuptools": "setuptools",
        "stale": "stale",
        "stale_options": "staleOptions",
        "testdir": "testdir",
        "version": "version",
        "vscode": "vscode",
        "watch_excludes": "watchExcludes",
        "watch_includes": "watchIncludes",
        "allow_signup": "allowSignup",
        "cloudscape_react_ts_website": "cloudscapeReactTsWebsite",
        "cloudscape_react_ts_websites": "cloudscapeReactTsWebsites",
        "stack_name": "stackName",
        "stages": "stages",
        "type_safe_api": "typeSafeApi",
        "type_safe_apis": "typeSafeApis",
    },
)
class InfrastructurePyProjectOptions(AwsCdkPythonAppOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_command: typing.Optional[builtins.str] = None,
        cdk_assert: typing.Optional[builtins.bool] = None,
        cdk_assertions: typing.Optional[builtins.bool] = None,
        cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
        cdkout: typing.Optional[builtins.str] = None,
        cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_version: typing.Optional[builtins.str] = None,
        cdk_version_pinning: typing.Optional[builtins.bool] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        constructs_version: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        feature_flags: typing.Optional[builtins.bool] = None,
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
        module_name: typing.Optional[builtins.str] = None,
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
        require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
        sample: typing.Optional[builtins.bool] = None,
        setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        setuptools: typing.Optional[builtins.bool] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        testdir: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vscode: typing.Optional[builtins.bool] = None,
        watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_signup: typing.Optional[builtins.bool] = None,
        cloudscape_react_ts_website: typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f] = None,
        cloudscape_react_ts_websites: typing.Optional[typing.Sequence[_CloudscapeReactTsWebsiteProject_ef2bfd2f]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[typing.Union[DeploymentStage, typing.Dict[builtins.str, typing.Any]]]] = None,
        type_safe_api: typing.Optional[_TypeSafeApiProject_b9e4f1cf] = None,
        type_safe_apis: typing.Optional[typing.Sequence[_TypeSafeApiProject_b9e4f1cf]] = None,
    ) -> None:
        '''Configuration options for the InfrastructurePyProject.

        :param name: Default: $BASEDIR
        :param author_email: (experimental) Author's e-mail. Default: $GIT_USER_EMAIL
        :param author_name: (experimental) Author's name. Default: $GIT_USER_NAME
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param build_command: (experimental) A command to execute before synthesis. This command will be called when running ``cdk synth`` or when ``cdk watch`` identifies a change in your source code before redeployment. Default: - no build command
        :param cdk_assert: (deprecated) Warning: NodeJS only. Install the Default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0
        :param cdk_assertions: (experimental) Install the assertions library? Only needed for CDK 1.x. If using CDK 2.x then assertions is already included in 'aws-cdk-lib' Default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0
        :param cdk_dependencies: (deprecated) Which AWS CDKv1 modules this project requires.
        :param cdk_dependencies_as_deps: (deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``). This is to ensure that downstream consumers actually have your CDK dependencies installed when using npm < 7 or yarn, where peer dependencies are not automatically installed. If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure they are present during development. Note: this setting only applies to construct library projects Default: true
        :param cdkout: (experimental) cdk.out directory. Default: "cdk.out"
        :param cdk_test_dependencies: (deprecated) AWS CDK modules required for testing.
        :param cdk_version: (experimental) Minimum version of the AWS CDK to depend on. Default: "2.1.0"
        :param cdk_version_pinning: (experimental) Use pinned version instead of caret version for CDK. You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates. If you use experimental features this will let you define the moment you include breaking changes.
        :param classifiers: (experimental) A list of PyPI trove classifiers that describe the project.
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param constructs_version: (experimental) Minimum version of the ``constructs`` library to depend on. Default: - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is "10.0.5".
        :param context: (experimental) Additional context to include in ``cdk.json``. Default: - no additional context
        :param deps: (experimental) List of runtime dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDependency()``. Default: []
        :param description: (experimental) A short description of the package.
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param dev_deps: (experimental) List of dev dependencies for this project. Dependencies use the format: ``<module>@<semver>``. Additional dependencies can be added via ``project.addDevDependency()``. Default: []
        :param feature_flags: (experimental) Include all feature flags in cdk.json. Default: true
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
        :param module_name: (experimental) Name of the python package as used in imports and filenames. Must only consist of alphanumeric characters and underscores. Default: $PYTHON_MODULE_NAME
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
        :param require_approval: (experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them. Default: ApprovalLevel.BROADENING
        :param sample: (experimental) Include sample code and test if the relevant directories don't exist. Default: true
        :param setup_config: (experimental) Additional fields to pass in the setup() function if using setuptools.
        :param setuptools: (experimental) Use setuptools with a setup.py script for packaging and publishing. Default: - true, unless poetry is true, then false
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param testdir: (experimental) Python sources directory. Default: "tests"
        :param version: (experimental) Version of the package. Default: "0.1.0"
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param watch_excludes: (experimental) Glob patterns to exclude from ``cdk watch``. Default: []
        :param watch_includes: (experimental) Glob patterns to include in ``cdk watch``. Default: []
        :param allow_signup: Allow self sign up for the UserIdentity construct. Default: - false
        :param cloudscape_react_ts_website: (deprecated) CloudscapeReactTsWebsiteProject instance to use when setting up the initial project sample code.
        :param cloudscape_react_ts_websites: CloudscapeReactTsWebsiteProject instances to use when setting up the initial project sample code.
        :param stack_name: Stack name. Default: infra-dev
        :param stages: List of deployment stages.
        :param type_safe_api: (deprecated) TypeSafeApi instance to use when setting up the initial project sample code.
        :param type_safe_apis: TypeSafeApi instances to use when setting up the initial project sample code.
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
            type_hints = typing.get_type_hints(_typecheckingstub__f976053715e4d3f0f05e190a57600d1bd7dd400a75f2f380efb578428967fda7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument cdk_assert", value=cdk_assert, expected_type=type_hints["cdk_assert"])
            check_type(argname="argument cdk_assertions", value=cdk_assertions, expected_type=type_hints["cdk_assertions"])
            check_type(argname="argument cdk_dependencies", value=cdk_dependencies, expected_type=type_hints["cdk_dependencies"])
            check_type(argname="argument cdk_dependencies_as_deps", value=cdk_dependencies_as_deps, expected_type=type_hints["cdk_dependencies_as_deps"])
            check_type(argname="argument cdkout", value=cdkout, expected_type=type_hints["cdkout"])
            check_type(argname="argument cdk_test_dependencies", value=cdk_test_dependencies, expected_type=type_hints["cdk_test_dependencies"])
            check_type(argname="argument cdk_version", value=cdk_version, expected_type=type_hints["cdk_version"])
            check_type(argname="argument cdk_version_pinning", value=cdk_version_pinning, expected_type=type_hints["cdk_version_pinning"])
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument constructs_version", value=constructs_version, expected_type=type_hints["constructs_version"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument feature_flags", value=feature_flags, expected_type=type_hints["feature_flags"])
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
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
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
            check_type(argname="argument require_approval", value=require_approval, expected_type=type_hints["require_approval"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument setup_config", value=setup_config, expected_type=type_hints["setup_config"])
            check_type(argname="argument setuptools", value=setuptools, expected_type=type_hints["setuptools"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument testdir", value=testdir, expected_type=type_hints["testdir"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument watch_excludes", value=watch_excludes, expected_type=type_hints["watch_excludes"])
            check_type(argname="argument watch_includes", value=watch_includes, expected_type=type_hints["watch_includes"])
            check_type(argname="argument allow_signup", value=allow_signup, expected_type=type_hints["allow_signup"])
            check_type(argname="argument cloudscape_react_ts_website", value=cloudscape_react_ts_website, expected_type=type_hints["cloudscape_react_ts_website"])
            check_type(argname="argument cloudscape_react_ts_websites", value=cloudscape_react_ts_websites, expected_type=type_hints["cloudscape_react_ts_websites"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
            check_type(argname="argument type_safe_api", value=type_safe_api, expected_type=type_hints["type_safe_api"])
            check_type(argname="argument type_safe_apis", value=type_safe_apis, expected_type=type_hints["type_safe_apis"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if build_command is not None:
            self._values["build_command"] = build_command
        if cdk_assert is not None:
            self._values["cdk_assert"] = cdk_assert
        if cdk_assertions is not None:
            self._values["cdk_assertions"] = cdk_assertions
        if cdk_dependencies is not None:
            self._values["cdk_dependencies"] = cdk_dependencies
        if cdk_dependencies_as_deps is not None:
            self._values["cdk_dependencies_as_deps"] = cdk_dependencies_as_deps
        if cdkout is not None:
            self._values["cdkout"] = cdkout
        if cdk_test_dependencies is not None:
            self._values["cdk_test_dependencies"] = cdk_test_dependencies
        if cdk_version is not None:
            self._values["cdk_version"] = cdk_version
        if cdk_version_pinning is not None:
            self._values["cdk_version_pinning"] = cdk_version_pinning
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if clobber is not None:
            self._values["clobber"] = clobber
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if constructs_version is not None:
            self._values["constructs_version"] = constructs_version
        if context is not None:
            self._values["context"] = context
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if feature_flags is not None:
            self._values["feature_flags"] = feature_flags
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
        if module_name is not None:
            self._values["module_name"] = module_name
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
        if require_approval is not None:
            self._values["require_approval"] = require_approval
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
        if testdir is not None:
            self._values["testdir"] = testdir
        if version is not None:
            self._values["version"] = version
        if vscode is not None:
            self._values["vscode"] = vscode
        if watch_excludes is not None:
            self._values["watch_excludes"] = watch_excludes
        if watch_includes is not None:
            self._values["watch_includes"] = watch_includes
        if allow_signup is not None:
            self._values["allow_signup"] = allow_signup
        if cloudscape_react_ts_website is not None:
            self._values["cloudscape_react_ts_website"] = cloudscape_react_ts_website
        if cloudscape_react_ts_websites is not None:
            self._values["cloudscape_react_ts_websites"] = cloudscape_react_ts_websites
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if stages is not None:
            self._values["stages"] = stages
        if type_safe_api is not None:
            self._values["type_safe_api"] = type_safe_api
        if type_safe_apis is not None:
            self._values["type_safe_apis"] = type_safe_apis

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
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A command to execute before synthesis.

        This command will be called when
        running ``cdk synth`` or when ``cdk watch`` identifies a change in your source
        code before redeployment.

        :default: - no build command

        :stability: experimental
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_assert(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Warning: NodeJS only.

        Install the

        :default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0

        :deprecated: The

        :stability: deprecated
        :aws-cdk: /assertions (in V1) and included in ``aws-cdk-lib`` for V2.
        '''
        result = self._values.get("cdk_assert")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_assertions(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install the assertions library?

        Only needed for CDK 1.x. If using CDK 2.x then
        assertions is already included in 'aws-cdk-lib'

        :default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0

        :stability: experimental
        '''
        result = self._values.get("cdk_assertions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Which AWS CDKv1 modules this project requires.

        :deprecated: For CDK 2.x use "deps" instead. (or "peerDeps" if you're building a library)

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_dependencies_as_deps(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``).

        This is to ensure that downstream consumers actually have your CDK dependencies installed
        when using npm < 7 or yarn, where peer dependencies are not automatically installed.
        If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure
        they are present during development.

        Note: this setting only applies to construct library projects

        :default: true

        :deprecated: Not supported in CDK v2.

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies_as_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdkout(self) -> typing.Optional[builtins.str]:
        '''(experimental) cdk.out directory.

        :default: "cdk.out"

        :stability: experimental
        '''
        result = self._values.get("cdkout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_test_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) AWS CDK modules required for testing.

        :deprecated: For CDK 2.x use 'devDeps' (in node.js projects) or 'testDeps' (in java projects) instead

        :stability: deprecated
        '''
        result = self._values.get("cdk_test_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the AWS CDK to depend on.

        :default: "2.1.0"

        :stability: experimental
        '''
        result = self._values.get("cdk_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_version_pinning(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use pinned version instead of caret version for CDK.

        You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates.
        If you use experimental features this will let you define the moment you include breaking changes.

        :stability: experimental
        '''
        result = self._values.get("cdk_version_pinning")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def constructs_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the ``constructs`` library to depend on.

        :default:

        - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is
        "10.0.5".

        :stability: experimental
        '''
        result = self._values.get("constructs_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional context to include in ``cdk.json``.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

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
    def feature_flags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include all feature flags in cdk.json.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("feature_flags")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def module_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the python package as used in imports and filenames.

        Must only consist of alphanumeric characters and underscores.

        :default: $PYTHON_MODULE_NAME

        :stability: experimental
        '''
        result = self._values.get("module_name")
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
    def require_approval(
        self,
    ) -> typing.Optional[_projen_awscdk_04054675.ApprovalLevel]:
        '''(experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them.

        :default: ApprovalLevel.BROADENING

        :stability: experimental
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[_projen_awscdk_04054675.ApprovalLevel], result)

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
    def testdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Python sources directory.

        :default: "tests"

        :stability: experimental
        '''
        result = self._values.get("testdir")
        return typing.cast(typing.Optional[builtins.str], result)

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
    def watch_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to exclude from ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def watch_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to include in ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_signup(self) -> typing.Optional[builtins.bool]:
        '''Allow self sign up for the UserIdentity construct.

        :default: - false
        '''
        result = self._values.get("allow_signup")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cloudscape_react_ts_website(
        self,
    ) -> typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f]:
        '''(deprecated) CloudscapeReactTsWebsiteProject instance to use when setting up the initial project sample code.

        :deprecated: use cloudscapeReactTsWebsites

        :stability: deprecated
        '''
        result = self._values.get("cloudscape_react_ts_website")
        return typing.cast(typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f], result)

    @builtins.property
    def cloudscape_react_ts_websites(
        self,
    ) -> typing.Optional[typing.List[_CloudscapeReactTsWebsiteProject_ef2bfd2f]]:
        '''CloudscapeReactTsWebsiteProject instances to use when setting up the initial project sample code.'''
        result = self._values.get("cloudscape_react_ts_websites")
        return typing.cast(typing.Optional[typing.List[_CloudscapeReactTsWebsiteProject_ef2bfd2f]], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Stack name.

        :default: infra-dev
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stages(self) -> typing.Optional[typing.List[DeploymentStage]]:
        '''List of deployment stages.'''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.List[DeploymentStage]], result)

    @builtins.property
    def type_safe_api(self) -> typing.Optional[_TypeSafeApiProject_b9e4f1cf]:
        '''(deprecated) TypeSafeApi instance to use when setting up the initial project sample code.

        :deprecated: use typeSafeApis

        :stability: deprecated
        '''
        result = self._values.get("type_safe_api")
        return typing.cast(typing.Optional[_TypeSafeApiProject_b9e4f1cf], result)

    @builtins.property
    def type_safe_apis(
        self,
    ) -> typing.Optional[typing.List[_TypeSafeApiProject_b9e4f1cf]]:
        '''TypeSafeApi instances to use when setting up the initial project sample code.'''
        result = self._values.get("type_safe_apis")
        return typing.cast(typing.Optional[typing.List[_TypeSafeApiProject_b9e4f1cf]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfrastructurePyProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InfrastructureTsProject(
    _projen_awscdk_04054675.AwsCdkTypeScriptApp,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.infrastructure.InfrastructureTsProject",
):
    '''Synthesizes a Infrastructure Typescript Project.'''

    def __init__(
        self,
        *,
        allow_signup: typing.Optional[builtins.bool] = None,
        cloudscape_react_ts_website: typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f] = None,
        cloudscape_react_ts_websites: typing.Optional[typing.Sequence[_CloudscapeReactTsWebsiteProject_ef2bfd2f]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[typing.Union[DeploymentStage, typing.Dict[builtins.str, typing.Any]]]] = None,
        type_safe_api: typing.Optional[_TypeSafeApiProject_b9e4f1cf] = None,
        type_safe_apis: typing.Optional[typing.Sequence[_TypeSafeApiProject_b9e4f1cf]] = None,
        type_safe_web_socket_apis: typing.Optional[typing.Sequence[_TypeSafeWebSocketApiProject_59b62fd2]] = None,
        name: builtins.str,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        app_entrypoint: typing.Optional[builtins.str] = None,
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
        build_command: typing.Optional[builtins.str] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cdk_assert: typing.Optional[builtins.bool] = None,
        cdk_assertions: typing.Optional[builtins.bool] = None,
        cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
        cdkout: typing.Optional[builtins.str] = None,
        cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_version: typing.Optional[builtins.str] = None,
        cdk_version_pinning: typing.Optional[builtins.bool] = None,
        check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        constructs_version: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
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
        edge_lambda_auto_discover: typing.Optional[builtins.bool] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        entrypoint_types: typing.Optional[builtins.str] = None,
        eslint: typing.Optional[builtins.bool] = None,
        eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        experimental_integ_runner: typing.Optional[builtins.bool] = None,
        feature_flags: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        integration_test_auto_discover: typing.Optional[builtins.bool] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_auto_discover: typing.Optional[builtins.bool] = None,
        lambda_extension_auto_discover: typing.Optional[builtins.bool] = None,
        lambda_options: typing.Optional[typing.Union[_projen_awscdk_04054675.LambdaFunctionCommonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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
        require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
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
        watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        :param allow_signup: Allow self sign up for the UserIdentity construct. Default: - false
        :param cloudscape_react_ts_website: (deprecated) CloudscapeReactTsWebsiteProject instance to use when setting up the initial project sample code.
        :param cloudscape_react_ts_websites: CloudscapeReactTsWebsiteProject instances to use when setting up the initial project sample code.
        :param stack_name: Stack name. Default: infra-dev
        :param stages: List of deployment stages.
        :param type_safe_api: (deprecated) TypeSafeApi instance to use when setting up the initial project sample code.
        :param type_safe_apis: TypeSafeApi instances to use when setting up the initial project sample code.
        :param type_safe_web_socket_apis: TypeSafeWebSocketApi instances to use when setting up the initial project sample code.
        :param name: Default: $BASEDIR
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param app_entrypoint: (experimental) The CDK app's entrypoint (relative to the source directory, which is "src" by default). Default: "main.ts"
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
        :param build_command: (experimental) A command to execute before synthesis. This command will be called when running ``cdk synth`` or when ``cdk watch`` identifies a change in your source code before redeployment. Default: - no build command
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_options: (experimental) Options for PR build workflow.
        :param build_workflow_triggers: (deprecated) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param cdk_assert: (deprecated) Warning: NodeJS only. Install the Default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0
        :param cdk_assertions: (experimental) Install the assertions library? Only needed for CDK 1.x. If using CDK 2.x then assertions is already included in 'aws-cdk-lib' Default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0
        :param cdk_dependencies: (deprecated) Which AWS CDKv1 modules this project requires.
        :param cdk_dependencies_as_deps: (deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``). This is to ensure that downstream consumers actually have your CDK dependencies installed when using npm < 7 or yarn, where peer dependencies are not automatically installed. If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure they are present during development. Note: this setting only applies to construct library projects Default: true
        :param cdkout: (experimental) cdk.out directory. Default: "cdk.out"
        :param cdk_test_dependencies: (deprecated) AWS CDK modules required for testing.
        :param cdk_version: (experimental) Minimum version of the AWS CDK to depend on. Default: "2.1.0"
        :param cdk_version_pinning: (experimental) Use pinned version instead of caret version for CDK. You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates. If you use experimental features this will let you define the moment you include breaking changes.
        :param check_licenses: (experimental) Configure which licenses should be deemed acceptable for use by dependencies. This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered. Default: - no license checks are run during the build and all licenses will be accepted
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v4 A secret is required for private repos. Configured with ``@codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories. Default: - if this option is not specified, only public repositories are supported
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param constructs_version: (experimental) Minimum version of the ``constructs`` library to depend on. Default: - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is "10.0.5".
        :param context: (experimental) Additional context to include in ``cdk.json``. Default: - no additional context
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
        :param edge_lambda_auto_discover: (experimental) Automatically adds an ``cloudfront.experimental.EdgeFunction`` for each ``.edge-lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project. Default: true
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json. Default: "lib/index.js"
        :param entrypoint_types: (experimental) The .d.ts file that includes the type declarations for this module. Default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)
        :param eslint: (experimental) Setup eslint. Default: true
        :param eslint_options: (experimental) Eslint options. Default: - opinionated default options
        :param experimental_integ_runner: (experimental) Enable experimental support for the AWS CDK integ-runner. Default: false
        :param feature_flags: (experimental) Include all feature flags in cdk.json. Default: true
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param homepage: (experimental) Package's Homepage / Website.
        :param integration_test_auto_discover: (experimental) Automatically discovers and creates integration tests for each ``.integ.ts`` file in under your test directory. Default: true
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param lambda_auto_discover: (experimental) Automatically adds an ``awscdk.LambdaFunction`` for each ``.lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project. Default: true
        :param lambda_extension_auto_discover: (experimental) Automatically adds an ``awscdk.LambdaExtension`` for each ``.lambda-extension.ts`` entrypoint in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project. Default: true
        :param lambda_options: (experimental) Common options for all AWS Lambda functions. Default: - default options
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
        :param require_approval: (experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them. Default: ApprovalLevel.BROADENING
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
        :param watch_excludes: (experimental) Glob patterns to exclude from ``cdk watch``. Default: []
        :param watch_includes: (experimental) Glob patterns to include in ``cdk watch``. Default: []
        :param workflow_bootstrap_steps: (experimental) Workflow steps to use in order to bootstrap this repo. Default: "yarn install --frozen-lockfile && yarn projen"
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_git_identity: (experimental) The git identity to use in workflows. Default: - GitHub Actions
        :param workflow_node_version: (experimental) The node version to use in GitHub workflows. Default: - same as ``minNodeVersion``
        :param workflow_package_cache: (experimental) Enable Node.js package cache in GitHub workflows. Default: false
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param yarn_berry_options: (experimental) Options for Yarn Berry. Default: - Yarn Berry v4 with all default options
        '''
        options = InfrastructureTsProjectOptions(
            allow_signup=allow_signup,
            cloudscape_react_ts_website=cloudscape_react_ts_website,
            cloudscape_react_ts_websites=cloudscape_react_ts_websites,
            stack_name=stack_name,
            stages=stages,
            type_safe_api=type_safe_api,
            type_safe_apis=type_safe_apis,
            type_safe_web_socket_apis=type_safe_web_socket_apis,
            name=name,
            allow_library_dependencies=allow_library_dependencies,
            app_entrypoint=app_entrypoint,
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
            build_command=build_command,
            build_workflow=build_workflow,
            build_workflow_options=build_workflow_options,
            build_workflow_triggers=build_workflow_triggers,
            bundled_deps=bundled_deps,
            bundler_options=bundler_options,
            cdk_assert=cdk_assert,
            cdk_assertions=cdk_assertions,
            cdk_dependencies=cdk_dependencies,
            cdk_dependencies_as_deps=cdk_dependencies_as_deps,
            cdkout=cdkout,
            cdk_test_dependencies=cdk_test_dependencies,
            cdk_version=cdk_version,
            cdk_version_pinning=cdk_version_pinning,
            check_licenses=check_licenses,
            clobber=clobber,
            code_artifact_options=code_artifact_options,
            code_cov=code_cov,
            code_cov_token_secret=code_cov_token_secret,
            commit_generated=commit_generated,
            constructs_version=constructs_version,
            context=context,
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
            edge_lambda_auto_discover=edge_lambda_auto_discover,
            entrypoint=entrypoint,
            entrypoint_types=entrypoint_types,
            eslint=eslint,
            eslint_options=eslint_options,
            experimental_integ_runner=experimental_integ_runner,
            feature_flags=feature_flags,
            github=github,
            github_options=github_options,
            gitignore=gitignore,
            git_ignore_options=git_ignore_options,
            git_options=git_options,
            gitpod=gitpod,
            homepage=homepage,
            integration_test_auto_discover=integration_test_auto_discover,
            jest=jest,
            jest_options=jest_options,
            jsii_release_version=jsii_release_version,
            keywords=keywords,
            lambda_auto_discover=lambda_auto_discover,
            lambda_extension_auto_discover=lambda_extension_auto_discover,
            lambda_options=lambda_options,
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
            require_approval=require_approval,
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
            watch_excludes=watch_excludes,
            watch_includes=watch_includes,
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


@jsii.data_type(
    jsii_type="@aws/pdk.infrastructure.InfrastructureTsProjectOptions",
    jsii_struct_bases=[AwsCdkTypeScriptAppOptions],
    name_mapping={
        "name": "name",
        "allow_library_dependencies": "allowLibraryDependencies",
        "app_entrypoint": "appEntrypoint",
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
        "build_command": "buildCommand",
        "build_workflow": "buildWorkflow",
        "build_workflow_options": "buildWorkflowOptions",
        "build_workflow_triggers": "buildWorkflowTriggers",
        "bundled_deps": "bundledDeps",
        "bundler_options": "bundlerOptions",
        "cdk_assert": "cdkAssert",
        "cdk_assertions": "cdkAssertions",
        "cdk_dependencies": "cdkDependencies",
        "cdk_dependencies_as_deps": "cdkDependenciesAsDeps",
        "cdkout": "cdkout",
        "cdk_test_dependencies": "cdkTestDependencies",
        "cdk_version": "cdkVersion",
        "cdk_version_pinning": "cdkVersionPinning",
        "check_licenses": "checkLicenses",
        "clobber": "clobber",
        "code_artifact_options": "codeArtifactOptions",
        "code_cov": "codeCov",
        "code_cov_token_secret": "codeCovTokenSecret",
        "commit_generated": "commitGenerated",
        "constructs_version": "constructsVersion",
        "context": "context",
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
        "edge_lambda_auto_discover": "edgeLambdaAutoDiscover",
        "entrypoint": "entrypoint",
        "entrypoint_types": "entrypointTypes",
        "eslint": "eslint",
        "eslint_options": "eslintOptions",
        "experimental_integ_runner": "experimentalIntegRunner",
        "feature_flags": "featureFlags",
        "github": "github",
        "github_options": "githubOptions",
        "gitignore": "gitignore",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "gitpod": "gitpod",
        "homepage": "homepage",
        "integration_test_auto_discover": "integrationTestAutoDiscover",
        "jest": "jest",
        "jest_options": "jestOptions",
        "jsii_release_version": "jsiiReleaseVersion",
        "keywords": "keywords",
        "lambda_auto_discover": "lambdaAutoDiscover",
        "lambda_extension_auto_discover": "lambdaExtensionAutoDiscover",
        "lambda_options": "lambdaOptions",
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
        "require_approval": "requireApproval",
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
        "watch_excludes": "watchExcludes",
        "watch_includes": "watchIncludes",
        "workflow_bootstrap_steps": "workflowBootstrapSteps",
        "workflow_container_image": "workflowContainerImage",
        "workflow_git_identity": "workflowGitIdentity",
        "workflow_node_version": "workflowNodeVersion",
        "workflow_package_cache": "workflowPackageCache",
        "workflow_runs_on": "workflowRunsOn",
        "workflow_runs_on_group": "workflowRunsOnGroup",
        "yarn_berry_options": "yarnBerryOptions",
        "allow_signup": "allowSignup",
        "cloudscape_react_ts_website": "cloudscapeReactTsWebsite",
        "cloudscape_react_ts_websites": "cloudscapeReactTsWebsites",
        "stack_name": "stackName",
        "stages": "stages",
        "type_safe_api": "typeSafeApi",
        "type_safe_apis": "typeSafeApis",
        "type_safe_web_socket_apis": "typeSafeWebSocketApis",
    },
)
class InfrastructureTsProjectOptions(AwsCdkTypeScriptAppOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        app_entrypoint: typing.Optional[builtins.str] = None,
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
        build_command: typing.Optional[builtins.str] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cdk_assert: typing.Optional[builtins.bool] = None,
        cdk_assertions: typing.Optional[builtins.bool] = None,
        cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
        cdkout: typing.Optional[builtins.str] = None,
        cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_version: typing.Optional[builtins.str] = None,
        cdk_version_pinning: typing.Optional[builtins.bool] = None,
        check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        commit_generated: typing.Optional[builtins.bool] = None,
        constructs_version: typing.Optional[builtins.str] = None,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
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
        edge_lambda_auto_discover: typing.Optional[builtins.bool] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        entrypoint_types: typing.Optional[builtins.str] = None,
        eslint: typing.Optional[builtins.bool] = None,
        eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        experimental_integ_runner: typing.Optional[builtins.bool] = None,
        feature_flags: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        integration_test_auto_discover: typing.Optional[builtins.bool] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_auto_discover: typing.Optional[builtins.bool] = None,
        lambda_extension_auto_discover: typing.Optional[builtins.bool] = None,
        lambda_options: typing.Optional[typing.Union[_projen_awscdk_04054675.LambdaFunctionCommonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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
        require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
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
        watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_git_identity: typing.Optional[typing.Union[_projen_github_04054675.GitIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_package_cache: typing.Optional[builtins.bool] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_projen_04054675.GroupRunnerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        yarn_berry_options: typing.Optional[typing.Union[_projen_javascript_04054675.YarnBerryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_signup: typing.Optional[builtins.bool] = None,
        cloudscape_react_ts_website: typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f] = None,
        cloudscape_react_ts_websites: typing.Optional[typing.Sequence[_CloudscapeReactTsWebsiteProject_ef2bfd2f]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Sequence[typing.Union[DeploymentStage, typing.Dict[builtins.str, typing.Any]]]] = None,
        type_safe_api: typing.Optional[_TypeSafeApiProject_b9e4f1cf] = None,
        type_safe_apis: typing.Optional[typing.Sequence[_TypeSafeApiProject_b9e4f1cf]] = None,
        type_safe_web_socket_apis: typing.Optional[typing.Sequence[_TypeSafeWebSocketApiProject_59b62fd2]] = None,
    ) -> None:
        '''Configuration options for the InfrastructureTsProject.

        :param name: Default: $BASEDIR
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param app_entrypoint: (experimental) The CDK app's entrypoint (relative to the source directory, which is "src" by default). Default: "main.ts"
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
        :param build_command: (experimental) A command to execute before synthesis. This command will be called when running ``cdk synth`` or when ``cdk watch`` identifies a change in your source code before redeployment. Default: - no build command
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_options: (experimental) Options for PR build workflow.
        :param build_workflow_triggers: (deprecated) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param cdk_assert: (deprecated) Warning: NodeJS only. Install the Default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0
        :param cdk_assertions: (experimental) Install the assertions library? Only needed for CDK 1.x. If using CDK 2.x then assertions is already included in 'aws-cdk-lib' Default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0
        :param cdk_dependencies: (deprecated) Which AWS CDKv1 modules this project requires.
        :param cdk_dependencies_as_deps: (deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``). This is to ensure that downstream consumers actually have your CDK dependencies installed when using npm < 7 or yarn, where peer dependencies are not automatically installed. If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure they are present during development. Note: this setting only applies to construct library projects Default: true
        :param cdkout: (experimental) cdk.out directory. Default: "cdk.out"
        :param cdk_test_dependencies: (deprecated) AWS CDK modules required for testing.
        :param cdk_version: (experimental) Minimum version of the AWS CDK to depend on. Default: "2.1.0"
        :param cdk_version_pinning: (experimental) Use pinned version instead of caret version for CDK. You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates. If you use experimental features this will let you define the moment you include breaking changes.
        :param check_licenses: (experimental) Configure which licenses should be deemed acceptable for use by dependencies. This setting will cause the build to fail, if any prohibited or not allowed licenses ares encountered. Default: - no license checks are run during the build and all licenses will be accepted
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v4 A secret is required for private repos. Configured with ``@codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories. Default: - if this option is not specified, only public repositories are supported
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param constructs_version: (experimental) Minimum version of the ``constructs`` library to depend on. Default: - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is "10.0.5".
        :param context: (experimental) Additional context to include in ``cdk.json``. Default: - no additional context
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
        :param edge_lambda_auto_discover: (experimental) Automatically adds an ``cloudfront.experimental.EdgeFunction`` for each ``.edge-lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project. Default: true
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json. Default: "lib/index.js"
        :param entrypoint_types: (experimental) The .d.ts file that includes the type declarations for this module. Default: - .d.ts file derived from the project's entrypoint (usually lib/index.d.ts)
        :param eslint: (experimental) Setup eslint. Default: true
        :param eslint_options: (experimental) Eslint options. Default: - opinionated default options
        :param experimental_integ_runner: (experimental) Enable experimental support for the AWS CDK integ-runner. Default: false
        :param feature_flags: (experimental) Include all feature flags in cdk.json. Default: true
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param homepage: (experimental) Package's Homepage / Website.
        :param integration_test_auto_discover: (experimental) Automatically discovers and creates integration tests for each ``.integ.ts`` file in under your test directory. Default: true
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param lambda_auto_discover: (experimental) Automatically adds an ``awscdk.LambdaFunction`` for each ``.lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project. Default: true
        :param lambda_extension_auto_discover: (experimental) Automatically adds an ``awscdk.LambdaExtension`` for each ``.lambda-extension.ts`` entrypoint in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project. Default: true
        :param lambda_options: (experimental) Common options for all AWS Lambda functions. Default: - default options
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
        :param require_approval: (experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them. Default: ApprovalLevel.BROADENING
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
        :param watch_excludes: (experimental) Glob patterns to exclude from ``cdk watch``. Default: []
        :param watch_includes: (experimental) Glob patterns to include in ``cdk watch``. Default: []
        :param workflow_bootstrap_steps: (experimental) Workflow steps to use in order to bootstrap this repo. Default: "yarn install --frozen-lockfile && yarn projen"
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_git_identity: (experimental) The git identity to use in workflows. Default: - GitHub Actions
        :param workflow_node_version: (experimental) The node version to use in GitHub workflows. Default: - same as ``minNodeVersion``
        :param workflow_package_cache: (experimental) Enable Node.js package cache in GitHub workflows. Default: false
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param yarn_berry_options: (experimental) Options for Yarn Berry. Default: - Yarn Berry v4 with all default options
        :param allow_signup: Allow self sign up for the UserIdentity construct. Default: - false
        :param cloudscape_react_ts_website: (deprecated) CloudscapeReactTsWebsiteProject instance to use when setting up the initial project sample code.
        :param cloudscape_react_ts_websites: CloudscapeReactTsWebsiteProject instances to use when setting up the initial project sample code.
        :param stack_name: Stack name. Default: infra-dev
        :param stages: List of deployment stages.
        :param type_safe_api: (deprecated) TypeSafeApi instance to use when setting up the initial project sample code.
        :param type_safe_apis: TypeSafeApi instances to use when setting up the initial project sample code.
        :param type_safe_web_socket_apis: TypeSafeWebSocketApi instances to use when setting up the initial project sample code.
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
        if isinstance(lambda_options, dict):
            lambda_options = _projen_awscdk_04054675.LambdaFunctionCommonOptions(**lambda_options)
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
            type_hints = typing.get_type_hints(_typecheckingstub__645c09c0b767a91c12b261df73ba2e103b6a81a457750a68d542cf7277553130)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_library_dependencies", value=allow_library_dependencies, expected_type=type_hints["allow_library_dependencies"])
            check_type(argname="argument app_entrypoint", value=app_entrypoint, expected_type=type_hints["app_entrypoint"])
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
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_workflow", value=build_workflow, expected_type=type_hints["build_workflow"])
            check_type(argname="argument build_workflow_options", value=build_workflow_options, expected_type=type_hints["build_workflow_options"])
            check_type(argname="argument build_workflow_triggers", value=build_workflow_triggers, expected_type=type_hints["build_workflow_triggers"])
            check_type(argname="argument bundled_deps", value=bundled_deps, expected_type=type_hints["bundled_deps"])
            check_type(argname="argument bundler_options", value=bundler_options, expected_type=type_hints["bundler_options"])
            check_type(argname="argument cdk_assert", value=cdk_assert, expected_type=type_hints["cdk_assert"])
            check_type(argname="argument cdk_assertions", value=cdk_assertions, expected_type=type_hints["cdk_assertions"])
            check_type(argname="argument cdk_dependencies", value=cdk_dependencies, expected_type=type_hints["cdk_dependencies"])
            check_type(argname="argument cdk_dependencies_as_deps", value=cdk_dependencies_as_deps, expected_type=type_hints["cdk_dependencies_as_deps"])
            check_type(argname="argument cdkout", value=cdkout, expected_type=type_hints["cdkout"])
            check_type(argname="argument cdk_test_dependencies", value=cdk_test_dependencies, expected_type=type_hints["cdk_test_dependencies"])
            check_type(argname="argument cdk_version", value=cdk_version, expected_type=type_hints["cdk_version"])
            check_type(argname="argument cdk_version_pinning", value=cdk_version_pinning, expected_type=type_hints["cdk_version_pinning"])
            check_type(argname="argument check_licenses", value=check_licenses, expected_type=type_hints["check_licenses"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument code_cov", value=code_cov, expected_type=type_hints["code_cov"])
            check_type(argname="argument code_cov_token_secret", value=code_cov_token_secret, expected_type=type_hints["code_cov_token_secret"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument constructs_version", value=constructs_version, expected_type=type_hints["constructs_version"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
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
            check_type(argname="argument edge_lambda_auto_discover", value=edge_lambda_auto_discover, expected_type=type_hints["edge_lambda_auto_discover"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument entrypoint_types", value=entrypoint_types, expected_type=type_hints["entrypoint_types"])
            check_type(argname="argument eslint", value=eslint, expected_type=type_hints["eslint"])
            check_type(argname="argument eslint_options", value=eslint_options, expected_type=type_hints["eslint_options"])
            check_type(argname="argument experimental_integ_runner", value=experimental_integ_runner, expected_type=type_hints["experimental_integ_runner"])
            check_type(argname="argument feature_flags", value=feature_flags, expected_type=type_hints["feature_flags"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument gitignore", value=gitignore, expected_type=type_hints["gitignore"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument integration_test_auto_discover", value=integration_test_auto_discover, expected_type=type_hints["integration_test_auto_discover"])
            check_type(argname="argument jest", value=jest, expected_type=type_hints["jest"])
            check_type(argname="argument jest_options", value=jest_options, expected_type=type_hints["jest_options"])
            check_type(argname="argument jsii_release_version", value=jsii_release_version, expected_type=type_hints["jsii_release_version"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument lambda_auto_discover", value=lambda_auto_discover, expected_type=type_hints["lambda_auto_discover"])
            check_type(argname="argument lambda_extension_auto_discover", value=lambda_extension_auto_discover, expected_type=type_hints["lambda_extension_auto_discover"])
            check_type(argname="argument lambda_options", value=lambda_options, expected_type=type_hints["lambda_options"])
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
            check_type(argname="argument require_approval", value=require_approval, expected_type=type_hints["require_approval"])
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
            check_type(argname="argument watch_excludes", value=watch_excludes, expected_type=type_hints["watch_excludes"])
            check_type(argname="argument watch_includes", value=watch_includes, expected_type=type_hints["watch_includes"])
            check_type(argname="argument workflow_bootstrap_steps", value=workflow_bootstrap_steps, expected_type=type_hints["workflow_bootstrap_steps"])
            check_type(argname="argument workflow_container_image", value=workflow_container_image, expected_type=type_hints["workflow_container_image"])
            check_type(argname="argument workflow_git_identity", value=workflow_git_identity, expected_type=type_hints["workflow_git_identity"])
            check_type(argname="argument workflow_node_version", value=workflow_node_version, expected_type=type_hints["workflow_node_version"])
            check_type(argname="argument workflow_package_cache", value=workflow_package_cache, expected_type=type_hints["workflow_package_cache"])
            check_type(argname="argument workflow_runs_on", value=workflow_runs_on, expected_type=type_hints["workflow_runs_on"])
            check_type(argname="argument workflow_runs_on_group", value=workflow_runs_on_group, expected_type=type_hints["workflow_runs_on_group"])
            check_type(argname="argument yarn_berry_options", value=yarn_berry_options, expected_type=type_hints["yarn_berry_options"])
            check_type(argname="argument allow_signup", value=allow_signup, expected_type=type_hints["allow_signup"])
            check_type(argname="argument cloudscape_react_ts_website", value=cloudscape_react_ts_website, expected_type=type_hints["cloudscape_react_ts_website"])
            check_type(argname="argument cloudscape_react_ts_websites", value=cloudscape_react_ts_websites, expected_type=type_hints["cloudscape_react_ts_websites"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
            check_type(argname="argument type_safe_api", value=type_safe_api, expected_type=type_hints["type_safe_api"])
            check_type(argname="argument type_safe_apis", value=type_safe_apis, expected_type=type_hints["type_safe_apis"])
            check_type(argname="argument type_safe_web_socket_apis", value=type_safe_web_socket_apis, expected_type=type_hints["type_safe_web_socket_apis"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_library_dependencies is not None:
            self._values["allow_library_dependencies"] = allow_library_dependencies
        if app_entrypoint is not None:
            self._values["app_entrypoint"] = app_entrypoint
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
        if build_command is not None:
            self._values["build_command"] = build_command
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
        if cdk_assert is not None:
            self._values["cdk_assert"] = cdk_assert
        if cdk_assertions is not None:
            self._values["cdk_assertions"] = cdk_assertions
        if cdk_dependencies is not None:
            self._values["cdk_dependencies"] = cdk_dependencies
        if cdk_dependencies_as_deps is not None:
            self._values["cdk_dependencies_as_deps"] = cdk_dependencies_as_deps
        if cdkout is not None:
            self._values["cdkout"] = cdkout
        if cdk_test_dependencies is not None:
            self._values["cdk_test_dependencies"] = cdk_test_dependencies
        if cdk_version is not None:
            self._values["cdk_version"] = cdk_version
        if cdk_version_pinning is not None:
            self._values["cdk_version_pinning"] = cdk_version_pinning
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
        if constructs_version is not None:
            self._values["constructs_version"] = constructs_version
        if context is not None:
            self._values["context"] = context
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
        if edge_lambda_auto_discover is not None:
            self._values["edge_lambda_auto_discover"] = edge_lambda_auto_discover
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if entrypoint_types is not None:
            self._values["entrypoint_types"] = entrypoint_types
        if eslint is not None:
            self._values["eslint"] = eslint
        if eslint_options is not None:
            self._values["eslint_options"] = eslint_options
        if experimental_integ_runner is not None:
            self._values["experimental_integ_runner"] = experimental_integ_runner
        if feature_flags is not None:
            self._values["feature_flags"] = feature_flags
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
        if integration_test_auto_discover is not None:
            self._values["integration_test_auto_discover"] = integration_test_auto_discover
        if jest is not None:
            self._values["jest"] = jest
        if jest_options is not None:
            self._values["jest_options"] = jest_options
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if keywords is not None:
            self._values["keywords"] = keywords
        if lambda_auto_discover is not None:
            self._values["lambda_auto_discover"] = lambda_auto_discover
        if lambda_extension_auto_discover is not None:
            self._values["lambda_extension_auto_discover"] = lambda_extension_auto_discover
        if lambda_options is not None:
            self._values["lambda_options"] = lambda_options
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
        if require_approval is not None:
            self._values["require_approval"] = require_approval
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
        if watch_excludes is not None:
            self._values["watch_excludes"] = watch_excludes
        if watch_includes is not None:
            self._values["watch_includes"] = watch_includes
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
        if allow_signup is not None:
            self._values["allow_signup"] = allow_signup
        if cloudscape_react_ts_website is not None:
            self._values["cloudscape_react_ts_website"] = cloudscape_react_ts_website
        if cloudscape_react_ts_websites is not None:
            self._values["cloudscape_react_ts_websites"] = cloudscape_react_ts_websites
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if stages is not None:
            self._values["stages"] = stages
        if type_safe_api is not None:
            self._values["type_safe_api"] = type_safe_api
        if type_safe_apis is not None:
            self._values["type_safe_apis"] = type_safe_apis
        if type_safe_web_socket_apis is not None:
            self._values["type_safe_web_socket_apis"] = type_safe_web_socket_apis

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
    def app_entrypoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) The CDK app's entrypoint (relative to the source directory, which is "src" by default).

        :default: "main.ts"

        :stability: experimental
        '''
        result = self._values.get("app_entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

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
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A command to execute before synthesis.

        This command will be called when
        running ``cdk synth`` or when ``cdk watch`` identifies a change in your source
        code before redeployment.

        :default: - no build command

        :stability: experimental
        '''
        result = self._values.get("build_command")
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
    def cdk_assert(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Warning: NodeJS only.

        Install the

        :default: - will be included by default for AWS CDK >= 1.0.0 < 2.0.0

        :deprecated: The

        :stability: deprecated
        :aws-cdk: /assertions (in V1) and included in ``aws-cdk-lib`` for V2.
        '''
        result = self._values.get("cdk_assert")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_assertions(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install the assertions library?

        Only needed for CDK 1.x. If using CDK 2.x then
        assertions is already included in 'aws-cdk-lib'

        :default: - will be included by default for AWS CDK >= 1.111.0 < 2.0.0

        :stability: experimental
        '''
        result = self._values.get("cdk_assertions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdk_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Which AWS CDKv1 modules this project requires.

        :deprecated: For CDK 2.x use "deps" instead. (or "peerDeps" if you're building a library)

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_dependencies_as_deps(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) If this is enabled (default), all modules declared in ``cdkDependencies`` will be also added as normal ``dependencies`` (as well as ``peerDependencies``).

        This is to ensure that downstream consumers actually have your CDK dependencies installed
        when using npm < 7 or yarn, where peer dependencies are not automatically installed.
        If this is disabled, ``cdkDependencies`` will be added to ``devDependencies`` to ensure
        they are present during development.

        Note: this setting only applies to construct library projects

        :default: true

        :deprecated: Not supported in CDK v2.

        :stability: deprecated
        '''
        result = self._values.get("cdk_dependencies_as_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cdkout(self) -> typing.Optional[builtins.str]:
        '''(experimental) cdk.out directory.

        :default: "cdk.out"

        :stability: experimental
        '''
        result = self._values.get("cdkout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_test_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) AWS CDK modules required for testing.

        :deprecated: For CDK 2.x use 'devDeps' (in node.js projects) or 'testDeps' (in java projects) instead

        :stability: deprecated
        '''
        result = self._values.get("cdk_test_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the AWS CDK to depend on.

        :default: "2.1.0"

        :stability: experimental
        '''
        result = self._values.get("cdk_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdk_version_pinning(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use pinned version instead of caret version for CDK.

        You can use this to prevent mixed versions for your CDK dependencies and to prevent auto-updates.
        If you use experimental features this will let you define the moment you include breaking changes.

        :stability: experimental
        '''
        result = self._values.get("cdk_version_pinning")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def constructs_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum version of the ``constructs`` library to depend on.

        :default:

        - for CDK 1.x the default is "3.2.27", for CDK 2.x the default is
        "10.0.5".

        :stability: experimental
        '''
        result = self._values.get("constructs_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional context to include in ``cdk.json``.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

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
        :featured: true
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
    def edge_lambda_auto_discover(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically adds an ``cloudfront.experimental.EdgeFunction`` for each ``.edge-lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edge_lambda_auto_discover")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def experimental_integ_runner(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable experimental support for the AWS CDK integ-runner.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("experimental_integ_runner")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def feature_flags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include all feature flags in cdk.json.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("feature_flags")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def integration_test_auto_discover(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically discovers and creates integration tests for each ``.integ.ts`` file in under your test directory.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("integration_test_auto_discover")
        return typing.cast(typing.Optional[builtins.bool], result)

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
    def lambda_auto_discover(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically adds an ``awscdk.LambdaFunction`` for each ``.lambda.ts`` handler in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("lambda_auto_discover")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lambda_extension_auto_discover(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically adds an ``awscdk.LambdaExtension`` for each ``.lambda-extension.ts`` entrypoint in your source tree. If this is disabled, you can manually add an ``awscdk.AutoDiscover`` component to your project.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("lambda_extension_auto_discover")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lambda_options(
        self,
    ) -> typing.Optional[_projen_awscdk_04054675.LambdaFunctionCommonOptions]:
        '''(experimental) Common options for all AWS Lambda functions.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("lambda_options")
        return typing.cast(typing.Optional[_projen_awscdk_04054675.LambdaFunctionCommonOptions], result)

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
        :featured: true
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
    def require_approval(
        self,
    ) -> typing.Optional[_projen_awscdk_04054675.ApprovalLevel]:
        '''(experimental) To protect you against unintended changes that affect your security posture, the AWS CDK Toolkit prompts you to approve security-related changes before deploying them.

        :default: ApprovalLevel.BROADENING

        :stability: experimental
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[_projen_awscdk_04054675.ApprovalLevel], result)

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
    def watch_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to exclude from ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def watch_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to include in ``cdk watch``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("watch_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

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
    def allow_signup(self) -> typing.Optional[builtins.bool]:
        '''Allow self sign up for the UserIdentity construct.

        :default: - false
        '''
        result = self._values.get("allow_signup")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cloudscape_react_ts_website(
        self,
    ) -> typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f]:
        '''(deprecated) CloudscapeReactTsWebsiteProject instance to use when setting up the initial project sample code.

        :deprecated: use cloudscapeReactTsWebsites

        :stability: deprecated
        '''
        result = self._values.get("cloudscape_react_ts_website")
        return typing.cast(typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f], result)

    @builtins.property
    def cloudscape_react_ts_websites(
        self,
    ) -> typing.Optional[typing.List[_CloudscapeReactTsWebsiteProject_ef2bfd2f]]:
        '''CloudscapeReactTsWebsiteProject instances to use when setting up the initial project sample code.'''
        result = self._values.get("cloudscape_react_ts_websites")
        return typing.cast(typing.Optional[typing.List[_CloudscapeReactTsWebsiteProject_ef2bfd2f]], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Stack name.

        :default: infra-dev
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stages(self) -> typing.Optional[typing.List[DeploymentStage]]:
        '''List of deployment stages.'''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.List[DeploymentStage]], result)

    @builtins.property
    def type_safe_api(self) -> typing.Optional[_TypeSafeApiProject_b9e4f1cf]:
        '''(deprecated) TypeSafeApi instance to use when setting up the initial project sample code.

        :deprecated: use typeSafeApis

        :stability: deprecated
        '''
        result = self._values.get("type_safe_api")
        return typing.cast(typing.Optional[_TypeSafeApiProject_b9e4f1cf], result)

    @builtins.property
    def type_safe_apis(
        self,
    ) -> typing.Optional[typing.List[_TypeSafeApiProject_b9e4f1cf]]:
        '''TypeSafeApi instances to use when setting up the initial project sample code.'''
        result = self._values.get("type_safe_apis")
        return typing.cast(typing.Optional[typing.List[_TypeSafeApiProject_b9e4f1cf]], result)

    @builtins.property
    def type_safe_web_socket_apis(
        self,
    ) -> typing.Optional[typing.List[_TypeSafeWebSocketApiProject_59b62fd2]]:
        '''TypeSafeWebSocketApi instances to use when setting up the initial project sample code.'''
        result = self._values.get("type_safe_web_socket_apis")
        return typing.cast(typing.Optional[typing.List[_TypeSafeWebSocketApiProject_59b62fd2]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfrastructureTsProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsCdkJavaAppOptions",
    "AwsCdkPythonAppOptions",
    "AwsCdkTypeScriptAppOptions",
    "DeploymentStage",
    "InfrastructureJavaProject",
    "InfrastructureJavaProjectOptions",
    "InfrastructurePyProject",
    "InfrastructurePyProjectOptions",
    "InfrastructureTsProject",
    "InfrastructureTsProjectOptions",
]

publication.publish()

def _typecheckingstub__3ea975ed4c9a1918e26b02319faeb5e7df13050f92baf8b835320a1908ec9b73(
    *,
    name: builtins.str,
    artifact_id: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_command: typing.Optional[builtins.str] = None,
    cdk_assert: typing.Optional[builtins.bool] = None,
    cdk_assertions: typing.Optional[builtins.bool] = None,
    cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
    cdkout: typing.Optional[builtins.str] = None,
    cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_version: typing.Optional[builtins.str] = None,
    cdk_version_pinning: typing.Optional[builtins.bool] = None,
    clobber: typing.Optional[builtins.bool] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    constructs_version: typing.Optional[builtins.str] = None,
    context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    distdir: typing.Optional[builtins.str] = None,
    feature_flags: typing.Optional[builtins.bool] = None,
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
    require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
    sample: typing.Optional[builtins.bool] = None,
    sample_java_package: typing.Optional[builtins.str] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    vscode: typing.Optional[builtins.bool] = None,
    watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05dda3da908a708305470f6c3db90baf552c1784e8fbb842f3a927f7577f28d(
    *,
    name: builtins.str,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_command: typing.Optional[builtins.str] = None,
    cdk_assert: typing.Optional[builtins.bool] = None,
    cdk_assertions: typing.Optional[builtins.bool] = None,
    cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
    cdkout: typing.Optional[builtins.str] = None,
    cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_version: typing.Optional[builtins.str] = None,
    cdk_version_pinning: typing.Optional[builtins.bool] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    constructs_version: typing.Optional[builtins.str] = None,
    context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    feature_flags: typing.Optional[builtins.bool] = None,
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
    module_name: typing.Optional[builtins.str] = None,
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
    require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
    sample: typing.Optional[builtins.bool] = None,
    setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    setuptools: typing.Optional[builtins.bool] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    testdir: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    vscode: typing.Optional[builtins.bool] = None,
    watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d18b26cb9f80927dee1642f1695c52ae992d3f492f97ff41c4a8baf4c9e5fd9(
    *,
    name: builtins.str,
    allow_library_dependencies: typing.Optional[builtins.bool] = None,
    app_entrypoint: typing.Optional[builtins.str] = None,
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
    build_command: typing.Optional[builtins.str] = None,
    build_workflow: typing.Optional[builtins.bool] = None,
    build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
    bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cdk_assert: typing.Optional[builtins.bool] = None,
    cdk_assertions: typing.Optional[builtins.bool] = None,
    cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
    cdkout: typing.Optional[builtins.str] = None,
    cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_version: typing.Optional[builtins.str] = None,
    cdk_version_pinning: typing.Optional[builtins.bool] = None,
    check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_cov: typing.Optional[builtins.bool] = None,
    code_cov_token_secret: typing.Optional[builtins.str] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    constructs_version: typing.Optional[builtins.str] = None,
    context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
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
    edge_lambda_auto_discover: typing.Optional[builtins.bool] = None,
    entrypoint: typing.Optional[builtins.str] = None,
    entrypoint_types: typing.Optional[builtins.str] = None,
    eslint: typing.Optional[builtins.bool] = None,
    eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    experimental_integ_runner: typing.Optional[builtins.bool] = None,
    feature_flags: typing.Optional[builtins.bool] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    homepage: typing.Optional[builtins.str] = None,
    integration_test_auto_discover: typing.Optional[builtins.bool] = None,
    jest: typing.Optional[builtins.bool] = None,
    jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    lambda_auto_discover: typing.Optional[builtins.bool] = None,
    lambda_extension_auto_discover: typing.Optional[builtins.bool] = None,
    lambda_options: typing.Optional[typing.Union[_projen_awscdk_04054675.LambdaFunctionCommonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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
    require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
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
    watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__6b730d5a9529973352ea249c46d5732448dd09ac35400ac252ba0be082864168(
    *,
    account: jsii.Number,
    region: builtins.str,
    stage_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1710385bc23fdc48cd7d8c347c87ab551177038b183cf7fa1d2bac8ec9bd68(
    *,
    name: builtins.str,
    artifact_id: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_command: typing.Optional[builtins.str] = None,
    cdk_assert: typing.Optional[builtins.bool] = None,
    cdk_assertions: typing.Optional[builtins.bool] = None,
    cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
    cdkout: typing.Optional[builtins.str] = None,
    cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_version: typing.Optional[builtins.str] = None,
    cdk_version_pinning: typing.Optional[builtins.bool] = None,
    clobber: typing.Optional[builtins.bool] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    compile_options: typing.Optional[typing.Union[_projen_java_04054675.MavenCompileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    constructs_version: typing.Optional[builtins.str] = None,
    context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    distdir: typing.Optional[builtins.str] = None,
    feature_flags: typing.Optional[builtins.bool] = None,
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
    require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
    sample: typing.Optional[builtins.bool] = None,
    sample_java_package: typing.Optional[builtins.str] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    test_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    vscode: typing.Optional[builtins.bool] = None,
    watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_signup: typing.Optional[builtins.bool] = None,
    cloudscape_react_ts_website: typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f] = None,
    cloudscape_react_ts_websites: typing.Optional[typing.Sequence[_CloudscapeReactTsWebsiteProject_ef2bfd2f]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    stages: typing.Optional[typing.Sequence[typing.Union[DeploymentStage, typing.Dict[builtins.str, typing.Any]]]] = None,
    type_safe_api: typing.Optional[_TypeSafeApiProject_b9e4f1cf] = None,
    type_safe_apis: typing.Optional[typing.Sequence[_TypeSafeApiProject_b9e4f1cf]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f976053715e4d3f0f05e190a57600d1bd7dd400a75f2f380efb578428967fda7(
    *,
    name: builtins.str,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    auto_approve_options: typing.Optional[typing.Union[_projen_github_04054675.AutoApproveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_projen_github_04054675.AutoMergeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_command: typing.Optional[builtins.str] = None,
    cdk_assert: typing.Optional[builtins.bool] = None,
    cdk_assertions: typing.Optional[builtins.bool] = None,
    cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
    cdkout: typing.Optional[builtins.str] = None,
    cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_version: typing.Optional[builtins.str] = None,
    cdk_version_pinning: typing.Optional[builtins.bool] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    constructs_version: typing.Optional[builtins.str] = None,
    context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    feature_flags: typing.Optional[builtins.bool] = None,
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
    module_name: typing.Optional[builtins.str] = None,
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
    require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
    sample: typing.Optional[builtins.bool] = None,
    setup_config: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    setuptools: typing.Optional[builtins.bool] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_projen_github_04054675.StaleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    testdir: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    vscode: typing.Optional[builtins.bool] = None,
    watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_signup: typing.Optional[builtins.bool] = None,
    cloudscape_react_ts_website: typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f] = None,
    cloudscape_react_ts_websites: typing.Optional[typing.Sequence[_CloudscapeReactTsWebsiteProject_ef2bfd2f]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    stages: typing.Optional[typing.Sequence[typing.Union[DeploymentStage, typing.Dict[builtins.str, typing.Any]]]] = None,
    type_safe_api: typing.Optional[_TypeSafeApiProject_b9e4f1cf] = None,
    type_safe_apis: typing.Optional[typing.Sequence[_TypeSafeApiProject_b9e4f1cf]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645c09c0b767a91c12b261df73ba2e103b6a81a457750a68d542cf7277553130(
    *,
    name: builtins.str,
    allow_library_dependencies: typing.Optional[builtins.bool] = None,
    app_entrypoint: typing.Optional[builtins.str] = None,
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
    build_command: typing.Optional[builtins.str] = None,
    build_workflow: typing.Optional[builtins.bool] = None,
    build_workflow_options: typing.Optional[typing.Union[_projen_javascript_04054675.BuildWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_workflow_triggers: typing.Optional[typing.Union[_projen_github_workflows_04054675.Triggers, typing.Dict[builtins.str, typing.Any]]] = None,
    bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    bundler_options: typing.Optional[typing.Union[_projen_javascript_04054675.BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cdk_assert: typing.Optional[builtins.bool] = None,
    cdk_assertions: typing.Optional[builtins.bool] = None,
    cdk_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_dependencies_as_deps: typing.Optional[builtins.bool] = None,
    cdkout: typing.Optional[builtins.str] = None,
    cdk_test_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_version: typing.Optional[builtins.str] = None,
    cdk_version_pinning: typing.Optional[builtins.bool] = None,
    check_licenses: typing.Optional[typing.Union[_projen_javascript_04054675.LicenseCheckerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    code_artifact_options: typing.Optional[typing.Union[_projen_javascript_04054675.CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_cov: typing.Optional[builtins.bool] = None,
    code_cov_token_secret: typing.Optional[builtins.str] = None,
    commit_generated: typing.Optional[builtins.bool] = None,
    constructs_version: typing.Optional[builtins.str] = None,
    context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
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
    edge_lambda_auto_discover: typing.Optional[builtins.bool] = None,
    entrypoint: typing.Optional[builtins.str] = None,
    entrypoint_types: typing.Optional[builtins.str] = None,
    eslint: typing.Optional[builtins.bool] = None,
    eslint_options: typing.Optional[typing.Union[_projen_javascript_04054675.EslintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    experimental_integ_runner: typing.Optional[builtins.bool] = None,
    feature_flags: typing.Optional[builtins.bool] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_projen_github_04054675.GitHubOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    homepage: typing.Optional[builtins.str] = None,
    integration_test_auto_discover: typing.Optional[builtins.bool] = None,
    jest: typing.Optional[builtins.bool] = None,
    jest_options: typing.Optional[typing.Union[_projen_javascript_04054675.JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    lambda_auto_discover: typing.Optional[builtins.bool] = None,
    lambda_extension_auto_discover: typing.Optional[builtins.bool] = None,
    lambda_options: typing.Optional[typing.Union[_projen_awscdk_04054675.LambdaFunctionCommonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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
    require_approval: typing.Optional[_projen_awscdk_04054675.ApprovalLevel] = None,
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
    watch_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    watch_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_projen_github_workflows_04054675.JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_git_identity: typing.Optional[typing.Union[_projen_github_04054675.GitIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_node_version: typing.Optional[builtins.str] = None,
    workflow_package_cache: typing.Optional[builtins.bool] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_projen_04054675.GroupRunnerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    yarn_berry_options: typing.Optional[typing.Union[_projen_javascript_04054675.YarnBerryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_signup: typing.Optional[builtins.bool] = None,
    cloudscape_react_ts_website: typing.Optional[_CloudscapeReactTsWebsiteProject_ef2bfd2f] = None,
    cloudscape_react_ts_websites: typing.Optional[typing.Sequence[_CloudscapeReactTsWebsiteProject_ef2bfd2f]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    stages: typing.Optional[typing.Sequence[typing.Union[DeploymentStage, typing.Dict[builtins.str, typing.Any]]]] = None,
    type_safe_api: typing.Optional[_TypeSafeApiProject_b9e4f1cf] = None,
    type_safe_apis: typing.Optional[typing.Sequence[_TypeSafeApiProject_b9e4f1cf]] = None,
    type_safe_web_socket_apis: typing.Optional[typing.Sequence[_TypeSafeWebSocketApiProject_59b62fd2]] = None,
) -> None:
    """Type checking stubs"""
    pass
