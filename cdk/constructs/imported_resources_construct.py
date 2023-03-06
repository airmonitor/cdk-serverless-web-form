# -*- coding: utf-8 -*-
"""CDK constructs for opinionated S3 bucket, SNS topic, SQS Queue."""

from constructs import Construct
import aws_cdk.aws_events as events
from cdk.schemas.configuration_vars import ConfigurationVars


class ImportedResources(Construct):
    """Imported resources for the Core stack."""

    # pylint: disable=W0622
    # pylint: disable=W0613
    def __init__(self, scope: Construct, construct_id: str, props, env):
        super().__init__(scope, construct_id)
        self.config_vars = ConfigurationVars(**props)

        # self.ssm_kms_key = self.imported_ssm_kms_key()

        self.output_props = props.copy()

    @property
    def outputs(self):
        """Update props dictionary.

        :return: Updated props dict
        """
        return self.output_props

    @property
    def default_event_bus(self):
        """CDK object for Event Bridge bus.

        :return: Updated props dict
        """
        return events.EventBus.from_event_bus_name(self, id="imported_default_event_bus", event_bus_name="default")

    #
    # def imported_ssm_kms_key(self):
    #     """CDK object for imported KMS key.
    #
    #     :return: Updated props dict
    #     """
    #     return kms.Key.from_key_arn(self, id="imported_ssm_kms_key", key_arn=self.config_vars.ssm_kms_key_arn)
    #
    # @property
    # def imported_ssm_parameter_authorization_key(self):
    #     """CDK object for SSM parameter.
    #
    #     :return: Updated props dict
    #     """
    #     return ssm.StringParameter.from_secure_string_parameter_attributes(
    #         self,
    #         id="imported_ssm_parameter_authorization_key",
    #         encryption_key=self.ssm_kms_key,
    #         parameter_name=f"/{self.config_vars.project}/form/authorization/key",
    #     )
    #
    # @property
    # def imported_ssm_parameter_csrf_key(self):
    #     """CDK object for SSM parameter.
    #
    #     :return: Updated props dict
    #     """
    #     return ssm.StringParameter.from_secure_string_parameter_attributes(
    #         self,
    #         id="imported_ssm_parameter_csrf_key",
    #         encryption_key=self.ssm_kms_key,
    #         parameter_name=f"/{self.config_vars.project}/form/csrf/key",
    #     )
