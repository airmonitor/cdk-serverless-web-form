# -*- coding: utf-8 -*-
"""CDK constructs for opinionated S3 bucket, SNS topic, SQS Queue."""
from constructs import Construct
import aws_cdk.aws_events as events
import aws_cdk.aws_certificatemanager as acm
import aws_cdk.aws_route53 as route53
from cdk.schemas.configuration_vars import ConfigurationVars


class ImportedResources(Construct):
    """Imported resources for the Core stack."""

    # pylint: disable=W0622
    # pylint: disable=W0613
    def __init__(self, scope: Construct, construct_id: str, props, env):
        super().__init__(scope, construct_id)

        self.config_vars = ConfigurationVars(**props)

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

    @property
    def imported_certificate(self) -> acm.ICertificate:
        """Returns ACM Certificate as CDK object."""
        return acm.Certificate.from_certificate_arn(
            self, id="imported_certificate", certificate_arn=self.config_vars.acm_certificate_arn
        )

    @property
    def imported_hosted_zone(self) -> route53.IHostedZone:
        """Returns Route53 Hosted Zone as CDK object."""
        return route53.HostedZone.from_hosted_zone_attributes(
            self,
            id="imported_hosted_zone",
            hosted_zone_id=self.config_vars.hosted_zone_id,
            zone_name=self.config_vars.hosted_zone_name,
        )
