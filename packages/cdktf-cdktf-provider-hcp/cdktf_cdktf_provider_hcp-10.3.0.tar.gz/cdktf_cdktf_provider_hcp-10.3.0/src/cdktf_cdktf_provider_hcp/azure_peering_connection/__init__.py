r'''
# `hcp_azure_peering_connection`

Refer to the Terraform Registry for docs: [`hcp_azure_peering_connection`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection).
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


class AzurePeeringConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.azurePeeringConnection.AzurePeeringConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection hcp_azure_peering_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hvn_link: builtins.str,
        peering_id: builtins.str,
        peer_resource_group_name: builtins.str,
        peer_subscription_id: builtins.str,
        peer_tenant_id: builtins.str,
        peer_vnet_name: builtins.str,
        peer_vnet_region: builtins.str,
        allow_forwarded_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AzurePeeringConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_remote_gateways: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection hcp_azure_peering_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hvn_link: The ``self_link`` of the HashiCorp Virtual Network (HVN). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#hvn_link AzurePeeringConnection#hvn_link}
        :param peering_id: The ID of the peering connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peering_id AzurePeeringConnection#peering_id}
        :param peer_resource_group_name: The resource group name of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_resource_group_name AzurePeeringConnection#peer_resource_group_name}
        :param peer_subscription_id: The subscription ID of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_subscription_id AzurePeeringConnection#peer_subscription_id}
        :param peer_tenant_id: The tenant ID of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_tenant_id AzurePeeringConnection#peer_tenant_id}
        :param peer_vnet_name: The name of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_vnet_name AzurePeeringConnection#peer_vnet_name}
        :param peer_vnet_region: The region of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_vnet_region AzurePeeringConnection#peer_vnet_region}
        :param allow_forwarded_traffic: Whether the forwarded traffic originating from the peered VNet is allowed in the HVN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#allow_forwarded_traffic AzurePeeringConnection#allow_forwarded_traffic}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#id AzurePeeringConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#timeouts AzurePeeringConnection#timeouts}
        :param use_remote_gateways: If the HVN should use the gateway of the peered VNet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#use_remote_gateways AzurePeeringConnection#use_remote_gateways}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d399aa42028deb2786e92e0cceb7ef03d3d7f8b59aa15cd55d0a7a0b8165da1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AzurePeeringConnectionConfig(
            hvn_link=hvn_link,
            peering_id=peering_id,
            peer_resource_group_name=peer_resource_group_name,
            peer_subscription_id=peer_subscription_id,
            peer_tenant_id=peer_tenant_id,
            peer_vnet_name=peer_vnet_name,
            peer_vnet_region=peer_vnet_region,
            allow_forwarded_traffic=allow_forwarded_traffic,
            id=id,
            timeouts=timeouts,
            use_remote_gateways=use_remote_gateways,
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
        '''Generates CDKTF code for importing a AzurePeeringConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AzurePeeringConnection to import.
        :param import_from_id: The id of the existing AzurePeeringConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AzurePeeringConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785e185019803f6b17db683303fc44df6bffa4fde8b5b4e3db0d514d80eb40f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#create AzurePeeringConnection#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#default AzurePeeringConnection#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#delete AzurePeeringConnection#delete}.
        '''
        value = AzurePeeringConnectionTimeouts(
            create=create, default=default, delete=delete
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowForwardedTraffic")
    def reset_allow_forwarded_traffic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowForwardedTraffic", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUseRemoteGateways")
    def reset_use_remote_gateways(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseRemoteGateways", []))

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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @builtins.property
    @jsii.member(jsii_name="azurePeeringId")
    def azure_peering_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azurePeeringId"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="expiresAt")
    def expires_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiresAt"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

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
    def timeouts(self) -> "AzurePeeringConnectionTimeoutsOutputReference":
        return typing.cast("AzurePeeringConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allowForwardedTrafficInput")
    def allow_forwarded_traffic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowForwardedTrafficInput"))

    @builtins.property
    @jsii.member(jsii_name="hvnLinkInput")
    def hvn_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hvnLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="peeringIdInput")
    def peering_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeringIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerResourceGroupNameInput")
    def peer_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerSubscriptionIdInput")
    def peer_subscription_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerSubscriptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerTenantIdInput")
    def peer_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerVnetNameInput")
    def peer_vnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerVnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerVnetRegionInput")
    def peer_vnet_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerVnetRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AzurePeeringConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AzurePeeringConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="useRemoteGatewaysInput")
    def use_remote_gateways_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useRemoteGatewaysInput"))

    @builtins.property
    @jsii.member(jsii_name="allowForwardedTraffic")
    def allow_forwarded_traffic(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowForwardedTraffic"))

    @allow_forwarded_traffic.setter
    def allow_forwarded_traffic(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e97e1b6aa90f3329c4b68bf72da5822876c1c76c3763973774f5136a18b506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowForwardedTraffic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hvnLink")
    def hvn_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hvnLink"))

    @hvn_link.setter
    def hvn_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3054ee7a5e7cf87fe9d00b3d49ac1fdc3bb7b729c487b4768d93fa20e66fa3a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hvnLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37694bbf009cddf2f27f0217f93aa3605101cb773bc6cf8622ab05332ea13d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peeringId")
    def peering_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeringId"))

    @peering_id.setter
    def peering_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95cec1030beb5767496b0a5d077a4ed752c5c9b7c2b39746a25f37a181bb3ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeringId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerResourceGroupName")
    def peer_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerResourceGroupName"))

    @peer_resource_group_name.setter
    def peer_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383620db23a3ab56c321e1e10718ab3ce8d29fc555874dcbbe13dd0bf40ee7c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerResourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerSubscriptionId")
    def peer_subscription_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerSubscriptionId"))

    @peer_subscription_id.setter
    def peer_subscription_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35644b35f38dbc172aa99cecd85b8ed5022aba920ca8ab71161ec078dcbf1c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerSubscriptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerTenantId")
    def peer_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerTenantId"))

    @peer_tenant_id.setter
    def peer_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe7f4dc984763dc29f8e01bdb4fa5ef128cd8a0d197e657969f97c1b310cc25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerVnetName")
    def peer_vnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerVnetName"))

    @peer_vnet_name.setter
    def peer_vnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ddd19187756a01226d8e55304b90041f482bc03137b577cf28b43dada8c1dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerVnetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerVnetRegion")
    def peer_vnet_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerVnetRegion"))

    @peer_vnet_region.setter
    def peer_vnet_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056beb5f9bcf71391515462dc8deb4306d7fdfc4fdd77b326615475647cd369a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerVnetRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useRemoteGateways")
    def use_remote_gateways(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useRemoteGateways"))

    @use_remote_gateways.setter
    def use_remote_gateways(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9651f213ef9fbdc69e65ea69ff2a3ecce935d5dce8fd4f3d686b650633c1fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useRemoteGateways", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.azurePeeringConnection.AzurePeeringConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hvn_link": "hvnLink",
        "peering_id": "peeringId",
        "peer_resource_group_name": "peerResourceGroupName",
        "peer_subscription_id": "peerSubscriptionId",
        "peer_tenant_id": "peerTenantId",
        "peer_vnet_name": "peerVnetName",
        "peer_vnet_region": "peerVnetRegion",
        "allow_forwarded_traffic": "allowForwardedTraffic",
        "id": "id",
        "timeouts": "timeouts",
        "use_remote_gateways": "useRemoteGateways",
    },
)
class AzurePeeringConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hvn_link: builtins.str,
        peering_id: builtins.str,
        peer_resource_group_name: builtins.str,
        peer_subscription_id: builtins.str,
        peer_tenant_id: builtins.str,
        peer_vnet_name: builtins.str,
        peer_vnet_region: builtins.str,
        allow_forwarded_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AzurePeeringConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_remote_gateways: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hvn_link: The ``self_link`` of the HashiCorp Virtual Network (HVN). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#hvn_link AzurePeeringConnection#hvn_link}
        :param peering_id: The ID of the peering connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peering_id AzurePeeringConnection#peering_id}
        :param peer_resource_group_name: The resource group name of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_resource_group_name AzurePeeringConnection#peer_resource_group_name}
        :param peer_subscription_id: The subscription ID of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_subscription_id AzurePeeringConnection#peer_subscription_id}
        :param peer_tenant_id: The tenant ID of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_tenant_id AzurePeeringConnection#peer_tenant_id}
        :param peer_vnet_name: The name of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_vnet_name AzurePeeringConnection#peer_vnet_name}
        :param peer_vnet_region: The region of the peer VNet in Azure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_vnet_region AzurePeeringConnection#peer_vnet_region}
        :param allow_forwarded_traffic: Whether the forwarded traffic originating from the peered VNet is allowed in the HVN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#allow_forwarded_traffic AzurePeeringConnection#allow_forwarded_traffic}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#id AzurePeeringConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#timeouts AzurePeeringConnection#timeouts}
        :param use_remote_gateways: If the HVN should use the gateway of the peered VNet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#use_remote_gateways AzurePeeringConnection#use_remote_gateways}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = AzurePeeringConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdeca02ceccf49e104c97dbf97368fcb5bf7c3b9bdbe2658f3fe03d7beaf4990)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument hvn_link", value=hvn_link, expected_type=type_hints["hvn_link"])
            check_type(argname="argument peering_id", value=peering_id, expected_type=type_hints["peering_id"])
            check_type(argname="argument peer_resource_group_name", value=peer_resource_group_name, expected_type=type_hints["peer_resource_group_name"])
            check_type(argname="argument peer_subscription_id", value=peer_subscription_id, expected_type=type_hints["peer_subscription_id"])
            check_type(argname="argument peer_tenant_id", value=peer_tenant_id, expected_type=type_hints["peer_tenant_id"])
            check_type(argname="argument peer_vnet_name", value=peer_vnet_name, expected_type=type_hints["peer_vnet_name"])
            check_type(argname="argument peer_vnet_region", value=peer_vnet_region, expected_type=type_hints["peer_vnet_region"])
            check_type(argname="argument allow_forwarded_traffic", value=allow_forwarded_traffic, expected_type=type_hints["allow_forwarded_traffic"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument use_remote_gateways", value=use_remote_gateways, expected_type=type_hints["use_remote_gateways"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hvn_link": hvn_link,
            "peering_id": peering_id,
            "peer_resource_group_name": peer_resource_group_name,
            "peer_subscription_id": peer_subscription_id,
            "peer_tenant_id": peer_tenant_id,
            "peer_vnet_name": peer_vnet_name,
            "peer_vnet_region": peer_vnet_region,
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
        if allow_forwarded_traffic is not None:
            self._values["allow_forwarded_traffic"] = allow_forwarded_traffic
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if use_remote_gateways is not None:
            self._values["use_remote_gateways"] = use_remote_gateways

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
    def hvn_link(self) -> builtins.str:
        '''The ``self_link`` of the HashiCorp Virtual Network (HVN).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#hvn_link AzurePeeringConnection#hvn_link}
        '''
        result = self._values.get("hvn_link")
        assert result is not None, "Required property 'hvn_link' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peering_id(self) -> builtins.str:
        '''The ID of the peering connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peering_id AzurePeeringConnection#peering_id}
        '''
        result = self._values.get("peering_id")
        assert result is not None, "Required property 'peering_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_resource_group_name(self) -> builtins.str:
        '''The resource group name of the peer VNet in Azure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_resource_group_name AzurePeeringConnection#peer_resource_group_name}
        '''
        result = self._values.get("peer_resource_group_name")
        assert result is not None, "Required property 'peer_resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_subscription_id(self) -> builtins.str:
        '''The subscription ID of the peer VNet in Azure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_subscription_id AzurePeeringConnection#peer_subscription_id}
        '''
        result = self._values.get("peer_subscription_id")
        assert result is not None, "Required property 'peer_subscription_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_tenant_id(self) -> builtins.str:
        '''The tenant ID of the peer VNet in Azure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_tenant_id AzurePeeringConnection#peer_tenant_id}
        '''
        result = self._values.get("peer_tenant_id")
        assert result is not None, "Required property 'peer_tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_vnet_name(self) -> builtins.str:
        '''The name of the peer VNet in Azure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_vnet_name AzurePeeringConnection#peer_vnet_name}
        '''
        result = self._values.get("peer_vnet_name")
        assert result is not None, "Required property 'peer_vnet_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_vnet_region(self) -> builtins.str:
        '''The region of the peer VNet in Azure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#peer_vnet_region AzurePeeringConnection#peer_vnet_region}
        '''
        result = self._values.get("peer_vnet_region")
        assert result is not None, "Required property 'peer_vnet_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_forwarded_traffic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the forwarded traffic originating from the peered VNet is allowed in the HVN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#allow_forwarded_traffic AzurePeeringConnection#allow_forwarded_traffic}
        '''
        result = self._values.get("allow_forwarded_traffic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#id AzurePeeringConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AzurePeeringConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#timeouts AzurePeeringConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AzurePeeringConnectionTimeouts"], result)

    @builtins.property
    def use_remote_gateways(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the HVN should use the gateway of the peered VNet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#use_remote_gateways AzurePeeringConnection#use_remote_gateways}
        '''
        result = self._values.get("use_remote_gateways")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurePeeringConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.azurePeeringConnection.AzurePeeringConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "default": "default", "delete": "delete"},
)
class AzurePeeringConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#create AzurePeeringConnection#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#default AzurePeeringConnection#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#delete AzurePeeringConnection#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__127f56bb37ab835fef1b18188f7621a124d0fb401d1e629d1300d24f99ad3d39)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#create AzurePeeringConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#default AzurePeeringConnection#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/azure_peering_connection#delete AzurePeeringConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurePeeringConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AzurePeeringConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.azurePeeringConnection.AzurePeeringConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de06caedb075d8d19ea645ec3e13b04d529215405a243af116f0428e862fc366)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38a8e76e7a3512daf4b534950dbd9d275ae378c6f2cdb318088ec4f426639ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @default.setter
    def default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd499f2873dbbe4ac74344bbe2ed4a398b3767a85093ce69f05a0afd28c12b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652fbf5b94f495557f8dd8cbaef3f753db0ad058b606704ce75e4f8c339f3300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzurePeeringConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzurePeeringConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzurePeeringConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d75cb149349ab690e23812d26049a41a9bcffec61cf834c97bbdc509fcc3de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AzurePeeringConnection",
    "AzurePeeringConnectionConfig",
    "AzurePeeringConnectionTimeouts",
    "AzurePeeringConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6d399aa42028deb2786e92e0cceb7ef03d3d7f8b59aa15cd55d0a7a0b8165da1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hvn_link: builtins.str,
    peering_id: builtins.str,
    peer_resource_group_name: builtins.str,
    peer_subscription_id: builtins.str,
    peer_tenant_id: builtins.str,
    peer_vnet_name: builtins.str,
    peer_vnet_region: builtins.str,
    allow_forwarded_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AzurePeeringConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_remote_gateways: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__785e185019803f6b17db683303fc44df6bffa4fde8b5b4e3db0d514d80eb40f9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e97e1b6aa90f3329c4b68bf72da5822876c1c76c3763973774f5136a18b506(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3054ee7a5e7cf87fe9d00b3d49ac1fdc3bb7b729c487b4768d93fa20e66fa3a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37694bbf009cddf2f27f0217f93aa3605101cb773bc6cf8622ab05332ea13d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95cec1030beb5767496b0a5d077a4ed752c5c9b7c2b39746a25f37a181bb3ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383620db23a3ab56c321e1e10718ab3ce8d29fc555874dcbbe13dd0bf40ee7c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35644b35f38dbc172aa99cecd85b8ed5022aba920ca8ab71161ec078dcbf1c58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe7f4dc984763dc29f8e01bdb4fa5ef128cd8a0d197e657969f97c1b310cc25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddd19187756a01226d8e55304b90041f482bc03137b577cf28b43dada8c1dab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056beb5f9bcf71391515462dc8deb4306d7fdfc4fdd77b326615475647cd369a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9651f213ef9fbdc69e65ea69ff2a3ecce935d5dce8fd4f3d686b650633c1fc1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdeca02ceccf49e104c97dbf97368fcb5bf7c3b9bdbe2658f3fe03d7beaf4990(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hvn_link: builtins.str,
    peering_id: builtins.str,
    peer_resource_group_name: builtins.str,
    peer_subscription_id: builtins.str,
    peer_tenant_id: builtins.str,
    peer_vnet_name: builtins.str,
    peer_vnet_region: builtins.str,
    allow_forwarded_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AzurePeeringConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_remote_gateways: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127f56bb37ab835fef1b18188f7621a124d0fb401d1e629d1300d24f99ad3d39(
    *,
    create: typing.Optional[builtins.str] = None,
    default: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de06caedb075d8d19ea645ec3e13b04d529215405a243af116f0428e862fc366(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a8e76e7a3512daf4b534950dbd9d275ae378c6f2cdb318088ec4f426639ca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd499f2873dbbe4ac74344bbe2ed4a398b3767a85093ce69f05a0afd28c12b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652fbf5b94f495557f8dd8cbaef3f753db0ad058b606704ce75e4f8c339f3300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d75cb149349ab690e23812d26049a41a9bcffec61cf834c97bbdc509fcc3de9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AzurePeeringConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
