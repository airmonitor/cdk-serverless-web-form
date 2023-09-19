# -*- coding: utf-8 -*-
"""CDK Setup file."""
import setuptools


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pipeline",
    version="0.0.1",
    description="CDK python serverless web form",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tomasz Szuster",
    package_dir={"": "cdk"},
    packages=setuptools.find_packages(where="cdk"),
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
