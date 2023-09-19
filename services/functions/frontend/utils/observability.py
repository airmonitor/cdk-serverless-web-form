# -*- coding: utf-8 -*-
"""Initialize global logger, tracer and metrics via aws-lambda-powertools."""
from os import environ
from aws_lambda_powertools.logging.logger import Logger
from aws_lambda_powertools.metrics.metrics import Metrics
from aws_lambda_powertools.tracing.tracer import Tracer

METRICS_NAMESPACE = environ["POWERTOOLS_SERVICE_NAME"]

logger: Logger = Logger()
tracer: Tracer = Tracer()
metrics = Metrics(namespace=METRICS_NAMESPACE)
