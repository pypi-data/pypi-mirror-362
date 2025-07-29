"""FastAPI application factory for S3-compatible object store API."""

import logging
import os

from fastapi import FastAPI
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter as GrpcLogExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GrpcSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter as HttpLogExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HttpSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, LogExporter
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SpanExporter,
)
from opentelemetry.trace import set_tracer_provider
from pydantic import HttpUrl

from . import middleware
from .handlers import router
from .store import ObjectStore
from .version import __version__


def create_app(
    store: ObjectStore,
    *,
    otel_exporter_http_endpoint: str | HttpUrl | None = None,
    otel_exporter_grpc_endpoint: str | HttpUrl | None = None,
    log_level: int | str | None = logging.DEBUG,
) -> FastAPI:
    """Create a FastAPI application with S3-compatible endpoints.

    Args:
        store: The object store implementation to use

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(title="BoxDrive", description="S3-compatible object store API", version=__version__)
    app.state.store = store

    app.add_middleware(middleware.Recover)
    app.add_middleware(middleware.LogInfo)
    app.add_middleware(middleware.InjectOtelContextIntoResponse)

    app.include_router(router)

    setup_opentelemetry(
        app,
        otel_exporter_http_endpoint=otel_exporter_http_endpoint,
        otel_exporter_grpc_endpoint=otel_exporter_grpc_endpoint,
        log_level=log_level,
    )
    return app


def setup_opentelemetry(
    app: FastAPI,
    *,
    otel_exporter_http_endpoint: str | HttpUrl | None = None,
    otel_exporter_grpc_endpoint: str | HttpUrl | None = None,
    log_level: int | str | None = logging.DEBUG,
) -> None:
    resource = Resource.create(
        attributes={
            SERVICE_NAME: app.title,
            SERVICE_VERSION: app.version,
        },
    )

    trace_provider = TracerProvider(resource=resource)
    logger_provider = LoggerProvider(resource=resource)

    if otel_exporter_http_endpoint:
        http_endpoint = HttpUrl(otel_exporter_http_endpoint)
        trace_provider.add_span_processor(BatchSpanProcessor(_create_http_span_exporter(http_endpoint)))
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(_create_http_log_exporter(http_endpoint)))
    if otel_exporter_grpc_endpoint:
        grpc_endpoint = HttpUrl(otel_exporter_grpc_endpoint)
        trace_provider.add_span_processor(BatchSpanProcessor(_create_grpc_span_exporter(grpc_endpoint)))
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(_create_grpc_log_exporter(grpc_endpoint)))

    set_tracer_provider(trace_provider)
    set_logger_provider(logger_provider)

    LoggingInstrumentor().instrument(set_logging_format=True, log_level=log_level)

    logging_handler = LoggingHandler(logger_provider=logger_provider)
    logging.getLogger().addHandler(logging_handler)

    FastAPIInstrumentor.instrument_app(app)
    HTTPXClientInstrumentor().instrument()


def _create_http_log_exporter(endpoint: HttpUrl) -> LogExporter:
    return HttpLogExporter(endpoint=os.path.join(str(endpoint), "v1/logs"))


def _create_grpc_log_exporter(endpoint: HttpUrl) -> LogExporter:
    return GrpcLogExporter(endpoint=os.path.join(str(endpoint), "v1/logs"))


def _create_http_span_exporter(endpoint: HttpUrl) -> SpanExporter:
    return HttpSpanExporter(
        endpoint=os.path.join(str(endpoint), "v1/traces"),
    )


def _create_grpc_span_exporter(endpoint: HttpUrl) -> SpanExporter:
    return GrpcSpanExporter(
        endpoint=os.path.join(str(endpoint), "v1/traces"),
    )
