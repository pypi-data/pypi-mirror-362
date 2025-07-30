r'''
# `provider`

Refer to the Terraform Registry for docs: [`hcp`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs).
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


class HcpProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.provider.HcpProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs hcp}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        credential_file: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        skip_status_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        workload_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HcpProviderWorkloadIdentity", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs hcp} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#alias HcpProvider#alias}
        :param client_id: The OAuth2 Client ID for API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#client_id HcpProvider#client_id}
        :param client_secret: The OAuth2 Client Secret for API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#client_secret HcpProvider#client_secret}
        :param credential_file: The path to an HCP credential file to use to authenticate the provider to HCP. You can alternatively set the HCP_CRED_FILE environment variable to point at a credential file as well. Using a credential file allows you to authenticate the provider as a service principal via client credentials or dynamically based on Workload Identity Federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#credential_file HcpProvider#credential_file}
        :param project_id: The default project in which resources should be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#project_id HcpProvider#project_id}
        :param skip_status_check: When set to true, the provider will skip checking the HCP status page for service outages or returning warnings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#skip_status_check HcpProvider#skip_status_check}
        :param workload_identity: workload_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#workload_identity HcpProvider#workload_identity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9962aa89ee76b9284f3c61b4b164aa99145fa8bddda7ed708d531d776d163687)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = HcpProviderConfig(
            alias=alias,
            client_id=client_id,
            client_secret=client_secret,
            credential_file=credential_file,
            project_id=project_id,
            skip_status_check=skip_status_check,
            workload_identity=workload_identity,
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
        '''Generates CDKTF code for importing a HcpProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HcpProvider to import.
        :param import_from_id: The id of the existing HcpProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HcpProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fafbf8cddab256e6ef8581a3794e58366b1544af1b15e13a0e6eb2ce1322276)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetCredentialFile")
    def reset_credential_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialFile", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetSkipStatusCheck")
    def reset_skip_status_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipStatusCheck", []))

    @jsii.member(jsii_name="resetWorkloadIdentity")
    def reset_workload_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadIdentity", []))

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
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialFileInput")
    def credential_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialFileInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="skipStatusCheckInput")
    def skip_status_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipStatusCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityInput")
    def workload_identity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HcpProviderWorkloadIdentity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HcpProviderWorkloadIdentity"]]], jsii.get(self, "workloadIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa8be209b897206395a67d051da62495fb9769d85c55d77ee87915a17cd8f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d607b19aa907e10ca7ac5b73851bbb232658dd8170dc27c627a8cb4dfc9e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dafcdfb9eabde61093679799aefdd014a3a23c3c2b1ac18507da12e6e1dd37c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialFile")
    def credential_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialFile"))

    @credential_file.setter
    def credential_file(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ffc942cd79a57e4dc575b85bc270124ebdb3fd85428ed986d3aec337e3defd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183b9b426aa5ee0c077e702bb0a40dbda09a1907bb4ebaafd785c83fc424880f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipStatusCheck")
    def skip_status_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipStatusCheck"))

    @skip_status_check.setter
    def skip_status_check(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb90b04aed44d60576fa84c7510a93f2b6eb8fb5ba7c9435a611daf99d90911a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipStatusCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadIdentity")
    def workload_identity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HcpProviderWorkloadIdentity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HcpProviderWorkloadIdentity"]]], jsii.get(self, "workloadIdentity"))

    @workload_identity.setter
    def workload_identity(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HcpProviderWorkloadIdentity"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a63706896f43d87a03c23af73326a79f1199cada7659cc2ba843fa37c10210a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadIdentity", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.provider.HcpProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "credential_file": "credentialFile",
        "project_id": "projectId",
        "skip_status_check": "skipStatusCheck",
        "workload_identity": "workloadIdentity",
    },
)
class HcpProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        credential_file: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        skip_status_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        workload_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HcpProviderWorkloadIdentity", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#alias HcpProvider#alias}
        :param client_id: The OAuth2 Client ID for API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#client_id HcpProvider#client_id}
        :param client_secret: The OAuth2 Client Secret for API operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#client_secret HcpProvider#client_secret}
        :param credential_file: The path to an HCP credential file to use to authenticate the provider to HCP. You can alternatively set the HCP_CRED_FILE environment variable to point at a credential file as well. Using a credential file allows you to authenticate the provider as a service principal via client credentials or dynamically based on Workload Identity Federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#credential_file HcpProvider#credential_file}
        :param project_id: The default project in which resources should be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#project_id HcpProvider#project_id}
        :param skip_status_check: When set to true, the provider will skip checking the HCP status page for service outages or returning warnings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#skip_status_check HcpProvider#skip_status_check}
        :param workload_identity: workload_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#workload_identity HcpProvider#workload_identity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6d52a2ef8cb5413ad5a8ca3a6605f03df54b36c17588f9157418d93854016b)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument credential_file", value=credential_file, expected_type=type_hints["credential_file"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument skip_status_check", value=skip_status_check, expected_type=type_hints["skip_status_check"])
            check_type(argname="argument workload_identity", value=workload_identity, expected_type=type_hints["workload_identity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if credential_file is not None:
            self._values["credential_file"] = credential_file
        if project_id is not None:
            self._values["project_id"] = project_id
        if skip_status_check is not None:
            self._values["skip_status_check"] = skip_status_check
        if workload_identity is not None:
            self._values["workload_identity"] = workload_identity

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#alias HcpProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The OAuth2 Client ID for API operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#client_id HcpProvider#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The OAuth2 Client Secret for API operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#client_secret HcpProvider#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credential_file(self) -> typing.Optional[builtins.str]:
        '''The path to an HCP credential file to use to authenticate the provider to HCP.

        You can alternatively set the HCP_CRED_FILE environment variable to point at a credential file as well. Using a credential file allows you to authenticate the provider as a service principal via client credentials or dynamically based on Workload Identity Federation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#credential_file HcpProvider#credential_file}
        '''
        result = self._values.get("credential_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The default project in which resources should be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#project_id HcpProvider#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_status_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, the provider will skip checking the HCP status page for service outages or returning warnings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#skip_status_check HcpProvider#skip_status_check}
        '''
        result = self._values.get("skip_status_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def workload_identity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HcpProviderWorkloadIdentity"]]]:
        '''workload_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#workload_identity HcpProvider#workload_identity}
        '''
        result = self._values.get("workload_identity")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HcpProviderWorkloadIdentity"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HcpProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.provider.HcpProviderWorkloadIdentity",
    jsii_struct_bases=[],
    name_mapping={
        "resource_name": "resourceName",
        "token": "token",
        "token_file": "tokenFile",
    },
)
class HcpProviderWorkloadIdentity:
    def __init__(
        self,
        *,
        resource_name: builtins.str,
        token: typing.Optional[builtins.str] = None,
        token_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_name: The resource_name of the Workload Identity Provider to exchange the token with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#resource_name HcpProvider#resource_name}
        :param token: The JWT token retrieved from an OpenID Connect (OIDC) or OAuth2 provider. At least one of ``token_file`` or ``token`` must be set, if both are set then ``token`` takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#token HcpProvider#token}
        :param token_file: The path to a file containing a JWT token retrieved from an OpenID Connect (OIDC) or OAuth2 provider. At least one of ``token_file`` or ``token`` must be set, if both are set then ``token`` takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#token_file HcpProvider#token_file}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f873a703f6c32aa3030b10b302c247493eb7ac9cb82faa555945f6b53027e97)
            check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument token_file", value=token_file, expected_type=type_hints["token_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_name": resource_name,
        }
        if token is not None:
            self._values["token"] = token
        if token_file is not None:
            self._values["token_file"] = token_file

    @builtins.property
    def resource_name(self) -> builtins.str:
        '''The resource_name of the Workload Identity Provider to exchange the token with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#resource_name HcpProvider#resource_name}
        '''
        result = self._values.get("resource_name")
        assert result is not None, "Required property 'resource_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''The JWT token retrieved from an OpenID Connect (OIDC) or OAuth2 provider.

        At least one of ``token_file`` or ``token`` must be set, if both are set then ``token`` takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#token HcpProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_file(self) -> typing.Optional[builtins.str]:
        '''The path to a file containing a JWT token retrieved from an OpenID Connect (OIDC) or OAuth2 provider.

        At least one of ``token_file`` or ``token`` must be set, if both are set then ``token`` takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs#token_file HcpProvider#token_file}
        '''
        result = self._values.get("token_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HcpProviderWorkloadIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HcpProvider",
    "HcpProviderConfig",
    "HcpProviderWorkloadIdentity",
]

publication.publish()

def _typecheckingstub__9962aa89ee76b9284f3c61b4b164aa99145fa8bddda7ed708d531d776d163687(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    credential_file: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    skip_status_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    workload_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HcpProviderWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fafbf8cddab256e6ef8581a3794e58366b1544af1b15e13a0e6eb2ce1322276(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa8be209b897206395a67d051da62495fb9769d85c55d77ee87915a17cd8f74(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d607b19aa907e10ca7ac5b73851bbb232658dd8170dc27c627a8cb4dfc9e11(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafcdfb9eabde61093679799aefdd014a3a23c3c2b1ac18507da12e6e1dd37c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ffc942cd79a57e4dc575b85bc270124ebdb3fd85428ed986d3aec337e3defd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183b9b426aa5ee0c077e702bb0a40dbda09a1907bb4ebaafd785c83fc424880f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb90b04aed44d60576fa84c7510a93f2b6eb8fb5ba7c9435a611daf99d90911a(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a63706896f43d87a03c23af73326a79f1199cada7659cc2ba843fa37c10210a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HcpProviderWorkloadIdentity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6d52a2ef8cb5413ad5a8ca3a6605f03df54b36c17588f9157418d93854016b(
    *,
    alias: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    credential_file: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    skip_status_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    workload_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HcpProviderWorkloadIdentity, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f873a703f6c32aa3030b10b302c247493eb7ac9cb82faa555945f6b53027e97(
    *,
    resource_name: builtins.str,
    token: typing.Optional[builtins.str] = None,
    token_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
