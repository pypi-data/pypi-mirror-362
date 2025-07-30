r'''
# CDKTF prebuilt bindings for hashicorp/boundary provider version 1.3.1

This repo builds and publishes the [Terraform boundary provider](https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-boundary](https://www.npmjs.com/package/@cdktf/provider-boundary).

`npm install @cdktf/provider-boundary`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-boundary](https://pypi.org/project/cdktf-cdktf-provider-boundary).

`pipenv install cdktf-cdktf-provider-boundary`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Boundary](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Boundary).

`dotnet add package HashiCorp.Cdktf.Providers.Boundary`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-boundary](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-boundary).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-boundary</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-boundary-go`](https://github.com/cdktf/cdktf-provider-boundary-go) package.

`go get github.com/cdktf/cdktf-provider-boundary-go/boundary/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-boundary-go/blob/main/boundary/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-boundary).

## Versioning

This project is explicitly not tracking the Terraform boundary provider version 1:1. In fact, it always tracks `latest` of `~> 1.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform boundary provider](https://registry.terraform.io/providers/hashicorp/boundary/1.3.1)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://github.com/projen/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktf/cdktf-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTF Repository Manager](https://github.com/cdktf/cdktf-repository-manager/).
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
    "account",
    "account_ldap",
    "account_oidc",
    "account_password",
    "alias_target",
    "auth_method",
    "auth_method_ldap",
    "auth_method_oidc",
    "auth_method_password",
    "credential_json",
    "credential_library_vault",
    "credential_library_vault_ssh_certificate",
    "credential_ssh_private_key",
    "credential_store_static",
    "credential_store_vault",
    "credential_username_password",
    "data_boundary_account",
    "data_boundary_auth_method",
    "data_boundary_group",
    "data_boundary_scope",
    "data_boundary_user",
    "group",
    "host",
    "host_catalog",
    "host_catalog_plugin",
    "host_catalog_static",
    "host_set",
    "host_set_plugin",
    "host_set_static",
    "host_static",
    "managed_group",
    "managed_group_ldap",
    "policy_storage",
    "provider",
    "role",
    "scope",
    "scope_policy_attachment",
    "storage_bucket",
    "target",
    "user",
    "worker",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import account
from . import account_ldap
from . import account_oidc
from . import account_password
from . import alias_target
from . import auth_method
from . import auth_method_ldap
from . import auth_method_oidc
from . import auth_method_password
from . import credential_json
from . import credential_library_vault
from . import credential_library_vault_ssh_certificate
from . import credential_ssh_private_key
from . import credential_store_static
from . import credential_store_vault
from . import credential_username_password
from . import data_boundary_account
from . import data_boundary_auth_method
from . import data_boundary_group
from . import data_boundary_scope
from . import data_boundary_user
from . import group
from . import host
from . import host_catalog
from . import host_catalog_plugin
from . import host_catalog_static
from . import host_set
from . import host_set_plugin
from . import host_set_static
from . import host_static
from . import managed_group
from . import managed_group_ldap
from . import policy_storage
from . import provider
from . import role
from . import scope
from . import scope_policy_attachment
from . import storage_bucket
from . import target
from . import user
from . import worker
