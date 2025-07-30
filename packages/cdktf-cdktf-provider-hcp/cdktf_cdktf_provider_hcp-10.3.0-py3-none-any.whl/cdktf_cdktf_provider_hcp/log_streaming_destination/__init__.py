r'''
# `hcp_log_streaming_destination`

Refer to the Terraform Registry for docs: [`hcp_log_streaming_destination`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination).
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


class LogStreamingDestination(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.logStreamingDestination.LogStreamingDestination",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination hcp_log_streaming_destination}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        cloudwatch: typing.Optional[typing.Union["LogStreamingDestinationCloudwatch", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["LogStreamingDestinationDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        splunk_cloud: typing.Optional[typing.Union["LogStreamingDestinationSplunkCloud", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination hcp_log_streaming_destination} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The HCP Log Streaming Destination’s name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#name LogStreamingDestination#name}
        :param cloudwatch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#cloudwatch LogStreamingDestination#cloudwatch}.
        :param datadog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#datadog LogStreamingDestination#datadog}.
        :param splunk_cloud: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#splunk_cloud LogStreamingDestination#splunk_cloud}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11c6ebf5918634ed0ff328a6d9c0c56d7a1e2d9e04145bb101b1bb1be7667ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = LogStreamingDestinationConfig(
            name=name,
            cloudwatch=cloudwatch,
            datadog=datadog,
            splunk_cloud=splunk_cloud,
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
        '''Generates CDKTF code for importing a LogStreamingDestination resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LogStreamingDestination to import.
        :param import_from_id: The id of the existing LogStreamingDestination that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LogStreamingDestination to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9871ebfffe2db91ba6f5fbb6fa07ecfb78c95b04a94997249396cb9ad26f87bc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCloudwatch")
    def put_cloudwatch(
        self,
        *,
        external_id: builtins.str,
        region: builtins.str,
        role_arn: builtins.str,
        log_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_id: The external_id to provide when assuming the aws IAM role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#external_id LogStreamingDestination#external_id}
        :param region: The region the CloudWatch destination is set up to stream to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#region LogStreamingDestination#region}
        :param role_arn: The role_arn that will be assumed to stream logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#role_arn LogStreamingDestination#role_arn}
        :param log_group_name: The log_group_name of the CloudWatch destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#log_group_name LogStreamingDestination#log_group_name}
        '''
        value = LogStreamingDestinationCloudwatch(
            external_id=external_id,
            region=region,
            role_arn=role_arn,
            log_group_name=log_group_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatch", [value]))

    @jsii.member(jsii_name="putDatadog")
    def put_datadog(
        self,
        *,
        api_key: builtins.str,
        endpoint: builtins.str,
        application_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key: The value for the DD-API-KEY to send when making requests to DataDog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#api_key LogStreamingDestination#api_key}
        :param endpoint: The Datadog endpoint to send logs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#endpoint LogStreamingDestination#endpoint}
        :param application_key: The value for the DD-APPLICATION-KEY to send when making requests to DataDog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#application_key LogStreamingDestination#application_key}
        '''
        value = LogStreamingDestinationDatadog(
            api_key=api_key, endpoint=endpoint, application_key=application_key
        )

        return typing.cast(None, jsii.invoke(self, "putDatadog", [value]))

    @jsii.member(jsii_name="putSplunkCloud")
    def put_splunk_cloud(self, *, endpoint: builtins.str, token: builtins.str) -> None:
        '''
        :param endpoint: The Splunk Cloud endpoint to send logs to. Streaming to free trial instances is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#endpoint LogStreamingDestination#endpoint}
        :param token: The authentication token that will be used by the platform to access Splunk Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#token LogStreamingDestination#token}
        '''
        value = LogStreamingDestinationSplunkCloud(endpoint=endpoint, token=token)

        return typing.cast(None, jsii.invoke(self, "putSplunkCloud", [value]))

    @jsii.member(jsii_name="resetCloudwatch")
    def reset_cloudwatch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatch", []))

    @jsii.member(jsii_name="resetDatadog")
    def reset_datadog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadog", []))

    @jsii.member(jsii_name="resetSplunkCloud")
    def reset_splunk_cloud(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplunkCloud", []))

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
    @jsii.member(jsii_name="cloudwatch")
    def cloudwatch(self) -> "LogStreamingDestinationCloudwatchOutputReference":
        return typing.cast("LogStreamingDestinationCloudwatchOutputReference", jsii.get(self, "cloudwatch"))

    @builtins.property
    @jsii.member(jsii_name="datadog")
    def datadog(self) -> "LogStreamingDestinationDatadogOutputReference":
        return typing.cast("LogStreamingDestinationDatadogOutputReference", jsii.get(self, "datadog"))

    @builtins.property
    @jsii.member(jsii_name="splunkCloud")
    def splunk_cloud(self) -> "LogStreamingDestinationSplunkCloudOutputReference":
        return typing.cast("LogStreamingDestinationSplunkCloudOutputReference", jsii.get(self, "splunkCloud"))

    @builtins.property
    @jsii.member(jsii_name="streamingDestinationId")
    def streaming_destination_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamingDestinationId"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchInput")
    def cloudwatch_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogStreamingDestinationCloudwatch"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogStreamingDestinationCloudwatch"]], jsii.get(self, "cloudwatchInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogInput")
    def datadog_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogStreamingDestinationDatadog"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogStreamingDestinationDatadog"]], jsii.get(self, "datadogInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="splunkCloudInput")
    def splunk_cloud_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogStreamingDestinationSplunkCloud"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogStreamingDestinationSplunkCloud"]], jsii.get(self, "splunkCloudInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abee79f41bacacf80bbdd23da87dc51fffe2792b0666cfd3d52660245dd4e09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.logStreamingDestination.LogStreamingDestinationCloudwatch",
    jsii_struct_bases=[],
    name_mapping={
        "external_id": "externalId",
        "region": "region",
        "role_arn": "roleArn",
        "log_group_name": "logGroupName",
    },
)
class LogStreamingDestinationCloudwatch:
    def __init__(
        self,
        *,
        external_id: builtins.str,
        region: builtins.str,
        role_arn: builtins.str,
        log_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_id: The external_id to provide when assuming the aws IAM role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#external_id LogStreamingDestination#external_id}
        :param region: The region the CloudWatch destination is set up to stream to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#region LogStreamingDestination#region}
        :param role_arn: The role_arn that will be assumed to stream logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#role_arn LogStreamingDestination#role_arn}
        :param log_group_name: The log_group_name of the CloudWatch destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#log_group_name LogStreamingDestination#log_group_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f24a43e6a90ead2dcd0645e32e261f3e409429066c9ad620601712793067883)
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "external_id": external_id,
            "region": region,
            "role_arn": role_arn,
        }
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name

    @builtins.property
    def external_id(self) -> builtins.str:
        '''The external_id to provide when assuming the aws IAM role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#external_id LogStreamingDestination#external_id}
        '''
        result = self._values.get("external_id")
        assert result is not None, "Required property 'external_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''The region the CloudWatch destination is set up to stream to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#region LogStreamingDestination#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The role_arn that will be assumed to stream logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#role_arn LogStreamingDestination#role_arn}
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The log_group_name of the CloudWatch destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#log_group_name LogStreamingDestination#log_group_name}
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogStreamingDestinationCloudwatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogStreamingDestinationCloudwatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.logStreamingDestination.LogStreamingDestinationCloudwatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bad724685a5d91e2bf675e9a42a1d16a1a6b8c944baee4f1fc6328c8165196ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @builtins.property
    @jsii.member(jsii_name="externalIdInput")
    def external_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalId"))

    @external_id.setter
    def external_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e98bc7a40127de25a6d1e1d15d46f7d3c9e7d256fcb27b510d4f36d7828d1b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948d4fdece8236a686bd6cb24b7825dc3c0555c12e9e348781afacbf1ec40238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2c4bfd5a4b0eff52bf43e0804c58e7bae6b037ecb0e9f0e3eee3fe5ceb6f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136e8b0bf6b05011c0abdabb58cf9b854986d88a8896d321ab164917410c4597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationCloudwatch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationCloudwatch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationCloudwatch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8822e9c251d64f7c13a314d5ba0ea080f4c2b42bb80b0e31bd3a8696ed4bb22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.logStreamingDestination.LogStreamingDestinationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "cloudwatch": "cloudwatch",
        "datadog": "datadog",
        "splunk_cloud": "splunkCloud",
    },
)
class LogStreamingDestinationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        cloudwatch: typing.Optional[typing.Union[LogStreamingDestinationCloudwatch, typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["LogStreamingDestinationDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        splunk_cloud: typing.Optional[typing.Union["LogStreamingDestinationSplunkCloud", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The HCP Log Streaming Destination’s name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#name LogStreamingDestination#name}
        :param cloudwatch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#cloudwatch LogStreamingDestination#cloudwatch}.
        :param datadog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#datadog LogStreamingDestination#datadog}.
        :param splunk_cloud: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#splunk_cloud LogStreamingDestination#splunk_cloud}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cloudwatch, dict):
            cloudwatch = LogStreamingDestinationCloudwatch(**cloudwatch)
        if isinstance(datadog, dict):
            datadog = LogStreamingDestinationDatadog(**datadog)
        if isinstance(splunk_cloud, dict):
            splunk_cloud = LogStreamingDestinationSplunkCloud(**splunk_cloud)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87df50a198e004a389d85b112dab5244530054281766ae374a7837aec8d330b1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cloudwatch", value=cloudwatch, expected_type=type_hints["cloudwatch"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument splunk_cloud", value=splunk_cloud, expected_type=type_hints["splunk_cloud"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if cloudwatch is not None:
            self._values["cloudwatch"] = cloudwatch
        if datadog is not None:
            self._values["datadog"] = datadog
        if splunk_cloud is not None:
            self._values["splunk_cloud"] = splunk_cloud

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
    def name(self) -> builtins.str:
        '''The HCP Log Streaming Destination’s name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#name LogStreamingDestination#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwatch(self) -> typing.Optional[LogStreamingDestinationCloudwatch]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#cloudwatch LogStreamingDestination#cloudwatch}.'''
        result = self._values.get("cloudwatch")
        return typing.cast(typing.Optional[LogStreamingDestinationCloudwatch], result)

    @builtins.property
    def datadog(self) -> typing.Optional["LogStreamingDestinationDatadog"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#datadog LogStreamingDestination#datadog}.'''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional["LogStreamingDestinationDatadog"], result)

    @builtins.property
    def splunk_cloud(self) -> typing.Optional["LogStreamingDestinationSplunkCloud"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#splunk_cloud LogStreamingDestination#splunk_cloud}.'''
        result = self._values.get("splunk_cloud")
        return typing.cast(typing.Optional["LogStreamingDestinationSplunkCloud"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogStreamingDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.logStreamingDestination.LogStreamingDestinationDatadog",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "endpoint": "endpoint",
        "application_key": "applicationKey",
    },
)
class LogStreamingDestinationDatadog:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        endpoint: builtins.str,
        application_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key: The value for the DD-API-KEY to send when making requests to DataDog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#api_key LogStreamingDestination#api_key}
        :param endpoint: The Datadog endpoint to send logs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#endpoint LogStreamingDestination#endpoint}
        :param application_key: The value for the DD-APPLICATION-KEY to send when making requests to DataDog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#application_key LogStreamingDestination#application_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35cba3bcf668395d80bc310b758b88009f4082db4a57b2ce7d47cde0e89f7f80)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument application_key", value=application_key, expected_type=type_hints["application_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "endpoint": endpoint,
        }
        if application_key is not None:
            self._values["application_key"] = application_key

    @builtins.property
    def api_key(self) -> builtins.str:
        '''The value for the DD-API-KEY to send when making requests to DataDog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#api_key LogStreamingDestination#api_key}
        '''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''The Datadog endpoint to send logs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#endpoint LogStreamingDestination#endpoint}
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_key(self) -> typing.Optional[builtins.str]:
        '''The value for the DD-APPLICATION-KEY to send when making requests to DataDog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#application_key LogStreamingDestination#application_key}
        '''
        result = self._values.get("application_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogStreamingDestinationDatadog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogStreamingDestinationDatadogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.logStreamingDestination.LogStreamingDestinationDatadogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__771199f24c158d745697f1d454f117d58419e575986b91c5eaba4e710dc1cc8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApplicationKey")
    def reset_application_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationKey", []))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationKeyInput")
    def application_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db57de67329516d41cb64e682cdffaa553e68413648cdd28fb0a3d55d924a128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationKey")
    def application_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationKey"))

    @application_key.setter
    def application_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7ffab33b769a7c3542f76a8a8ec1fe35627a2544799740c29cb30bda254a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c5f9b59fb1c0ceed7fb1e968a6d0b225141c9ae615e7bba60cb581832423fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationDatadog]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationDatadog]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationDatadog]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__451b67971c4ac9d3254c91ba43349091aece4737f7b2c5bb5a03a9e92c4cba14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.logStreamingDestination.LogStreamingDestinationSplunkCloud",
    jsii_struct_bases=[],
    name_mapping={"endpoint": "endpoint", "token": "token"},
)
class LogStreamingDestinationSplunkCloud:
    def __init__(self, *, endpoint: builtins.str, token: builtins.str) -> None:
        '''
        :param endpoint: The Splunk Cloud endpoint to send logs to. Streaming to free trial instances is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#endpoint LogStreamingDestination#endpoint}
        :param token: The authentication token that will be used by the platform to access Splunk Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#token LogStreamingDestination#token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c6d6eb16beed7155ca2b9ff87eca20f9f33f3f61813d26e13768ea0379378f)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "token": token,
        }

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''The Splunk Cloud endpoint to send logs to. Streaming to free trial instances is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#endpoint LogStreamingDestination#endpoint}
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token(self) -> builtins.str:
        '''The authentication token that will be used by the platform to access Splunk Cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/log_streaming_destination#token LogStreamingDestination#token}
        '''
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogStreamingDestinationSplunkCloud(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogStreamingDestinationSplunkCloudOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.logStreamingDestination.LogStreamingDestinationSplunkCloudOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33139b3379823351d44401e47592f250c30093727f87f169decdc6abab6018e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f31dcf60d9ad6ee0dbc3747e371d7f37905b9b81aa2a9d6ac9dce8b12c0d268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffffdcf458052b8abbb3220ad8fd07575bbdcb23fb3ca760fd11f8b6806b8ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationSplunkCloud]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationSplunkCloud]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationSplunkCloud]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3629f8aa0ea854ca487a93ee38fc47c61bb2e6651194e8016b4f2467c5be3a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LogStreamingDestination",
    "LogStreamingDestinationCloudwatch",
    "LogStreamingDestinationCloudwatchOutputReference",
    "LogStreamingDestinationConfig",
    "LogStreamingDestinationDatadog",
    "LogStreamingDestinationDatadogOutputReference",
    "LogStreamingDestinationSplunkCloud",
    "LogStreamingDestinationSplunkCloudOutputReference",
]

publication.publish()

def _typecheckingstub__d11c6ebf5918634ed0ff328a6d9c0c56d7a1e2d9e04145bb101b1bb1be7667ee(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    cloudwatch: typing.Optional[typing.Union[LogStreamingDestinationCloudwatch, typing.Dict[builtins.str, typing.Any]]] = None,
    datadog: typing.Optional[typing.Union[LogStreamingDestinationDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
    splunk_cloud: typing.Optional[typing.Union[LogStreamingDestinationSplunkCloud, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9871ebfffe2db91ba6f5fbb6fa07ecfb78c95b04a94997249396cb9ad26f87bc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abee79f41bacacf80bbdd23da87dc51fffe2792b0666cfd3d52660245dd4e09f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f24a43e6a90ead2dcd0645e32e261f3e409429066c9ad620601712793067883(
    *,
    external_id: builtins.str,
    region: builtins.str,
    role_arn: builtins.str,
    log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad724685a5d91e2bf675e9a42a1d16a1a6b8c944baee4f1fc6328c8165196ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e98bc7a40127de25a6d1e1d15d46f7d3c9e7d256fcb27b510d4f36d7828d1b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948d4fdece8236a686bd6cb24b7825dc3c0555c12e9e348781afacbf1ec40238(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2c4bfd5a4b0eff52bf43e0804c58e7bae6b037ecb0e9f0e3eee3fe5ceb6f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136e8b0bf6b05011c0abdabb58cf9b854986d88a8896d321ab164917410c4597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8822e9c251d64f7c13a314d5ba0ea080f4c2b42bb80b0e31bd3a8696ed4bb22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationCloudwatch]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87df50a198e004a389d85b112dab5244530054281766ae374a7837aec8d330b1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    cloudwatch: typing.Optional[typing.Union[LogStreamingDestinationCloudwatch, typing.Dict[builtins.str, typing.Any]]] = None,
    datadog: typing.Optional[typing.Union[LogStreamingDestinationDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
    splunk_cloud: typing.Optional[typing.Union[LogStreamingDestinationSplunkCloud, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35cba3bcf668395d80bc310b758b88009f4082db4a57b2ce7d47cde0e89f7f80(
    *,
    api_key: builtins.str,
    endpoint: builtins.str,
    application_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771199f24c158d745697f1d454f117d58419e575986b91c5eaba4e710dc1cc8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db57de67329516d41cb64e682cdffaa553e68413648cdd28fb0a3d55d924a128(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7ffab33b769a7c3542f76a8a8ec1fe35627a2544799740c29cb30bda254a88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c5f9b59fb1c0ceed7fb1e968a6d0b225141c9ae615e7bba60cb581832423fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451b67971c4ac9d3254c91ba43349091aece4737f7b2c5bb5a03a9e92c4cba14(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationDatadog]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c6d6eb16beed7155ca2b9ff87eca20f9f33f3f61813d26e13768ea0379378f(
    *,
    endpoint: builtins.str,
    token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33139b3379823351d44401e47592f250c30093727f87f169decdc6abab6018e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f31dcf60d9ad6ee0dbc3747e371d7f37905b9b81aa2a9d6ac9dce8b12c0d268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffffdcf458052b8abbb3220ad8fd07575bbdcb23fb3ca760fd11f8b6806b8ffd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3629f8aa0ea854ca487a93ee38fc47c61bb2e6651194e8016b4f2467c5be3a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogStreamingDestinationSplunkCloud]],
) -> None:
    """Type checking stubs"""
    pass
