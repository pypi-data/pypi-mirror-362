import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "renovosolutions.aws-cdk-cloudwatch-alarms",
    "version": "0.0.9",
    "description": "AWS CDK Construct Library to automatically create CloudWatch Alarms for resources in a CDK app based on resource type.",
    "license": "Apache-2.0",
    "url": "https://github.com/RenovoSolutions/cdk-library-cloudwatch-alarms.git",
    "long_description_content_type": "text/markdown",
    "author": "Renovo Solutions<webmaster+cdk@renovo1.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/RenovoSolutions/cdk-library-cloudwatch-alarms.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "renovosolutions_recommended_cloudwatch_alarms",
        "renovosolutions_recommended_cloudwatch_alarms._jsii"
    ],
    "package_data": {
        "renovosolutions_recommended_cloudwatch_alarms._jsii": [
            "cdk-library-cloudwatch-alarms@0.0.9.jsii.tgz"
        ],
        "renovosolutions_recommended_cloudwatch_alarms": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.202.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
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
