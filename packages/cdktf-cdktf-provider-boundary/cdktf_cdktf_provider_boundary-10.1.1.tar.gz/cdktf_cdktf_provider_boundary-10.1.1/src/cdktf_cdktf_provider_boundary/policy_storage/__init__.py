r'''
# `boundary_policy_storage`

Refer to the Terraform Registry for docs: [`boundary_policy_storage`](https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage).
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


class PolicyStorage(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-boundary.policyStorage.PolicyStorage",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage boundary_policy_storage}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        delete_after_days: typing.Optional[jsii.Number] = None,
        delete_after_overridable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        retain_for_days: typing.Optional[jsii.Number] = None,
        retain_for_overridable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage boundary_policy_storage} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#scope_id PolicyStorage#scope_id}
        :param delete_after_days: The number of days after which a session recording will be automatically deleted. Defaults to 0: never automatically delete. However, delete_after_days and retain_for_days cannot both be 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#delete_after_days PolicyStorage#delete_after_days}
        :param delete_after_overridable: Whether or not the associated delete_after_days value can be overridden by org scopes. Note: if the associated delete_after_days value is 0, overridable is ignored Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#delete_after_overridable PolicyStorage#delete_after_overridable}
        :param description: The policy description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#description PolicyStorage#description}
        :param name: The policy name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#name PolicyStorage#name}
        :param retain_for_days: The number of days a session recording is required to be stored. Defaults to 0: allow deletions at any time. However, retain_for_days and delete_after_days cannot both be 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#retain_for_days PolicyStorage#retain_for_days}
        :param retain_for_overridable: Whether or not the associated retain_for_days value can be overridden by org scopes. Note: if the associated retain_for_days value is 0, overridable is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#retain_for_overridable PolicyStorage#retain_for_overridable}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb1ab42baa72ad738197bb1907783796a995d91ca0f741ddda7f704f21bf311)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = PolicyStorageConfig(
            scope_id=scope_id,
            delete_after_days=delete_after_days,
            delete_after_overridable=delete_after_overridable,
            description=description,
            name=name,
            retain_for_days=retain_for_days,
            retain_for_overridable=retain_for_overridable,
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
        '''Generates CDKTF code for importing a PolicyStorage resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PolicyStorage to import.
        :param import_from_id: The id of the existing PolicyStorage that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PolicyStorage to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c75bf8f3147c7fb5aa36d7e82817096180aeaa7b44abe9fcb2252525ce97ff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDeleteAfterDays")
    def reset_delete_after_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfterDays", []))

    @jsii.member(jsii_name="resetDeleteAfterOverridable")
    def reset_delete_after_overridable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfterOverridable", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRetainForDays")
    def reset_retain_for_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainForDays", []))

    @jsii.member(jsii_name="resetRetainForOverridable")
    def reset_retain_for_overridable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainForOverridable", []))

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
    @jsii.member(jsii_name="deleteAfterDaysInput")
    def delete_after_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterOverridableInput")
    def delete_after_overridable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteAfterOverridableInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="retainForDaysInput")
    def retain_for_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retainForDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="retainForOverridableInput")
    def retain_for_overridable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retainForOverridableInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDays")
    def delete_after_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfterDays"))

    @delete_after_days.setter
    def delete_after_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678350e03669779f9b0716808607aff9ce5f6c6d490b5f3ebaec70a5bea82696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfterDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfterOverridable")
    def delete_after_overridable(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteAfterOverridable"))

    @delete_after_overridable.setter
    def delete_after_overridable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36739855be62816ebe7dadc7980ce121b56bb2ef8a5d7ddbd813bd4ab175772b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfterOverridable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca1d6a259946badddd6b358ed5b193e80af43965f31d1f676ac4c76625153a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a1a04051abe8946f89043314f8de3f2cbccdcfc2b85db677ecf5e727ca1a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retainForDays")
    def retain_for_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retainForDays"))

    @retain_for_days.setter
    def retain_for_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd977e78f2d931ac349dbb5b1510ed4b366cf6d629d112ecfe4f8a9cf35d89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainForDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retainForOverridable")
    def retain_for_overridable(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retainForOverridable"))

    @retain_for_overridable.setter
    def retain_for_overridable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34bdcfa8e3e0f741a13540ffc647c7476bb047f94058b6cacec87f60bc619b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainForOverridable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab80c4b0aa040462a01a1f2744b72971f6039b5c0866500d4a8dbc008e186db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-boundary.policyStorage.PolicyStorageConfig",
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
        "delete_after_days": "deleteAfterDays",
        "delete_after_overridable": "deleteAfterOverridable",
        "description": "description",
        "name": "name",
        "retain_for_days": "retainForDays",
        "retain_for_overridable": "retainForOverridable",
    },
)
class PolicyStorageConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        delete_after_days: typing.Optional[jsii.Number] = None,
        delete_after_overridable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        retain_for_days: typing.Optional[jsii.Number] = None,
        retain_for_overridable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param scope_id: The scope for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#scope_id PolicyStorage#scope_id}
        :param delete_after_days: The number of days after which a session recording will be automatically deleted. Defaults to 0: never automatically delete. However, delete_after_days and retain_for_days cannot both be 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#delete_after_days PolicyStorage#delete_after_days}
        :param delete_after_overridable: Whether or not the associated delete_after_days value can be overridden by org scopes. Note: if the associated delete_after_days value is 0, overridable is ignored Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#delete_after_overridable PolicyStorage#delete_after_overridable}
        :param description: The policy description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#description PolicyStorage#description}
        :param name: The policy name. Defaults to the resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#name PolicyStorage#name}
        :param retain_for_days: The number of days a session recording is required to be stored. Defaults to 0: allow deletions at any time. However, retain_for_days and delete_after_days cannot both be 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#retain_for_days PolicyStorage#retain_for_days}
        :param retain_for_overridable: Whether or not the associated retain_for_days value can be overridden by org scopes. Note: if the associated retain_for_days value is 0, overridable is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#retain_for_overridable PolicyStorage#retain_for_overridable}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519301c29b552d4e0821e56bbdacfda01b364f1414a77b8290d03dc707029bc0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument scope_id", value=scope_id, expected_type=type_hints["scope_id"])
            check_type(argname="argument delete_after_days", value=delete_after_days, expected_type=type_hints["delete_after_days"])
            check_type(argname="argument delete_after_overridable", value=delete_after_overridable, expected_type=type_hints["delete_after_overridable"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument retain_for_days", value=retain_for_days, expected_type=type_hints["retain_for_days"])
            check_type(argname="argument retain_for_overridable", value=retain_for_overridable, expected_type=type_hints["retain_for_overridable"])
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
        if delete_after_days is not None:
            self._values["delete_after_days"] = delete_after_days
        if delete_after_overridable is not None:
            self._values["delete_after_overridable"] = delete_after_overridable
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if retain_for_days is not None:
            self._values["retain_for_days"] = retain_for_days
        if retain_for_overridable is not None:
            self._values["retain_for_overridable"] = retain_for_overridable

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
        '''The scope for this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#scope_id PolicyStorage#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_after_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days after which a session recording will be automatically deleted.

        Defaults to 0: never automatically delete. However, delete_after_days and retain_for_days cannot both be 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#delete_after_days PolicyStorage#delete_after_days}
        '''
        result = self._values.get("delete_after_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_after_overridable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the associated delete_after_days value can be overridden by org scopes.

        Note: if the associated delete_after_days value is 0, overridable is ignored

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#delete_after_overridable PolicyStorage#delete_after_overridable}
        '''
        result = self._values.get("delete_after_overridable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The policy description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#description PolicyStorage#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The policy name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#name PolicyStorage#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retain_for_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days a session recording is required to be stored.

        Defaults to 0: allow deletions at any time. However, retain_for_days and delete_after_days cannot both be 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#retain_for_days PolicyStorage#retain_for_days}
        '''
        result = self._values.get("retain_for_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retain_for_overridable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the associated retain_for_days value can be overridden by org scopes.

        Note: if the associated retain_for_days value is 0, overridable is ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/boundary/1.3.1/docs/resources/policy_storage#retain_for_overridable PolicyStorage#retain_for_overridable}
        '''
        result = self._values.get("retain_for_overridable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PolicyStorage",
    "PolicyStorageConfig",
]

publication.publish()

def _typecheckingstub__4cb1ab42baa72ad738197bb1907783796a995d91ca0f741ddda7f704f21bf311(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    scope_id: builtins.str,
    delete_after_days: typing.Optional[jsii.Number] = None,
    delete_after_overridable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    retain_for_days: typing.Optional[jsii.Number] = None,
    retain_for_overridable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__71c75bf8f3147c7fb5aa36d7e82817096180aeaa7b44abe9fcb2252525ce97ff(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678350e03669779f9b0716808607aff9ce5f6c6d490b5f3ebaec70a5bea82696(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36739855be62816ebe7dadc7980ce121b56bb2ef8a5d7ddbd813bd4ab175772b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca1d6a259946badddd6b358ed5b193e80af43965f31d1f676ac4c76625153a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a1a04051abe8946f89043314f8de3f2cbccdcfc2b85db677ecf5e727ca1a89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd977e78f2d931ac349dbb5b1510ed4b366cf6d629d112ecfe4f8a9cf35d89e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34bdcfa8e3e0f741a13540ffc647c7476bb047f94058b6cacec87f60bc619b2f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab80c4b0aa040462a01a1f2744b72971f6039b5c0866500d4a8dbc008e186db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519301c29b552d4e0821e56bbdacfda01b364f1414a77b8290d03dc707029bc0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scope_id: builtins.str,
    delete_after_days: typing.Optional[jsii.Number] = None,
    delete_after_overridable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    retain_for_days: typing.Optional[jsii.Number] = None,
    retain_for_overridable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
