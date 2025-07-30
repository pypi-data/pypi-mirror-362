r'''
# `hcp_waypoint_template`

Refer to the Terraform Registry for docs: [`hcp_waypoint_template`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template).
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


class WaypointTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointTemplate.WaypointTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template hcp_waypoint_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        summary: builtins.str,
        terraform_no_code_module_id: builtins.str,
        terraform_no_code_module_source: builtins.str,
        terraform_project_id: builtins.str,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_id: typing.Optional[builtins.str] = None,
        readme_markdown_template: typing.Optional[builtins.str] = None,
        terraform_agent_pool_id: typing.Optional[builtins.str] = None,
        terraform_cloud_workspace_details: typing.Optional[typing.Union["WaypointTemplateTerraformCloudWorkspaceDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        terraform_execution_mode: typing.Optional[builtins.str] = None,
        use_module_readme: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        variable_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WaypointTemplateVariableOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template hcp_waypoint_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#name WaypointTemplate#name}
        :param summary: A brief description of the template, up to 110 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#summary WaypointTemplate#summary}
        :param terraform_no_code_module_id: The ID of the Terraform no-code module to use for running Terraform operations. This is in the format of 'nocode-'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_no_code_module_id WaypointTemplate#terraform_no_code_module_id}
        :param terraform_no_code_module_source: Terraform Cloud No-Code Module details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_no_code_module_source WaypointTemplate#terraform_no_code_module_source}
        :param terraform_project_id: The ID of the Terraform Cloud Project to create workspaces in. The ID is found on the Terraform Cloud Project settings page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_project_id WaypointTemplate#terraform_project_id}
        :param actions: List of actions by 'ID' to assign to this Template. Applications created from this Template will have these actions assigned to them. Only 'ID' is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#actions WaypointTemplate#actions}
        :param description: A description of the template, along with when and why it should be used, up to 500 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#description WaypointTemplate#description}
        :param labels: List of labels attached to this Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#labels WaypointTemplate#labels}
        :param project_id: The ID of the HCP project where the Waypoint Template is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#project_id WaypointTemplate#project_id}
        :param readme_markdown_template: Instructions for using the template (markdown format supported). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#readme_markdown_template WaypointTemplate#readme_markdown_template}
        :param terraform_agent_pool_id: The ID of the agent pool to use for Terraform operations, for workspaces created for applications using this template. Required if terraform_execution_mode is set to 'agent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_agent_pool_id WaypointTemplate#terraform_agent_pool_id}
        :param terraform_cloud_workspace_details: Terraform Cloud Workspace details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_cloud_workspace_details WaypointTemplate#terraform_cloud_workspace_details}
        :param terraform_execution_mode: The execution mode of the HCP Terraform workspaces created for applications using this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_execution_mode WaypointTemplate#terraform_execution_mode}
        :param use_module_readme: If true, will auto-import the readme form the Terraform module used. If this is set to true, users should not also set ``readme_markdown_template``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#use_module_readme WaypointTemplate#use_module_readme}
        :param variable_options: List of variable options for the template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#variable_options WaypointTemplate#variable_options}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d93a2c22ceb0c7c2063924c82f78ac18a885651209563e8dfe35b65a38c88f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = WaypointTemplateConfig(
            name=name,
            summary=summary,
            terraform_no_code_module_id=terraform_no_code_module_id,
            terraform_no_code_module_source=terraform_no_code_module_source,
            terraform_project_id=terraform_project_id,
            actions=actions,
            description=description,
            labels=labels,
            project_id=project_id,
            readme_markdown_template=readme_markdown_template,
            terraform_agent_pool_id=terraform_agent_pool_id,
            terraform_cloud_workspace_details=terraform_cloud_workspace_details,
            terraform_execution_mode=terraform_execution_mode,
            use_module_readme=use_module_readme,
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
        '''Generates CDKTF code for importing a WaypointTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WaypointTemplate to import.
        :param import_from_id: The id of the existing WaypointTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WaypointTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754b073703e5b7f43d30c025172aa26c0d18c3cf53d89bde9dced26be96e7294)
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
        :param name: Name of the Terraform Cloud Project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#name WaypointTemplate#name}
        :param terraform_project_id: Terraform Cloud Project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_project_id WaypointTemplate#terraform_project_id}
        '''
        value = WaypointTemplateTerraformCloudWorkspaceDetails(
            name=name, terraform_project_id=terraform_project_id
        )

        return typing.cast(None, jsii.invoke(self, "putTerraformCloudWorkspaceDetails", [value]))

    @jsii.member(jsii_name="putVariableOptions")
    def put_variable_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WaypointTemplateVariableOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92be09f25a4ab9c4cb21f9562cf68ddc29d67c159c99df0b134698273ad794af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariableOptions", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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

    @jsii.member(jsii_name="resetUseModuleReadme")
    def reset_use_module_readme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseModuleReadme", []))

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
    ) -> "WaypointTemplateTerraformCloudWorkspaceDetailsOutputReference":
        return typing.cast("WaypointTemplateTerraformCloudWorkspaceDetailsOutputReference", jsii.get(self, "terraformCloudWorkspaceDetails"))

    @builtins.property
    @jsii.member(jsii_name="variableOptions")
    def variable_options(self) -> "WaypointTemplateVariableOptionsList":
        return typing.cast("WaypointTemplateVariableOptionsList", jsii.get(self, "variableOptions"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WaypointTemplateTerraformCloudWorkspaceDetails"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WaypointTemplateTerraformCloudWorkspaceDetails"]], jsii.get(self, "terraformCloudWorkspaceDetailsInput"))

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
    @jsii.member(jsii_name="useModuleReadmeInput")
    def use_module_readme_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useModuleReadmeInput"))

    @builtins.property
    @jsii.member(jsii_name="variableOptionsInput")
    def variable_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WaypointTemplateVariableOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WaypointTemplateVariableOptions"]]], jsii.get(self, "variableOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fa9cfeb325ba7c69fdb93335eade6742bb030b2f3d584128780aa71574cc39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc2aa1624adbb3df1ef2cd1847d2f3f745ea020cb858d8aa92aa1dc2e5e2fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71590dd89e983e1de44bc44640718859d5d7aeaca69f2a84606f0d1c95884d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e23d0533d8e58a6d6a691e23655a71577836f077151d09e101b6a16b65a2b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe338800a031d4e7b77f258ca80ec6e913537ab613130c1ae0f3396643a47aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readmeMarkdownTemplate")
    def readme_markdown_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readmeMarkdownTemplate"))

    @readme_markdown_template.setter
    def readme_markdown_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2380d797fd9eafbeb393e9c5874d252b8c0a6a4415580552f1b5302d7c3e08e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readmeMarkdownTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="summary")
    def summary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "summary"))

    @summary.setter
    def summary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5f4449b41a59dcc89c0800d657e4a427a510140f759137b8f03c9df0eaa168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "summary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformAgentPoolId")
    def terraform_agent_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformAgentPoolId"))

    @terraform_agent_pool_id.setter
    def terraform_agent_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9ca9262963c916622f8c9b14e1505cc7de3f0ee566f20349d645455b3d780f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAgentPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformExecutionMode")
    def terraform_execution_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformExecutionMode"))

    @terraform_execution_mode.setter
    def terraform_execution_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd062ca11663006ed22c179fd7905a1916f08d2d11c320e82f6eb00ffd61b695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformExecutionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformNoCodeModuleId")
    def terraform_no_code_module_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformNoCodeModuleId"))

    @terraform_no_code_module_id.setter
    def terraform_no_code_module_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625d201d950d5710afaa8d8f5062263d5ae3d01dc0a21365ec4769386993ad56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformNoCodeModuleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformNoCodeModuleSource")
    def terraform_no_code_module_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformNoCodeModuleSource"))

    @terraform_no_code_module_source.setter
    def terraform_no_code_module_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25326e0b1b47f05cae8beb0e078f98e54848d188554f34f5c7d8c1938450200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformNoCodeModuleSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformProjectId")
    def terraform_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformProjectId"))

    @terraform_project_id.setter
    def terraform_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2266edf3348f0eb3a1a1108932a5f4620d782bb6ae318e1467961adfdf038e74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useModuleReadme")
    def use_module_readme(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useModuleReadme"))

    @use_module_readme.setter
    def use_module_readme(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ba9fd073834045844e8a5729be8262ca3aa4964dc0545585a227057e70bcf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useModuleReadme", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointTemplate.WaypointTemplateConfig",
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
        "summary": "summary",
        "terraform_no_code_module_id": "terraformNoCodeModuleId",
        "terraform_no_code_module_source": "terraformNoCodeModuleSource",
        "terraform_project_id": "terraformProjectId",
        "actions": "actions",
        "description": "description",
        "labels": "labels",
        "project_id": "projectId",
        "readme_markdown_template": "readmeMarkdownTemplate",
        "terraform_agent_pool_id": "terraformAgentPoolId",
        "terraform_cloud_workspace_details": "terraformCloudWorkspaceDetails",
        "terraform_execution_mode": "terraformExecutionMode",
        "use_module_readme": "useModuleReadme",
        "variable_options": "variableOptions",
    },
)
class WaypointTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        summary: builtins.str,
        terraform_no_code_module_id: builtins.str,
        terraform_no_code_module_source: builtins.str,
        terraform_project_id: builtins.str,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_id: typing.Optional[builtins.str] = None,
        readme_markdown_template: typing.Optional[builtins.str] = None,
        terraform_agent_pool_id: typing.Optional[builtins.str] = None,
        terraform_cloud_workspace_details: typing.Optional[typing.Union["WaypointTemplateTerraformCloudWorkspaceDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        terraform_execution_mode: typing.Optional[builtins.str] = None,
        use_module_readme: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        variable_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WaypointTemplateVariableOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#name WaypointTemplate#name}
        :param summary: A brief description of the template, up to 110 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#summary WaypointTemplate#summary}
        :param terraform_no_code_module_id: The ID of the Terraform no-code module to use for running Terraform operations. This is in the format of 'nocode-'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_no_code_module_id WaypointTemplate#terraform_no_code_module_id}
        :param terraform_no_code_module_source: Terraform Cloud No-Code Module details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_no_code_module_source WaypointTemplate#terraform_no_code_module_source}
        :param terraform_project_id: The ID of the Terraform Cloud Project to create workspaces in. The ID is found on the Terraform Cloud Project settings page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_project_id WaypointTemplate#terraform_project_id}
        :param actions: List of actions by 'ID' to assign to this Template. Applications created from this Template will have these actions assigned to them. Only 'ID' is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#actions WaypointTemplate#actions}
        :param description: A description of the template, along with when and why it should be used, up to 500 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#description WaypointTemplate#description}
        :param labels: List of labels attached to this Template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#labels WaypointTemplate#labels}
        :param project_id: The ID of the HCP project where the Waypoint Template is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#project_id WaypointTemplate#project_id}
        :param readme_markdown_template: Instructions for using the template (markdown format supported). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#readme_markdown_template WaypointTemplate#readme_markdown_template}
        :param terraform_agent_pool_id: The ID of the agent pool to use for Terraform operations, for workspaces created for applications using this template. Required if terraform_execution_mode is set to 'agent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_agent_pool_id WaypointTemplate#terraform_agent_pool_id}
        :param terraform_cloud_workspace_details: Terraform Cloud Workspace details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_cloud_workspace_details WaypointTemplate#terraform_cloud_workspace_details}
        :param terraform_execution_mode: The execution mode of the HCP Terraform workspaces created for applications using this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_execution_mode WaypointTemplate#terraform_execution_mode}
        :param use_module_readme: If true, will auto-import the readme form the Terraform module used. If this is set to true, users should not also set ``readme_markdown_template``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#use_module_readme WaypointTemplate#use_module_readme}
        :param variable_options: List of variable options for the template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#variable_options WaypointTemplate#variable_options}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(terraform_cloud_workspace_details, dict):
            terraform_cloud_workspace_details = WaypointTemplateTerraformCloudWorkspaceDetails(**terraform_cloud_workspace_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb798a134f7ce51e6d907918b88d4944226fa55e9519ea7f7effbfa1142d3e8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument summary", value=summary, expected_type=type_hints["summary"])
            check_type(argname="argument terraform_no_code_module_id", value=terraform_no_code_module_id, expected_type=type_hints["terraform_no_code_module_id"])
            check_type(argname="argument terraform_no_code_module_source", value=terraform_no_code_module_source, expected_type=type_hints["terraform_no_code_module_source"])
            check_type(argname="argument terraform_project_id", value=terraform_project_id, expected_type=type_hints["terraform_project_id"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument readme_markdown_template", value=readme_markdown_template, expected_type=type_hints["readme_markdown_template"])
            check_type(argname="argument terraform_agent_pool_id", value=terraform_agent_pool_id, expected_type=type_hints["terraform_agent_pool_id"])
            check_type(argname="argument terraform_cloud_workspace_details", value=terraform_cloud_workspace_details, expected_type=type_hints["terraform_cloud_workspace_details"])
            check_type(argname="argument terraform_execution_mode", value=terraform_execution_mode, expected_type=type_hints["terraform_execution_mode"])
            check_type(argname="argument use_module_readme", value=use_module_readme, expected_type=type_hints["use_module_readme"])
            check_type(argname="argument variable_options", value=variable_options, expected_type=type_hints["variable_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if actions is not None:
            self._values["actions"] = actions
        if description is not None:
            self._values["description"] = description
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
        if use_module_readme is not None:
            self._values["use_module_readme"] = use_module_readme
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
    def name(self) -> builtins.str:
        '''The name of the Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#name WaypointTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def summary(self) -> builtins.str:
        '''A brief description of the template, up to 110 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#summary WaypointTemplate#summary}
        '''
        result = self._values.get("summary")
        assert result is not None, "Required property 'summary' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_no_code_module_id(self) -> builtins.str:
        '''The ID of the Terraform no-code module to use for running Terraform operations.

        This is in the format of 'nocode-'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_no_code_module_id WaypointTemplate#terraform_no_code_module_id}
        '''
        result = self._values.get("terraform_no_code_module_id")
        assert result is not None, "Required property 'terraform_no_code_module_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_no_code_module_source(self) -> builtins.str:
        '''Terraform Cloud No-Code Module details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_no_code_module_source WaypointTemplate#terraform_no_code_module_source}
        '''
        result = self._values.get("terraform_no_code_module_source")
        assert result is not None, "Required property 'terraform_no_code_module_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_project_id(self) -> builtins.str:
        '''The ID of the Terraform Cloud Project to create workspaces in.

        The ID is found on the Terraform Cloud Project settings page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_project_id WaypointTemplate#terraform_project_id}
        '''
        result = self._values.get("terraform_project_id")
        assert result is not None, "Required property 'terraform_project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of actions by 'ID' to assign to this Template.

        Applications created from this Template will have these actions assigned to them. Only 'ID' is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#actions WaypointTemplate#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the template, along with when and why it should be used, up to 500 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#description WaypointTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of labels attached to this Template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#labels WaypointTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the HCP project where the Waypoint Template is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#project_id WaypointTemplate#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme_markdown_template(self) -> typing.Optional[builtins.str]:
        '''Instructions for using the template (markdown format supported).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#readme_markdown_template WaypointTemplate#readme_markdown_template}
        '''
        result = self._values.get("readme_markdown_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terraform_agent_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the agent pool to use for Terraform operations, for workspaces created for applications using this template.

        Required if terraform_execution_mode is set to 'agent'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_agent_pool_id WaypointTemplate#terraform_agent_pool_id}
        '''
        result = self._values.get("terraform_agent_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terraform_cloud_workspace_details(
        self,
    ) -> typing.Optional["WaypointTemplateTerraformCloudWorkspaceDetails"]:
        '''Terraform Cloud Workspace details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_cloud_workspace_details WaypointTemplate#terraform_cloud_workspace_details}
        '''
        result = self._values.get("terraform_cloud_workspace_details")
        return typing.cast(typing.Optional["WaypointTemplateTerraformCloudWorkspaceDetails"], result)

    @builtins.property
    def terraform_execution_mode(self) -> typing.Optional[builtins.str]:
        '''The execution mode of the HCP Terraform workspaces created for applications using this template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_execution_mode WaypointTemplate#terraform_execution_mode}
        '''
        result = self._values.get("terraform_execution_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_module_readme(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, will auto-import the readme form the Terraform module used.

        If this is set to true, users should not also set ``readme_markdown_template``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#use_module_readme WaypointTemplate#use_module_readme}
        '''
        result = self._values.get("use_module_readme")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def variable_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WaypointTemplateVariableOptions"]]]:
        '''List of variable options for the template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#variable_options WaypointTemplate#variable_options}
        '''
        result = self._values.get("variable_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WaypointTemplateVariableOptions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointTemplate.WaypointTemplateTerraformCloudWorkspaceDetails",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "terraform_project_id": "terraformProjectId"},
)
class WaypointTemplateTerraformCloudWorkspaceDetails:
    def __init__(
        self,
        *,
        name: builtins.str,
        terraform_project_id: builtins.str,
    ) -> None:
        '''
        :param name: Name of the Terraform Cloud Project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#name WaypointTemplate#name}
        :param terraform_project_id: Terraform Cloud Project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_project_id WaypointTemplate#terraform_project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f4c19f5ab894e5dda95911e7033b9c487ceecbcd9091ecea5d84e2e113c480)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument terraform_project_id", value=terraform_project_id, expected_type=type_hints["terraform_project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "terraform_project_id": terraform_project_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Terraform Cloud Project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#name WaypointTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_project_id(self) -> builtins.str:
        '''Terraform Cloud Project ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#terraform_project_id WaypointTemplate#terraform_project_id}
        '''
        result = self._values.get("terraform_project_id")
        assert result is not None, "Required property 'terraform_project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointTemplateTerraformCloudWorkspaceDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WaypointTemplateTerraformCloudWorkspaceDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointTemplate.WaypointTemplateTerraformCloudWorkspaceDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7be23973618c91db4ff487d15951eda05800a095e2e27f35a7640e0348d0bed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6eb4f6809114699c7f96fe1ce8c617754e9caa5ec5826eba87000f3bf1ef6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformProjectId")
    def terraform_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformProjectId"))

    @terraform_project_id.setter
    def terraform_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80454f54ca4200f7a78a6688ee1d9813f3a9043bfb6709eef5332d90bd82d77d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointTemplateTerraformCloudWorkspaceDetails]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointTemplateTerraformCloudWorkspaceDetails]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointTemplateTerraformCloudWorkspaceDetails]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d5f9cb682194bf8d077761779ac41ca7784454b997b5196adb1151f533e50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointTemplate.WaypointTemplateVariableOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "variable_type": "variableType",
        "options": "options",
        "user_editable": "userEditable",
    },
)
class WaypointTemplateVariableOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        variable_type: builtins.str,
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_editable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Variable name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#name WaypointTemplate#name}
        :param variable_type: Variable type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#variable_type WaypointTemplate#variable_type}
        :param options: List of options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#options WaypointTemplate#options}
        :param user_editable: Whether the variable is editable by the user creating an application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#user_editable WaypointTemplate#user_editable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba56c1af40163b418372638d060772f18cb5157e59ffc2c39be7e30fb6d9bc9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#name WaypointTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def variable_type(self) -> builtins.str:
        '''Variable type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#variable_type WaypointTemplate#variable_type}
        '''
        result = self._values.get("variable_type")
        assert result is not None, "Required property 'variable_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#options WaypointTemplate#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_editable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the variable is editable by the user creating an application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_template#user_editable WaypointTemplate#user_editable}
        '''
        result = self._values.get("user_editable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointTemplateVariableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WaypointTemplateVariableOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointTemplate.WaypointTemplateVariableOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4ec761272c813e7a482d0d5fc448cd2c0e639d19b4baf223e75280ca3145c76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WaypointTemplateVariableOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063c31d97014ea8f27a106491ab18a508046c0849cb717ab3d6a8c794dd08c29)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WaypointTemplateVariableOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec484395caae1472ee1d4f7ca4062b0429278e1c75911cc25bb54f1405f8b78b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21c85c497aff00053518a6ae1ad7091eb6d2bf34fed8deea1f10680b262d2937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7219cf655ef6d185911d31a2efb8c2b701f8643ba143d980ff17df417d51e84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WaypointTemplateVariableOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WaypointTemplateVariableOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WaypointTemplateVariableOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e19213ae453a75a0f9954b36fe9c132f80525bac6e09b02842ff1375d4cb08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WaypointTemplateVariableOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointTemplate.WaypointTemplateVariableOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0461135a299f58b3c794fde20316164b9aa3ff58473f38b9ed69a106aeb07298)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9307a73f9ec5f2dad4f7ce00c18f48ee1c33fad69687ea697699545fc593d3e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19f950b9e2f7fb1367d7e5290bfa0ad202aaef4fbbfeb7afd61be461ec0577a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dccf1dbf751f7dbb361bb4b77c0800a975f71b0b0a5c2d97764101c778072fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEditable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variableType")
    def variable_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variableType"))

    @variable_type.setter
    def variable_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681a75395b9755a394bf175abf81469dc10b747e2e1ada363071a6ac5af6bb03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variableType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointTemplateVariableOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointTemplateVariableOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointTemplateVariableOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c760b2794b776fecd8eff96183f1f308d8c2cf19e8e1cdcc6f13216296c8ae76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WaypointTemplate",
    "WaypointTemplateConfig",
    "WaypointTemplateTerraformCloudWorkspaceDetails",
    "WaypointTemplateTerraformCloudWorkspaceDetailsOutputReference",
    "WaypointTemplateVariableOptions",
    "WaypointTemplateVariableOptionsList",
    "WaypointTemplateVariableOptionsOutputReference",
]

