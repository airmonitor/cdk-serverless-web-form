# -*- coding: utf-8 -*-
"""Create CDK objects for imported resources from other stages."""
from os import path


def check_ansible_dir(directory: str) -> bool:
    """Check if ansible directory exist in root path.

    :return: Bool - True if ansible directory exist, false if not
    """
    this_dir = path.dirname(__file__)
    ansible_path = path.abspath(path.join(this_dir, directory))
    return path.isdir(ansible_path)
