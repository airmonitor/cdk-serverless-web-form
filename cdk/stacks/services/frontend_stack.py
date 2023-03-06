# -*- coding: utf-8 -*-
"""Deploy services."""
from cdk_opinionated_constructs.lmb import AWSPythonLambdaFunction
import aws_cdk as cdk
import aws_cdk.aws_ssm as ssm
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sns as sns
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_cloudwatch as cloudwatch
from constructs import Construct
import cdk_monitoring_constructs as cdk_monitoring

from aws_cdk import Aspects
from cdk_nag import AwsSolutionsChecks, NagSuppressions

from cdk.constructs.imported_resources_construct import ImportedResources
from cdk.schemas.configuration_vars import ConfigurationVars


class FrontEndStack(cdk.Stack):
    """Service stack."""

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
        imported_resources = ImportedResources(self, construct_id="imported_resources", props=props, env=env)
        self.imported_event_bridge_bus = imported_resources.default_event_bus
        # self.ssm_param_authorization_key = imported_resources.imported_ssm_parameter_authorization_key
        # self.ssm_param_csrf_key = imported_resources.imported_ssm_parameter_csrf_key

        aws_lambda_function_name = "frontend"
        aws_lambda_construct = AWSPythonLambdaFunction(self, f"{aws_lambda_function_name}_construct")
        aws_lambda_layer = aws_lambda_construct.create_lambda_layer(
            construct_id=f"{aws_lambda_function_name}_layer", code_path=f"services/layers/{aws_lambda_function_name}"
        )

        aws_lambda_signing_config = aws_lambda_construct.signing_config(
            signing_profile_name=f"{aws_lambda_function_name}_signing_profile"
        )

        aws_lambda_function = aws_lambda_construct.create_lambda_function(
            code_path=f"services/functions/{aws_lambda_function_name}",
            env=env,
            env_variables={
                "LOG_LEVEL": "DEBUG",
                "LOG_SAMPLING_RATE": "1.0",
                "POWERTOOLS_SERVICE_NAME": f"{aws_lambda_function_name.replace('_', '-')}",
                "CURRENT_REGION": env.region,
                # "EVENT_BUS_NAME": self.imported_event_bridge_bus.event_bus_name,
                # "EVENT_SOURCE_NAME": f"{config_vars.project}-front-end-lambda",
                # "EVENT_DETAIL_TYPE": "form-details",
                # "AUTHORIZATION_KEY": self.ssm_param_authorization_key.parameter_name,
                # "CSRF_KEY": self.ssm_param_csrf_key.parameter_name,
            },
            function_name=f"{config_vars.project}-{aws_lambda_function_name.replace('_', '-')}",
            handler="handler.handler",
            layers=[aws_lambda_layer],
            reserved_concurrent_executions=2,
            signing_config=aws_lambda_signing_config,
            timeout=26,
        )

        # self.ssm_param_authorization_key.grant_read(aws_lambda_function)
        # self.ssm_param_csrf_key.grant_read(aws_lambda_function)

        # Create api gateway proxy method
        api_gw = apigw.LambdaRestApi(
            self,
            id="api_gateway",
            endpoint_configuration=apigw.EndpointConfiguration(types=[apigw.EndpointType.REGIONAL]),
            handler=aws_lambda_function,
            policy=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=["execute-api:Invoke"],
                        resources=["execute-api:/*/*/*"],
                        effect=iam.Effect.DENY,
                        principals=[iam.StarPrincipal()],
                        conditions={
                            "NotIpAddress": {"aws:SourceIp": ["46.227.242.211", "165.225.206.0/23"]},
                        },
                    ),
                    iam.PolicyStatement(
                        actions=["execute-api:Invoke"],
                        resources=["execute-api:/*/*/*"],
                        effect=iam.Effect.ALLOW,
                        principals=[iam.StarPrincipal()],
                    ),
                ]
            ),
            proxy=True,
            rest_api_name=f"{config_vars.project}-api-gateway",
        )
        # Validate stack against AWS Solutions checklist
        NagSuppressions.add_stack_suppressions(self, self.nag_suppression())
        Aspects.of(self).add(AwsSolutionsChecks(log_ignores=True))

        self.output_props = props.copy()
        self.output_props["aws_lambda_function"] = aws_lambda_function
        self.output_props["api_gw"] = api_gw

    @staticmethod
    def nag_suppression() -> list:
        """Create CFN-NAG suppression.

        :return:
        """
        return [
            {
                "id": "AwsSolutions-APIG2",
                "reason": "Validation is conducted in a Flask application itself",
            },
            {
                "id": "AwsSolutions-APIG1",
                "reason": "Logging on API GW level is not required "
                "as all requests are transmitted as a proxy to lambda function",
            },
            {
                "id": "AwsSolutions-APIG3",
                "reason": "This is internal API and not exposed to public",
            },
            {
                "id": "AwsSolutions-APIG4",
                "reason": "This is internal API and not exposed to public",
            },
            {
                "id": "AwsSolutions-APIG6",
                "reason": "Logging is enabled on a lambda level",
            },
            {
                "id": "AwsSolutions-COG4",
                "reason": "Authorization is not required for this API",
            },
            {
                "id": "AwsSolutions-IAM4",
                "reason": "Using managed policies is allowed",
            },
            {
                "id": "AwsSolutions-IAM5",
                "reason": "There isn't a way to tailor IAM policy using more restrictive permissions for "
                "used API calls logs:CreateLogGroup, xray:PutTelemetryRecords, xray:PutTraceSegments",
            },
        ]

    @property
    def outputs(self):
        """Update props dictionary.

        :return: Updated props dict
        """
        return self.output_props

        # Validate stack against AWS Solutions checklist


