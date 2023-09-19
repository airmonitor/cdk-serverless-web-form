# -*- coding: utf-8 -*-
"""Validate variables against pydantic models."""

from typing import Literal, Optional

from pydantic import BaseModel, constr, PositiveFloat, EmailStr


class Observability(BaseModel):
    """Observability variables."""

    LOG_LEVEL: Literal["DEBUG", "INFO", "ERROR", "CRITICAL", "WARNING", "EXCEPTION"]
    LOG_SAMPLING_RATE: PositiveFloat


class PipelineVars(BaseModel):
    """CI/CD variables.."""

    aws_region: Literal["eu-central-1", "us-west-2", "eu-north-1"]
    aws_account: constr(min_length=12, max_length=12)  # type: ignore
    dev_aws_region: Literal["eu-central-1", "us-west-2", "eu-north-1"]
    dev_aws_account: constr(min_length=12, max_length=12)  # type: ignore
    project: str
    repository: constr(min_length=3, max_length=255)  # type: ignore
    ci_cd_notification_email: EmailStr
    slack_channel_id: Optional[constr(min_length=0, max_length=11)]  # type: ignore
    slack_workspace_id: Optional[constr(min_length=0, max_length=11)]  # type: ignore


class ConfigurationVars(PipelineVars):
    """Notification details, including email, slack, etc."""

    stage: Literal["dev", "stg", "prod"]
    alarm_emails: list[EmailStr]
    domain_name: str
    acm_certificate_arn: constr(pattern="^arn:aws:acm:*")  # type: ignore
    hosted_zone_id: str
    hosted_zone_name: str
