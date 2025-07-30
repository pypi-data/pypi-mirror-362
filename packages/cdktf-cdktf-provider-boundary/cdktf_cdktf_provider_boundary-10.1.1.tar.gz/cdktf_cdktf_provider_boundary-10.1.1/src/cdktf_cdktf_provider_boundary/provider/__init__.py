r'''
# `provider`

Refer to the Terraform Registry for docs: [`boundary`](https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class BoundaryProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-boundary.provider.BoundaryProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs boundary}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        addr: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        auth_method_id: typing.Optional[builtins.str] = None,
        auth_method_login_name: typing.Optional[builtins.str] = None,
        auth_method_password: typing.Optional[builtins.str] = None,
        password_auth_method_login_name: typing.Optional[builtins.str] = None,
        password_auth_method_password: typing.Optional[builtins.str] = None,
        plugin_execution_dir: typing.Optional[builtins.str] = None,
        recovery_kms_hcl: typing.Optional[builtins.str] = None,
        scope_id: typing.Optional[builtins.str] = None,
        tls_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs boundary} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param addr: The base url of the Boundary API, e.g. "http://127.0.0.1:9200". If not set, it will be read from the "BOUNDARY_ADDR" env var. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#addr BoundaryProvider#addr}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#alias BoundaryProvider#alias}
        :param auth_method_id: The auth method ID e.g. ampw_1234567890. If not set, the default auth method for the given scope ID will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#auth_method_id BoundaryProvider#auth_method_id}
        :param auth_method_login_name: The auth method login name for password-style or ldap-style auth methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#auth_method_login_name BoundaryProvider#auth_method_login_name}
        :param auth_method_password: The auth method password for password-style or ldap-style auth methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#auth_method_password BoundaryProvider#auth_method_password}
        :param password_auth_method_login_name: The auth method login name for password-style auth methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#password_auth_method_login_name BoundaryProvider#password_auth_method_login_name}
        :param password_auth_method_password: The auth method password for password-style auth methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#password_auth_method_password BoundaryProvider#password_auth_method_password}
        :param plugin_execution_dir: Specifies a directory that the Boundary provider can use to write and execute its built-in plugins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#plugin_execution_dir BoundaryProvider#plugin_execution_dir}
        :param recovery_kms_hcl: Can be a heredoc string or a path on disk. If set, the string/file will be parsed as HCL and used with the recovery KMS mechanism. While this is set, it will override any other authentication information; the KMS mechanism will always be used. See Boundary's KMS docs for examples: https://boundaryproject.io/docs/configuration/kms Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#recovery_kms_hcl BoundaryProvider#recovery_kms_hcl}
        :param scope_id: The scope ID for the default auth method. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#scope_id BoundaryProvider#scope_id}
        :param tls_insecure: When set to true, does not validate the Boundary API endpoint certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#tls_insecure BoundaryProvider#tls_insecure}
        :param token: The Boundary token to use, as a string or path on disk containing just the string. If set, the token read here will be used in place of authenticating with the auth method specified in "auth_method_id", although the recovery KMS mechanism will still override this. Can also be set with the BOUNDARY_TOKEN environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#token BoundaryProvider#token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce45866643ede5c3f23dda6c62ba4515b4bf12276ac23bc01292aac21f883d15)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = BoundaryProviderConfig(
            addr=addr,
            alias=alias,
            auth_method_id=auth_method_id,
            auth_method_login_name=auth_method_login_name,
            auth_method_password=auth_method_password,
            password_auth_method_login_name=password_auth_method_login_name,
            password_auth_method_password=password_auth_method_password,
            plugin_execution_dir=plugin_execution_dir,
            recovery_kms_hcl=recovery_kms_hcl,
            scope_id=scope_id,
            tls_insecure=tls_insecure,
            token=token,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a BoundaryProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BoundaryProvider to import.
        :param import_from_id: The id of the existing BoundaryProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BoundaryProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc778755ea1ae165d642a9c02e4af74bc984663a807c91b55f9c54706b655068)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAuthMethodId")
    def reset_auth_method_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthMethodId", []))

    @jsii.member(jsii_name="resetAuthMethodLoginName")
    def reset_auth_method_login_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthMethodLoginName", []))

    @jsii.member(jsii_name="resetAuthMethodPassword")
    def reset_auth_method_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthMethodPassword", []))

    @jsii.member(jsii_name="resetPasswordAuthMethodLoginName")
    def reset_password_auth_method_login_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordAuthMethodLoginName", []))

    @jsii.member(jsii_name="resetPasswordAuthMethodPassword")
    def reset_password_auth_method_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordAuthMethodPassword", []))

    @jsii.member(jsii_name="resetPluginExecutionDir")
    def reset_plugin_execution_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginExecutionDir", []))

    @jsii.member(jsii_name="resetRecoveryKmsHcl")
    def reset_recovery_kms_hcl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryKmsHcl", []))

    @jsii.member(jsii_name="resetScopeId")
    def reset_scope_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopeId", []))

    @jsii.member(jsii_name="resetTlsInsecure")
    def reset_tls_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsInsecure", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="addrInput")
    def addr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addrInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="authMethodIdInput")
    def auth_method_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodIdInput"))

    @builtins.property
    @jsii.member(jsii_name="authMethodLoginNameInput")
    def auth_method_login_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodLoginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="authMethodPasswordInput")
    def auth_method_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordAuthMethodLoginNameInput")
    def password_auth_method_login_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordAuthMethodLoginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordAuthMethodPasswordInput")
    def password_auth_method_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordAuthMethodPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginExecutionDirInput")
    def plugin_execution_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginExecutionDirInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryKmsHclInput")
    def recovery_kms_hcl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryKmsHclInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInsecureInput")
    def tls_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="addr")
    def addr(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addr"))

    @addr.setter
    def addr(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a34d3d9d46934dfe3565814684b509ef8f26045ef5d92a3a822f85dfc9839d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e62e83f4ceb67a7e9dc9925f1564ef59ebdc11b116deff75e2ac6c1ebef83ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authMethodId")
    def auth_method_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodId"))

    @auth_method_id.setter
    def auth_method_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2725d022c2deea8b625155d570f7db08889b9e2501b025b8bcd3c0bb37333a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authMethodId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authMethodLoginName")
    def auth_method_login_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodLoginName"))

    @auth_method_login_name.setter
    def auth_method_login_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c1a2ef3122bc21ec37d300d33b2c01a908ff9b85c93c6934e4ca1de8aba1cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authMethodLoginName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authMethodPassword")
    def auth_method_password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodPassword"))

    @auth_method_password.setter
    def auth_method_password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01e0464f8b958da50ea13e286fab96f54ca1046db1b813376c776e314fb3d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authMethodPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordAuthMethodLoginName")
    def password_auth_method_login_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordAuthMethodLoginName"))

    @password_auth_method_login_name.setter
    def password_auth_method_login_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabd5c6761b8bcfcdfeab1c4614c3239afc5c5195cb0737e2c7a072f825ae1c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordAuthMethodLoginName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordAuthMethodPassword")
    def password_auth_method_password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordAuthMethodPassword"))

    @password_auth_method_password.setter
    def password_auth_method_password(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb9757d3fb77bebe1705c5c5bae845725893d4d6695b748681b2ae0bc5b414b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordAuthMethodPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginExecutionDir")
    def plugin_execution_dir(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginExecutionDir"))

    @plugin_execution_dir.setter
    def plugin_execution_dir(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af4795e9b151948888a32c0422833ccb29aa5bcc1f2f4e7e40d5b0091908946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginExecutionDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryKmsHcl")
    def recovery_kms_hcl(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryKmsHcl"))

    @recovery_kms_hcl.setter
    def recovery_kms_hcl(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c06b6ad9ad0ce2579d32d44fba48c214d823b7ae0408b23b18cbf711645cebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryKmsHcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05557cea268fa23feb8870c5ed10873ea583c37f6f4968d8b7fcf85f7d027bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsInsecure")
    def tls_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsInsecure"))

    @tls_insecure.setter
    def tls_insecure(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d45de75c3b0a644c867dc11ee56f568344787458407066bb12389c976f5b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec656c56dbf793fa88cec5837526fd62df33a6d74b7f9a54af2e3f7b3a0c6e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-boundary.provider.BoundaryProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "addr": "addr",
        "alias": "alias",
        "auth_method_id": "authMethodId",
        "auth_method_login_name": "authMethodLoginName",
        "auth_method_password": "authMethodPassword",
        "password_auth_method_login_name": "passwordAuthMethodLoginName",
        "password_auth_method_password": "passwordAuthMethodPassword",
        "plugin_execution_dir": "pluginExecutionDir",
        "recovery_kms_hcl": "recoveryKmsHcl",
        "scope_id": "scopeId",
        "tls_insecure": "tlsInsecure",
        "token": "token",
    },
)
class BoundaryProviderConfig:
    def __init__(
        self,
        *,
        addr: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        auth_method_id: typing.Optional[builtins.str] = None,
        auth_method_login_name: typing.Optional[builtins.str] = None,
        auth_method_password: typing.Optional[builtins.str] = None,
        password_auth_method_login_name: typing.Optional[builtins.str] = None,
        password_auth_method_password: typing.Optional[builtins.str] = None,
        plugin_execution_dir: typing.Optional[builtins.str] = None,
        recovery_kms_hcl: typing.Optional[builtins.str] = None,
        scope_id: typing.Optional[builtins.str] = None,
        tls_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param addr: The base url of the Boundary API, e.g. "http://127.0.0.1:9200". If not set, it will be read from the "BOUNDARY_ADDR" env var. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#addr BoundaryProvider#addr}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#alias BoundaryProvider#alias}
        :param auth_method_id: The auth method ID e.g. ampw_1234567890. If not set, the default auth method for the given scope ID will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#auth_method_id BoundaryProvider#auth_method_id}
        :param auth_method_login_name: The auth method login name for password-style or ldap-style auth methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#auth_method_login_name BoundaryProvider#auth_method_login_name}
        :param auth_method_password: The auth method password for password-style or ldap-style auth methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#auth_method_password BoundaryProvider#auth_method_password}
        :param password_auth_method_login_name: The auth method login name for password-style auth methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#password_auth_method_login_name BoundaryProvider#password_auth_method_login_name}
        :param password_auth_method_password: The auth method password for password-style auth methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#password_auth_method_password BoundaryProvider#password_auth_method_password}
        :param plugin_execution_dir: Specifies a directory that the Boundary provider can use to write and execute its built-in plugins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#plugin_execution_dir BoundaryProvider#plugin_execution_dir}
        :param recovery_kms_hcl: Can be a heredoc string or a path on disk. If set, the string/file will be parsed as HCL and used with the recovery KMS mechanism. While this is set, it will override any other authentication information; the KMS mechanism will always be used. See Boundary's KMS docs for examples: https://boundaryproject.io/docs/configuration/kms Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#recovery_kms_hcl BoundaryProvider#recovery_kms_hcl}
        :param scope_id: The scope ID for the default auth method. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#scope_id BoundaryProvider#scope_id}
        :param tls_insecure: When set to true, does not validate the Boundary API endpoint certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#tls_insecure BoundaryProvider#tls_insecure}
        :param token: The Boundary token to use, as a string or path on disk containing just the string. If set, the token read here will be used in place of authenticating with the auth method specified in "auth_method_id", although the recovery KMS mechanism will still override this. Can also be set with the BOUNDARY_TOKEN environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#token BoundaryProvider#token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb8f2baf8fdc05f14b99407eb26d4ce7c1d5cfdffa21ca1c28275218ffd85f4)
            check_type(argname="argument addr", value=addr, expected_type=type_hints["addr"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument auth_method_id", value=auth_method_id, expected_type=type_hints["auth_method_id"])
            check_type(argname="argument auth_method_login_name", value=auth_method_login_name, expected_type=type_hints["auth_method_login_name"])
            check_type(argname="argument auth_method_password", value=auth_method_password, expected_type=type_hints["auth_method_password"])
            check_type(argname="argument password_auth_method_login_name", value=password_auth_method_login_name, expected_type=type_hints["password_auth_method_login_name"])
            check_type(argname="argument password_auth_method_password", value=password_auth_method_password, expected_type=type_hints["password_auth_method_password"])
            check_type(argname="argument plugin_execution_dir", value=plugin_execution_dir, expected_type=type_hints["plugin_execution_dir"])
            check_type(argname="argument recovery_kms_hcl", value=recovery_kms_hcl, expected_type=type_hints["recovery_kms_hcl"])
            check_type(argname="argument scope_id", value=scope_id, expected_type=type_hints["scope_id"])
            check_type(argname="argument tls_insecure", value=tls_insecure, expected_type=type_hints["tls_insecure"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "addr": addr,
        }
        if alias is not None:
            self._values["alias"] = alias
        if auth_method_id is not None:
            self._values["auth_method_id"] = auth_method_id
        if auth_method_login_name is not None:
            self._values["auth_method_login_name"] = auth_method_login_name
        if auth_method_password is not None:
            self._values["auth_method_password"] = auth_method_password
        if password_auth_method_login_name is not None:
            self._values["password_auth_method_login_name"] = password_auth_method_login_name
        if password_auth_method_password is not None:
            self._values["password_auth_method_password"] = password_auth_method_password
        if plugin_execution_dir is not None:
            self._values["plugin_execution_dir"] = plugin_execution_dir
        if recovery_kms_hcl is not None:
            self._values["recovery_kms_hcl"] = recovery_kms_hcl
        if scope_id is not None:
            self._values["scope_id"] = scope_id
        if tls_insecure is not None:
            self._values["tls_insecure"] = tls_insecure
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def addr(self) -> builtins.str:
        '''The base url of the Boundary API, e.g. "http://127.0.0.1:9200". If not set, it will be read from the "BOUNDARY_ADDR" env var.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#addr BoundaryProvider#addr}
        '''
        result = self._values.get("addr")
        assert result is not None, "Required property 'addr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#alias BoundaryProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_method_id(self) -> typing.Optional[builtins.str]:
        '''The auth method ID e.g. ampw_1234567890. If not set, the default auth method for the given scope ID will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#auth_method_id BoundaryProvider#auth_method_id}
        '''
        result = self._values.get("auth_method_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_method_login_name(self) -> typing.Optional[builtins.str]:
        '''The auth method login name for password-style or ldap-style auth methods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#auth_method_login_name BoundaryProvider#auth_method_login_name}
        '''
        result = self._values.get("auth_method_login_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_method_password(self) -> typing.Optional[builtins.str]:
        '''The auth method password for password-style or ldap-style auth methods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#auth_method_password BoundaryProvider#auth_method_password}
        '''
        result = self._values.get("auth_method_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_auth_method_login_name(self) -> typing.Optional[builtins.str]:
        '''The auth method login name for password-style auth methods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#password_auth_method_login_name BoundaryProvider#password_auth_method_login_name}
        '''
        result = self._values.get("password_auth_method_login_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_auth_method_password(self) -> typing.Optional[builtins.str]:
        '''The auth method password for password-style auth methods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#password_auth_method_password BoundaryProvider#password_auth_method_password}
        '''
        result = self._values.get("password_auth_method_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_execution_dir(self) -> typing.Optional[builtins.str]:
        '''Specifies a directory that the Boundary provider can use to write and execute its built-in plugins.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#plugin_execution_dir BoundaryProvider#plugin_execution_dir}
        '''
        result = self._values.get("plugin_execution_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_kms_hcl(self) -> typing.Optional[builtins.str]:
        '''Can be a heredoc string or a path on disk.

        If set, the string/file will be parsed as HCL and used with the recovery KMS mechanism. While this is set, it will override any other authentication information; the KMS mechanism will always be used. See Boundary's KMS docs for examples: https://boundaryproject.io/docs/configuration/kms

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#recovery_kms_hcl BoundaryProvider#recovery_kms_hcl}
        '''
        result = self._values.get("recovery_kms_hcl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope_id(self) -> typing.Optional[builtins.str]:
        '''The scope ID for the default auth method.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#scope_id BoundaryProvider#scope_id}
        '''
        result = self._values.get("scope_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, does not validate the Boundary API endpoint certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#tls_insecure BoundaryProvider#tls_insecure}
        '''
        result = self._values.get("tls_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''The Boundary token to use, as a string or path on disk containing just the string.

        If set, the token read here will be used in place of authenticating with the auth method specified in "auth_method_id", although the recovery KMS mechanism will still override this. Can also be set with the BOUNDARY_TOKEN environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs#token BoundaryProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BoundaryProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BoundaryProvider",
    "BoundaryProviderConfig",
]

