# -*- coding: utf-8 -*-
"""The AWS shared resources for core application stage."""
import aws_cdk as cdk
from constructs import Construct
from cdk.stacks.services.frontend_stack import FrontEndStack, FrontEndMonitoring


class ServicesStage(cdk.Stage):
    """Create CI/CD stage with shared resources."""

    def __init__(self, scope: Construct, construct_id: str, env: cdk.Environment, props: dict, **kwargs) -> None:
        """Initialize default parameters from AWS CDK and configuration file.

        :param scope:
        :param construct_id:
        :param env: Tha AWS CDK Environment class which provide AWS Account ID and AWS Region.
        :param props:
        :param kwargs:
        """
        super().__init__(scope, construct_id, env=env, **kwargs)

        service_name = "frontend"
        front_end_stack = FrontEndStack(
            self,
            construct_id=f"{service_name}-service-stack",
            env=env,
            props=props,
        )
        FrontEndMonitoring(
            self,
            name=f"{service_name}-monitoring-stack",
            env=env,
            props=front_end_stack.output_props,
        )
