r'''
# `hcp_waypoint_action`

Refer to the Terraform Registry for docs: [`hcp_waypoint_action`](https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action).
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


class WaypointAction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointAction.WaypointAction",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action hcp_waypoint_action}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        request: typing.Union["WaypointActionRequest", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action hcp_waypoint_action} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the Action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#name WaypointAction#name}
        :param request: The kind of HTTP request this should trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#request WaypointAction#request}
        :param description: A description of the Action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#description WaypointAction#description}
        :param project_id: The ID of the HCP project where the Action is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#project_id WaypointAction#project_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24a34500d6c115f9cad8837252f3c64f8c047dc518864267164f46cf26ee014)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = WaypointActionConfig(
            name=name,
            request=request,
            description=description,
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
        '''Generates CDKTF code for importing a WaypointAction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WaypointAction to import.
        :param import_from_id: The id of the existing WaypointAction that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WaypointAction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe55db6c5ed360be0107c19e0df2d0f7956688bb745ea42bd5992407cc91f6d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRequest")
    def put_request(
        self,
        *,
        agent: typing.Optional[typing.Union["WaypointActionRequestAgent", typing.Dict[builtins.str, typing.Any]]] = None,
        custom: typing.Optional[typing.Union["WaypointActionRequestCustom", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: Agent mode allows users to define the agent to use for the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#agent WaypointAction#agent}
        :param custom: Custom mode allows users to define the HTTP method, the request body, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#custom WaypointAction#custom}
        '''
        value = WaypointActionRequest(agent=agent, custom=custom)

        return typing.cast(None, jsii.invoke(self, "putRequest", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="request")
    def request(self) -> "WaypointActionRequestOutputReference":
        return typing.cast("WaypointActionRequestOutputReference", jsii.get(self, "request"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="requestInput")
    def request_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WaypointActionRequest"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WaypointActionRequest"]], jsii.get(self, "requestInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0612448f9d5017ddfca325cb8c9d9eafd32ceca1dabc83e141172ecae38c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d6a77621623f4e2128c435bd80c3baa540e692beff114f3b28cf6c13c23fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77982ebdc15b76c440f3df0ad63c5c226bf376666b990fd70f3c07d9ec69f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointAction.WaypointActionConfig",
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
        "request": "request",
        "description": "description",
        "project_id": "projectId",
    },
)
class WaypointActionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        request: typing.Union["WaypointActionRequest", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
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
        :param name: The name of the Action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#name WaypointAction#name}
        :param request: The kind of HTTP request this should trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#request WaypointAction#request}
        :param description: A description of the Action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#description WaypointAction#description}
        :param project_id: The ID of the HCP project where the Action is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#project_id WaypointAction#project_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(request, dict):
            request = WaypointActionRequest(**request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dcc18507e51326004eae31cbfc5a977b7a353bea03ebe75450d12f30f55536)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument request", value=request, expected_type=type_hints["request"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "request": request,
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
        if description is not None:
            self._values["description"] = description
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
    def name(self) -> builtins.str:
        '''The name of the Action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#name WaypointAction#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request(self) -> "WaypointActionRequest":
        '''The kind of HTTP request this should trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#request WaypointAction#request}
        '''
        result = self._values.get("request")
        assert result is not None, "Required property 'request' is missing"
        return typing.cast("WaypointActionRequest", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the Action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#description WaypointAction#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the HCP project where the Action is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#project_id WaypointAction#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointAction.WaypointActionRequest",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent", "custom": "custom"},
)
class WaypointActionRequest:
    def __init__(
        self,
        *,
        agent: typing.Optional[typing.Union["WaypointActionRequestAgent", typing.Dict[builtins.str, typing.Any]]] = None,
        custom: typing.Optional[typing.Union["WaypointActionRequestCustom", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param agent: Agent mode allows users to define the agent to use for the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#agent WaypointAction#agent}
        :param custom: Custom mode allows users to define the HTTP method, the request body, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#custom WaypointAction#custom}
        '''
        if isinstance(agent, dict):
            agent = WaypointActionRequestAgent(**agent)
        if isinstance(custom, dict):
            custom = WaypointActionRequestCustom(**custom)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd18a9a38418ee949faa6925308fedb346cb09bbe263a4f832a791c5137d135)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent is not None:
            self._values["agent"] = agent
        if custom is not None:
            self._values["custom"] = custom

    @builtins.property
    def agent(self) -> typing.Optional["WaypointActionRequestAgent"]:
        '''Agent mode allows users to define the agent to use for the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#agent WaypointAction#agent}
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional["WaypointActionRequestAgent"], result)

    @builtins.property
    def custom(self) -> typing.Optional["WaypointActionRequestCustom"]:
        '''Custom mode allows users to define the HTTP method, the request body, etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#custom WaypointAction#custom}
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional["WaypointActionRequestCustom"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointActionRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointAction.WaypointActionRequestAgent",
    jsii_struct_bases=[],
    name_mapping={
        "group": "group",
        "operation_id": "operationId",
        "action_run_id": "actionRunId",
        "body": "body",
    },
)
class WaypointActionRequestAgent:
    def __init__(
        self,
        *,
        group: builtins.str,
        operation_id: builtins.str,
        action_run_id: typing.Optional[builtins.str] = None,
        body: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group: The name of the group that the operation is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#group WaypointAction#group}
        :param operation_id: The identifying name of the operation in the agent config file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#operation_id WaypointAction#operation_id}
        :param action_run_id: An optional action run id. If specified the agent will interact with the actions subsystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#action_run_id WaypointAction#action_run_id}
        :param body: Arguments to the operation, specified as JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#body WaypointAction#body}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6d469647f3769e07b36b004985ef7abb00ac126ce955a1d47068153918ba02)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument operation_id", value=operation_id, expected_type=type_hints["operation_id"])
            check_type(argname="argument action_run_id", value=action_run_id, expected_type=type_hints["action_run_id"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
            "operation_id": operation_id,
        }
        if action_run_id is not None:
            self._values["action_run_id"] = action_run_id
        if body is not None:
            self._values["body"] = body

    @builtins.property
    def group(self) -> builtins.str:
        '''The name of the group that the operation is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#group WaypointAction#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operation_id(self) -> builtins.str:
        '''The identifying name of the operation in the agent config file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#operation_id WaypointAction#operation_id}
        '''
        result = self._values.get("operation_id")
        assert result is not None, "Required property 'operation_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_run_id(self) -> typing.Optional[builtins.str]:
        '''An optional action run id. If specified the agent will interact with the actions subsystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#action_run_id WaypointAction#action_run_id}
        '''
        result = self._values.get("action_run_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''Arguments to the operation, specified as JSON.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#body WaypointAction#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointActionRequestAgent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WaypointActionRequestAgentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointAction.WaypointActionRequestAgentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2be9cc858685ffa8faae04aff3527d1b0b41974d5cb03c1c9a4edbf9f4d1f6a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActionRunId")
    def reset_action_run_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionRunId", []))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @builtins.property
    @jsii.member(jsii_name="actionRunIdInput")
    def action_run_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionRunIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="operationIdInput")
    def operation_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="actionRunId")
    def action_run_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionRunId"))

    @action_run_id.setter
    def action_run_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2e119f1521e1aed748670331a4574de1322196fabd653c183f09b832f63f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionRunId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bc7b52bacc2badae3d5adb1c614c2afc0eb1d49874a5b30f94dfebea81e34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb492843bcc84f602720f493da33343f43ef3029f4edd15ae49574ea937edad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationId")
    def operation_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationId"))

    @operation_id.setter
    def operation_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad03599e3ebea2ace1af9b78af3a0e6a0c7f2caa62d9b47f4c7b0d4ef05e510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestAgent]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestAgent]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestAgent]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bfc243d3865b2706d26d9656f1de46a483fbe1f34cacaa8e9f131f0644bf7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.waypointAction.WaypointActionRequestCustom",
    jsii_struct_bases=[],
    name_mapping={
        "method": "method",
        "body": "body",
        "headers": "headers",
        "url": "url",
    },
)
class WaypointActionRequestCustom:
    def __init__(
        self,
        *,
        method: builtins.str,
        body: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: The HTTP method to use for the request. Must be one of: 'GET', 'POST', 'PUT', 'DELETE', or 'PATCH'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#method WaypointAction#method}
        :param body: The body to be submitted with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#body WaypointAction#body}
        :param headers: Key value headers to send with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#headers WaypointAction#headers}
        :param url: The full URL this request should make when invoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#url WaypointAction#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa709303ff77d73309067aee841ef3de0708b7e4bb430fe4e4c18958837ebbff)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "method": method,
        }
        if body is not None:
            self._values["body"] = body
        if headers is not None:
            self._values["headers"] = headers
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def method(self) -> builtins.str:
        '''The HTTP method to use for the request. Must be one of: 'GET', 'POST', 'PUT', 'DELETE', or 'PATCH'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#method WaypointAction#method}
        '''
        result = self._values.get("method")
        assert result is not None, "Required property 'method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''The body to be submitted with the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#body WaypointAction#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key value headers to send with the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#headers WaypointAction#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The full URL this request should make when invoked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#url WaypointAction#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaypointActionRequestCustom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WaypointActionRequestCustomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointAction.WaypointActionRequestCustomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__961faec7aa4cb9fbc49ef2426dbacb82c876300b6265ea5cfc847f32df31fc5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69e035eac03dd89550e7c6f1fea8f6dbe8d9c9c3ee8943564bdfe5e1a444a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ff7f7b43733cdf79a6f7628db97073b6c617a31993a2b887c060d809a9596a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64784ecb28732a6f28084f4929ed84b2e7412c831c58c04c4dd7552d5c973034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4fb7e9c761d968622f5cdeee939878fc6b6445f5ea0f63c7206552d9221968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestCustom]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestCustom]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestCustom]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76902ccb0af0dcf4640d893d88a2cd33adb3ca046d2518458b24cf77d8648c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WaypointActionRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.waypointAction.WaypointActionRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29842bf9897637784b1a698d122c7d68c634b5191e6699ce0345ed85ace27fbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAgent")
    def put_agent(
        self,
        *,
        group: builtins.str,
        operation_id: builtins.str,
        action_run_id: typing.Optional[builtins.str] = None,
        body: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group: The name of the group that the operation is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#group WaypointAction#group}
        :param operation_id: The identifying name of the operation in the agent config file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#operation_id WaypointAction#operation_id}
        :param action_run_id: An optional action run id. If specified the agent will interact with the actions subsystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#action_run_id WaypointAction#action_run_id}
        :param body: Arguments to the operation, specified as JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#body WaypointAction#body}
        '''
        value = WaypointActionRequestAgent(
            group=group,
            operation_id=operation_id,
            action_run_id=action_run_id,
            body=body,
        )

        return typing.cast(None, jsii.invoke(self, "putAgent", [value]))

    @jsii.member(jsii_name="putCustom")
    def put_custom(
        self,
        *,
        method: builtins.str,
        body: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: The HTTP method to use for the request. Must be one of: 'GET', 'POST', 'PUT', 'DELETE', or 'PATCH'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#method WaypointAction#method}
        :param body: The body to be submitted with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#body WaypointAction#body}
        :param headers: Key value headers to send with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#headers WaypointAction#headers}
        :param url: The full URL this request should make when invoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/hcp/0.109.0/docs/resources/waypoint_action#url WaypointAction#url}
        '''
        value = WaypointActionRequestCustom(
            method=method, body=body, headers=headers, url=url
        )

        return typing.cast(None, jsii.invoke(self, "putCustom", [value]))

    @jsii.member(jsii_name="resetAgent")
    def reset_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgent", []))

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> WaypointActionRequestAgentOutputReference:
        return typing.cast(WaypointActionRequestAgentOutputReference, jsii.get(self, "agent"))

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(self) -> WaypointActionRequestCustomOutputReference:
        return typing.cast(WaypointActionRequestCustomOutputReference, jsii.get(self, "custom"))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestAgent]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestAgent]], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestCustom]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestCustom]], jsii.get(self, "customInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequest]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequest]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequest]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b759c7ed66fbd4f98e7e443baadc77b06bdd8f1c8fc819cf1a606fd3b000bbe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WaypointAction",
    "WaypointActionConfig",
    "WaypointActionRequest",
    "WaypointActionRequestAgent",
    "WaypointActionRequestAgentOutputReference",
    "WaypointActionRequestCustom",
    "WaypointActionRequestCustomOutputReference",
    "WaypointActionRequestOutputReference",
]

