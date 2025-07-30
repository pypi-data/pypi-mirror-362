r'''
# `boundary_storage_bucket`

Refer to the Terraform Registry for docs: [`boundary_storage_bucket`](https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket).
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


class StorageBucket(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-boundary.storageBucket.StorageBucket",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket boundary_storage_bucket}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: builtins.str,
        scope_id: builtins.str,
        worker_filter: builtins.str,
        attributes_json: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        plugin_id: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        secrets_json: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket boundary_storage_bucket} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket_name: The name of the bucket within the external object store service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#bucket_name StorageBucket#bucket_name}
        :param scope_id: The scope for this storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#scope_id StorageBucket#scope_id}
        :param worker_filter: Filters to the worker(s) that can handle requests for this storage bucket. The filter must match an existing worker in order to create a storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#worker_filter StorageBucket#worker_filter}
        :param attributes_json: The attributes for the storage bucket. The "region" attribute field is required when creating an AWS storage bucket. Values are either encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" or remove the block to clear all attributes in the storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#attributes_json StorageBucket#attributes_json}
        :param bucket_prefix: The prefix used to organize the data held within the external object store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#bucket_prefix StorageBucket#bucket_prefix}
        :param description: The storage bucket description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#description StorageBucket#description}
        :param name: The storage bucket name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#name StorageBucket#name}
        :param plugin_id: The ID of the plugin that should back the resource. This or plugin_name must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#plugin_id StorageBucket#plugin_id}
        :param plugin_name: The name of the plugin that should back the resource. This or plugin_id must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#plugin_name StorageBucket#plugin_name}
        :param secrets_json: The secrets for the storage bucket. Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" to clear any existing values. NOTE: Unlike "attributes_json", removing this block will NOT clear secrets from the storage bucket; this allows injecting secrets for one call, then removing them for storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#secrets_json StorageBucket#secrets_json}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c63a45d170fccc591d5fae9d77fa19994cca5b07121a2c5124e867f3e3eb454)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = StorageBucketConfig(
            bucket_name=bucket_name,
            scope_id=scope_id,
            worker_filter=worker_filter,
            attributes_json=attributes_json,
            bucket_prefix=bucket_prefix,
            description=description,
            name=name,
            plugin_id=plugin_id,
            plugin_name=plugin_name,
            secrets_json=secrets_json,
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
        '''Generates CDKTF code for importing a StorageBucket resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageBucket to import.
        :param import_from_id: The id of the existing StorageBucket that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageBucket to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a521dcf964a12fb144fc9fbef855bbe75f36ef4ff78e8929bcb445fd5785408e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAttributesJson")
    def reset_attributes_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributesJson", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPluginId")
    def reset_plugin_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginId", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetSecretsJson")
    def reset_secrets_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretsJson", []))

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
    @jsii.member(jsii_name="internalForceUpdate")
    def internal_force_update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalForceUpdate"))

    @builtins.property
    @jsii.member(jsii_name="internalHmacUsedForSecretsConfigHmac")
    def internal_hmac_used_for_secrets_config_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalHmacUsedForSecretsConfigHmac"))

    @builtins.property
    @jsii.member(jsii_name="internalSecretsConfigHmac")
    def internal_secrets_config_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalSecretsConfigHmac"))

    @builtins.property
    @jsii.member(jsii_name="secretsHmac")
    def secrets_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsHmac"))

    @builtins.property
    @jsii.member(jsii_name="attributesJsonInput")
    def attributes_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributesJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginIdInput")
    def plugin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsJsonInput")
    def secrets_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretsJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="workerFilterInput")
    def worker_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesJson")
    def attributes_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributesJson"))

    @attributes_json.setter
    def attributes_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__537e22bc80bcf3a1fc5c33b7eaa9124aef8debd5e083a45ff908bff27162c52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributesJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bc09c359a50976f9c76dd735801497c7309f4aa5ec7758e9c09831ff19b0a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6059516f0e7ba782de8cfba727509b9b1e1af51102fc3185aeb1d7db7f3d1df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad62f029e2e5ac8ce859901f83f4a8050d6bebb33a67302a8359871b7008ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c09bc8e0f85ebadea1e4ebe0217ca0a23b786bd7108a078beb067648ecf094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginId")
    def plugin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginId"))

    @plugin_id.setter
    def plugin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5853726a64357df2073fda469df5984a8033a3a812d0149f0722f36ef3fcea2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf69d7546a3db11314c8de6722574622ff8b51180cffe349d6d62a7d57ce046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa275afa34bb80cb385de7258baaf0c40b2d5fcc5dcd744228b2b2fc020c1f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretsJson")
    def secrets_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsJson"))

    @secrets_json.setter
    def secrets_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d044ef3d441e4c4e1a81130a2ba158781fdc96857d06422cd4e7f6fad447bb66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretsJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerFilter")
    def worker_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerFilter"))

    @worker_filter.setter
    def worker_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05abd97d1341d9b82f60aa487a92d7f911f0f92f3587060fba06b2ec4c23c8b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerFilter", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-boundary.storageBucket.StorageBucketConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket_name": "bucketName",
        "scope_id": "scopeId",
        "worker_filter": "workerFilter",
        "attributes_json": "attributesJson",
        "bucket_prefix": "bucketPrefix",
        "description": "description",
        "name": "name",
        "plugin_id": "pluginId",
        "plugin_name": "pluginName",
        "secrets_json": "secretsJson",
    },
)
class StorageBucketConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket_name: builtins.str,
        scope_id: builtins.str,
        worker_filter: builtins.str,
        attributes_json: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        plugin_id: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        secrets_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket_name: The name of the bucket within the external object store service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#bucket_name StorageBucket#bucket_name}
        :param scope_id: The scope for this storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#scope_id StorageBucket#scope_id}
        :param worker_filter: Filters to the worker(s) that can handle requests for this storage bucket. The filter must match an existing worker in order to create a storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#worker_filter StorageBucket#worker_filter}
        :param attributes_json: The attributes for the storage bucket. The "region" attribute field is required when creating an AWS storage bucket. Values are either encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" or remove the block to clear all attributes in the storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#attributes_json StorageBucket#attributes_json}
        :param bucket_prefix: The prefix used to organize the data held within the external object store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#bucket_prefix StorageBucket#bucket_prefix}
        :param description: The storage bucket description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#description StorageBucket#description}
        :param name: The storage bucket name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#name StorageBucket#name}
        :param plugin_id: The ID of the plugin that should back the resource. This or plugin_name must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#plugin_id StorageBucket#plugin_id}
        :param plugin_name: The name of the plugin that should back the resource. This or plugin_id must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#plugin_name StorageBucket#plugin_name}
        :param secrets_json: The secrets for the storage bucket. Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" to clear any existing values. NOTE: Unlike "attributes_json", removing this block will NOT clear secrets from the storage bucket; this allows injecting secrets for one call, then removing them for storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#secrets_json StorageBucket#secrets_json}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a020f1e42b21ae062f173ab01eff0f31c45b607286cb95c086da3cb32293966f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument scope_id", value=scope_id, expected_type=type_hints["scope_id"])
            check_type(argname="argument worker_filter", value=worker_filter, expected_type=type_hints["worker_filter"])
            check_type(argname="argument attributes_json", value=attributes_json, expected_type=type_hints["attributes_json"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument plugin_id", value=plugin_id, expected_type=type_hints["plugin_id"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument secrets_json", value=secrets_json, expected_type=type_hints["secrets_json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "scope_id": scope_id,
            "worker_filter": worker_filter,
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
        if attributes_json is not None:
            self._values["attributes_json"] = attributes_json
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if plugin_id is not None:
            self._values["plugin_id"] = plugin_id
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if secrets_json is not None:
            self._values["secrets_json"] = secrets_json

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
    def bucket_name(self) -> builtins.str:
        '''The name of the bucket within the external object store service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#bucket_name StorageBucket#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope for this storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#scope_id StorageBucket#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def worker_filter(self) -> builtins.str:
        '''Filters to the worker(s) that can handle requests for this storage bucket.

        The filter must match an existing worker in order to create a storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#worker_filter StorageBucket#worker_filter}
        '''
        result = self._values.get("worker_filter")
        assert result is not None, "Required property 'worker_filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes_json(self) -> typing.Optional[builtins.str]:
        '''The attributes for the storage bucket.

        The "region" attribute field is required when creating an AWS storage bucket. Values are either encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" or remove the block to clear all attributes in the storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#attributes_json StorageBucket#attributes_json}
        '''
        result = self._values.get("attributes_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix used to organize the data held within the external object store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#bucket_prefix StorageBucket#bucket_prefix}
        '''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The storage bucket description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#description StorageBucket#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The storage bucket name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#name StorageBucket#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the plugin that should back the resource. This or plugin_name must be defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#plugin_id StorageBucket#plugin_id}
        '''
        result = self._values.get("plugin_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''The name of the plugin that should back the resource. This or plugin_id must be defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#plugin_name StorageBucket#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_json(self) -> typing.Optional[builtins.str]:
        '''The secrets for the storage bucket.

        Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" to clear any existing values. NOTE: Unlike "attributes_json", removing this block will NOT clear secrets from the storage bucket; this allows injecting secrets for one call, then removing them for storage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/storage_bucket#secrets_json StorageBucket#secrets_json}
        '''
        result = self._values.get("secrets_json")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "StorageBucket",
    "StorageBucketConfig",
]

publication.publish()

def _typecheckingstub__1c63a45d170fccc591d5fae9d77fa19994cca5b07121a2c5124e867f3e3eb454(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: builtins.str,
    scope_id: builtins.str,
    worker_filter: builtins.str,
    attributes_json: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    plugin_id: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    secrets_json: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a521dcf964a12fb144fc9fbef855bbe75f36ef4ff78e8929bcb445fd5785408e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537e22bc80bcf3a1fc5c33b7eaa9124aef8debd5e083a45ff908bff27162c52a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bc09c359a50976f9c76dd735801497c7309f4aa5ec7758e9c09831ff19b0a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6059516f0e7ba782de8cfba727509b9b1e1af51102fc3185aeb1d7db7f3d1df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad62f029e2e5ac8ce859901f83f4a8050d6bebb33a67302a8359871b7008ff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c09bc8e0f85ebadea1e4ebe0217ca0a23b786bd7108a078beb067648ecf094(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5853726a64357df2073fda469df5984a8033a3a812d0149f0722f36ef3fcea2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf69d7546a3db11314c8de6722574622ff8b51180cffe349d6d62a7d57ce046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa275afa34bb80cb385de7258baaf0c40b2d5fcc5dcd744228b2b2fc020c1f08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d044ef3d441e4c4e1a81130a2ba158781fdc96857d06422cd4e7f6fad447bb66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05abd97d1341d9b82f60aa487a92d7f911f0f92f3587060fba06b2ec4c23c8b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a020f1e42b21ae062f173ab01eff0f31c45b607286cb95c086da3cb32293966f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket_name: builtins.str,
    scope_id: builtins.str,
    worker_filter: builtins.str,
    attributes_json: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    plugin_id: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    secrets_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
