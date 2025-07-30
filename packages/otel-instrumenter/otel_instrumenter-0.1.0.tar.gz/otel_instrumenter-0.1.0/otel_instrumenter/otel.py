import logging
from typing import Optional

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor


def configure_otel(
    service_name: str,
    endpoint: str = "http://localhost:4317",
    insecure: bool = True,
    headers: Optional[dict] = None,
):
    """
    Configura OpenTelemetry para tracing e logs.

    :param service_name: Nome do serviço.
    :param endpoint: Endpoint do OTLP (ex: http://localhost:4317).
    :param insecure: Se True, usa conexão não segura (sem TLS).
    :param headers: Dicionário de headers (ex: {"Authorization": "Bearer ..."}).
    """
    # Recurso com nome do serviço
    resource = Resource.create({SERVICE_NAME: service_name})

    # ----- TRACES -----
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    trace_exporter = OTLPSpanExporter(
        endpoint=endpoint,
        insecure=insecure,
        headers=headers,
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

    # ----- LOGS -----
    log_exporter = OTLPLogExporter(
        endpoint=endpoint,
        insecure=insecure,
        headers=headers,
    )
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)

    # Manipulador para logs padrão do Python
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)

    # ----- INSTRUMENTAÇÃO AUTOMÁTICA -----
    HTTPXClientInstrumentor().instrument()
    FastAPIInstrumentor().instrument()
