import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "mbonig.nightynight",
    "version": "2.0.4",
    "description": "A CDK construct that will automatically stop a running EC2 instance at a given time.",
    "license": "Apache-2.0",
    "url": "https://github.com/mbonig/nightynight",
    "long_description_content_type": "text/markdown",
    "author": "Matthew Bonig<matthew.bonig@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mbonig/nightynight"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mbonig.nightynight",
        "mbonig.nightynight._jsii"
    ],
    "package_data": {
        "mbonig.nightynight._jsii": [
            "nightynight@2.0.4.jsii.tgz"
        ],
        "mbonig.nightynight": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.202.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.98.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
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