class FrontEndMonitoring(cdk.Stack):
    """Create monitoring resources for PRS.

    This includes:
    * AWS CW Dashboard
    * Metrics
    * Alarms
    * Subscription to SNS topic
    * similar
    """

    # pylint: disable=W0613
    def __init__(self, scope, name, env, props):
        super().__init__(scope, name)
        config_vars = ConfigurationVars(**props)
        alarm_sns_topic = sns.Topic.from_topic_arn(
            self,
            id="imported_sns_topic",
            topic_arn=ssm.StringParameter.value_for_string_parameter(
                self, parameter_name=f"/{config_vars.project}/topic/alarm/arn"
            ),
        )
        aws_lambda_function: lmb.Function = props["aws_lambda_function"]  # type: ignore
        api_gw: apigw.LambdaRestApi = props["api_gw"]

        documentation = ""

        monitoring = cdk_monitoring.MonitoringFacade(
            self,
            f"{config_vars.project}-frontend",
            alarm_factory_defaults=cdk_monitoring.AlarmFactoryDefaults(
                action=cdk_monitoring.SnsAlarmActionStrategy(on_alarm_topic=alarm_sns_topic),
                alarm_name_prefix=config_vars.project,
                actions_enabled=True,
            ),
        )

        monitoring.add_large_header("Frontend").monitor_lambda_function(
            lambda_function=aws_lambda_function,
            lambda_insights_enabled=True,
            rate_computation_method=cdk_monitoring.RateComputationMethod.PER_SECOND,
            add_concurrent_executions_count_alarm={
                "Critical": cdk_monitoring.RunningTaskCountThreshold(
                    datapoints_to_alarm=1,
                    comparison_operator_override=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                    documentation_link=documentation,
                    evaluation_periods=1,
                    fill_alarm_range=True,
                    period=cdk.Duration.seconds(10),
                    max_running_tasks=10,
                ),
            },
            add_fault_count_alarm={
                "Critical": cdk_monitoring.ErrorCountThreshold(
                    datapoints_to_alarm=1,
                    comparison_operator_override=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                    documentation_link=documentation,
                    evaluation_periods=1,
                    period=cdk.Duration.minutes(1),
                    max_error_count=1,
                )
            },
            add_throttles_count_alarm={
                "Critical": cdk_monitoring.ErrorCountThreshold(
                    datapoints_to_alarm=1,
                    comparison_operator_override=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                    documentation_link=documentation,
                    evaluation_periods=1,
                    period=cdk.Duration.minutes(1),
                    max_error_count=1,
                )
            },
            add_latency_p99_alarm={
                "Critical": cdk_monitoring.LatencyThreshold(
                    datapoints_to_alarm=1,
                    comparison_operator_override=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                    documentation_link=documentation,
                    evaluation_periods=1,
                    period=cdk.Duration.minutes(1),
                    max_latency=cdk.Duration.seconds(aws_lambda_function.timeout.to_seconds() * 0.99),
                )
            },
        )

        monitoring.add_large_header("Frontend: errors").monitor_log(
            alarm_friendly_name="code errors",
            limit=5,
            log_group_name=f"/aws/lambda/{aws_lambda_function.function_name}",
            pattern="ERROR",
        )

        monitoring.add_large_header("API GW").monitor_api_gateway(
            api=api_gw,
            add4_xx_error_count_alarm={
                "Critical": cdk_monitoring.ErrorCountThreshold(
                    datapoints_to_alarm=1,
                    documentation_link=documentation,
                    evaluation_periods=1,
                    fill_alarm_range=True,
                    period=cdk.Duration.minutes(1),
                    max_error_count=1,
                )
            },
            add5_xx_fault_count_alarm={
                "Critical": cdk_monitoring.ErrorCountThreshold(
                    datapoints_to_alarm=1,
                    documentation_link=documentation,
                    evaluation_periods=1,
                    fill_alarm_range=True,
                    period=cdk.Duration.minutes(1),
                    max_error_count=1,
                )
            },
        )
