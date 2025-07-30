r'''
# `boundary_credential_library_vault_ssh_certificate`

Refer to the Terraform Registry for docs: [`boundary_credential_library_vault_ssh_certificate`](https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate).
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


class CredentialLibraryVaultSshCertificate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-boundary.credentialLibraryVaultSshCertificate.CredentialLibraryVaultSshCertificate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate boundary_credential_library_vault_ssh_certificate}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        credential_store_id: builtins.str,
        path: builtins.str,
        username: builtins.str,
        additional_valid_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        critical_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        extensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        key_bits: typing.Optional[jsii.Number] = None,
        key_id: typing.Optional[builtins.str] = None,
        key_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate boundary_credential_library_vault_ssh_certificate} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param credential_store_id: The ID of the credential store that this library belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#credential_store_id CredentialLibraryVaultSshCertificate#credential_store_id}
        :param path: The path in Vault to request credentials from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#path CredentialLibraryVaultSshCertificate#path}
        :param username: The username to use with the certificate returned by the library. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#username CredentialLibraryVaultSshCertificate#username}
        :param additional_valid_principals: Principals to be signed as "valid_principles" in addition to username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#additional_valid_principals CredentialLibraryVaultSshCertificate#additional_valid_principals}
        :param critical_options: Specifies a map of the critical options that the certificate should be signed for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#critical_options CredentialLibraryVaultSshCertificate#critical_options}
        :param description: The Vault credential library description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#description CredentialLibraryVaultSshCertificate#description}
        :param extensions: Specifies a map of the extensions that the certificate should be signed for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#extensions CredentialLibraryVaultSshCertificate#extensions}
        :param key_bits: Specifies the number of bits to use for the generated keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#key_bits CredentialLibraryVaultSshCertificate#key_bits}
        :param key_id: Specifies the key id a certificate should have. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#key_id CredentialLibraryVaultSshCertificate#key_id}
        :param key_type: Specifies the desired key type; must be ed25519, ecdsa, or rsa. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#key_type CredentialLibraryVaultSshCertificate#key_type}
        :param name: The Vault credential library name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#name CredentialLibraryVaultSshCertificate#name}
        :param ttl: Specifies the requested time to live for a certificate returned from the library. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#ttl CredentialLibraryVaultSshCertificate#ttl}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69aad12352e98817e6f00f37ecc3de8039fa7c57cb9b850547942c06204e5ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = CredentialLibraryVaultSshCertificateConfig(
            credential_store_id=credential_store_id,
            path=path,
            username=username,
            additional_valid_principals=additional_valid_principals,
            critical_options=critical_options,
            description=description,
            extensions=extensions,
            key_bits=key_bits,
            key_id=key_id,
            key_type=key_type,
            name=name,
            ttl=ttl,
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
        '''Generates CDKTF code for importing a CredentialLibraryVaultSshCertificate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CredentialLibraryVaultSshCertificate to import.
        :param import_from_id: The id of the existing CredentialLibraryVaultSshCertificate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CredentialLibraryVaultSshCertificate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7190fe129cf76728c675704972f411f78fd326b467bff93be73661374f92bf19)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAdditionalValidPrincipals")
    def reset_additional_valid_principals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalValidPrincipals", []))

    @jsii.member(jsii_name="resetCriticalOptions")
    def reset_critical_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCriticalOptions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExtensions")
    def reset_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtensions", []))

    @jsii.member(jsii_name="resetKeyBits")
    def reset_key_bits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyBits", []))

    @jsii.member(jsii_name="resetKeyId")
    def reset_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyId", []))

    @jsii.member(jsii_name="resetKeyType")
    def reset_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyType", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

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
    @jsii.member(jsii_name="additionalValidPrincipalsInput")
    def additional_valid_principals_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalValidPrincipalsInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialStoreIdInput")
    def credential_store_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialStoreIdInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalOptionsInput")
    def critical_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "criticalOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionsInput")
    def extensions_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyBitsInput")
    def key_bits_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keyBitsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyIdInput")
    def key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyTypeInput")
    def key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalValidPrincipals")
    def additional_valid_principals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalValidPrincipals"))

    @additional_valid_principals.setter
    def additional_valid_principals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b451c90271f26b94aeb33db6857b20237faba918296321a3b39077a79d4665e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalValidPrincipals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialStoreId")
    def credential_store_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialStoreId"))

    @credential_store_id.setter
    def credential_store_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c02a22621103de34ff003ad4d58f9d3e3c03f32b0b776e8d8259434590ddd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialStoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="criticalOptions")
    def critical_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "criticalOptions"))

    @critical_options.setter
    def critical_options(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d27f7313d3ddeebee89dbd2a0a19c647bcdb31f73f8ae8be3a041f17ca22a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criticalOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f8e85b15c7fc149b21d81746d9dcdb8775d0619ee9db18ade7a24fb7141bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extensions")
    def extensions(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extensions"))

    @extensions.setter
    def extensions(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e637c9d8f30ef67de587d8d4c70cb4777e140453beefdd67c32f1d8591f7fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyBits")
    def key_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyBits"))

    @key_bits.setter
    def key_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84aa62192db123f13385a72f7077c278c8e37425aeb462216bc12053ea37123b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyBits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @key_id.setter
    def key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fbc3913b2f08bba412e6d2c4f6929ba4d2ff27b4a7dcd7279866823d5a7a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyType")
    def key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyType"))

    @key_type.setter
    def key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb33b5dd3582fe2eef5f82f734b0a3bc732a50342e3437ca89eb3eda7aab0b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1a5c8862589a124db250072f7d5aee9191ca1b4d49e72cc9023576a2f35e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4557441c4dfd179ec3b4e8d697e33c60260926113dc3618d44cdb1b143ad9904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc7720603e9543c3026f8eb217276341482ebd273147afc4ca1597878e36395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b55a9586af7cc5e911f0c64e83f79a5c47f14cb105c5711fe4d530fa528095aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-boundary.credentialLibraryVaultSshCertificate.CredentialLibraryVaultSshCertificateConfig",
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
        "username": "username",
        "additional_valid_principals": "additionalValidPrincipals",
        "critical_options": "criticalOptions",
        "description": "description",
        "extensions": "extensions",
        "key_bits": "keyBits",
        "key_id": "keyId",
        "key_type": "keyType",
        "name": "name",
        "ttl": "ttl",
    },
)
class CredentialLibraryVaultSshCertificateConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        username: builtins.str,
        additional_valid_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        critical_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        extensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        key_bits: typing.Optional[jsii.Number] = None,
        key_id: typing.Optional[builtins.str] = None,
        key_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param credential_store_id: The ID of the credential store that this library belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#credential_store_id CredentialLibraryVaultSshCertificate#credential_store_id}
        :param path: The path in Vault to request credentials from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#path CredentialLibraryVaultSshCertificate#path}
        :param username: The username to use with the certificate returned by the library. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#username CredentialLibraryVaultSshCertificate#username}
        :param additional_valid_principals: Principals to be signed as "valid_principles" in addition to username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#additional_valid_principals CredentialLibraryVaultSshCertificate#additional_valid_principals}
        :param critical_options: Specifies a map of the critical options that the certificate should be signed for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#critical_options CredentialLibraryVaultSshCertificate#critical_options}
        :param description: The Vault credential library description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#description CredentialLibraryVaultSshCertificate#description}
        :param extensions: Specifies a map of the extensions that the certificate should be signed for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#extensions CredentialLibraryVaultSshCertificate#extensions}
        :param key_bits: Specifies the number of bits to use for the generated keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#key_bits CredentialLibraryVaultSshCertificate#key_bits}
        :param key_id: Specifies the key id a certificate should have. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#key_id CredentialLibraryVaultSshCertificate#key_id}
        :param key_type: Specifies the desired key type; must be ed25519, ecdsa, or rsa. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#key_type CredentialLibraryVaultSshCertificate#key_type}
        :param name: The Vault credential library name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#name CredentialLibraryVaultSshCertificate#name}
        :param ttl: Specifies the requested time to live for a certificate returned from the library. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#ttl CredentialLibraryVaultSshCertificate#ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a8dcdd30946ca78931edfad9b73c37ebdc6bbf6b64db6c12efef586c5bdaeb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument credential_store_id", value=credential_store_id, expected_type=type_hints["credential_store_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument additional_valid_principals", value=additional_valid_principals, expected_type=type_hints["additional_valid_principals"])
            check_type(argname="argument critical_options", value=critical_options, expected_type=type_hints["critical_options"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument extensions", value=extensions, expected_type=type_hints["extensions"])
            check_type(argname="argument key_bits", value=key_bits, expected_type=type_hints["key_bits"])
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credential_store_id": credential_store_id,
            "path": path,
            "username": username,
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
        if additional_valid_principals is not None:
            self._values["additional_valid_principals"] = additional_valid_principals
        if critical_options is not None:
            self._values["critical_options"] = critical_options
        if description is not None:
            self._values["description"] = description
        if extensions is not None:
            self._values["extensions"] = extensions
        if key_bits is not None:
            self._values["key_bits"] = key_bits
        if key_id is not None:
            self._values["key_id"] = key_id
        if key_type is not None:
            self._values["key_type"] = key_type
        if name is not None:
            self._values["name"] = name
        if ttl is not None:
            self._values["ttl"] = ttl

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#credential_store_id CredentialLibraryVaultSshCertificate#credential_store_id}
        '''
        result = self._values.get("credential_store_id")
        assert result is not None, "Required property 'credential_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path in Vault to request credentials from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#path CredentialLibraryVaultSshCertificate#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username to use with the certificate returned by the library.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#username CredentialLibraryVaultSshCertificate#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_valid_principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Principals to be signed as "valid_principles" in addition to username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#additional_valid_principals CredentialLibraryVaultSshCertificate#additional_valid_principals}
        '''
        result = self._values.get("additional_valid_principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def critical_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Specifies a map of the critical options that the certificate should be signed for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#critical_options CredentialLibraryVaultSshCertificate#critical_options}
        '''
        result = self._values.get("critical_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The Vault credential library description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#description CredentialLibraryVaultSshCertificate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extensions(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Specifies a map of the extensions that the certificate should be signed for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#extensions CredentialLibraryVaultSshCertificate#extensions}
        '''
        result = self._values.get("extensions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def key_bits(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of bits to use for the generated keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#key_bits CredentialLibraryVaultSshCertificate#key_bits}
        '''
        result = self._values.get("key_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def key_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the key id a certificate should have.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#key_id CredentialLibraryVaultSshCertificate#key_id}
        '''
        result = self._values.get("key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the desired key type; must be ed25519, ecdsa, or rsa.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#key_type CredentialLibraryVaultSshCertificate#key_type}
        '''
        result = self._values.get("key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The Vault credential library name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#name CredentialLibraryVaultSshCertificate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''Specifies the requested time to live for a certificate returned from the library.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/credential_library_vault_ssh_certificate#ttl CredentialLibraryVaultSshCertificate#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CredentialLibraryVaultSshCertificateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CredentialLibraryVaultSshCertificate",
    "CredentialLibraryVaultSshCertificateConfig",
]

publication.publish()

def _typecheckingstub__f69aad12352e98817e6f00f37ecc3de8039fa7c57cb9b850547942c06204e5ee(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    credential_store_id: builtins.str,
    path: builtins.str,
    username: builtins.str,
    additional_valid_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    critical_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    extensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    key_bits: typing.Optional[jsii.Number] = None,
    key_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__7190fe129cf76728c675704972f411f78fd326b467bff93be73661374f92bf19(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b451c90271f26b94aeb33db6857b20237faba918296321a3b39077a79d4665e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c02a22621103de34ff003ad4d58f9d3e3c03f32b0b776e8d8259434590ddd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d27f7313d3ddeebee89dbd2a0a19c647bcdb31f73f8ae8be3a041f17ca22a2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f8e85b15c7fc149b21d81746d9dcdb8775d0619ee9db18ade7a24fb7141bc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e637c9d8f30ef67de587d8d4c70cb4777e140453beefdd67c32f1d8591f7fb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84aa62192db123f13385a72f7077c278c8e37425aeb462216bc12053ea37123b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fbc3913b2f08bba412e6d2c4f6929ba4d2ff27b4a7dcd7279866823d5a7a5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb33b5dd3582fe2eef5f82f734b0a3bc732a50342e3437ca89eb3eda7aab0b5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1a5c8862589a124db250072f7d5aee9191ca1b4d49e72cc9023576a2f35e79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4557441c4dfd179ec3b4e8d697e33c60260926113dc3618d44cdb1b143ad9904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc7720603e9543c3026f8eb217276341482ebd273147afc4ca1597878e36395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55a9586af7cc5e911f0c64e83f79a5c47f14cb105c5711fe4d530fa528095aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a8dcdd30946ca78931edfad9b73c37ebdc6bbf6b64db6c12efef586c5bdaeb(
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
    username: builtins.str,
    additional_valid_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    critical_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    extensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    key_bits: typing.Optional[jsii.Number] = None,
    key_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