publication.publish()

def _typecheckingstub__f24a34500d6c115f9cad8837252f3c64f8c047dc518864267164f46cf26ee014(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    request: typing.Union[WaypointActionRequest, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__bfe55db6c5ed360be0107c19e0df2d0f7956688bb745ea42bd5992407cc91f6d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0612448f9d5017ddfca325cb8c9d9eafd32ceca1dabc83e141172ecae38c7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d6a77621623f4e2128c435bd80c3baa540e692beff114f3b28cf6c13c23fb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77982ebdc15b76c440f3df0ad63c5c226bf376666b990fd70f3c07d9ec69f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dcc18507e51326004eae31cbfc5a977b7a353bea03ebe75450d12f30f55536(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    request: typing.Union[WaypointActionRequest, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd18a9a38418ee949faa6925308fedb346cb09bbe263a4f832a791c5137d135(
    *,
    agent: typing.Optional[typing.Union[WaypointActionRequestAgent, typing.Dict[builtins.str, typing.Any]]] = None,
    custom: typing.Optional[typing.Union[WaypointActionRequestCustom, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6d469647f3769e07b36b004985ef7abb00ac126ce955a1d47068153918ba02(
    *,
    group: builtins.str,
    operation_id: builtins.str,
    action_run_id: typing.Optional[builtins.str] = None,
    body: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be9cc858685ffa8faae04aff3527d1b0b41974d5cb03c1c9a4edbf9f4d1f6a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2e119f1521e1aed748670331a4574de1322196fabd653c183f09b832f63f8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bc7b52bacc2badae3d5adb1c614c2afc0eb1d49874a5b30f94dfebea81e34e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb492843bcc84f602720f493da33343f43ef3029f4edd15ae49574ea937edad8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad03599e3ebea2ace1af9b78af3a0e6a0c7f2caa62d9b47f4c7b0d4ef05e510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bfc243d3865b2706d26d9656f1de46a483fbe1f34cacaa8e9f131f0644bf7c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestAgent]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa709303ff77d73309067aee841ef3de0708b7e4bb430fe4e4c18958837ebbff(
    *,
    method: builtins.str,
    body: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961faec7aa4cb9fbc49ef2426dbacb82c876300b6265ea5cfc847f32df31fc5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69e035eac03dd89550e7c6f1fea8f6dbe8d9c9c3ee8943564bdfe5e1a444a7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ff7f7b43733cdf79a6f7628db97073b6c617a31993a2b887c060d809a9596a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64784ecb28732a6f28084f4929ed84b2e7412c831c58c04c4dd7552d5c973034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4fb7e9c761d968622f5cdeee939878fc6b6445f5ea0f63c7206552d9221968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76902ccb0af0dcf4640d893d88a2cd33adb3ca046d2518458b24cf77d8648c0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequestCustom]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29842bf9897637784b1a698d122c7d68c634b5191e6699ce0345ed85ace27fbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b759c7ed66fbd4f98e7e443baadc77b06bdd8f1c8fc819cf1a606fd3b000bbe5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WaypointActionRequest]],
) -> None:
    """Type checking stubs"""
    pass