publication.publish()

def _typecheckingstub__ce45866643ede5c3f23dda6c62ba4515b4bf12276ac23bc01292aac21f883d15(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    addr: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    auth_method_id: typing.Optional[builtins.str] = None,
    auth_method_login_name: typing.Optional[builtins.str] = None,
    auth_method_password: typing.Optional[builtins.str] = None,
    password_auth_method_login_name: typing.Optional[builtins.str] = None,
    password_auth_method_password: typing.Optional[builtins.str] = None,
    plugin_execution_dir: typing.Optional[builtins.str] = None,
    recovery_kms_hcl: typing.Optional[builtins.str] = None,
    scope_id: typing.Optional[builtins.str] = None,
    tls_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc778755ea1ae165d642a9c02e4af74bc984663a807c91b55f9c54706b655068(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a34d3d9d46934dfe3565814684b509ef8f26045ef5d92a3a822f85dfc9839d3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e62e83f4ceb67a7e9dc9925f1564ef59ebdc11b116deff75e2ac6c1ebef83ce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2725d022c2deea8b625155d570f7db08889b9e2501b025b8bcd3c0bb37333a0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c1a2ef3122bc21ec37d300d33b2c01a908ff9b85c93c6934e4ca1de8aba1cb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01e0464f8b958da50ea13e286fab96f54ca1046db1b813376c776e314fb3d73(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabd5c6761b8bcfcdfeab1c4614c3239afc5c5195cb0737e2c7a072f825ae1c1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb9757d3fb77bebe1705c5c5bae845725893d4d6695b748681b2ae0bc5b414b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af4795e9b151948888a32c0422833ccb29aa5bcc1f2f4e7e40d5b0091908946(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c06b6ad9ad0ce2579d32d44fba48c214d823b7ae0408b23b18cbf711645cebf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05557cea268fa23feb8870c5ed10873ea583c37f6f4968d8b7fcf85f7d027bb9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d45de75c3b0a644c867dc11ee56f568344787458407066bb12389c976f5b3b(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec656c56dbf793fa88cec5837526fd62df33a6d74b7f9a54af2e3f7b3a0c6e07(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb8f2baf8fdc05f14b99407eb26d4ce7c1d5cfdffa21ca1c28275218ffd85f4(
    *,
    addr: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    auth_method_id: typing.Optional[builtins.str] = None,
    auth_method_login_name: typing.Optional[builtins.str] = None,
    auth_method_password: typing.Optional[builtins.str] = None,
    password_auth_method_login_name: typing.Optional[builtins.str] = None,
    password_auth_method_password: typing.Optional[builtins.str] = None,
    plugin_execution_dir: typing.Optional[builtins.str] = None,
    recovery_kms_hcl: typing.Optional[builtins.str] = None,
    scope_id: typing.Optional[builtins.str] = None,
    tls_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
