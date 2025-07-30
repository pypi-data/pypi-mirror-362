r'''
# `hcp_waypoint_add_on_definition`

Refer to the Terraform Registry for docs: [`hcp_waypoint_add_on_definition`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition).
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


class WaypointAddOnDefinition(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointAddOnDefinition.WaypointAddOnDefinition",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition hcp_waypoint_add_on_definition}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
        name: builtins.str,
        summary: builtins.str,
        terraform_no_code_module_id: builtins.str,
        terraform_no_code_module_source: builtins.str,
        terraform_project_id: builtins.str,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_id: typing.Optional[builtins.str] = None,
        readme_markdown_template: typing.Optional[builtins.str] = None,
        terraform_agent_pool_id: typing.Optional[builtins.str] = None,
        terraform_cloud_workspace_details: typing.Optional[typing.Union["WaypointAddOnDefinitionTerraformCloudWorkspaceDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        terraform_execution_mode: typing.Optional[builtins.str] = None,
        variable_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WaypointAddOnDefinitionVariableOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition hcp_waypoint_add_on_definition} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: A longer description of the Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#description WaypointAddOnDefinition#description}
        :param name: The name of the Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#name WaypointAddOnDefinition#name}
        :param summary: A short summary of the Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#summary WaypointAddOnDefinition#summary}
        :param terraform_no_code_module_id: The ID of the Terraform no-code module to use for running Terraform operations. This is in the format of 'nocode-'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_no_code_module_id WaypointAddOnDefinition#terraform_no_code_module_id}
        :param terraform_no_code_module_source: Terraform Cloud no-code Module Source, expected to be in one of the following formats: "app.terraform.io/hcp_waypoint_example/ecs-advanced-microservice/aws" or "private/hcp_waypoint_example/ecs-advanced-microservice/aws". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_no_code_module_source WaypointAddOnDefinition#terraform_no_code_module_source}
        :param terraform_project_id: The ID of the Terraform Cloud Project to create workspaces in. The ID is found on the Terraform Cloud Project settings page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_project_id WaypointAddOnDefinition#terraform_project_id}
        :param labels: List of labels attached to this Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#labels WaypointAddOnDefinition#labels}
        :param project_id: The ID of the HCP project where the Waypoint Add-on Definition is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#project_id WaypointAddOnDefinition#project_id}
        :param readme_markdown_template: The markdown template for the Add-on Definition README (markdown format supported). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#readme_markdown_template WaypointAddOnDefinition#readme_markdown_template}
        :param terraform_agent_pool_id: The ID of the Terraform agent pool to use for running Terraform operations. This is only applicable when the execution mode is set to 'agent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_agent_pool_id WaypointAddOnDefinition#terraform_agent_pool_id}
        :param terraform_cloud_workspace_details: Terraform Cloud Workspace details. If not provided, defaults to the HCP Terraform project of the associated application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_cloud_workspace_details WaypointAddOnDefinition#terraform_cloud_workspace_details}
        :param terraform_execution_mode: The execution mode of the HCP Terraform workspaces for add-ons using this add-on definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_execution_mode WaypointAddOnDefinition#terraform_execution_mode}
        :param variable_options: List of variable options for the Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#variable_options WaypointAddOnDefinition#variable_options}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228a48df25a261b668774144693c4eff33450f646342dbb58693c15b2c1aa9b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = WaypointAddOnDefinitionConfig(
            description=description,
            name=name,
            summary=summary,
            terraform_no_code_module_id=terraform_no_code_module_id,
            terraform_no_code_module_source=terraform_no_code_module_source,
            terraform_project_id=terraform_project_id,
            labels=labels,
            project_id=project_id,
            readme_markdown_template=readme_markdown_template,
            terraform_agent_pool_id=terraform_agent_pool_id,
            terraform_cloud_workspace_details=terraform_cloud_workspace_details,
            terraform_execution_mode=terraform_execution_mode,
            variable_options=variable_options,
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
        '''Generates CDKTF code for importing a WaypointAddOnDefinition resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WaypointAddOnDefinition to import.
        :param import_from_id: The id of the existing WaypointAddOnDefinition that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WaypointAddOnDefinition to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a92ada119c0a532b472e365d34a9a0ffd135ffce66552e97a1b089d14db6e43)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTerraformCloudWorkspaceDetails")
    def put_terraform_cloud_workspace_details(
        self,
        *,
        name: builtins.str,
        terraform_project_id: builtins.str,
    ) -> None:
        '''
        :param name: Name of the Terraform Cloud Project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#name WaypointAddOnDefinition#name}
        :param terraform_project_id: Terraform Cloud Project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_project_id WaypointAddOnDefinition#terraform_project_id}
        '''
        value = WaypointAddOnDefinitionTerraformCloudWorkspaceDetails(
            name=name, terraform_project_id=terraform_project_id
        )

        return typing.cast(None, jsii.invoke(self, "putTerraformCloudWorkspaceDetails", [value]))

    @jsii.member(jsii_name="putVariableOptions")
    def put_variable_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WaypointAddOnDefinitionVariableOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964621e2c2a33d3954f02bf3d1bb1be659d7cffcbdf6639bf86e1878616041de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariableOptions", [value]))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetReadmeMarkdownTemplate")
    def reset_readme_markdown_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadmeMarkdownTemplate", []))

    @jsii.member(jsii_name="resetTerraformAgentPoolId")
    def reset_terraform_agent_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerraformAgentPoolId", []))

    @jsii.member(jsii_name="resetTerraformCloudWorkspaceDetails")
    def reset_terraform_cloud_workspace_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerraformCloudWorkspaceDetails", []))

    @jsii.member(jsii_name="resetTerraformExecutionMode")
    def reset_terraform_execution_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerraformExecutionMode", []))

    @jsii.member(jsii_name="resetVariableOptions")
    def reset_variable_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariableOptions", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="terraformCloudWorkspaceDetails")
    def terraform_cloud_workspace_details(
        self,
    ) -> "WaypointAddOnDefinitionTerraformCloudWorkspaceDetailsOutputReference":
        return typing.cast("WaypointAddOnDefinitionTerraformCloudWorkspaceDetailsOutputReference", jsii.get(self, "terraformCloudWorkspaceDetails"))

    @builtins.property
    @jsii.member(jsii_name="variableOptions")
    def variable_options(self) -> "WaypointAddOnDefinitionVariableOptionsList":
        return typing.cast("WaypointAddOnDefinitionVariableOptionsList", jsii.get(self, "variableOptions"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="readmeMarkdownTemplateInput")
    def readme_markdown_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readmeMarkdownTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="summaryInput")
    def summary_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "summaryInput"))

    @builtins.property
    @jsii.member(jsii_name="terraformAgentPoolIdInput")
    def terraform_agent_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformAgentPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="terraformCloudWorkspaceDetailsInput")
    def terraform_cloud_workspace_details_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WaypointAddOnDefinitionTerraformCloudWorkspaceDetails"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WaypointAddOnDefinitionTerraformCloudWorkspaceDetails"]], jsii.get(self, "terraformCloudWorkspaceDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="terraformExecutionModeInput")
    def terraform_execution_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformExecutionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="terraformNoCodeModuleIdInput")
    def terraform_no_code_module_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformNoCodeModuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="terraformNoCodeModuleSourceInput")
    def terraform_no_code_module_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformNoCodeModuleSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="terraformProjectIdInput")
    def terraform_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="variableOptionsInput")
    def variable_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WaypointAddOnDefinitionVariableOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WaypointAddOnDefinitionVariableOptions"]]], jsii.get(self, "variableOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848b9ec45669c16c71902265fa5b2c111e23df57ca3b89561e2299ffd64d2685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437dbd9280036805298e97467c3303b62333bf8bb4610e30903dc895ca7b7a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7eab7b2b83d1fbbfce11dfee65a0e63ba15f6715fb0b6cc7594642b8c804a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf644f29b299073cce6f2463c54a924ebd0d80084d04db9dfec8cce10a3ddd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readmeMarkdownTemplate")
    def readme_markdown_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readmeMarkdownTemplate"))

    @readme_markdown_template.setter
    def readme_markdown_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f722d58a72bba34fdf713aca00de214a7e720ac0700ecaefd86c2417824760bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readmeMarkdownTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="summary")
    def summary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "summary"))

    @summary.setter
    def summary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605b12050a84e5c69b93ec0ff96f6886075d6e7a323a4e0008211b0a4569bdef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "summary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformAgentPoolId")
    def terraform_agent_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformAgentPoolId"))

    @terraform_agent_pool_id.setter
    def terraform_agent_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56ad2d2a1ba809a1b331b19b3ee1889865fa4c673f5ed3c95debe575086e2e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAgentPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformExecutionMode")
    def terraform_execution_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformExecutionMode"))

    @terraform_execution_mode.setter
    def terraform_execution_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01c1a9c4f72d8020b2bf62b0b82cd4ab7557835cd36e273972c37a14e5878e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformExecutionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformNoCodeModuleId")
    def terraform_no_code_module_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformNoCodeModuleId"))

    @terraform_no_code_module_id.setter
    def terraform_no_code_module_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4da8244973ba469f6b3a6f29e789019429363abe9d49d38e29e473e87ca89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformNoCodeModuleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformNoCodeModuleSource")
    def terraform_no_code_module_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformNoCodeModuleSource"))

    @terraform_no_code_module_source.setter
    def terraform_no_code_module_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6fadd41603d70672814a96fa31b87b200bffaa1bcc740040912c7a4c5d81b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformNoCodeModuleSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformProjectId")
    def terraform_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformProjectId"))

    @terraform_project_id.setter
    def terraform_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a0d209cb50be6ce5c770d95921f8d0e01511b5b73755fd35a125fe1e282a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformProjectId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointAddOnDefinition.WaypointAddOnDefinitionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "description": "description",
        "name": "name",
        "summary": "summary",
        "terraform_no_code_module_id": "terraformNoCodeModuleId",
        "terraform_no_code_module_source": "terraformNoCodeModuleSource",
        "terraform_project_id": "terraformProjectId",
        "labels": "labels",
        "project_id": "projectId",
        "readme_markdown_template": "readmeMarkdownTemplate",
        "terraform_agent_pool_id": "terraformAgentPoolId",
        "terraform_cloud_workspace_details": "terraformCloudWorkspaceDetails",
        "terraform_execution_mode": "terraformExecutionMode",
        "variable_options": "variableOptions",
    },
)
class WaypointAddOnDefinitionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: builtins.str,
        name: builtins.str,
        summary: builtins.str,
        terraform_no_code_module_id: builtins.str,
        terraform_no_code_module_source: builtins.str,
        terraform_project_id: builtins.str,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_id: typing.Optional[builtins.str] = None,
        readme_markdown_template: typing.Optional[builtins.str] = None,
        terraform_agent_pool_id: typing.Optional[builtins.str] = None,
        terraform_cloud_workspace_details: typing.Optional[typing.Union["WaypointAddOnDefinitionTerraformCloudWorkspaceDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        terraform_execution_mode: typing.Optional[builtins.str] = None,
        variable_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WaypointAddOnDefinitionVariableOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: A longer description of the Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#description WaypointAddOnDefinition#description}
        :param name: The name of the Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#name WaypointAddOnDefinition#name}
        :param summary: A short summary of the Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#summary WaypointAddOnDefinition#summary}
        :param terraform_no_code_module_id: The ID of the Terraform no-code module to use for running Terraform operations. This is in the format of 'nocode-'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_no_code_module_id WaypointAddOnDefinition#terraform_no_code_module_id}
        :param terraform_no_code_module_source: Terraform Cloud no-code Module Source, expected to be in one of the following formats: "app.terraform.io/hcp_waypoint_example/ecs-advanced-microservice/aws" or "private/hcp_waypoint_example/ecs-advanced-microservice/aws". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_no_code_module_source WaypointAddOnDefinition#terraform_no_code_module_source}
        :param terraform_project_id: The ID of the Terraform Cloud Project to create workspaces in. The ID is found on the Terraform Cloud Project settings page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_project_id WaypointAddOnDefinition#terraform_project_id}
        :param labels: List of labels attached to this Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#labels WaypointAddOnDefinition#labels}
        :param project_id: The ID of the HCP project where the Waypoint Add-on Definition is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#project_id WaypointAddOnDefinition#project_id}
        :param readme_markdown_template: The markdown template for the Add-on Definition README (markdown format supported). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#readme_markdown_template WaypointAddOnDefinition#readme_markdown_template}
        :param terraform_agent_pool_id: The ID of the Terraform agent pool to use for running Terraform operations. This is only applicable when the execution mode is set to 'agent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_agent_pool_id WaypointAddOnDefinition#terraform_agent_pool_id}
        :param terraform_cloud_workspace_details: Terraform Cloud Workspace details. If not provided, defaults to the HCP Terraform project of the associated application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_cloud_workspace_details WaypointAddOnDefinition#terraform_cloud_workspace_details}
        :param terraform_execution_mode: The execution mode of the HCP Terraform workspaces for add-ons using this add-on definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_execution_mode WaypointAddOnDefinition#terraform_execution_mode}
        :param variable_options: List of variable options for the Add-on Definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#variable_options WaypointAddOnDefinition#variable_options}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(terraform_cloud_workspace_details, dict):
            terraform_cloud_workspace_details = WaypointAddOnDefinitionTerraformCloudWorkspaceDetails(**terraform_cloud_workspace_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40a2cbc7571adb614c8a0532c8a86107dd834e783021898b5df56a91c33947c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument summary", value=summary, expected_type=type_hints["summary"])
            check_type(argname="argument terraform_no_code_module_id", value=terraform_no_code_module_id, expected_type=type_hints["terraform_no_code_module_id"])
            check_type(argname="argument terraform_no_code_module_source", value=terraform_no_code_module_source, expected_type=type_hints["terraform_no_code_module_source"])
            check_type(argname="argument terraform_project_id", value=terraform_project_id, expected_type=type_hints["terraform_project_id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument readme_markdown_template", value=readme_markdown_template, expected_type=type_hints["readme_markdown_template"])
            check_type(argname="argument terraform_agent_pool_id", value=terraform_agent_pool_id, expected_type=type_hints["terraform_agent_pool_id"])
            check_type(argname="argument terraform_cloud_workspace_details", value=terraform_cloud_workspace_details, expected_type=type_hints["terraform_cloud_workspace_details"])
            check_type(argname="argument terraform_execution_mode", value=terraform_execution_mode, expected_type=type_hints["terraform_execution_mode"])
            check_type(argname="argument variable_options", value=variable_options, expected_type=type_hints["variable_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "name": name,
            "summary": summary,
            "terraform_no_code_module_id": terraform_no_code_module_id,
            "terraform_no_code_module_source": terraform_no_code_module_source,
            "terraform_project_id": terraform_project_id,
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
        if labels is not None:
            self._values["labels"] = labels
        if project_id is not None:
            self._values["project_id"] = project_id
        if readme_markdown_template is not None:
            self._values["readme_markdown_template"] = readme_markdown_template
        if terraform_agent_pool_id is not None:
            self._values["terraform_agent_pool_id"] = terraform_agent_pool_id
        if terraform_cloud_workspace_details is not None:
            self._values["terraform_cloud_workspace_details"] = terraform_cloud_workspace_details
        if terraform_execution_mode is not None:
            self._values["terraform_execution_mode"] = terraform_execution_mode
        if variable_options is not None:
            self._values["variable_options"] = variable_options

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
    def description(self) -> builtins.str:
        '''A longer description of the Add-on Definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#description WaypointAddOnDefinition#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Add-on Definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#name WaypointAddOnDefinition#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def summary(self) -> builtins.str:
        '''A short summary of the Add-on Definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#summary WaypointAddOnDefinition#summary}
        '''
        result = self._values.get("summary")
        assert result is not None, "Required property 'summary' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_no_code_module_id(self) -> builtins.str:
        '''The ID of the Terraform no-code module to use for running Terraform operations.

        This is in the format of 'nocode-'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_no_code_module_id WaypointAddOnDefinition#terraform_no_code_module_id}
        '''
        result = self._values.get("terraform_no_code_module_id")
        assert result is not None, "Required property 'terraform_no_code_module_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_no_code_module_source(self) -> builtins.str:
        '''Terraform Cloud no-code Module Source, expected to be in one of the following formats: "app.terraform.io/hcp_waypoint_example/ecs-advanced-microservice/aws" or "private/hcp_waypoint_example/ecs-advanced-microservice/aws".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_no_code_module_source WaypointAddOnDefinition#terraform_no_code_module_source}
        '''
        result = self._values.get("terraform_no_code_module_source")
        assert result is not None, "Required property 'terraform_no_code_module_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_project_id(self) -> builtins.str:
        '''The ID of the Terraform Cloud Project to create workspaces in.

        The ID is found on the Terraform Cloud Project settings page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_project_id WaypointAddOnDefinition#terraform_project_id}
        '''
        result = self._values.get("terraform_project_id")
        assert result is not None, "Required property 'terraform_project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of labels attached to this Add-on Definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#labels WaypointAddOnDefinition#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the HCP project where the Waypoint Add-on Definition is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#project_id WaypointAddOnDefinition#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme_markdown_template(self) -> typing.Optional[builtins.str]:
        '''The markdown template for the Add-on Definition README (markdown format supported).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#readme_markdown_template WaypointAddOnDefinition#readme_markdown_template}
        '''
        result = self._values.get("readme_markdown_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terraform_agent_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Terraform agent pool to use for running Terraform operations.

        This is only applicable when the execution mode is set to 'agent'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_agent_pool_id WaypointAddOnDefinition#terraform_agent_pool_id}
        '''
        result = self._values.get("terraform_agent_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terraform_cloud_workspace_details(
        self,
    ) -> typing.Optional["WaypointAddOnDefinitionTerraformCloudWorkspaceDetails"]:
        '''Terraform Cloud Workspace details. If not provided, defaults to the HCP Terraform project of the associated application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_cloud_workspace_details WaypointAddOnDefinition#terraform_cloud_workspace_details}
        '''
        result = self._values.get("terraform_cloud_workspace_details")
        return typing.cast(typing.Optional["WaypointAddOnDefinitionTerraformCloudWorkspaceDetails"], result)

    @builtins.property
    def terraform_execution_mode(self) -> typing.Optional[builtins.str]:
        '''The execution mode of the HCP Terraform workspaces for add-ons using this add-on definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_execution_mode WaypointAddOnDefinition#terraform_execution_mode}
        '''
        result = self._values.get("terraform_execution_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variable_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WaypointAddOnDefinitionVariableOptions"]]]:
        '''List of variable options for the Add-on Definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#variable_options WaypointAddOnDefinition#variable_options}
        '''
        result = self._values.get("variable_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WaypointAddOnDefinitionVariableOptions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointAddOnDefinitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointAddOnDefinition.WaypointAddOnDefinitionTerraformCloudWorkspaceDetails",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "terraform_project_id": "terraformProjectId"},
)
class WaypointAddOnDefinitionTerraformCloudWorkspaceDetails:
    def __init__(
        self,
        *,
        name: builtins.str,
        terraform_project_id: builtins.str,
    ) -> None:
        '''
        :param name: Name of the Terraform Cloud Project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#name WaypointAddOnDefinition#name}
        :param terraform_project_id: Terraform Cloud Project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_project_id WaypointAddOnDefinition#terraform_project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47af780e6812a10dbd9e57daea3b71738809a49206fca17d31d7a6b3b2315fac)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument terraform_project_id", value=terraform_project_id, expected_type=type_hints["terraform_project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "terraform_project_id": terraform_project_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Terraform Cloud Project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#name WaypointAddOnDefinition#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_project_id(self) -> builtins.str:
        '''Terraform Cloud Project ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#terraform_project_id WaypointAddOnDefinition#terraform_project_id}
        '''
        result = self._values.get("terraform_project_id")
        assert result is not None, "Required property 'terraform_project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointAddOnDefinitionTerraformCloudWorkspaceDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WaypointAddOnDefinitionTerraformCloudWorkspaceDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointAddOnDefinition.WaypointAddOnDefinitionTerraformCloudWorkspaceDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46eec1c20996930cb3e69621bd80aff391b9259e1d65b7281201ebcc5c8f7bd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="terraformProjectIdInput")
    def terraform_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6da2bbe02b80a5b4b00120c0196d7dcbf1dd48fcd0ee500a0f032a7f3de467a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformProjectId")
    def terraform_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformProjectId"))

    @terraform_project_id.setter
    def terraform_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9d847eb5b9b53c5832551b5df56d2edd77dd25d0b987551d6839fd3a1b2f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointAddOnDefinitionTerraformCloudWorkspaceDetails]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointAddOnDefinitionTerraformCloudWorkspaceDetails]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointAddOnDefinitionTerraformCloudWorkspaceDetails]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3855be17e5c38327e1dbc815a7d66891eabf9e89c72d00cd00c99afbad885787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointAddOnDefinition.WaypointAddOnDefinitionVariableOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "variable_type": "variableType",
        "options": "options",
        "user_editable": "userEditable",
    },
)
class WaypointAddOnDefinitionVariableOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        variable_type: builtins.str,
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_editable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Variable name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#name WaypointAddOnDefinition#name}
        :param variable_type: Variable type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#variable_type WaypointAddOnDefinition#variable_type}
        :param options: List of options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#options WaypointAddOnDefinition#options}
        :param user_editable: Whether the variable is editable by the user creating an add-on. If options are provided, then the user may only use those options, regardless of this setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#user_editable WaypointAddOnDefinition#user_editable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7646e0a9112c86b9ef8b36b0278f68d36a7c44ce18fe4e015ab9188bc6dab6af)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument variable_type", value=variable_type, expected_type=type_hints["variable_type"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument user_editable", value=user_editable, expected_type=type_hints["user_editable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "variable_type": variable_type,
        }
        if options is not None:
            self._values["options"] = options
        if user_editable is not None:
            self._values["user_editable"] = user_editable

    @builtins.property
    def name(self) -> builtins.str:
        '''Variable name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#name WaypointAddOnDefinition#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def variable_type(self) -> builtins.str:
        '''Variable type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#variable_type WaypointAddOnDefinition#variable_type}
        '''
        result = self._values.get("variable_type")
        assert result is not None, "Required property 'variable_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#options WaypointAddOnDefinition#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_editable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the variable is editable by the user creating an add-on.

        If options are provided, then the user may only use those options, regardless of this setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_add_on_definition#user_editable WaypointAddOnDefinition#user_editable}
        '''
        result = self._values.get("user_editable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointAddOnDefinitionVariableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WaypointAddOnDefinitionVariableOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointAddOnDefinition.WaypointAddOnDefinitionVariableOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b00e595357cd29d39989704360e8887023996ee75635eea899c9d45d8c54beeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WaypointAddOnDefinitionVariableOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190cf7b2bbe0a2634c5df0d923ba99cdff7a1fb5bedca67b23639587d68f1088)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WaypointAddOnDefinitionVariableOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91862c38c7f051b1a2dcf024aa703c537fa5df9affef9395b9d064a5ffcdf204)
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
            type_hints = typing.get_type_hints(_typecheckingstub__913439af155bfa8d7c2411ef0fced64f21b496e0dbd8bf2f9ddb5df348548a81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85b1742e34f856b39c50db3ade0ada01a2bb305182d5407cb65d38c46411ff35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WaypointAddOnDefinitionVariableOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WaypointAddOnDefinitionVariableOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WaypointAddOnDefinitionVariableOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c9dcbbcd0b8abfd32be9132fce3599051c7ac44c8c551b5203a3613f709af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WaypointAddOnDefinitionVariableOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointAddOnDefinition.WaypointAddOnDefinitionVariableOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3783914cf57fbadd0563d000439477e8fd9a16909a77dfcf8fd97824f7f6e7ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetUserEditable")
    def reset_user_editable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserEditable", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="userEditableInput")
    def user_editable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userEditableInput"))

    @builtins.property
    @jsii.member(jsii_name="variableTypeInput")
    def variable_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variableTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0c961c1dcf693c49f5dc354859cfd733cc97884b675f3cb346a4619ec63702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562f8a286c004d2f3e252d811a1f92c7d26009def1da7ceb16a31ff015df0cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userEditable")
    def user_editable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "userEditable"))

    @user_editable.setter
    def user_editable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb4fc4e0a68190f64dcbf9abf3bd768f920df48095cfd53370d7aa1cee16294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEditable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variableType")
    def variable_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variableType"))

    @variable_type.setter
    def variable_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a83700ea10fca175431ac526c96c63ae5fb3a785e5b513dc95c2958722974b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variableType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointAddOnDefinitionVariableOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointAddOnDefinitionVariableOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointAddOnDefinitionVariableOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d3137057d512118661b57ab0c37376c7e1584c0831d1c51940d25515a7a0f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WaypointAddOnDefinition",
    "WaypointAddOnDefinitionConfig",
    "WaypointAddOnDefinitionTerraformCloudWorkspaceDetails",
    "WaypointAddOnDefinitionTerraformCloudWorkspaceDetailsOutputReference",
    "WaypointAddOnDefinitionVariableOptions",
    "WaypointAddOnDefinitionVariableOptionsList",
    "WaypointAddOnDefinitionVariableOptionsOutputReference",
]

publication.publish()

def _typecheckingstub__228a48df25a261b668774144693c4eff33450f646342dbb58693c15b2c1aa9b9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: builtins.str,
    name: builtins.str,
    summary: builtins.str,
    terraform_no_code_module_id: builtins.str,
    terraform_no_code_module_source: builtins.str,
    terraform_project_id: builtins.str,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    project_id: typing.Optional[builtins.str] = None,
    readme_markdown_template: typing.Optional[builtins.str] = None,
    terraform_agent_pool_id: typing.Optional[builtins.str] = None,
    terraform_cloud_workspace_details: typing.Optional[typing.Union[WaypointAddOnDefinitionTerraformCloudWorkspaceDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    terraform_execution_mode: typing.Optional[builtins.str] = None,
    variable_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WaypointAddOnDefinitionVariableOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__2a92ada119c0a532b472e365d34a9a0ffd135ffce66552e97a1b089d14db6e43(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964621e2c2a33d3954f02bf3d1bb1be659d7cffcbdf6639bf86e1878616041de(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WaypointAddOnDefinitionVariableOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848b9ec45669c16c71902265fa5b2c111e23df57ca3b89561e2299ffd64d2685(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437dbd9280036805298e97467c3303b62333bf8bb4610e30903dc895ca7b7a33(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7eab7b2b83d1fbbfce11dfee65a0e63ba15f6715fb0b6cc7594642b8c804a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf644f29b299073cce6f2463c54a924ebd0d80084d04db9dfec8cce10a3ddd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f722d58a72bba34fdf713aca00de214a7e720ac0700ecaefd86c2417824760bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605b12050a84e5c69b93ec0ff96f6886075d6e7a323a4e0008211b0a4569bdef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ad2d2a1ba809a1b331b19b3ee1889865fa4c673f5ed3c95debe575086e2e8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01c1a9c4f72d8020b2bf62b0b82cd4ab7557835cd36e273972c37a14e5878e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4da8244973ba469f6b3a6f29e789019429363abe9d49d38e29e473e87ca89e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6fadd41603d70672814a96fa31b87b200bffaa1bcc740040912c7a4c5d81b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a0d209cb50be6ce5c770d95921f8d0e01511b5b73755fd35a125fe1e282a07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40a2cbc7571adb614c8a0532c8a86107dd834e783021898b5df56a91c33947c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: builtins.str,
    name: builtins.str,
    summary: builtins.str,
    terraform_no_code_module_id: builtins.str,
    terraform_no_code_module_source: builtins.str,
    terraform_project_id: builtins.str,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    project_id: typing.Optional[builtins.str] = None,
    readme_markdown_template: typing.Optional[builtins.str] = None,
    terraform_agent_pool_id: typing.Optional[builtins.str] = None,
    terraform_cloud_workspace_details: typing.Optional[typing.Union[WaypointAddOnDefinitionTerraformCloudWorkspaceDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    terraform_execution_mode: typing.Optional[builtins.str] = None,
    variable_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WaypointAddOnDefinitionVariableOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47af780e6812a10dbd9e57daea3b71738809a49206fca17d31d7a6b3b2315fac(
    *,
    name: builtins.str,
    terraform_project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46eec1c20996930cb3e69621bd80aff391b9259e1d65b7281201ebcc5c8f7bd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6da2bbe02b80a5b4b00120c0196d7dcbf1dd48fcd0ee500a0f032a7f3de467a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9d847eb5b9b53c5832551b5df56d2edd77dd25d0b987551d6839fd3a1b2f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3855be17e5c38327e1dbc815a7d66891eabf9e89c72d00cd00c99afbad885787(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointAddOnDefinitionTerraformCloudWorkspaceDetails]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7646e0a9112c86b9ef8b36b0278f68d36a7c44ce18fe4e015ab9188bc6dab6af(
    *,
    name: builtins.str,
    variable_type: builtins.str,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_editable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00e595357cd29d39989704360e8887023996ee75635eea899c9d45d8c54beeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190cf7b2bbe0a2634c5df0d923ba99cdff7a1fb5bedca67b23639587d68f1088(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91862c38c7f051b1a2dcf024aa703c537fa5df9affef9395b9d064a5ffcdf204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913439af155bfa8d7c2411ef0fced64f21b496e0dbd8bf2f9ddb5df348548a81(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b1742e34f856b39c50db3ade0ada01a2bb305182d5407cb65d38c46411ff35(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c9dcbbcd0b8abfd32be9132fce3599051c7ac44c8c551b5203a3613f709af6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WaypointAddOnDefinitionVariableOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3783914cf57fbadd0563d000439477e8fd9a16909a77dfcf8fd97824f7f6e7ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0c961c1dcf693c49f5dc354859cfd733cc97884b675f3cb346a4619ec63702(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562f8a286c004d2f3e252d811a1f92c7d26009def1da7ceb16a31ff015df0cab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb4fc4e0a68190f64dcbf9abf3bd768f920df48095cfd53370d7aa1cee16294(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a83700ea10fca175431ac526c96c63ae5fb3a785e5b513dc95c2958722974b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3137057d512118661b57ab0c37376c7e1584c0831d1c51940d25515a7a0f89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointAddOnDefinitionVariableOptions]],
) -> None:
    """Type checking stubs"""
    pass
