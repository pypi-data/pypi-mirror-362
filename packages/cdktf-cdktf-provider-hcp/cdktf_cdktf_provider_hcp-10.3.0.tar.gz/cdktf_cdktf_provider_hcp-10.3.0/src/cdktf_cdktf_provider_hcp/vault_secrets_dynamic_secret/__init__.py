r'''
# `hcp_vault_secrets_dynamic_secret`

Refer to the Terraform Registry for docs: [`hcp_vault_secrets_dynamic_secret`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret).
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


class VaultSecretsDynamicSecret(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsDynamicSecret.VaultSecretsDynamicSecret",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret hcp_vault_secrets_dynamic_secret}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_name: builtins.str,
        integration_name: builtins.str,
        name: builtins.str,
        secret_provider: builtins.str,
        aws_assume_role: typing.Optional[typing.Union["VaultSecretsDynamicSecretAwsAssumeRole", typing.Dict[builtins.str, typing.Any]]] = None,
        default_ttl: typing.Optional[builtins.str] = None,
        gcp_impersonate_service_account: typing.Optional[typing.Union["VaultSecretsDynamicSecretGcpImpersonateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret hcp_vault_secrets_dynamic_secret} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_name: Vault Secrets application name that owns the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#app_name VaultSecretsDynamicSecret#app_name}
        :param integration_name: The Vault Secrets integration name with the capability to manage the secret's lifecycle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#integration_name VaultSecretsDynamicSecret#integration_name}
        :param name: The Vault Secrets secret name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#name VaultSecretsDynamicSecret#name}
        :param secret_provider: The third party platform the dynamic credentials give access to. One of ``aws`` or ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#secret_provider VaultSecretsDynamicSecret#secret_provider}
        :param aws_assume_role: AWS configuration to generate dynamic credentials by assuming an IAM role. Required if ``secret_provider`` is ``aws``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#aws_assume_role VaultSecretsDynamicSecret#aws_assume_role}
        :param default_ttl: TTL the generated credentials will be valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#default_ttl VaultSecretsDynamicSecret#default_ttl}
        :param gcp_impersonate_service_account: GCP configuration to generate dynamic credentials by impersonating a service account. Required if ``secret_provider`` is ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#gcp_impersonate_service_account VaultSecretsDynamicSecret#gcp_impersonate_service_account}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#project_id VaultSecretsDynamicSecret#project_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1bb63ddd14fa8759f99da85910c7666f76e84eb051813ddba540f08118438c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = VaultSecretsDynamicSecretConfig(
            app_name=app_name,
            integration_name=integration_name,
            name=name,
            secret_provider=secret_provider,
            aws_assume_role=aws_assume_role,
            default_ttl=default_ttl,
            gcp_impersonate_service_account=gcp_impersonate_service_account,
            project_id=project_id,
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
        '''Generates CDKTF code for importing a VaultSecretsDynamicSecret resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VaultSecretsDynamicSecret to import.
        :param import_from_id: The id of the existing VaultSecretsDynamicSecret that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VaultSecretsDynamicSecret to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3bf551baa977bf625db0f08c79a869ce7e3288ba4fd02c7d982d7eefc2e6fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAwsAssumeRole")
    def put_aws_assume_role(self, *, iam_role_arn: builtins.str) -> None:
        '''
        :param iam_role_arn: AWS IAM role ARN to assume when generating credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#iam_role_arn VaultSecretsDynamicSecret#iam_role_arn}
        '''
        value = VaultSecretsDynamicSecretAwsAssumeRole(iam_role_arn=iam_role_arn)

        return typing.cast(None, jsii.invoke(self, "putAwsAssumeRole", [value]))

    @jsii.member(jsii_name="putGcpImpersonateServiceAccount")
    def put_gcp_impersonate_service_account(
        self,
        *,
        service_account_email: builtins.str,
    ) -> None:
        '''
        :param service_account_email: GCP service account email to impersonate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#service_account_email VaultSecretsDynamicSecret#service_account_email}
        '''
        value = VaultSecretsDynamicSecretGcpImpersonateServiceAccount(
            service_account_email=service_account_email
        )

        return typing.cast(None, jsii.invoke(self, "putGcpImpersonateServiceAccount", [value]))

    @jsii.member(jsii_name="resetAwsAssumeRole")
    def reset_aws_assume_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAssumeRole", []))

    @jsii.member(jsii_name="resetDefaultTtl")
    def reset_default_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTtl", []))

    @jsii.member(jsii_name="resetGcpImpersonateServiceAccount")
    def reset_gcp_impersonate_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpImpersonateServiceAccount", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

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
    @jsii.member(jsii_name="awsAssumeRole")
    def aws_assume_role(
        self,
    ) -> "VaultSecretsDynamicSecretAwsAssumeRoleOutputReference":
        return typing.cast("VaultSecretsDynamicSecretAwsAssumeRoleOutputReference", jsii.get(self, "awsAssumeRole"))

    @builtins.property
    @jsii.member(jsii_name="gcpImpersonateServiceAccount")
    def gcp_impersonate_service_account(
        self,
    ) -> "VaultSecretsDynamicSecretGcpImpersonateServiceAccountOutputReference":
        return typing.cast("VaultSecretsDynamicSecretGcpImpersonateServiceAccountOutputReference", jsii.get(self, "gcpImpersonateServiceAccount"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="appNameInput")
    def app_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appNameInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAssumeRoleInput")
    def aws_assume_role_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsDynamicSecretAwsAssumeRole"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsDynamicSecretAwsAssumeRole"]], jsii.get(self, "awsAssumeRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTtlInput")
    def default_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpImpersonateServiceAccountInput")
    def gcp_impersonate_service_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsDynamicSecretGcpImpersonateServiceAccount"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsDynamicSecretGcpImpersonateServiceAccount"]], jsii.get(self, "gcpImpersonateServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationNameInput")
    def integration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretProviderInput")
    def secret_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="appName")
    def app_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appName"))

    @app_name.setter
    def app_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fee3f2e95be7a7b0f6166c54ca2504cc3e8386969d317b6eaaddea1d0ba5b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea727f2742d79f7ca8244def69f7d40f77cad816d824f6ca95e3ad7ced80f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationName")
    def integration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationName"))

    @integration_name.setter
    def integration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bad11b0d547a9ee8da094cc45692b8617067362d4e254bb21a3f56eb44eb1d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a465ce359bb3fce8285c0743fa6a43bd490633d8244ce580484cbe7b7baacbf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921441da9bf4603a976c1f5b4bd1837e484e31beb817abc480cbc26552b035fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretProvider")
    def secret_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretProvider"))

    @secret_provider.setter
    def secret_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6286ab96b7edc895e66bb9efaad960f98e6c0d61e69df61be067984ad9f0dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretProvider", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsDynamicSecret.VaultSecretsDynamicSecretAwsAssumeRole",
    jsii_struct_bases=[],
    name_mapping={"iam_role_arn": "iamRoleArn"},
)
class VaultSecretsDynamicSecretAwsAssumeRole:
    def __init__(self, *, iam_role_arn: builtins.str) -> None:
        '''
        :param iam_role_arn: AWS IAM role ARN to assume when generating credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#iam_role_arn VaultSecretsDynamicSecret#iam_role_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18bc80dd6de0fb2c16bd225f920042a171cbcc6823d24c70ff8157ee02cf1030)
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iam_role_arn": iam_role_arn,
        }

    @builtins.property
    def iam_role_arn(self) -> builtins.str:
        '''AWS IAM role ARN to assume when generating credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#iam_role_arn VaultSecretsDynamicSecret#iam_role_arn}
        '''
        result = self._values.get("iam_role_arn")
        assert result is not None, "Required property 'iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsDynamicSecretAwsAssumeRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsDynamicSecretAwsAssumeRoleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsDynamicSecret.VaultSecretsDynamicSecretAwsAssumeRoleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fcd9827454b1e432cfbf93507daac1407b3d4802e05eadf6d723a8014442dee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="iamRoleArnInput")
    def iam_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145428732d916407dcc55608e8d7ee0a49ef1965a846f843a49595441cfd0fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsDynamicSecretAwsAssumeRole]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsDynamicSecretAwsAssumeRole]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsDynamicSecretAwsAssumeRole]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b25f340f6cef3b2d07495afb54a8b176bbb75757c6ab27e681a22f221b67d8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsDynamicSecret.VaultSecretsDynamicSecretConfig",
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
        "secret_provider": "secretProvider",
        "aws_assume_role": "awsAssumeRole",
        "default_ttl": "defaultTtl",
        "gcp_impersonate_service_account": "gcpImpersonateServiceAccount",
        "project_id": "projectId",
    },
)
class VaultSecretsDynamicSecretConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        secret_provider: builtins.str,
        aws_assume_role: typing.Optional[typing.Union[VaultSecretsDynamicSecretAwsAssumeRole, typing.Dict[builtins.str, typing.Any]]] = None,
        default_ttl: typing.Optional[builtins.str] = None,
        gcp_impersonate_service_account: typing.Optional[typing.Union["VaultSecretsDynamicSecretGcpImpersonateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_name: Vault Secrets application name that owns the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#app_name VaultSecretsDynamicSecret#app_name}
        :param integration_name: The Vault Secrets integration name with the capability to manage the secret's lifecycle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#integration_name VaultSecretsDynamicSecret#integration_name}
        :param name: The Vault Secrets secret name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#name VaultSecretsDynamicSecret#name}
        :param secret_provider: The third party platform the dynamic credentials give access to. One of ``aws`` or ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#secret_provider VaultSecretsDynamicSecret#secret_provider}
        :param aws_assume_role: AWS configuration to generate dynamic credentials by assuming an IAM role. Required if ``secret_provider`` is ``aws``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#aws_assume_role VaultSecretsDynamicSecret#aws_assume_role}
        :param default_ttl: TTL the generated credentials will be valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#default_ttl VaultSecretsDynamicSecret#default_ttl}
        :param gcp_impersonate_service_account: GCP configuration to generate dynamic credentials by impersonating a service account. Required if ``secret_provider`` is ``gcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#gcp_impersonate_service_account VaultSecretsDynamicSecret#gcp_impersonate_service_account}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#project_id VaultSecretsDynamicSecret#project_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws_assume_role, dict):
            aws_assume_role = VaultSecretsDynamicSecretAwsAssumeRole(**aws_assume_role)
        if isinstance(gcp_impersonate_service_account, dict):
            gcp_impersonate_service_account = VaultSecretsDynamicSecretGcpImpersonateServiceAccount(**gcp_impersonate_service_account)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8658ef12a350e7b3860793e8ad1839731f4fcd69ac10ece1fa057c0b89fc76)
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
            check_type(argname="argument secret_provider", value=secret_provider, expected_type=type_hints["secret_provider"])
            check_type(argname="argument aws_assume_role", value=aws_assume_role, expected_type=type_hints["aws_assume_role"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument gcp_impersonate_service_account", value=gcp_impersonate_service_account, expected_type=type_hints["gcp_impersonate_service_account"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_name": app_name,
            "integration_name": integration_name,
            "name": name,
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
        if aws_assume_role is not None:
            self._values["aws_assume_role"] = aws_assume_role
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if gcp_impersonate_service_account is not None:
            self._values["gcp_impersonate_service_account"] = gcp_impersonate_service_account
        if project_id is not None:
            self._values["project_id"] = project_id

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#app_name VaultSecretsDynamicSecret#app_name}
        '''
        result = self._values.get("app_name")
        assert result is not None, "Required property 'app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_name(self) -> builtins.str:
        '''The Vault Secrets integration name with the capability to manage the secret's lifecycle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#integration_name VaultSecretsDynamicSecret#integration_name}
        '''
        result = self._values.get("integration_name")
        assert result is not None, "Required property 'integration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The Vault Secrets secret name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#name VaultSecretsDynamicSecret#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_provider(self) -> builtins.str:
        '''The third party platform the dynamic credentials give access to. One of ``aws`` or ``gcp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#secret_provider VaultSecretsDynamicSecret#secret_provider}
        '''
        result = self._values.get("secret_provider")
        assert result is not None, "Required property 'secret_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_assume_role(
        self,
    ) -> typing.Optional[VaultSecretsDynamicSecretAwsAssumeRole]:
        '''AWS configuration to generate dynamic credentials by assuming an IAM role. Required if ``secret_provider`` is ``aws``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#aws_assume_role VaultSecretsDynamicSecret#aws_assume_role}
        '''
        result = self._values.get("aws_assume_role")
        return typing.cast(typing.Optional[VaultSecretsDynamicSecretAwsAssumeRole], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[builtins.str]:
        '''TTL the generated credentials will be valid for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#default_ttl VaultSecretsDynamicSecret#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_impersonate_service_account(
        self,
    ) -> typing.Optional["VaultSecretsDynamicSecretGcpImpersonateServiceAccount"]:
        '''GCP configuration to generate dynamic credentials by impersonating a service account. Required if ``secret_provider`` is ``gcp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#gcp_impersonate_service_account VaultSecretsDynamicSecret#gcp_impersonate_service_account}
        '''
        result = self._values.get("gcp_impersonate_service_account")
        return typing.cast(typing.Optional["VaultSecretsDynamicSecretGcpImpersonateServiceAccount"], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#project_id VaultSecretsDynamicSecret#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsDynamicSecretConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsDynamicSecret.VaultSecretsDynamicSecretGcpImpersonateServiceAccount",
    jsii_struct_bases=[],
    name_mapping={"service_account_email": "serviceAccountEmail"},
)
class VaultSecretsDynamicSecretGcpImpersonateServiceAccount:
    def __init__(self, *, service_account_email: builtins.str) -> None:
        '''
        :param service_account_email: GCP service account email to impersonate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#service_account_email VaultSecretsDynamicSecret#service_account_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f951a3012504e29a4d6a7e677d0b585bb74ec5c71077b5a1c46285ad683b631)
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account_email": service_account_email,
        }

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''GCP service account email to impersonate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_dynamic_secret#service_account_email VaultSecretsDynamicSecret#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsDynamicSecretGcpImpersonateServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsDynamicSecretGcpImpersonateServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsDynamicSecret.VaultSecretsDynamicSecretGcpImpersonateServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d0c30e0a56b6fdb0bc249426f0482012f446db64d76c8270f0447c50a0dca8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ca42e271f46a7b20f7432c33b941f2eb81dc6c1231fd3edf6ce6c05f97f40f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsDynamicSecretGcpImpersonateServiceAccount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsDynamicSecretGcpImpersonateServiceAccount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsDynamicSecretGcpImpersonateServiceAccount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cdec7d5046d4cc1d496734b18aa2dca9be2b6e067f359e776bea2a6b8bce07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VaultSecretsDynamicSecret",
    "VaultSecretsDynamicSecretAwsAssumeRole",
    "VaultSecretsDynamicSecretAwsAssumeRoleOutputReference",
    "VaultSecretsDynamicSecretConfig",
    "VaultSecretsDynamicSecretGcpImpersonateServiceAccount",
    "VaultSecretsDynamicSecretGcpImpersonateServiceAccountOutputReference",
]

