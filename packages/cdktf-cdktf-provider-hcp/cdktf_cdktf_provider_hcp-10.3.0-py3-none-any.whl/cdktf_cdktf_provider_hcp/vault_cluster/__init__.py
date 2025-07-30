r'''
# `hcp_vault_cluster`

Refer to the Terraform Registry for docs: [`hcp_vault_cluster`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster).
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


class VaultCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster hcp_vault_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        hvn_id: builtins.str,
        audit_log_config: typing.Optional[typing.Union["VaultClusterAuditLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VaultClusterIpAllowlistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        major_version_upgrade_config: typing.Optional[typing.Union["VaultClusterMajorVersionUpgradeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_config: typing.Optional[typing.Union["VaultClusterMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        min_vault_version: typing.Optional[builtins.str] = None,
        paths_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        primary_link: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        proxy_endpoint: typing.Optional[builtins.str] = None,
        public_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VaultClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster hcp_vault_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: The ID of the HCP Vault cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cluster_id VaultCluster#cluster_id}
        :param hvn_id: The ID of the HVN this HCP Vault cluster is associated to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#hvn_id VaultCluster#hvn_id}
        :param audit_log_config: audit_log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#audit_log_config VaultCluster#audit_log_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#id VaultCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_allowlist: ip_allowlist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#ip_allowlist VaultCluster#ip_allowlist}
        :param major_version_upgrade_config: major_version_upgrade_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#major_version_upgrade_config VaultCluster#major_version_upgrade_config}
        :param metrics_config: metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#metrics_config VaultCluster#metrics_config}
        :param min_vault_version: The minimum Vault version to use when creating the cluster. If not specified, it is defaulted to the version that is currently recommended by HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#min_vault_version VaultCluster#min_vault_version}
        :param paths_filter: The performance replication `paths filter <https://developer.hashicorp.com/vault/tutorials/cloud-ops/vault-replication-terraform>`_. Applies to performance replication secondaries only and operates in "deny" mode only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#paths_filter VaultCluster#paths_filter}
        :param primary_link: The ``self_link`` of the HCP Vault Plus tier cluster which is the primary in the performance replication setup with this HCP Vault Plus tier cluster. If not specified, it is a standalone Plus tier HCP Vault cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#primary_link VaultCluster#primary_link}
        :param project_id: The ID of the HCP project where the Vault cluster is located. If not specified, the project specified in the HCP Provider config block will be used, if configured. If a project is not configured in the HCP Provider config block, the oldest project in the organization will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#project_id VaultCluster#project_id}
        :param proxy_endpoint: Denotes that the cluster has a proxy endpoint. Valid options are ``ENABLED``, ``DISABLED``. Defaults to ``DISABLED``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#proxy_endpoint VaultCluster#proxy_endpoint}
        :param public_endpoint: Denotes that the cluster has a public endpoint. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#public_endpoint VaultCluster#public_endpoint}
        :param tier: Tier of the HCP Vault cluster. Valid options for tiers - ``dev``, ``standard_small``, ``standard_medium``, ``standard_large``, ``plus_small``, ``plus_medium``, ``plus_large``. See `pricing information <https://www.hashicorp.com/products/vault/pricing>`_. Changing a cluster's size or tier is only available to admins. See `Scale a cluster <https://registry.terraform.io/providers/hashicorp/hcp/latest/docs/guides/vault-scaling>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#tier VaultCluster#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#timeouts VaultCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a1b511b563b877d6fa1e39c5fcee395fa5006b8ec1cdc089eaff3f1e18e966)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VaultClusterConfig(
            cluster_id=cluster_id,
            hvn_id=hvn_id,
            audit_log_config=audit_log_config,
            id=id,
            ip_allowlist=ip_allowlist,
            major_version_upgrade_config=major_version_upgrade_config,
            metrics_config=metrics_config,
            min_vault_version=min_vault_version,
            paths_filter=paths_filter,
            primary_link=primary_link,
            project_id=project_id,
            proxy_endpoint=proxy_endpoint,
            public_endpoint=public_endpoint,
            tier=tier,
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
        '''Generates CDKTF code for importing a VaultCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VaultCluster to import.
        :param import_from_id: The id of the existing VaultCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VaultCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58842deedd49ef02ced6c37958c2839e494ba9286baf07c9f6f708cdb80270f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuditLogConfig")
    def put_audit_log_config(
        self,
        *,
        cloudwatch_access_key_id: typing.Optional[builtins.str] = None,
        cloudwatch_region: typing.Optional[builtins.str] = None,
        cloudwatch_secret_access_key: typing.Optional[builtins.str] = None,
        datadog_api_key: typing.Optional[builtins.str] = None,
        datadog_region: typing.Optional[builtins.str] = None,
        elasticsearch_endpoint: typing.Optional[builtins.str] = None,
        elasticsearch_password: typing.Optional[builtins.str] = None,
        elasticsearch_user: typing.Optional[builtins.str] = None,
        grafana_endpoint: typing.Optional[builtins.str] = None,
        grafana_password: typing.Optional[builtins.str] = None,
        grafana_user: typing.Optional[builtins.str] = None,
        http_basic_password: typing.Optional[builtins.str] = None,
        http_basic_user: typing.Optional[builtins.str] = None,
        http_bearer_token: typing.Optional[builtins.str] = None,
        http_codec: typing.Optional[builtins.str] = None,
        http_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        http_payload_prefix: typing.Optional[builtins.str] = None,
        http_payload_suffix: typing.Optional[builtins.str] = None,
        http_uri: typing.Optional[builtins.str] = None,
        newrelic_account_id: typing.Optional[builtins.str] = None,
        newrelic_license_key: typing.Optional[builtins.str] = None,
        newrelic_region: typing.Optional[builtins.str] = None,
        splunk_hecendpoint: typing.Optional[builtins.str] = None,
        splunk_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloudwatch_access_key_id: CloudWatch access key ID for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_access_key_id VaultCluster#cloudwatch_access_key_id}
        :param cloudwatch_region: CloudWatch region for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_region VaultCluster#cloudwatch_region}
        :param cloudwatch_secret_access_key: CloudWatch secret access key for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_secret_access_key VaultCluster#cloudwatch_secret_access_key}
        :param datadog_api_key: Datadog api key for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_api_key VaultCluster#datadog_api_key}
        :param datadog_region: Datadog region for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_region VaultCluster#datadog_region}
        :param elasticsearch_endpoint: ElasticSearch endpoint for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_endpoint VaultCluster#elasticsearch_endpoint}
        :param elasticsearch_password: ElasticSearch password for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_password VaultCluster#elasticsearch_password}
        :param elasticsearch_user: ElasticSearch user for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_user VaultCluster#elasticsearch_user}
        :param grafana_endpoint: Grafana endpoint for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_endpoint VaultCluster#grafana_endpoint}
        :param grafana_password: Grafana password for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_password VaultCluster#grafana_password}
        :param grafana_user: Grafana user for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_user VaultCluster#grafana_user}
        :param http_basic_password: HTTP basic authentication password for streaming audit logs, one of the two available authentication methods, can be specified only if http_basic_user is also provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_password VaultCluster#http_basic_password}
        :param http_basic_user: HTTP basic authentication username for streaming audit logs, one of the two available authentication methods, can be specified only if http_basic_password is also provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_user VaultCluster#http_basic_user}
        :param http_bearer_token: HTTP bearer authentication token for streaming audit logs, one of the two available authentication methods, can be specified only if http_basic_user and http_basic_password are not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_bearer_token VaultCluster#http_bearer_token}
        :param http_codec: HTTP codec for streaming audit logs, allowed values are JSON and NDJSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_codec VaultCluster#http_codec}
        :param http_compression: HTTP compression flag for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_compression VaultCluster#http_compression}
        :param http_headers: HTTP headers for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_headers VaultCluster#http_headers}
        :param http_method: HTTP payload method for streaming audit logs, , allowed values are PATCH, POST, or PUT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_method VaultCluster#http_method}
        :param http_payload_prefix: HTTP payload prefix for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_prefix VaultCluster#http_payload_prefix}
        :param http_payload_suffix: HTTP payload suffix for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_suffix VaultCluster#http_payload_suffix}
        :param http_uri: HTTP URI for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_uri VaultCluster#http_uri}
        :param newrelic_account_id: NewRelic Account ID for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_account_id VaultCluster#newrelic_account_id}
        :param newrelic_license_key: NewRelic license key for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_license_key VaultCluster#newrelic_license_key}
        :param newrelic_region: NewRelic region for streaming audit logs, allowed values are "US" and "EU". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_region VaultCluster#newrelic_region}
        :param splunk_hecendpoint: Splunk endpoint for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_hecendpoint VaultCluster#splunk_hecendpoint}
        :param splunk_token: Splunk token for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_token VaultCluster#splunk_token}
        '''
        value = VaultClusterAuditLogConfig(
            cloudwatch_access_key_id=cloudwatch_access_key_id,
            cloudwatch_region=cloudwatch_region,
            cloudwatch_secret_access_key=cloudwatch_secret_access_key,
            datadog_api_key=datadog_api_key,
            datadog_region=datadog_region,
            elasticsearch_endpoint=elasticsearch_endpoint,
            elasticsearch_password=elasticsearch_password,
            elasticsearch_user=elasticsearch_user,
            grafana_endpoint=grafana_endpoint,
            grafana_password=grafana_password,
            grafana_user=grafana_user,
            http_basic_password=http_basic_password,
            http_basic_user=http_basic_user,
            http_bearer_token=http_bearer_token,
            http_codec=http_codec,
            http_compression=http_compression,
            http_headers=http_headers,
            http_method=http_method,
            http_payload_prefix=http_payload_prefix,
            http_payload_suffix=http_payload_suffix,
            http_uri=http_uri,
            newrelic_account_id=newrelic_account_id,
            newrelic_license_key=newrelic_license_key,
            newrelic_region=newrelic_region,
            splunk_hecendpoint=splunk_hecendpoint,
            splunk_token=splunk_token,
        )

        return typing.cast(None, jsii.invoke(self, "putAuditLogConfig", [value]))

    @jsii.member(jsii_name="putIpAllowlist")
    def put_ip_allowlist(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VaultClusterIpAllowlistStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0d5ebbcb8f2ec1e2751e932862783f51e4081f0e243679212cb3df1a01facd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpAllowlist", [value]))

    @jsii.member(jsii_name="putMajorVersionUpgradeConfig")
    def put_major_version_upgrade_config(
        self,
        *,
        upgrade_type: builtins.str,
        maintenance_window_day: typing.Optional[builtins.str] = None,
        maintenance_window_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param upgrade_type: The major upgrade type for the cluster. Valid options for upgrade type - ``AUTOMATIC``, ``SCHEDULED``, ``MANUAL``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#upgrade_type VaultCluster#upgrade_type}
        :param maintenance_window_day: The maintenance day of the week for scheduled upgrades. Valid options for maintenance window day - ``MONDAY``, ``TUESDAY``, ``WEDNESDAY``, ``THURSDAY``, ``FRIDAY``, ``SATURDAY``, ``SUNDAY`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#maintenance_window_day VaultCluster#maintenance_window_day}
        :param maintenance_window_time: The maintenance time frame for scheduled upgrades. Valid options for maintenance window time - ``WINDOW_12AM_4AM``, ``WINDOW_6AM_10AM``, ``WINDOW_12PM_4PM``, ``WINDOW_6PM_10PM``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#maintenance_window_time VaultCluster#maintenance_window_time}
        '''
        value = VaultClusterMajorVersionUpgradeConfig(
            upgrade_type=upgrade_type,
            maintenance_window_day=maintenance_window_day,
            maintenance_window_time=maintenance_window_time,
        )

        return typing.cast(None, jsii.invoke(self, "putMajorVersionUpgradeConfig", [value]))

    @jsii.member(jsii_name="putMetricsConfig")
    def put_metrics_config(
        self,
        *,
        cloudwatch_access_key_id: typing.Optional[builtins.str] = None,
        cloudwatch_region: typing.Optional[builtins.str] = None,
        cloudwatch_secret_access_key: typing.Optional[builtins.str] = None,
        datadog_api_key: typing.Optional[builtins.str] = None,
        datadog_region: typing.Optional[builtins.str] = None,
        elasticsearch_endpoint: typing.Optional[builtins.str] = None,
        elasticsearch_password: typing.Optional[builtins.str] = None,
        elasticsearch_user: typing.Optional[builtins.str] = None,
        grafana_endpoint: typing.Optional[builtins.str] = None,
        grafana_password: typing.Optional[builtins.str] = None,
        grafana_user: typing.Optional[builtins.str] = None,
        http_basic_password: typing.Optional[builtins.str] = None,
        http_basic_user: typing.Optional[builtins.str] = None,
        http_bearer_token: typing.Optional[builtins.str] = None,
        http_codec: typing.Optional[builtins.str] = None,
        http_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        http_payload_prefix: typing.Optional[builtins.str] = None,
        http_payload_suffix: typing.Optional[builtins.str] = None,
        http_uri: typing.Optional[builtins.str] = None,
        newrelic_account_id: typing.Optional[builtins.str] = None,
        newrelic_license_key: typing.Optional[builtins.str] = None,
        newrelic_region: typing.Optional[builtins.str] = None,
        splunk_hecendpoint: typing.Optional[builtins.str] = None,
        splunk_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloudwatch_access_key_id: CloudWatch access key ID for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_access_key_id VaultCluster#cloudwatch_access_key_id}
        :param cloudwatch_region: CloudWatch region for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_region VaultCluster#cloudwatch_region}
        :param cloudwatch_secret_access_key: CloudWatch secret access key for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_secret_access_key VaultCluster#cloudwatch_secret_access_key}
        :param datadog_api_key: Datadog api key for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_api_key VaultCluster#datadog_api_key}
        :param datadog_region: Datadog region for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_region VaultCluster#datadog_region}
        :param elasticsearch_endpoint: ElasticSearch endpoint for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_endpoint VaultCluster#elasticsearch_endpoint}
        :param elasticsearch_password: ElasticSearch password for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_password VaultCluster#elasticsearch_password}
        :param elasticsearch_user: ElasticSearch user for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_user VaultCluster#elasticsearch_user}
        :param grafana_endpoint: Grafana endpoint for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_endpoint VaultCluster#grafana_endpoint}
        :param grafana_password: Grafana password for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_password VaultCluster#grafana_password}
        :param grafana_user: Grafana user for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_user VaultCluster#grafana_user}
        :param http_basic_password: HTTP basic authentication password for streaming metrics, one of the two available authentication methods, can be specified only if http_basic_user is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_password VaultCluster#http_basic_password}
        :param http_basic_user: HTTP basic authentication username for streaming metrics, one of the two available authentication methods, can be specified only if http_basic_password is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_user VaultCluster#http_basic_user}
        :param http_bearer_token: HTTP bearer authentication token for streaming metrics, one of the two available authentication methods, can be specified only if http_basic_user and http_basic_password are not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_bearer_token VaultCluster#http_bearer_token}
        :param http_codec: HTTP codec for streaming metrics, allowed values are JSON and NDJSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_codec VaultCluster#http_codec}
        :param http_compression: HTTP compression flag for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_compression VaultCluster#http_compression}
        :param http_headers: HTTP headers for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_headers VaultCluster#http_headers}
        :param http_method: HTTP payload method for streaming metrics, allowed values are PATCH, POST, or PUT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_method VaultCluster#http_method}
        :param http_payload_prefix: HTTP payload prefix for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_prefix VaultCluster#http_payload_prefix}
        :param http_payload_suffix: HTTP payload suffix for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_suffix VaultCluster#http_payload_suffix}
        :param http_uri: HTTP URI for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_uri VaultCluster#http_uri}
        :param newrelic_account_id: NewRelic Account ID for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_account_id VaultCluster#newrelic_account_id}
        :param newrelic_license_key: NewRelic license key for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_license_key VaultCluster#newrelic_license_key}
        :param newrelic_region: NewRelic region for streaming metrics, allowed values are "US" and "EU". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_region VaultCluster#newrelic_region}
        :param splunk_hecendpoint: Splunk endpoint for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_hecendpoint VaultCluster#splunk_hecendpoint}
        :param splunk_token: Splunk token for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_token VaultCluster#splunk_token}
        '''
        value = VaultClusterMetricsConfig(
            cloudwatch_access_key_id=cloudwatch_access_key_id,
            cloudwatch_region=cloudwatch_region,
            cloudwatch_secret_access_key=cloudwatch_secret_access_key,
            datadog_api_key=datadog_api_key,
            datadog_region=datadog_region,
            elasticsearch_endpoint=elasticsearch_endpoint,
            elasticsearch_password=elasticsearch_password,
            elasticsearch_user=elasticsearch_user,
            grafana_endpoint=grafana_endpoint,
            grafana_password=grafana_password,
            grafana_user=grafana_user,
            http_basic_password=http_basic_password,
            http_basic_user=http_basic_user,
            http_bearer_token=http_bearer_token,
            http_codec=http_codec,
            http_compression=http_compression,
            http_headers=http_headers,
            http_method=http_method,
            http_payload_prefix=http_payload_prefix,
            http_payload_suffix=http_payload_suffix,
            http_uri=http_uri,
            newrelic_account_id=newrelic_account_id,
            newrelic_license_key=newrelic_license_key,
            newrelic_region=newrelic_region,
            splunk_hecendpoint=splunk_hecendpoint,
            splunk_token=splunk_token,
        )

        return typing.cast(None, jsii.invoke(self, "putMetricsConfig", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#create VaultCluster#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#default VaultCluster#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#delete VaultCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#update VaultCluster#update}.
        '''
        value = VaultClusterTimeouts(
            create=create, default=default, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuditLogConfig")
    def reset_audit_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuditLogConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAllowlist")
    def reset_ip_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAllowlist", []))

    @jsii.member(jsii_name="resetMajorVersionUpgradeConfig")
    def reset_major_version_upgrade_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMajorVersionUpgradeConfig", []))

    @jsii.member(jsii_name="resetMetricsConfig")
    def reset_metrics_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsConfig", []))

    @jsii.member(jsii_name="resetMinVaultVersion")
    def reset_min_vault_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinVaultVersion", []))

    @jsii.member(jsii_name="resetPathsFilter")
    def reset_paths_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathsFilter", []))

    @jsii.member(jsii_name="resetPrimaryLink")
    def reset_primary_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryLink", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetProxyEndpoint")
    def reset_proxy_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyEndpoint", []))

    @jsii.member(jsii_name="resetPublicEndpoint")
    def reset_public_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicEndpoint", []))

    @jsii.member(jsii_name="resetTier")
    def reset_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTier", []))

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
    @jsii.member(jsii_name="auditLogConfig")
    def audit_log_config(self) -> "VaultClusterAuditLogConfigOutputReference":
        return typing.cast("VaultClusterAuditLogConfigOutputReference", jsii.get(self, "auditLogConfig"))

    @builtins.property
    @jsii.member(jsii_name="cloudProvider")
    def cloud_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudProvider"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="ipAllowlist")
    def ip_allowlist(self) -> "VaultClusterIpAllowlistStructList":
        return typing.cast("VaultClusterIpAllowlistStructList", jsii.get(self, "ipAllowlist"))

    @builtins.property
    @jsii.member(jsii_name="majorVersionUpgradeConfig")
    def major_version_upgrade_config(
        self,
    ) -> "VaultClusterMajorVersionUpgradeConfigOutputReference":
        return typing.cast("VaultClusterMajorVersionUpgradeConfigOutputReference", jsii.get(self, "majorVersionUpgradeConfig"))

    @builtins.property
    @jsii.member(jsii_name="metricsConfig")
    def metrics_config(self) -> "VaultClusterMetricsConfigOutputReference":
        return typing.cast("VaultClusterMetricsConfigOutputReference", jsii.get(self, "metricsConfig"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

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
    def timeouts(self) -> "VaultClusterTimeoutsOutputReference":
        return typing.cast("VaultClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vaultPrivateEndpointUrl")
    def vault_private_endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultPrivateEndpointUrl"))

    @builtins.property
    @jsii.member(jsii_name="vaultProxyEndpointUrl")
    def vault_proxy_endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultProxyEndpointUrl"))

    @builtins.property
    @jsii.member(jsii_name="vaultPublicEndpointUrl")
    def vault_public_endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultPublicEndpointUrl"))

    @builtins.property
    @jsii.member(jsii_name="vaultVersion")
    def vault_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultVersion"))

    @builtins.property
    @jsii.member(jsii_name="auditLogConfigInput")
    def audit_log_config_input(self) -> typing.Optional["VaultClusterAuditLogConfig"]:
        return typing.cast(typing.Optional["VaultClusterAuditLogConfig"], jsii.get(self, "auditLogConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VaultClusterIpAllowlistStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VaultClusterIpAllowlistStruct"]]], jsii.get(self, "ipAllowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="majorVersionUpgradeConfigInput")
    def major_version_upgrade_config_input(
        self,
    ) -> typing.Optional["VaultClusterMajorVersionUpgradeConfig"]:
        return typing.cast(typing.Optional["VaultClusterMajorVersionUpgradeConfig"], jsii.get(self, "majorVersionUpgradeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsConfigInput")
    def metrics_config_input(self) -> typing.Optional["VaultClusterMetricsConfig"]:
        return typing.cast(typing.Optional["VaultClusterMetricsConfig"], jsii.get(self, "metricsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="minVaultVersionInput")
    def min_vault_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minVaultVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsFilterInput")
    def paths_filter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryLinkInput")
    def primary_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyEndpointInput")
    def proxy_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="publicEndpointInput")
    def public_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c28bc1d0d3a11385f69f5b593a33f6d3cc36b251943c87e7d84b71d9f8a55c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hvnId")
    def hvn_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hvnId"))

    @hvn_id.setter
    def hvn_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cdedf475d77d4cb3670ceece6593d632a9a72936b6238f2f76aa2514ef4572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hvnId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c4e2848248807929ac0f0629a93ce153465a1bb489918b844c01429318169b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minVaultVersion")
    def min_vault_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minVaultVersion"))

    @min_vault_version.setter
    def min_vault_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90a99787bbba8532314d4fd46a461dc8ba4d79f11b79268b61109a69c9385f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minVaultVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathsFilter")
    def paths_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pathsFilter"))

    @paths_filter.setter
    def paths_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c447c3a56ed005d7cea3740b1d9073d95b302c6ca34d5cb42b113743dd43d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathsFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryLink")
    def primary_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryLink"))

    @primary_link.setter
    def primary_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd1ba2389475dbdef88d02a36491fcce5ddc9cb2a19ece1b06b2f06d94ce93c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46663258d898984c2d26b55c68517713e452a0fc7f350d4c14bf6b7f45e9e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyEndpoint")
    def proxy_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyEndpoint"))

    @proxy_endpoint.setter
    def proxy_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d845db4733b3eb319ff97d79116510674de8d3a9867ebcdce2e411a468e1e83f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyEndpoint", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__016406781c3e03ebe4828004b44a7c0d843366101b7bba83be5a1eda02278189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c863274558c2e6fbc79bf383c815279e3522fca7fe37c4616fd7fb98b80fa456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterAuditLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_access_key_id": "cloudwatchAccessKeyId",
        "cloudwatch_region": "cloudwatchRegion",
        "cloudwatch_secret_access_key": "cloudwatchSecretAccessKey",
        "datadog_api_key": "datadogApiKey",
        "datadog_region": "datadogRegion",
        "elasticsearch_endpoint": "elasticsearchEndpoint",
        "elasticsearch_password": "elasticsearchPassword",
        "elasticsearch_user": "elasticsearchUser",
        "grafana_endpoint": "grafanaEndpoint",
        "grafana_password": "grafanaPassword",
        "grafana_user": "grafanaUser",
        "http_basic_password": "httpBasicPassword",
        "http_basic_user": "httpBasicUser",
        "http_bearer_token": "httpBearerToken",
        "http_codec": "httpCodec",
        "http_compression": "httpCompression",
        "http_headers": "httpHeaders",
        "http_method": "httpMethod",
        "http_payload_prefix": "httpPayloadPrefix",
        "http_payload_suffix": "httpPayloadSuffix",
        "http_uri": "httpUri",
        "newrelic_account_id": "newrelicAccountId",
        "newrelic_license_key": "newrelicLicenseKey",
        "newrelic_region": "newrelicRegion",
        "splunk_hecendpoint": "splunkHecendpoint",
        "splunk_token": "splunkToken",
    },
)
class VaultClusterAuditLogConfig:
    def __init__(
        self,
        *,
        cloudwatch_access_key_id: typing.Optional[builtins.str] = None,
        cloudwatch_region: typing.Optional[builtins.str] = None,
        cloudwatch_secret_access_key: typing.Optional[builtins.str] = None,
        datadog_api_key: typing.Optional[builtins.str] = None,
        datadog_region: typing.Optional[builtins.str] = None,
        elasticsearch_endpoint: typing.Optional[builtins.str] = None,
        elasticsearch_password: typing.Optional[builtins.str] = None,
        elasticsearch_user: typing.Optional[builtins.str] = None,
        grafana_endpoint: typing.Optional[builtins.str] = None,
        grafana_password: typing.Optional[builtins.str] = None,
        grafana_user: typing.Optional[builtins.str] = None,
        http_basic_password: typing.Optional[builtins.str] = None,
        http_basic_user: typing.Optional[builtins.str] = None,
        http_bearer_token: typing.Optional[builtins.str] = None,
        http_codec: typing.Optional[builtins.str] = None,
        http_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        http_payload_prefix: typing.Optional[builtins.str] = None,
        http_payload_suffix: typing.Optional[builtins.str] = None,
        http_uri: typing.Optional[builtins.str] = None,
        newrelic_account_id: typing.Optional[builtins.str] = None,
        newrelic_license_key: typing.Optional[builtins.str] = None,
        newrelic_region: typing.Optional[builtins.str] = None,
        splunk_hecendpoint: typing.Optional[builtins.str] = None,
        splunk_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloudwatch_access_key_id: CloudWatch access key ID for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_access_key_id VaultCluster#cloudwatch_access_key_id}
        :param cloudwatch_region: CloudWatch region for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_region VaultCluster#cloudwatch_region}
        :param cloudwatch_secret_access_key: CloudWatch secret access key for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_secret_access_key VaultCluster#cloudwatch_secret_access_key}
        :param datadog_api_key: Datadog api key for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_api_key VaultCluster#datadog_api_key}
        :param datadog_region: Datadog region for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_region VaultCluster#datadog_region}
        :param elasticsearch_endpoint: ElasticSearch endpoint for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_endpoint VaultCluster#elasticsearch_endpoint}
        :param elasticsearch_password: ElasticSearch password for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_password VaultCluster#elasticsearch_password}
        :param elasticsearch_user: ElasticSearch user for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_user VaultCluster#elasticsearch_user}
        :param grafana_endpoint: Grafana endpoint for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_endpoint VaultCluster#grafana_endpoint}
        :param grafana_password: Grafana password for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_password VaultCluster#grafana_password}
        :param grafana_user: Grafana user for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_user VaultCluster#grafana_user}
        :param http_basic_password: HTTP basic authentication password for streaming audit logs, one of the two available authentication methods, can be specified only if http_basic_user is also provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_password VaultCluster#http_basic_password}
        :param http_basic_user: HTTP basic authentication username for streaming audit logs, one of the two available authentication methods, can be specified only if http_basic_password is also provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_user VaultCluster#http_basic_user}
        :param http_bearer_token: HTTP bearer authentication token for streaming audit logs, one of the two available authentication methods, can be specified only if http_basic_user and http_basic_password are not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_bearer_token VaultCluster#http_bearer_token}
        :param http_codec: HTTP codec for streaming audit logs, allowed values are JSON and NDJSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_codec VaultCluster#http_codec}
        :param http_compression: HTTP compression flag for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_compression VaultCluster#http_compression}
        :param http_headers: HTTP headers for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_headers VaultCluster#http_headers}
        :param http_method: HTTP payload method for streaming audit logs, , allowed values are PATCH, POST, or PUT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_method VaultCluster#http_method}
        :param http_payload_prefix: HTTP payload prefix for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_prefix VaultCluster#http_payload_prefix}
        :param http_payload_suffix: HTTP payload suffix for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_suffix VaultCluster#http_payload_suffix}
        :param http_uri: HTTP URI for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_uri VaultCluster#http_uri}
        :param newrelic_account_id: NewRelic Account ID for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_account_id VaultCluster#newrelic_account_id}
        :param newrelic_license_key: NewRelic license key for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_license_key VaultCluster#newrelic_license_key}
        :param newrelic_region: NewRelic region for streaming audit logs, allowed values are "US" and "EU". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_region VaultCluster#newrelic_region}
        :param splunk_hecendpoint: Splunk endpoint for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_hecendpoint VaultCluster#splunk_hecendpoint}
        :param splunk_token: Splunk token for streaming audit logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_token VaultCluster#splunk_token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945e965e9dab450573c42b8a5cc975ed8d0713bf41d459bead13f88051d0a34e)
            check_type(argname="argument cloudwatch_access_key_id", value=cloudwatch_access_key_id, expected_type=type_hints["cloudwatch_access_key_id"])
            check_type(argname="argument cloudwatch_region", value=cloudwatch_region, expected_type=type_hints["cloudwatch_region"])
            check_type(argname="argument cloudwatch_secret_access_key", value=cloudwatch_secret_access_key, expected_type=type_hints["cloudwatch_secret_access_key"])
            check_type(argname="argument datadog_api_key", value=datadog_api_key, expected_type=type_hints["datadog_api_key"])
            check_type(argname="argument datadog_region", value=datadog_region, expected_type=type_hints["datadog_region"])
            check_type(argname="argument elasticsearch_endpoint", value=elasticsearch_endpoint, expected_type=type_hints["elasticsearch_endpoint"])
            check_type(argname="argument elasticsearch_password", value=elasticsearch_password, expected_type=type_hints["elasticsearch_password"])
            check_type(argname="argument elasticsearch_user", value=elasticsearch_user, expected_type=type_hints["elasticsearch_user"])
            check_type(argname="argument grafana_endpoint", value=grafana_endpoint, expected_type=type_hints["grafana_endpoint"])
            check_type(argname="argument grafana_password", value=grafana_password, expected_type=type_hints["grafana_password"])
            check_type(argname="argument grafana_user", value=grafana_user, expected_type=type_hints["grafana_user"])
            check_type(argname="argument http_basic_password", value=http_basic_password, expected_type=type_hints["http_basic_password"])
            check_type(argname="argument http_basic_user", value=http_basic_user, expected_type=type_hints["http_basic_user"])
            check_type(argname="argument http_bearer_token", value=http_bearer_token, expected_type=type_hints["http_bearer_token"])
            check_type(argname="argument http_codec", value=http_codec, expected_type=type_hints["http_codec"])
            check_type(argname="argument http_compression", value=http_compression, expected_type=type_hints["http_compression"])
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument http_payload_prefix", value=http_payload_prefix, expected_type=type_hints["http_payload_prefix"])
            check_type(argname="argument http_payload_suffix", value=http_payload_suffix, expected_type=type_hints["http_payload_suffix"])
            check_type(argname="argument http_uri", value=http_uri, expected_type=type_hints["http_uri"])
            check_type(argname="argument newrelic_account_id", value=newrelic_account_id, expected_type=type_hints["newrelic_account_id"])
            check_type(argname="argument newrelic_license_key", value=newrelic_license_key, expected_type=type_hints["newrelic_license_key"])
            check_type(argname="argument newrelic_region", value=newrelic_region, expected_type=type_hints["newrelic_region"])
            check_type(argname="argument splunk_hecendpoint", value=splunk_hecendpoint, expected_type=type_hints["splunk_hecendpoint"])
            check_type(argname="argument splunk_token", value=splunk_token, expected_type=type_hints["splunk_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_access_key_id is not None:
            self._values["cloudwatch_access_key_id"] = cloudwatch_access_key_id
        if cloudwatch_region is not None:
            self._values["cloudwatch_region"] = cloudwatch_region
        if cloudwatch_secret_access_key is not None:
            self._values["cloudwatch_secret_access_key"] = cloudwatch_secret_access_key
        if datadog_api_key is not None:
            self._values["datadog_api_key"] = datadog_api_key
        if datadog_region is not None:
            self._values["datadog_region"] = datadog_region
        if elasticsearch_endpoint is not None:
            self._values["elasticsearch_endpoint"] = elasticsearch_endpoint
        if elasticsearch_password is not None:
            self._values["elasticsearch_password"] = elasticsearch_password
        if elasticsearch_user is not None:
            self._values["elasticsearch_user"] = elasticsearch_user
        if grafana_endpoint is not None:
            self._values["grafana_endpoint"] = grafana_endpoint
        if grafana_password is not None:
            self._values["grafana_password"] = grafana_password
        if grafana_user is not None:
            self._values["grafana_user"] = grafana_user
        if http_basic_password is not None:
            self._values["http_basic_password"] = http_basic_password
        if http_basic_user is not None:
            self._values["http_basic_user"] = http_basic_user
        if http_bearer_token is not None:
            self._values["http_bearer_token"] = http_bearer_token
        if http_codec is not None:
            self._values["http_codec"] = http_codec
        if http_compression is not None:
            self._values["http_compression"] = http_compression
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if http_method is not None:
            self._values["http_method"] = http_method
        if http_payload_prefix is not None:
            self._values["http_payload_prefix"] = http_payload_prefix
        if http_payload_suffix is not None:
            self._values["http_payload_suffix"] = http_payload_suffix
        if http_uri is not None:
            self._values["http_uri"] = http_uri
        if newrelic_account_id is not None:
            self._values["newrelic_account_id"] = newrelic_account_id
        if newrelic_license_key is not None:
            self._values["newrelic_license_key"] = newrelic_license_key
        if newrelic_region is not None:
            self._values["newrelic_region"] = newrelic_region
        if splunk_hecendpoint is not None:
            self._values["splunk_hecendpoint"] = splunk_hecendpoint
        if splunk_token is not None:
            self._values["splunk_token"] = splunk_token

    @builtins.property
    def cloudwatch_access_key_id(self) -> typing.Optional[builtins.str]:
        '''CloudWatch access key ID for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_access_key_id VaultCluster#cloudwatch_access_key_id}
        '''
        result = self._values.get("cloudwatch_access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch_region(self) -> typing.Optional[builtins.str]:
        '''CloudWatch region for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_region VaultCluster#cloudwatch_region}
        '''
        result = self._values.get("cloudwatch_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch_secret_access_key(self) -> typing.Optional[builtins.str]:
        '''CloudWatch secret access key for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_secret_access_key VaultCluster#cloudwatch_secret_access_key}
        '''
        result = self._values.get("cloudwatch_secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datadog_api_key(self) -> typing.Optional[builtins.str]:
        '''Datadog api key for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_api_key VaultCluster#datadog_api_key}
        '''
        result = self._values.get("datadog_api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datadog_region(self) -> typing.Optional[builtins.str]:
        '''Datadog region for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_region VaultCluster#datadog_region}
        '''
        result = self._values.get("datadog_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_endpoint(self) -> typing.Optional[builtins.str]:
        '''ElasticSearch endpoint for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_endpoint VaultCluster#elasticsearch_endpoint}
        '''
        result = self._values.get("elasticsearch_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_password(self) -> typing.Optional[builtins.str]:
        '''ElasticSearch password for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_password VaultCluster#elasticsearch_password}
        '''
        result = self._values.get("elasticsearch_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_user(self) -> typing.Optional[builtins.str]:
        '''ElasticSearch user for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_user VaultCluster#elasticsearch_user}
        '''
        result = self._values.get("elasticsearch_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grafana_endpoint(self) -> typing.Optional[builtins.str]:
        '''Grafana endpoint for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_endpoint VaultCluster#grafana_endpoint}
        '''
        result = self._values.get("grafana_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grafana_password(self) -> typing.Optional[builtins.str]:
        '''Grafana password for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_password VaultCluster#grafana_password}
        '''
        result = self._values.get("grafana_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grafana_user(self) -> typing.Optional[builtins.str]:
        '''Grafana user for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_user VaultCluster#grafana_user}
        '''
        result = self._values.get("grafana_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_basic_password(self) -> typing.Optional[builtins.str]:
        '''HTTP basic authentication password for streaming audit logs, one of the two available authentication methods, can be specified only if http_basic_user is also provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_password VaultCluster#http_basic_password}
        '''
        result = self._values.get("http_basic_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_basic_user(self) -> typing.Optional[builtins.str]:
        '''HTTP basic authentication username for streaming audit logs, one of the two available authentication methods, can be specified only if http_basic_password is also provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_user VaultCluster#http_basic_user}
        '''
        result = self._values.get("http_basic_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_bearer_token(self) -> typing.Optional[builtins.str]:
        '''HTTP bearer authentication token for streaming audit logs, one of the two available authentication methods, can be specified only if http_basic_user and http_basic_password are not provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_bearer_token VaultCluster#http_bearer_token}
        '''
        result = self._values.get("http_bearer_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_codec(self) -> typing.Optional[builtins.str]:
        '''HTTP codec for streaming audit logs, allowed values are JSON and NDJSON.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_codec VaultCluster#http_codec}
        '''
        result = self._values.get("http_codec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_compression(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''HTTP compression flag for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_compression VaultCluster#http_compression}
        '''
        result = self._values.get("http_compression")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''HTTP headers for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_headers VaultCluster#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''HTTP payload method for streaming audit logs, , allowed values are PATCH, POST, or PUT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_method VaultCluster#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_payload_prefix(self) -> typing.Optional[builtins.str]:
        '''HTTP payload prefix for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_prefix VaultCluster#http_payload_prefix}
        '''
        result = self._values.get("http_payload_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_payload_suffix(self) -> typing.Optional[builtins.str]:
        '''HTTP payload suffix for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_suffix VaultCluster#http_payload_suffix}
        '''
        result = self._values.get("http_payload_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_uri(self) -> typing.Optional[builtins.str]:
        '''HTTP URI for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_uri VaultCluster#http_uri}
        '''
        result = self._values.get("http_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def newrelic_account_id(self) -> typing.Optional[builtins.str]:
        '''NewRelic Account ID for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_account_id VaultCluster#newrelic_account_id}
        '''
        result = self._values.get("newrelic_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def newrelic_license_key(self) -> typing.Optional[builtins.str]:
        '''NewRelic license key for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_license_key VaultCluster#newrelic_license_key}
        '''
        result = self._values.get("newrelic_license_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def newrelic_region(self) -> typing.Optional[builtins.str]:
        '''NewRelic region for streaming audit logs, allowed values are "US" and "EU".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_region VaultCluster#newrelic_region}
        '''
        result = self._values.get("newrelic_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def splunk_hecendpoint(self) -> typing.Optional[builtins.str]:
        '''Splunk endpoint for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_hecendpoint VaultCluster#splunk_hecendpoint}
        '''
        result = self._values.get("splunk_hecendpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def splunk_token(self) -> typing.Optional[builtins.str]:
        '''Splunk token for streaming audit logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_token VaultCluster#splunk_token}
        '''
        result = self._values.get("splunk_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultClusterAuditLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultClusterAuditLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterAuditLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8b875f9e1e5a69e90f3ccbd14774843fdcf1ec3dea2e285c4304b00a740ea8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCloudwatchAccessKeyId")
    def reset_cloudwatch_access_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchAccessKeyId", []))

    @jsii.member(jsii_name="resetCloudwatchRegion")
    def reset_cloudwatch_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchRegion", []))

    @jsii.member(jsii_name="resetCloudwatchSecretAccessKey")
    def reset_cloudwatch_secret_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchSecretAccessKey", []))

    @jsii.member(jsii_name="resetDatadogApiKey")
    def reset_datadog_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadogApiKey", []))

    @jsii.member(jsii_name="resetDatadogRegion")
    def reset_datadog_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadogRegion", []))

    @jsii.member(jsii_name="resetElasticsearchEndpoint")
    def reset_elasticsearch_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchEndpoint", []))

    @jsii.member(jsii_name="resetElasticsearchPassword")
    def reset_elasticsearch_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchPassword", []))

    @jsii.member(jsii_name="resetElasticsearchUser")
    def reset_elasticsearch_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchUser", []))

    @jsii.member(jsii_name="resetGrafanaEndpoint")
    def reset_grafana_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrafanaEndpoint", []))

    @jsii.member(jsii_name="resetGrafanaPassword")
    def reset_grafana_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrafanaPassword", []))

    @jsii.member(jsii_name="resetGrafanaUser")
    def reset_grafana_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrafanaUser", []))

    @jsii.member(jsii_name="resetHttpBasicPassword")
    def reset_http_basic_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpBasicPassword", []))

    @jsii.member(jsii_name="resetHttpBasicUser")
    def reset_http_basic_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpBasicUser", []))

    @jsii.member(jsii_name="resetHttpBearerToken")
    def reset_http_bearer_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpBearerToken", []))

    @jsii.member(jsii_name="resetHttpCodec")
    def reset_http_codec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCodec", []))

    @jsii.member(jsii_name="resetHttpCompression")
    def reset_http_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCompression", []))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetHttpMethod")
    def reset_http_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethod", []))

    @jsii.member(jsii_name="resetHttpPayloadPrefix")
    def reset_http_payload_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpPayloadPrefix", []))

    @jsii.member(jsii_name="resetHttpPayloadSuffix")
    def reset_http_payload_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpPayloadSuffix", []))

    @jsii.member(jsii_name="resetHttpUri")
    def reset_http_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpUri", []))

    @jsii.member(jsii_name="resetNewrelicAccountId")
    def reset_newrelic_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewrelicAccountId", []))

    @jsii.member(jsii_name="resetNewrelicLicenseKey")
    def reset_newrelic_license_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewrelicLicenseKey", []))

    @jsii.member(jsii_name="resetNewrelicRegion")
    def reset_newrelic_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewrelicRegion", []))

    @jsii.member(jsii_name="resetSplunkHecendpoint")
    def reset_splunk_hecendpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplunkHecendpoint", []))

    @jsii.member(jsii_name="resetSplunkToken")
    def reset_splunk_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplunkToken", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchGroupName")
    def cloudwatch_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchGroupName"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchStreamName")
    def cloudwatch_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchStreamName"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchDataset")
    def elasticsearch_dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchDataset"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAccessKeyIdInput")
    def cloudwatch_access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchAccessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchRegionInput")
    def cloudwatch_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchSecretAccessKeyInput")
    def cloudwatch_secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchSecretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogApiKeyInput")
    def datadog_api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datadogApiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogRegionInput")
    def datadog_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datadogRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchEndpointInput")
    def elasticsearch_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchPasswordInput")
    def elasticsearch_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchUserInput")
    def elasticsearch_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchUserInput"))

    @builtins.property
    @jsii.member(jsii_name="grafanaEndpointInput")
    def grafana_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grafanaEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="grafanaPasswordInput")
    def grafana_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grafanaPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="grafanaUserInput")
    def grafana_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grafanaUserInput"))

    @builtins.property
    @jsii.member(jsii_name="httpBasicPasswordInput")
    def http_basic_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpBasicPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="httpBasicUserInput")
    def http_basic_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpBasicUserInput"))

    @builtins.property
    @jsii.member(jsii_name="httpBearerTokenInput")
    def http_bearer_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpBearerTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCodecInput")
    def http_codec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCodecInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCompressionInput")
    def http_compression_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpCompressionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="httpPayloadPrefixInput")
    def http_payload_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpPayloadPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="httpPayloadSuffixInput")
    def http_payload_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpPayloadSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="httpUriInput")
    def http_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpUriInput"))

    @builtins.property
    @jsii.member(jsii_name="newrelicAccountIdInput")
    def newrelic_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newrelicAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="newrelicLicenseKeyInput")
    def newrelic_license_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newrelicLicenseKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="newrelicRegionInput")
    def newrelic_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newrelicRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="splunkHecendpointInput")
    def splunk_hecendpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "splunkHecendpointInput"))

    @builtins.property
    @jsii.member(jsii_name="splunkTokenInput")
    def splunk_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "splunkTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAccessKeyId")
    def cloudwatch_access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchAccessKeyId"))

    @cloudwatch_access_key_id.setter
    def cloudwatch_access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c956f4d204b61d52c24ab82cf4bd3db61643a60ee25f267a37c5527c4672b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchAccessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudwatchRegion")
    def cloudwatch_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchRegion"))

    @cloudwatch_region.setter
    def cloudwatch_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb965ffa2d2b64591ae4dd554bdba65e764e37bccadc24e84259a13844eb5e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudwatchSecretAccessKey")
    def cloudwatch_secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchSecretAccessKey"))

    @cloudwatch_secret_access_key.setter
    def cloudwatch_secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37227117d192d2ce343997d96903ae09393d02948abb68d20741f959866671e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchSecretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datadogApiKey")
    def datadog_api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datadogApiKey"))

    @datadog_api_key.setter
    def datadog_api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b6ffc4fdcdfc68f19b0649b3264f8e211b7e469bd01556c00b2071a18f4583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datadogApiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datadogRegion")
    def datadog_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datadogRegion"))

    @datadog_region.setter
    def datadog_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52584035adf1cf6ac49bc62a4ac84427a1190b4e2a7d5a650d7e74ae236d99e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datadogRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticsearchEndpoint")
    def elasticsearch_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchEndpoint"))

    @elasticsearch_endpoint.setter
    def elasticsearch_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d529d88d9bea14a52c73eea4cba00d3434d6e979128b8e2872b03118d73adf50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticsearchPassword")
    def elasticsearch_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchPassword"))

    @elasticsearch_password.setter
    def elasticsearch_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88bb8a5696b324b29776ea449f774539f34cfba17aa4799429b1a51844383af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticsearchUser")
    def elasticsearch_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchUser"))

    @elasticsearch_user.setter
    def elasticsearch_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c0b927ec43598325947959512a056b2b45e20a034aabd58fa66571f9065f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grafanaEndpoint")
    def grafana_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grafanaEndpoint"))

    @grafana_endpoint.setter
    def grafana_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d1c04f0203c3a9f08cfaf64b33eb749078f35c5b9cc82332488d49b6209dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grafanaPassword")
    def grafana_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grafanaPassword"))

    @grafana_password.setter
    def grafana_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bf93f6ea32ddf32ca74534faaaf7627202436b7312f697895778a1d2d64871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grafanaUser")
    def grafana_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grafanaUser"))

    @grafana_user.setter
    def grafana_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9d0b3500812b9094d68925a982d1b6932bbf0ac677a39454abd2a24d756ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpBasicPassword")
    def http_basic_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpBasicPassword"))

    @http_basic_password.setter
    def http_basic_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7202d71685672f4243a816cb22d33cf1dd1493cfd58916b284cb0803524624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpBasicPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpBasicUser")
    def http_basic_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpBasicUser"))

    @http_basic_user.setter
    def http_basic_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c941feef05017f89c98a0b09427aa74b6283593b5d5292736aa53150f7ddd89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpBasicUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpBearerToken")
    def http_bearer_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpBearerToken"))

    @http_bearer_token.setter
    def http_bearer_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b10d967b3cd52ec26a2ddbf9b9e46251a0a94d0f78a549a37b55907f3ed810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpBearerToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCodec")
    def http_codec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCodec"))

    @http_codec.setter
    def http_codec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66e4614cc923e95dc7aa655441404d276aa10e12c028576245ef1e5e998ce0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCodec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCompression")
    def http_compression(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpCompression"))

    @http_compression.setter
    def http_compression(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd900b6cf459db8fed2063c75bbf028f168887d287d7181c71682c91f04e5e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCompression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "httpHeaders"))

    @http_headers.setter
    def http_headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae4e04d34a6bfb5251032a779984bf7a88b7a84c712eaa1642863538364f17e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbdba2697ea3f78c179d2aa733616101eac581864ed3d8ef673f1687bcffedce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpPayloadPrefix")
    def http_payload_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpPayloadPrefix"))

    @http_payload_prefix.setter
    def http_payload_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294120ebd8080fc24755438cfd5ca8aca3b996669f06c4469c452917e0aeeaf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpPayloadPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpPayloadSuffix")
    def http_payload_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpPayloadSuffix"))

    @http_payload_suffix.setter
    def http_payload_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27fd14b69df7479632091e254e69cbc8c157141295618a648f2110d973c7283e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpPayloadSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpUri")
    def http_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpUri"))

    @http_uri.setter
    def http_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e10d58dc7a1708597f664084fad3027458d1ba87b7981fedaf229e22fdd40c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newrelicAccountId")
    def newrelic_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newrelicAccountId"))

    @newrelic_account_id.setter
    def newrelic_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad6d8831dfcdae3205286f608e7a2458e6dfc44b7d3ce71b603a3cd5b950db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newrelicAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newrelicLicenseKey")
    def newrelic_license_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newrelicLicenseKey"))

    @newrelic_license_key.setter
    def newrelic_license_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be3938192c1bfe850f25da53abc192fe5d1c7aadbbf1049d031fa66e07672c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newrelicLicenseKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newrelicRegion")
    def newrelic_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newrelicRegion"))

    @newrelic_region.setter
    def newrelic_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66b53d581dcbe8ad9db5e4b7d512731a6a94a436f2e24180e10aca31d21bf6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newrelicRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="splunkHecendpoint")
    def splunk_hecendpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "splunkHecendpoint"))

    @splunk_hecendpoint.setter
    def splunk_hecendpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a053588ad2844b98959edfef3e01d2d1e9515509c6f776522a4756f7fe6fd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "splunkHecendpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="splunkToken")
    def splunk_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "splunkToken"))

    @splunk_token.setter
    def splunk_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7584064c3929586049d8fb7cba2238d2bfb9dab2c965ebaeeea3863eba36bf1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "splunkToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VaultClusterAuditLogConfig]:
        return typing.cast(typing.Optional[VaultClusterAuditLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VaultClusterAuditLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b2d391a17055a27cde669c5b609a5fa628c2645bdd1b56018ee38cb2caa8d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterConfig",
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
        "audit_log_config": "auditLogConfig",
        "id": "id",
        "ip_allowlist": "ipAllowlist",
        "major_version_upgrade_config": "majorVersionUpgradeConfig",
        "metrics_config": "metricsConfig",
        "min_vault_version": "minVaultVersion",
        "paths_filter": "pathsFilter",
        "primary_link": "primaryLink",
        "project_id": "projectId",
        "proxy_endpoint": "proxyEndpoint",
        "public_endpoint": "publicEndpoint",
        "tier": "tier",
        "timeouts": "timeouts",
    },
)
class VaultClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        audit_log_config: typing.Optional[typing.Union[VaultClusterAuditLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VaultClusterIpAllowlistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        major_version_upgrade_config: typing.Optional[typing.Union["VaultClusterMajorVersionUpgradeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_config: typing.Optional[typing.Union["VaultClusterMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        min_vault_version: typing.Optional[builtins.str] = None,
        paths_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        primary_link: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        proxy_endpoint: typing.Optional[builtins.str] = None,
        public_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VaultClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: The ID of the HCP Vault cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cluster_id VaultCluster#cluster_id}
        :param hvn_id: The ID of the HVN this HCP Vault cluster is associated to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#hvn_id VaultCluster#hvn_id}
        :param audit_log_config: audit_log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#audit_log_config VaultCluster#audit_log_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#id VaultCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_allowlist: ip_allowlist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#ip_allowlist VaultCluster#ip_allowlist}
        :param major_version_upgrade_config: major_version_upgrade_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#major_version_upgrade_config VaultCluster#major_version_upgrade_config}
        :param metrics_config: metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#metrics_config VaultCluster#metrics_config}
        :param min_vault_version: The minimum Vault version to use when creating the cluster. If not specified, it is defaulted to the version that is currently recommended by HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#min_vault_version VaultCluster#min_vault_version}
        :param paths_filter: The performance replication `paths filter <https://developer.hashicorp.com/vault/tutorials/cloud-ops/vault-replication-terraform>`_. Applies to performance replication secondaries only and operates in "deny" mode only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#paths_filter VaultCluster#paths_filter}
        :param primary_link: The ``self_link`` of the HCP Vault Plus tier cluster which is the primary in the performance replication setup with this HCP Vault Plus tier cluster. If not specified, it is a standalone Plus tier HCP Vault cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#primary_link VaultCluster#primary_link}
        :param project_id: The ID of the HCP project where the Vault cluster is located. If not specified, the project specified in the HCP Provider config block will be used, if configured. If a project is not configured in the HCP Provider config block, the oldest project in the organization will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#project_id VaultCluster#project_id}
        :param proxy_endpoint: Denotes that the cluster has a proxy endpoint. Valid options are ``ENABLED``, ``DISABLED``. Defaults to ``DISABLED``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#proxy_endpoint VaultCluster#proxy_endpoint}
        :param public_endpoint: Denotes that the cluster has a public endpoint. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#public_endpoint VaultCluster#public_endpoint}
        :param tier: Tier of the HCP Vault cluster. Valid options for tiers - ``dev``, ``standard_small``, ``standard_medium``, ``standard_large``, ``plus_small``, ``plus_medium``, ``plus_large``. See `pricing information <https://www.hashicorp.com/products/vault/pricing>`_. Changing a cluster's size or tier is only available to admins. See `Scale a cluster <https://registry.terraform.io/providers/hashicorp/hcp/latest/docs/guides/vault-scaling>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#tier VaultCluster#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#timeouts VaultCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(audit_log_config, dict):
            audit_log_config = VaultClusterAuditLogConfig(**audit_log_config)
        if isinstance(major_version_upgrade_config, dict):
            major_version_upgrade_config = VaultClusterMajorVersionUpgradeConfig(**major_version_upgrade_config)
        if isinstance(metrics_config, dict):
            metrics_config = VaultClusterMetricsConfig(**metrics_config)
        if isinstance(timeouts, dict):
            timeouts = VaultClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a47be8c3817c70555bc777416f18db7e158d5f4a408d5a70bef49dc6666cf0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument hvn_id", value=hvn_id, expected_type=type_hints["hvn_id"])
            check_type(argname="argument audit_log_config", value=audit_log_config, expected_type=type_hints["audit_log_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_allowlist", value=ip_allowlist, expected_type=type_hints["ip_allowlist"])
            check_type(argname="argument major_version_upgrade_config", value=major_version_upgrade_config, expected_type=type_hints["major_version_upgrade_config"])
            check_type(argname="argument metrics_config", value=metrics_config, expected_type=type_hints["metrics_config"])
            check_type(argname="argument min_vault_version", value=min_vault_version, expected_type=type_hints["min_vault_version"])
            check_type(argname="argument paths_filter", value=paths_filter, expected_type=type_hints["paths_filter"])
            check_type(argname="argument primary_link", value=primary_link, expected_type=type_hints["primary_link"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument proxy_endpoint", value=proxy_endpoint, expected_type=type_hints["proxy_endpoint"])
            check_type(argname="argument public_endpoint", value=public_endpoint, expected_type=type_hints["public_endpoint"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
            "hvn_id": hvn_id,
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
        if audit_log_config is not None:
            self._values["audit_log_config"] = audit_log_config
        if id is not None:
            self._values["id"] = id
        if ip_allowlist is not None:
            self._values["ip_allowlist"] = ip_allowlist
        if major_version_upgrade_config is not None:
            self._values["major_version_upgrade_config"] = major_version_upgrade_config
        if metrics_config is not None:
            self._values["metrics_config"] = metrics_config
        if min_vault_version is not None:
            self._values["min_vault_version"] = min_vault_version
        if paths_filter is not None:
            self._values["paths_filter"] = paths_filter
        if primary_link is not None:
            self._values["primary_link"] = primary_link
        if project_id is not None:
            self._values["project_id"] = project_id
        if proxy_endpoint is not None:
            self._values["proxy_endpoint"] = proxy_endpoint
        if public_endpoint is not None:
            self._values["public_endpoint"] = public_endpoint
        if tier is not None:
            self._values["tier"] = tier
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
        '''The ID of the HCP Vault cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cluster_id VaultCluster#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hvn_id(self) -> builtins.str:
        '''The ID of the HVN this HCP Vault cluster is associated to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#hvn_id VaultCluster#hvn_id}
        '''
        result = self._values.get("hvn_id")
        assert result is not None, "Required property 'hvn_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audit_log_config(self) -> typing.Optional[VaultClusterAuditLogConfig]:
        '''audit_log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#audit_log_config VaultCluster#audit_log_config}
        '''
        result = self._values.get("audit_log_config")
        return typing.cast(typing.Optional[VaultClusterAuditLogConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#id VaultCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_allowlist(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VaultClusterIpAllowlistStruct"]]]:
        '''ip_allowlist block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#ip_allowlist VaultCluster#ip_allowlist}
        '''
        result = self._values.get("ip_allowlist")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VaultClusterIpAllowlistStruct"]]], result)

    @builtins.property
    def major_version_upgrade_config(
        self,
    ) -> typing.Optional["VaultClusterMajorVersionUpgradeConfig"]:
        '''major_version_upgrade_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#major_version_upgrade_config VaultCluster#major_version_upgrade_config}
        '''
        result = self._values.get("major_version_upgrade_config")
        return typing.cast(typing.Optional["VaultClusterMajorVersionUpgradeConfig"], result)

    @builtins.property
    def metrics_config(self) -> typing.Optional["VaultClusterMetricsConfig"]:
        '''metrics_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#metrics_config VaultCluster#metrics_config}
        '''
        result = self._values.get("metrics_config")
        return typing.cast(typing.Optional["VaultClusterMetricsConfig"], result)

    @builtins.property
    def min_vault_version(self) -> typing.Optional[builtins.str]:
        '''The minimum Vault version to use when creating the cluster.

        If not specified, it is defaulted to the version that is currently recommended by HCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#min_vault_version VaultCluster#min_vault_version}
        '''
        result = self._values.get("min_vault_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paths_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The performance replication `paths filter <https://developer.hashicorp.com/vault/tutorials/cloud-ops/vault-replication-terraform>`_. Applies to performance replication secondaries only and operates in "deny" mode only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#paths_filter VaultCluster#paths_filter}
        '''
        result = self._values.get("paths_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def primary_link(self) -> typing.Optional[builtins.str]:
        '''The ``self_link`` of the HCP Vault Plus tier cluster which is the primary in the performance replication setup with this HCP Vault Plus tier cluster.

        If not specified, it is a standalone Plus tier HCP Vault cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#primary_link VaultCluster#primary_link}
        '''
        result = self._values.get("primary_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the HCP project where the Vault cluster is located.

        If not specified, the project specified in the HCP Provider config block will be used, if configured.
        If a project is not configured in the HCP Provider config block, the oldest project in the organization will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#project_id VaultCluster#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_endpoint(self) -> typing.Optional[builtins.str]:
        '''Denotes that the cluster has a proxy endpoint. Valid options are ``ENABLED``, ``DISABLED``. Defaults to ``DISABLED``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#proxy_endpoint VaultCluster#proxy_endpoint}
        '''
        result = self._values.get("proxy_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes that the cluster has a public endpoint. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#public_endpoint VaultCluster#public_endpoint}
        '''
        result = self._values.get("public_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''Tier of the HCP Vault cluster.

        Valid options for tiers - ``dev``, ``standard_small``, ``standard_medium``, ``standard_large``, ``plus_small``, ``plus_medium``, ``plus_large``. See `pricing information <https://www.hashicorp.com/products/vault/pricing>`_. Changing a cluster's size or tier is only available to admins. See `Scale a cluster <https://registry.terraform.io/providers/hashicorp/hcp/latest/docs/guides/vault-scaling>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#tier VaultCluster#tier}
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VaultClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#timeouts VaultCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VaultClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterIpAllowlistStruct",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "description": "description"},
)
class VaultClusterIpAllowlistStruct:
    def __init__(
        self,
        *,
        address: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: IP address range in CIDR notation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#address VaultCluster#address}
        :param description: Description to help identify source (maximum 255 chars). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#description VaultCluster#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48c36a2424146eaec6d565f2569acb3069b65fe5f4a807e3e0afed1f25f2bca)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#address VaultCluster#address}
        '''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description to help identify source (maximum 255 chars).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#description VaultCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultClusterIpAllowlistStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultClusterIpAllowlistStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterIpAllowlistStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__985eba6ed21e2a1c5d52f5d867ff7aac704220930d604d70d34dd6a72590bb43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VaultClusterIpAllowlistStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f53ceb6f0c328586cbb8f6382586cc87f4c28ed3645bb5ec09d2f4f36629b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VaultClusterIpAllowlistStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf49f37ffd1b565fd5b61994ee3b8c8ae03ab92510f1bd58a7d91793f3bf53b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c764d3e4a06026c3c41f9d125c3dea24fa70044256864acb196301c4bf511eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7dad15290a675b93a1195becc9883fa53829537f82288b9848c54e2bbfbc301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VaultClusterIpAllowlistStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VaultClusterIpAllowlistStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VaultClusterIpAllowlistStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30da3b098cb0125a3448fb843da715065ace2a1a01a368e92db5603ecaf6e098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VaultClusterIpAllowlistStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterIpAllowlistStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73155db860af3e73b315bfc634d2bc75cdb042758445c3192058d8c66399bc45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e06fdb61915d991389e2e36db84284474dda42314791401110578535f717557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb0ef2870e50cc24c4f6f030266222cb70499931f6975a6196e8c4e7b69546a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultClusterIpAllowlistStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultClusterIpAllowlistStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultClusterIpAllowlistStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9c81efaa39e470521c8b644e32669a91ec4fb9c4a89f80691be1a8a6d59afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterMajorVersionUpgradeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "upgrade_type": "upgradeType",
        "maintenance_window_day": "maintenanceWindowDay",
        "maintenance_window_time": "maintenanceWindowTime",
    },
)
class VaultClusterMajorVersionUpgradeConfig:
    def __init__(
        self,
        *,
        upgrade_type: builtins.str,
        maintenance_window_day: typing.Optional[builtins.str] = None,
        maintenance_window_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param upgrade_type: The major upgrade type for the cluster. Valid options for upgrade type - ``AUTOMATIC``, ``SCHEDULED``, ``MANUAL``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#upgrade_type VaultCluster#upgrade_type}
        :param maintenance_window_day: The maintenance day of the week for scheduled upgrades. Valid options for maintenance window day - ``MONDAY``, ``TUESDAY``, ``WEDNESDAY``, ``THURSDAY``, ``FRIDAY``, ``SATURDAY``, ``SUNDAY`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#maintenance_window_day VaultCluster#maintenance_window_day}
        :param maintenance_window_time: The maintenance time frame for scheduled upgrades. Valid options for maintenance window time - ``WINDOW_12AM_4AM``, ``WINDOW_6AM_10AM``, ``WINDOW_12PM_4PM``, ``WINDOW_6PM_10PM``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#maintenance_window_time VaultCluster#maintenance_window_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4962f49b844cabab740d8df01f3b70a715d3f1306b60fec54b6272426400d44)
            check_type(argname="argument upgrade_type", value=upgrade_type, expected_type=type_hints["upgrade_type"])
            check_type(argname="argument maintenance_window_day", value=maintenance_window_day, expected_type=type_hints["maintenance_window_day"])
            check_type(argname="argument maintenance_window_time", value=maintenance_window_time, expected_type=type_hints["maintenance_window_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "upgrade_type": upgrade_type,
        }
        if maintenance_window_day is not None:
            self._values["maintenance_window_day"] = maintenance_window_day
        if maintenance_window_time is not None:
            self._values["maintenance_window_time"] = maintenance_window_time

    @builtins.property
    def upgrade_type(self) -> builtins.str:
        '''The major upgrade type for the cluster. Valid options for upgrade type - ``AUTOMATIC``, ``SCHEDULED``, ``MANUAL``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#upgrade_type VaultCluster#upgrade_type}
        '''
        result = self._values.get("upgrade_type")
        assert result is not None, "Required property 'upgrade_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def maintenance_window_day(self) -> typing.Optional[builtins.str]:
        '''The maintenance day of the week for scheduled upgrades.

        Valid options for maintenance window day - ``MONDAY``, ``TUESDAY``, ``WEDNESDAY``, ``THURSDAY``, ``FRIDAY``, ``SATURDAY``, ``SUNDAY``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#maintenance_window_day VaultCluster#maintenance_window_day}
        '''
        result = self._values.get("maintenance_window_day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window_time(self) -> typing.Optional[builtins.str]:
        '''The maintenance time frame for scheduled upgrades. Valid options for maintenance window time - ``WINDOW_12AM_4AM``, ``WINDOW_6AM_10AM``, ``WINDOW_12PM_4PM``, ``WINDOW_6PM_10PM``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#maintenance_window_time VaultCluster#maintenance_window_time}
        '''
        result = self._values.get("maintenance_window_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultClusterMajorVersionUpgradeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultClusterMajorVersionUpgradeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterMajorVersionUpgradeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00220fe9e0d944a01da3073321aa1195a8785491ef20ede83c5c9e60456cfccc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaintenanceWindowDay")
    def reset_maintenance_window_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindowDay", []))

    @jsii.member(jsii_name="resetMaintenanceWindowTime")
    def reset_maintenance_window_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindowTime", []))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowDayInput")
    def maintenance_window_day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceWindowDayInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowTimeInput")
    def maintenance_window_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceWindowTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeTypeInput")
    def upgrade_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "upgradeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowDay")
    def maintenance_window_day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceWindowDay"))

    @maintenance_window_day.setter
    def maintenance_window_day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731c8b0a131354c50c4187c419df1ca0b4ceae942541b703dccc29bddc2ae24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceWindowDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowTime")
    def maintenance_window_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceWindowTime"))

    @maintenance_window_time.setter
    def maintenance_window_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f434d7fee16e563e0a028d6996e7baa865d83d6283058a983dd31e012a5ee7d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceWindowTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upgradeType")
    def upgrade_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upgradeType"))

    @upgrade_type.setter
    def upgrade_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985cbace5e3cd0b9202218537c218691890d235d32455d4d255ad4bdb2d63fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upgradeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VaultClusterMajorVersionUpgradeConfig]:
        return typing.cast(typing.Optional[VaultClusterMajorVersionUpgradeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VaultClusterMajorVersionUpgradeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73923462dd4285e4699c6c87591575ddc937cd2eac326dd6c048a6d19e1d13e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterMetricsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_access_key_id": "cloudwatchAccessKeyId",
        "cloudwatch_region": "cloudwatchRegion",
        "cloudwatch_secret_access_key": "cloudwatchSecretAccessKey",
        "datadog_api_key": "datadogApiKey",
        "datadog_region": "datadogRegion",
        "elasticsearch_endpoint": "elasticsearchEndpoint",
        "elasticsearch_password": "elasticsearchPassword",
        "elasticsearch_user": "elasticsearchUser",
        "grafana_endpoint": "grafanaEndpoint",
        "grafana_password": "grafanaPassword",
        "grafana_user": "grafanaUser",
        "http_basic_password": "httpBasicPassword",
        "http_basic_user": "httpBasicUser",
        "http_bearer_token": "httpBearerToken",
        "http_codec": "httpCodec",
        "http_compression": "httpCompression",
        "http_headers": "httpHeaders",
        "http_method": "httpMethod",
        "http_payload_prefix": "httpPayloadPrefix",
        "http_payload_suffix": "httpPayloadSuffix",
        "http_uri": "httpUri",
        "newrelic_account_id": "newrelicAccountId",
        "newrelic_license_key": "newrelicLicenseKey",
        "newrelic_region": "newrelicRegion",
        "splunk_hecendpoint": "splunkHecendpoint",
        "splunk_token": "splunkToken",
    },
)
class VaultClusterMetricsConfig:
    def __init__(
        self,
        *,
        cloudwatch_access_key_id: typing.Optional[builtins.str] = None,
        cloudwatch_region: typing.Optional[builtins.str] = None,
        cloudwatch_secret_access_key: typing.Optional[builtins.str] = None,
        datadog_api_key: typing.Optional[builtins.str] = None,
        datadog_region: typing.Optional[builtins.str] = None,
        elasticsearch_endpoint: typing.Optional[builtins.str] = None,
        elasticsearch_password: typing.Optional[builtins.str] = None,
        elasticsearch_user: typing.Optional[builtins.str] = None,
        grafana_endpoint: typing.Optional[builtins.str] = None,
        grafana_password: typing.Optional[builtins.str] = None,
        grafana_user: typing.Optional[builtins.str] = None,
        http_basic_password: typing.Optional[builtins.str] = None,
        http_basic_user: typing.Optional[builtins.str] = None,
        http_bearer_token: typing.Optional[builtins.str] = None,
        http_codec: typing.Optional[builtins.str] = None,
        http_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        http_payload_prefix: typing.Optional[builtins.str] = None,
        http_payload_suffix: typing.Optional[builtins.str] = None,
        http_uri: typing.Optional[builtins.str] = None,
        newrelic_account_id: typing.Optional[builtins.str] = None,
        newrelic_license_key: typing.Optional[builtins.str] = None,
        newrelic_region: typing.Optional[builtins.str] = None,
        splunk_hecendpoint: typing.Optional[builtins.str] = None,
        splunk_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloudwatch_access_key_id: CloudWatch access key ID for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_access_key_id VaultCluster#cloudwatch_access_key_id}
        :param cloudwatch_region: CloudWatch region for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_region VaultCluster#cloudwatch_region}
        :param cloudwatch_secret_access_key: CloudWatch secret access key for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_secret_access_key VaultCluster#cloudwatch_secret_access_key}
        :param datadog_api_key: Datadog api key for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_api_key VaultCluster#datadog_api_key}
        :param datadog_region: Datadog region for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_region VaultCluster#datadog_region}
        :param elasticsearch_endpoint: ElasticSearch endpoint for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_endpoint VaultCluster#elasticsearch_endpoint}
        :param elasticsearch_password: ElasticSearch password for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_password VaultCluster#elasticsearch_password}
        :param elasticsearch_user: ElasticSearch user for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_user VaultCluster#elasticsearch_user}
        :param grafana_endpoint: Grafana endpoint for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_endpoint VaultCluster#grafana_endpoint}
        :param grafana_password: Grafana password for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_password VaultCluster#grafana_password}
        :param grafana_user: Grafana user for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_user VaultCluster#grafana_user}
        :param http_basic_password: HTTP basic authentication password for streaming metrics, one of the two available authentication methods, can be specified only if http_basic_user is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_password VaultCluster#http_basic_password}
        :param http_basic_user: HTTP basic authentication username for streaming metrics, one of the two available authentication methods, can be specified only if http_basic_password is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_user VaultCluster#http_basic_user}
        :param http_bearer_token: HTTP bearer authentication token for streaming metrics, one of the two available authentication methods, can be specified only if http_basic_user and http_basic_password are not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_bearer_token VaultCluster#http_bearer_token}
        :param http_codec: HTTP codec for streaming metrics, allowed values are JSON and NDJSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_codec VaultCluster#http_codec}
        :param http_compression: HTTP compression flag for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_compression VaultCluster#http_compression}
        :param http_headers: HTTP headers for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_headers VaultCluster#http_headers}
        :param http_method: HTTP payload method for streaming metrics, allowed values are PATCH, POST, or PUT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_method VaultCluster#http_method}
        :param http_payload_prefix: HTTP payload prefix for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_prefix VaultCluster#http_payload_prefix}
        :param http_payload_suffix: HTTP payload suffix for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_suffix VaultCluster#http_payload_suffix}
        :param http_uri: HTTP URI for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_uri VaultCluster#http_uri}
        :param newrelic_account_id: NewRelic Account ID for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_account_id VaultCluster#newrelic_account_id}
        :param newrelic_license_key: NewRelic license key for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_license_key VaultCluster#newrelic_license_key}
        :param newrelic_region: NewRelic region for streaming metrics, allowed values are "US" and "EU". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_region VaultCluster#newrelic_region}
        :param splunk_hecendpoint: Splunk endpoint for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_hecendpoint VaultCluster#splunk_hecendpoint}
        :param splunk_token: Splunk token for streaming metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_token VaultCluster#splunk_token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41328d9c30b2160db3534c4e47502c0f13855650febdfb88b239dcb6d6ee814)
            check_type(argname="argument cloudwatch_access_key_id", value=cloudwatch_access_key_id, expected_type=type_hints["cloudwatch_access_key_id"])
            check_type(argname="argument cloudwatch_region", value=cloudwatch_region, expected_type=type_hints["cloudwatch_region"])
            check_type(argname="argument cloudwatch_secret_access_key", value=cloudwatch_secret_access_key, expected_type=type_hints["cloudwatch_secret_access_key"])
            check_type(argname="argument datadog_api_key", value=datadog_api_key, expected_type=type_hints["datadog_api_key"])
            check_type(argname="argument datadog_region", value=datadog_region, expected_type=type_hints["datadog_region"])
            check_type(argname="argument elasticsearch_endpoint", value=elasticsearch_endpoint, expected_type=type_hints["elasticsearch_endpoint"])
            check_type(argname="argument elasticsearch_password", value=elasticsearch_password, expected_type=type_hints["elasticsearch_password"])
            check_type(argname="argument elasticsearch_user", value=elasticsearch_user, expected_type=type_hints["elasticsearch_user"])
            check_type(argname="argument grafana_endpoint", value=grafana_endpoint, expected_type=type_hints["grafana_endpoint"])
            check_type(argname="argument grafana_password", value=grafana_password, expected_type=type_hints["grafana_password"])
            check_type(argname="argument grafana_user", value=grafana_user, expected_type=type_hints["grafana_user"])
            check_type(argname="argument http_basic_password", value=http_basic_password, expected_type=type_hints["http_basic_password"])
            check_type(argname="argument http_basic_user", value=http_basic_user, expected_type=type_hints["http_basic_user"])
            check_type(argname="argument http_bearer_token", value=http_bearer_token, expected_type=type_hints["http_bearer_token"])
            check_type(argname="argument http_codec", value=http_codec, expected_type=type_hints["http_codec"])
            check_type(argname="argument http_compression", value=http_compression, expected_type=type_hints["http_compression"])
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument http_payload_prefix", value=http_payload_prefix, expected_type=type_hints["http_payload_prefix"])
            check_type(argname="argument http_payload_suffix", value=http_payload_suffix, expected_type=type_hints["http_payload_suffix"])
            check_type(argname="argument http_uri", value=http_uri, expected_type=type_hints["http_uri"])
            check_type(argname="argument newrelic_account_id", value=newrelic_account_id, expected_type=type_hints["newrelic_account_id"])
            check_type(argname="argument newrelic_license_key", value=newrelic_license_key, expected_type=type_hints["newrelic_license_key"])
            check_type(argname="argument newrelic_region", value=newrelic_region, expected_type=type_hints["newrelic_region"])
            check_type(argname="argument splunk_hecendpoint", value=splunk_hecendpoint, expected_type=type_hints["splunk_hecendpoint"])
            check_type(argname="argument splunk_token", value=splunk_token, expected_type=type_hints["splunk_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_access_key_id is not None:
            self._values["cloudwatch_access_key_id"] = cloudwatch_access_key_id
        if cloudwatch_region is not None:
            self._values["cloudwatch_region"] = cloudwatch_region
        if cloudwatch_secret_access_key is not None:
            self._values["cloudwatch_secret_access_key"] = cloudwatch_secret_access_key
        if datadog_api_key is not None:
            self._values["datadog_api_key"] = datadog_api_key
        if datadog_region is not None:
            self._values["datadog_region"] = datadog_region
        if elasticsearch_endpoint is not None:
            self._values["elasticsearch_endpoint"] = elasticsearch_endpoint
        if elasticsearch_password is not None:
            self._values["elasticsearch_password"] = elasticsearch_password
        if elasticsearch_user is not None:
            self._values["elasticsearch_user"] = elasticsearch_user
        if grafana_endpoint is not None:
            self._values["grafana_endpoint"] = grafana_endpoint
        if grafana_password is not None:
            self._values["grafana_password"] = grafana_password
        if grafana_user is not None:
            self._values["grafana_user"] = grafana_user
        if http_basic_password is not None:
            self._values["http_basic_password"] = http_basic_password
        if http_basic_user is not None:
            self._values["http_basic_user"] = http_basic_user
        if http_bearer_token is not None:
            self._values["http_bearer_token"] = http_bearer_token
        if http_codec is not None:
            self._values["http_codec"] = http_codec
        if http_compression is not None:
            self._values["http_compression"] = http_compression
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if http_method is not None:
            self._values["http_method"] = http_method
        if http_payload_prefix is not None:
            self._values["http_payload_prefix"] = http_payload_prefix
        if http_payload_suffix is not None:
            self._values["http_payload_suffix"] = http_payload_suffix
        if http_uri is not None:
            self._values["http_uri"] = http_uri
        if newrelic_account_id is not None:
            self._values["newrelic_account_id"] = newrelic_account_id
        if newrelic_license_key is not None:
            self._values["newrelic_license_key"] = newrelic_license_key
        if newrelic_region is not None:
            self._values["newrelic_region"] = newrelic_region
        if splunk_hecendpoint is not None:
            self._values["splunk_hecendpoint"] = splunk_hecendpoint
        if splunk_token is not None:
            self._values["splunk_token"] = splunk_token

    @builtins.property
    def cloudwatch_access_key_id(self) -> typing.Optional[builtins.str]:
        '''CloudWatch access key ID for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_access_key_id VaultCluster#cloudwatch_access_key_id}
        '''
        result = self._values.get("cloudwatch_access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch_region(self) -> typing.Optional[builtins.str]:
        '''CloudWatch region for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_region VaultCluster#cloudwatch_region}
        '''
        result = self._values.get("cloudwatch_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch_secret_access_key(self) -> typing.Optional[builtins.str]:
        '''CloudWatch secret access key for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#cloudwatch_secret_access_key VaultCluster#cloudwatch_secret_access_key}
        '''
        result = self._values.get("cloudwatch_secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datadog_api_key(self) -> typing.Optional[builtins.str]:
        '''Datadog api key for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_api_key VaultCluster#datadog_api_key}
        '''
        result = self._values.get("datadog_api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datadog_region(self) -> typing.Optional[builtins.str]:
        '''Datadog region for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#datadog_region VaultCluster#datadog_region}
        '''
        result = self._values.get("datadog_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_endpoint(self) -> typing.Optional[builtins.str]:
        '''ElasticSearch endpoint for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_endpoint VaultCluster#elasticsearch_endpoint}
        '''
        result = self._values.get("elasticsearch_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_password(self) -> typing.Optional[builtins.str]:
        '''ElasticSearch password for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_password VaultCluster#elasticsearch_password}
        '''
        result = self._values.get("elasticsearch_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_user(self) -> typing.Optional[builtins.str]:
        '''ElasticSearch user for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#elasticsearch_user VaultCluster#elasticsearch_user}
        '''
        result = self._values.get("elasticsearch_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grafana_endpoint(self) -> typing.Optional[builtins.str]:
        '''Grafana endpoint for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_endpoint VaultCluster#grafana_endpoint}
        '''
        result = self._values.get("grafana_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grafana_password(self) -> typing.Optional[builtins.str]:
        '''Grafana password for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_password VaultCluster#grafana_password}
        '''
        result = self._values.get("grafana_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grafana_user(self) -> typing.Optional[builtins.str]:
        '''Grafana user for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#grafana_user VaultCluster#grafana_user}
        '''
        result = self._values.get("grafana_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_basic_password(self) -> typing.Optional[builtins.str]:
        '''HTTP basic authentication password for streaming metrics, one of the two available authentication methods, can be specified only if http_basic_user is also specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_password VaultCluster#http_basic_password}
        '''
        result = self._values.get("http_basic_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_basic_user(self) -> typing.Optional[builtins.str]:
        '''HTTP basic authentication username for streaming metrics, one of the two available authentication methods, can be specified only if http_basic_password is also specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_basic_user VaultCluster#http_basic_user}
        '''
        result = self._values.get("http_basic_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_bearer_token(self) -> typing.Optional[builtins.str]:
        '''HTTP bearer authentication token for streaming metrics, one of the two available authentication methods, can be specified only if http_basic_user and http_basic_password are not provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_bearer_token VaultCluster#http_bearer_token}
        '''
        result = self._values.get("http_bearer_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_codec(self) -> typing.Optional[builtins.str]:
        '''HTTP codec for streaming metrics, allowed values are JSON and NDJSON.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_codec VaultCluster#http_codec}
        '''
        result = self._values.get("http_codec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_compression(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''HTTP compression flag for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_compression VaultCluster#http_compression}
        '''
        result = self._values.get("http_compression")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''HTTP headers for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_headers VaultCluster#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''HTTP payload method for streaming metrics, allowed values are PATCH, POST, or PUT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_method VaultCluster#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_payload_prefix(self) -> typing.Optional[builtins.str]:
        '''HTTP payload prefix for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_prefix VaultCluster#http_payload_prefix}
        '''
        result = self._values.get("http_payload_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_payload_suffix(self) -> typing.Optional[builtins.str]:
        '''HTTP payload suffix for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_payload_suffix VaultCluster#http_payload_suffix}
        '''
        result = self._values.get("http_payload_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_uri(self) -> typing.Optional[builtins.str]:
        '''HTTP URI for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#http_uri VaultCluster#http_uri}
        '''
        result = self._values.get("http_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def newrelic_account_id(self) -> typing.Optional[builtins.str]:
        '''NewRelic Account ID for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_account_id VaultCluster#newrelic_account_id}
        '''
        result = self._values.get("newrelic_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def newrelic_license_key(self) -> typing.Optional[builtins.str]:
        '''NewRelic license key for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_license_key VaultCluster#newrelic_license_key}
        '''
        result = self._values.get("newrelic_license_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def newrelic_region(self) -> typing.Optional[builtins.str]:
        '''NewRelic region for streaming metrics, allowed values are "US" and "EU".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#newrelic_region VaultCluster#newrelic_region}
        '''
        result = self._values.get("newrelic_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def splunk_hecendpoint(self) -> typing.Optional[builtins.str]:
        '''Splunk endpoint for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_hecendpoint VaultCluster#splunk_hecendpoint}
        '''
        result = self._values.get("splunk_hecendpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def splunk_token(self) -> typing.Optional[builtins.str]:
        '''Splunk token for streaming metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#splunk_token VaultCluster#splunk_token}
        '''
        result = self._values.get("splunk_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultClusterMetricsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultClusterMetricsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterMetricsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7573747a2312afa8ffc8dafc01025857a8dc813746d0e47c1ba6fbbe8778ac35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCloudwatchAccessKeyId")
    def reset_cloudwatch_access_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchAccessKeyId", []))

    @jsii.member(jsii_name="resetCloudwatchRegion")
    def reset_cloudwatch_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchRegion", []))

    @jsii.member(jsii_name="resetCloudwatchSecretAccessKey")
    def reset_cloudwatch_secret_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchSecretAccessKey", []))

    @jsii.member(jsii_name="resetDatadogApiKey")
    def reset_datadog_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadogApiKey", []))

    @jsii.member(jsii_name="resetDatadogRegion")
    def reset_datadog_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadogRegion", []))

    @jsii.member(jsii_name="resetElasticsearchEndpoint")
    def reset_elasticsearch_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchEndpoint", []))

    @jsii.member(jsii_name="resetElasticsearchPassword")
    def reset_elasticsearch_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchPassword", []))

    @jsii.member(jsii_name="resetElasticsearchUser")
    def reset_elasticsearch_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchUser", []))

    @jsii.member(jsii_name="resetGrafanaEndpoint")
    def reset_grafana_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrafanaEndpoint", []))

    @jsii.member(jsii_name="resetGrafanaPassword")
    def reset_grafana_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrafanaPassword", []))

    @jsii.member(jsii_name="resetGrafanaUser")
    def reset_grafana_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrafanaUser", []))

    @jsii.member(jsii_name="resetHttpBasicPassword")
    def reset_http_basic_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpBasicPassword", []))

    @jsii.member(jsii_name="resetHttpBasicUser")
    def reset_http_basic_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpBasicUser", []))

    @jsii.member(jsii_name="resetHttpBearerToken")
    def reset_http_bearer_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpBearerToken", []))

    @jsii.member(jsii_name="resetHttpCodec")
    def reset_http_codec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCodec", []))

    @jsii.member(jsii_name="resetHttpCompression")
    def reset_http_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCompression", []))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetHttpMethod")
    def reset_http_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethod", []))

    @jsii.member(jsii_name="resetHttpPayloadPrefix")
    def reset_http_payload_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpPayloadPrefix", []))

    @jsii.member(jsii_name="resetHttpPayloadSuffix")
    def reset_http_payload_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpPayloadSuffix", []))

    @jsii.member(jsii_name="resetHttpUri")
    def reset_http_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpUri", []))

    @jsii.member(jsii_name="resetNewrelicAccountId")
    def reset_newrelic_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewrelicAccountId", []))

    @jsii.member(jsii_name="resetNewrelicLicenseKey")
    def reset_newrelic_license_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewrelicLicenseKey", []))

    @jsii.member(jsii_name="resetNewrelicRegion")
    def reset_newrelic_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewrelicRegion", []))

    @jsii.member(jsii_name="resetSplunkHecendpoint")
    def reset_splunk_hecendpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplunkHecendpoint", []))

    @jsii.member(jsii_name="resetSplunkToken")
    def reset_splunk_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplunkToken", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchNamespace")
    def cloudwatch_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchNamespace"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchDataset")
    def elasticsearch_dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchDataset"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAccessKeyIdInput")
    def cloudwatch_access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchAccessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchRegionInput")
    def cloudwatch_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchSecretAccessKeyInput")
    def cloudwatch_secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchSecretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogApiKeyInput")
    def datadog_api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datadogApiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogRegionInput")
    def datadog_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datadogRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchEndpointInput")
    def elasticsearch_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchPasswordInput")
    def elasticsearch_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchUserInput")
    def elasticsearch_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchUserInput"))

    @builtins.property
    @jsii.member(jsii_name="grafanaEndpointInput")
    def grafana_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grafanaEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="grafanaPasswordInput")
    def grafana_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grafanaPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="grafanaUserInput")
    def grafana_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grafanaUserInput"))

    @builtins.property
    @jsii.member(jsii_name="httpBasicPasswordInput")
    def http_basic_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpBasicPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="httpBasicUserInput")
    def http_basic_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpBasicUserInput"))

    @builtins.property
    @jsii.member(jsii_name="httpBearerTokenInput")
    def http_bearer_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpBearerTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCodecInput")
    def http_codec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCodecInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCompressionInput")
    def http_compression_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpCompressionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="httpPayloadPrefixInput")
    def http_payload_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpPayloadPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="httpPayloadSuffixInput")
    def http_payload_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpPayloadSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="httpUriInput")
    def http_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpUriInput"))

    @builtins.property
    @jsii.member(jsii_name="newrelicAccountIdInput")
    def newrelic_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newrelicAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="newrelicLicenseKeyInput")
    def newrelic_license_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newrelicLicenseKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="newrelicRegionInput")
    def newrelic_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newrelicRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="splunkHecendpointInput")
    def splunk_hecendpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "splunkHecendpointInput"))

    @builtins.property
    @jsii.member(jsii_name="splunkTokenInput")
    def splunk_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "splunkTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAccessKeyId")
    def cloudwatch_access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchAccessKeyId"))

    @cloudwatch_access_key_id.setter
    def cloudwatch_access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758bc1323488d37e5be24cb588eb05e9b1ea186ddf33106231f0942e6a250457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchAccessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudwatchRegion")
    def cloudwatch_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchRegion"))

    @cloudwatch_region.setter
    def cloudwatch_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ca2107c285ff7103e9d8cd7e2d0976cdb9f6a3feba8c720609ff9b9eb3ec6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudwatchSecretAccessKey")
    def cloudwatch_secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchSecretAccessKey"))

    @cloudwatch_secret_access_key.setter
    def cloudwatch_secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68ac04c06206961e5cf9ba5882a68cb0bfbd85ecfdd142d184b698fe4a4f6f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchSecretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datadogApiKey")
    def datadog_api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datadogApiKey"))

    @datadog_api_key.setter
    def datadog_api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01774f33baeaf10f919c131dc102f79f36eeff62b05d905990090cc7a031f8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datadogApiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datadogRegion")
    def datadog_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datadogRegion"))

    @datadog_region.setter
    def datadog_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53493b753297becfad9e332d6d76bf38108bc351b6b3e20baddb9bb07893b458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datadogRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticsearchEndpoint")
    def elasticsearch_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchEndpoint"))

    @elasticsearch_endpoint.setter
    def elasticsearch_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e4cb56ff8310fc10c9c431d7e653a8a9253b3f4174b00ce6c2b7f625417bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticsearchPassword")
    def elasticsearch_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchPassword"))

    @elasticsearch_password.setter
    def elasticsearch_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7451546117c82e865df91b13a3a9cd2f030683c0b55f26f22fd2331f19765c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticsearchUser")
    def elasticsearch_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchUser"))

    @elasticsearch_user.setter
    def elasticsearch_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ac0a029a6e68ca276d64fe802736b4e2cb729b3f3b720a0f2a817e6c5ba9e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grafanaEndpoint")
    def grafana_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grafanaEndpoint"))

    @grafana_endpoint.setter
    def grafana_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae544b6a716e103200c258e30bdeecaffec6121c50d96449de5d9b48fbbc24c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grafanaPassword")
    def grafana_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grafanaPassword"))

    @grafana_password.setter
    def grafana_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1064d1abe056bb9b3eb383bd3d0f5cb018fb61bf6744005bc22fc06f26bca5cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grafanaUser")
    def grafana_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grafanaUser"))

    @grafana_user.setter
    def grafana_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc49e4808e51cb5e796669e09cca32630adbb4539a73b19a0900c53fcf47a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpBasicPassword")
    def http_basic_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpBasicPassword"))

    @http_basic_password.setter
    def http_basic_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd2272cc554376c4ee7460e1ece41acf6e82ab18159262787e46844c534e4de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpBasicPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpBasicUser")
    def http_basic_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpBasicUser"))

    @http_basic_user.setter
    def http_basic_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68a7991850fa3b8895c725822d25de33cf88bc11e15ca05a15a6d9f72aca641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpBasicUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpBearerToken")
    def http_bearer_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpBearerToken"))

    @http_bearer_token.setter
    def http_bearer_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d193928fb15de28a352119ab0730245621db1a2de614cab0a647f47da56aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpBearerToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCodec")
    def http_codec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCodec"))

    @http_codec.setter
    def http_codec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b08897bda522f649369a0f5822f7068f42a9a2f17f40c33da88d37c168835e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCodec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCompression")
    def http_compression(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpCompression"))

    @http_compression.setter
    def http_compression(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709586c778e6e98a06a5c98c19f9da11ca2ee2892df0096c9208c626f08c6b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCompression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "httpHeaders"))

    @http_headers.setter
    def http_headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e0be2fd685f7d14c400739a883e0233d60e056fa4929c6cbdbb9075836ef4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67c4f59028e7f55cab0d141cc1c000d3c1c2944dc8535327858993f43755570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpPayloadPrefix")
    def http_payload_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpPayloadPrefix"))

    @http_payload_prefix.setter
    def http_payload_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7947b144062ddc10d647cc3a19078eb0b8a24f34e18f4fe8c6c6af1addcbff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpPayloadPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpPayloadSuffix")
    def http_payload_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpPayloadSuffix"))

    @http_payload_suffix.setter
    def http_payload_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f5fe7bbf17e4a963687ca4ae201ce034a0d1b95d3d2d048378c7d938d738cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpPayloadSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpUri")
    def http_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpUri"))

    @http_uri.setter
    def http_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d6b376f5f719508a680e77ead2ef96ce3a9418ee4e63d88f543073ae53a2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newrelicAccountId")
    def newrelic_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newrelicAccountId"))

    @newrelic_account_id.setter
    def newrelic_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d46b16c4dae7a6c0dc38aafe4b0fb1ea9111a14e463f6531d8e9588ba40e6a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newrelicAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newrelicLicenseKey")
    def newrelic_license_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newrelicLicenseKey"))

    @newrelic_license_key.setter
    def newrelic_license_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a2bb7dafe9c4af8a2847ca5d16dd8b6fdffff5d34d9a2cfb87341b004ea74e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newrelicLicenseKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newrelicRegion")
    def newrelic_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newrelicRegion"))

    @newrelic_region.setter
    def newrelic_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f100b864dc5edf018fb3edd2e0d5c157421bdc6fc551acdd95f93b9ea0639d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newrelicRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="splunkHecendpoint")
    def splunk_hecendpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "splunkHecendpoint"))

    @splunk_hecendpoint.setter
    def splunk_hecendpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3d1fedf5a113300f4ff7aff7390f5a7677acca337373f048c07ca807be7bd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "splunkHecendpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="splunkToken")
    def splunk_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "splunkToken"))

    @splunk_token.setter
    def splunk_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41262da7c69a34522658c9a64fb97b513270eab90b33134705d21e460bf4bf7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "splunkToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VaultClusterMetricsConfig]:
        return typing.cast(typing.Optional[VaultClusterMetricsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VaultClusterMetricsConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2bf482f44b38423d4061abe71c12776c465cb81d41e5ec0fd2fd93519e289f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "default": "default",
        "delete": "delete",
        "update": "update",
    },
)
class VaultClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#create VaultCluster#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#default VaultCluster#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#delete VaultCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#update VaultCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ee5e56e863fb68b056cf0c52c11694127fd2447b2109705c1c013124bc122b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#create VaultCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#default VaultCluster#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#delete VaultCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_cluster#update VaultCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultCluster.VaultClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65ecdf217b4bc03cba984541a801600b2d5439419fe5d42ba40ff7ac32ec3333)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db2c8ee9a177a1817b11e58fd9878424e1054d355e3bcb7b746bbe30fa3cbc2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @default.setter
    def default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87e66bf7ba09872850753eb0320a0428faf4ccd45ba0b681c88af537cb66fbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b560841a2a171c6555944671bf203111462c74d3d57852b50f20076467171e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507fb6faf5cecc7fb6c63feaca0dae7ff5b1a3150654d705aecead89ab25793c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc0b876897d7750cc1f48d98ef8fac9b2418b3c42aad84f70d54d171bb85f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VaultCluster",
    "VaultClusterAuditLogConfig",
    "VaultClusterAuditLogConfigOutputReference",
    "VaultClusterConfig",
    "VaultClusterIpAllowlistStruct",
    "VaultClusterIpAllowlistStructList",
    "VaultClusterIpAllowlistStructOutputReference",
    "VaultClusterMajorVersionUpgradeConfig",
    "VaultClusterMajorVersionUpgradeConfigOutputReference",
    "VaultClusterMetricsConfig",
    "VaultClusterMetricsConfigOutputReference",
    "VaultClusterTimeouts",
    "VaultClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a0a1b511b563b877d6fa1e39c5fcee395fa5006b8ec1cdc089eaff3f1e18e966(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    hvn_id: builtins.str,
    audit_log_config: typing.Optional[typing.Union[VaultClusterAuditLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VaultClusterIpAllowlistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    major_version_upgrade_config: typing.Optional[typing.Union[VaultClusterMajorVersionUpgradeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metrics_config: typing.Optional[typing.Union[VaultClusterMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    min_vault_version: typing.Optional[builtins.str] = None,
    paths_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    primary_link: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    proxy_endpoint: typing.Optional[builtins.str] = None,
    public_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VaultClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d58842deedd49ef02ced6c37958c2839e494ba9286baf07c9f6f708cdb80270f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0d5ebbcb8f2ec1e2751e932862783f51e4081f0e243679212cb3df1a01facd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VaultClusterIpAllowlistStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28bc1d0d3a11385f69f5b593a33f6d3cc36b251943c87e7d84b71d9f8a55c96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cdedf475d77d4cb3670ceece6593d632a9a72936b6238f2f76aa2514ef4572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c4e2848248807929ac0f0629a93ce153465a1bb489918b844c01429318169b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90a99787bbba8532314d4fd46a461dc8ba4d79f11b79268b61109a69c9385f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c447c3a56ed005d7cea3740b1d9073d95b302c6ca34d5cb42b113743dd43d4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd1ba2389475dbdef88d02a36491fcce5ddc9cb2a19ece1b06b2f06d94ce93c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46663258d898984c2d26b55c68517713e452a0fc7f350d4c14bf6b7f45e9e37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d845db4733b3eb319ff97d79116510674de8d3a9867ebcdce2e411a468e1e83f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016406781c3e03ebe4828004b44a7c0d843366101b7bba83be5a1eda02278189(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c863274558c2e6fbc79bf383c815279e3522fca7fe37c4616fd7fb98b80fa456(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945e965e9dab450573c42b8a5cc975ed8d0713bf41d459bead13f88051d0a34e(
    *,
    cloudwatch_access_key_id: typing.Optional[builtins.str] = None,
    cloudwatch_region: typing.Optional[builtins.str] = None,
    cloudwatch_secret_access_key: typing.Optional[builtins.str] = None,
    datadog_api_key: typing.Optional[builtins.str] = None,
    datadog_region: typing.Optional[builtins.str] = None,
    elasticsearch_endpoint: typing.Optional[builtins.str] = None,
    elasticsearch_password: typing.Optional[builtins.str] = None,
    elasticsearch_user: typing.Optional[builtins.str] = None,
    grafana_endpoint: typing.Optional[builtins.str] = None,
    grafana_password: typing.Optional[builtins.str] = None,
    grafana_user: typing.Optional[builtins.str] = None,
    http_basic_password: typing.Optional[builtins.str] = None,
    http_basic_user: typing.Optional[builtins.str] = None,
    http_bearer_token: typing.Optional[builtins.str] = None,
    http_codec: typing.Optional[builtins.str] = None,
    http_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    http_method: typing.Optional[builtins.str] = None,
    http_payload_prefix: typing.Optional[builtins.str] = None,
    http_payload_suffix: typing.Optional[builtins.str] = None,
    http_uri: typing.Optional[builtins.str] = None,
    newrelic_account_id: typing.Optional[builtins.str] = None,
    newrelic_license_key: typing.Optional[builtins.str] = None,
    newrelic_region: typing.Optional[builtins.str] = None,
    splunk_hecendpoint: typing.Optional[builtins.str] = None,
    splunk_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b875f9e1e5a69e90f3ccbd14774843fdcf1ec3dea2e285c4304b00a740ea8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c956f4d204b61d52c24ab82cf4bd3db61643a60ee25f267a37c5527c4672b14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb965ffa2d2b64591ae4dd554bdba65e764e37bccadc24e84259a13844eb5e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37227117d192d2ce343997d96903ae09393d02948abb68d20741f959866671e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b6ffc4fdcdfc68f19b0649b3264f8e211b7e469bd01556c00b2071a18f4583(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52584035adf1cf6ac49bc62a4ac84427a1190b4e2a7d5a650d7e74ae236d99e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d529d88d9bea14a52c73eea4cba00d3434d6e979128b8e2872b03118d73adf50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88bb8a5696b324b29776ea449f774539f34cfba17aa4799429b1a51844383af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c0b927ec43598325947959512a056b2b45e20a034aabd58fa66571f9065f8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d1c04f0203c3a9f08cfaf64b33eb749078f35c5b9cc82332488d49b6209dba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bf93f6ea32ddf32ca74534faaaf7627202436b7312f697895778a1d2d64871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9d0b3500812b9094d68925a982d1b6932bbf0ac677a39454abd2a24d756ec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7202d71685672f4243a816cb22d33cf1dd1493cfd58916b284cb0803524624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c941feef05017f89c98a0b09427aa74b6283593b5d5292736aa53150f7ddd89e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b10d967b3cd52ec26a2ddbf9b9e46251a0a94d0f78a549a37b55907f3ed810(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66e4614cc923e95dc7aa655441404d276aa10e12c028576245ef1e5e998ce0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd900b6cf459db8fed2063c75bbf028f168887d287d7181c71682c91f04e5e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae4e04d34a6bfb5251032a779984bf7a88b7a84c712eaa1642863538364f17e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdba2697ea3f78c179d2aa733616101eac581864ed3d8ef673f1687bcffedce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294120ebd8080fc24755438cfd5ca8aca3b996669f06c4469c452917e0aeeaf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27fd14b69df7479632091e254e69cbc8c157141295618a648f2110d973c7283e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e10d58dc7a1708597f664084fad3027458d1ba87b7981fedaf229e22fdd40c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad6d8831dfcdae3205286f608e7a2458e6dfc44b7d3ce71b603a3cd5b950db8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be3938192c1bfe850f25da53abc192fe5d1c7aadbbf1049d031fa66e07672c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66b53d581dcbe8ad9db5e4b7d512731a6a94a436f2e24180e10aca31d21bf6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a053588ad2844b98959edfef3e01d2d1e9515509c6f776522a4756f7fe6fd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7584064c3929586049d8fb7cba2238d2bfb9dab2c965ebaeeea3863eba36bf1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2d391a17055a27cde669c5b609a5fa628c2645bdd1b56018ee38cb2caa8d1c(
    value: typing.Optional[VaultClusterAuditLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a47be8c3817c70555bc777416f18db7e158d5f4a408d5a70bef49dc6666cf0(
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
    audit_log_config: typing.Optional[typing.Union[VaultClusterAuditLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VaultClusterIpAllowlistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    major_version_upgrade_config: typing.Optional[typing.Union[VaultClusterMajorVersionUpgradeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metrics_config: typing.Optional[typing.Union[VaultClusterMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    min_vault_version: typing.Optional[builtins.str] = None,
    paths_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    primary_link: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    proxy_endpoint: typing.Optional[builtins.str] = None,
    public_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VaultClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48c36a2424146eaec6d565f2569acb3069b65fe5f4a807e3e0afed1f25f2bca(
    *,
    address: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985eba6ed21e2a1c5d52f5d867ff7aac704220930d604d70d34dd6a72590bb43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f53ceb6f0c328586cbb8f6382586cc87f4c28ed3645bb5ec09d2f4f36629b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf49f37ffd1b565fd5b61994ee3b8c8ae03ab92510f1bd58a7d91793f3bf53b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c764d3e4a06026c3c41f9d125c3dea24fa70044256864acb196301c4bf511eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7dad15290a675b93a1195becc9883fa53829537f82288b9848c54e2bbfbc301(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30da3b098cb0125a3448fb843da715065ace2a1a01a368e92db5603ecaf6e098(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VaultClusterIpAllowlistStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73155db860af3e73b315bfc634d2bc75cdb042758445c3192058d8c66399bc45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e06fdb61915d991389e2e36db84284474dda42314791401110578535f717557(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb0ef2870e50cc24c4f6f030266222cb70499931f6975a6196e8c4e7b69546a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9c81efaa39e470521c8b644e32669a91ec4fb9c4a89f80691be1a8a6d59afc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultClusterIpAllowlistStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4962f49b844cabab740d8df01f3b70a715d3f1306b60fec54b6272426400d44(
    *,
    upgrade_type: builtins.str,
    maintenance_window_day: typing.Optional[builtins.str] = None,
    maintenance_window_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00220fe9e0d944a01da3073321aa1195a8785491ef20ede83c5c9e60456cfccc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731c8b0a131354c50c4187c419df1ca0b4ceae942541b703dccc29bddc2ae24d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f434d7fee16e563e0a028d6996e7baa865d83d6283058a983dd31e012a5ee7d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985cbace5e3cd0b9202218537c218691890d235d32455d4d255ad4bdb2d63fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73923462dd4285e4699c6c87591575ddc937cd2eac326dd6c048a6d19e1d13e1(
    value: typing.Optional[VaultClusterMajorVersionUpgradeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41328d9c30b2160db3534c4e47502c0f13855650febdfb88b239dcb6d6ee814(
    *,
    cloudwatch_access_key_id: typing.Optional[builtins.str] = None,
    cloudwatch_region: typing.Optional[builtins.str] = None,
    cloudwatch_secret_access_key: typing.Optional[builtins.str] = None,
    datadog_api_key: typing.Optional[builtins.str] = None,
    datadog_region: typing.Optional[builtins.str] = None,
    elasticsearch_endpoint: typing.Optional[builtins.str] = None,
    elasticsearch_password: typing.Optional[builtins.str] = None,
    elasticsearch_user: typing.Optional[builtins.str] = None,
    grafana_endpoint: typing.Optional[builtins.str] = None,
    grafana_password: typing.Optional[builtins.str] = None,
    grafana_user: typing.Optional[builtins.str] = None,
    http_basic_password: typing.Optional[builtins.str] = None,
    http_basic_user: typing.Optional[builtins.str] = None,
    http_bearer_token: typing.Optional[builtins.str] = None,
    http_codec: typing.Optional[builtins.str] = None,
    http_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    http_method: typing.Optional[builtins.str] = None,
    http_payload_prefix: typing.Optional[builtins.str] = None,
    http_payload_suffix: typing.Optional[builtins.str] = None,
    http_uri: typing.Optional[builtins.str] = None,
    newrelic_account_id: typing.Optional[builtins.str] = None,
    newrelic_license_key: typing.Optional[builtins.str] = None,
    newrelic_region: typing.Optional[builtins.str] = None,
    splunk_hecendpoint: typing.Optional[builtins.str] = None,
    splunk_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7573747a2312afa8ffc8dafc01025857a8dc813746d0e47c1ba6fbbe8778ac35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758bc1323488d37e5be24cb588eb05e9b1ea186ddf33106231f0942e6a250457(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ca2107c285ff7103e9d8cd7e2d0976cdb9f6a3feba8c720609ff9b9eb3ec6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68ac04c06206961e5cf9ba5882a68cb0bfbd85ecfdd142d184b698fe4a4f6f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01774f33baeaf10f919c131dc102f79f36eeff62b05d905990090cc7a031f8a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53493b753297becfad9e332d6d76bf38108bc351b6b3e20baddb9bb07893b458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e4cb56ff8310fc10c9c431d7e653a8a9253b3f4174b00ce6c2b7f625417bd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7451546117c82e865df91b13a3a9cd2f030683c0b55f26f22fd2331f19765c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ac0a029a6e68ca276d64fe802736b4e2cb729b3f3b720a0f2a817e6c5ba9e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae544b6a716e103200c258e30bdeecaffec6121c50d96449de5d9b48fbbc24c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1064d1abe056bb9b3eb383bd3d0f5cb018fb61bf6744005bc22fc06f26bca5cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc49e4808e51cb5e796669e09cca32630adbb4539a73b19a0900c53fcf47a3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd2272cc554376c4ee7460e1ece41acf6e82ab18159262787e46844c534e4de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68a7991850fa3b8895c725822d25de33cf88bc11e15ca05a15a6d9f72aca641(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d193928fb15de28a352119ab0730245621db1a2de614cab0a647f47da56aa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b08897bda522f649369a0f5822f7068f42a9a2f17f40c33da88d37c168835e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709586c778e6e98a06a5c98c19f9da11ca2ee2892df0096c9208c626f08c6b1d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e0be2fd685f7d14c400739a883e0233d60e056fa4929c6cbdbb9075836ef4f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67c4f59028e7f55cab0d141cc1c000d3c1c2944dc8535327858993f43755570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7947b144062ddc10d647cc3a19078eb0b8a24f34e18f4fe8c6c6af1addcbff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f5fe7bbf17e4a963687ca4ae201ce034a0d1b95d3d2d048378c7d938d738cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d6b376f5f719508a680e77ead2ef96ce3a9418ee4e63d88f543073ae53a2bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d46b16c4dae7a6c0dc38aafe4b0fb1ea9111a14e463f6531d8e9588ba40e6a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a2bb7dafe9c4af8a2847ca5d16dd8b6fdffff5d34d9a2cfb87341b004ea74e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f100b864dc5edf018fb3edd2e0d5c157421bdc6fc551acdd95f93b9ea0639d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3d1fedf5a113300f4ff7aff7390f5a7677acca337373f048c07ca807be7bd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41262da7c69a34522658c9a64fb97b513270eab90b33134705d21e460bf4bf7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2bf482f44b38423d4061abe71c12776c465cb81d41e5ec0fd2fd93519e289f(
    value: typing.Optional[VaultClusterMetricsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ee5e56e863fb68b056cf0c52c11694127fd2447b2109705c1c013124bc122b(
    *,
    create: typing.Optional[builtins.str] = None,
    default: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ecdf217b4bc03cba984541a801600b2d5439419fe5d42ba40ff7ac32ec3333(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2c8ee9a177a1817b11e58fd9878424e1054d355e3bcb7b746bbe30fa3cbc2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87e66bf7ba09872850753eb0320a0428faf4ccd45ba0b681c88af537cb66fbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b560841a2a171c6555944671bf203111462c74d3d57852b50f20076467171e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507fb6faf5cecc7fb6c63feaca0dae7ff5b1a3150654d705aecead89ab25793c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc0b876897d7750cc1f48d98ef8fac9b2418b3c42aad84f70d54d171bb85f4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
