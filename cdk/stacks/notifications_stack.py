# -*- coding: utf-8 -*-
"""Create AWS resources responsible for notifications.

Example sns alarm topic
"""
from cdk_opinionated_constructs.sns import SNSTopic
import aws_cdk as cdk
from constructs import Construct
from cdk.schemas.configuration_vars import ConfigurationVars
import aws_cdk.aws_ssm as ssm
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sns_subscriptions as sns_subscriptions
from aws_cdk import Aspects
from cdk_nag import AwsSolutionsChecks, NagSuppressions


class NotificationsStack(cdk.Stack):
    """Service stack.

    Create notifications cloudformation stack.
    """

    def __init__(self, scope: Construct, construct_id: str, env: cdk.Environment, props: dict, **kwargs) -> None:
        """Initialize default parameters from AWS CDK and configuration file.

        :param scope: The AWS CDK parent class from which this class inherits
        :param construct_id: The name of CDK construct
        :param env: Tha AWS CDK Environment class which provide AWS Account ID and AWS Region
        :param props: The dictionary which contain configuration values loaded initially from /config/config-env.yaml
        :param kwargs:
        """
        super().__init__(scope, construct_id, env=env, **kwargs)
        config_vars = ConfigurationVars(**props)

        sns_construct = SNSTopic(self, id="topic_construct")
        sns_topic = sns_construct.create_sns_topic(topic_name=f"{config_vars.project}-alarms", master_key=None)

        # grant cloudwatch permissions to publish to the topic
        sns_topic.add_to_resource_policy(
            statement=iam.PolicyStatement(
                sid="CloudWatchPolicy",
                actions=["sns:Publish"],
                resources=[sns_topic.topic_arn],
                principals=[iam.ServicePrincipal("cloudwatch.amazonaws.com")],
                effect=iam.Effect.ALLOW,
            )
        )

        ssm.StringParameter(
            self,
            id="sns_topic_ssm_param",
            string_value=sns_topic.topic_arn,
            parameter_name=f"/{config_vars.project}/topic/alarm/arn",
        )

        for email_address in config_vars.alarm_emails:
            sns_topic.add_subscription(
                topic_subscription=sns_subscriptions.EmailSubscription(email_address=email_address)
            )

        # Validate stack against AWS Solutions checklist
        NagSuppressions.add_stack_suppressions(self, self.nag_suppression())
        Aspects.of(self).add(AwsSolutionsChecks(log_ignores=True))

    @staticmethod
    def nag_suppression() -> list:
        """Create CFN-NAG suppression.

        :return:
        """
        return [
            {
                "id": "AwsSolutions-SNS2",
                "reason": "Notifications stack, doesn't require encryption",
            }
        ]
