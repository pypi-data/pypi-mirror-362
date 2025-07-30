r'''
# `hcp_vault_secrets_rotating_secret`

Refer to the Terraform Registry for docs: [`hcp_vault_secrets_rotating_secret`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret).
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


class VaultSecretsRotatingSecret(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecret",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret hcp_vault_secrets_rotating_secret}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_name: builtins.str,
        integration_name: builtins.str,
        name: builtins.str,
        rotation_policy_name: builtins.str,
        secret_provider: builtins.str,
        aws_access_keys: typing.Optional[typing.Union["VaultSecretsRotatingSecretAwsAccessKeys", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_application_password: typing.Optional[typing.Union["VaultSecretsRotatingSecretAzureApplicationPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        confluent_service_account: typing.Optional[typing.Union["VaultSecretsRotatingSecretConfluentServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        gcp_service_account_key: typing.Optional[typing.Union["VaultSecretsRotatingSecretGcpServiceAccountKey", typing.Dict[builtins.str, typing.Any]]] = None,
        mongodb_atlas_user: typing.Optional[typing.Union["VaultSecretsRotatingSecretMongodbAtlasUser", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        twilio_api_key: typing.Optional[typing.Union["VaultSecretsRotatingSecretTwilioApiKey", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret hcp_vault_secrets_rotating_secret} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_name: Vault Secrets application name that owns the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#app_name VaultSecretsRotatingSecret#app_name}
        :param integration_name: The Vault Secrets integration name with the capability to manage the secret's lifecycle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#integration_name VaultSecretsRotatingSecret#integration_name}
        :param name: The Vault Secrets secret name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#name VaultSecretsRotatingSecret#name}
        :param rotation_policy_name: Name of the rotation policy that governs the rotation of the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#rotation_policy_name VaultSecretsRotatingSecret#rotation_policy_name}
        :param secret_provider: The third party platform the dynamic credentials give access to. One of ``aws`` or ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#secret_provider VaultSecretsRotatingSecret#secret_provider}
        :param aws_access_keys: AWS configuration to manage the access key rotation for the given IAM user. Required if ``secret_provider`` is ``aws``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#aws_access_keys VaultSecretsRotatingSecret#aws_access_keys}
        :param azure_application_password: Azure configuration to manage the application password rotation for the given application. Required if ``secret_provider`` is ``Azure``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#azure_application_password VaultSecretsRotatingSecret#azure_application_password}
        :param confluent_service_account: Confluent configuration to manage the cloud api key rotation for the given service account. Required if ``secret_provider`` is ``confluent``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#confluent_service_account VaultSecretsRotatingSecret#confluent_service_account}
        :param gcp_service_account_key: GCP configuration to manage the service account key rotation for the given service account. Required if ``secret_provider`` is ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#gcp_service_account_key VaultSecretsRotatingSecret#gcp_service_account_key}
        :param mongodb_atlas_user: MongoDB Atlas configuration to manage the user password rotation on the given database. Required if ``secret_provider`` is ``mongodb_atlas``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#mongodb_atlas_user VaultSecretsRotatingSecret#mongodb_atlas_user}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#project_id VaultSecretsRotatingSecret#project_id}
        :param twilio_api_key: Twilio configuration to manage the api key rotation on the given account. Required if ``secret_provider`` is ``twilio``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#twilio_api_key VaultSecretsRotatingSecret#twilio_api_key}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec6532dc85e8c9a5219edbee934665fcd4a46eb79216eff7c5ca31773872085)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = VaultSecretsRotatingSecretConfig(
            app_name=app_name,
            integration_name=integration_name,
            name=name,
            rotation_policy_name=rotation_policy_name,
            secret_provider=secret_provider,
            aws_access_keys=aws_access_keys,
            azure_application_password=azure_application_password,
            confluent_service_account=confluent_service_account,
            gcp_service_account_key=gcp_service_account_key,
            mongodb_atlas_user=mongodb_atlas_user,
            project_id=project_id,
            twilio_api_key=twilio_api_key,
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
        '''Generates CDKTF code for importing a VaultSecretsRotatingSecret resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VaultSecretsRotatingSecret to import.
        :param import_from_id: The id of the existing VaultSecretsRotatingSecret that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VaultSecretsRotatingSecret to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b6ad29897b9f7701354369e5ef5e61d5e48fccdfdf42edbe71ae7f44ade1ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAwsAccessKeys")
    def put_aws_access_keys(self, *, iam_username: builtins.str) -> None:
        '''
        :param iam_username: AWS IAM username to rotate the access keys for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#iam_username VaultSecretsRotatingSecret#iam_username}
        '''
        value = VaultSecretsRotatingSecretAwsAccessKeys(iam_username=iam_username)

        return typing.cast(None, jsii.invoke(self, "putAwsAccessKeys", [value]))

    @jsii.member(jsii_name="putAzureApplicationPassword")
    def put_azure_application_password(
        self,
        *,
        app_client_id: builtins.str,
        app_object_id: builtins.str,
    ) -> None:
        '''
        :param app_client_id: Application client ID to rotate the application password for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#app_client_id VaultSecretsRotatingSecret#app_client_id}
        :param app_object_id: Application object ID to rotate the application password for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#app_object_id VaultSecretsRotatingSecret#app_object_id}
        '''
        value = VaultSecretsRotatingSecretAzureApplicationPassword(
            app_client_id=app_client_id, app_object_id=app_object_id
        )

        return typing.cast(None, jsii.invoke(self, "putAzureApplicationPassword", [value]))

    @jsii.member(jsii_name="putConfluentServiceAccount")
    def put_confluent_service_account(
        self,
        *,
        service_account_id: builtins.str,
    ) -> None:
        '''
        :param service_account_id: Confluent service account to rotate the cloud api key for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#service_account_id VaultSecretsRotatingSecret#service_account_id}
        '''
        value = VaultSecretsRotatingSecretConfluentServiceAccount(
            service_account_id=service_account_id
        )

        return typing.cast(None, jsii.invoke(self, "putConfluentServiceAccount", [value]))

    @jsii.member(jsii_name="putGcpServiceAccountKey")
    def put_gcp_service_account_key(
        self,
        *,
        service_account_email: builtins.str,
    ) -> None:
        '''
        :param service_account_email: GCP service account email to impersonate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#service_account_email VaultSecretsRotatingSecret#service_account_email}
        '''
        value = VaultSecretsRotatingSecretGcpServiceAccountKey(
            service_account_email=service_account_email
        )

        return typing.cast(None, jsii.invoke(self, "putGcpServiceAccountKey", [value]))

    @jsii.member(jsii_name="putMongodbAtlasUser")
    def put_mongodb_atlas_user(
        self,
        *,
        database_name: builtins.str,
        project_id: builtins.str,
        roles: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param database_name: MongoDB Atlas database or cluster name to rotate the username and password for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#database_name VaultSecretsRotatingSecret#database_name}
        :param project_id: MongoDB Atlas project ID to rotate the username and password for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#project_id VaultSecretsRotatingSecret#project_id}
        :param roles: MongoDB Atlas roles to assign to the rotating user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#roles VaultSecretsRotatingSecret#roles}
        '''
        value = VaultSecretsRotatingSecretMongodbAtlasUser(
            database_name=database_name, project_id=project_id, roles=roles
        )

        return typing.cast(None, jsii.invoke(self, "putMongodbAtlasUser", [value]))

    @jsii.member(jsii_name="putTwilioApiKey")
    def put_twilio_api_key(self) -> None:
        value = VaultSecretsRotatingSecretTwilioApiKey()

        return typing.cast(None, jsii.invoke(self, "putTwilioApiKey", [value]))

    @jsii.member(jsii_name="resetAwsAccessKeys")
    def reset_aws_access_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccessKeys", []))

    @jsii.member(jsii_name="resetAzureApplicationPassword")
    def reset_azure_application_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureApplicationPassword", []))

    @jsii.member(jsii_name="resetConfluentServiceAccount")
    def reset_confluent_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfluentServiceAccount", []))

    @jsii.member(jsii_name="resetGcpServiceAccountKey")
    def reset_gcp_service_account_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountKey", []))

    @jsii.member(jsii_name="resetMongodbAtlasUser")
    def reset_mongodb_atlas_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMongodbAtlasUser", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetTwilioApiKey")
    def reset_twilio_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwilioApiKey", []))

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
    def aws_access_keys(
        self,
    ) -> "VaultSecretsRotatingSecretAwsAccessKeysOutputReference":
        return typing.cast("VaultSecretsRotatingSecretAwsAccessKeysOutputReference", jsii.get(self, "awsAccessKeys"))

    @builtins.property
    @jsii.member(jsii_name="azureApplicationPassword")
    def azure_application_password(
        self,
    ) -> "VaultSecretsRotatingSecretAzureApplicationPasswordOutputReference":
        return typing.cast("VaultSecretsRotatingSecretAzureApplicationPasswordOutputReference", jsii.get(self, "azureApplicationPassword"))

    @builtins.property
    @jsii.member(jsii_name="confluentServiceAccount")
    def confluent_service_account(
        self,
    ) -> "VaultSecretsRotatingSecretConfluentServiceAccountOutputReference":
        return typing.cast("VaultSecretsRotatingSecretConfluentServiceAccountOutputReference", jsii.get(self, "confluentServiceAccount"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountKey")
    def gcp_service_account_key(
        self,
    ) -> "VaultSecretsRotatingSecretGcpServiceAccountKeyOutputReference":
        return typing.cast("VaultSecretsRotatingSecretGcpServiceAccountKeyOutputReference", jsii.get(self, "gcpServiceAccountKey"))

    @builtins.property
    @jsii.member(jsii_name="mongodbAtlasUser")
    def mongodb_atlas_user(
        self,
    ) -> "VaultSecretsRotatingSecretMongodbAtlasUserOutputReference":
        return typing.cast("VaultSecretsRotatingSecretMongodbAtlasUserOutputReference", jsii.get(self, "mongodbAtlasUser"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="twilioApiKey")
    def twilio_api_key(self) -> "VaultSecretsRotatingSecretTwilioApiKeyOutputReference":
        return typing.cast("VaultSecretsRotatingSecretTwilioApiKeyOutputReference", jsii.get(self, "twilioApiKey"))

    @builtins.property
    @jsii.member(jsii_name="appNameInput")
    def app_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appNameInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccessKeysInput")
    def aws_access_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretAwsAccessKeys"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretAwsAccessKeys"]], jsii.get(self, "awsAccessKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="azureApplicationPasswordInput")
    def azure_application_password_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretAzureApplicationPassword"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretAzureApplicationPassword"]], jsii.get(self, "azureApplicationPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="confluentServiceAccountInput")
    def confluent_service_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretConfluentServiceAccount"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretConfluentServiceAccount"]], jsii.get(self, "confluentServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountKeyInput")
    def gcp_service_account_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretGcpServiceAccountKey"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretGcpServiceAccountKey"]], jsii.get(self, "gcpServiceAccountKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationNameInput")
    def integration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mongodbAtlasUserInput")
    def mongodb_atlas_user_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretMongodbAtlasUser"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretMongodbAtlasUser"]], jsii.get(self, "mongodbAtlasUserInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationPolicyNameInput")
    def rotation_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rotationPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretProviderInput")
    def secret_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="twilioApiKeyInput")
    def twilio_api_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretTwilioApiKey"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsRotatingSecretTwilioApiKey"]], jsii.get(self, "twilioApiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="appName")
    def app_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appName"))

    @app_name.setter
    def app_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6a59417fd0347239ea9b769fda1cddcc6df1c5a8854f9f276cadfb78c95b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationName")
    def integration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationName"))

    @integration_name.setter
    def integration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca99b61e7d88f6c15d9727f38bf62d5c37fc40aec4af6f4384d02d556826eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e19ffcf4a1d7deabcfca054ae0b3c4e33fa809877709e95ff6fb320b91c4087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf17e38aa728ae2447cccf6b4056e84f056ddce7041ed2c94539e30eba49625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationPolicyName")
    def rotation_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationPolicyName"))

    @rotation_policy_name.setter
    def rotation_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c78775b2c443915b327cf0813b1bd9e38d85964a4f7b71c38b26e9890b620f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationPolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretProvider")
    def secret_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretProvider"))

    @secret_provider.setter
    def secret_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4efedcb236b22468fe2cea5a009d9f8e57ca6338ad01b7fe4d327a0d009286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretProvider", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretAwsAccessKeys",
    jsii_struct_bases=[],
    name_mapping={"iam_username": "iamUsername"},
)
class VaultSecretsRotatingSecretAwsAccessKeys:
    def __init__(self, *, iam_username: builtins.str) -> None:
        '''
        :param iam_username: AWS IAM username to rotate the access keys for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#iam_username VaultSecretsRotatingSecret#iam_username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808741ffffe717c6429bde4c9af942b56b0efa06c0f61760e87121d4362cfb7d)
            check_type(argname="argument iam_username", value=iam_username, expected_type=type_hints["iam_username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iam_username": iam_username,
        }

    @builtins.property
    def iam_username(self) -> builtins.str:
        '''AWS IAM username to rotate the access keys for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#iam_username VaultSecretsRotatingSecret#iam_username}
        '''
        result = self._values.get("iam_username")
        assert result is not None, "Required property 'iam_username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsRotatingSecretAwsAccessKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsRotatingSecretAwsAccessKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretAwsAccessKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96fdec798989335bfb16596e68e140971390f18723c9913b0681d56572100351)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="iamUsernameInput")
    def iam_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="iamUsername")
    def iam_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamUsername"))

    @iam_username.setter
    def iam_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0996733eaf40f142da865e9e0fd0e735f51849bad89d620bb486c2dd903f3af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretAwsAccessKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretAwsAccessKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretAwsAccessKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1567ecbfc0764bc9927f1e94a79aeaa1cca420aebb770f5595a226e8477bc7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretAzureApplicationPassword",
    jsii_struct_bases=[],
    name_mapping={"app_client_id": "appClientId", "app_object_id": "appObjectId"},
)
class VaultSecretsRotatingSecretAzureApplicationPassword:
    def __init__(
        self,
        *,
        app_client_id: builtins.str,
        app_object_id: builtins.str,
    ) -> None:
        '''
        :param app_client_id: Application client ID to rotate the application password for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#app_client_id VaultSecretsRotatingSecret#app_client_id}
        :param app_object_id: Application object ID to rotate the application password for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#app_object_id VaultSecretsRotatingSecret#app_object_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb097111b8bcc3a0b185863fa3eeeb70fdbe003d9021d0ca061672a82850b27)
            check_type(argname="argument app_client_id", value=app_client_id, expected_type=type_hints["app_client_id"])
            check_type(argname="argument app_object_id", value=app_object_id, expected_type=type_hints["app_object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_client_id": app_client_id,
            "app_object_id": app_object_id,
        }

    @builtins.property
    def app_client_id(self) -> builtins.str:
        '''Application client ID to rotate the application password for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#app_client_id VaultSecretsRotatingSecret#app_client_id}
        '''
        result = self._values.get("app_client_id")
        assert result is not None, "Required property 'app_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_object_id(self) -> builtins.str:
        '''Application object ID to rotate the application password for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#app_object_id VaultSecretsRotatingSecret#app_object_id}
        '''
        result = self._values.get("app_object_id")
        assert result is not None, "Required property 'app_object_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsRotatingSecretAzureApplicationPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsRotatingSecretAzureApplicationPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretAzureApplicationPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0552b65c7d4170341208bde6db1b9c280069b6d10f68ed34c9b9870114d61796)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="appClientIdInput")
    def app_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appObjectIdInput")
    def app_object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appObjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appClientId")
    def app_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appClientId"))

    @app_client_id.setter
    def app_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b299d8374eb52c808c573cef922c9f4bfb5c149ffb41b065c0c4500f0f73ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appObjectId")
    def app_object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appObjectId"))

    @app_object_id.setter
    def app_object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bdd411cb9b3027d53e3fe28bf8f08897ad2633b04b5c7a69fd9dcbde3ae1a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appObjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretAzureApplicationPassword]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretAzureApplicationPassword]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretAzureApplicationPassword]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07d0787fd8c9598849e092d0a11752f0049692900610d4be321be6627bbae0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_name": "appName",
        "integration_name": "integrationName",
        "name": "name",
        "rotation_policy_name": "rotationPolicyName",
        "secret_provider": "secretProvider",
        "aws_access_keys": "awsAccessKeys",
        "azure_application_password": "azureApplicationPassword",
        "confluent_service_account": "confluentServiceAccount",
        "gcp_service_account_key": "gcpServiceAccountKey",
        "mongodb_atlas_user": "mongodbAtlasUser",
        "project_id": "projectId",
        "twilio_api_key": "twilioApiKey",
    },
)
class VaultSecretsRotatingSecretConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_name: builtins.str,
        integration_name: builtins.str,
        name: builtins.str,
        rotation_policy_name: builtins.str,
        secret_provider: builtins.str,
        aws_access_keys: typing.Optional[typing.Union[VaultSecretsRotatingSecretAwsAccessKeys, typing.Dict[builtins.str, typing.Any]]] = None,
        azure_application_password: typing.Optional[typing.Union[VaultSecretsRotatingSecretAzureApplicationPassword, typing.Dict[builtins.str, typing.Any]]] = None,
        confluent_service_account: typing.Optional[typing.Union["VaultSecretsRotatingSecretConfluentServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        gcp_service_account_key: typing.Optional[typing.Union["VaultSecretsRotatingSecretGcpServiceAccountKey", typing.Dict[builtins.str, typing.Any]]] = None,
        mongodb_atlas_user: typing.Optional[typing.Union["VaultSecretsRotatingSecretMongodbAtlasUser", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        twilio_api_key: typing.Optional[typing.Union["VaultSecretsRotatingSecretTwilioApiKey", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_name: Vault Secrets application name that owns the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#app_name VaultSecretsRotatingSecret#app_name}
        :param integration_name: The Vault Secrets integration name with the capability to manage the secret's lifecycle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#integration_name VaultSecretsRotatingSecret#integration_name}
        :param name: The Vault Secrets secret name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#name VaultSecretsRotatingSecret#name}
        :param rotation_policy_name: Name of the rotation policy that governs the rotation of the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#rotation_policy_name VaultSecretsRotatingSecret#rotation_policy_name}
        :param secret_provider: The third party platform the dynamic credentials give access to. One of ``aws`` or ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#secret_provider VaultSecretsRotatingSecret#secret_provider}
        :param aws_access_keys: AWS configuration to manage the access key rotation for the given IAM user. Required if ``secret_provider`` is ``aws``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#aws_access_keys VaultSecretsRotatingSecret#aws_access_keys}
        :param azure_application_password: Azure configuration to manage the application password rotation for the given application. Required if ``secret_provider`` is ``Azure``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#azure_application_password VaultSecretsRotatingSecret#azure_application_password}
        :param confluent_service_account: Confluent configuration to manage the cloud api key rotation for the given service account. Required if ``secret_provider`` is ``confluent``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#confluent_service_account VaultSecretsRotatingSecret#confluent_service_account}
        :param gcp_service_account_key: GCP configuration to manage the service account key rotation for the given service account. Required if ``secret_provider`` is ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#gcp_service_account_key VaultSecretsRotatingSecret#gcp_service_account_key}
        :param mongodb_atlas_user: MongoDB Atlas configuration to manage the user password rotation on the given database. Required if ``secret_provider`` is ``mongodb_atlas``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#mongodb_atlas_user VaultSecretsRotatingSecret#mongodb_atlas_user}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#project_id VaultSecretsRotatingSecret#project_id}
        :param twilio_api_key: Twilio configuration to manage the api key rotation on the given account. Required if ``secret_provider`` is ``twilio``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#twilio_api_key VaultSecretsRotatingSecret#twilio_api_key}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws_access_keys, dict):
            aws_access_keys = VaultSecretsRotatingSecretAwsAccessKeys(**aws_access_keys)
        if isinstance(azure_application_password, dict):
            azure_application_password = VaultSecretsRotatingSecretAzureApplicationPassword(**azure_application_password)
        if isinstance(confluent_service_account, dict):
            confluent_service_account = VaultSecretsRotatingSecretConfluentServiceAccount(**confluent_service_account)
        if isinstance(gcp_service_account_key, dict):
            gcp_service_account_key = VaultSecretsRotatingSecretGcpServiceAccountKey(**gcp_service_account_key)
        if isinstance(mongodb_atlas_user, dict):
            mongodb_atlas_user = VaultSecretsRotatingSecretMongodbAtlasUser(**mongodb_atlas_user)
        if isinstance(twilio_api_key, dict):
            twilio_api_key = VaultSecretsRotatingSecretTwilioApiKey(**twilio_api_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997d0111db41a34ec4ab3e2172e798abbb22286f43d57eaf9e4dfd104b5aa13a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_name", value=app_name, expected_type=type_hints["app_name"])
            check_type(argname="argument integration_name", value=integration_name, expected_type=type_hints["integration_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rotation_policy_name", value=rotation_policy_name, expected_type=type_hints["rotation_policy_name"])
            check_type(argname="argument secret_provider", value=secret_provider, expected_type=type_hints["secret_provider"])
            check_type(argname="argument aws_access_keys", value=aws_access_keys, expected_type=type_hints["aws_access_keys"])
            check_type(argname="argument azure_application_password", value=azure_application_password, expected_type=type_hints["azure_application_password"])
            check_type(argname="argument confluent_service_account", value=confluent_service_account, expected_type=type_hints["confluent_service_account"])
            check_type(argname="argument gcp_service_account_key", value=gcp_service_account_key, expected_type=type_hints["gcp_service_account_key"])
            check_type(argname="argument mongodb_atlas_user", value=mongodb_atlas_user, expected_type=type_hints["mongodb_atlas_user"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument twilio_api_key", value=twilio_api_key, expected_type=type_hints["twilio_api_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_name": app_name,
            "integration_name": integration_name,
            "name": name,
            "rotation_policy_name": rotation_policy_name,
            "secret_provider": secret_provider,
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
        if azure_application_password is not None:
            self._values["azure_application_password"] = azure_application_password
        if confluent_service_account is not None:
            self._values["confluent_service_account"] = confluent_service_account
        if gcp_service_account_key is not None:
            self._values["gcp_service_account_key"] = gcp_service_account_key
        if mongodb_atlas_user is not None:
            self._values["mongodb_atlas_user"] = mongodb_atlas_user
        if project_id is not None:
            self._values["project_id"] = project_id
        if twilio_api_key is not None:
            self._values["twilio_api_key"] = twilio_api_key

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
    def app_name(self) -> builtins.str:
        '''Vault Secrets application name that owns the secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#app_name VaultSecretsRotatingSecret#app_name}
        '''
        result = self._values.get("app_name")
        assert result is not None, "Required property 'app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_name(self) -> builtins.str:
        '''The Vault Secrets integration name with the capability to manage the secret's lifecycle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#integration_name VaultSecretsRotatingSecret#integration_name}
        '''
        result = self._values.get("integration_name")
        assert result is not None, "Required property 'integration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The Vault Secrets secret name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#name VaultSecretsRotatingSecret#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rotation_policy_name(self) -> builtins.str:
        '''Name of the rotation policy that governs the rotation of the secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#rotation_policy_name VaultSecretsRotatingSecret#rotation_policy_name}
        '''
        result = self._values.get("rotation_policy_name")
        assert result is not None, "Required property 'rotation_policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_provider(self) -> builtins.str:
        '''The third party platform the dynamic credentials give access to. One of ``aws`` or ``gcp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#secret_provider VaultSecretsRotatingSecret#secret_provider}
        '''
        result = self._values.get("secret_provider")
        assert result is not None, "Required property 'secret_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_access_keys(
        self,
    ) -> typing.Optional[VaultSecretsRotatingSecretAwsAccessKeys]:
        '''AWS configuration to manage the access key rotation for the given IAM user. Required if ``secret_provider`` is ``aws``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#aws_access_keys VaultSecretsRotatingSecret#aws_access_keys}
        '''
        result = self._values.get("aws_access_keys")
        return typing.cast(typing.Optional[VaultSecretsRotatingSecretAwsAccessKeys], result)

    @builtins.property
    def azure_application_password(
        self,
    ) -> typing.Optional[VaultSecretsRotatingSecretAzureApplicationPassword]:
        '''Azure configuration to manage the application password rotation for the given application. Required if ``secret_provider`` is ``Azure``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#azure_application_password VaultSecretsRotatingSecret#azure_application_password}
        '''
        result = self._values.get("azure_application_password")
        return typing.cast(typing.Optional[VaultSecretsRotatingSecretAzureApplicationPassword], result)

    @builtins.property
    def confluent_service_account(
        self,
    ) -> typing.Optional["VaultSecretsRotatingSecretConfluentServiceAccount"]:
        '''Confluent configuration to manage the cloud api key rotation for the given service account. Required if ``secret_provider`` is ``confluent``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#confluent_service_account VaultSecretsRotatingSecret#confluent_service_account}
        '''
        result = self._values.get("confluent_service_account")
        return typing.cast(typing.Optional["VaultSecretsRotatingSecretConfluentServiceAccount"], result)

    @builtins.property
    def gcp_service_account_key(
        self,
    ) -> typing.Optional["VaultSecretsRotatingSecretGcpServiceAccountKey"]:
        '''GCP configuration to manage the service account key rotation for the given service account. Required if ``secret_provider`` is ``gcp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#gcp_service_account_key VaultSecretsRotatingSecret#gcp_service_account_key}
        '''
        result = self._values.get("gcp_service_account_key")
        return typing.cast(typing.Optional["VaultSecretsRotatingSecretGcpServiceAccountKey"], result)

    @builtins.property
    def mongodb_atlas_user(
        self,
    ) -> typing.Optional["VaultSecretsRotatingSecretMongodbAtlasUser"]:
        '''MongoDB Atlas configuration to manage the user password rotation on the given database. Required if ``secret_provider`` is ``mongodb_atlas``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#mongodb_atlas_user VaultSecretsRotatingSecret#mongodb_atlas_user}
        '''
        result = self._values.get("mongodb_atlas_user")
        return typing.cast(typing.Optional["VaultSecretsRotatingSecretMongodbAtlasUser"], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#project_id VaultSecretsRotatingSecret#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twilio_api_key(
        self,
    ) -> typing.Optional["VaultSecretsRotatingSecretTwilioApiKey"]:
        '''Twilio configuration to manage the api key rotation on the given account. Required if ``secret_provider`` is ``twilio``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#twilio_api_key VaultSecretsRotatingSecret#twilio_api_key}
        '''
        result = self._values.get("twilio_api_key")
        return typing.cast(typing.Optional["VaultSecretsRotatingSecretTwilioApiKey"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsRotatingSecretConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretConfluentServiceAccount",
    jsii_struct_bases=[],
    name_mapping={"service_account_id": "serviceAccountId"},
)
class VaultSecretsRotatingSecretConfluentServiceAccount:
    def __init__(self, *, service_account_id: builtins.str) -> None:
        '''
        :param service_account_id: Confluent service account to rotate the cloud api key for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#service_account_id VaultSecretsRotatingSecret#service_account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296cc033573dfc49f86902f6d43667db66162f0b28ca5347eeb73e8eb55703cb)
            check_type(argname="argument service_account_id", value=service_account_id, expected_type=type_hints["service_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account_id": service_account_id,
        }

    @builtins.property
    def service_account_id(self) -> builtins.str:
        '''Confluent service account to rotate the cloud api key for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#service_account_id VaultSecretsRotatingSecret#service_account_id}
        '''
        result = self._values.get("service_account_id")
        assert result is not None, "Required property 'service_account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsRotatingSecretConfluentServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsRotatingSecretConfluentServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretConfluentServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0914d4a2c0f828faa0804507c14db928967dd1d2dab58661503084eed543372)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="serviceAccountIdInput")
    def service_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountId")
    def service_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountId"))

    @service_account_id.setter
    def service_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac1316a001c7ef1b4b0c271ed89623a08ba77576c009b0b64d08b07d70f447b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretConfluentServiceAccount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretConfluentServiceAccount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretConfluentServiceAccount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0155863efe01606072cede817b5c3cf9871643014da7bc6d21756cd152a09207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretGcpServiceAccountKey",
    jsii_struct_bases=[],
    name_mapping={"service_account_email": "serviceAccountEmail"},
)
class VaultSecretsRotatingSecretGcpServiceAccountKey:
    def __init__(self, *, service_account_email: builtins.str) -> None:
        '''
        :param service_account_email: GCP service account email to impersonate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#service_account_email VaultSecretsRotatingSecret#service_account_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec31f51905b9be9eb9f20ed08367ba3713f52764254f2f1ff0eaf0bb7b8d6209)
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account_email": service_account_email,
        }

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''GCP service account email to impersonate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#service_account_email VaultSecretsRotatingSecret#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsRotatingSecretGcpServiceAccountKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsRotatingSecretGcpServiceAccountKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretGcpServiceAccountKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c7a42485a9fd547de0331cee9613677045b3405914b0f62f0d77058fd296d71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1209f0c459ac70073bb408261533108b68befa6805bb82fc792e0ffbad5616eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretGcpServiceAccountKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretGcpServiceAccountKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretGcpServiceAccountKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06bc25eee53f4e54cafd229758dddf41e39c1cfc2841f250c60450e981d18884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretMongodbAtlasUser",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "project_id": "projectId",
        "roles": "roles",
    },
)
class VaultSecretsRotatingSecretMongodbAtlasUser:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        project_id: builtins.str,
        roles: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param database_name: MongoDB Atlas database or cluster name to rotate the username and password for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#database_name VaultSecretsRotatingSecret#database_name}
        :param project_id: MongoDB Atlas project ID to rotate the username and password for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#project_id VaultSecretsRotatingSecret#project_id}
        :param roles: MongoDB Atlas roles to assign to the rotating user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#roles VaultSecretsRotatingSecret#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe05bcc2cf91feb767a6b58ac86aa2edfc2ca33413257bbcc06fa58ae30ab16)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "project_id": project_id,
            "roles": roles,
        }

    @builtins.property
    def database_name(self) -> builtins.str:
        '''MongoDB Atlas database or cluster name to rotate the username and password for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#database_name VaultSecretsRotatingSecret#database_name}
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''MongoDB Atlas project ID to rotate the username and password for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#project_id VaultSecretsRotatingSecret#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def roles(self) -> typing.List[builtins.str]:
        '''MongoDB Atlas roles to assign to the rotating user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_rotating_secret#roles VaultSecretsRotatingSecret#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsRotatingSecretMongodbAtlasUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsRotatingSecretMongodbAtlasUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretMongodbAtlasUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6afd9905b606b1b85a3d38c1a91207ef4d80d0457881caffaf780f01a89bcad5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b77cf62db09a5b00ee108561285696c198061069ac98d54dc904dac9b9c08a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948669935eb4b7a015c66fead409c42ba0946d952054a30cfed8f56ce941b5ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df0825350a6a55f3ce168fdca9d7570b37d4aa798c29a5ceee255e45becb1af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretMongodbAtlasUser]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretMongodbAtlasUser]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretMongodbAtlasUser]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd268cd715f1d9fbda886160f7d07eafacece51f7e1a48f2049d346313fb7725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretTwilioApiKey",
    jsii_struct_bases=[],
    name_mapping={},
)
class VaultSecretsRotatingSecretTwilioApiKey:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsRotatingSecretTwilioApiKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsRotatingSecretTwilioApiKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsRotatingSecret.VaultSecretsRotatingSecretTwilioApiKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c542da3b9d902b8a7dbbcc7b1d8f9997196323da5379daf654cf4841d260e35f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretTwilioApiKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretTwilioApiKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretTwilioApiKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4b615860b382899640a33eb60cb09f7efc756205323e646000db8d61dc821f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VaultSecretsRotatingSecret",
    "VaultSecretsRotatingSecretAwsAccessKeys",
    "VaultSecretsRotatingSecretAwsAccessKeysOutputReference",
    "VaultSecretsRotatingSecretAzureApplicationPassword",
    "VaultSecretsRotatingSecretAzureApplicationPasswordOutputReference",
    "VaultSecretsRotatingSecretConfig",
    "VaultSecretsRotatingSecretConfluentServiceAccount",
    "VaultSecretsRotatingSecretConfluentServiceAccountOutputReference",
    "VaultSecretsRotatingSecretGcpServiceAccountKey",
    "VaultSecretsRotatingSecretGcpServiceAccountKeyOutputReference",
    "VaultSecretsRotatingSecretMongodbAtlasUser",
    "VaultSecretsRotatingSecretMongodbAtlasUserOutputReference",
    "VaultSecretsRotatingSecretTwilioApiKey",
    "VaultSecretsRotatingSecretTwilioApiKeyOutputReference",
]

publication.publish()

def _typecheckingstub__5ec6532dc85e8c9a5219edbee934665fcd4a46eb79216eff7c5ca31773872085(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_name: builtins.str,
    integration_name: builtins.str,
    name: builtins.str,
    rotation_policy_name: builtins.str,
    secret_provider: builtins.str,
    aws_access_keys: typing.Optional[typing.Union[VaultSecretsRotatingSecretAwsAccessKeys, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_application_password: typing.Optional[typing.Union[VaultSecretsRotatingSecretAzureApplicationPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    confluent_service_account: typing.Optional[typing.Union[VaultSecretsRotatingSecretConfluentServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    gcp_service_account_key: typing.Optional[typing.Union[VaultSecretsRotatingSecretGcpServiceAccountKey, typing.Dict[builtins.str, typing.Any]]] = None,
    mongodb_atlas_user: typing.Optional[typing.Union[VaultSecretsRotatingSecretMongodbAtlasUser, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    twilio_api_key: typing.Optional[typing.Union[VaultSecretsRotatingSecretTwilioApiKey, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__47b6ad29897b9f7701354369e5ef5e61d5e48fccdfdf42edbe71ae7f44ade1ec(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6a59417fd0347239ea9b769fda1cddcc6df1c5a8854f9f276cadfb78c95b1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca99b61e7d88f6c15d9727f38bf62d5c37fc40aec4af6f4384d02d556826eb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e19ffcf4a1d7deabcfca054ae0b3c4e33fa809877709e95ff6fb320b91c4087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf17e38aa728ae2447cccf6b4056e84f056ddce7041ed2c94539e30eba49625(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c78775b2c443915b327cf0813b1bd9e38d85964a4f7b71c38b26e9890b620f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4efedcb236b22468fe2cea5a009d9f8e57ca6338ad01b7fe4d327a0d009286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808741ffffe717c6429bde4c9af942b56b0efa06c0f61760e87121d4362cfb7d(
    *,
    iam_username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fdec798989335bfb16596e68e140971390f18723c9913b0681d56572100351(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0996733eaf40f142da865e9e0fd0e735f51849bad89d620bb486c2dd903f3af6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1567ecbfc0764bc9927f1e94a79aeaa1cca420aebb770f5595a226e8477bc7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretAwsAccessKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb097111b8bcc3a0b185863fa3eeeb70fdbe003d9021d0ca061672a82850b27(
    *,
    app_client_id: builtins.str,
    app_object_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0552b65c7d4170341208bde6db1b9c280069b6d10f68ed34c9b9870114d61796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b299d8374eb52c808c573cef922c9f4bfb5c149ffb41b065c0c4500f0f73ba3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdd411cb9b3027d53e3fe28bf8f08897ad2633b04b5c7a69fd9dcbde3ae1a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07d0787fd8c9598849e092d0a11752f0049692900610d4be321be6627bbae0b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretAzureApplicationPassword]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997d0111db41a34ec4ab3e2172e798abbb22286f43d57eaf9e4dfd104b5aa13a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_name: builtins.str,
    integration_name: builtins.str,
    name: builtins.str,
    rotation_policy_name: builtins.str,
    secret_provider: builtins.str,
    aws_access_keys: typing.Optional[typing.Union[VaultSecretsRotatingSecretAwsAccessKeys, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_application_password: typing.Optional[typing.Union[VaultSecretsRotatingSecretAzureApplicationPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    confluent_service_account: typing.Optional[typing.Union[VaultSecretsRotatingSecretConfluentServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    gcp_service_account_key: typing.Optional[typing.Union[VaultSecretsRotatingSecretGcpServiceAccountKey, typing.Dict[builtins.str, typing.Any]]] = None,
    mongodb_atlas_user: typing.Optional[typing.Union[VaultSecretsRotatingSecretMongodbAtlasUser, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    twilio_api_key: typing.Optional[typing.Union[VaultSecretsRotatingSecretTwilioApiKey, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296cc033573dfc49f86902f6d43667db66162f0b28ca5347eeb73e8eb55703cb(
    *,
    service_account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0914d4a2c0f828faa0804507c14db928967dd1d2dab58661503084eed543372(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac1316a001c7ef1b4b0c271ed89623a08ba77576c009b0b64d08b07d70f447b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0155863efe01606072cede817b5c3cf9871643014da7bc6d21756cd152a09207(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretConfluentServiceAccount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec31f51905b9be9eb9f20ed08367ba3713f52764254f2f1ff0eaf0bb7b8d6209(
    *,
    service_account_email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7a42485a9fd547de0331cee9613677045b3405914b0f62f0d77058fd296d71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1209f0c459ac70073bb408261533108b68befa6805bb82fc792e0ffbad5616eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bc25eee53f4e54cafd229758dddf41e39c1cfc2841f250c60450e981d18884(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretGcpServiceAccountKey]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe05bcc2cf91feb767a6b58ac86aa2edfc2ca33413257bbcc06fa58ae30ab16(
    *,
    database_name: builtins.str,
    project_id: builtins.str,
    roles: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6afd9905b606b1b85a3d38c1a91207ef4d80d0457881caffaf780f01a89bcad5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b77cf62db09a5b00ee108561285696c198061069ac98d54dc904dac9b9c08a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948669935eb4b7a015c66fead409c42ba0946d952054a30cfed8f56ce941b5ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df0825350a6a55f3ce168fdca9d7570b37d4aa798c29a5ceee255e45becb1af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd268cd715f1d9fbda886160f7d07eafacece51f7e1a48f2049d346313fb7725(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretMongodbAtlasUser]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c542da3b9d902b8a7dbbcc7b1d8f9997196323da5379daf654cf4841d260e35f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4b615860b382899640a33eb60cb09f7efc756205323e646000db8d61dc821f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsRotatingSecretTwilioApiKey]],
) -> None:
    """Type checking stubs"""
    pass
