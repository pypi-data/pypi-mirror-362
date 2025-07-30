r'''
# `hcp_vault_secrets_integration`

Refer to the Terraform Registry for docs: [`hcp_vault_secrets_integration`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration).
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


class VaultSecretsIntegration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration hcp_vault_secrets_integration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        capabilities: typing.Sequence[builtins.str],
        name: builtins.str,
        provider_type: builtins.str,
        aws_access_keys: typing.Optional[typing.Union["VaultSecretsIntegrationAwsAccessKeys", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_federated_workload_identity: typing.Optional[typing.Union["VaultSecretsIntegrationAwsFederatedWorkloadIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_client_secret: typing.Optional[typing.Union["VaultSecretsIntegrationAzureClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_federated_workload_identity: typing.Optional[typing.Union["VaultSecretsIntegrationAzureFederatedWorkloadIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        confluent_static_credentials: typing.Optional[typing.Union["VaultSecretsIntegrationConfluentStaticCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        gcp_federated_workload_identity: typing.Optional[typing.Union["VaultSecretsIntegrationGcpFederatedWorkloadIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        gcp_service_account_key: typing.Optional[typing.Union["VaultSecretsIntegrationGcpServiceAccountKey", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_access: typing.Optional[typing.Union["VaultSecretsIntegrationGitlabAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        mongodb_atlas_static_credentials: typing.Optional[typing.Union["VaultSecretsIntegrationMongodbAtlasStaticCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        twilio_static_credentials: typing.Optional[typing.Union["VaultSecretsIntegrationTwilioStaticCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration hcp_vault_secrets_integration} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capabilities: Capabilities enabled for the integration. See the Vault Secrets documentation for the list of supported capabilities per provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#capabilities VaultSecretsIntegration#capabilities}
        :param name: The Vault Secrets integration name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#name VaultSecretsIntegration#name}
        :param provider_type: The provider or 3rd party platform the integration is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#provider_type VaultSecretsIntegration#provider_type}
        :param aws_access_keys: AWS IAM key pair used to authenticate against the target AWS account. Cannot be used with ``federated_workload_identity``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#aws_access_keys VaultSecretsIntegration#aws_access_keys}
        :param aws_federated_workload_identity: (Recommended) Federated identity configuration to authenticate against the target AWS account. Cannot be used with ``access_keys``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#aws_federated_workload_identity VaultSecretsIntegration#aws_federated_workload_identity}
        :param azure_client_secret: Azure client secret used to authenticate against the target Azure application. Cannot be used with ``federated_workload_identity``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#azure_client_secret VaultSecretsIntegration#azure_client_secret}
        :param azure_federated_workload_identity: (Recommended) Federated identity configuration to authenticate against the target Azure application. Cannot be used with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#azure_federated_workload_identity VaultSecretsIntegration#azure_federated_workload_identity}
        :param confluent_static_credentials: Confluent API key used to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#confluent_static_credentials VaultSecretsIntegration#confluent_static_credentials}
        :param gcp_federated_workload_identity: (Recommended) Federated identity configuration to authenticate against the target GCP project. Cannot be used with ``service_account_key``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#gcp_federated_workload_identity VaultSecretsIntegration#gcp_federated_workload_identity}
        :param gcp_service_account_key: GCP service account key used to authenticate against the target GCP project. Cannot be used with ``federated_workload_identity``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#gcp_service_account_key VaultSecretsIntegration#gcp_service_account_key}
        :param gitlab_access: GitLab access token used to authenticate against the target GitLab account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#gitlab_access VaultSecretsIntegration#gitlab_access}
        :param mongodb_atlas_static_credentials: MongoDB Atlas API key used to authenticate against the target project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#mongodb_atlas_static_credentials VaultSecretsIntegration#mongodb_atlas_static_credentials}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#project_id VaultSecretsIntegration#project_id}
        :param twilio_static_credentials: Twilio API key parts used to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#twilio_static_credentials VaultSecretsIntegration#twilio_static_credentials}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2562d56f521106b9e798eb60978ee1985ca00fa5e41574b4da5b8873d58a168)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = VaultSecretsIntegrationConfig(
            capabilities=capabilities,
            name=name,
            provider_type=provider_type,
            aws_access_keys=aws_access_keys,
            aws_federated_workload_identity=aws_federated_workload_identity,
            azure_client_secret=azure_client_secret,
            azure_federated_workload_identity=azure_federated_workload_identity,
            confluent_static_credentials=confluent_static_credentials,
            gcp_federated_workload_identity=gcp_federated_workload_identity,
            gcp_service_account_key=gcp_service_account_key,
            gitlab_access=gitlab_access,
            mongodb_atlas_static_credentials=mongodb_atlas_static_credentials,
            project_id=project_id,
            twilio_static_credentials=twilio_static_credentials,
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
        '''Generates CDKTF code for importing a VaultSecretsIntegration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VaultSecretsIntegration to import.
        :param import_from_id: The id of the existing VaultSecretsIntegration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VaultSecretsIntegration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df9acaf9183d622e8ee43d1d4155fb4f7f585583dc420bfe5eef67c77d1949c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAwsAccessKeys")
    def put_aws_access_keys(
        self,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
    ) -> None:
        '''
        :param access_key_id: Key ID used with the secret key to authenticate against the target AWS account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#access_key_id VaultSecretsIntegration#access_key_id}
        :param secret_access_key: Secret key used with the key ID to authenticate against the target AWS account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#secret_access_key VaultSecretsIntegration#secret_access_key}
        '''
        value = VaultSecretsIntegrationAwsAccessKeys(
            access_key_id=access_key_id, secret_access_key=secret_access_key
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAccessKeys", [value]))

    @jsii.member(jsii_name="putAwsFederatedWorkloadIdentity")
    def put_aws_federated_workload_identity(
        self,
        *,
        audience: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param audience: Audience configured on the AWS IAM identity provider to federate access with HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#audience VaultSecretsIntegration#audience}
        :param role_arn: AWS IAM role ARN the integration will assume to carry operations for the appropriate capabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#role_arn VaultSecretsIntegration#role_arn}
        '''
        value = VaultSecretsIntegrationAwsFederatedWorkloadIdentity(
            audience=audience, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putAwsFederatedWorkloadIdentity", [value]))

    @jsii.member(jsii_name="putAzureClientSecret")
    def put_azure_client_secret(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param client_id: Azure client ID corresponding to the Azure application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#client_id VaultSecretsIntegration#client_id}
        :param client_secret: Secret value corresponding to the Azure client secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#client_secret VaultSecretsIntegration#client_secret}
        :param tenant_id: Azure tenant ID corresponding to the Azure application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#tenant_id VaultSecretsIntegration#tenant_id}
        '''
        value = VaultSecretsIntegrationAzureClientSecret(
            client_id=client_id, client_secret=client_secret, tenant_id=tenant_id
        )

        return typing.cast(None, jsii.invoke(self, "putAzureClientSecret", [value]))

    @jsii.member(jsii_name="putAzureFederatedWorkloadIdentity")
    def put_azure_federated_workload_identity(
        self,
        *,
        audience: builtins.str,
        client_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param audience: Audience configured on the Azure federated identity credentials to federate access with HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#audience VaultSecretsIntegration#audience}
        :param client_id: Azure client ID corresponding to the Azure application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#client_id VaultSecretsIntegration#client_id}
        :param tenant_id: Azure tenant ID corresponding to the Azure application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#tenant_id VaultSecretsIntegration#tenant_id}
        '''
        value = VaultSecretsIntegrationAzureFederatedWorkloadIdentity(
            audience=audience, client_id=client_id, tenant_id=tenant_id
        )

        return typing.cast(None, jsii.invoke(self, "putAzureFederatedWorkloadIdentity", [value]))

    @jsii.member(jsii_name="putConfluentStaticCredentials")
    def put_confluent_static_credentials(
        self,
        *,
        cloud_api_key_id: builtins.str,
        cloud_api_secret: builtins.str,
    ) -> None:
        '''
        :param cloud_api_key_id: Public key used alongside the private key to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#cloud_api_key_id VaultSecretsIntegration#cloud_api_key_id}
        :param cloud_api_secret: Private key used alongside the public key to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#cloud_api_secret VaultSecretsIntegration#cloud_api_secret}
        '''
        value = VaultSecretsIntegrationConfluentStaticCredentials(
            cloud_api_key_id=cloud_api_key_id, cloud_api_secret=cloud_api_secret
        )

        return typing.cast(None, jsii.invoke(self, "putConfluentStaticCredentials", [value]))

    @jsii.member(jsii_name="putGcpFederatedWorkloadIdentity")
    def put_gcp_federated_workload_identity(
        self,
        *,
        audience: builtins.str,
        service_account_email: builtins.str,
    ) -> None:
        '''
        :param audience: Audience configured on the GCP identity provider to federate access with HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#audience VaultSecretsIntegration#audience}
        :param service_account_email: GCP service account email that HVS will impersonate to carry operations for the appropriate capabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#service_account_email VaultSecretsIntegration#service_account_email}
        '''
        value = VaultSecretsIntegrationGcpFederatedWorkloadIdentity(
            audience=audience, service_account_email=service_account_email
        )

        return typing.cast(None, jsii.invoke(self, "putGcpFederatedWorkloadIdentity", [value]))

    @jsii.member(jsii_name="putGcpServiceAccountKey")
    def put_gcp_service_account_key(self, *, credentials: builtins.str) -> None:
        '''
        :param credentials: JSON or base64 encoded service account key received from GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#credentials VaultSecretsIntegration#credentials}
        '''
        value = VaultSecretsIntegrationGcpServiceAccountKey(credentials=credentials)

        return typing.cast(None, jsii.invoke(self, "putGcpServiceAccountKey", [value]))

    @jsii.member(jsii_name="putGitlabAccess")
    def put_gitlab_access(self, *, token: builtins.str) -> None:
        '''
        :param token: Access token used to authenticate against the target GitLab account. This token must have privilege to create CI/CD variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#token VaultSecretsIntegration#token}
        '''
        value = VaultSecretsIntegrationGitlabAccess(token=token)

        return typing.cast(None, jsii.invoke(self, "putGitlabAccess", [value]))

    @jsii.member(jsii_name="putMongodbAtlasStaticCredentials")
    def put_mongodb_atlas_static_credentials(
        self,
        *,
        api_private_key: builtins.str,
        api_public_key: builtins.str,
    ) -> None:
        '''
        :param api_private_key: Private key used alongside the public key to authenticate against the target project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_private_key VaultSecretsIntegration#api_private_key}
        :param api_public_key: Public key used alongside the private key to authenticate against the target project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_public_key VaultSecretsIntegration#api_public_key}
        '''
        value = VaultSecretsIntegrationMongodbAtlasStaticCredentials(
            api_private_key=api_private_key, api_public_key=api_public_key
        )

        return typing.cast(None, jsii.invoke(self, "putMongodbAtlasStaticCredentials", [value]))

    @jsii.member(jsii_name="putTwilioStaticCredentials")
    def put_twilio_static_credentials(
        self,
        *,
        account_sid: builtins.str,
        api_key_secret: builtins.str,
        api_key_sid: builtins.str,
    ) -> None:
        '''
        :param account_sid: Account SID for the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#account_sid VaultSecretsIntegration#account_sid}
        :param api_key_secret: Api key secret used with the api key SID to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_key_secret VaultSecretsIntegration#api_key_secret}
        :param api_key_sid: Api key SID to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_key_sid VaultSecretsIntegration#api_key_sid}
        '''
        value = VaultSecretsIntegrationTwilioStaticCredentials(
            account_sid=account_sid,
            api_key_secret=api_key_secret,
            api_key_sid=api_key_sid,
        )

        return typing.cast(None, jsii.invoke(self, "putTwilioStaticCredentials", [value]))

    @jsii.member(jsii_name="resetAwsAccessKeys")
    def reset_aws_access_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccessKeys", []))

    @jsii.member(jsii_name="resetAwsFederatedWorkloadIdentity")
    def reset_aws_federated_workload_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsFederatedWorkloadIdentity", []))

    @jsii.member(jsii_name="resetAzureClientSecret")
    def reset_azure_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureClientSecret", []))

    @jsii.member(jsii_name="resetAzureFederatedWorkloadIdentity")
    def reset_azure_federated_workload_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureFederatedWorkloadIdentity", []))

    @jsii.member(jsii_name="resetConfluentStaticCredentials")
    def reset_confluent_static_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfluentStaticCredentials", []))

    @jsii.member(jsii_name="resetGcpFederatedWorkloadIdentity")
    def reset_gcp_federated_workload_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpFederatedWorkloadIdentity", []))

    @jsii.member(jsii_name="resetGcpServiceAccountKey")
    def reset_gcp_service_account_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountKey", []))

    @jsii.member(jsii_name="resetGitlabAccess")
    def reset_gitlab_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitlabAccess", []))

    @jsii.member(jsii_name="resetMongodbAtlasStaticCredentials")
    def reset_mongodb_atlas_static_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMongodbAtlasStaticCredentials", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetTwilioStaticCredentials")
    def reset_twilio_static_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwilioStaticCredentials", []))

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
    @jsii.member(jsii_name="awsAccessKeys")
    def aws_access_keys(self) -> "VaultSecretsIntegrationAwsAccessKeysOutputReference":
        return typing.cast("VaultSecretsIntegrationAwsAccessKeysOutputReference", jsii.get(self, "awsAccessKeys"))

    @builtins.property
    @jsii.member(jsii_name="awsFederatedWorkloadIdentity")
    def aws_federated_workload_identity(
        self,
    ) -> "VaultSecretsIntegrationAwsFederatedWorkloadIdentityOutputReference":
        return typing.cast("VaultSecretsIntegrationAwsFederatedWorkloadIdentityOutputReference", jsii.get(self, "awsFederatedWorkloadIdentity"))

    @builtins.property
    @jsii.member(jsii_name="azureClientSecret")
    def azure_client_secret(
        self,
    ) -> "VaultSecretsIntegrationAzureClientSecretOutputReference":
        return typing.cast("VaultSecretsIntegrationAzureClientSecretOutputReference", jsii.get(self, "azureClientSecret"))

    @builtins.property
    @jsii.member(jsii_name="azureFederatedWorkloadIdentity")
    def azure_federated_workload_identity(
        self,
    ) -> "VaultSecretsIntegrationAzureFederatedWorkloadIdentityOutputReference":
        return typing.cast("VaultSecretsIntegrationAzureFederatedWorkloadIdentityOutputReference", jsii.get(self, "azureFederatedWorkloadIdentity"))

    @builtins.property
    @jsii.member(jsii_name="confluentStaticCredentials")
    def confluent_static_credentials(
        self,
    ) -> "VaultSecretsIntegrationConfluentStaticCredentialsOutputReference":
        return typing.cast("VaultSecretsIntegrationConfluentStaticCredentialsOutputReference", jsii.get(self, "confluentStaticCredentials"))

    @builtins.property
    @jsii.member(jsii_name="gcpFederatedWorkloadIdentity")
    def gcp_federated_workload_identity(
        self,
    ) -> "VaultSecretsIntegrationGcpFederatedWorkloadIdentityOutputReference":
        return typing.cast("VaultSecretsIntegrationGcpFederatedWorkloadIdentityOutputReference", jsii.get(self, "gcpFederatedWorkloadIdentity"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountKey")
    def gcp_service_account_key(
        self,
    ) -> "VaultSecretsIntegrationGcpServiceAccountKeyOutputReference":
        return typing.cast("VaultSecretsIntegrationGcpServiceAccountKeyOutputReference", jsii.get(self, "gcpServiceAccountKey"))

    @builtins.property
    @jsii.member(jsii_name="gitlabAccess")
    def gitlab_access(self) -> "VaultSecretsIntegrationGitlabAccessOutputReference":
        return typing.cast("VaultSecretsIntegrationGitlabAccessOutputReference", jsii.get(self, "gitlabAccess"))

    @builtins.property
    @jsii.member(jsii_name="mongodbAtlasStaticCredentials")
    def mongodb_atlas_static_credentials(
        self,
    ) -> "VaultSecretsIntegrationMongodbAtlasStaticCredentialsOutputReference":
        return typing.cast("VaultSecretsIntegrationMongodbAtlasStaticCredentialsOutputReference", jsii.get(self, "mongodbAtlasStaticCredentials"))

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
    @jsii.member(jsii_name="twilioStaticCredentials")
    def twilio_static_credentials(
        self,
    ) -> "VaultSecretsIntegrationTwilioStaticCredentialsOutputReference":
        return typing.cast("VaultSecretsIntegrationTwilioStaticCredentialsOutputReference", jsii.get(self, "twilioStaticCredentials"))

    @builtins.property
    @jsii.member(jsii_name="awsAccessKeysInput")
    def aws_access_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationAwsAccessKeys"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationAwsAccessKeys"]], jsii.get(self, "awsAccessKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="awsFederatedWorkloadIdentityInput")
    def aws_federated_workload_identity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationAwsFederatedWorkloadIdentity"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationAwsFederatedWorkloadIdentity"]], jsii.get(self, "awsFederatedWorkloadIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="azureClientSecretInput")
    def azure_client_secret_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationAzureClientSecret"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationAzureClientSecret"]], jsii.get(self, "azureClientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="azureFederatedWorkloadIdentityInput")
    def azure_federated_workload_identity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationAzureFederatedWorkloadIdentity"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationAzureFederatedWorkloadIdentity"]], jsii.get(self, "azureFederatedWorkloadIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="capabilitiesInput")
    def capabilities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="confluentStaticCredentialsInput")
    def confluent_static_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationConfluentStaticCredentials"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationConfluentStaticCredentials"]], jsii.get(self, "confluentStaticCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpFederatedWorkloadIdentityInput")
    def gcp_federated_workload_identity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGcpFederatedWorkloadIdentity"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGcpFederatedWorkloadIdentity"]], jsii.get(self, "gcpFederatedWorkloadIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountKeyInput")
    def gcp_service_account_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGcpServiceAccountKey"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGcpServiceAccountKey"]], jsii.get(self, "gcpServiceAccountKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="gitlabAccessInput")
    def gitlab_access_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGitlabAccess"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationGitlabAccess"]], jsii.get(self, "gitlabAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="mongodbAtlasStaticCredentialsInput")
    def mongodb_atlas_static_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationMongodbAtlasStaticCredentials"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationMongodbAtlasStaticCredentials"]], jsii.get(self, "mongodbAtlasStaticCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="providerTypeInput")
    def provider_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="twilioStaticCredentialsInput")
    def twilio_static_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationTwilioStaticCredentials"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationTwilioStaticCredentials"]], jsii.get(self, "twilioStaticCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "capabilities"))

    @capabilities.setter
    def capabilities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722651326bf62d63e85483dbe38b3310717702493486c00e27eab1d44d645c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capabilities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da77f3411b182ac7bd46adf9d909aba0858aae2a4d4b677acc824ecfb2de3689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d3c75d93198fed50c17bafa930f5535d2e9b3ab3fbc041daddeb2eccaa6b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerType")
    def provider_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerType"))

    @provider_type.setter
    def provider_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9475c18bbef9789b7167f9005bb2a2026d4ec7de7ed209a48b72826e6e88357f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationAwsAccessKeys",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "secret_access_key": "secretAccessKey",
    },
)
class VaultSecretsIntegrationAwsAccessKeys:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
    ) -> None:
        '''
        :param access_key_id: Key ID used with the secret key to authenticate against the target AWS account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#access_key_id VaultSecretsIntegration#access_key_id}
        :param secret_access_key: Secret key used with the key ID to authenticate against the target AWS account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#secret_access_key VaultSecretsIntegration#secret_access_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b9db9d07130834d3f2db6bba649170373a5425586f7f5295afe72adef570f8)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
        }

    @builtins.property
    def access_key_id(self) -> builtins.str:
        '''Key ID used with the secret key to authenticate against the target AWS account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#access_key_id VaultSecretsIntegration#access_key_id}
        '''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key(self) -> builtins.str:
        '''Secret key used with the key ID to authenticate against the target AWS account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#secret_access_key VaultSecretsIntegration#secret_access_key}
        '''
        result = self._values.get("secret_access_key")
        assert result is not None, "Required property 'secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationAwsAccessKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationAwsAccessKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationAwsAccessKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0647d815335539cc16a4a58261329ea0b5cb1220af33db7c88cadcc43744ea0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accessKeyIdInput")
    def access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyInput")
    def secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770656e077f1175fa4f190ced950df09d0f9d3e70500d7f6e403d117a8992045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a09ee83b71910d22d3267fa5224631ead18d43f3cedb35b5e885038fef0a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAwsAccessKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAwsAccessKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAwsAccessKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572b65a018c6ba833d8159a688f49bddb55e3afb073732f176240db69702d908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationAwsFederatedWorkloadIdentity",
    jsii_struct_bases=[],
    name_mapping={"audience": "audience", "role_arn": "roleArn"},
)
class VaultSecretsIntegrationAwsFederatedWorkloadIdentity:
    def __init__(self, *, audience: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param audience: Audience configured on the AWS IAM identity provider to federate access with HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#audience VaultSecretsIntegration#audience}
        :param role_arn: AWS IAM role ARN the integration will assume to carry operations for the appropriate capabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#role_arn VaultSecretsIntegration#role_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080663c8e8bb0cf6a4e9ceb924142363f0b39092159fddff16ed50330992fd72)
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audience": audience,
            "role_arn": role_arn,
        }

    @builtins.property
    def audience(self) -> builtins.str:
        '''Audience configured on the AWS IAM identity provider to federate access with HCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#audience VaultSecretsIntegration#audience}
        '''
        result = self._values.get("audience")
        assert result is not None, "Required property 'audience' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''AWS IAM role ARN the integration will assume to carry operations for the appropriate capabilities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#role_arn VaultSecretsIntegration#role_arn}
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationAwsFederatedWorkloadIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationAwsFederatedWorkloadIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationAwsFederatedWorkloadIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__879cdfa1ef86841f3a77098dcc3a79b3f6865ce5b385eea4fc9689781028756a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8378faa6cac2bdaa044a6f9551307e3331495981561db38e1cd477d67c74439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4056798cd3a6b059100ec36bd41a91ab39197452fce94026575a1680dc5a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAwsFederatedWorkloadIdentity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAwsFederatedWorkloadIdentity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAwsFederatedWorkloadIdentity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc8a9083fbf2f66e8b45e527e50fac481fd949f43b177e795d9212823ab7f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationAzureClientSecret",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "tenant_id": "tenantId",
    },
)
class VaultSecretsIntegrationAzureClientSecret:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param client_id: Azure client ID corresponding to the Azure application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#client_id VaultSecretsIntegration#client_id}
        :param client_secret: Secret value corresponding to the Azure client secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#client_secret VaultSecretsIntegration#client_secret}
        :param tenant_id: Azure tenant ID corresponding to the Azure application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#tenant_id VaultSecretsIntegration#tenant_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bee425770f92e9a6b1285c5acec21b3f1f7121de278326014a2b9fcac81f516)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "tenant_id": tenant_id,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Azure client ID corresponding to the Azure application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#client_id VaultSecretsIntegration#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Secret value corresponding to the Azure client secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#client_secret VaultSecretsIntegration#client_secret}
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''Azure tenant ID corresponding to the Azure application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#tenant_id VaultSecretsIntegration#tenant_id}
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationAzureClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationAzureClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationAzureClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fac43137b5814634fecaacb07256b59f5a9fb88a5351514fd43a2f14709ad65a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668c7eed2d3ea453def081a82ed65894463a962deeedf5d8ff8d1de8382dcd98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24319efc4c9cfb5b6fa4c8b87ff38be85495f3550972271b5ee18e3d1ccf9ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9221795e828c61c73e9d3fc9a5d59971978e78b95850cff9058580400e0757be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAzureClientSecret]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAzureClientSecret]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAzureClientSecret]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54139cc11b7cd9af6345322b2438f45a48827ef004c6ca4e9a34fd8bd757af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationAzureFederatedWorkloadIdentity",
    jsii_struct_bases=[],
    name_mapping={
        "audience": "audience",
        "client_id": "clientId",
        "tenant_id": "tenantId",
    },
)
class VaultSecretsIntegrationAzureFederatedWorkloadIdentity:
    def __init__(
        self,
        *,
        audience: builtins.str,
        client_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param audience: Audience configured on the Azure federated identity credentials to federate access with HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#audience VaultSecretsIntegration#audience}
        :param client_id: Azure client ID corresponding to the Azure application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#client_id VaultSecretsIntegration#client_id}
        :param tenant_id: Azure tenant ID corresponding to the Azure application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#tenant_id VaultSecretsIntegration#tenant_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b166c23d1ded8139f9456d26340fd37c032f128ee86120a87b9ef8f0dc8b981a)
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audience": audience,
            "client_id": client_id,
            "tenant_id": tenant_id,
        }

    @builtins.property
    def audience(self) -> builtins.str:
        '''Audience configured on the Azure federated identity credentials to federate access with HCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#audience VaultSecretsIntegration#audience}
        '''
        result = self._values.get("audience")
        assert result is not None, "Required property 'audience' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Azure client ID corresponding to the Azure application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#client_id VaultSecretsIntegration#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''Azure tenant ID corresponding to the Azure application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#tenant_id VaultSecretsIntegration#tenant_id}
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationAzureFederatedWorkloadIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationAzureFederatedWorkloadIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationAzureFederatedWorkloadIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3a570fa3cd00a7af4f4f0c23cc731efe889a78b20c095edafe3b68845ea4ff9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270a9b6535c7e38c7c617abdc0815d9422296de94ad7aee1cbc0eb4ea2118eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d6c58f15cca9644ed8b47c245e129504e28c748aa71cbe75467f98d725f121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d8b3af5c6c3fbf640f922367d4299ece8a42d3d79b6828ca962489646106a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAzureFederatedWorkloadIdentity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAzureFederatedWorkloadIdentity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAzureFederatedWorkloadIdentity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3911b4ed49939fe240e8521f12e143e4cc509cad64685339692602142d9c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationConfig",
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
        "provider_type": "providerType",
        "aws_access_keys": "awsAccessKeys",
        "aws_federated_workload_identity": "awsFederatedWorkloadIdentity",
        "azure_client_secret": "azureClientSecret",
        "azure_federated_workload_identity": "azureFederatedWorkloadIdentity",
        "confluent_static_credentials": "confluentStaticCredentials",
        "gcp_federated_workload_identity": "gcpFederatedWorkloadIdentity",
        "gcp_service_account_key": "gcpServiceAccountKey",
        "gitlab_access": "gitlabAccess",
        "mongodb_atlas_static_credentials": "mongodbAtlasStaticCredentials",
        "project_id": "projectId",
        "twilio_static_credentials": "twilioStaticCredentials",
    },
)
class VaultSecretsIntegrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        provider_type: builtins.str,
        aws_access_keys: typing.Optional[typing.Union[VaultSecretsIntegrationAwsAccessKeys, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationAwsFederatedWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        azure_client_secret: typing.Optional[typing.Union[VaultSecretsIntegrationAzureClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
        azure_federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationAzureFederatedWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        confluent_static_credentials: typing.Optional[typing.Union["VaultSecretsIntegrationConfluentStaticCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        gcp_federated_workload_identity: typing.Optional[typing.Union["VaultSecretsIntegrationGcpFederatedWorkloadIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        gcp_service_account_key: typing.Optional[typing.Union["VaultSecretsIntegrationGcpServiceAccountKey", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_access: typing.Optional[typing.Union["VaultSecretsIntegrationGitlabAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        mongodb_atlas_static_credentials: typing.Optional[typing.Union["VaultSecretsIntegrationMongodbAtlasStaticCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        twilio_static_credentials: typing.Optional[typing.Union["VaultSecretsIntegrationTwilioStaticCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capabilities: Capabilities enabled for the integration. See the Vault Secrets documentation for the list of supported capabilities per provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#capabilities VaultSecretsIntegration#capabilities}
        :param name: The Vault Secrets integration name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#name VaultSecretsIntegration#name}
        :param provider_type: The provider or 3rd party platform the integration is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#provider_type VaultSecretsIntegration#provider_type}
        :param aws_access_keys: AWS IAM key pair used to authenticate against the target AWS account. Cannot be used with ``federated_workload_identity``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#aws_access_keys VaultSecretsIntegration#aws_access_keys}
        :param aws_federated_workload_identity: (Recommended) Federated identity configuration to authenticate against the target AWS account. Cannot be used with ``access_keys``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#aws_federated_workload_identity VaultSecretsIntegration#aws_federated_workload_identity}
        :param azure_client_secret: Azure client secret used to authenticate against the target Azure application. Cannot be used with ``federated_workload_identity``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#azure_client_secret VaultSecretsIntegration#azure_client_secret}
        :param azure_federated_workload_identity: (Recommended) Federated identity configuration to authenticate against the target Azure application. Cannot be used with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#azure_federated_workload_identity VaultSecretsIntegration#azure_federated_workload_identity}
        :param confluent_static_credentials: Confluent API key used to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#confluent_static_credentials VaultSecretsIntegration#confluent_static_credentials}
        :param gcp_federated_workload_identity: (Recommended) Federated identity configuration to authenticate against the target GCP project. Cannot be used with ``service_account_key``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#gcp_federated_workload_identity VaultSecretsIntegration#gcp_federated_workload_identity}
        :param gcp_service_account_key: GCP service account key used to authenticate against the target GCP project. Cannot be used with ``federated_workload_identity``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#gcp_service_account_key VaultSecretsIntegration#gcp_service_account_key}
        :param gitlab_access: GitLab access token used to authenticate against the target GitLab account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#gitlab_access VaultSecretsIntegration#gitlab_access}
        :param mongodb_atlas_static_credentials: MongoDB Atlas API key used to authenticate against the target project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#mongodb_atlas_static_credentials VaultSecretsIntegration#mongodb_atlas_static_credentials}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#project_id VaultSecretsIntegration#project_id}
        :param twilio_static_credentials: Twilio API key parts used to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#twilio_static_credentials VaultSecretsIntegration#twilio_static_credentials}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws_access_keys, dict):
            aws_access_keys = VaultSecretsIntegrationAwsAccessKeys(**aws_access_keys)
        if isinstance(aws_federated_workload_identity, dict):
            aws_federated_workload_identity = VaultSecretsIntegrationAwsFederatedWorkloadIdentity(**aws_federated_workload_identity)
        if isinstance(azure_client_secret, dict):
            azure_client_secret = VaultSecretsIntegrationAzureClientSecret(**azure_client_secret)
        if isinstance(azure_federated_workload_identity, dict):
            azure_federated_workload_identity = VaultSecretsIntegrationAzureFederatedWorkloadIdentity(**azure_federated_workload_identity)
        if isinstance(confluent_static_credentials, dict):
            confluent_static_credentials = VaultSecretsIntegrationConfluentStaticCredentials(**confluent_static_credentials)
        if isinstance(gcp_federated_workload_identity, dict):
            gcp_federated_workload_identity = VaultSecretsIntegrationGcpFederatedWorkloadIdentity(**gcp_federated_workload_identity)
        if isinstance(gcp_service_account_key, dict):
            gcp_service_account_key = VaultSecretsIntegrationGcpServiceAccountKey(**gcp_service_account_key)
        if isinstance(gitlab_access, dict):
            gitlab_access = VaultSecretsIntegrationGitlabAccess(**gitlab_access)
        if isinstance(mongodb_atlas_static_credentials, dict):
            mongodb_atlas_static_credentials = VaultSecretsIntegrationMongodbAtlasStaticCredentials(**mongodb_atlas_static_credentials)
        if isinstance(twilio_static_credentials, dict):
            twilio_static_credentials = VaultSecretsIntegrationTwilioStaticCredentials(**twilio_static_credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64ec084c6d8734ea68fc18f26cf657477a33ca4fc94df0223d13de263e3ff7c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument aws_access_keys", value=aws_access_keys, expected_type=type_hints["aws_access_keys"])
            check_type(argname="argument aws_federated_workload_identity", value=aws_federated_workload_identity, expected_type=type_hints["aws_federated_workload_identity"])
            check_type(argname="argument azure_client_secret", value=azure_client_secret, expected_type=type_hints["azure_client_secret"])
            check_type(argname="argument azure_federated_workload_identity", value=azure_federated_workload_identity, expected_type=type_hints["azure_federated_workload_identity"])
            check_type(argname="argument confluent_static_credentials", value=confluent_static_credentials, expected_type=type_hints["confluent_static_credentials"])
            check_type(argname="argument gcp_federated_workload_identity", value=gcp_federated_workload_identity, expected_type=type_hints["gcp_federated_workload_identity"])
            check_type(argname="argument gcp_service_account_key", value=gcp_service_account_key, expected_type=type_hints["gcp_service_account_key"])
            check_type(argname="argument gitlab_access", value=gitlab_access, expected_type=type_hints["gitlab_access"])
            check_type(argname="argument mongodb_atlas_static_credentials", value=mongodb_atlas_static_credentials, expected_type=type_hints["mongodb_atlas_static_credentials"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument twilio_static_credentials", value=twilio_static_credentials, expected_type=type_hints["twilio_static_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capabilities": capabilities,
            "name": name,
            "provider_type": provider_type,
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
        if aws_access_keys is not None:
            self._values["aws_access_keys"] = aws_access_keys
        if aws_federated_workload_identity is not None:
            self._values["aws_federated_workload_identity"] = aws_federated_workload_identity
        if azure_client_secret is not None:
            self._values["azure_client_secret"] = azure_client_secret
        if azure_federated_workload_identity is not None:
            self._values["azure_federated_workload_identity"] = azure_federated_workload_identity
        if confluent_static_credentials is not None:
            self._values["confluent_static_credentials"] = confluent_static_credentials
        if gcp_federated_workload_identity is not None:
            self._values["gcp_federated_workload_identity"] = gcp_federated_workload_identity
        if gcp_service_account_key is not None:
            self._values["gcp_service_account_key"] = gcp_service_account_key
        if gitlab_access is not None:
            self._values["gitlab_access"] = gitlab_access
        if mongodb_atlas_static_credentials is not None:
            self._values["mongodb_atlas_static_credentials"] = mongodb_atlas_static_credentials
        if project_id is not None:
            self._values["project_id"] = project_id
        if twilio_static_credentials is not None:
            self._values["twilio_static_credentials"] = twilio_static_credentials

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#capabilities VaultSecretsIntegration#capabilities}
        '''
        result = self._values.get("capabilities")
        assert result is not None, "Required property 'capabilities' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The Vault Secrets integration name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#name VaultSecretsIntegration#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_type(self) -> builtins.str:
        '''The provider or 3rd party platform the integration is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#provider_type VaultSecretsIntegration#provider_type}
        '''
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_access_keys(self) -> typing.Optional[VaultSecretsIntegrationAwsAccessKeys]:
        '''AWS IAM key pair used to authenticate against the target AWS account. Cannot be used with ``federated_workload_identity``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#aws_access_keys VaultSecretsIntegration#aws_access_keys}
        '''
        result = self._values.get("aws_access_keys")
        return typing.cast(typing.Optional[VaultSecretsIntegrationAwsAccessKeys], result)

    @builtins.property
    def aws_federated_workload_identity(
        self,
    ) -> typing.Optional[VaultSecretsIntegrationAwsFederatedWorkloadIdentity]:
        '''(Recommended) Federated identity configuration to authenticate against the target AWS account. Cannot be used with ``access_keys``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#aws_federated_workload_identity VaultSecretsIntegration#aws_federated_workload_identity}
        '''
        result = self._values.get("aws_federated_workload_identity")
        return typing.cast(typing.Optional[VaultSecretsIntegrationAwsFederatedWorkloadIdentity], result)

    @builtins.property
    def azure_client_secret(
        self,
    ) -> typing.Optional[VaultSecretsIntegrationAzureClientSecret]:
        '''Azure client secret used to authenticate against the target Azure application. Cannot be used with ``federated_workload_identity``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#azure_client_secret VaultSecretsIntegration#azure_client_secret}
        '''
        result = self._values.get("azure_client_secret")
        return typing.cast(typing.Optional[VaultSecretsIntegrationAzureClientSecret], result)

    @builtins.property
    def azure_federated_workload_identity(
        self,
    ) -> typing.Optional[VaultSecretsIntegrationAzureFederatedWorkloadIdentity]:
        '''(Recommended) Federated identity configuration to authenticate against the target Azure application. Cannot be used with ``client_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#azure_federated_workload_identity VaultSecretsIntegration#azure_federated_workload_identity}
        '''
        result = self._values.get("azure_federated_workload_identity")
        return typing.cast(typing.Optional[VaultSecretsIntegrationAzureFederatedWorkloadIdentity], result)

    @builtins.property
    def confluent_static_credentials(
        self,
    ) -> typing.Optional["VaultSecretsIntegrationConfluentStaticCredentials"]:
        '''Confluent API key used to authenticate for cloud apis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#confluent_static_credentials VaultSecretsIntegration#confluent_static_credentials}
        '''
        result = self._values.get("confluent_static_credentials")
        return typing.cast(typing.Optional["VaultSecretsIntegrationConfluentStaticCredentials"], result)

    @builtins.property
    def gcp_federated_workload_identity(
        self,
    ) -> typing.Optional["VaultSecretsIntegrationGcpFederatedWorkloadIdentity"]:
        '''(Recommended) Federated identity configuration to authenticate against the target GCP project. Cannot be used with ``service_account_key``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#gcp_federated_workload_identity VaultSecretsIntegration#gcp_federated_workload_identity}
        '''
        result = self._values.get("gcp_federated_workload_identity")
        return typing.cast(typing.Optional["VaultSecretsIntegrationGcpFederatedWorkloadIdentity"], result)

    @builtins.property
    def gcp_service_account_key(
        self,
    ) -> typing.Optional["VaultSecretsIntegrationGcpServiceAccountKey"]:
        '''GCP service account key used to authenticate against the target GCP project. Cannot be used with ``federated_workload_identity``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#gcp_service_account_key VaultSecretsIntegration#gcp_service_account_key}
        '''
        result = self._values.get("gcp_service_account_key")
        return typing.cast(typing.Optional["VaultSecretsIntegrationGcpServiceAccountKey"], result)

    @builtins.property
    def gitlab_access(self) -> typing.Optional["VaultSecretsIntegrationGitlabAccess"]:
        '''GitLab access token used to authenticate against the target GitLab account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#gitlab_access VaultSecretsIntegration#gitlab_access}
        '''
        result = self._values.get("gitlab_access")
        return typing.cast(typing.Optional["VaultSecretsIntegrationGitlabAccess"], result)

    @builtins.property
    def mongodb_atlas_static_credentials(
        self,
    ) -> typing.Optional["VaultSecretsIntegrationMongodbAtlasStaticCredentials"]:
        '''MongoDB Atlas API key used to authenticate against the target project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#mongodb_atlas_static_credentials VaultSecretsIntegration#mongodb_atlas_static_credentials}
        '''
        result = self._values.get("mongodb_atlas_static_credentials")
        return typing.cast(typing.Optional["VaultSecretsIntegrationMongodbAtlasStaticCredentials"], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#project_id VaultSecretsIntegration#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twilio_static_credentials(
        self,
    ) -> typing.Optional["VaultSecretsIntegrationTwilioStaticCredentials"]:
        '''Twilio API key parts used to authenticate against the target Twilio account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#twilio_static_credentials VaultSecretsIntegration#twilio_static_credentials}
        '''
        result = self._values.get("twilio_static_credentials")
        return typing.cast(typing.Optional["VaultSecretsIntegrationTwilioStaticCredentials"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationConfluentStaticCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_api_key_id": "cloudApiKeyId",
        "cloud_api_secret": "cloudApiSecret",
    },
)
class VaultSecretsIntegrationConfluentStaticCredentials:
    def __init__(
        self,
        *,
        cloud_api_key_id: builtins.str,
        cloud_api_secret: builtins.str,
    ) -> None:
        '''
        :param cloud_api_key_id: Public key used alongside the private key to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#cloud_api_key_id VaultSecretsIntegration#cloud_api_key_id}
        :param cloud_api_secret: Private key used alongside the public key to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#cloud_api_secret VaultSecretsIntegration#cloud_api_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378ae7a764904fbd85b673c5822143483f4b1e43308b8627e8498021f7dec7dc)
            check_type(argname="argument cloud_api_key_id", value=cloud_api_key_id, expected_type=type_hints["cloud_api_key_id"])
            check_type(argname="argument cloud_api_secret", value=cloud_api_secret, expected_type=type_hints["cloud_api_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_api_key_id": cloud_api_key_id,
            "cloud_api_secret": cloud_api_secret,
        }

    @builtins.property
    def cloud_api_key_id(self) -> builtins.str:
        '''Public key used alongside the private key to authenticate for cloud apis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#cloud_api_key_id VaultSecretsIntegration#cloud_api_key_id}
        '''
        result = self._values.get("cloud_api_key_id")
        assert result is not None, "Required property 'cloud_api_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_api_secret(self) -> builtins.str:
        '''Private key used alongside the public key to authenticate for cloud apis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#cloud_api_secret VaultSecretsIntegration#cloud_api_secret}
        '''
        result = self._values.get("cloud_api_secret")
        assert result is not None, "Required property 'cloud_api_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationConfluentStaticCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationConfluentStaticCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationConfluentStaticCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7439b68c3ae4549291f9c4fc1dddd0167ae124733091e824c54e34878e24192)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cloudApiKeyIdInput")
    def cloud_api_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudApiKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudApiSecretInput")
    def cloud_api_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudApiSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudApiKeyId")
    def cloud_api_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudApiKeyId"))

    @cloud_api_key_id.setter
    def cloud_api_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811d5bc7b304ef50e9c04a94a0f7767bfc1d209812442c19a750961a577bf760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudApiKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudApiSecret")
    def cloud_api_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudApiSecret"))

    @cloud_api_secret.setter
    def cloud_api_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061b72f54957e3e8c99d63313756b687fe7aded9c215ebdbddeeb6bd059f8aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudApiSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationConfluentStaticCredentials]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationConfluentStaticCredentials]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationConfluentStaticCredentials]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f48a30898337b54f7246185910ce670baa1d87bd71af248ed85b1e27bf83612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationGcpFederatedWorkloadIdentity",
    jsii_struct_bases=[],
    name_mapping={
        "audience": "audience",
        "service_account_email": "serviceAccountEmail",
    },
)
class VaultSecretsIntegrationGcpFederatedWorkloadIdentity:
    def __init__(
        self,
        *,
        audience: builtins.str,
        service_account_email: builtins.str,
    ) -> None:
        '''
        :param audience: Audience configured on the GCP identity provider to federate access with HCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#audience VaultSecretsIntegration#audience}
        :param service_account_email: GCP service account email that HVS will impersonate to carry operations for the appropriate capabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#service_account_email VaultSecretsIntegration#service_account_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542ae0a9c2e87907c3a4407ada20659f45ee6ade209db1f79f8b67dfcc2b1e56)
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audience": audience,
            "service_account_email": service_account_email,
        }

    @builtins.property
    def audience(self) -> builtins.str:
        '''Audience configured on the GCP identity provider to federate access with HCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#audience VaultSecretsIntegration#audience}
        '''
        result = self._values.get("audience")
        assert result is not None, "Required property 'audience' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''GCP service account email that HVS will impersonate to carry operations for the appropriate capabilities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#service_account_email VaultSecretsIntegration#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationGcpFederatedWorkloadIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationGcpFederatedWorkloadIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationGcpFederatedWorkloadIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__073bdf147386ca728b9ec0e0d36b1945a3700681ac038f7892bf5834cf477040)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82a73cf518edc38b539601f4f45aef39c40aee2524902d13b8acebc404704112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68df1e988221a88f5fef65e4da55de9310d940f58ac6081c54b8bdb546f96c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpFederatedWorkloadIdentity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpFederatedWorkloadIdentity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpFederatedWorkloadIdentity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5302940a1c785bf278cd08bff7d36393514d94e64307b63cdcd371ef188962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationGcpServiceAccountKey",
    jsii_struct_bases=[],
    name_mapping={"credentials": "credentials"},
)
class VaultSecretsIntegrationGcpServiceAccountKey:
    def __init__(self, *, credentials: builtins.str) -> None:
        '''
        :param credentials: JSON or base64 encoded service account key received from GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#credentials VaultSecretsIntegration#credentials}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b211fe857af4577f93e06cf5cf038512fb8810824ed22510ca7a6f05b40bfe)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
        }

    @builtins.property
    def credentials(self) -> builtins.str:
        '''JSON or base64 encoded service account key received from GCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#credentials VaultSecretsIntegration#credentials}
        '''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationGcpServiceAccountKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationGcpServiceAccountKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationGcpServiceAccountKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b430e6feb89f2ecf3c2d73718879765ea69eb8d36071c2cd26a6c318c5bedc15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecf2fb3fee5681e762e8263d5640df2310bab82b0cd1d3143fd6c8ff49754fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpServiceAccountKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpServiceAccountKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpServiceAccountKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d8305ceadad1a03deb94170dd61eb8c930b12cc1ddbc8f09f930302966c77e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationGitlabAccess",
    jsii_struct_bases=[],
    name_mapping={"token": "token"},
)
class VaultSecretsIntegrationGitlabAccess:
    def __init__(self, *, token: builtins.str) -> None:
        '''
        :param token: Access token used to authenticate against the target GitLab account. This token must have privilege to create CI/CD variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#token VaultSecretsIntegration#token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2ed1ba21f91261a1e46fae9fe1231631e4a199dae5f8fdd7187d51d419ca13)
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "token": token,
        }

    @builtins.property
    def token(self) -> builtins.str:
        '''Access token used to authenticate against the target GitLab account. This token must have privilege to create CI/CD variables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#token VaultSecretsIntegration#token}
        '''
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationGitlabAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationGitlabAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationGitlabAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ab44d5fcf276eb7157860e3fd6b3885eb32b706109bd7e1e320e6fd87bf2727)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9aa3a6785b05cb4aed94f80710d7b0540b82a4462d6f3ce086b3fb1d8f8c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGitlabAccess]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGitlabAccess]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGitlabAccess]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f72c304241b362d165dde3cd68bb2f1b98f82661e74a4b048ef18c63be5eab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationMongodbAtlasStaticCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "api_private_key": "apiPrivateKey",
        "api_public_key": "apiPublicKey",
    },
)
class VaultSecretsIntegrationMongodbAtlasStaticCredentials:
    def __init__(
        self,
        *,
        api_private_key: builtins.str,
        api_public_key: builtins.str,
    ) -> None:
        '''
        :param api_private_key: Private key used alongside the public key to authenticate against the target project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_private_key VaultSecretsIntegration#api_private_key}
        :param api_public_key: Public key used alongside the private key to authenticate against the target project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_public_key VaultSecretsIntegration#api_public_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e69ce7164a8d8a62e68970d1cc9d36bbc17e6006d8f9b8867c86787b68629b)
            check_type(argname="argument api_private_key", value=api_private_key, expected_type=type_hints["api_private_key"])
            check_type(argname="argument api_public_key", value=api_public_key, expected_type=type_hints["api_public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_private_key": api_private_key,
            "api_public_key": api_public_key,
        }

    @builtins.property
    def api_private_key(self) -> builtins.str:
        '''Private key used alongside the public key to authenticate against the target project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_private_key VaultSecretsIntegration#api_private_key}
        '''
        result = self._values.get("api_private_key")
        assert result is not None, "Required property 'api_private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_public_key(self) -> builtins.str:
        '''Public key used alongside the private key to authenticate against the target project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_public_key VaultSecretsIntegration#api_public_key}
        '''
        result = self._values.get("api_public_key")
        assert result is not None, "Required property 'api_public_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationMongodbAtlasStaticCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationMongodbAtlasStaticCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationMongodbAtlasStaticCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__851ceeedf5ecf2cb51b6981ccce19a3201b8fbf3d7b2e4114639cad6306a8709)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiPrivateKeyInput")
    def api_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiPublicKeyInput")
    def api_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiPrivateKey")
    def api_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiPrivateKey"))

    @api_private_key.setter
    def api_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6056716eb9cfe0dfa7067b496f50a7caae15882791409bdbb19631b8f5fa2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiPublicKey")
    def api_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiPublicKey"))

    @api_public_key.setter
    def api_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592cbfa7e1d3de074dbfa5381442b0362af517f30e8e6b8e63406fce90033847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationMongodbAtlasStaticCredentials]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationMongodbAtlasStaticCredentials]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationMongodbAtlasStaticCredentials]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7e0b751a3a71851c159ae6de1f2f8a7a36eef33e4b891d2c8d70b66e4d2c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationTwilioStaticCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "account_sid": "accountSid",
        "api_key_secret": "apiKeySecret",
        "api_key_sid": "apiKeySid",
    },
)
class VaultSecretsIntegrationTwilioStaticCredentials:
    def __init__(
        self,
        *,
        account_sid: builtins.str,
        api_key_secret: builtins.str,
        api_key_sid: builtins.str,
    ) -> None:
        '''
        :param account_sid: Account SID for the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#account_sid VaultSecretsIntegration#account_sid}
        :param api_key_secret: Api key secret used with the api key SID to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_key_secret VaultSecretsIntegration#api_key_secret}
        :param api_key_sid: Api key SID to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_key_sid VaultSecretsIntegration#api_key_sid}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf434ecbad6f1b01ebba49c8b5877c7d3673d9dded2b54a4f9160ffc6ca933e)
            check_type(argname="argument account_sid", value=account_sid, expected_type=type_hints["account_sid"])
            check_type(argname="argument api_key_secret", value=api_key_secret, expected_type=type_hints["api_key_secret"])
            check_type(argname="argument api_key_sid", value=api_key_sid, expected_type=type_hints["api_key_sid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_sid": account_sid,
            "api_key_secret": api_key_secret,
            "api_key_sid": api_key_sid,
        }

    @builtins.property
    def account_sid(self) -> builtins.str:
        '''Account SID for the target Twilio account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#account_sid VaultSecretsIntegration#account_sid}
        '''
        result = self._values.get("account_sid")
        assert result is not None, "Required property 'account_sid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_secret(self) -> builtins.str:
        '''Api key secret used with the api key SID to authenticate against the target Twilio account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_key_secret VaultSecretsIntegration#api_key_secret}
        '''
        result = self._values.get("api_key_secret")
        assert result is not None, "Required property 'api_key_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_sid(self) -> builtins.str:
        '''Api key SID to authenticate against the target Twilio account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration#api_key_sid VaultSecretsIntegration#api_key_sid}
        '''
        result = self._values.get("api_key_sid")
        assert result is not None, "Required property 'api_key_sid' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationTwilioStaticCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationTwilioStaticCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegration.VaultSecretsIntegrationTwilioStaticCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__155553b178048e6a89c2380b23384ebfe86b74f6999086e9d492272644fd05d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accountSidInput")
    def account_sid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountSidInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeySecretInput")
    def api_key_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeySecretInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeySidInput")
    def api_key_sid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeySidInput"))

    @builtins.property
    @jsii.member(jsii_name="accountSid")
    def account_sid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountSid"))

    @account_sid.setter
    def account_sid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b371c73165b0565197d9f5455d56e2e67c01d4712ca1cac4b6f87fddcc5f7af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountSid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKeySecret")
    def api_key_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKeySecret"))

    @api_key_secret.setter
    def api_key_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55587d5b3badee4a407ebe118b3a141e8b04e99de0a6fd5062b40031ad2c2b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeySecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKeySid")
    def api_key_sid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKeySid"))

    @api_key_sid.setter
    def api_key_sid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b57b038d91c10a78d45f8d79176c215bbf420e92351c44b27bf4d1dbbfb0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeySid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationTwilioStaticCredentials]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationTwilioStaticCredentials]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationTwilioStaticCredentials]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337c971288f63700bce0ed9a0dbb74e9f470a89fa16e95cecbe1ce23e22b3ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VaultSecretsIntegration",
    "VaultSecretsIntegrationAwsAccessKeys",
    "VaultSecretsIntegrationAwsAccessKeysOutputReference",
    "VaultSecretsIntegrationAwsFederatedWorkloadIdentity",
    "VaultSecretsIntegrationAwsFederatedWorkloadIdentityOutputReference",
    "VaultSecretsIntegrationAzureClientSecret",
    "VaultSecretsIntegrationAzureClientSecretOutputReference",
    "VaultSecretsIntegrationAzureFederatedWorkloadIdentity",
    "VaultSecretsIntegrationAzureFederatedWorkloadIdentityOutputReference",
    "VaultSecretsIntegrationConfig",
    "VaultSecretsIntegrationConfluentStaticCredentials",
    "VaultSecretsIntegrationConfluentStaticCredentialsOutputReference",
    "VaultSecretsIntegrationGcpFederatedWorkloadIdentity",
    "VaultSecretsIntegrationGcpFederatedWorkloadIdentityOutputReference",
    "VaultSecretsIntegrationGcpServiceAccountKey",
    "VaultSecretsIntegrationGcpServiceAccountKeyOutputReference",
    "VaultSecretsIntegrationGitlabAccess",
    "VaultSecretsIntegrationGitlabAccessOutputReference",
    "VaultSecretsIntegrationMongodbAtlasStaticCredentials",
    "VaultSecretsIntegrationMongodbAtlasStaticCredentialsOutputReference",
    "VaultSecretsIntegrationTwilioStaticCredentials",
    "VaultSecretsIntegrationTwilioStaticCredentialsOutputReference",
]

publication.publish()

def _typecheckingstub__b2562d56f521106b9e798eb60978ee1985ca00fa5e41574b4da5b8873d58a168(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    capabilities: typing.Sequence[builtins.str],
    name: builtins.str,
    provider_type: builtins.str,
    aws_access_keys: typing.Optional[typing.Union[VaultSecretsIntegrationAwsAccessKeys, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationAwsFederatedWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_client_secret: typing.Optional[typing.Union[VaultSecretsIntegrationAzureClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationAzureFederatedWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    confluent_static_credentials: typing.Optional[typing.Union[VaultSecretsIntegrationConfluentStaticCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    gcp_federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationGcpFederatedWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    gcp_service_account_key: typing.Optional[typing.Union[VaultSecretsIntegrationGcpServiceAccountKey, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_access: typing.Optional[typing.Union[VaultSecretsIntegrationGitlabAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    mongodb_atlas_static_credentials: typing.Optional[typing.Union[VaultSecretsIntegrationMongodbAtlasStaticCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    twilio_static_credentials: typing.Optional[typing.Union[VaultSecretsIntegrationTwilioStaticCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5df9acaf9183d622e8ee43d1d4155fb4f7f585583dc420bfe5eef67c77d1949c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722651326bf62d63e85483dbe38b3310717702493486c00e27eab1d44d645c5c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da77f3411b182ac7bd46adf9d909aba0858aae2a4d4b677acc824ecfb2de3689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d3c75d93198fed50c17bafa930f5535d2e9b3ab3fbc041daddeb2eccaa6b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9475c18bbef9789b7167f9005bb2a2026d4ec7de7ed209a48b72826e6e88357f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b9db9d07130834d3f2db6bba649170373a5425586f7f5295afe72adef570f8(
    *,
    access_key_id: builtins.str,
    secret_access_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0647d815335539cc16a4a58261329ea0b5cb1220af33db7c88cadcc43744ea0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770656e077f1175fa4f190ced950df09d0f9d3e70500d7f6e403d117a8992045(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a09ee83b71910d22d3267fa5224631ead18d43f3cedb35b5e885038fef0a8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572b65a018c6ba833d8159a688f49bddb55e3afb073732f176240db69702d908(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAwsAccessKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080663c8e8bb0cf6a4e9ceb924142363f0b39092159fddff16ed50330992fd72(
    *,
    audience: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879cdfa1ef86841f3a77098dcc3a79b3f6865ce5b385eea4fc9689781028756a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8378faa6cac2bdaa044a6f9551307e3331495981561db38e1cd477d67c74439(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4056798cd3a6b059100ec36bd41a91ab39197452fce94026575a1680dc5a5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc8a9083fbf2f66e8b45e527e50fac481fd949f43b177e795d9212823ab7f9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAwsFederatedWorkloadIdentity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bee425770f92e9a6b1285c5acec21b3f1f7121de278326014a2b9fcac81f516(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    tenant_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac43137b5814634fecaacb07256b59f5a9fb88a5351514fd43a2f14709ad65a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668c7eed2d3ea453def081a82ed65894463a962deeedf5d8ff8d1de8382dcd98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24319efc4c9cfb5b6fa4c8b87ff38be85495f3550972271b5ee18e3d1ccf9ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9221795e828c61c73e9d3fc9a5d59971978e78b95850cff9058580400e0757be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54139cc11b7cd9af6345322b2438f45a48827ef004c6ca4e9a34fd8bd757af6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAzureClientSecret]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b166c23d1ded8139f9456d26340fd37c032f128ee86120a87b9ef8f0dc8b981a(
    *,
    audience: builtins.str,
    client_id: builtins.str,
    tenant_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a570fa3cd00a7af4f4f0c23cc731efe889a78b20c095edafe3b68845ea4ff9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270a9b6535c7e38c7c617abdc0815d9422296de94ad7aee1cbc0eb4ea2118eef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d6c58f15cca9644ed8b47c245e129504e28c748aa71cbe75467f98d725f121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d8b3af5c6c3fbf640f922367d4299ece8a42d3d79b6828ca962489646106a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3911b4ed49939fe240e8521f12e143e4cc509cad64685339692602142d9c50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationAzureFederatedWorkloadIdentity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64ec084c6d8734ea68fc18f26cf657477a33ca4fc94df0223d13de263e3ff7c(
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
    provider_type: builtins.str,
    aws_access_keys: typing.Optional[typing.Union[VaultSecretsIntegrationAwsAccessKeys, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationAwsFederatedWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_client_secret: typing.Optional[typing.Union[VaultSecretsIntegrationAzureClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationAzureFederatedWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    confluent_static_credentials: typing.Optional[typing.Union[VaultSecretsIntegrationConfluentStaticCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    gcp_federated_workload_identity: typing.Optional[typing.Union[VaultSecretsIntegrationGcpFederatedWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    gcp_service_account_key: typing.Optional[typing.Union[VaultSecretsIntegrationGcpServiceAccountKey, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_access: typing.Optional[typing.Union[VaultSecretsIntegrationGitlabAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    mongodb_atlas_static_credentials: typing.Optional[typing.Union[VaultSecretsIntegrationMongodbAtlasStaticCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    twilio_static_credentials: typing.Optional[typing.Union[VaultSecretsIntegrationTwilioStaticCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378ae7a764904fbd85b673c5822143483f4b1e43308b8627e8498021f7dec7dc(
    *,
    cloud_api_key_id: builtins.str,
    cloud_api_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7439b68c3ae4549291f9c4fc1dddd0167ae124733091e824c54e34878e24192(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811d5bc7b304ef50e9c04a94a0f7767bfc1d209812442c19a750961a577bf760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061b72f54957e3e8c99d63313756b687fe7aded9c215ebdbddeeb6bd059f8aa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f48a30898337b54f7246185910ce670baa1d87bd71af248ed85b1e27bf83612(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationConfluentStaticCredentials]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542ae0a9c2e87907c3a4407ada20659f45ee6ade209db1f79f8b67dfcc2b1e56(
    *,
    audience: builtins.str,
    service_account_email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073bdf147386ca728b9ec0e0d36b1945a3700681ac038f7892bf5834cf477040(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a73cf518edc38b539601f4f45aef39c40aee2524902d13b8acebc404704112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68df1e988221a88f5fef65e4da55de9310d940f58ac6081c54b8bdb546f96c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5302940a1c785bf278cd08bff7d36393514d94e64307b63cdcd371ef188962(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpFederatedWorkloadIdentity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b211fe857af4577f93e06cf5cf038512fb8810824ed22510ca7a6f05b40bfe(
    *,
    credentials: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b430e6feb89f2ecf3c2d73718879765ea69eb8d36071c2cd26a6c318c5bedc15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf2fb3fee5681e762e8263d5640df2310bab82b0cd1d3143fd6c8ff49754fb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d8305ceadad1a03deb94170dd61eb8c930b12cc1ddbc8f09f930302966c77e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGcpServiceAccountKey]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2ed1ba21f91261a1e46fae9fe1231631e4a199dae5f8fdd7187d51d419ca13(
    *,
    token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab44d5fcf276eb7157860e3fd6b3885eb32b706109bd7e1e320e6fd87bf2727(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9aa3a6785b05cb4aed94f80710d7b0540b82a4462d6f3ce086b3fb1d8f8c1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f72c304241b362d165dde3cd68bb2f1b98f82661e74a4b048ef18c63be5eab1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationGitlabAccess]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e69ce7164a8d8a62e68970d1cc9d36bbc17e6006d8f9b8867c86787b68629b(
    *,
    api_private_key: builtins.str,
    api_public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851ceeedf5ecf2cb51b6981ccce19a3201b8fbf3d7b2e4114639cad6306a8709(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6056716eb9cfe0dfa7067b496f50a7caae15882791409bdbb19631b8f5fa2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592cbfa7e1d3de074dbfa5381442b0362af517f30e8e6b8e63406fce90033847(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7e0b751a3a71851c159ae6de1f2f8a7a36eef33e4b891d2c8d70b66e4d2c76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationMongodbAtlasStaticCredentials]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf434ecbad6f1b01ebba49c8b5877c7d3673d9dded2b54a4f9160ffc6ca933e(
    *,
    account_sid: builtins.str,
    api_key_secret: builtins.str,
    api_key_sid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155553b178048e6a89c2380b23384ebfe86b74f6999086e9d492272644fd05d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b371c73165b0565197d9f5455d56e2e67c01d4712ca1cac4b6f87fddcc5f7af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55587d5b3badee4a407ebe118b3a141e8b04e99de0a6fd5062b40031ad2c2b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b57b038d91c10a78d45f8d79176c215bbf420e92351c44b27bf4d1dbbfb0aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337c971288f63700bce0ed9a0dbb74e9f470a89fa16e95cecbe1ce23e22b3ec1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationTwilioStaticCredentials]],
) -> None:
    """Type checking stubs"""
    pass
