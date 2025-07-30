r'''
# `hcp_vault_secrets_integration_gcp`

Refer to the Terraform Registry for docs: [`hcp_vault_secrets_integration_gcp`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp).
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


class VaultSecretsIntegrationGcp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationGcp.VaultSecretsIntegrationGcp",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp hcp_vault_secrets_integration_gcp}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        capabilities: typing.Sequence[builtins.str],
        name: builtins.str,
        federated_workload_identity: typing.Optional[typing.Union["VaultSecretsIntegrationGcpFederatedWorkloadIdentityA", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        service_account_key: typing.Optional[typing.Union["VaultSecretsIntegrationGcpServiceAccountKeyA", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp hcp_vault_secrets_integration_gcp} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capabilities: Capabilities enabled for the integration. See the Vault Secrets documentation for the list of supported capabilities per provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#capabilities VaultSecretsIntegrationGcp#capabilities}
        :param name: The Vault Secrets integration name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#name VaultSecretsIntegrationGcp#name}
        :param federated_workload_identity: (Recommended) Federated identity configuration to authenticate against the target GCP project. Cannot be used with ``service_account_key``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#federated_workload_identity VaultSecretsIntegrationGcp#federated_workload_identity}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#project_id VaultSecretsIntegrationGcp#project_id}
        :param service_account_key: GCP service account key used to authenticate against the target GCP project. Cannot be used with ``federated_workload_identity``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#service_account_key VaultSecretsIntegrationGcp#service_account_key}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c431009d41648fa5cb299b3248bc51e80f33ea6ea1f569b7570e4c4889fae0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = VaultSecretsIntegrationGcpConfig(
            capabilities=capabilities,
            name=name,
            federated_workload_identity=federated_workload_identity,
            project_id=project_id,
            service_account_key=service_account_key,
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
        '''Generates CDKTF code for importing a VaultSecretsIntegrationGcp resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VaultSecretsIntegrationGcp to import.
        :param import_from_id: The id of the existing VaultSecretsIntegrationGcp that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VaultSecretsIntegrationGcp to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60efccd8320430fc0d39b81428fbf6eedd4f26227cf1256a10bbd62d0e1043c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFederatedWorkloadIdentity")
    def put_federated_workload_identity(
        self,
        *,
        audience: builtins.str,
        service_account_email: builtins.str,
    ) -> None:
        '''
        :param audience: Audience configured on the GCP identity provider to federate access with HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#audience VaultSecretsIntegrationGcp#audience}
        :param service_account_email: GCP service account email that HVS will impersonate to carry operations for the appropriate capabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#service_account_email VaultSecretsIntegrationGcp#service_account_email}
        '''
        value = VaultSecretsIntegrationGcpFederatedWorkloadIdentityA(
            audience=audience, service_account_email=service_account_email
        )

        return typing.cast(None, jsii.invoke(self, "putFederatedWorkloadIdentity", [value]))

    @jsii.member(jsii_name="putServiceAccountKey")
    def put_service_account_key(self, *, credentials: builtins.str) -> None:
        '''
        :param credentials: JSON or base64 encoded service account key received from GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#credentials VaultSecretsIntegrationGcp#credentials}
        '''
        value = VaultSecretsIntegrationGcpServiceAccountKeyA(credentials=credentials)

        return typing.cast(None, jsii.invoke(self, "putServiceAccountKey", [value]))

    @jsii.member(jsii_name="resetFederatedWorkloadIdentity")
    def reset_federated_workload_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFederatedWorkloadIdentity", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetServiceAccountKey")
    def reset_service_account_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountKey", []))

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
    @jsii.member(jsii_name="federatedWorkloadIdentity")
    def federated_workload_identity(
        self,
    ) -> "VaultSecretsIntegrationGcpFederatedWorkloadIdentityAOutputReference":
        return typing.cast("VaultSecretsIntegrationGcpFederatedWorkloadIdentityAOutputReference", jsii.get(self, "federatedWorkloadIdentity"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="resourceName")
    def resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceName"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountKey")
    def service_account_key(
        self,
    ) -> "VaultSecretsIntegrationGcpServiceAccountKeyAOutputReference":
        return typing.cast("VaultSecretsIntegrationGcpServiceAccountKeyAOutputReference", jsii.get(self, "serviceAccountKey"))

    @builtins.property
    @jsii.member(jsii_name="capabilitiesInput")
    def capabilities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="federatedWorkloadIdentityInput")
    def federated_workload_identity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGcpFederatedWorkloadIdentityA"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGcpFederatedWorkloadIdentityA"]], jsii.get(self, "federatedWorkloadIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountKeyInput")
    def service_account_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGcpServiceAccountKeyA"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGcpServiceAccountKeyA"]], jsii.get(self, "serviceAccountKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "capabilities"))

    @capabilities.setter
    def capabilities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be59dfb41cf9ed3a39b8bd12e58b100393e82c173440e01bddb7ff8d183939ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capabilities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1433759be56b567b476ae5e2990dbc74874d66e4286bf169cc544794b21d1a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9768d9b85f840121964d125d5e81586ec6ac0775f62ba22b41b398252cd8a192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationGcp.VaultSecretsIntegrationGcpConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "capabilities": "capabilities",
        "name": "name",
        "federated_workload_identity": "federatedWorkloadIdentity",
        "project_id": "projectId",
        "service_account_key": "serviceAccountKey",
    },
)
class VaultSecretsIntegrationGcpConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capabilities: typing.Sequence[builtins.str],
        name: builtins.str,
        federated_workload_identity: typing.Optional[typing.Union["VaultSecretsIntegrationGcpFederatedWorkloadIdentityA", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        service_account_key: typing.Optional[typing.Union["VaultSecretsIntegrationGcpServiceAccountKeyA", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capabilities: Capabilities enabled for the integration. See the Vault Secrets documentation for the list of supported capabilities per provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#capabilities VaultSecretsIntegrationGcp#capabilities}
        :param name: The Vault Secrets integration name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#name VaultSecretsIntegrationGcp#name}
        :param federated_workload_identity: (Recommended) Federated identity configuration to authenticate against the target GCP project. Cannot be used with ``service_account_key``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#federated_workload_identity VaultSecretsIntegrationGcp#federated_workload_identity}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#project_id VaultSecretsIntegrationGcp#project_id}
        :param service_account_key: GCP service account key used to authenticate against the target GCP project. Cannot be used with ``federated_workload_identity``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#service_account_key VaultSecretsIntegrationGcp#service_account_key}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(federated_workload_identity, dict):
            federated_workload_identity = VaultSecretsIntegrationGcpFederatedWorkloadIdentityA(**federated_workload_identity)
        if isinstance(service_account_key, dict):
            service_account_key = VaultSecretsIntegrationGcpServiceAccountKeyA(**service_account_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e157b236dcba805e2e4a395b3bef0e2c04af8d07ce8d9437287996789676ba)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument federated_workload_identity", value=federated_workload_identity, expected_type=type_hints["federated_workload_identity"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument service_account_key", value=service_account_key, expected_type=type_hints["service_account_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capabilities": capabilities,
            "name": name,
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
        if federated_workload_identity is not None:
            self._values["federated_workload_identity"] = federated_workload_identity
        if project_id is not None:
            self._values["project_id"] = project_id
        if service_account_key is not None:
            self._values["service_account_key"] = service_account_key

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
    def capabilities(self) -> typing.List[builtins.str]:
        '''Capabilities enabled for the integration. See the Vault Secrets documentation for the list of supported capabilities per provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#capabilities VaultSecretsIntegrationGcp#capabilities}
        '''
        result = self._values.get("capabilities")
        assert result is not None, "Required property 'capabilities' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The Vault Secrets integration name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#name VaultSecretsIntegrationGcp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def federated_workload_identity(
        self,
    ) -> typing.Optional["VaultSecretsIntegrationGcpFederatedWorkloadIdentityA"]:
        '''(Recommended) Federated identity configuration to authenticate against the target GCP project. Cannot be used with ``service_account_key``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#federated_workload_identity VaultSecretsIntegrationGcp#federated_workload_identity}
        '''
        result = self._values.get("federated_workload_identity")
        return typing.cast(typing.Optional["VaultSecretsIntegrationGcpFederatedWorkloadIdentityA"], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#project_id VaultSecretsIntegrationGcp#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_key(
        self,
    ) -> typing.Optional["VaultSecretsIntegrationGcpServiceAccountKeyA"]:
        '''GCP service account key used to authenticate against the target GCP project. Cannot be used with ``federated_workload_identity``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#service_account_key VaultSecretsIntegrationGcp#service_account_key}
        '''
        result = self._values.get("service_account_key")
        return typing.cast(typing.Optional["VaultSecretsIntegrationGcpServiceAccountKeyA"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationGcpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationGcp.VaultSecretsIntegrationGcpFederatedWorkloadIdentityA",
    jsii_struct_bases=[],
    name_mapping={
        "audience": "audience",
        "service_account_email": "serviceAccountEmail",
    },
)
class VaultSecretsIntegrationGcpFederatedWorkloadIdentityA:
    def __init__(
        self,
        *,
        audience: builtins.str,
        service_account_email: builtins.str,
    ) -> None:
        '''
        :param audience: Audience configured on the GCP identity provider to federate access with HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#audience VaultSecretsIntegrationGcp#audience}
        :param service_account_email: GCP service account email that HVS will impersonate to carry operations for the appropriate capabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#service_account_email VaultSecretsIntegrationGcp#service_account_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c573e203ef85c64c18cc3b9f9f24befb3771f4505196dcfa869ebb7680d5ff)
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audience": audience,
            "service_account_email": service_account_email,
        }

    @builtins.property
    def audience(self) -> builtins.str:
        '''Audience configured on the GCP identity provider to federate access with HCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#audience VaultSecretsIntegrationGcp#audience}
        '''
        result = self._values.get("audience")
        assert result is not None, "Required property 'audience' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''GCP service account email that HVS will impersonate to carry operations for the appropriate capabilities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#service_account_email VaultSecretsIntegrationGcp#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationGcpFederatedWorkloadIdentityA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationGcpFederatedWorkloadIdentityAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationGcp.VaultSecretsIntegrationGcpFederatedWorkloadIdentityAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da139b53a28457dd8b1644df36b5a862b49a074583278acb91b9344d8243dbe0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ece364a6aea1b7e1feca96a20bfbdac61dac2700f11abdd50ae9df929ebfa13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4eea7769f61eb44a29cfd8b58fc7e8a695fb0e64aa4567e7b1ce6896d08fdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpFederatedWorkloadIdentityA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpFederatedWorkloadIdentityA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpFederatedWorkloadIdentityA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d54421d9a17230287efa622716ec0ef3c01265c2628740adb35399fc77c962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationGcp.VaultSecretsIntegrationGcpServiceAccountKeyA",
    jsii_struct_bases=[],
    name_mapping={"credentials": "credentials"},
)
class VaultSecretsIntegrationGcpServiceAccountKeyA:
    def __init__(self, *, credentials: builtins.str) -> None:
        '''
        :param credentials: JSON or base64 encoded service account key received from GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#credentials VaultSecretsIntegrationGcp#credentials}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382bb53d430651d7facda770a5381e690003ac5a9e7805332d9e21d370425dba)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
        }

    @builtins.property
    def credentials(self) -> builtins.str:
        '''JSON or base64 encoded service account key received from GCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_gcp#credentials VaultSecretsIntegrationGcp#credentials}
        '''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationGcpServiceAccountKeyA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationGcpServiceAccountKeyAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationGcp.VaultSecretsIntegrationGcpServiceAccountKeyAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__684590aaf821022ae4eab2abcd88dcb3f9184d2e564d269f4553407e965abf75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientEmail")
    def client_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientEmail"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838d0a0c04ee000764a7e46c53247201e4cb2fdd1cc47cae0871e81b0c920790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpServiceAccountKeyA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpServiceAccountKeyA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpServiceAccountKeyA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a461beb9acc28690739288af26954dcdec777c329501f2b1019df9a29b52af75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VaultSecretsIntegrationGcp",
    "VaultSecretsIntegrationGcpConfig",
    "VaultSecretsIntegrationGcpFederatedWorkloadIdentityA",
    "VaultSecretsIntegrationGcpFederatedWorkloadIdentityAOutputReference",
    "VaultSecretsIntegrationGcpServiceAccountKeyA",
    "VaultSecretsIntegrationGcpServiceAccountKeyAOutputReference",
]

publication.publish()

def _typecheckingstub__a9c431009d41648fa5cb299b3248bc51e80f33ea6ea1f569b7570e4c4889fae0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    capabilities: typing.Sequence[builtins.str],
    name: builtins.str,
    federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationGcpFederatedWorkloadIdentityA, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    service_account_key: typing.Optional[typing.Union[VaultSecretsIntegrationGcpServiceAccountKeyA, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__60efccd8320430fc0d39b81428fbf6eedd4f26227cf1256a10bbd62d0e1043c0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be59dfb41cf9ed3a39b8bd12e58b100393e82c173440e01bddb7ff8d183939ec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1433759be56b567b476ae5e2990dbc74874d66e4286bf169cc544794b21d1a51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9768d9b85f840121964d125d5e81586ec6ac0775f62ba22b41b398252cd8a192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e157b236dcba805e2e4a395b3bef0e2c04af8d07ce8d9437287996789676ba(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capabilities: typing.Sequence[builtins.str],
    name: builtins.str,
    federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationGcpFederatedWorkloadIdentityA, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    service_account_key: typing.Optional[typing.Union[VaultSecretsIntegrationGcpServiceAccountKeyA, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c573e203ef85c64c18cc3b9f9f24befb3771f4505196dcfa869ebb7680d5ff(
    *,
    audience: builtins.str,
    service_account_email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da139b53a28457dd8b1644df36b5a862b49a074583278acb91b9344d8243dbe0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ece364a6aea1b7e1feca96a20bfbdac61dac2700f11abdd50ae9df929ebfa13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4eea7769f61eb44a29cfd8b58fc7e8a695fb0e64aa4567e7b1ce6896d08fdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d54421d9a17230287efa622716ec0ef3c01265c2628740adb35399fc77c962(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpFederatedWorkloadIdentityA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382bb53d430651d7facda770a5381e690003ac5a9e7805332d9e21d370425dba(
    *,
    credentials: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684590aaf821022ae4eab2abcd88dcb3f9184d2e564d269f4553407e965abf75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838d0a0c04ee000764a7e46c53247201e4cb2fdd1cc47cae0871e81b0c920790(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a461beb9acc28690739288af26954dcdec777c329501f2b1019df9a29b52af75(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpServiceAccountKeyA]],
) -> None:
    """Type checking stubs"""
    pass
