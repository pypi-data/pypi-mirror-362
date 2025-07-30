r'''
# `hcp_vault_secrets_integration_confluent`

Refer to the Terraform Registry for docs: [`hcp_vault_secrets_integration_confluent`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent).
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


class VaultSecretsIntegrationConfluent(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationConfluent.VaultSecretsIntegrationConfluent",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent hcp_vault_secrets_integration_confluent}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        capabilities: typing.Sequence[builtins.str],
        name: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
        static_credential_details: typing.Optional[typing.Union["VaultSecretsIntegrationConfluentStaticCredentialDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent hcp_vault_secrets_integration_confluent} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capabilities: Capabilities enabled for the integration. See the Vault Secrets documentation for the list of supported capabilities per provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#capabilities VaultSecretsIntegrationConfluent#capabilities}
        :param name: The Vault Secrets integration name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#name VaultSecretsIntegrationConfluent#name}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#project_id VaultSecretsIntegrationConfluent#project_id}
        :param static_credential_details: Confluent API key used to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#static_credential_details VaultSecretsIntegrationConfluent#static_credential_details}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb1708aa123376abfa2a4a3c56c3704c967969cb6df99c030f975ec15452c02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = VaultSecretsIntegrationConfluentConfig(
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
        '''Generates CDKTF code for importing a VaultSecretsIntegrationConfluent resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VaultSecretsIntegrationConfluent to import.
        :param import_from_id: The id of the existing VaultSecretsIntegrationConfluent that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VaultSecretsIntegrationConfluent to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95358f82a4c42e8a130686fc87fd560a291cf16fd341128b5fecafbc1af10703)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStaticCredentialDetails")
    def put_static_credential_details(
        self,
        *,
        cloud_api_key_id: builtins.str,
        cloud_api_secret: builtins.str,
    ) -> None:
        '''
        :param cloud_api_key_id: Public key used alongside the private key to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#cloud_api_key_id VaultSecretsIntegrationConfluent#cloud_api_key_id}
        :param cloud_api_secret: Private key used alongside the public key to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#cloud_api_secret VaultSecretsIntegrationConfluent#cloud_api_secret}
        '''
        value = VaultSecretsIntegrationConfluentStaticCredentialDetails(
            cloud_api_key_id=cloud_api_key_id, cloud_api_secret=cloud_api_secret
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
    ) -> "VaultSecretsIntegrationConfluentStaticCredentialDetailsOutputReference":
        return typing.cast("VaultSecretsIntegrationConfluentStaticCredentialDetailsOutputReference", jsii.get(self, "staticCredentialDetails"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationConfluentStaticCredentialDetails"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VaultSecretsIntegrationConfluentStaticCredentialDetails"]], jsii.get(self, "staticCredentialDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "capabilities"))

    @capabilities.setter
    def capabilities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c4e066309cc0a85ff8b93d9215cec812e83e00fb2cc5093ae71ee620ce370a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capabilities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5e4e19ce10b36d8c8296ab3f682048b47d34067b53d8e6a9f405fd5ea89313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8fdb8202fc43f4cd8784ffdd50e432779ba0408f352feb0dc69931235d1b50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationConfluent.VaultSecretsIntegrationConfluentConfig",
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
class VaultSecretsIntegrationConfluentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        static_credential_details: typing.Optional[typing.Union["VaultSecretsIntegrationConfluentStaticCredentialDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capabilities: Capabilities enabled for the integration. See the Vault Secrets documentation for the list of supported capabilities per provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#capabilities VaultSecretsIntegrationConfluent#capabilities}
        :param name: The Vault Secrets integration name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#name VaultSecretsIntegrationConfluent#name}
        :param project_id: HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#project_id VaultSecretsIntegrationConfluent#project_id}
        :param static_credential_details: Confluent API key used to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#static_credential_details VaultSecretsIntegrationConfluent#static_credential_details}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(static_credential_details, dict):
            static_credential_details = VaultSecretsIntegrationConfluentStaticCredentialDetails(**static_credential_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f173de991a5152625c9b0a959f49863830afa9de87ff53f525deedf6f762f02c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#capabilities VaultSecretsIntegrationConfluent#capabilities}
        '''
        result = self._values.get("capabilities")
        assert result is not None, "Required property 'capabilities' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The Vault Secrets integration name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#name VaultSecretsIntegrationConfluent#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''HCP project ID that owns the HCP Vault Secrets integration. Inferred from the provider configuration if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#project_id VaultSecretsIntegrationConfluent#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_credential_details(
        self,
    ) -> typing.Optional["VaultSecretsIntegrationConfluentStaticCredentialDetails"]:
        '''Confluent API key used to authenticate for cloud apis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#static_credential_details VaultSecretsIntegrationConfluent#static_credential_details}
        '''
        result = self._values.get("static_credential_details")
        return typing.cast(typing.Optional["VaultSecretsIntegrationConfluentStaticCredentialDetails"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationConfluentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationConfluent.VaultSecretsIntegrationConfluentStaticCredentialDetails",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_api_key_id": "cloudApiKeyId",
        "cloud_api_secret": "cloudApiSecret",
    },
)
class VaultSecretsIntegrationConfluentStaticCredentialDetails:
    def __init__(
        self,
        *,
        cloud_api_key_id: builtins.str,
        cloud_api_secret: builtins.str,
    ) -> None:
        '''
        :param cloud_api_key_id: Public key used alongside the private key to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#cloud_api_key_id VaultSecretsIntegrationConfluent#cloud_api_key_id}
        :param cloud_api_secret: Private key used alongside the public key to authenticate for cloud apis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#cloud_api_secret VaultSecretsIntegrationConfluent#cloud_api_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b881c29d28224de26f664b7a2188372a804971eea8e4f1afcc4704e3226e92)
            check_type(argname="argument cloud_api_key_id", value=cloud_api_key_id, expected_type=type_hints["cloud_api_key_id"])
            check_type(argname="argument cloud_api_secret", value=cloud_api_secret, expected_type=type_hints["cloud_api_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_api_key_id": cloud_api_key_id,
            "cloud_api_secret": cloud_api_secret,
        }

    @builtins.property
    def cloud_api_key_id(self) -> builtins.str:
        '''Public key used alongside the private key to authenticate for cloud apis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#cloud_api_key_id VaultSecretsIntegrationConfluent#cloud_api_key_id}
        '''
        result = self._values.get("cloud_api_key_id")
        assert result is not None, "Required property 'cloud_api_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_api_secret(self) -> builtins.str:
        '''Private key used alongside the public key to authenticate for cloud apis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/vault_secrets_integration_confluent#cloud_api_secret VaultSecretsIntegrationConfluent#cloud_api_secret}
        '''
        result = self._values.get("cloud_api_secret")
        assert result is not None, "Required property 'cloud_api_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultSecretsIntegrationConfluentStaticCredentialDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VaultSecretsIntegrationConfluentStaticCredentialDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.vaultSecretsIntegrationConfluent.VaultSecretsIntegrationConfluentStaticCredentialDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b702d7baf6acc276d82092616aa6e0118919814f2905783d735370c04956d5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f08c415780aead24f37c15be4483f32182ba8d38949019ed7102d200f2c34ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudApiKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudApiSecret")
    def cloud_api_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudApiSecret"))

    @cloud_api_secret.setter
    def cloud_api_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbbc89451dbb48df23e6e4149290d2dd61a09173b47c807bbd146924a2aff1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudApiSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationConfluentStaticCredentialDetails]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationConfluentStaticCredentialDetails]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationConfluentStaticCredentialDetails]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a822f9ee52414e481d9fcef7a20707249cddd48ce014dc4678d8d6d1e8cacf0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VaultSecretsIntegrationConfluent",
    "VaultSecretsIntegrationConfluentConfig",
    "VaultSecretsIntegrationConfluentStaticCredentialDetails",
    "VaultSecretsIntegrationConfluentStaticCredentialDetailsOutputReference",
]

