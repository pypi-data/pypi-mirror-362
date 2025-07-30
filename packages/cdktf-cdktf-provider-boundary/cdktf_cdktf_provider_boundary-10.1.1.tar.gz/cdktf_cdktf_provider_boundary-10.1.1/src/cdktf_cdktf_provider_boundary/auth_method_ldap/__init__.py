r'''
# `boundary_auth_method_ldap`

Refer to the Terraform Registry for docs: [`boundary_auth_method_ldap`](https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap).
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


class AuthMethodLdap(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-boundary.authMethodLdap.AuthMethodLdap",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap boundary_auth_method_ldap}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        account_attribute_maps: typing.Optional[typing.Sequence[builtins.str]] = None,
        anon_group_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bind_dn: typing.Optional[builtins.str] = None,
        bind_password: typing.Optional[builtins.str] = None,
        bind_password_hmac: typing.Optional[builtins.str] = None,
        certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_certificate_key: typing.Optional[builtins.str] = None,
        client_certificate_key_hmac: typing.Optional[builtins.str] = None,
        dereference_aliases: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        discover_dn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_attr: typing.Optional[builtins.str] = None,
        group_dn: typing.Optional[builtins.str] = None,
        group_filter: typing.Optional[builtins.str] = None,
        insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_primary_for_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maximum_page_size: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        start_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        state: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        upn_domain: typing.Optional[builtins.str] = None,
        urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_attr: typing.Optional[builtins.str] = None,
        user_dn: typing.Optional[builtins.str] = None,
        user_filter: typing.Optional[builtins.str] = None,
        use_token_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap boundary_auth_method_ldap} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#scope_id AuthMethodLdap#scope_id}
        :param account_attribute_maps: Account attribute maps fullname and email. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#account_attribute_maps AuthMethodLdap#account_attribute_maps}
        :param anon_group_search: Use anon bind when performing LDAP group searches (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#anon_group_search AuthMethodLdap#anon_group_search}
        :param bind_dn: The distinguished name of entry to bind when performing user and group searches (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#bind_dn AuthMethodLdap#bind_dn}
        :param bind_password: The password to use along with bind-dn performing user and group searches (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#bind_password AuthMethodLdap#bind_password}
        :param bind_password_hmac: The HMAC of the bind password returned by the Boundary controller, which is used for comparison after initial setting of the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#bind_password_hmac AuthMethodLdap#bind_password_hmac}
        :param certificates: PEM-encoded X.509 CA certificate in ASN.1 DER form that can be used as a trust anchor when connecting to an LDAP server(optional). This may be specified multiple times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#certificates AuthMethodLdap#certificates}
        :param client_certificate: PEM-encoded X.509 client certificate in ASN.1 DER form that can be used to authenticate against an LDAP server(optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#client_certificate AuthMethodLdap#client_certificate}
        :param client_certificate_key: PEM-encoded X.509 client certificate key in PKCS #8, ASN.1 DER form used with the client certificate (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#client_certificate_key AuthMethodLdap#client_certificate_key}
        :param client_certificate_key_hmac: The HMAC of the client certificate key returned by the Boundary controller, which is used for comparison after initial setting of the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#client_certificate_key_hmac AuthMethodLdap#client_certificate_key_hmac}
        :param dereference_aliases: Control how aliases are dereferenced when performing the search. Can be one of: NeverDerefAliases, DerefInSearching, DerefFindingBaseObj, and DerefAlways (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#dereference_aliases AuthMethodLdap#dereference_aliases}
        :param description: The auth method description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#description AuthMethodLdap#description}
        :param discover_dn: Use anon bind to discover the bind DN of a user (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#discover_dn AuthMethodLdap#discover_dn}
        :param enable_groups: Find the authenticated user's groups during authentication (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#enable_groups AuthMethodLdap#enable_groups}
        :param group_attr: The attribute that enumerates a user's group membership from entries returned by a group search (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#group_attr AuthMethodLdap#group_attr}
        :param group_dn: The base DN under which to perform group search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#group_dn AuthMethodLdap#group_dn}
        :param group_filter: A go template used to construct a LDAP group search filter (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#group_filter AuthMethodLdap#group_filter}
        :param insecure_tls: Skip the LDAP server SSL certificate validation (optional) - insecure and use with caution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#insecure_tls AuthMethodLdap#insecure_tls}
        :param is_primary_for_scope: When true, makes this auth method the primary auth method for the scope in which it resides. The primary auth method for a scope means the the user will be automatically created when they login using an LDAP account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#is_primary_for_scope AuthMethodLdap#is_primary_for_scope}
        :param maximum_page_size: MaximumPageSize specifies a maximum search result size to use when retrieving the authenticated user's groups (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#maximum_page_size AuthMethodLdap#maximum_page_size}
        :param name: The auth method name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#name AuthMethodLdap#name}
        :param start_tls: Issue StartTLS command after connecting (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#start_tls AuthMethodLdap#start_tls}
        :param state: Can be one of 'inactive', 'active-private', or 'active-public'. Defaults to active-public. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#state AuthMethodLdap#state}
        :param type: The type of auth method; hardcoded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#type AuthMethodLdap#type}
        :param upn_domain: The userPrincipalDomain used to construct the UPN string for the authenticating user (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#upn_domain AuthMethodLdap#upn_domain}
        :param urls: The LDAP URLs that specify LDAP servers to connect to (required). May be specified multiple times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#urls AuthMethodLdap#urls}
        :param user_attr: The attribute on user entry matching the username passed when authenticating (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#user_attr AuthMethodLdap#user_attr}
        :param user_dn: The base DN under which to perform user search (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#user_dn AuthMethodLdap#user_dn}
        :param user_filter: A go template used to construct a LDAP user search filter (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#user_filter AuthMethodLdap#user_filter}
        :param use_token_groups: Use the Active Directory tokenGroups constructed attribute of the user to find the group memberships (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#use_token_groups AuthMethodLdap#use_token_groups}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81df91e74f7309d44b4335008d4adbdb6ab75f49ef810a5b5d3cb7bb491fefc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AuthMethodLdapConfig(
            scope_id=scope_id,
            account_attribute_maps=account_attribute_maps,
            anon_group_search=anon_group_search,
            bind_dn=bind_dn,
            bind_password=bind_password,
            bind_password_hmac=bind_password_hmac,
            certificates=certificates,
            client_certificate=client_certificate,
            client_certificate_key=client_certificate_key,
            client_certificate_key_hmac=client_certificate_key_hmac,
            dereference_aliases=dereference_aliases,
            description=description,
            discover_dn=discover_dn,
            enable_groups=enable_groups,
            group_attr=group_attr,
            group_dn=group_dn,
            group_filter=group_filter,
            insecure_tls=insecure_tls,
            is_primary_for_scope=is_primary_for_scope,
            maximum_page_size=maximum_page_size,
            name=name,
            start_tls=start_tls,
            state=state,
            type=type,
            upn_domain=upn_domain,
            urls=urls,
            user_attr=user_attr,
            user_dn=user_dn,
            user_filter=user_filter,
            use_token_groups=use_token_groups,
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
        '''Generates CDKTF code for importing a AuthMethodLdap resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AuthMethodLdap to import.
        :param import_from_id: The id of the existing AuthMethodLdap that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AuthMethodLdap to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db66f29195e83a62225dbcf5f20f7b5cd76cd2a0b42855af0532de7169c81b10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccountAttributeMaps")
    def reset_account_attribute_maps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountAttributeMaps", []))

    @jsii.member(jsii_name="resetAnonGroupSearch")
    def reset_anon_group_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnonGroupSearch", []))

    @jsii.member(jsii_name="resetBindDn")
    def reset_bind_dn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBindDn", []))

    @jsii.member(jsii_name="resetBindPassword")
    def reset_bind_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBindPassword", []))

    @jsii.member(jsii_name="resetBindPasswordHmac")
    def reset_bind_password_hmac(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBindPasswordHmac", []))

    @jsii.member(jsii_name="resetCertificates")
    def reset_certificates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificates", []))

    @jsii.member(jsii_name="resetClientCertificate")
    def reset_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificate", []))

    @jsii.member(jsii_name="resetClientCertificateKey")
    def reset_client_certificate_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateKey", []))

    @jsii.member(jsii_name="resetClientCertificateKeyHmac")
    def reset_client_certificate_key_hmac(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateKeyHmac", []))

    @jsii.member(jsii_name="resetDereferenceAliases")
    def reset_dereference_aliases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDereferenceAliases", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiscoverDn")
    def reset_discover_dn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscoverDn", []))

    @jsii.member(jsii_name="resetEnableGroups")
    def reset_enable_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableGroups", []))

    @jsii.member(jsii_name="resetGroupAttr")
    def reset_group_attr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupAttr", []))

    @jsii.member(jsii_name="resetGroupDn")
    def reset_group_dn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupDn", []))

    @jsii.member(jsii_name="resetGroupFilter")
    def reset_group_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupFilter", []))

    @jsii.member(jsii_name="resetInsecureTls")
    def reset_insecure_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureTls", []))

    @jsii.member(jsii_name="resetIsPrimaryForScope")
    def reset_is_primary_for_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsPrimaryForScope", []))

    @jsii.member(jsii_name="resetMaximumPageSize")
    def reset_maximum_page_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumPageSize", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetStartTls")
    def reset_start_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTls", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUpnDomain")
    def reset_upn_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpnDomain", []))

    @jsii.member(jsii_name="resetUrls")
    def reset_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrls", []))

    @jsii.member(jsii_name="resetUserAttr")
    def reset_user_attr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAttr", []))

    @jsii.member(jsii_name="resetUserDn")
    def reset_user_dn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDn", []))

    @jsii.member(jsii_name="resetUserFilter")
    def reset_user_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserFilter", []))

    @jsii.member(jsii_name="resetUseTokenGroups")
    def reset_use_token_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseTokenGroups", []))

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
    @jsii.member(jsii_name="accountAttributeMapsInput")
    def account_attribute_maps_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountAttributeMapsInput"))

    @builtins.property
    @jsii.member(jsii_name="anonGroupSearchInput")
    def anon_group_search_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "anonGroupSearchInput"))

    @builtins.property
    @jsii.member(jsii_name="bindDnInput")
    def bind_dn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bindDnInput"))

    @builtins.property
    @jsii.member(jsii_name="bindPasswordHmacInput")
    def bind_password_hmac_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bindPasswordHmacInput"))

    @builtins.property
    @jsii.member(jsii_name="bindPasswordInput")
    def bind_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bindPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatesInput")
    def certificates_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificatesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateKeyHmacInput")
    def client_certificate_key_hmac_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateKeyHmacInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateKeyInput")
    def client_certificate_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="dereferenceAliasesInput")
    def dereference_aliases_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dereferenceAliasesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="discoverDnInput")
    def discover_dn_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "discoverDnInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGroupsInput")
    def enable_groups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupAttrInput")
    def group_attr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupAttrInput"))

    @builtins.property
    @jsii.member(jsii_name="groupDnInput")
    def group_dn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupDnInput"))

    @builtins.property
    @jsii.member(jsii_name="groupFilterInput")
    def group_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureTlsInput")
    def insecure_tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="isPrimaryForScopeInput")
    def is_primary_for_scope_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isPrimaryForScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumPageSizeInput")
    def maximum_page_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumPageSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="startTlsInput")
    def start_tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="upnDomainInput")
    def upn_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "upnDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="urlsInput")
    def urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urlsInput"))

    @builtins.property
    @jsii.member(jsii_name="userAttrInput")
    def user_attr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAttrInput"))

    @builtins.property
    @jsii.member(jsii_name="userDnInput")
    def user_dn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDnInput"))

    @builtins.property
    @jsii.member(jsii_name="userFilterInput")
    def user_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="useTokenGroupsInput")
    def use_token_groups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useTokenGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountAttributeMaps")
    def account_attribute_maps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountAttributeMaps"))

    @account_attribute_maps.setter
    def account_attribute_maps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8320960f700bfb54157c064ecbc0a07bd2f7a791ca88a06366e8dc80d526c757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountAttributeMaps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="anonGroupSearch")
    def anon_group_search(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "anonGroupSearch"))

    @anon_group_search.setter
    def anon_group_search(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a20afa16a45c8486ba9839ef8469d01d0cffdd15e4f0818c575aac9a1b6f4d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anonGroupSearch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bindDn")
    def bind_dn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bindDn"))

    @bind_dn.setter
    def bind_dn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca478227f5e6c5a16b4efa937650d35af3ed65f45606a1ef3e3e2ebca4531a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bindDn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bindPassword")
    def bind_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bindPassword"))

    @bind_password.setter
    def bind_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562de4f13fb1899d00990b3d6662720ba910501d9fe55fe073477decd0677c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bindPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bindPasswordHmac")
    def bind_password_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bindPasswordHmac"))

    @bind_password_hmac.setter
    def bind_password_hmac(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5296cd77c36c442cc8a0129b1c91a8b25d4a88a49da280e8d89bc4f35c8218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bindPasswordHmac", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificates")
    def certificates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificates"))

    @certificates.setter
    def certificates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c63ff0bc85620263ee2563e74be65c31e1ff87e37d6e5553f41697783ef8a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc420167ebfefb413a534405c5533fd465a71524077b94a27edfd9d2924ab554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateKey")
    def client_certificate_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateKey"))

    @client_certificate_key.setter
    def client_certificate_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f84e59e0854cfe11209c5cf151190476b6241abad494868599582e4648a6f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateKeyHmac")
    def client_certificate_key_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateKeyHmac"))

    @client_certificate_key_hmac.setter
    def client_certificate_key_hmac(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0933104f1d49b756de962badbd38cec0e5cf49fec4409c21f78fcedce27a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateKeyHmac", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dereferenceAliases")
    def dereference_aliases(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dereferenceAliases"))

    @dereference_aliases.setter
    def dereference_aliases(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1201919c1cae34720958313cc692e07635cfa580b756b614f791abb80568b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dereferenceAliases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc34aa93629cd42d132def40529a95379ad9e90d44571a255700a63ff2e6d497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="discoverDn")
    def discover_dn(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "discoverDn"))

    @discover_dn.setter
    def discover_dn(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cb7ed28fa4a0116bf0b5f0b91bef473a27b3fdd1d716b733e1c8935863e536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discoverDn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableGroups")
    def enable_groups(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableGroups"))

    @enable_groups.setter
    def enable_groups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787668195e9afe5ce1177e38e1361c782e68b20fdec55494abf504a01d2257fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupAttr")
    def group_attr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupAttr"))

    @group_attr.setter
    def group_attr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a8ac0c2988a04f2bbd1b144fbbf7a2f89336a9317ac7983453299f5b10308c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupAttr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupDn")
    def group_dn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupDn"))

    @group_dn.setter
    def group_dn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03fcbb38cc8f9406c2cfd16040920893dcf30bb461381c2b3d5cb2097e4e2a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupDn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupFilter")
    def group_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupFilter"))

    @group_filter.setter
    def group_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3811d143a779e5db6802a877f8d1e5d35ef6e290a103733931344be891bc2a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureTls")
    def insecure_tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureTls"))

    @insecure_tls.setter
    def insecure_tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b50955cfc6be58bc116a9a719270ede6b05b8b944e6ce2f5d03042852e86a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureTls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isPrimaryForScope")
    def is_primary_for_scope(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isPrimaryForScope"))

    @is_primary_for_scope.setter
    def is_primary_for_scope(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9e6556d1e4d8fdd19c67e70d3acefa9ac4002742bc3a35cbf53963628bed71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPrimaryForScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumPageSize")
    def maximum_page_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumPageSize"))

    @maximum_page_size.setter
    def maximum_page_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4fe2bcf42b95cc375319705a8dd886e0009071afc816b2e4dbe4292bc673ccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumPageSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4865469105da1b4cb96fbe003d28167a8dba6a19bf37685df4b88d5f28f35902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed66626d03d31cce48dbd172a26b270dbcb8dbae8f7ed0274299bf789c7e323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTls")
    def start_tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "startTls"))

    @start_tls.setter
    def start_tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58376f9104d53029b663eca31ae37b1f290dc0e63e66f9e561e35cb7b714bfc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89e2335ebb8607d3ff609185cbee39a6defd9728e3eb43e2bc872046d120d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12cc14c4467d2334bac44fb376b88282497918103e54403f9416b0c4502c85b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upnDomain")
    def upn_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upnDomain"))

    @upn_domain.setter
    def upn_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bac6a1d85c0091f258fa7f2ca9cffc683d02f112acef453b14dc874c84069b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upnDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urls")
    def urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "urls"))

    @urls.setter
    def urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa9979ff22fb1523e2f1ae1b61686a8552bc8580c5cebb01f6957ae84de82d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAttr")
    def user_attr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAttr"))

    @user_attr.setter
    def user_attr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__469a9df9a8d9ede8b4fea64523558fab2ff5febb447411078485608fa32bf5d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAttr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userDn")
    def user_dn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userDn"))

    @user_dn.setter
    def user_dn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07c5aecaa4f52ccbfdd664e06255e2e2d0c19441b5d6b85350894450c55dafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userFilter")
    def user_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userFilter"))

    @user_filter.setter
    def user_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ee5f07a9e24049e27fde3aac778e6c81cf5e06ab995d4a346e99074d981b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useTokenGroups")
    def use_token_groups(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useTokenGroups"))

    @use_token_groups.setter
    def use_token_groups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381ae065fa83ad3d9a1a6a01bba165b118704c4e657dc30d1f47c1e320b0c2fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTokenGroups", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-boundary.authMethodLdap.AuthMethodLdapConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "scope_id": "scopeId",
        "account_attribute_maps": "accountAttributeMaps",
        "anon_group_search": "anonGroupSearch",
        "bind_dn": "bindDn",
        "bind_password": "bindPassword",
        "bind_password_hmac": "bindPasswordHmac",
        "certificates": "certificates",
        "client_certificate": "clientCertificate",
        "client_certificate_key": "clientCertificateKey",
        "client_certificate_key_hmac": "clientCertificateKeyHmac",
        "dereference_aliases": "dereferenceAliases",
        "description": "description",
        "discover_dn": "discoverDn",
        "enable_groups": "enableGroups",
        "group_attr": "groupAttr",
        "group_dn": "groupDn",
        "group_filter": "groupFilter",
        "insecure_tls": "insecureTls",
        "is_primary_for_scope": "isPrimaryForScope",
        "maximum_page_size": "maximumPageSize",
        "name": "name",
        "start_tls": "startTls",
        "state": "state",
        "type": "type",
        "upn_domain": "upnDomain",
        "urls": "urls",
        "user_attr": "userAttr",
        "user_dn": "userDn",
        "user_filter": "userFilter",
        "use_token_groups": "useTokenGroups",
    },
)
class AuthMethodLdapConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        scope_id: builtins.str,
        account_attribute_maps: typing.Optional[typing.Sequence[builtins.str]] = None,
        anon_group_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bind_dn: typing.Optional[builtins.str] = None,
        bind_password: typing.Optional[builtins.str] = None,
        bind_password_hmac: typing.Optional[builtins.str] = None,
        certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_certificate_key: typing.Optional[builtins.str] = None,
        client_certificate_key_hmac: typing.Optional[builtins.str] = None,
        dereference_aliases: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        discover_dn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_attr: typing.Optional[builtins.str] = None,
        group_dn: typing.Optional[builtins.str] = None,
        group_filter: typing.Optional[builtins.str] = None,
        insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_primary_for_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maximum_page_size: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        start_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        state: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        upn_domain: typing.Optional[builtins.str] = None,
        urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_attr: typing.Optional[builtins.str] = None,
        user_dn: typing.Optional[builtins.str] = None,
        user_filter: typing.Optional[builtins.str] = None,
        use_token_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param scope_id: The scope ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#scope_id AuthMethodLdap#scope_id}
        :param account_attribute_maps: Account attribute maps fullname and email. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#account_attribute_maps AuthMethodLdap#account_attribute_maps}
        :param anon_group_search: Use anon bind when performing LDAP group searches (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#anon_group_search AuthMethodLdap#anon_group_search}
        :param bind_dn: The distinguished name of entry to bind when performing user and group searches (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#bind_dn AuthMethodLdap#bind_dn}
        :param bind_password: The password to use along with bind-dn performing user and group searches (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#bind_password AuthMethodLdap#bind_password}
        :param bind_password_hmac: The HMAC of the bind password returned by the Boundary controller, which is used for comparison after initial setting of the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#bind_password_hmac AuthMethodLdap#bind_password_hmac}
        :param certificates: PEM-encoded X.509 CA certificate in ASN.1 DER form that can be used as a trust anchor when connecting to an LDAP server(optional). This may be specified multiple times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#certificates AuthMethodLdap#certificates}
        :param client_certificate: PEM-encoded X.509 client certificate in ASN.1 DER form that can be used to authenticate against an LDAP server(optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#client_certificate AuthMethodLdap#client_certificate}
        :param client_certificate_key: PEM-encoded X.509 client certificate key in PKCS #8, ASN.1 DER form used with the client certificate (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#client_certificate_key AuthMethodLdap#client_certificate_key}
        :param client_certificate_key_hmac: The HMAC of the client certificate key returned by the Boundary controller, which is used for comparison after initial setting of the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#client_certificate_key_hmac AuthMethodLdap#client_certificate_key_hmac}
        :param dereference_aliases: Control how aliases are dereferenced when performing the search. Can be one of: NeverDerefAliases, DerefInSearching, DerefFindingBaseObj, and DerefAlways (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#dereference_aliases AuthMethodLdap#dereference_aliases}
        :param description: The auth method description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#description AuthMethodLdap#description}
        :param discover_dn: Use anon bind to discover the bind DN of a user (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#discover_dn AuthMethodLdap#discover_dn}
        :param enable_groups: Find the authenticated user's groups during authentication (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#enable_groups AuthMethodLdap#enable_groups}
        :param group_attr: The attribute that enumerates a user's group membership from entries returned by a group search (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#group_attr AuthMethodLdap#group_attr}
        :param group_dn: The base DN under which to perform group search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#group_dn AuthMethodLdap#group_dn}
        :param group_filter: A go template used to construct a LDAP group search filter (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#group_filter AuthMethodLdap#group_filter}
        :param insecure_tls: Skip the LDAP server SSL certificate validation (optional) - insecure and use with caution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#insecure_tls AuthMethodLdap#insecure_tls}
        :param is_primary_for_scope: When true, makes this auth method the primary auth method for the scope in which it resides. The primary auth method for a scope means the the user will be automatically created when they login using an LDAP account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#is_primary_for_scope AuthMethodLdap#is_primary_for_scope}
        :param maximum_page_size: MaximumPageSize specifies a maximum search result size to use when retrieving the authenticated user's groups (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#maximum_page_size AuthMethodLdap#maximum_page_size}
        :param name: The auth method name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#name AuthMethodLdap#name}
        :param start_tls: Issue StartTLS command after connecting (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#start_tls AuthMethodLdap#start_tls}
        :param state: Can be one of 'inactive', 'active-private', or 'active-public'. Defaults to active-public. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#state AuthMethodLdap#state}
        :param type: The type of auth method; hardcoded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#type AuthMethodLdap#type}
        :param upn_domain: The userPrincipalDomain used to construct the UPN string for the authenticating user (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#upn_domain AuthMethodLdap#upn_domain}
        :param urls: The LDAP URLs that specify LDAP servers to connect to (required). May be specified multiple times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#urls AuthMethodLdap#urls}
        :param user_attr: The attribute on user entry matching the username passed when authenticating (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#user_attr AuthMethodLdap#user_attr}
        :param user_dn: The base DN under which to perform user search (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#user_dn AuthMethodLdap#user_dn}
        :param user_filter: A go template used to construct a LDAP user search filter (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#user_filter AuthMethodLdap#user_filter}
        :param use_token_groups: Use the Active Directory tokenGroups constructed attribute of the user to find the group memberships (optional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#use_token_groups AuthMethodLdap#use_token_groups}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3fa989bab318c9833759914b8a10299e3bf7eec840275545f2026b3766418d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument scope_id", value=scope_id, expected_type=type_hints["scope_id"])
            check_type(argname="argument account_attribute_maps", value=account_attribute_maps, expected_type=type_hints["account_attribute_maps"])
            check_type(argname="argument anon_group_search", value=anon_group_search, expected_type=type_hints["anon_group_search"])
            check_type(argname="argument bind_dn", value=bind_dn, expected_type=type_hints["bind_dn"])
            check_type(argname="argument bind_password", value=bind_password, expected_type=type_hints["bind_password"])
            check_type(argname="argument bind_password_hmac", value=bind_password_hmac, expected_type=type_hints["bind_password_hmac"])
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_certificate_key", value=client_certificate_key, expected_type=type_hints["client_certificate_key"])
            check_type(argname="argument client_certificate_key_hmac", value=client_certificate_key_hmac, expected_type=type_hints["client_certificate_key_hmac"])
            check_type(argname="argument dereference_aliases", value=dereference_aliases, expected_type=type_hints["dereference_aliases"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument discover_dn", value=discover_dn, expected_type=type_hints["discover_dn"])
            check_type(argname="argument enable_groups", value=enable_groups, expected_type=type_hints["enable_groups"])
            check_type(argname="argument group_attr", value=group_attr, expected_type=type_hints["group_attr"])
            check_type(argname="argument group_dn", value=group_dn, expected_type=type_hints["group_dn"])
            check_type(argname="argument group_filter", value=group_filter, expected_type=type_hints["group_filter"])
            check_type(argname="argument insecure_tls", value=insecure_tls, expected_type=type_hints["insecure_tls"])
            check_type(argname="argument is_primary_for_scope", value=is_primary_for_scope, expected_type=type_hints["is_primary_for_scope"])
            check_type(argname="argument maximum_page_size", value=maximum_page_size, expected_type=type_hints["maximum_page_size"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument start_tls", value=start_tls, expected_type=type_hints["start_tls"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument upn_domain", value=upn_domain, expected_type=type_hints["upn_domain"])
            check_type(argname="argument urls", value=urls, expected_type=type_hints["urls"])
            check_type(argname="argument user_attr", value=user_attr, expected_type=type_hints["user_attr"])
            check_type(argname="argument user_dn", value=user_dn, expected_type=type_hints["user_dn"])
            check_type(argname="argument user_filter", value=user_filter, expected_type=type_hints["user_filter"])
            check_type(argname="argument use_token_groups", value=use_token_groups, expected_type=type_hints["use_token_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scope_id": scope_id,
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
        if account_attribute_maps is not None:
            self._values["account_attribute_maps"] = account_attribute_maps
        if anon_group_search is not None:
            self._values["anon_group_search"] = anon_group_search
        if bind_dn is not None:
            self._values["bind_dn"] = bind_dn
        if bind_password is not None:
            self._values["bind_password"] = bind_password
        if bind_password_hmac is not None:
            self._values["bind_password_hmac"] = bind_password_hmac
        if certificates is not None:
            self._values["certificates"] = certificates
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_certificate_key is not None:
            self._values["client_certificate_key"] = client_certificate_key
        if client_certificate_key_hmac is not None:
            self._values["client_certificate_key_hmac"] = client_certificate_key_hmac
        if dereference_aliases is not None:
            self._values["dereference_aliases"] = dereference_aliases
        if description is not None:
            self._values["description"] = description
        if discover_dn is not None:
            self._values["discover_dn"] = discover_dn
        if enable_groups is not None:
            self._values["enable_groups"] = enable_groups
        if group_attr is not None:
            self._values["group_attr"] = group_attr
        if group_dn is not None:
            self._values["group_dn"] = group_dn
        if group_filter is not None:
            self._values["group_filter"] = group_filter
        if insecure_tls is not None:
            self._values["insecure_tls"] = insecure_tls
        if is_primary_for_scope is not None:
            self._values["is_primary_for_scope"] = is_primary_for_scope
        if maximum_page_size is not None:
            self._values["maximum_page_size"] = maximum_page_size
        if name is not None:
            self._values["name"] = name
        if start_tls is not None:
            self._values["start_tls"] = start_tls
        if state is not None:
            self._values["state"] = state
        if type is not None:
            self._values["type"] = type
        if upn_domain is not None:
            self._values["upn_domain"] = upn_domain
        if urls is not None:
            self._values["urls"] = urls
        if user_attr is not None:
            self._values["user_attr"] = user_attr
        if user_dn is not None:
            self._values["user_dn"] = user_dn
        if user_filter is not None:
            self._values["user_filter"] = user_filter
        if use_token_groups is not None:
            self._values["use_token_groups"] = use_token_groups

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
    def scope_id(self) -> builtins.str:
        '''The scope ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#scope_id AuthMethodLdap#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_attribute_maps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Account attribute maps fullname and email.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#account_attribute_maps AuthMethodLdap#account_attribute_maps}
        '''
        result = self._values.get("account_attribute_maps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def anon_group_search(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use anon bind when performing LDAP group searches (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#anon_group_search AuthMethodLdap#anon_group_search}
        '''
        result = self._values.get("anon_group_search")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bind_dn(self) -> typing.Optional[builtins.str]:
        '''The distinguished name of entry to bind when performing user and group searches (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#bind_dn AuthMethodLdap#bind_dn}
        '''
        result = self._values.get("bind_dn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bind_password(self) -> typing.Optional[builtins.str]:
        '''The password to use along with bind-dn performing user and group searches (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#bind_password AuthMethodLdap#bind_password}
        '''
        result = self._values.get("bind_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bind_password_hmac(self) -> typing.Optional[builtins.str]:
        '''The HMAC of the bind password returned by the Boundary controller, which is used for comparison after initial setting of the value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#bind_password_hmac AuthMethodLdap#bind_password_hmac}
        '''
        result = self._values.get("bind_password_hmac")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''PEM-encoded X.509 CA certificate in ASN.1 DER form that can be used as a trust anchor when connecting to an LDAP server(optional).  This may be specified multiple times.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#certificates AuthMethodLdap#certificates}
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded X.509 client certificate in ASN.1 DER form that can be used to authenticate against an LDAP server(optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#client_certificate AuthMethodLdap#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_key(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded X.509 client certificate key in PKCS #8, ASN.1 DER form used with the client certificate (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#client_certificate_key AuthMethodLdap#client_certificate_key}
        '''
        result = self._values.get("client_certificate_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_key_hmac(self) -> typing.Optional[builtins.str]:
        '''The HMAC of the client certificate key returned by the Boundary controller, which is used for comparison after initial setting of the value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#client_certificate_key_hmac AuthMethodLdap#client_certificate_key_hmac}
        '''
        result = self._values.get("client_certificate_key_hmac")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dereference_aliases(self) -> typing.Optional[builtins.str]:
        '''Control how aliases are dereferenced when performing the search. Can be one of: NeverDerefAliases, DerefInSearching, DerefFindingBaseObj, and DerefAlways (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#dereference_aliases AuthMethodLdap#dereference_aliases}
        '''
        result = self._values.get("dereference_aliases")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The auth method description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#description AuthMethodLdap#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def discover_dn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use anon bind to discover the bind DN of a user (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#discover_dn AuthMethodLdap#discover_dn}
        '''
        result = self._values.get("discover_dn")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Find the authenticated user's groups during authentication (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#enable_groups AuthMethodLdap#enable_groups}
        '''
        result = self._values.get("enable_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group_attr(self) -> typing.Optional[builtins.str]:
        '''The attribute that enumerates a user's group membership from entries returned by a group search (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#group_attr AuthMethodLdap#group_attr}
        '''
        result = self._values.get("group_attr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_dn(self) -> typing.Optional[builtins.str]:
        '''The base DN under which to perform group search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#group_dn AuthMethodLdap#group_dn}
        '''
        result = self._values.get("group_dn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_filter(self) -> typing.Optional[builtins.str]:
        '''A go template used to construct a LDAP group search filter (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#group_filter AuthMethodLdap#group_filter}
        '''
        result = self._values.get("group_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Skip the LDAP server SSL certificate validation (optional) - insecure and use with caution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#insecure_tls AuthMethodLdap#insecure_tls}
        '''
        result = self._values.get("insecure_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_primary_for_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, makes this auth method the primary auth method for the scope in which it resides.

        The primary auth method for a scope means the the user will be automatically created when they login using an LDAP account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#is_primary_for_scope AuthMethodLdap#is_primary_for_scope}
        '''
        result = self._values.get("is_primary_for_scope")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def maximum_page_size(self) -> typing.Optional[jsii.Number]:
        '''MaximumPageSize specifies a maximum search result size to use when retrieving the authenticated user's groups (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#maximum_page_size AuthMethodLdap#maximum_page_size}
        '''
        result = self._values.get("maximum_page_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The auth method name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#name AuthMethodLdap#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Issue StartTLS command after connecting (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#start_tls AuthMethodLdap#start_tls}
        '''
        result = self._values.get("start_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Can be one of 'inactive', 'active-private', or 'active-public'. Defaults to active-public.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#state AuthMethodLdap#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of auth method; hardcoded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#type AuthMethodLdap#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upn_domain(self) -> typing.Optional[builtins.str]:
        '''The userPrincipalDomain used to construct the UPN string for the authenticating user (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#upn_domain AuthMethodLdap#upn_domain}
        '''
        result = self._values.get("upn_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The LDAP URLs that specify LDAP servers to connect to (required).  May be specified multiple times.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#urls AuthMethodLdap#urls}
        '''
        result = self._values.get("urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_attr(self) -> typing.Optional[builtins.str]:
        '''The attribute on user entry matching the username passed when authenticating (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#user_attr AuthMethodLdap#user_attr}
        '''
        result = self._values.get("user_attr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_dn(self) -> typing.Optional[builtins.str]:
        '''The base DN under which to perform user search (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#user_dn AuthMethodLdap#user_dn}
        '''
        result = self._values.get("user_dn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_filter(self) -> typing.Optional[builtins.str]:
        '''A go template used to construct a LDAP user search filter (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#user_filter AuthMethodLdap#user_filter}
        '''
        result = self._values.get("user_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_token_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use the Active Directory tokenGroups constructed attribute of the user to find the group memberships (optional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/auth_method_ldap#use_token_groups AuthMethodLdap#use_token_groups}
        '''
        result = self._values.get("use_token_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthMethodLdapConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AuthMethodLdap",
    "AuthMethodLdapConfig",
]

publication.publish()

def _typecheckingstub__d81df91e74f7309d44b4335008d4adbdb6ab75f49ef810a5b5d3cb7bb491fefc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    scope_id: builtins.str,
    account_attribute_maps: typing.Optional[typing.Sequence[builtins.str]] = None,
    anon_group_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bind_dn: typing.Optional[builtins.str] = None,
    bind_password: typing.Optional[builtins.str] = None,
    bind_password_hmac: typing.Optional[builtins.str] = None,
    certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_certificate_key: typing.Optional[builtins.str] = None,
    client_certificate_key_hmac: typing.Optional[builtins.str] = None,
    dereference_aliases: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    discover_dn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_attr: typing.Optional[builtins.str] = None,
    group_dn: typing.Optional[builtins.str] = None,
    group_filter: typing.Optional[builtins.str] = None,
    insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_primary_for_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maximum_page_size: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    start_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    state: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    upn_domain: typing.Optional[builtins.str] = None,
    urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_attr: typing.Optional[builtins.str] = None,
    user_dn: typing.Optional[builtins.str] = None,
    user_filter: typing.Optional[builtins.str] = None,
    use_token_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__db66f29195e83a62225dbcf5f20f7b5cd76cd2a0b42855af0532de7169c81b10(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8320960f700bfb54157c064ecbc0a07bd2f7a791ca88a06366e8dc80d526c757(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a20afa16a45c8486ba9839ef8469d01d0cffdd15e4f0818c575aac9a1b6f4d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca478227f5e6c5a16b4efa937650d35af3ed65f45606a1ef3e3e2ebca4531a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562de4f13fb1899d00990b3d6662720ba910501d9fe55fe073477decd0677c09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5296cd77c36c442cc8a0129b1c91a8b25d4a88a49da280e8d89bc4f35c8218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c63ff0bc85620263ee2563e74be65c31e1ff87e37d6e5553f41697783ef8a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc420167ebfefb413a534405c5533fd465a71524077b94a27edfd9d2924ab554(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f84e59e0854cfe11209c5cf151190476b6241abad494868599582e4648a6f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0933104f1d49b756de962badbd38cec0e5cf49fec4409c21f78fcedce27a02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1201919c1cae34720958313cc692e07635cfa580b756b614f791abb80568b6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc34aa93629cd42d132def40529a95379ad9e90d44571a255700a63ff2e6d497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cb7ed28fa4a0116bf0b5f0b91bef473a27b3fdd1d716b733e1c8935863e536(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787668195e9afe5ce1177e38e1361c782e68b20fdec55494abf504a01d2257fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a8ac0c2988a04f2bbd1b144fbbf7a2f89336a9317ac7983453299f5b10308c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03fcbb38cc8f9406c2cfd16040920893dcf30bb461381c2b3d5cb2097e4e2a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3811d143a779e5db6802a877f8d1e5d35ef6e290a103733931344be891bc2a3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b50955cfc6be58bc116a9a719270ede6b05b8b944e6ce2f5d03042852e86a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9e6556d1e4d8fdd19c67e70d3acefa9ac4002742bc3a35cbf53963628bed71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4fe2bcf42b95cc375319705a8dd886e0009071afc816b2e4dbe4292bc673ccb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4865469105da1b4cb96fbe003d28167a8dba6a19bf37685df4b88d5f28f35902(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed66626d03d31cce48dbd172a26b270dbcb8dbae8f7ed0274299bf789c7e323(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58376f9104d53029b663eca31ae37b1f290dc0e63e66f9e561e35cb7b714bfc7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89e2335ebb8607d3ff609185cbee39a6defd9728e3eb43e2bc872046d120d1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12cc14c4467d2334bac44fb376b88282497918103e54403f9416b0c4502c85b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bac6a1d85c0091f258fa7f2ca9cffc683d02f112acef453b14dc874c84069b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa9979ff22fb1523e2f1ae1b61686a8552bc8580c5cebb01f6957ae84de82d1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469a9df9a8d9ede8b4fea64523558fab2ff5febb447411078485608fa32bf5d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07c5aecaa4f52ccbfdd664e06255e2e2d0c19441b5d6b85350894450c55dafc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ee5f07a9e24049e27fde3aac778e6c81cf5e06ab995d4a346e99074d981b45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381ae065fa83ad3d9a1a6a01bba165b118704c4e657dc30d1f47c1e320b0c2fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3fa989bab318c9833759914b8a10299e3bf7eec840275545f2026b3766418d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scope_id: builtins.str,
    account_attribute_maps: typing.Optional[typing.Sequence[builtins.str]] = None,
    anon_group_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bind_dn: typing.Optional[builtins.str] = None,
    bind_password: typing.Optional[builtins.str] = None,
    bind_password_hmac: typing.Optional[builtins.str] = None,
    certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_certificate_key: typing.Optional[builtins.str] = None,
    client_certificate_key_hmac: typing.Optional[builtins.str] = None,
    dereference_aliases: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    discover_dn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_attr: typing.Optional[builtins.str] = None,
    group_dn: typing.Optional[builtins.str] = None,
    group_filter: typing.Optional[builtins.str] = None,
    insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_primary_for_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maximum_page_size: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    start_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    state: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    upn_domain: typing.Optional[builtins.str] = None,
    urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_attr: typing.Optional[builtins.str] = None,
    user_dn: typing.Optional[builtins.str] = None,
    user_filter: typing.Optional[builtins.str] = None,
    use_token_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
