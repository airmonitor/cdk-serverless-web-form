# -*- coding: utf-8 -*-
"""Deploy AWS CodeCommit repository."""
import aws_cdk as cdk
import aws_cdk.aws_codecommit as codecommit
from constructs import Construct
from cdk.schemas.configuration_vars import PipelineVars

from aws_cdk import Aspects
from cdk_nag import AwsSolutionsChecks


class RepositoryStack(cdk.Stack):
    """Repository stack."""

    def __init__(self, scope: Construct, construct_id: str, env: cdk.Environment, props: dict, **kwargs) -> None:
        """Initialize default parameters from AWS CDK and configuration file.

        :param scope: The AWS CDK parent class from which this class inherits
        :param construct_id: The name of CDK construct
        :param env: Tha AWS CDK Environment class which provide AWS Account ID and AWS Region
        :param props: The dictionary which contain configuration values loaded initially from /config/config-env.yaml
        :param kwargs:
        """
        super().__init__(scope, construct_id, env=env, **kwargs)
        pipeline_vars = PipelineVars(**props)

        codecommit.Repository(self, id=pipeline_vars.repository, repository_name=pipeline_vars.repository)

        Aspects.of(self).add(AwsSolutionsChecks(log_ignores=True))
