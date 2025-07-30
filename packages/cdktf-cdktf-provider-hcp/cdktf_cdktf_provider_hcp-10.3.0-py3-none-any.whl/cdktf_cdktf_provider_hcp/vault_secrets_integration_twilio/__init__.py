r'''
# `hcp_vault_secrets_integration_twilio`

Refer to the Terraform Registry for docs: [`hcp_vault_secrets_integration_twilio`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio).
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


class VaultSecretsIntegrationTwilio(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationTwilio.VaultSecretsIntegrationTwilio",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio hcp_vault_secrets_integration_twilio}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        capabilities: typing.Sequence[builtins.str],
        name: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
        static_credential_details: typing.Optional[typing.Union["VaultSecretsIntegrationTwilioStaticCredentialDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio hcp_vault_secrets_integration_twilio} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capabilities: Capabilities enabled for the integration. See the Vault Secrets documentation for the list of supported capabilities per provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#capabilities VaultSecretsIntegrationTwilio#capabilities}
        :param name: The Vault Secrets integration name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#name VaultSecretsIntegrationTwilio#name}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#project_id VaultSecretsIntegrationTwilio#project_id}
        :param static_credential_details: Twilio API key parts used to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#static_credential_details VaultSecretsIntegrationTwilio#static_credential_details}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ac99521f2a7b691a66ba3bc428a6deb0eafb28445ab6d5e376df2824a201e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = VaultSecretsIntegrationTwilioConfig(
            capabilities=capabilities,
            name=name,
            project_id=project_id,
            static_credential_details=static_credential_details,
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
        '''Generates CDKTF code for importing a VaultSecretsIntegrationTwilio resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VaultSecretsIntegrationTwilio to import.
        :param import_from_id: The id of the existing VaultSecretsIntegrationTwilio that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VaultSecretsIntegrationTwilio to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb747a53498aae27282638176b9fc883b2e977fb84c2f1c4ea3835e5023ab41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStaticCredentialDetails")
    def put_static_credential_details(
        self,
        *,
        account_sid: builtins.str,
        api_key_secret: builtins.str,
        api_key_sid: builtins.str,
    ) -> None:
        '''
        :param account_sid: Account SID for the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#account_sid VaultSecretsIntegrationTwilio#account_sid}
        :param api_key_secret: Api key secret used with the api key SID to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#api_key_secret VaultSecretsIntegrationTwilio#api_key_secret}
        :param api_key_sid: Api key SID to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#api_key_sid VaultSecretsIntegrationTwilio#api_key_sid}
        '''
        value = VaultSecretsIntegrationTwilioStaticCredentialDetails(
            account_sid=account_sid,
            api_key_secret=api_key_secret,
            api_key_sid=api_key_sid,
        )

        return typing.cast(None, jsii.invoke(self, "putStaticCredentialDetails", [value]))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetStaticCredentialDetails")
    def reset_static_credential_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticCredentialDetails", []))

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
    @jsii.member(jsii_name="staticCredentialDetails")
    def static_credential_details(
        self,
    ) -> "VaultSecretsIntegrationTwilioStaticCredentialDetailsOutputReference":
        return typing.cast("VaultSecretsIntegrationTwilioStaticCredentialDetailsOutputReference", jsii.get(self, "staticCredentialDetails"))

    @builtins.property
    @jsii.member(jsii_name="capabilitiesInput")
    def capabilities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="staticCredentialDetailsInput")
    def static_credential_details_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationTwilioStaticCredentialDetails"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationTwilioStaticCredentialDetails"]], jsii.get(self, "staticCredentialDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "capabilities"))

    @capabilities.setter
    def capabilities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d319a9de7e46a25125fc5eb22a8b84d8e80bc7f25fb6652f0f2a1f21f282d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capabilities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26f301e64c4ad29f35866e1346d77a505d435bef970c4a03b24ac2132a16bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c402d2b95af43dfc02ec6e72dab9bcf2f190150c90c15d60639debbce9d0ab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationTwilio.VaultSecretsIntegrationTwilioConfig",
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
        "project_id": "projectId",
        "static_credential_details": "staticCredentialDetails",
    },
)
class VaultSecretsIntegrationTwilioConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        project_id: typing.Optional[builtins.str] = None,
        static_credential_details: typing.Optional[typing.Union["VaultSecretsIntegrationTwilioStaticCredentialDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capabilities: Capabilities enabled for the integration. See the Vault Secrets documentation for the list of supported capabilities per provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#capabilities VaultSecretsIntegrationTwilio#capabilities}
        :param name: The Vault Secrets integration name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#name VaultSecretsIntegrationTwilio#name}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#project_id VaultSecretsIntegrationTwilio#project_id}
        :param static_credential_details: Twilio API key parts used to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#static_credential_details VaultSecretsIntegrationTwilio#static_credential_details}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(static_credential_details, dict):
            static_credential_details = VaultSecretsIntegrationTwilioStaticCredentialDetails(**static_credential_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1affd0e981c24b70569953f3942c09757604f71cbcef5cebdcd1f02370a203)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument static_credential_details", value=static_credential_details, expected_type=type_hints["static_credential_details"])
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
        if project_id is not None:
            self._values["project_id"] = project_id
        if static_credential_details is not None:
            self._values["static_credential_details"] = static_credential_details

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#capabilities VaultSecretsIntegrationTwilio#capabilities}
        '''
        result = self._values.get("capabilities")
        assert result is not None, "Required property 'capabilities' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The Vault Secrets integration name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#name VaultSecretsIntegrationTwilio#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#project_id VaultSecretsIntegrationTwilio#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_credential_details(
        self,
    ) -> typing.Optional["VaultSecretsIntegrationTwilioStaticCredentialDetails"]:
        '''Twilio API key parts used to authenticate against the target Twilio account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#static_credential_details VaultSecretsIntegrationTwilio#static_credential_details}
        '''
        result = self._values.get("static_credential_details")
        return typing.cast(typing.Optional["VaultSecretsIntegrationTwilioStaticCredentialDetails"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationTwilioConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationTwilio.VaultSecretsIntegrationTwilioStaticCredentialDetails",
    jsii_struct_bases=[],
    name_mapping={
        "account_sid": "accountSid",
        "api_key_secret": "apiKeySecret",
        "api_key_sid": "apiKeySid",
    },
)
class VaultSecretsIntegrationTwilioStaticCredentialDetails:
    def __init__(
        self,
        *,
        account_sid: builtins.str,
        api_key_secret: builtins.str,
        api_key_sid: builtins.str,
    ) -> None:
        '''
        :param account_sid: Account SID for the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#account_sid VaultSecretsIntegrationTwilio#account_sid}
        :param api_key_secret: Api key secret used with the api key SID to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#api_key_secret VaultSecretsIntegrationTwilio#api_key_secret}
        :param api_key_sid: Api key SID to authenticate against the target Twilio account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#api_key_sid VaultSecretsIntegrationTwilio#api_key_sid}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdae9947765fbb063f1ba9adf88788605e7b9e2a51e160170dba2a3afdca7114)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#account_sid VaultSecretsIntegrationTwilio#account_sid}
        '''
        result = self._values.get("account_sid")
        assert result is not None, "Required property 'account_sid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_secret(self) -> builtins.str:
        '''Api key secret used with the api key SID to authenticate against the target Twilio account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#api_key_secret VaultSecretsIntegrationTwilio#api_key_secret}
        '''
        result = self._values.get("api_key_secret")
        assert result is not None, "Required property 'api_key_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_sid(self) -> builtins.str:
        '''Api key SID to authenticate against the target Twilio account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_twilio#api_key_sid VaultSecretsIntegrationTwilio#api_key_sid}
        '''
        result = self._values.get("api_key_sid")
        assert result is not None, "Required property 'api_key_sid' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationTwilioStaticCredentialDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationTwilioStaticCredentialDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationTwilio.VaultSecretsIntegrationTwilioStaticCredentialDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee20c54375d8da584d21e1e80caafe1438233f9b21f951e3f9c08383756ab7b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37739ad37f421271729a5e5084f779909c8e39c014a9c35900f260db0a484669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountSid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKeySecret")
    def api_key_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKeySecret"))

    @api_key_secret.setter
    def api_key_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef07845552f0c1552b10bf7786d5fda155e785fa381eb4fb55168a28c6453670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeySecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKeySid")
    def api_key_sid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKeySid"))

    @api_key_sid.setter
    def api_key_sid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b17ed156514981dd37ef2f8a813ef52514f65df32ae3d73d0fb7370ed1617f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeySid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationTwilioStaticCredentialDetails]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationTwilioStaticCredentialDetails]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationTwilioStaticCredentialDetails]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd46ad3495c640784d3a51d4c4d02c08e3e26a0bc8d70ba17d906d898bacd74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VaultSecretsIntegrationTwilio",
    "VaultSecretsIntegrationTwilioConfig",
    "VaultSecretsIntegrationTwilioStaticCredentialDetails",
    "VaultSecretsIntegrationTwilioStaticCredentialDetailsOutputReference",
]

publication.publish()

def _typecheckingstub__16ac99521f2a7b691a66ba3bc428a6deb0eafb28445ab6d5e376df2824a201e8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    capabilities: typing.Sequence[builtins.str],
    name: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
    static_credential_details: typing.Optional[typing.Union[VaultSecretsIntegrationTwilioStaticCredentialDetails, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4cb747a53498aae27282638176b9fc883b2e977fb84c2f1c4ea3835e5023ab41(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d319a9de7e46a25125fc5eb22a8b84d8e80bc7f25fb6652f0f2a1f21f282d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26f301e64c4ad29f35866e1346d77a505d435bef970c4a03b24ac2132a16bb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c402d2b95af43dfc02ec6e72dab9bcf2f190150c90c15d60639debbce9d0ab4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1affd0e981c24b70569953f3942c09757604f71cbcef5cebdcd1f02370a203(
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
    project_id: typing.Optional[builtins.str] = None,
    static_credential_details: typing.Optional[typing.Union[VaultSecretsIntegrationTwilioStaticCredentialDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdae9947765fbb063f1ba9adf88788605e7b9e2a51e160170dba2a3afdca7114(
    *,
    account_sid: builtins.str,
    api_key_secret: builtins.str,
    api_key_sid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee20c54375d8da584d21e1e80caafe1438233f9b21f951e3f9c08383756ab7b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37739ad37f421271729a5e5084f779909c8e39c014a9c35900f260db0a484669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef07845552f0c1552b10bf7786d5fda155e785fa381eb4fb55168a28c6453670(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b17ed156514981dd37ef2f8a813ef52514f65df32ae3d73d0fb7370ed1617f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd46ad3495c640784d3a51d4c4d02c08e3e26a0bc8d70ba17d906d898bacd74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationTwilioStaticCredentialDetails]],
) -> None:
    """Type checking stubs"""
    pass
