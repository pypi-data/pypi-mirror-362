r'''
# `hcp_boundary_cluster`

Refer to the Terraform Registry for docs: [`hcp_boundary_cluster`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster).
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


class BoundaryCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.boundaryCluster.BoundaryCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster hcp_boundary_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        password: builtins.str,
        tier: builtins.str,
        username: builtins.str,
        auth_token_time_to_live: typing.Optional[builtins.str] = None,
        auth_token_time_to_stale: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window_config: typing.Optional[typing.Union["BoundaryClusterMaintenanceWindowConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BoundaryClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster hcp_boundary_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: The ID of the Boundary cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#cluster_id BoundaryCluster#cluster_id}
        :param password: The password of the initial admin user. This must be at least 8 characters in length. Note that this may show up in logs, and it will be stored in the state file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#password BoundaryCluster#password}
        :param tier: The tier that the HCP Boundary cluster will be provisioned as, 'Standard' or 'Plus'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#tier BoundaryCluster#tier}
        :param username: The username of the initial admin user. This must be at least 3 characters in length, alphanumeric, hyphen, or period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#username BoundaryCluster#username}
        :param auth_token_time_to_live: The time to live for the auth token in golang's time.Duration string format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#auth_token_time_to_live BoundaryCluster#auth_token_time_to_live}
        :param auth_token_time_to_stale: The time to stale for the auth token in golang's time.Duration string format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#auth_token_time_to_stale BoundaryCluster#auth_token_time_to_stale}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#id BoundaryCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window_config: maintenance_window_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#maintenance_window_config BoundaryCluster#maintenance_window_config}
        :param project_id: The ID of the HCP project where the Boundary cluster is located. If not specified, the project specified in the HCP Provider config block will be used, if configured. If a project is not configured in the HCP Provider config block, the oldest project in the organization will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#project_id BoundaryCluster#project_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#timeouts BoundaryCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2149f6f97208781b0ed0d20d3a33cf69f49b4c88d0ef68630f02618f6ae9b3ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BoundaryClusterConfig(
            cluster_id=cluster_id,
            password=password,
            tier=tier,
            username=username,
            auth_token_time_to_live=auth_token_time_to_live,
            auth_token_time_to_stale=auth_token_time_to_stale,
            id=id,
            maintenance_window_config=maintenance_window_config,
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
        '''Generates CDKTF code for importing a BoundaryCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BoundaryCluster to import.
        :param import_from_id: The id of the existing BoundaryCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BoundaryCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67da469fcdd669646f55f79b7cafb23f36feafb06f7bb720dbab7b885b4dd530)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMaintenanceWindowConfig")
    def put_maintenance_window_config(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        end: typing.Optional[jsii.Number] = None,
        start: typing.Optional[jsii.Number] = None,
        upgrade_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param day: The maintenance day of the week for scheduled upgrades. Valid options for maintenance window day - ``MONDAY``, ``TUESDAY``, ``WEDNESDAY``, ``THURSDAY``, ``FRIDAY``, ``SATURDAY``, ``SUNDAY`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#day BoundaryCluster#day}
        :param end: The end time which upgrades can be performed. Uses 24H clock and must be in UTC time zone. Valid options include - 1 to 24 (inclusive) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#end BoundaryCluster#end}
        :param start: The start time which upgrades can be performed. Uses 24H clock and must be in UTC time zone. Valid options include - 0 to 23 (inclusive) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#start BoundaryCluster#start}
        :param upgrade_type: The upgrade type for the cluster. Valid options for upgrade type - ``AUTOMATIC``, ``SCHEDULED``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#upgrade_type BoundaryCluster#upgrade_type}
        '''
        value = BoundaryClusterMaintenanceWindowConfig(
            day=day, end=end, start=start, upgrade_type=upgrade_type
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindowConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#create BoundaryCluster#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#default BoundaryCluster#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#delete BoundaryCluster#delete}.
        '''
        value = BoundaryClusterTimeouts(create=create, default=default, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthTokenTimeToLive")
    def reset_auth_token_time_to_live(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthTokenTimeToLive", []))

    @jsii.member(jsii_name="resetAuthTokenTimeToStale")
    def reset_auth_token_time_to_stale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthTokenTimeToStale", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintenanceWindowConfig")
    def reset_maintenance_window_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindowConfig", []))

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
    @jsii.member(jsii_name="clusterUrl")
    def cluster_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterUrl"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowConfig")
    def maintenance_window_config(
        self,
    ) -> "BoundaryClusterMaintenanceWindowConfigOutputReference":
        return typing.cast("BoundaryClusterMaintenanceWindowConfigOutputReference", jsii.get(self, "maintenanceWindowConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BoundaryClusterTimeoutsOutputReference":
        return typing.cast("BoundaryClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="authTokenTimeToLiveInput")
    def auth_token_time_to_live_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTokenTimeToLiveInput"))

    @builtins.property
    @jsii.member(jsii_name="authTokenTimeToStaleInput")
    def auth_token_time_to_stale_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTokenTimeToStaleInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowConfigInput")
    def maintenance_window_config_input(
        self,
    ) -> typing.Optional["BoundaryClusterMaintenanceWindowConfig"]:
        return typing.cast(typing.Optional["BoundaryClusterMaintenanceWindowConfig"], jsii.get(self, "maintenanceWindowConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BoundaryClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BoundaryClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="authTokenTimeToLive")
    def auth_token_time_to_live(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authTokenTimeToLive"))

    @auth_token_time_to_live.setter
    def auth_token_time_to_live(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b8cda09e709cb676211927190c35a9bffcbd70414702fcebdf38f895bde3c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authTokenTimeToLive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authTokenTimeToStale")
    def auth_token_time_to_stale(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authTokenTimeToStale"))

    @auth_token_time_to_stale.setter
    def auth_token_time_to_stale(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05246809e26a0a0d506c6c05e4e5a643bee9969de0c9f39730593ae309c70a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authTokenTimeToStale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa7d662878ed3841c944ecbf552ec57189b1695817348c75cd19477c8c10474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb672faf1078202156e1e54a61e419c37309872930fbef7bd585eb879921388a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc255f7edb509d131f10cb4ddaa62d947db3fb5bb0a288c57a593b1fb445ac7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b43cdd11763015675b53618ea88d0f76e90bf620f71bb1336ace32476f14a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e409f01fd012bb249e5d82ed6d99110267f8a2d0da3bb806723c933bee99f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f4fda9f14965d1aece6ee8d4f4866bcf86cdd4f6d839739eb9c20409f101e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.boundaryCluster.BoundaryClusterConfig",
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
        "password": "password",
        "tier": "tier",
        "username": "username",
        "auth_token_time_to_live": "authTokenTimeToLive",
        "auth_token_time_to_stale": "authTokenTimeToStale",
        "id": "id",
        "maintenance_window_config": "maintenanceWindowConfig",
        "project_id": "projectId",
        "timeouts": "timeouts",
    },
)
class BoundaryClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        password: builtins.str,
        tier: builtins.str,
        username: builtins.str,
        auth_token_time_to_live: typing.Optional[builtins.str] = None,
        auth_token_time_to_stale: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window_config: typing.Optional[typing.Union["BoundaryClusterMaintenanceWindowConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BoundaryClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: The ID of the Boundary cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#cluster_id BoundaryCluster#cluster_id}
        :param password: The password of the initial admin user. This must be at least 8 characters in length. Note that this may show up in logs, and it will be stored in the state file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#password BoundaryCluster#password}
        :param tier: The tier that the HCP Boundary cluster will be provisioned as, 'Standard' or 'Plus'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#tier BoundaryCluster#tier}
        :param username: The username of the initial admin user. This must be at least 3 characters in length, alphanumeric, hyphen, or period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#username BoundaryCluster#username}
        :param auth_token_time_to_live: The time to live for the auth token in golang's time.Duration string format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#auth_token_time_to_live BoundaryCluster#auth_token_time_to_live}
        :param auth_token_time_to_stale: The time to stale for the auth token in golang's time.Duration string format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#auth_token_time_to_stale BoundaryCluster#auth_token_time_to_stale}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#id BoundaryCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window_config: maintenance_window_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#maintenance_window_config BoundaryCluster#maintenance_window_config}
        :param project_id: The ID of the HCP project where the Boundary cluster is located. If not specified, the project specified in the HCP Provider config block will be used, if configured. If a project is not configured in the HCP Provider config block, the oldest project in the organization will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#project_id BoundaryCluster#project_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#timeouts BoundaryCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(maintenance_window_config, dict):
            maintenance_window_config = BoundaryClusterMaintenanceWindowConfig(**maintenance_window_config)
        if isinstance(timeouts, dict):
            timeouts = BoundaryClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a42c8435422f6174ef4b14850c898cf15aef2c0f59ff51f8537eff8217911b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument auth_token_time_to_live", value=auth_token_time_to_live, expected_type=type_hints["auth_token_time_to_live"])
            check_type(argname="argument auth_token_time_to_stale", value=auth_token_time_to_stale, expected_type=type_hints["auth_token_time_to_stale"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintenance_window_config", value=maintenance_window_config, expected_type=type_hints["maintenance_window_config"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
            "password": password,
            "tier": tier,
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
        if auth_token_time_to_live is not None:
            self._values["auth_token_time_to_live"] = auth_token_time_to_live
        if auth_token_time_to_stale is not None:
            self._values["auth_token_time_to_stale"] = auth_token_time_to_stale
        if id is not None:
            self._values["id"] = id
        if maintenance_window_config is not None:
            self._values["maintenance_window_config"] = maintenance_window_config
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
    def cluster_id(self) -> builtins.str:
        '''The ID of the Boundary cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#cluster_id BoundaryCluster#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''The password of the initial admin user.

        This must be at least 8 characters in length. Note that this may show up in logs, and it will be stored in the state file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#password BoundaryCluster#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''The tier that the HCP Boundary cluster will be provisioned as, 'Standard' or 'Plus'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#tier BoundaryCluster#tier}
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username of the initial admin user.

        This must be at least 3 characters in length, alphanumeric, hyphen, or period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#username BoundaryCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_token_time_to_live(self) -> typing.Optional[builtins.str]:
        '''The time to live for the auth token in golang's time.Duration string format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#auth_token_time_to_live BoundaryCluster#auth_token_time_to_live}
        '''
        result = self._values.get("auth_token_time_to_live")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_token_time_to_stale(self) -> typing.Optional[builtins.str]:
        '''The time to stale for the auth token in golang's time.Duration string format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#auth_token_time_to_stale BoundaryCluster#auth_token_time_to_stale}
        '''
        result = self._values.get("auth_token_time_to_stale")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#id BoundaryCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window_config(
        self,
    ) -> typing.Optional["BoundaryClusterMaintenanceWindowConfig"]:
        '''maintenance_window_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#maintenance_window_config BoundaryCluster#maintenance_window_config}
        '''
        result = self._values.get("maintenance_window_config")
        return typing.cast(typing.Optional["BoundaryClusterMaintenanceWindowConfig"], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the HCP project where the Boundary cluster is located.

        If not specified, the project specified in the HCP Provider config block will be used, if configured.
        If a project is not configured in the HCP Provider config block, the oldest project in the organization will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#project_id BoundaryCluster#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BoundaryClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#timeouts BoundaryCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BoundaryClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BoundaryClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.boundaryCluster.BoundaryClusterMaintenanceWindowConfig",
    jsii_struct_bases=[],
    name_mapping={
        "day": "day",
        "end": "end",
        "start": "start",
        "upgrade_type": "upgradeType",
    },
)
class BoundaryClusterMaintenanceWindowConfig:
    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        end: typing.Optional[jsii.Number] = None,
        start: typing.Optional[jsii.Number] = None,
        upgrade_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param day: The maintenance day of the week for scheduled upgrades. Valid options for maintenance window day - ``MONDAY``, ``TUESDAY``, ``WEDNESDAY``, ``THURSDAY``, ``FRIDAY``, ``SATURDAY``, ``SUNDAY`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#day BoundaryCluster#day}
        :param end: The end time which upgrades can be performed. Uses 24H clock and must be in UTC time zone. Valid options include - 1 to 24 (inclusive) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#end BoundaryCluster#end}
        :param start: The start time which upgrades can be performed. Uses 24H clock and must be in UTC time zone. Valid options include - 0 to 23 (inclusive) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#start BoundaryCluster#start}
        :param upgrade_type: The upgrade type for the cluster. Valid options for upgrade type - ``AUTOMATIC``, ``SCHEDULED``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#upgrade_type BoundaryCluster#upgrade_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c425230c6c9dad28011618e997da80031379d340f0aa60178db1ed0b4af0b989)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument upgrade_type", value=upgrade_type, expected_type=type_hints["upgrade_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if end is not None:
            self._values["end"] = end
        if start is not None:
            self._values["start"] = start
        if upgrade_type is not None:
            self._values["upgrade_type"] = upgrade_type

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''The maintenance day of the week for scheduled upgrades.

        Valid options for maintenance window day - ``MONDAY``, ``TUESDAY``, ``WEDNESDAY``, ``THURSDAY``, ``FRIDAY``, ``SATURDAY``, ``SUNDAY``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#day BoundaryCluster#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end(self) -> typing.Optional[jsii.Number]:
        '''The end time which upgrades can be performed.

        Uses 24H clock and must be in UTC time zone. Valid options include - 1 to 24 (inclusive)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#end BoundaryCluster#end}
        '''
        result = self._values.get("end")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start(self) -> typing.Optional[jsii.Number]:
        '''The start time which upgrades can be performed.

        Uses 24H clock and must be in UTC time zone. Valid options include - 0 to 23 (inclusive)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#start BoundaryCluster#start}
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def upgrade_type(self) -> typing.Optional[builtins.str]:
        '''The upgrade type for the cluster. Valid options for upgrade type - ``AUTOMATIC``, ``SCHEDULED``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#upgrade_type BoundaryCluster#upgrade_type}
        '''
        result = self._values.get("upgrade_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BoundaryClusterMaintenanceWindowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BoundaryClusterMaintenanceWindowConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.boundaryCluster.BoundaryClusterMaintenanceWindowConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a524aaffe7484b83587870e381bbc085c07bab5d09ffac269ad7df036190abb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @jsii.member(jsii_name="resetUpgradeType")
    def reset_upgrade_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradeType", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeTypeInput")
    def upgrade_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "upgradeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab4f2f14f79828a1c007287a78e647fed149c40905ced276e7210fe5a2f3a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "end"))

    @end.setter
    def end(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15cfa558819e5ce898f69da3c07430f544b4812b287529ac7c849b284165ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8dd0a068d738e4d6fcc63d2ce00afea94f90abe3915552501dc74b0834ed87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upgradeType")
    def upgrade_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upgradeType"))

    @upgrade_type.setter
    def upgrade_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa78cef4bf65531863d2b5e2dca68a2a2ca4dc45cf1a18080e1bd52622fd5cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upgradeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BoundaryClusterMaintenanceWindowConfig]:
        return typing.cast(typing.Optional[BoundaryClusterMaintenanceWindowConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BoundaryClusterMaintenanceWindowConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacbe9efd9bfae7b5c4bb85ceecf8f501d77e62f65166c848d97bd8335d3be80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.boundaryCluster.BoundaryClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "default": "default", "delete": "delete"},
)
class BoundaryClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#create BoundaryCluster#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#default BoundaryCluster#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#delete BoundaryCluster#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1df35e6c2ce2e7de0ee92af3344b57d6ac6a21e84b62284e97df14a42ec523f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#create BoundaryCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#default BoundaryCluster#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/boundary_cluster#delete BoundaryCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BoundaryClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BoundaryClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.boundaryCluster.BoundaryClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1a84d0d879ad4081c4994340c0b643df3f62c6d9e2dca8862e07ee96b0014f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__812c7385c981f3ddef71061ff10514c92017f93cf56d9505b4f80c27279c9dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @default.setter
    def default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cfb3e33fefb6555f7d73f4ed61b0287677bde5ff0cfc27515dd09f6b000151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aca605c519f9636c809615141505ebc781d4c8cbfdbf4e34e7b56ebfd09a696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BoundaryClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BoundaryClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BoundaryClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3cbd4af49d45de4053a87b8e8b5e0cfe9d7f8992c3ddffab300262865c3d7f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BoundaryCluster",
    "BoundaryClusterConfig",
    "BoundaryClusterMaintenanceWindowConfig",
    "BoundaryClusterMaintenanceWindowConfigOutputReference",
    "BoundaryClusterTimeouts",
    "BoundaryClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2149f6f97208781b0ed0d20d3a33cf69f49b4c88d0ef68630f02618f6ae9b3ef(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    password: builtins.str,
    tier: builtins.str,
    username: builtins.str,
    auth_token_time_to_live: typing.Optional[builtins.str] = None,
    auth_token_time_to_stale: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window_config: typing.Optional[typing.Union[BoundaryClusterMaintenanceWindowConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BoundaryClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__67da469fcdd669646f55f79b7cafb23f36feafb06f7bb720dbab7b885b4dd530(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b8cda09e709cb676211927190c35a9bffcbd70414702fcebdf38f895bde3c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05246809e26a0a0d506c6c05e4e5a643bee9969de0c9f39730593ae309c70a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa7d662878ed3841c944ecbf552ec57189b1695817348c75cd19477c8c10474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb672faf1078202156e1e54a61e419c37309872930fbef7bd585eb879921388a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc255f7edb509d131f10cb4ddaa62d947db3fb5bb0a288c57a593b1fb445ac7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b43cdd11763015675b53618ea88d0f76e90bf620f71bb1336ace32476f14a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e409f01fd012bb249e5d82ed6d99110267f8a2d0da3bb806723c933bee99f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f4fda9f14965d1aece6ee8d4f4866bcf86cdd4f6d839739eb9c20409f101e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a42c8435422f6174ef4b14850c898cf15aef2c0f59ff51f8537eff8217911b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_id: builtins.str,
    password: builtins.str,
    tier: builtins.str,
    username: builtins.str,
    auth_token_time_to_live: typing.Optional[builtins.str] = None,
    auth_token_time_to_stale: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window_config: typing.Optional[typing.Union[BoundaryClusterMaintenanceWindowConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BoundaryClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c425230c6c9dad28011618e997da80031379d340f0aa60178db1ed0b4af0b989(
    *,
    day: typing.Optional[builtins.str] = None,
    end: typing.Optional[jsii.Number] = None,
    start: typing.Optional[jsii.Number] = None,
    upgrade_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a524aaffe7484b83587870e381bbc085c07bab5d09ffac269ad7df036190abb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab4f2f14f79828a1c007287a78e647fed149c40905ced276e7210fe5a2f3a6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15cfa558819e5ce898f69da3c07430f544b4812b287529ac7c849b284165ddf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8dd0a068d738e4d6fcc63d2ce00afea94f90abe3915552501dc74b0834ed87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa78cef4bf65531863d2b5e2dca68a2a2ca4dc45cf1a18080e1bd52622fd5cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacbe9efd9bfae7b5c4bb85ceecf8f501d77e62f65166c848d97bd8335d3be80(
    value: typing.Optional[BoundaryClusterMaintenanceWindowConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1df35e6c2ce2e7de0ee92af3344b57d6ac6a21e84b62284e97df14a42ec523f(
    *,
    create: typing.Optional[builtins.str] = None,
    default: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a84d0d879ad4081c4994340c0b643df3f62c6d9e2dca8862e07ee96b0014f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812c7385c981f3ddef71061ff10514c92017f93cf56d9505b4f80c27279c9dbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cfb3e33fefb6555f7d73f4ed61b0287677bde5ff0cfc27515dd09f6b000151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aca605c519f9636c809615141505ebc781d4c8cbfdbf4e34e7b56ebfd09a696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3cbd4af49d45de4053a87b8e8b5e0cfe9d7f8992c3ddffab300262865c3d7f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BoundaryClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
