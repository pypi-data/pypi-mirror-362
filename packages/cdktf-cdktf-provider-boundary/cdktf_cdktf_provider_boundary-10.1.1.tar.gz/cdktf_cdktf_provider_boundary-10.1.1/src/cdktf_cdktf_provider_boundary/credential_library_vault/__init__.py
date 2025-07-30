r'''
# `boundary_credential_library_vault`

Refer to the Terraform Registry for docs: [`boundary_credential_library_vault`](https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault).
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


class CredentialLibraryVault(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-boundary.credentialLibraryVault.CredentialLibraryVault",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault boundary_credential_library_vault}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        credential_store_id: builtins.str,
        path: builtins.str,
        credential_mapping_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        credential_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http_method: typing.Optional[builtins.str] = None,
        http_request_body: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault boundary_credential_library_vault} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param credential_store_id: The ID of the credential store that this library belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#credential_store_id CredentialLibraryVault#credential_store_id}
        :param path: The path in Vault to request credentials from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#path CredentialLibraryVault#path}
        :param credential_mapping_overrides: The credential mapping override. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#credential_mapping_overrides CredentialLibraryVault#credential_mapping_overrides}
        :param credential_type: The type of credential the library generates. Cannot be updated on an existing resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#credential_type CredentialLibraryVault#credential_type}
        :param description: The Vault credential library description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#description CredentialLibraryVault#description}
        :param http_method: The HTTP method the library uses when requesting credentials from Vault. Defaults to 'GET'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#http_method CredentialLibraryVault#http_method}
        :param http_request_body: The body of the HTTP request the library sends to Vault when requesting credentials. Only valid if ``http_method`` is set to ``POST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#http_request_body CredentialLibraryVault#http_request_body}
        :param name: The Vault credential library name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#name CredentialLibraryVault#name}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7794ad7b86d45c1549eee6068bb23a8a71281ae30b02bdf7759399adcd109c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = CredentialLibraryVaultConfig(
            credential_store_id=credential_store_id,
            path=path,
            credential_mapping_overrides=credential_mapping_overrides,
            credential_type=credential_type,
            description=description,
            http_method=http_method,
            http_request_body=http_request_body,
            name=name,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
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
        '''Generates CDKTF code for importing a CredentialLibraryVault resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CredentialLibraryVault to import.
        :param import_from_id: The id of the existing CredentialLibraryVault that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CredentialLibraryVault to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548a9299fa73b6bffba1d98163168cbb8eb654f38a54e99e4d80161085c8bc49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCredentialMappingOverrides")
    def reset_credential_mapping_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialMappingOverrides", []))

    @jsii.member(jsii_name="resetCredentialType")
    def reset_credential_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHttpMethod")
    def reset_http_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethod", []))

    @jsii.member(jsii_name="resetHttpRequestBody")
    def reset_http_request_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRequestBody", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="credentialMappingOverridesInput")
    def credential_mapping_overrides_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "credentialMappingOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialStoreIdInput")
    def credential_store_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialStoreIdInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialTypeInput")
    def credential_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRequestBodyInput")
    def http_request_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpRequestBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialMappingOverrides")
    def credential_mapping_overrides(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "credentialMappingOverrides"))

    @credential_mapping_overrides.setter
    def credential_mapping_overrides(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b1da054770468b1b93f778449e0705f34918017edc84a8e8fb3f82fec4340ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialMappingOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialStoreId")
    def credential_store_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialStoreId"))

    @credential_store_id.setter
    def credential_store_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b19a9ee74cf98c706bd7e31f270aa6b2ae1a875454ddb1ebd1cfc1515ebfc837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialStoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialType")
    def credential_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialType"))

    @credential_type.setter
    def credential_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7f498fbcd7f005d9bf2a2b81957ef6b9ab9b6c5f40dbfdccd4f17fc7bf1e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1170caa0d4a050767ebb5e75606dd4c2dfbf113a9960b639cf657a5b5ca157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76ab3fc20767eeff4ca9c934b3ee3334ddee04ab4b03dd03fc468e892753407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpRequestBody")
    def http_request_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpRequestBody"))

    @http_request_body.setter
    def http_request_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce6ae762b960b6b94adae7421faefe990ffcf11b9436a3243f88e3ba4cb2c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpRequestBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55eaa9aaad7395b145b67dd84840c5472604e77694921a884412d77a07b4cfcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2043a0e4a187bb2d65a5e9154b89020d9a22c2ece2c185c7bba875f0d958886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-boundary.credentialLibraryVault.CredentialLibraryVaultConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "credential_store_id": "credentialStoreId",
        "path": "path",
        "credential_mapping_overrides": "credentialMappingOverrides",
        "credential_type": "credentialType",
        "description": "description",
        "http_method": "httpMethod",
        "http_request_body": "httpRequestBody",
        "name": "name",
    },
)
class CredentialLibraryVaultConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        credential_store_id: builtins.str,
        path: builtins.str,
        credential_mapping_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        credential_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http_method: typing.Optional[builtins.str] = None,
        http_request_body: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param credential_store_id: The ID of the credential store that this library belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#credential_store_id CredentialLibraryVault#credential_store_id}
        :param path: The path in Vault to request credentials from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#path CredentialLibraryVault#path}
        :param credential_mapping_overrides: The credential mapping override. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#credential_mapping_overrides CredentialLibraryVault#credential_mapping_overrides}
        :param credential_type: The type of credential the library generates. Cannot be updated on an existing resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#credential_type CredentialLibraryVault#credential_type}
        :param description: The Vault credential library description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#description CredentialLibraryVault#description}
        :param http_method: The HTTP method the library uses when requesting credentials from Vault. Defaults to 'GET'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#http_method CredentialLibraryVault#http_method}
        :param http_request_body: The body of the HTTP request the library sends to Vault when requesting credentials. Only valid if ``http_method`` is set to ``POST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#http_request_body CredentialLibraryVault#http_request_body}
        :param name: The Vault credential library name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#name CredentialLibraryVault#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91de0f894b7ba615dddb6aca0eb531c0b3eb874ab7cf11ccd93bc0005f9d79fb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument credential_store_id", value=credential_store_id, expected_type=type_hints["credential_store_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument credential_mapping_overrides", value=credential_mapping_overrides, expected_type=type_hints["credential_mapping_overrides"])
            check_type(argname="argument credential_type", value=credential_type, expected_type=type_hints["credential_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument http_request_body", value=http_request_body, expected_type=type_hints["http_request_body"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credential_store_id": credential_store_id,
            "path": path,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if credential_mapping_overrides is not None:
            self._values["credential_mapping_overrides"] = credential_mapping_overrides
        if credential_type is not None:
            self._values["credential_type"] = credential_type
        if description is not None:
            self._values["description"] = description
        if http_method is not None:
            self._values["http_method"] = http_method
        if http_request_body is not None:
            self._values["http_request_body"] = http_request_body
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def credential_store_id(self) -> builtins.str:
        '''The ID of the credential store that this library belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#credential_store_id CredentialLibraryVault#credential_store_id}
        '''
        result = self._values.get("credential_store_id")
        assert result is not None, "Required property 'credential_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path in Vault to request credentials from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#path CredentialLibraryVault#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credential_mapping_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The credential mapping override.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#credential_mapping_overrides CredentialLibraryVault#credential_mapping_overrides}
        '''
        result = self._values.get("credential_mapping_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def credential_type(self) -> typing.Optional[builtins.str]:
        '''The type of credential the library generates. Cannot be updated on an existing resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#credential_type CredentialLibraryVault#credential_type}
        '''
        result = self._values.get("credential_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The Vault credential library description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#description CredentialLibraryVault#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''The HTTP method the library uses when requesting credentials from Vault. Defaults to 'GET'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#http_method CredentialLibraryVault#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_request_body(self) -> typing.Optional[builtins.str]:
        '''The body of the HTTP request the library sends to Vault when requesting credentials.

        Only valid if ``http_method`` is set to ``POST``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#http_request_body CredentialLibraryVault#http_request_body}
        '''
        result = self._values.get("http_request_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The Vault credential library name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault#name CredentialLibraryVault#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CredentialLibraryVaultConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CredentialLibraryVault",
    "CredentialLibraryVaultConfig",
]

publication.publish()

def _typecheckingstub__4d7794ad7b86d45c1549eee6068bb23a8a71281ae30b02bdf7759399adcd109c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    credential_store_id: builtins.str,
    path: builtins.str,
    credential_mapping_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    credential_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[builtins.str] = None,
    http_request_body: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548a9299fa73b6bffba1d98163168cbb8eb654f38a54e99e4d80161085c8bc49(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1da054770468b1b93f778449e0705f34918017edc84a8e8fb3f82fec4340ce(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19a9ee74cf98c706bd7e31f270aa6b2ae1a875454ddb1ebd1cfc1515ebfc837(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7f498fbcd7f005d9bf2a2b81957ef6b9ab9b6c5f40dbfdccd4f17fc7bf1e63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1170caa0d4a050767ebb5e75606dd4c2dfbf113a9960b639cf657a5b5ca157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76ab3fc20767eeff4ca9c934b3ee3334ddee04ab4b03dd03fc468e892753407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce6ae762b960b6b94adae7421faefe990ffcf11b9436a3243f88e3ba4cb2c7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55eaa9aaad7395b145b67dd84840c5472604e77694921a884412d77a07b4cfcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2043a0e4a187bb2d65a5e9154b89020d9a22c2ece2c185c7bba875f0d958886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91de0f894b7ba615dddb6aca0eb531c0b3eb874ab7cf11ccd93bc0005f9d79fb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    credential_store_id: builtins.str,
    path: builtins.str,
    credential_mapping_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    credential_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[builtins.str] = None,
    http_request_body: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
