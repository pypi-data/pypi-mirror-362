r'''
# AWS PDK

All documentation is located at: https://aws.github.io/aws-pdk

# aws-arch

Please refer to [Developer Guide](./docs/developer_guides/aws-arch/index.md).

# cdk-graph

Please refer to [Developer Guide](./docs/developer_guides/cdk-graph/index.md).

# cdk-graph-plugin-diagram

Please refer to [Developer Guide](./docs/developer_guides/cdk-graph-plugin-diagram/index.md).

# cdk-graph-plugin-threat-composer

Please refer to [Developer Guide](./docs/developer_guides/cdk-graph-plugin-threat-composer/index.md).

# cloudscape-react-ts-website

Please refer to [Developer Guide](./docs/developer_guides/cloudscape-react-ts-website/index.md).

# identity

Please refer to [Developer Guide](./docs/developer_guides/identity/index.md).

# infrastructure

Please refer to [Developer Guide](./docs/developer_guides/infrastructure/index.md).

# monorepo

Please refer to [Developer Guide](./docs/developer_guides/monorepo/index.md).

# pdk-nag

Please refer to [Developer Guide](./docs/developer_guides/pdk-nag/index.md).

# pipeline

Please refer to [Developer Guide](./docs/developer_guides/pipeline/index.md).

# static-website

Please refer to [Developer Guide](./docs/developer_guides/static-website/index.md).

# type-safe-api

Please refer to [Developer Guide](./docs/developer_guides/type-safe-api/index.md).
'''
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

from ._jsii import *

__all__ = [
    "aws_arch",
    "cdk_graph",
    "cdk_graph_plugin_diagram",
    "cdk_graph_plugin_threat_composer",
    "cloudscape_react_ts_website",
    "identity",
    "infrastructure",
    "monorepo",
    "pdk_nag",
    "pipeline",
    "static_website",
    "type_safe_api",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import aws_arch
from . import cdk_graph
from . import cdk_graph_plugin_diagram
from . import cdk_graph_plugin_threat_composer
from . import cloudscape_react_ts_website
from . import identity
from . import infrastructure
from . import monorepo
from . import pdk_nag
from . import pipeline
from . import static_website
from . import type_safe_api