publication.publish()

def _typecheckingstub__8d93a2c22ceb0c7c2063924c82f78ac18a885651209563e8dfe35b65a38c88f2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    summary: builtins.str,
    terraform_no_code_module_id: builtins.str,
    terraform_no_code_module_source: builtins.str,
    terraform_project_id: builtins.str,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    project_id: typing.Optional[builtins.str] = None,
    readme_markdown_template: typing.Optional[builtins.str] = None,
    terraform_agent_pool_id: typing.Optional[builtins.str] = None,
    terraform_cloud_workspace_details: typing.Optional[typing.Union[WaypointTemplateTerraformCloudWorkspaceDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    terraform_execution_mode: typing.Optional[builtins.str] = None,
    use_module_readme: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    variable_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WaypointTemplateVariableOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__754b073703e5b7f43d30c025172aa26c0d18c3cf53d89bde9dced26be96e7294(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92be09f25a4ab9c4cb21f9562cf68ddc29d67c159c99df0b134698273ad794af(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WaypointTemplateVariableOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fa9cfeb325ba7c69fdb93335eade6742bb030b2f3d584128780aa71574cc39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc2aa1624adbb3df1ef2cd1847d2f3f745ea020cb858d8aa92aa1dc2e5e2fd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71590dd89e983e1de44bc44640718859d5d7aeaca69f2a84606f0d1c95884d0a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e23d0533d8e58a6d6a691e23655a71577836f077151d09e101b6a16b65a2b6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe338800a031d4e7b77f258ca80ec6e913537ab613130c1ae0f3396643a47aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2380d797fd9eafbeb393e9c5874d252b8c0a6a4415580552f1b5302d7c3e08e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5f4449b41a59dcc89c0800d657e4a427a510140f759137b8f03c9df0eaa168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9ca9262963c916622f8c9b14e1505cc7de3f0ee566f20349d645455b3d780f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd062ca11663006ed22c179fd7905a1916f08d2d11c320e82f6eb00ffd61b695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625d201d950d5710afaa8d8f5062263d5ae3d01dc0a21365ec4769386993ad56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25326e0b1b47f05cae8beb0e078f98e54848d188554f34f5c7d8c1938450200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2266edf3348f0eb3a1a1108932a5f4620d782bb6ae318e1467961adfdf038e74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ba9fd073834045844e8a5729be8262ca3aa4964dc0545585a227057e70bcf0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb798a134f7ce51e6d907918b88d4944226fa55e9519ea7f7effbfa1142d3e8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    summary: builtins.str,
    terraform_no_code_module_id: builtins.str,
    terraform_no_code_module_source: builtins.str,
    terraform_project_id: builtins.str,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    project_id: typing.Optional[builtins.str] = None,
    readme_markdown_template: typing.Optional[builtins.str] = None,
    terraform_agent_pool_id: typing.Optional[builtins.str] = None,
    terraform_cloud_workspace_details: typing.Optional[typing.Union[WaypointTemplateTerraformCloudWorkspaceDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    terraform_execution_mode: typing.Optional[builtins.str] = None,
    use_module_readme: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    variable_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WaypointTemplateVariableOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f4c19f5ab894e5dda95911e7033b9c487ceecbcd9091ecea5d84e2e113c480(
    *,
    name: builtins.str,
    terraform_project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7be23973618c91db4ff487d15951eda05800a095e2e27f35a7640e0348d0bed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6eb4f6809114699c7f96fe1ce8c617754e9caa5ec5826eba87000f3bf1ef6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80454f54ca4200f7a78a6688ee1d9813f3a9043bfb6709eef5332d90bd82d77d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d5f9cb682194bf8d077761779ac41ca7784454b997b5196adb1151f533e50a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointTemplateTerraformCloudWorkspaceDetails]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba56c1af40163b418372638d060772f18cb5157e59ffc2c39be7e30fb6d9bc9(
    *,
    name: builtins.str,
    variable_type: builtins.str,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_editable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ec761272c813e7a482d0d5fc448cd2c0e639d19b4baf223e75280ca3145c76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063c31d97014ea8f27a106491ab18a508046c0849cb717ab3d6a8c794dd08c29(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec484395caae1472ee1d4f7ca4062b0429278e1c75911cc25bb54f1405f8b78b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c85c497aff00053518a6ae1ad7091eb6d2bf34fed8deea1f10680b262d2937(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7219cf655ef6d185911d31a2efb8c2b701f8643ba143d980ff17df417d51e84e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e19213ae453a75a0f9954b36fe9c132f80525bac6e09b02842ff1375d4cb08d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WaypointTemplateVariableOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0461135a299f58b3c794fde20316164b9aa3ff58473f38b9ed69a106aeb07298(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9307a73f9ec5f2dad4f7ce00c18f48ee1c33fad69687ea697699545fc593d3e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19f950b9e2f7fb1367d7e5290bfa0ad202aaef4fbbfeb7afd61be461ec0577a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dccf1dbf751f7dbb361bb4b77c0800a975f71b0b0a5c2d97764101c778072fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681a75395b9755a394bf175abf81469dc10b747e2e1ada363071a6ac5af6bb03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c760b2794b776fecd8eff96183f1f308d8c2cf19e8e1cdcc6f13216296c8ae76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointTemplateVariableOptions]],
) -> None:
    """Type checking stubs"""
    pass