publication.publish()

def _typecheckingstub__ad1bb63ddd14fa8759f99da85910c7666f76e84eb051813ddba540f08118438c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_name: builtins.str,
    integration_name: builtins.str,
    name: builtins.str,
    secret_provider: builtins.str,
    aws_assume_role: typing.Optional[typing.Union[VaultSecretsDynamicSecretAwsAssumeRole, typing.Dict[builtins.str, typing.Any]]] = None,
    default_ttl: typing.Optional[builtins.str] = None,
    gcp_impersonate_service_account: typing.Optional[typing.Union[VaultSecretsDynamicSecretGcpImpersonateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ba3bf551baa977bf625db0f08c79a869ce7e3288ba4fd02c7d982d7eefc2e6fc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fee3f2e95be7a7b0f6166c54ca2504cc3e8386969d317b6eaaddea1d0ba5b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea727f2742d79f7ca8244def69f7d40f77cad816d824f6ca95e3ad7ced80f31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bad11b0d547a9ee8da094cc45692b8617067362d4e254bb21a3f56eb44eb1d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a465ce359bb3fce8285c0743fa6a43bd490633d8244ce580484cbe7b7baacbf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921441da9bf4603a976c1f5b4bd1837e484e31beb817abc480cbc26552b035fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6286ab96b7edc895e66bb9efaad960f98e6c0d61e69df61be067984ad9f0dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bc80dd6de0fb2c16bd225f920042a171cbcc6823d24c70ff8157ee02cf1030(
    *,
    iam_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcd9827454b1e432cfbf93507daac1407b3d4802e05eadf6d723a8014442dee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145428732d916407dcc55608e8d7ee0a49ef1965a846f843a49595441cfd0fa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b25f340f6cef3b2d07495afb54a8b176bbb75757c6ab27e681a22f221b67d8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsDynamicSecretAwsAssumeRole]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8658ef12a350e7b3860793e8ad1839731f4fcd69ac10ece1fa057c0b89fc76(
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
    secret_provider: builtins.str,
    aws_assume_role: typing.Optional[typing.Union[VaultSecretsDynamicSecretAwsAssumeRole, typing.Dict[builtins.str, typing.Any]]] = None,
    default_ttl: typing.Optional[builtins.str] = None,
    gcp_impersonate_service_account: typing.Optional[typing.Union[VaultSecretsDynamicSecretGcpImpersonateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f951a3012504e29a4d6a7e677d0b585bb74ec5c71077b5a1c46285ad683b631(
    *,
    service_account_email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0c30e0a56b6fdb0bc249426f0482012f446db64d76c8270f0447c50a0dca8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca42e271f46a7b20f7432c33b941f2eb81dc6c1231fd3edf6ce6c05f97f40f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cdec7d5046d4cc1d496734b18aa2dca9be2b6e067f359e776bea2a6b8bce07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsDynamicSecretGcpImpersonateServiceAccount]],
) -> None:
    """Type checking stubs"""
    pass
