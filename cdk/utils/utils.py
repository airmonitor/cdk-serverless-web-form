# -*- coding: utf-8 -*-
"""Helper functions to make your life simple."""

from os import path
from typing import Dict, Union, Callable

import aws_cdk as cdk


def check_ansible_dir(directory: str) -> bool:
    """Check if ansible directory exist in root path.

    :return: Bool - True if ansible directory exist, false if not
    """
    this_dir = path.dirname(__file__)
    ansible_path = path.abspath(path.join(this_dir, directory))
    return path.isdir(ansible_path)


def apply_tags(props: Dict, resource: Union[cdk.Stack, cdk.Stage]) -> Callable:
    """Add standardized tags to every resource created in stack.

    :param props: Contain standardized tags (key value) for TR
    :param resource: CDK Stack, Stage or app
    :return: Input object (class) with added tags
    """
    for key, value in props["tags"].items():
        cdk.Tags.of(resource).add(key, value)

    return resource
