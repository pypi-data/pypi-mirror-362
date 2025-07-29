from __future__ import annotations

import logging
import os
from typing import Any

import wrapt
from opentelemetry.environment_variables import OTEL_LOGS_EXPORTER, OTEL_METRICS_EXPORTER, OTEL_TRACES_EXPORTER
from opentelemetry.instrumentation import wsgi as otel_wsgi
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.sdk.environment_variables import (
    OTEL_EXPORTER_OTLP_ENDPOINT,
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT,
    OTEL_EXPORTER_OTLP_PROTOCOL,
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
    OTEL_TRACES_SAMPLER,
)
from opentelemetry.trace import Span

import odoo

from ..instrumentation.odoo import OdooInstrumentor
from ._loader import OtelLoader

_logger = logging.getLogger("opentelemetry.distro.odoo")


def _handle_error_rpc(span: Span, env: dict[str, Any], v: str, env2: list[tuple[str, str]]):
    print(span, env, v, env2)
    print(span.is_recording())


class OdooDistro(BaseDistro):
    def __init__(self):
        super().__init__()
        self.loader = OtelLoader(self)

    def _activate_instrument(self):
        if odoo.evented:
            # Don't instrument Odoo gevent forked processes
            return False
        if os.getenv("OTEL_SDK_DISABLED", "false").lower() == "true":
            _logger.info("OpenTelemetry SDK disabled by environment variable")
            return False
        if not (
            os.getenv(OTEL_EXPORTER_OTLP_ENDPOINT)
            or os.getenv(OTEL_EXPORTER_OTLP_TRACES_ENDPOINT)
            or os.getenv(OTEL_EXPORTER_OTLP_METRICS_ENDPOINT)
        ):
            _logger.info("No endpoint defined for OpenTelemetry")
            return False
        return True

    def _configure(self, **kwargs: Any):
        _logger.info("Start OpenTelemetry Odoo Distro")
        os.environ.setdefault(OTEL_TRACES_EXPORTER, "otlp")
        os.environ.setdefault(OTEL_METRICS_EXPORTER, "otlp")
        os.environ.setdefault(OTEL_LOGS_EXPORTER, "otlp")
        os.environ.setdefault(OTEL_EXPORTER_OTLP_PROTOCOL, "grpc")
        os.environ.setdefault(OTEL_TRACES_SAMPLER, "odoo")

        def wrap_threaded_server_start_(wrapped, instance, args, kwargs):
            stop = args and args[0] or kwargs.get("stop") or False
            if stop:
                return wrapped(*args, **kwargs)
            self.loader.load_samplers()
            self.loader.load_exporters()
            instance._origin_app = instance.app
            instance.app = otel_wsgi.OpenTelemetryMiddleware(wsgi=instance._origin_app, response_hook=_handle_error_rpc)
            self.loader.load_instrument()
            self.loader.setup_logging()
            return wrapped(*args, **kwargs)

        def wrap_worker_http_start_(wrapped, instance, args, kwargs):
            res = wrapped(*args, **kwargs)
            self.loader.load_samplers()
            self.loader.load_exporters()
            instance._origin_app = instance.server.app
            instance.server.app = otel_wsgi.OpenTelemetryMiddleware(instance._origin_app)
            self.loader.load_instrument()
            self.loader.setup_logging()
            OdooInstrumentor().worker_count.add(1, attributes={})
            _logger.info("Start WorkerCounter add 1 [%s]", instance.pid)
            return res

        def wrap_worker_http_signal_handler_(wrapped, instance, args, kwargs):
            sig = args and args[0] or kwargs.get("sig")
            OdooInstrumentor().worker_count.add(-1, attributes={"process.command_args": sig})
            return wrapped(*args, **kwargs)

        try:
            wrapt.wrap_function_wrapper(
                "odoo.service.server", "ThreadedServer.start", wrapper=wrap_threaded_server_start_
            )
        except Exception as ex:  # pylint: disable=broad-except
            _logger.warning("Failed to patch ThreadedServer. %s", str(ex))
        try:
            wrapt.wrap_function_wrapper("odoo.service.server", "WorkerHTTP.start", wrapper=wrap_worker_http_start_)
            wrapt.wrap_function_wrapper(
                "odoo.service.server", "WorkerHTTP.signal_handler", wrapper=wrap_worker_http_signal_handler_
            )
        except Exception as ex:  # pylint: disable=broad-except
            _logger.warning("Failed to patch PreforkServer. %s", str(ex))
        return True
