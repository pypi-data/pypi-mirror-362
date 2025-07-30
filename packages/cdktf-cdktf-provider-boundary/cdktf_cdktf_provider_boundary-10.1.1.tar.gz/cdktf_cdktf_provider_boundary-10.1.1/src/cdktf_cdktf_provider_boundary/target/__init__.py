r'''
# `boundary_target`

Refer to the Terraform Registry for docs: [`boundary_target`](https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target).
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


class Target(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-boundary.target.Target",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target boundary_target}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        type: builtins.str,
        address: typing.Optional[builtins.str] = None,
        brokered_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_client_port: typing.Optional[jsii.Number] = None,
        default_port: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        egress_worker_filter: typing.Optional[builtins.str] = None,
        enable_session_recording: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ingress_worker_filter: typing.Optional[builtins.str] = None,
        injected_application_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        session_connection_limit: typing.Optional[jsii.Number] = None,
        session_max_seconds: typing.Optional[jsii.Number] = None,
        storage_bucket_id: typing.Optional[builtins.str] = None,
        worker_filter: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target boundary_target} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#scope_id Target#scope_id}
        :param type: The target resource type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#type Target#type}
        :param address: Optionally, a valid network address to connect to for this target. Cannot be used alongside host_source_ids. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#address Target#address}
        :param brokered_credential_source_ids: A list of brokered credential source ID's. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#brokered_credential_source_ids Target#brokered_credential_source_ids}
        :param default_client_port: The default client port for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#default_client_port Target#default_client_port}
        :param default_port: The default port for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#default_port Target#default_port}
        :param description: The target description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#description Target#description}
        :param egress_worker_filter: Boolean expression to filter the workers used to access this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#egress_worker_filter Target#egress_worker_filter}
        :param enable_session_recording: HCP/Ent Only. Enable sessions recording for this target. Only applicable for SSH targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#enable_session_recording Target#enable_session_recording}
        :param host_source_ids: A list of host source ID's. Cannot be used alongside address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#host_source_ids Target#host_source_ids}
        :param ingress_worker_filter: HCP Only. Boolean expression to filter the workers a user will connect to when initiating a session against this target Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#ingress_worker_filter Target#ingress_worker_filter}
        :param injected_application_credential_source_ids: A list of injected application credential source ID's. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#injected_application_credential_source_ids Target#injected_application_credential_source_ids}
        :param name: The target name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#name Target#name}
        :param session_connection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#session_connection_limit Target#session_connection_limit}.
        :param session_max_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#session_max_seconds Target#session_max_seconds}.
        :param storage_bucket_id: HCP/Ent Only. Storage bucket for this target. Only applicable for SSH targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#storage_bucket_id Target#storage_bucket_id}
        :param worker_filter: Boolean expression to filter the workers for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#worker_filter Target#worker_filter}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebef56477817cc49a79ac7548eea89611e3135869c19926d29a79a062fa47ab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TargetConfig(
            scope_id=scope_id,
            type=type,
            address=address,
            brokered_credential_source_ids=brokered_credential_source_ids,
            default_client_port=default_client_port,
            default_port=default_port,
            description=description,
            egress_worker_filter=egress_worker_filter,
            enable_session_recording=enable_session_recording,
            host_source_ids=host_source_ids,
            ingress_worker_filter=ingress_worker_filter,
            injected_application_credential_source_ids=injected_application_credential_source_ids,
            name=name,
            session_connection_limit=session_connection_limit,
            session_max_seconds=session_max_seconds,
            storage_bucket_id=storage_bucket_id,
            worker_filter=worker_filter,
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
        '''Generates CDKTF code for importing a Target resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Target to import.
        :param import_from_id: The id of the existing Target that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Target to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848349402aba15585e0db3e16fd2861e09eb262ee77830ae06b98f91da57f28e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetBrokeredCredentialSourceIds")
    def reset_brokered_credential_source_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrokeredCredentialSourceIds", []))

    @jsii.member(jsii_name="resetDefaultClientPort")
    def reset_default_client_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultClientPort", []))

    @jsii.member(jsii_name="resetDefaultPort")
    def reset_default_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPort", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEgressWorkerFilter")
    def reset_egress_worker_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressWorkerFilter", []))

    @jsii.member(jsii_name="resetEnableSessionRecording")
    def reset_enable_session_recording(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSessionRecording", []))

    @jsii.member(jsii_name="resetHostSourceIds")
    def reset_host_source_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostSourceIds", []))

    @jsii.member(jsii_name="resetIngressWorkerFilter")
    def reset_ingress_worker_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressWorkerFilter", []))

    @jsii.member(jsii_name="resetInjectedApplicationCredentialSourceIds")
    def reset_injected_application_credential_source_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInjectedApplicationCredentialSourceIds", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSessionConnectionLimit")
    def reset_session_connection_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionConnectionLimit", []))

    @jsii.member(jsii_name="resetSessionMaxSeconds")
    def reset_session_max_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionMaxSeconds", []))

    @jsii.member(jsii_name="resetStorageBucketId")
    def reset_storage_bucket_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageBucketId", []))

    @jsii.member(jsii_name="resetWorkerFilter")
    def reset_worker_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerFilter", []))

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
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="brokeredCredentialSourceIdsInput")
    def brokered_credential_source_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "brokeredCredentialSourceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultClientPortInput")
    def default_client_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultClientPortInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPortInput")
    def default_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultPortInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="egressWorkerFilterInput")
    def egress_worker_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "egressWorkerFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSessionRecordingInput")
    def enable_session_recording_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSessionRecordingInput"))

    @builtins.property
    @jsii.member(jsii_name="hostSourceIdsInput")
    def host_source_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostSourceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressWorkerFilterInput")
    def ingress_worker_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingressWorkerFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="injectedApplicationCredentialSourceIdsInput")
    def injected_application_credential_source_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "injectedApplicationCredentialSourceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionConnectionLimitInput")
    def session_connection_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionConnectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionMaxSecondsInput")
    def session_max_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionMaxSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageBucketIdInput")
    def storage_bucket_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageBucketIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="workerFilterInput")
    def worker_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632559626c42a52bb07e40ad36155c4a8a1008aff47ed9d61c18d0b768aee85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="brokeredCredentialSourceIds")
    def brokered_credential_source_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "brokeredCredentialSourceIds"))

    @brokered_credential_source_ids.setter
    def brokered_credential_source_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2d85aca1b17af87cd56f9f72cb476381b44805f888013726836aff0b115fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "brokeredCredentialSourceIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultClientPort")
    def default_client_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultClientPort"))

    @default_client_port.setter
    def default_client_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e476bc2f762d60541597a12cf70e3cbc3484d4e3c28a1ce779bc61e5582d3235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultClientPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultPort")
    def default_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultPort"))

    @default_port.setter
    def default_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97b18eb3a15bc6ab1b42641e60d81d079f8f7d823b41c19ca5a4b2da786085e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018aafdcf46c5443bea080998e12df13e2909b4fdace106e9818b3fc9ed11a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="egressWorkerFilter")
    def egress_worker_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egressWorkerFilter"))

    @egress_worker_filter.setter
    def egress_worker_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9cf447e2c3bf738c04825b3d3d690fc6e4fc1074d0c9d1be6b0f7b09ec4491e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressWorkerFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSessionRecording")
    def enable_session_recording(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSessionRecording"))

    @enable_session_recording.setter
    def enable_session_recording(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d65f622e2816185407e0842a0167152dd4f9bee25d4a60c4a3d557fdda7058b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSessionRecording", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostSourceIds")
    def host_source_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostSourceIds"))

    @host_source_ids.setter
    def host_source_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d8449714a75da6a8a016433195537e2ea03d77ae129cff8f0cd51582e0949bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostSourceIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressWorkerFilter")
    def ingress_worker_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressWorkerFilter"))

    @ingress_worker_filter.setter
    def ingress_worker_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb793b2b023cfcd0977ca2d4931eb8b05b2388b050069bdbb8460efd7d4acc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressWorkerFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="injectedApplicationCredentialSourceIds")
    def injected_application_credential_source_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "injectedApplicationCredentialSourceIds"))

    @injected_application_credential_source_ids.setter
    def injected_application_credential_source_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc6e67ebe948279fdb61e592aef13052af8b6ff959b6b0163d895c5fe55059c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "injectedApplicationCredentialSourceIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6567040255f83a757f6b8703ccb67788f84aca7d141c3be546ee621fc16e08fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c24274b1c03c129609cd03c4b80a7a3bffe2e6013a47add4a3fcdf991f5b1a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionConnectionLimit")
    def session_connection_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionConnectionLimit"))

    @session_connection_limit.setter
    def session_connection_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01185b25a064b1f61ffc9bd13d65e473a1738c83a4622e4f6eb7e58acf1368f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionConnectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionMaxSeconds")
    def session_max_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionMaxSeconds"))

    @session_max_seconds.setter
    def session_max_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa0ffa367b07562530ed2e66eb6a5f5960a529db2287d3ca45cb49b5c3ee6e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionMaxSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageBucketId")
    def storage_bucket_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageBucketId"))

    @storage_bucket_id.setter
    def storage_bucket_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679ccd243498534b29dba8acdaec191134c01bb273425cd76fcb3bd8f2549fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageBucketId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad96d6a290125eb065090a5f3e95c6a91f9579aee425335c6010e9ff0d5a131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerFilter")
    def worker_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerFilter"))

    @worker_filter.setter
    def worker_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6604025668de90136fded85bdae8bc989cd26cefc48879ed1d30940f71253562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerFilter", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-boundary.target.TargetConfig",
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
        "type": "type",
        "address": "address",
        "brokered_credential_source_ids": "brokeredCredentialSourceIds",
        "default_client_port": "defaultClientPort",
        "default_port": "defaultPort",
        "description": "description",
        "egress_worker_filter": "egressWorkerFilter",
        "enable_session_recording": "enableSessionRecording",
        "host_source_ids": "hostSourceIds",
        "ingress_worker_filter": "ingressWorkerFilter",
        "injected_application_credential_source_ids": "injectedApplicationCredentialSourceIds",
        "name": "name",
        "session_connection_limit": "sessionConnectionLimit",
        "session_max_seconds": "sessionMaxSeconds",
        "storage_bucket_id": "storageBucketId",
        "worker_filter": "workerFilter",
    },
)
class TargetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        address: typing.Optional[builtins.str] = None,
        brokered_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_client_port: typing.Optional[jsii.Number] = None,
        default_port: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        egress_worker_filter: typing.Optional[builtins.str] = None,
        enable_session_recording: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ingress_worker_filter: typing.Optional[builtins.str] = None,
        injected_application_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        session_connection_limit: typing.Optional[jsii.Number] = None,
        session_max_seconds: typing.Optional[jsii.Number] = None,
        storage_bucket_id: typing.Optional[builtins.str] = None,
        worker_filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#scope_id Target#scope_id}
        :param type: The target resource type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#type Target#type}
        :param address: Optionally, a valid network address to connect to for this target. Cannot be used alongside host_source_ids. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#address Target#address}
        :param brokered_credential_source_ids: A list of brokered credential source ID's. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#brokered_credential_source_ids Target#brokered_credential_source_ids}
        :param default_client_port: The default client port for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#default_client_port Target#default_client_port}
        :param default_port: The default port for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#default_port Target#default_port}
        :param description: The target description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#description Target#description}
        :param egress_worker_filter: Boolean expression to filter the workers used to access this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#egress_worker_filter Target#egress_worker_filter}
        :param enable_session_recording: HCP/Ent Only. Enable sessions recording for this target. Only applicable for SSH targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#enable_session_recording Target#enable_session_recording}
        :param host_source_ids: A list of host source ID's. Cannot be used alongside address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#host_source_ids Target#host_source_ids}
        :param ingress_worker_filter: HCP Only. Boolean expression to filter the workers a user will connect to when initiating a session against this target Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#ingress_worker_filter Target#ingress_worker_filter}
        :param injected_application_credential_source_ids: A list of injected application credential source ID's. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#injected_application_credential_source_ids Target#injected_application_credential_source_ids}
        :param name: The target name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#name Target#name}
        :param session_connection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#session_connection_limit Target#session_connection_limit}.
        :param session_max_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#session_max_seconds Target#session_max_seconds}.
        :param storage_bucket_id: HCP/Ent Only. Storage bucket for this target. Only applicable for SSH targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#storage_bucket_id Target#storage_bucket_id}
        :param worker_filter: Boolean expression to filter the workers for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#worker_filter Target#worker_filter}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3790b32773af6299bc7839606b6164e1bada068e491dd6db09b0641a30f5e25)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument scope_id", value=scope_id, expected_type=type_hints["scope_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument brokered_credential_source_ids", value=brokered_credential_source_ids, expected_type=type_hints["brokered_credential_source_ids"])
            check_type(argname="argument default_client_port", value=default_client_port, expected_type=type_hints["default_client_port"])
            check_type(argname="argument default_port", value=default_port, expected_type=type_hints["default_port"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument egress_worker_filter", value=egress_worker_filter, expected_type=type_hints["egress_worker_filter"])
            check_type(argname="argument enable_session_recording", value=enable_session_recording, expected_type=type_hints["enable_session_recording"])
            check_type(argname="argument host_source_ids", value=host_source_ids, expected_type=type_hints["host_source_ids"])
            check_type(argname="argument ingress_worker_filter", value=ingress_worker_filter, expected_type=type_hints["ingress_worker_filter"])
            check_type(argname="argument injected_application_credential_source_ids", value=injected_application_credential_source_ids, expected_type=type_hints["injected_application_credential_source_ids"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument session_connection_limit", value=session_connection_limit, expected_type=type_hints["session_connection_limit"])
            check_type(argname="argument session_max_seconds", value=session_max_seconds, expected_type=type_hints["session_max_seconds"])
            check_type(argname="argument storage_bucket_id", value=storage_bucket_id, expected_type=type_hints["storage_bucket_id"])
            check_type(argname="argument worker_filter", value=worker_filter, expected_type=type_hints["worker_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scope_id": scope_id,
            "type": type,
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
        if address is not None:
            self._values["address"] = address
        if brokered_credential_source_ids is not None:
            self._values["brokered_credential_source_ids"] = brokered_credential_source_ids
        if default_client_port is not None:
            self._values["default_client_port"] = default_client_port
        if default_port is not None:
            self._values["default_port"] = default_port
        if description is not None:
            self._values["description"] = description
        if egress_worker_filter is not None:
            self._values["egress_worker_filter"] = egress_worker_filter
        if enable_session_recording is not None:
            self._values["enable_session_recording"] = enable_session_recording
        if host_source_ids is not None:
            self._values["host_source_ids"] = host_source_ids
        if ingress_worker_filter is not None:
            self._values["ingress_worker_filter"] = ingress_worker_filter
        if injected_application_credential_source_ids is not None:
            self._values["injected_application_credential_source_ids"] = injected_application_credential_source_ids
        if name is not None:
            self._values["name"] = name
        if session_connection_limit is not None:
            self._values["session_connection_limit"] = session_connection_limit
        if session_max_seconds is not None:
            self._values["session_max_seconds"] = session_max_seconds
        if storage_bucket_id is not None:
            self._values["storage_bucket_id"] = storage_bucket_id
        if worker_filter is not None:
            self._values["worker_filter"] = worker_filter

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
        '''The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#scope_id Target#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The target resource type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#type Target#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Optionally, a valid network address to connect to for this target. Cannot be used alongside host_source_ids.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#address Target#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def brokered_credential_source_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of brokered credential source ID's.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#brokered_credential_source_ids Target#brokered_credential_source_ids}
        '''
        result = self._values.get("brokered_credential_source_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_client_port(self) -> typing.Optional[jsii.Number]:
        '''The default client port for this target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#default_client_port Target#default_client_port}
        '''
        result = self._values.get("default_client_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_port(self) -> typing.Optional[jsii.Number]:
        '''The default port for this target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#default_port Target#default_port}
        '''
        result = self._values.get("default_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The target description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#description Target#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def egress_worker_filter(self) -> typing.Optional[builtins.str]:
        '''Boolean expression to filter the workers used to access this target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#egress_worker_filter Target#egress_worker_filter}
        '''
        result = self._values.get("egress_worker_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_session_recording(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''HCP/Ent Only. Enable sessions recording for this target. Only applicable for SSH targets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#enable_session_recording Target#enable_session_recording}
        '''
        result = self._values.get("enable_session_recording")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_source_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of host source ID's. Cannot be used alongside address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#host_source_ids Target#host_source_ids}
        '''
        result = self._values.get("host_source_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ingress_worker_filter(self) -> typing.Optional[builtins.str]:
        '''HCP Only.

        Boolean expression to filter the workers a user will connect to when initiating a session against this target

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#ingress_worker_filter Target#ingress_worker_filter}
        '''
        result = self._values.get("ingress_worker_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def injected_application_credential_source_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of injected application credential source ID's.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#injected_application_credential_source_ids Target#injected_application_credential_source_ids}
        '''
        result = self._values.get("injected_application_credential_source_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The target name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#name Target#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_connection_limit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#session_connection_limit Target#session_connection_limit}.'''
        result = self._values.get("session_connection_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_max_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#session_max_seconds Target#session_max_seconds}.'''
        result = self._values.get("session_max_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_bucket_id(self) -> typing.Optional[builtins.str]:
        '''HCP/Ent Only. Storage bucket for this target. Only applicable for SSH targets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#storage_bucket_id Target#storage_bucket_id}
        '''
        result = self._values.get("storage_bucket_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_filter(self) -> typing.Optional[builtins.str]:
        '''Boolean expression to filter the workers for this target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/target#worker_filter Target#worker_filter}
        '''
        result = self._values.get("worker_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Target",
    "TargetConfig",
]

publication.publish()

def _typecheckingstub__aebef56477817cc49a79ac7548eea89611e3135869c19926d29a79a062fa47ab(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    scope_id: builtins.str,
    type: builtins.str,
    address: typing.Optional[builtins.str] = None,
    brokered_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_client_port: typing.Optional[jsii.Number] = None,
    default_port: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    egress_worker_filter: typing.Optional[builtins.str] = None,
    enable_session_recording: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ingress_worker_filter: typing.Optional[builtins.str] = None,
    injected_application_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    session_connection_limit: typing.Optional[jsii.Number] = None,
    session_max_seconds: typing.Optional[jsii.Number] = None,
    storage_bucket_id: typing.Optional[builtins.str] = None,
    worker_filter: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__848349402aba15585e0db3e16fd2861e09eb262ee77830ae06b98f91da57f28e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632559626c42a52bb07e40ad36155c4a8a1008aff47ed9d61c18d0b768aee85a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2d85aca1b17af87cd56f9f72cb476381b44805f888013726836aff0b115fe1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e476bc2f762d60541597a12cf70e3cbc3484d4e3c28a1ce779bc61e5582d3235(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97b18eb3a15bc6ab1b42641e60d81d079f8f7d823b41c19ca5a4b2da786085e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018aafdcf46c5443bea080998e12df13e2909b4fdace106e9818b3fc9ed11a04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cf447e2c3bf738c04825b3d3d690fc6e4fc1074d0c9d1be6b0f7b09ec4491e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d65f622e2816185407e0842a0167152dd4f9bee25d4a60c4a3d557fdda7058b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8449714a75da6a8a016433195537e2ea03d77ae129cff8f0cd51582e0949bb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb793b2b023cfcd0977ca2d4931eb8b05b2388b050069bdbb8460efd7d4acc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc6e67ebe948279fdb61e592aef13052af8b6ff959b6b0163d895c5fe55059c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6567040255f83a757f6b8703ccb67788f84aca7d141c3be546ee621fc16e08fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24274b1c03c129609cd03c4b80a7a3bffe2e6013a47add4a3fcdf991f5b1a50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01185b25a064b1f61ffc9bd13d65e473a1738c83a4622e4f6eb7e58acf1368f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa0ffa367b07562530ed2e66eb6a5f5960a529db2287d3ca45cb49b5c3ee6e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679ccd243498534b29dba8acdaec191134c01bb273425cd76fcb3bd8f2549fa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad96d6a290125eb065090a5f3e95c6a91f9579aee425335c6010e9ff0d5a131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6604025668de90136fded85bdae8bc989cd26cefc48879ed1d30940f71253562(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3790b32773af6299bc7839606b6164e1bada068e491dd6db09b0641a30f5e25(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scope_id: builtins.str,
    type: builtins.str,
    address: typing.Optional[builtins.str] = None,
    brokered_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_client_port: typing.Optional[jsii.Number] = None,
    default_port: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    egress_worker_filter: typing.Optional[builtins.str] = None,
    enable_session_recording: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ingress_worker_filter: typing.Optional[builtins.str] = None,
    injected_application_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    session_connection_limit: typing.Optional[jsii.Number] = None,
    session_max_seconds: typing.Optional[jsii.Number] = None,
    storage_bucket_id: typing.Optional[builtins.str] = None,
    worker_filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
