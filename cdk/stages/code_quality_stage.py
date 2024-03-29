# -*- coding: utf-8 -*-
"""The CI/CD stage - implements jobs to validate code quality.
"""
import aws_cdk as cdk
from constructs import Construct
from cdk.stacks.code_quality_stack import CodeQualityStack


class CodeQualityStage(cdk.Stage):
    """
    Create CI/CD stage with one stack and several jobs to check code quality
    using: pre-commit and ansible-lint.

    """

    def __init__(self, scope: Construct, construct_id: str, env: cdk.Environment, props: dict, **kwargs) -> None:
        """Initialize default parameters from AWS CDK and configuration file.

        :param scope:
        :param construct_id:
        :param env: Tha AWS CDK Environment class which provide AWS Account ID and AWS Region.
        :param props:
        :param kwargs:
        """
        super().__init__(scope, construct_id, env=env, **kwargs)

        CodeQualityStack(
            self,
            construct_id="codequality-stack",
            env=env,
            props=props,
        )
