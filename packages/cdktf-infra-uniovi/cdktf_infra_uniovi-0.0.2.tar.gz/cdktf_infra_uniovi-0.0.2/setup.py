import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-infra-uniovi",
    "version": "0.0.2",
    "description": "cdktf-infra-uniovi",
    "license": "Apache-2.0",
    "url": "https://github.com/Yori1999/cdktf-infra-uniovi.git",
    "long_description_content_type": "text/markdown",
    "author": "María Flórez<mariaf987@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/Yori1999/cdktf-infra-uniovi.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_infra_uniovi",
        "cdktf_infra_uniovi._jsii"
    ],
    "package_data": {
        "cdktf_infra_uniovi._jsii": [
            "cdktf-infra-uniovi@0.0.2.jsii.tgz"
        ],
        "cdktf_infra_uniovi": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdktf-cdktf-provider-aws>=19.0.0, <20.0.0",
        "cdktf-cdktf-provider-docker>=11.0.0, <12.0.0",
        "cdktf>=0.20.11, <0.21.0",
        "constructs>=10.3.0, <11.0.0",
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
