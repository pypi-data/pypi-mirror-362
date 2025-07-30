import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-boundary",
    "version": "10.1.1",
    "description": "Prebuilt boundary Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-boundary.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-boundary.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_boundary",
        "cdktf_cdktf_provider_boundary._jsii",
        "cdktf_cdktf_provider_boundary.account",
        "cdktf_cdktf_provider_boundary.account_ldap",
        "cdktf_cdktf_provider_boundary.account_oidc",
        "cdktf_cdktf_provider_boundary.account_password",
        "cdktf_cdktf_provider_boundary.alias_target",
        "cdktf_cdktf_provider_boundary.auth_method",
        "cdktf_cdktf_provider_boundary.auth_method_ldap",
        "cdktf_cdktf_provider_boundary.auth_method_oidc",
        "cdktf_cdktf_provider_boundary.auth_method_password",
        "cdktf_cdktf_provider_boundary.credential_json",
        "cdktf_cdktf_provider_boundary.credential_library_vault",
        "cdktf_cdktf_provider_boundary.credential_library_vault_ssh_certificate",
        "cdktf_cdktf_provider_boundary.credential_ssh_private_key",
        "cdktf_cdktf_provider_boundary.credential_store_static",
        "cdktf_cdktf_provider_boundary.credential_store_vault",
        "cdktf_cdktf_provider_boundary.credential_username_password",
        "cdktf_cdktf_provider_boundary.data_boundary_account",
        "cdktf_cdktf_provider_boundary.data_boundary_auth_method",
        "cdktf_cdktf_provider_boundary.data_boundary_group",
        "cdktf_cdktf_provider_boundary.data_boundary_scope",
        "cdktf_cdktf_provider_boundary.data_boundary_user",
        "cdktf_cdktf_provider_boundary.group",
        "cdktf_cdktf_provider_boundary.host",
        "cdktf_cdktf_provider_boundary.host_catalog",
        "cdktf_cdktf_provider_boundary.host_catalog_plugin",
        "cdktf_cdktf_provider_boundary.host_catalog_static",
        "cdktf_cdktf_provider_boundary.host_set",
        "cdktf_cdktf_provider_boundary.host_set_plugin",
        "cdktf_cdktf_provider_boundary.host_set_static",
        "cdktf_cdktf_provider_boundary.host_static",
        "cdktf_cdktf_provider_boundary.managed_group",
        "cdktf_cdktf_provider_boundary.managed_group_ldap",
        "cdktf_cdktf_provider_boundary.policy_storage",
        "cdktf_cdktf_provider_boundary.provider",
        "cdktf_cdktf_provider_boundary.role",
        "cdktf_cdktf_provider_boundary.scope",
        "cdktf_cdktf_provider_boundary.scope_policy_attachment",
        "cdktf_cdktf_provider_boundary.storage_bucket",
        "cdktf_cdktf_provider_boundary.target",
        "cdktf_cdktf_provider_boundary.user",
        "cdktf_cdktf_provider_boundary.worker"
    ],
    "package_data": {
        "cdktf_cdktf_provider_boundary._jsii": [
            "provider-boundary@10.1.1.jsii.tgz"
        ],
        "cdktf_cdktf_provider_boundary": [
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
