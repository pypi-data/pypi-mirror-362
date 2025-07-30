r'''
# `hcp_hvn_route`

Refer to the Terraform Registry for docs: [`hcp_hvn_route`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route).
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


class HvnRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.hvnRoute.HvnRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route hcp_hvn_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination_cidr: builtins.str,
        hvn_link: builtins.str,
        hvn_route_id: builtins.str,
        target_link: builtins.str,
        azure_config: typing.Optional[typing.Union["HvnRouteAzureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["HvnRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route hcp_hvn_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination_cidr: The destination CIDR of the HVN route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#destination_cidr HvnRoute#destination_cidr}
        :param hvn_link: The ``self_link`` of the HashiCorp Virtual Network (HVN). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#hvn_link HvnRoute#hvn_link}
        :param hvn_route_id: The ID of the HVN route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#hvn_route_id HvnRoute#hvn_route_id}
        :param target_link: A unique URL identifying the target of the HVN route. Examples of the target: ```aws_network_peering`` <aws_network_peering.md>`_, ```aws_transit_gateway_attachment`` <aws_transit_gateway_attachment.md>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#target_link HvnRoute#target_link}
        :param azure_config: azure_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#azure_config HvnRoute#azure_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#id HvnRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project_id: The ID of the HCP project where the HVN route is located. Always matches the project ID in ``hvn_link``. Setting this attribute is deprecated, but it will remain usable in read-only form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#project_id HvnRoute#project_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#timeouts HvnRoute#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a17d6b8cf3db69b7342f70da2c474c2d1d7611598e9a7fff081727517345746)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HvnRouteConfig(
            destination_cidr=destination_cidr,
            hvn_link=hvn_link,
            hvn_route_id=hvn_route_id,
            target_link=target_link,
            azure_config=azure_config,
            id=id,
            project_id=project_id,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a HvnRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HvnRoute to import.
        :param import_from_id: The id of the existing HvnRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HvnRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed88b0a40bd57f5a83dd9159a901519c48cb919ff47ef2a83bc67b8416839b80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAzureConfig")
    def put_azure_config(
        self,
        *,
        next_hop_type: builtins.str,
        next_hop_ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param next_hop_type: The type of Azure hop the packet should be sent to. Valid options for Next Hop Type - ``VIRTUAL_APPLIANCE`` or ``VIRTUAL_NETWORK_GATEWAY`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#next_hop_type HvnRoute#next_hop_type}
        :param next_hop_ip_address: Contains the IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is VIRTUAL_APPLIANCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#next_hop_ip_address HvnRoute#next_hop_ip_address}
        '''
        value = HvnRouteAzureConfig(
            next_hop_type=next_hop_type, next_hop_ip_address=next_hop_ip_address
        )

        return typing.cast(None, jsii.invoke(self, "putAzureConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#create HvnRoute#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#default HvnRoute#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#delete HvnRoute#delete}.
        '''
        value = HvnRouteTimeouts(create=create, default=default, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAzureConfig")
    def reset_azure_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="azureConfig")
    def azure_config(self) -> "HvnRouteAzureConfigOutputReference":
        return typing.cast("HvnRouteAzureConfigOutputReference", jsii.get(self, "azureConfig"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HvnRouteTimeoutsOutputReference":
        return typing.cast("HvnRouteTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="azureConfigInput")
    def azure_config_input(self) -> typing.Optional["HvnRouteAzureConfig"]:
        return typing.cast(typing.Optional["HvnRouteAzureConfig"], jsii.get(self, "azureConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationCidrInput")
    def destination_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="hvnLinkInput")
    def hvn_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hvnLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="hvnRouteIdInput")
    def hvn_route_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hvnRouteIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetLinkInput")
    def target_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HvnRouteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HvnRouteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationCidr")
    def destination_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationCidr"))

    @destination_cidr.setter
    def destination_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9e54d9ff0c25dc1f1cb4902ccd6d30f010d64704c3318fdd368ea9bcbc7af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hvnLink")
    def hvn_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hvnLink"))

    @hvn_link.setter
    def hvn_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bf3c339aa87cb6cf9e1aa5514a14a9054c44a02f4fc1fc2551ca3d8c1f3968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hvnLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hvnRouteId")
    def hvn_route_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hvnRouteId"))

    @hvn_route_id.setter
    def hvn_route_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476e4cd36b551871725bf628ba44765524cd4e581d6a66d0b64b254a5f73c7c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hvnRouteId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814a0ed126b8900e8fc119cf255c6c2b059877d571ac1f4c9dfc3344a38bbeb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ceb0f388c3e97e31dd02ae237e5266c665472c0b2fa6bb371dd85e603f3153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetLink")
    def target_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetLink"))

    @target_link.setter
    def target_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9509f91d22ed6edebfeba29a3d564c1df05a2ee9b04281706fdba99514e5a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetLink", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.hvnRoute.HvnRouteAzureConfig",
    jsii_struct_bases=[],
    name_mapping={
        "next_hop_type": "nextHopType",
        "next_hop_ip_address": "nextHopIpAddress",
    },
)
class HvnRouteAzureConfig:
    def __init__(
        self,
        *,
        next_hop_type: builtins.str,
        next_hop_ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param next_hop_type: The type of Azure hop the packet should be sent to. Valid options for Next Hop Type - ``VIRTUAL_APPLIANCE`` or ``VIRTUAL_NETWORK_GATEWAY`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#next_hop_type HvnRoute#next_hop_type}
        :param next_hop_ip_address: Contains the IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is VIRTUAL_APPLIANCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#next_hop_ip_address HvnRoute#next_hop_ip_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2929b04f73fd48476737189c89f21fca0b54cd0e99e77e3ff3e92be261001e)
            check_type(argname="argument next_hop_type", value=next_hop_type, expected_type=type_hints["next_hop_type"])
            check_type(argname="argument next_hop_ip_address", value=next_hop_ip_address, expected_type=type_hints["next_hop_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "next_hop_type": next_hop_type,
        }
        if next_hop_ip_address is not None:
            self._values["next_hop_ip_address"] = next_hop_ip_address

    @builtins.property
    def next_hop_type(self) -> builtins.str:
        '''The type of Azure hop the packet should be sent to.

        Valid options for Next Hop Type - ``VIRTUAL_APPLIANCE`` or ``VIRTUAL_NETWORK_GATEWAY``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#next_hop_type HvnRoute#next_hop_type}
        '''
        result = self._values.get("next_hop_type")
        assert result is not None, "Required property 'next_hop_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def next_hop_ip_address(self) -> typing.Optional[builtins.str]:
        '''Contains the IP address packets should be forwarded to.

        Next hop values are only allowed in routes where the next hop type is VIRTUAL_APPLIANCE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#next_hop_ip_address HvnRoute#next_hop_ip_address}
        '''
        result = self._values.get("next_hop_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HvnRouteAzureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HvnRouteAzureConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.hvnRoute.HvnRouteAzureConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20917ad05b736c136e9b44b6dd96e5be9092ab926bff3c60fa610f304e15b329)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNextHopIpAddress")
    def reset_next_hop_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopIpAddress", []))

    @builtins.property
    @jsii.member(jsii_name="nextHopIpAddressInput")
    def next_hop_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopTypeInput")
    def next_hop_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopIpAddress")
    def next_hop_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopIpAddress"))

    @next_hop_ip_address.setter
    def next_hop_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df61b7c331c62c26d641d972a6bd00934f4cc9a033915870fa9d2b97c86e826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopType")
    def next_hop_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopType"))

    @next_hop_type.setter
    def next_hop_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d48ad2d16f59546564de92bad3dac97d2173e5bdda65d2d602d730fc097c310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HvnRouteAzureConfig]:
        return typing.cast(typing.Optional[HvnRouteAzureConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[HvnRouteAzureConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f97847fffc4649e31d0e717d839a85faa681d0507dfb9dff7f4168139bb18ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.hvnRoute.HvnRouteConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination_cidr": "destinationCidr",
        "hvn_link": "hvnLink",
        "hvn_route_id": "hvnRouteId",
        "target_link": "targetLink",
        "azure_config": "azureConfig",
        "id": "id",
        "project_id": "projectId",
        "timeouts": "timeouts",
    },
)
class HvnRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination_cidr: builtins.str,
        hvn_link: builtins.str,
        hvn_route_id: builtins.str,
        target_link: builtins.str,
        azure_config: typing.Optional[typing.Union[HvnRouteAzureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["HvnRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination_cidr: The destination CIDR of the HVN route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#destination_cidr HvnRoute#destination_cidr}
        :param hvn_link: The ``self_link`` of the HashiCorp Virtual Network (HVN). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#hvn_link HvnRoute#hvn_link}
        :param hvn_route_id: The ID of the HVN route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#hvn_route_id HvnRoute#hvn_route_id}
        :param target_link: A unique URL identifying the target of the HVN route. Examples of the target: ```aws_network_peering`` <aws_network_peering.md>`_, ```aws_transit_gateway_attachment`` <aws_transit_gateway_attachment.md>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#target_link HvnRoute#target_link}
        :param azure_config: azure_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#azure_config HvnRoute#azure_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#id HvnRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project_id: The ID of the HCP project where the HVN route is located. Always matches the project ID in ``hvn_link``. Setting this attribute is deprecated, but it will remain usable in read-only form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#project_id HvnRoute#project_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#timeouts HvnRoute#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(azure_config, dict):
            azure_config = HvnRouteAzureConfig(**azure_config)
        if isinstance(timeouts, dict):
            timeouts = HvnRouteTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f8a11ad97253aa3b4db1898b778709d07fdea552ee920fe7548e933e30e5f3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument hvn_link", value=hvn_link, expected_type=type_hints["hvn_link"])
            check_type(argname="argument hvn_route_id", value=hvn_route_id, expected_type=type_hints["hvn_route_id"])
            check_type(argname="argument target_link", value=target_link, expected_type=type_hints["target_link"])
            check_type(argname="argument azure_config", value=azure_config, expected_type=type_hints["azure_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_cidr": destination_cidr,
            "hvn_link": hvn_link,
            "hvn_route_id": hvn_route_id,
            "target_link": target_link,
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
        if azure_config is not None:
            self._values["azure_config"] = azure_config
        if id is not None:
            self._values["id"] = id
        if project_id is not None:
            self._values["project_id"] = project_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def destination_cidr(self) -> builtins.str:
        '''The destination CIDR of the HVN route.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#destination_cidr HvnRoute#destination_cidr}
        '''
        result = self._values.get("destination_cidr")
        assert result is not None, "Required property 'destination_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hvn_link(self) -> builtins.str:
        '''The ``self_link`` of the HashiCorp Virtual Network (HVN).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#hvn_link HvnRoute#hvn_link}
        '''
        result = self._values.get("hvn_link")
        assert result is not None, "Required property 'hvn_link' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hvn_route_id(self) -> builtins.str:
        '''The ID of the HVN route.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#hvn_route_id HvnRoute#hvn_route_id}
        '''
        result = self._values.get("hvn_route_id")
        assert result is not None, "Required property 'hvn_route_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_link(self) -> builtins.str:
        '''A unique URL identifying the target of the HVN route. Examples of the target: ```aws_network_peering`` <aws_network_peering.md>`_, ```aws_transit_gateway_attachment`` <aws_transit_gateway_attachment.md>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#target_link HvnRoute#target_link}
        '''
        result = self._values.get("target_link")
        assert result is not None, "Required property 'target_link' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def azure_config(self) -> typing.Optional[HvnRouteAzureConfig]:
        '''azure_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#azure_config HvnRoute#azure_config}
        '''
        result = self._values.get("azure_config")
        return typing.cast(typing.Optional[HvnRouteAzureConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#id HvnRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the HCP project where the HVN route is located.

        Always matches the project ID in ``hvn_link``. Setting this attribute is deprecated, but it will remain usable in read-only form.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#project_id HvnRoute#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HvnRouteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#timeouts HvnRoute#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HvnRouteTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HvnRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.hvnRoute.HvnRouteTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "default": "default", "delete": "delete"},
)
class HvnRouteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#create HvnRoute#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#default HvnRoute#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#delete HvnRoute#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7530df28c80a750f79162999178fa310eed9eb7c994ca81b4125415b6563456)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if default is not None:
            self._values["default"] = default
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#create HvnRoute#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#default HvnRoute#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/hvn_route#delete HvnRoute#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HvnRouteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HvnRouteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.hvnRoute.HvnRouteTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1f97ab1af4061452a808fd4c975168cc528b0b07ed5bc50b193b7f6b9bf89f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43af6be95b0212e893e55f68b02652485eb6a9600db72dc93729c83f27363079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @default.setter
    def default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de3b04ca1058744988b9dcdcc913790323dabfebc326ef626467a956a5086ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9a4c69b9870a24e0632381de585b5fb99537cba3ffba103bc7b803905aabaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HvnRouteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HvnRouteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HvnRouteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da6313a3e738335a80309b378e5bd9531ef61b3b919209eb26fa623b1e148b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HvnRoute",
    "HvnRouteAzureConfig",
    "HvnRouteAzureConfigOutputReference",
    "HvnRouteConfig",
    "HvnRouteTimeouts",
    "HvnRouteTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1a17d6b8cf3db69b7342f70da2c474c2d1d7611598e9a7fff081727517345746(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination_cidr: builtins.str,
    hvn_link: builtins.str,
    hvn_route_id: builtins.str,
    target_link: builtins.str,
    azure_config: typing.Optional[typing.Union[HvnRouteAzureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[HvnRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ed88b0a40bd57f5a83dd9159a901519c48cb919ff47ef2a83bc67b8416839b80(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9e54d9ff0c25dc1f1cb4902ccd6d30f010d64704c3318fdd368ea9bcbc7af1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bf3c339aa87cb6cf9e1aa5514a14a9054c44a02f4fc1fc2551ca3d8c1f3968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476e4cd36b551871725bf628ba44765524cd4e581d6a66d0b64b254a5f73c7c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814a0ed126b8900e8fc119cf255c6c2b059877d571ac1f4c9dfc3344a38bbeb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ceb0f388c3e97e31dd02ae237e5266c665472c0b2fa6bb371dd85e603f3153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9509f91d22ed6edebfeba29a3d564c1df05a2ee9b04281706fdba99514e5a6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2929b04f73fd48476737189c89f21fca0b54cd0e99e77e3ff3e92be261001e(
    *,
    next_hop_type: builtins.str,
    next_hop_ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20917ad05b736c136e9b44b6dd96e5be9092ab926bff3c60fa610f304e15b329(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df61b7c331c62c26d641d972a6bd00934f4cc9a033915870fa9d2b97c86e826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d48ad2d16f59546564de92bad3dac97d2173e5bdda65d2d602d730fc097c310(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97847fffc4649e31d0e717d839a85faa681d0507dfb9dff7f4168139bb18ee3(
    value: typing.Optional[HvnRouteAzureConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f8a11ad97253aa3b4db1898b778709d07fdea552ee920fe7548e933e30e5f3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination_cidr: builtins.str,
    hvn_link: builtins.str,
    hvn_route_id: builtins.str,
    target_link: builtins.str,
    azure_config: typing.Optional[typing.Union[HvnRouteAzureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[HvnRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7530df28c80a750f79162999178fa310eed9eb7c994ca81b4125415b6563456(
    *,
    create: typing.Optional[builtins.str] = None,
    default: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1f97ab1af4061452a808fd4c975168cc528b0b07ed5bc50b193b7f6b9bf89f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43af6be95b0212e893e55f68b02652485eb6a9600db72dc93729c83f27363079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de3b04ca1058744988b9dcdcc913790323dabfebc326ef626467a956a5086ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9a4c69b9870a24e0632381de585b5fb99537cba3ffba103bc7b803905aabaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da6313a3e738335a80309b378e5bd9531ef61b3b919209eb26fa623b1e148b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HvnRouteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