publication.publish()

def _typecheckingstub__3cb1708aa123376abfa2a4a3c56c3704c967969cb6df99c030f975ec15452c02(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    capabilities: typing.Sequence[builtins.str],
    name: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
    static_credential_details: typing.Optional[typing.Union[VaultSecretsIntegrationConfluentStaticCredentialDetails, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__95358f82a4c42e8a130686fc87fd560a291cf16fd341128b5fecafbc1af10703(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c4e066309cc0a85ff8b93d9215cec812e83e00fb2cc5093ae71ee620ce370a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5e4e19ce10b36d8c8296ab3f682048b47d34067b53d8e6a9f405fd5ea89313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8fdb8202fc43f4cd8784ffdd50e432779ba0408f352feb0dc69931235d1b50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f173de991a5152625c9b0a959f49863830afa9de87ff53f525deedf6f762f02c(
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
    static_credential_details: typing.Optional[typing.Union[VaultSecretsIntegrationConfluentStaticCredentialDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b881c29d28224de26f664b7a2188372a804971eea8e4f1afcc4704e3226e92(
    *,
    cloud_api_key_id: builtins.str,
    cloud_api_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b702d7baf6acc276d82092616aa6e0118919814f2905783d735370c04956d5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08c415780aead24f37c15be4483f32182ba8d38949019ed7102d200f2c34ee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbbc89451dbb48df23e6e4149290d2dd61a09173b47c807bbd146924a2aff1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a822f9ee52414e481d9fcef7a20707249cddd48ce014dc4678d8d6d1e8cacf0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VaultSecretsIntegrationConfluentStaticCredentialDetails]],
) -> None:
    """Type checking stubs"""
    pass
