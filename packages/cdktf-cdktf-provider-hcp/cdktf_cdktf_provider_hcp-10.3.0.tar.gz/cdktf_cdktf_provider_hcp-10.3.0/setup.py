import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-hcp",
    "version": "10.3.0",
    "description": "Prebuilt hcp Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-hcp.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-hcp.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_hcp",
        "cdktf_cdktf_provider_hcp._jsii",
        "cdktf_cdktf_provider_hcp.aws_network_peering",
        "cdktf_cdktf_provider_hcp.aws_transit_gateway_attachment",
        "cdktf_cdktf_provider_hcp.azure_peering_connection",
        "cdktf_cdktf_provider_hcp.boundary_cluster",
        "cdktf_cdktf_provider_hcp.consul_cluster",
        "cdktf_cdktf_provider_hcp.consul_cluster_root_token",
        "cdktf_cdktf_provider_hcp.consul_snapshot",
        "cdktf_cdktf_provider_hcp.data_hcp_aws_network_peering",
        "cdktf_cdktf_provider_hcp.data_hcp_aws_transit_gateway_attachment",
        "cdktf_cdktf_provider_hcp.data_hcp_azure_peering_connection",
        "cdktf_cdktf_provider_hcp.data_hcp_boundary_cluster",
        "cdktf_cdktf_provider_hcp.data_hcp_consul_agent_helm_config",
        "cdktf_cdktf_provider_hcp.data_hcp_consul_agent_kubernetes_secret",
        "cdktf_cdktf_provider_hcp.data_hcp_consul_cluster",
        "cdktf_cdktf_provider_hcp.data_hcp_consul_versions",
        "cdktf_cdktf_provider_hcp.data_hcp_group",
        "cdktf_cdktf_provider_hcp.data_hcp_hvn",
        "cdktf_cdktf_provider_hcp.data_hcp_hvn_peering_connection",
        "cdktf_cdktf_provider_hcp.data_hcp_hvn_route",
        "cdktf_cdktf_provider_hcp.data_hcp_iam_policy",
        "cdktf_cdktf_provider_hcp.data_hcp_organization",
        "cdktf_cdktf_provider_hcp.data_hcp_packer_artifact",
        "cdktf_cdktf_provider_hcp.data_hcp_packer_bucket_names",
        "cdktf_cdktf_provider_hcp.data_hcp_packer_run_task",
        "cdktf_cdktf_provider_hcp.data_hcp_packer_version",
        "cdktf_cdktf_provider_hcp.data_hcp_project",
        "cdktf_cdktf_provider_hcp.data_hcp_service_principal",
        "cdktf_cdktf_provider_hcp.data_hcp_user_principal",
        "cdktf_cdktf_provider_hcp.data_hcp_vault_cluster",
        "cdktf_cdktf_provider_hcp.data_hcp_vault_plugin",
        "cdktf_cdktf_provider_hcp.data_hcp_vault_radar_resources",
        "cdktf_cdktf_provider_hcp.data_hcp_vault_secrets_app",
        "cdktf_cdktf_provider_hcp.data_hcp_vault_secrets_dynamic_secret",
        "cdktf_cdktf_provider_hcp.data_hcp_vault_secrets_rotating_secret",
        "cdktf_cdktf_provider_hcp.data_hcp_vault_secrets_secret",
        "cdktf_cdktf_provider_hcp.data_hcp_waypoint_action",
        "cdktf_cdktf_provider_hcp.data_hcp_waypoint_add_on",
        "cdktf_cdktf_provider_hcp.data_hcp_waypoint_add_on_definition",
        "cdktf_cdktf_provider_hcp.data_hcp_waypoint_agent_group",
        "cdktf_cdktf_provider_hcp.data_hcp_waypoint_application",
        "cdktf_cdktf_provider_hcp.data_hcp_waypoint_template",
        "cdktf_cdktf_provider_hcp.group",
        "cdktf_cdktf_provider_hcp.group_iam_binding",
        "cdktf_cdktf_provider_hcp.group_iam_policy",
        "cdktf_cdktf_provider_hcp.group_members",
        "cdktf_cdktf_provider_hcp.hvn",
        "cdktf_cdktf_provider_hcp.hvn_peering_connection",
        "cdktf_cdktf_provider_hcp.hvn_route",
        "cdktf_cdktf_provider_hcp.iam_workload_identity_provider",
        "cdktf_cdktf_provider_hcp.log_streaming_destination",
        "cdktf_cdktf_provider_hcp.notifications_webhook",
        "cdktf_cdktf_provider_hcp.organization_iam_binding",
        "cdktf_cdktf_provider_hcp.organization_iam_policy",
        "cdktf_cdktf_provider_hcp.packer_bucket",
        "cdktf_cdktf_provider_hcp.packer_bucket_iam_binding",
        "cdktf_cdktf_provider_hcp.packer_bucket_iam_policy",
        "cdktf_cdktf_provider_hcp.packer_channel",
        "cdktf_cdktf_provider_hcp.packer_channel_assignment",
        "cdktf_cdktf_provider_hcp.packer_run_task",
        "cdktf_cdktf_provider_hcp.project",
        "cdktf_cdktf_provider_hcp.project_iam_binding",
        "cdktf_cdktf_provider_hcp.project_iam_policy",
        "cdktf_cdktf_provider_hcp.provider",
        "cdktf_cdktf_provider_hcp.service_principal",
        "cdktf_cdktf_provider_hcp.service_principal_key",
        "cdktf_cdktf_provider_hcp.vault_cluster",
        "cdktf_cdktf_provider_hcp.vault_cluster_admin_token",
        "cdktf_cdktf_provider_hcp.vault_plugin",
        "cdktf_cdktf_provider_hcp.vault_radar_integration_jira_connection",
        "cdktf_cdktf_provider_hcp.vault_radar_integration_jira_subscription",
        "cdktf_cdktf_provider_hcp.vault_radar_integration_slack_connection",
        "cdktf_cdktf_provider_hcp.vault_radar_integration_slack_subscription",
        "cdktf_cdktf_provider_hcp.vault_radar_resource_iam_binding",
        "cdktf_cdktf_provider_hcp.vault_radar_resource_iam_policy",
        "cdktf_cdktf_provider_hcp.vault_radar_source_github_cloud",
        "cdktf_cdktf_provider_hcp.vault_radar_source_github_enterprise",
        "cdktf_cdktf_provider_hcp.vault_secrets_app",
        "cdktf_cdktf_provider_hcp.vault_secrets_app_iam_binding",
        "cdktf_cdktf_provider_hcp.vault_secrets_app_iam_policy",
        "cdktf_cdktf_provider_hcp.vault_secrets_dynamic_secret",
        "cdktf_cdktf_provider_hcp.vault_secrets_integration",
        "cdktf_cdktf_provider_hcp.vault_secrets_integration_aws",
        "cdktf_cdktf_provider_hcp.vault_secrets_integration_azure",
        "cdktf_cdktf_provider_hcp.vault_secrets_integration_confluent",
        "cdktf_cdktf_provider_hcp.vault_secrets_integration_gcp",
        "cdktf_cdktf_provider_hcp.vault_secrets_integration_mongodbatlas",
        "cdktf_cdktf_provider_hcp.vault_secrets_integration_twilio",
        "cdktf_cdktf_provider_hcp.vault_secrets_rotating_secret",
        "cdktf_cdktf_provider_hcp.vault_secrets_secret",
        "cdktf_cdktf_provider_hcp.vault_secrets_sync",
        "cdktf_cdktf_provider_hcp.waypoint_action",
        "cdktf_cdktf_provider_hcp.waypoint_add_on",
        "cdktf_cdktf_provider_hcp.waypoint_add_on_definition",
        "cdktf_cdktf_provider_hcp.waypoint_agent_group",
        "cdktf_cdktf_provider_hcp.waypoint_application",
        "cdktf_cdktf_provider_hcp.waypoint_template",
        "cdktf_cdktf_provider_hcp.waypoint_tfc_config"
    ],
    "package_data": {
        "cdktf_cdktf_provider_hcp._jsii": [
            "provider-hcp@10.3.0.jsii.tgz"
        ],
        "cdktf_cdktf_provider_hcp": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdktf>=0.21.0, <0.22.0",
        "constructs>=10.4.2, <11.0.0",
        "jsii>=1.112.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
