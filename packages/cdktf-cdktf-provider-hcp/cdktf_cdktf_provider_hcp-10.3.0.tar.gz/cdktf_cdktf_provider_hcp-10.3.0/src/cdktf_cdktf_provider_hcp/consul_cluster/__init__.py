r'''
# `hcp_consul_cluster`

Refer to the Terraform Registry for docs: [`hcp_consul_cluster`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster).
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


class ConsulCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.consulCluster.ConsulCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster hcp_consul_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        hvn_id: builtins.str,
        tier: builtins.str,
        auto_hvn_to_hvn_peering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connect_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        datacenter: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ConsulClusterIpAllowlistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_consul_version: typing.Optional[builtins.str] = None,
        primary_link: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        public_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        size: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ConsulClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster hcp_consul_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: The ID of the HCP Consul cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#cluster_id ConsulCluster#cluster_id}
        :param hvn_id: The ID of the HVN this HCP Consul cluster is associated to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#hvn_id ConsulCluster#hvn_id}
        :param tier: The tier that the HCP Consul cluster will be provisioned as. Only ``development``, ``standard``, ``plus``, and ``premium`` are available at this time. See `pricing information <https://www.hashicorp.com/products/consul/pricing>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#tier ConsulCluster#tier}
        :param auto_hvn_to_hvn_peering: Enables automatic HVN to HVN peering when creating a secondary cluster in a federation. The alternative to using the auto-accept feature is to create an ```hcp_hvn_peering_connection`` <hvn_peering_connection.md>`_ resource that explicitly defines the HVN resources that are allowed to communicate with each other. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#auto_hvn_to_hvn_peering ConsulCluster#auto_hvn_to_hvn_peering}
        :param connect_enabled: Denotes the Consul connect feature should be enabled for this cluster. Default to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#connect_enabled ConsulCluster#connect_enabled}
        :param datacenter: The Consul data center name of the cluster. If not specified, it is defaulted to the value of ``cluster_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#datacenter ConsulCluster#datacenter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#id ConsulCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_allowlist: ip_allowlist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#ip_allowlist ConsulCluster#ip_allowlist}
        :param min_consul_version: The minimum Consul patch version of the cluster. Allows only the rightmost version component to increment (E.g: ``1.13.0`` will allow installation of ``1.13.2`` and ``1.13.3`` etc., but not ``1.14.0``). If not specified, it is defaulted to the version that is currently recommended by HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#min_consul_version ConsulCluster#min_consul_version}
        :param primary_link: The ``self_link`` of the HCP Consul cluster which is the primary in the federation setup with this HCP Consul cluster. If not specified, it is a standalone cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#primary_link ConsulCluster#primary_link}
        :param project_id: The ID of the HCP project where the HCP Consul cluster is located. If not specified, the project specified in the HCP Provider config block will be used, if configured. If a project is not configured in the HCP Provider config block, the oldest project in the organization will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#project_id ConsulCluster#project_id}
        :param public_endpoint: Denotes that the cluster has a public endpoint for the Consul UI. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#public_endpoint ConsulCluster#public_endpoint}
        :param size: The t-shirt size representation of each server VM that this Consul cluster is provisioned with. Valid option for development tier - ``x_small``. Valid options for other tiers - ``small``, ``medium``, ``large``. For more details - https://cloud.hashicorp.com/pricing/consul. Upgrading the size of a cluster after creation is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#size ConsulCluster#size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#timeouts ConsulCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7c20b7ddf41d17c61fe074b752741828b3a4eb16bf152212fad486670fea93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ConsulClusterConfig(
            cluster_id=cluster_id,
            hvn_id=hvn_id,
            tier=tier,
            auto_hvn_to_hvn_peering=auto_hvn_to_hvn_peering,
            connect_enabled=connect_enabled,
            datacenter=datacenter,
            id=id,
            ip_allowlist=ip_allowlist,
            min_consul_version=min_consul_version,
            primary_link=primary_link,
            project_id=project_id,
            public_endpoint=public_endpoint,
            size=size,
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
        '''Generates CDKTF code for importing a ConsulCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ConsulCluster to import.
        :param import_from_id: The id of the existing ConsulCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ConsulCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf3cf719cbdd1a39f93411698768d7c6a63dfd8a1ee01c964211ba9100c5682)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIpAllowlist")
    def put_ip_allowlist(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ConsulClusterIpAllowlistStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755884b6b52cb4ceb3d316fc3c2b2052c5a874d7588a584a685b12e0ef9ae248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpAllowlist", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#create ConsulCluster#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#default ConsulCluster#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#delete ConsulCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#update ConsulCluster#update}.
        '''
        value = ConsulClusterTimeouts(
            create=create, default=default, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoHvnToHvnPeering")
    def reset_auto_hvn_to_hvn_peering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoHvnToHvnPeering", []))

    @jsii.member(jsii_name="resetConnectEnabled")
    def reset_connect_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectEnabled", []))

    @jsii.member(jsii_name="resetDatacenter")
    def reset_datacenter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatacenter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAllowlist")
    def reset_ip_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAllowlist", []))

    @jsii.member(jsii_name="resetMinConsulVersion")
    def reset_min_consul_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinConsulVersion", []))

    @jsii.member(jsii_name="resetPrimaryLink")
    def reset_primary_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryLink", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetPublicEndpoint")
    def reset_public_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicEndpoint", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

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
    @jsii.member(jsii_name="cloudProvider")
    def cloud_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudProvider"))

    @builtins.property
    @jsii.member(jsii_name="consulAutomaticUpgrades")
    def consul_automatic_upgrades(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "consulAutomaticUpgrades"))

    @builtins.property
    @jsii.member(jsii_name="consulCaFile")
    def consul_ca_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consulCaFile"))

    @builtins.property
    @jsii.member(jsii_name="consulConfigFile")
    def consul_config_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consulConfigFile"))

    @builtins.property
    @jsii.member(jsii_name="consulPrivateEndpointUrl")
    def consul_private_endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consulPrivateEndpointUrl"))

    @builtins.property
    @jsii.member(jsii_name="consulPublicEndpointUrl")
    def consul_public_endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consulPublicEndpointUrl"))

    @builtins.property
    @jsii.member(jsii_name="consulRootTokenAccessorId")
    def consul_root_token_accessor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consulRootTokenAccessorId"))

    @builtins.property
    @jsii.member(jsii_name="consulRootTokenSecretId")
    def consul_root_token_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consulRootTokenSecretId"))

    @builtins.property
    @jsii.member(jsii_name="consulSnapshotInterval")
    def consul_snapshot_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consulSnapshotInterval"))

    @builtins.property
    @jsii.member(jsii_name="consulSnapshotRetention")
    def consul_snapshot_retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consulSnapshotRetention"))

    @builtins.property
    @jsii.member(jsii_name="consulVersion")
    def consul_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consulVersion"))

    @builtins.property
    @jsii.member(jsii_name="ipAllowlist")
    def ip_allowlist(self) -> "ConsulClusterIpAllowlistStructList":
        return typing.cast("ConsulClusterIpAllowlistStructList", jsii.get(self, "ipAllowlist"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scale"))

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
    def timeouts(self) -> "ConsulClusterTimeoutsOutputReference":
        return typing.cast("ConsulClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoHvnToHvnPeeringInput")
    def auto_hvn_to_hvn_peering_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoHvnToHvnPeeringInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="connectEnabledInput")
    def connect_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "connectEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="datacenterInput")
    def datacenter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datacenterInput"))

    @builtins.property
    @jsii.member(jsii_name="hvnIdInput")
    def hvn_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hvnIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAllowlistInput")
    def ip_allowlist_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConsulClusterIpAllowlistStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConsulClusterIpAllowlistStruct"]]], jsii.get(self, "ipAllowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="minConsulVersionInput")
    def min_consul_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minConsulVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryLinkInput")
    def primary_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicEndpointInput")
    def public_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ConsulClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ConsulClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoHvnToHvnPeering")
    def auto_hvn_to_hvn_peering(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoHvnToHvnPeering"))

    @auto_hvn_to_hvn_peering.setter
    def auto_hvn_to_hvn_peering(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7747ae866839e23f038061aaab38dc05ef11533d9002e932b6be784b255a7358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoHvnToHvnPeering", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d5779aa0756377d1f8ad36a81925b16d2b12a7e7458a2c0bb1830affdf4c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectEnabled")
    def connect_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "connectEnabled"))

    @connect_enabled.setter
    def connect_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf5822ac9c1ddfa4d7d58f3b139669326e3baa379f450b3412dccccbeb099c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datacenter")
    def datacenter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datacenter"))

    @datacenter.setter
    def datacenter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e618abefd1c144a8796b2f5f9d18bb9b09e608d289348ba2cfaace5ea0adedc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datacenter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hvnId")
    def hvn_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hvnId"))

    @hvn_id.setter
    def hvn_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c49e63d9c3759b8ffccc3116d120c162c3a7e1b42dede85aa34595767bfa87a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hvnId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66c49eb73fc16fbfd57ff197d0da80c444a30f06bb6b43fc7ce6c7d45172a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minConsulVersion")
    def min_consul_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minConsulVersion"))

    @min_consul_version.setter
    def min_consul_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bba4e53c0cc775fa86a4ac6310dbae013a17c79e26f003792ee4297a0d1570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minConsulVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryLink")
    def primary_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryLink"))

    @primary_link.setter
    def primary_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf0a6825bb773010015eff5f8aadc9a75a069c3681422e9f7d5b55cbb84a36f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e2f44aa2af69bd3be566d174766c27fd030806628f0ee8624239eb6ebcd38d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicEndpoint")
    def public_endpoint(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicEndpoint"))

    @public_endpoint.setter
    def public_endpoint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81827a748f42f6f6180a762db990988705288acbc1daea0a7901a0f287b91d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "size"))

    @size.setter
    def size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce6238faf34e924fb7c172fd378160f245b6b5035cdf41cd749e1a04df3d8e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2d89c9bb70f0ba2091025931be50cd10248e4bc51aa6202682f398607bc0fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.consulCluster.ConsulClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_id": "clusterId",
        "hvn_id": "hvnId",
        "tier": "tier",
        "auto_hvn_to_hvn_peering": "autoHvnToHvnPeering",
        "connect_enabled": "connectEnabled",
        "datacenter": "datacenter",
        "id": "id",
        "ip_allowlist": "ipAllowlist",
        "min_consul_version": "minConsulVersion",
        "primary_link": "primaryLink",
        "project_id": "projectId",
        "public_endpoint": "publicEndpoint",
        "size": "size",
        "timeouts": "timeouts",
    },
)
class ConsulClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_id: builtins.str,
        hvn_id: builtins.str,
        tier: builtins.str,
        auto_hvn_to_hvn_peering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connect_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        datacenter: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ConsulClusterIpAllowlistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_consul_version: typing.Optional[builtins.str] = None,
        primary_link: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        public_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        size: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ConsulClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: The ID of the HCP Consul cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#cluster_id ConsulCluster#cluster_id}
        :param hvn_id: The ID of the HVN this HCP Consul cluster is associated to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#hvn_id ConsulCluster#hvn_id}
        :param tier: The tier that the HCP Consul cluster will be provisioned as. Only ``development``, ``standard``, ``plus``, and ``premium`` are available at this time. See `pricing information <https://www.hashicorp.com/products/consul/pricing>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#tier ConsulCluster#tier}
        :param auto_hvn_to_hvn_peering: Enables automatic HVN to HVN peering when creating a secondary cluster in a federation. The alternative to using the auto-accept feature is to create an ```hcp_hvn_peering_connection`` <hvn_peering_connection.md>`_ resource that explicitly defines the HVN resources that are allowed to communicate with each other. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#auto_hvn_to_hvn_peering ConsulCluster#auto_hvn_to_hvn_peering}
        :param connect_enabled: Denotes the Consul connect feature should be enabled for this cluster. Default to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#connect_enabled ConsulCluster#connect_enabled}
        :param datacenter: The Consul data center name of the cluster. If not specified, it is defaulted to the value of ``cluster_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#datacenter ConsulCluster#datacenter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#id ConsulCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_allowlist: ip_allowlist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#ip_allowlist ConsulCluster#ip_allowlist}
        :param min_consul_version: The minimum Consul patch version of the cluster. Allows only the rightmost version component to increment (E.g: ``1.13.0`` will allow installation of ``1.13.2`` and ``1.13.3`` etc., but not ``1.14.0``). If not specified, it is defaulted to the version that is currently recommended by HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#min_consul_version ConsulCluster#min_consul_version}
        :param primary_link: The ``self_link`` of the HCP Consul cluster which is the primary in the federation setup with this HCP Consul cluster. If not specified, it is a standalone cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#primary_link ConsulCluster#primary_link}
        :param project_id: The ID of the HCP project where the HCP Consul cluster is located. If not specified, the project specified in the HCP Provider config block will be used, if configured. If a project is not configured in the HCP Provider config block, the oldest project in the organization will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#project_id ConsulCluster#project_id}
        :param public_endpoint: Denotes that the cluster has a public endpoint for the Consul UI. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#public_endpoint ConsulCluster#public_endpoint}
        :param size: The t-shirt size representation of each server VM that this Consul cluster is provisioned with. Valid option for development tier - ``x_small``. Valid options for other tiers - ``small``, ``medium``, ``large``. For more details - https://cloud.hashicorp.com/pricing/consul. Upgrading the size of a cluster after creation is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#size ConsulCluster#size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#timeouts ConsulCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ConsulClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15a4aa3c9e2c590b1a7243a86035a6b7c3197aaded71d8b2ef48bed209d4f0a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument hvn_id", value=hvn_id, expected_type=type_hints["hvn_id"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument auto_hvn_to_hvn_peering", value=auto_hvn_to_hvn_peering, expected_type=type_hints["auto_hvn_to_hvn_peering"])
            check_type(argname="argument connect_enabled", value=connect_enabled, expected_type=type_hints["connect_enabled"])
            check_type(argname="argument datacenter", value=datacenter, expected_type=type_hints["datacenter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_allowlist", value=ip_allowlist, expected_type=type_hints["ip_allowlist"])
            check_type(argname="argument min_consul_version", value=min_consul_version, expected_type=type_hints["min_consul_version"])
            check_type(argname="argument primary_link", value=primary_link, expected_type=type_hints["primary_link"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument public_endpoint", value=public_endpoint, expected_type=type_hints["public_endpoint"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
            "hvn_id": hvn_id,
            "tier": tier,
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
        if auto_hvn_to_hvn_peering is not None:
            self._values["auto_hvn_to_hvn_peering"] = auto_hvn_to_hvn_peering
        if connect_enabled is not None:
            self._values["connect_enabled"] = connect_enabled
        if datacenter is not None:
            self._values["datacenter"] = datacenter
        if id is not None:
            self._values["id"] = id
        if ip_allowlist is not None:
            self._values["ip_allowlist"] = ip_allowlist
        if min_consul_version is not None:
            self._values["min_consul_version"] = min_consul_version
        if primary_link is not None:
            self._values["primary_link"] = primary_link
        if project_id is not None:
            self._values["project_id"] = project_id
        if public_endpoint is not None:
            self._values["public_endpoint"] = public_endpoint
        if size is not None:
            self._values["size"] = size
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
    def cluster_id(self) -> builtins.str:
        '''The ID of the HCP Consul cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#cluster_id ConsulCluster#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hvn_id(self) -> builtins.str:
        '''The ID of the HVN this HCP Consul cluster is associated to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#hvn_id ConsulCluster#hvn_id}
        '''
        result = self._values.get("hvn_id")
        assert result is not None, "Required property 'hvn_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''The tier that the HCP Consul cluster will be provisioned as.

        Only ``development``, ``standard``, ``plus``, and ``premium`` are available at this time. See `pricing information <https://www.hashicorp.com/products/consul/pricing>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#tier ConsulCluster#tier}
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_hvn_to_hvn_peering(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables automatic HVN to HVN peering when creating a secondary cluster in a federation.

        The alternative to using the auto-accept feature is to create an ```hcp_hvn_peering_connection`` <hvn_peering_connection.md>`_ resource that explicitly defines the HVN resources that are allowed to communicate with each other.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#auto_hvn_to_hvn_peering ConsulCluster#auto_hvn_to_hvn_peering}
        '''
        result = self._values.get("auto_hvn_to_hvn_peering")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def connect_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes the Consul connect feature should be enabled for this cluster.  Default to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#connect_enabled ConsulCluster#connect_enabled}
        '''
        result = self._values.get("connect_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def datacenter(self) -> typing.Optional[builtins.str]:
        '''The Consul data center name of the cluster. If not specified, it is defaulted to the value of ``cluster_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#datacenter ConsulCluster#datacenter}
        '''
        result = self._values.get("datacenter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#id ConsulCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_allowlist(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConsulClusterIpAllowlistStruct"]]]:
        '''ip_allowlist block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#ip_allowlist ConsulCluster#ip_allowlist}
        '''
        result = self._values.get("ip_allowlist")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ConsulClusterIpAllowlistStruct"]]], result)

    @builtins.property
    def min_consul_version(self) -> typing.Optional[builtins.str]:
        '''The minimum Consul patch version of the cluster.

        Allows only the rightmost version component to increment (E.g: ``1.13.0`` will allow installation of ``1.13.2`` and ``1.13.3`` etc., but not ``1.14.0``). If not specified, it is defaulted to the version that is currently recommended by HCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#min_consul_version ConsulCluster#min_consul_version}
        '''
        result = self._values.get("min_consul_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_link(self) -> typing.Optional[builtins.str]:
        '''The ``self_link`` of the HCP Consul cluster which is the primary in the federation setup with this HCP Consul cluster.

        If not specified, it is a standalone cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#primary_link ConsulCluster#primary_link}
        '''
        result = self._values.get("primary_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the HCP project where the HCP Consul cluster is located.

        If not specified, the project specified in the HCP Provider config block will be used, if configured.
        If a project is not configured in the HCP Provider config block, the oldest project in the organization will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#project_id ConsulCluster#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes that the cluster has a public endpoint for the Consul UI. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#public_endpoint ConsulCluster#public_endpoint}
        '''
        result = self._values.get("public_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def size(self) -> typing.Optional[builtins.str]:
        '''The t-shirt size representation of each server VM that this Consul cluster is provisioned with.

        Valid option for development tier - ``x_small``. Valid options for other tiers - ``small``, ``medium``, ``large``. For more details - https://cloud.hashicorp.com/pricing/consul. Upgrading the size of a cluster after creation is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#size ConsulCluster#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ConsulClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#timeouts ConsulCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ConsulClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConsulClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.consulCluster.ConsulClusterIpAllowlistStruct",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "description": "description"},
)
class ConsulClusterIpAllowlistStruct:
    def __init__(
        self,
        *,
        address: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: IP address range in CIDR notation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#address ConsulCluster#address}
        :param description: Description to help identify source (maximum 255 chars). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#description ConsulCluster#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495bb421883917349d0c876a105aad0e63018a81a54757bca42ff15aaf04b408)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def address(self) -> builtins.str:
        '''IP address range in CIDR notation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#address ConsulCluster#address}
        '''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description to help identify source (maximum 255 chars).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#description ConsulCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConsulClusterIpAllowlistStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConsulClusterIpAllowlistStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.consulCluster.ConsulClusterIpAllowlistStructList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef2712e9abb4007415e17821ff130fb6fd48d65ee8af510323462e80ad7d2a3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ConsulClusterIpAllowlistStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4405900900a041b3994d04144e748db3c5336e5fba02058113bbb2d8962ea263)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ConsulClusterIpAllowlistStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0094d48a6503eac508bfa7f6bf01ab93adb051777dc0991fd8cd86e789beec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace5d4e52324b7a12bd9c10d1454e468de8d393cd0b1fc67d9962ea98696c406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824e61c22c5096752c28b33c325804ce1c836c0aeb9e3c27572b8fd3b07830ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConsulClusterIpAllowlistStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConsulClusterIpAllowlistStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConsulClusterIpAllowlistStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1c7d49c82de7949e660dd0d03d7edbbc5faf46339581b6c4bf46846197fd13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ConsulClusterIpAllowlistStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.consulCluster.ConsulClusterIpAllowlistStructOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30d85cc6021da0044b187926624eb015e5d2085f7fcb50040c74d3a2292d4b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b477e5be33f33b7dabc89a4dea378edc97599e1a998024b7111d6ba6a03521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6989d529c550b945e7d4b7cc3f52fe5634253fd4b2bf55e96098d3ccb8eb9eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConsulClusterIpAllowlistStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConsulClusterIpAllowlistStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConsulClusterIpAllowlistStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7c903fbbaf1f7ca9f3c1ea2d982b0509e631815dd7ad05f6d82f767a4dc7b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.consulCluster.ConsulClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "default": "default",
        "delete": "delete",
        "update": "update",
    },
)
class ConsulClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#create ConsulCluster#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#default ConsulCluster#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#delete ConsulCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#update ConsulCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f659835463a84e60ea15cd993c4c5de4055fb363e403183b9791dcfc6d21d85)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if default is not None:
            self._values["default"] = default
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#create ConsulCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#default ConsulCluster#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#delete ConsulCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/consul_cluster#update ConsulCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConsulClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConsulClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.consulCluster.ConsulClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94d5dbda44fa1c3822b839946dfffea16746f702f71b01b9b4aa3a4837cc60c8)
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

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

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
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0d965328870ac2d92b49b7a1d6a09c5e6dcf53f5dc685d77e322b4297a2ca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @default.setter
    def default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ce23c5b93062d89c97a51e3cb504200bc09e362e3216325b0b12eb309c3fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e858153a37edf1a4cb823ba6fbdd2505a683aee5d0c9b256afbf2e64475fc1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfb0efcf89cc12a39e94753cf38eb78c5b6959cc9c388c40a1026174af131f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConsulClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConsulClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConsulClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad66e8c77c2f12142263c98e8941b79dd72a5d3eec38a2d0768109e832203bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ConsulCluster",
    "ConsulClusterConfig",
    "ConsulClusterIpAllowlistStruct",
    "ConsulClusterIpAllowlistStructList",
    "ConsulClusterIpAllowlistStructOutputReference",
    "ConsulClusterTimeouts",
    "ConsulClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dd7c20b7ddf41d17c61fe074b752741828b3a4eb16bf152212fad486670fea93(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    hvn_id: builtins.str,
    tier: builtins.str,
    auto_hvn_to_hvn_peering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connect_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    datacenter: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ConsulClusterIpAllowlistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    min_consul_version: typing.Optional[builtins.str] = None,
    primary_link: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    public_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    size: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ConsulClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ebf3cf719cbdd1a39f93411698768d7c6a63dfd8a1ee01c964211ba9100c5682(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755884b6b52cb4ceb3d316fc3c2b2052c5a874d7588a584a685b12e0ef9ae248(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ConsulClusterIpAllowlistStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7747ae866839e23f038061aaab38dc05ef11533d9002e932b6be784b255a7358(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d5779aa0756377d1f8ad36a81925b16d2b12a7e7458a2c0bb1830affdf4c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf5822ac9c1ddfa4d7d58f3b139669326e3baa379f450b3412dccccbeb099c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e618abefd1c144a8796b2f5f9d18bb9b09e608d289348ba2cfaace5ea0adedc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49e63d9c3759b8ffccc3116d120c162c3a7e1b42dede85aa34595767bfa87a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66c49eb73fc16fbfd57ff197d0da80c444a30f06bb6b43fc7ce6c7d45172a92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bba4e53c0cc775fa86a4ac6310dbae013a17c79e26f003792ee4297a0d1570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf0a6825bb773010015eff5f8aadc9a75a069c3681422e9f7d5b55cbb84a36f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e2f44aa2af69bd3be566d174766c27fd030806628f0ee8624239eb6ebcd38d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81827a748f42f6f6180a762db990988705288acbc1daea0a7901a0f287b91d01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce6238faf34e924fb7c172fd378160f245b6b5035cdf41cd749e1a04df3d8e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2d89c9bb70f0ba2091025931be50cd10248e4bc51aa6202682f398607bc0fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15a4aa3c9e2c590b1a7243a86035a6b7c3197aaded71d8b2ef48bed209d4f0a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_id: builtins.str,
    hvn_id: builtins.str,
    tier: builtins.str,
    auto_hvn_to_hvn_peering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connect_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    datacenter: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ConsulClusterIpAllowlistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    min_consul_version: typing.Optional[builtins.str] = None,
    primary_link: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    public_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    size: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ConsulClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495bb421883917349d0c876a105aad0e63018a81a54757bca42ff15aaf04b408(
    *,
    address: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2712e9abb4007415e17821ff130fb6fd48d65ee8af510323462e80ad7d2a3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4405900900a041b3994d04144e748db3c5336e5fba02058113bbb2d8962ea263(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0094d48a6503eac508bfa7f6bf01ab93adb051777dc0991fd8cd86e789beec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace5d4e52324b7a12bd9c10d1454e468de8d393cd0b1fc67d9962ea98696c406(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824e61c22c5096752c28b33c325804ce1c836c0aeb9e3c27572b8fd3b07830ba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1c7d49c82de7949e660dd0d03d7edbbc5faf46339581b6c4bf46846197fd13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ConsulClusterIpAllowlistStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30d85cc6021da0044b187926624eb015e5d2085f7fcb50040c74d3a2292d4b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b477e5be33f33b7dabc89a4dea378edc97599e1a998024b7111d6ba6a03521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6989d529c550b945e7d4b7cc3f52fe5634253fd4b2bf55e96098d3ccb8eb9eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7c903fbbaf1f7ca9f3c1ea2d982b0509e631815dd7ad05f6d82f767a4dc7b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConsulClusterIpAllowlistStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f659835463a84e60ea15cd993c4c5de4055fb363e403183b9791dcfc6d21d85(
    *,
    create: typing.Optional[builtins.str] = None,
    default: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d5dbda44fa1c3822b839946dfffea16746f702f71b01b9b4aa3a4837cc60c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0d965328870ac2d92b49b7a1d6a09c5e6dcf53f5dc685d77e322b4297a2ca7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ce23c5b93062d89c97a51e3cb504200bc09e362e3216325b0b12eb309c3fdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e858153a37edf1a4cb823ba6fbdd2505a683aee5d0c9b256afbf2e64475fc1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfb0efcf89cc12a39e94753cf38eb78c5b6959cc9c388c40a1026174af131f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad66e8c77c2f12142263c98e8941b79dd72a5d3eec38a2d0768109e832203bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ConsulClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
