r'''
# `hcp_iam_workload_identity_provider`

Refer to the Terraform Registry for docs: [`hcp_iam_workload_identity_provider`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider).
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


class IamWorkloadIdentityProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.iamWorkloadIdentityProvider.IamWorkloadIdentityProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider hcp_iam_workload_identity_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        conditional_access: builtins.str,
        name: builtins.str,
        service_principal: builtins.str,
        aws: typing.Optional[typing.Union["IamWorkloadIdentityProviderAws", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["IamWorkloadIdentityProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider hcp_iam_workload_identity_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param conditional_access: conditional_access is a hashicorp/go-bexpr string that is evaluated when exchanging tokens. It restricts which upstream identities are allowed to access the service principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#conditional_access IamWorkloadIdentityProvider#conditional_access}
        :param name: The workload identity provider's name. Ideally, this should be descriptive of the workload being federated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#name IamWorkloadIdentityProvider#name}
        :param service_principal: The service principal's resource name for which the workload identity provider will be created for. Only service principals created within a project are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#service_principal IamWorkloadIdentityProvider#service_principal}
        :param aws: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#aws IamWorkloadIdentityProvider#aws}.
        :param description: A description for the workload identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#description IamWorkloadIdentityProvider#description}
        :param oidc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#oidc IamWorkloadIdentityProvider#oidc}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e56d98d1d449ac3971dd48cdaa253224ebfbbe217066732f8ca0c49de4b0bc5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = IamWorkloadIdentityProviderConfig(
            conditional_access=conditional_access,
            name=name,
            service_principal=service_principal,
            aws=aws,
            description=description,
            oidc=oidc,
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
        '''Generates CDKTF code for importing a IamWorkloadIdentityProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IamWorkloadIdentityProvider to import.
        :param import_from_id: The id of the existing IamWorkloadIdentityProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IamWorkloadIdentityProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c0b6ec46308d2ce67d80a00cc9fa87a5a330fb05d00b589be88012db40a3b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAws")
    def put_aws(self, *, account_id: builtins.str) -> None:
        '''
        :param account_id: The AWS Account ID that is allowed to exchange workload identities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#account_id IamWorkloadIdentityProvider#account_id}
        '''
        value = IamWorkloadIdentityProviderAws(account_id=account_id)

        return typing.cast(None, jsii.invoke(self, "putAws", [value]))

    @jsii.member(jsii_name="putOidc")
    def put_oidc(
        self,
        *,
        issuer_uri: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param issuer_uri: The URL of the OIDC Issuer that is allowed to exchange workload identities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#issuer_uri IamWorkloadIdentityProvider#issuer_uri}
        :param allowed_audiences: allowed_audiences is the set of audiences set on the access token that are allowed to exchange identities. The access token must have an audience that is contained in this set. If no audience is set, the default allowed audience will be the resource name of the WorkloadIdentityProvider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#allowed_audiences IamWorkloadIdentityProvider#allowed_audiences}
        '''
        value = IamWorkloadIdentityProviderOidc(
            issuer_uri=issuer_uri, allowed_audiences=allowed_audiences
        )

        return typing.cast(None, jsii.invoke(self, "putOidc", [value]))

    @jsii.member(jsii_name="resetAws")
    def reset_aws(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAws", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetOidc")
    def reset_oidc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidc", []))

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
    @jsii.member(jsii_name="aws")
    def aws(self) -> "IamWorkloadIdentityProviderAwsOutputReference":
        return typing.cast("IamWorkloadIdentityProviderAwsOutputReference", jsii.get(self, "aws"))

    @builtins.property
    @jsii.member(jsii_name="oidc")
    def oidc(self) -> "IamWorkloadIdentityProviderOidcOutputReference":
        return typing.cast("IamWorkloadIdentityProviderOidcOutputReference", jsii.get(self, "oidc"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="resourceName")
    def resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceName"))

    @builtins.property
    @jsii.member(jsii_name="awsInput")
    def aws_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamWorkloadIdentityProviderAws"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamWorkloadIdentityProviderAws"]], jsii.get(self, "awsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionalAccessInput")
    def conditional_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionalAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcInput")
    def oidc_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamWorkloadIdentityProviderOidc"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamWorkloadIdentityProviderOidc"]], jsii.get(self, "oidcInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalInput")
    def service_principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePrincipalInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionalAccess")
    def conditional_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionalAccess"))

    @conditional_access.setter
    def conditional_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a343b5ec6f2e56cd1776b35ec7f67667eb12e9ded1b7831112382625a17ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionalAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2fbf7ce669d141413e1e173b7b3792b1ea90f5db0f8cb38bedbb7a8879728d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7160182d2b91cb28a0ae01a50e620c2e3fde888b70ab627d5a345dc1fb29d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrincipal")
    def service_principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePrincipal"))

    @service_principal.setter
    def service_principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c03a476e19d8f3c2849038fb1e8b4e5b669b0d13793fcfbb3ae2ee3c0a1487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipal", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.iamWorkloadIdentityProvider.IamWorkloadIdentityProviderAws",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId"},
)
class IamWorkloadIdentityProviderAws:
    def __init__(self, *, account_id: builtins.str) -> None:
        '''
        :param account_id: The AWS Account ID that is allowed to exchange workload identities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#account_id IamWorkloadIdentityProvider#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a88a38e54d44075f437e416e6f61bb4578f42daed5134d47297282da052296)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The AWS Account ID that is allowed to exchange workload identities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#account_id IamWorkloadIdentityProvider#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityProviderAws(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkloadIdentityProviderAwsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.iamWorkloadIdentityProvider.IamWorkloadIdentityProviderAwsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5454aa1427682b12f94e06f81fb3db201f93534da9a2cd731d52c63f8db5f534)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119799c2a8a1302486c73e01029949f9ba6b62aa1d3980f6667eea84175161e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityProviderAws]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityProviderAws]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityProviderAws]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc398feb3696efe66b342ae4eee327babd3f29ceb6f70283284fec8b9e4a543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.iamWorkloadIdentityProvider.IamWorkloadIdentityProviderConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "conditional_access": "conditionalAccess",
        "name": "name",
        "service_principal": "servicePrincipal",
        "aws": "aws",
        "description": "description",
        "oidc": "oidc",
    },
)
class IamWorkloadIdentityProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        conditional_access: builtins.str,
        name: builtins.str,
        service_principal: builtins.str,
        aws: typing.Optional[typing.Union[IamWorkloadIdentityProviderAws, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["IamWorkloadIdentityProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param conditional_access: conditional_access is a hashicorp/go-bexpr string that is evaluated when exchanging tokens. It restricts which upstream identities are allowed to access the service principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#conditional_access IamWorkloadIdentityProvider#conditional_access}
        :param name: The workload identity provider's name. Ideally, this should be descriptive of the workload being federated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#name IamWorkloadIdentityProvider#name}
        :param service_principal: The service principal's resource name for which the workload identity provider will be created for. Only service principals created within a project are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#service_principal IamWorkloadIdentityProvider#service_principal}
        :param aws: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#aws IamWorkloadIdentityProvider#aws}.
        :param description: A description for the workload identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#description IamWorkloadIdentityProvider#description}
        :param oidc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#oidc IamWorkloadIdentityProvider#oidc}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws, dict):
            aws = IamWorkloadIdentityProviderAws(**aws)
        if isinstance(oidc, dict):
            oidc = IamWorkloadIdentityProviderOidc(**oidc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af865736a68509808729e4f897540aab4d947915d022a1cd414e229b47ddb999)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument conditional_access", value=conditional_access, expected_type=type_hints["conditional_access"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_principal", value=service_principal, expected_type=type_hints["service_principal"])
            check_type(argname="argument aws", value=aws, expected_type=type_hints["aws"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument oidc", value=oidc, expected_type=type_hints["oidc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conditional_access": conditional_access,
            "name": name,
            "service_principal": service_principal,
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
        if aws is not None:
            self._values["aws"] = aws
        if description is not None:
            self._values["description"] = description
        if oidc is not None:
            self._values["oidc"] = oidc

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
    def conditional_access(self) -> builtins.str:
        '''conditional_access is a hashicorp/go-bexpr string that is evaluated when exchanging tokens.

        It restricts which upstream identities are allowed to access the service principal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#conditional_access IamWorkloadIdentityProvider#conditional_access}
        '''
        result = self._values.get("conditional_access")
        assert result is not None, "Required property 'conditional_access' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The workload identity provider's name. Ideally, this should be descriptive of the workload being federated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#name IamWorkloadIdentityProvider#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_principal(self) -> builtins.str:
        '''The service principal's resource name for which the workload identity provider will be created for.

        Only service principals created within a project are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#service_principal IamWorkloadIdentityProvider#service_principal}
        '''
        result = self._values.get("service_principal")
        assert result is not None, "Required property 'service_principal' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws(self) -> typing.Optional[IamWorkloadIdentityProviderAws]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#aws IamWorkloadIdentityProvider#aws}.'''
        result = self._values.get("aws")
        return typing.cast(typing.Optional[IamWorkloadIdentityProviderAws], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the workload identity provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#description IamWorkloadIdentityProvider#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc(self) -> typing.Optional["IamWorkloadIdentityProviderOidc"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#oidc IamWorkloadIdentityProvider#oidc}.'''
        result = self._values.get("oidc")
        return typing.cast(typing.Optional["IamWorkloadIdentityProviderOidc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.iamWorkloadIdentityProvider.IamWorkloadIdentityProviderOidc",
    jsii_struct_bases=[],
    name_mapping={"issuer_uri": "issuerUri", "allowed_audiences": "allowedAudiences"},
)
class IamWorkloadIdentityProviderOidc:
    def __init__(
        self,
        *,
        issuer_uri: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param issuer_uri: The URL of the OIDC Issuer that is allowed to exchange workload identities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#issuer_uri IamWorkloadIdentityProvider#issuer_uri}
        :param allowed_audiences: allowed_audiences is the set of audiences set on the access token that are allowed to exchange identities. The access token must have an audience that is contained in this set. If no audience is set, the default allowed audience will be the resource name of the WorkloadIdentityProvider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#allowed_audiences IamWorkloadIdentityProvider#allowed_audiences}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d832e70488c30ef1f2c9d719017e8842c4dfd326e3714d546f23d07881baf8d8)
            check_type(argname="argument issuer_uri", value=issuer_uri, expected_type=type_hints["issuer_uri"])
            check_type(argname="argument allowed_audiences", value=allowed_audiences, expected_type=type_hints["allowed_audiences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer_uri": issuer_uri,
        }
        if allowed_audiences is not None:
            self._values["allowed_audiences"] = allowed_audiences

    @builtins.property
    def issuer_uri(self) -> builtins.str:
        '''The URL of the OIDC Issuer that is allowed to exchange workload identities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#issuer_uri IamWorkloadIdentityProvider#issuer_uri}
        '''
        result = self._values.get("issuer_uri")
        assert result is not None, "Required property 'issuer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''allowed_audiences is the set of audiences set on the access token that are allowed to exchange identities.

        The access token must have an audience that is contained in this set. If no audience is set, the default allowed audience will be the resource name of the WorkloadIdentityProvider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/iam_workload_identity_provider#allowed_audiences IamWorkloadIdentityProvider#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityProviderOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkloadIdentityProviderOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.iamWorkloadIdentityProvider.IamWorkloadIdentityProviderOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baaf42239cb1ce0ac5df7dcdb7c630553b900d9e5ee3e993432e885498fc01b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedAudiences")
    def reset_allowed_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAudiences", []))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiencesInput")
    def allowed_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAudiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUriInput")
    def issuer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @allowed_audiences.setter
    def allowed_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca735e8ae438bab7bdc28ecf0e116540509ec99580dfcba2404d1fb821847d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b557bb3bb35d4597e7099b15f02c4063ea29b707bcb8b62a154c1140b2dc234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityProviderOidc]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityProviderOidc]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityProviderOidc]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1161ce00a8b95bbadbaefba218e49628a08bbd1dd72e4e3b4227d89aa9fc38c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IamWorkloadIdentityProvider",
    "IamWorkloadIdentityProviderAws",
    "IamWorkloadIdentityProviderAwsOutputReference",
    "IamWorkloadIdentityProviderConfig",
    "IamWorkloadIdentityProviderOidc",
    "IamWorkloadIdentityProviderOidcOutputReference",
]

publication.publish()

def _typecheckingstub__0e56d98d1d449ac3971dd48cdaa253224ebfbbe217066732f8ca0c49de4b0bc5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    conditional_access: builtins.str,
    name: builtins.str,
    service_principal: builtins.str,
    aws: typing.Optional[typing.Union[IamWorkloadIdentityProviderAws, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[IamWorkloadIdentityProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e8c0b6ec46308d2ce67d80a00cc9fa87a5a330fb05d00b589be88012db40a3b7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a343b5ec6f2e56cd1776b35ec7f67667eb12e9ded1b7831112382625a17ddd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2fbf7ce669d141413e1e173b7b3792b1ea90f5db0f8cb38bedbb7a8879728d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7160182d2b91cb28a0ae01a50e620c2e3fde888b70ab627d5a345dc1fb29d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c03a476e19d8f3c2849038fb1e8b4e5b669b0d13793fcfbb3ae2ee3c0a1487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a88a38e54d44075f437e416e6f61bb4578f42daed5134d47297282da052296(
    *,
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5454aa1427682b12f94e06f81fb3db201f93534da9a2cd731d52c63f8db5f534(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119799c2a8a1302486c73e01029949f9ba6b62aa1d3980f6667eea84175161e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc398feb3696efe66b342ae4eee327babd3f29ceb6f70283284fec8b9e4a543(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityProviderAws]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af865736a68509808729e4f897540aab4d947915d022a1cd414e229b47ddb999(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    conditional_access: builtins.str,
    name: builtins.str,
    service_principal: builtins.str,
    aws: typing.Optional[typing.Union[IamWorkloadIdentityProviderAws, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[IamWorkloadIdentityProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d832e70488c30ef1f2c9d719017e8842c4dfd326e3714d546f23d07881baf8d8(
    *,
    issuer_uri: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baaf42239cb1ce0ac5df7dcdb7c630553b900d9e5ee3e993432e885498fc01b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca735e8ae438bab7bdc28ecf0e116540509ec99580dfcba2404d1fb821847d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b557bb3bb35d4597e7099b15f02c4063ea29b707bcb8b62a154c1140b2dc234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1161ce00a8b95bbadbaefba218e49628a08bbd1dd72e4e3b4227d89aa9fc38c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityProviderOidc]],
) -> None:
    """Type checking stubs"""
    pass
