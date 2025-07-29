from __future__ import annotations

import logging
import os
from typing import Sequence

from opentelemetry.environment_variables import OTEL_LOGS_EXPORTER, OTEL_METRICS_EXPORTER, OTEL_TRACES_EXPORTER
from opentelemetry.instrumentation.auto_instrumentation import _load_instrumentors
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.sdk._configuration import (
    _get_exporter_entry_point,
    _import_exporters,
    _import_sampler_factory,
    _init_logging,
    _init_metrics,
    _init_tracing,
)
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.sdk.environment_variables import (
    OTEL_EXPERIMENTAL_RESOURCE_DETECTORS,
    OTEL_TRACES_SAMPLER,
    OTEL_TRACES_SAMPLER_ARG,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.sampling import _KNOWN_SAMPLERS, Sampler
from typing_extensions import Literal

from ..semconv.environment_variables import (
    ODOO_OTEL_DISTRO_DEFAULT_RESOURCE_DETECTORS,
    ODOO_OTEL_LOG_FORMAT,
    ODOO_OTEL_LOG_FORMAT_DEFAULT,
    ODOO_OTEL_LOGS_FILTER,
    ODOO_OTEL_TRACE_CUSTOM,
    ODOO_OTEL_TRACE_CUSTOM_DEFAULT,
    ODOO_OTEL_TRACE_CUSTOM_DEFAULT_ARGS,
)
from ..utils import CompositeSampler

try:
    from logfmter import Logfmter
except ImportError:
    Logfmter = None

_logger = logging.getLogger("opentelemetry.distro.odoo.loader")


class OdooFilter(logging.Filter):
    def __init__(self):
        self._exclude = {
            "werkzeug",
            "longpolling",
            "odoo.addons.bus.models.bus",
        }
        self._exclude.union(set(os.getenv(ODOO_OTEL_LOGS_FILTER, "").split(",")))

    def filter(self, record):
        return record.name not in self._exclude


_EXPORTER_ENV_BY_SIGNAL_TYPE = {
    "traces": OTEL_TRACES_EXPORTER,
    "metrics": OTEL_METRICS_EXPORTER,
    "logs": OTEL_LOGS_EXPORTER,
}


def _get_exporter_names(signal_type: Literal["traces", "metrics", "logs"]) -> Sequence[str]:
    names = os.environ.get(_EXPORTER_ENV_BY_SIGNAL_TYPE.get(signal_type, ""))
    if not names or names.lower().strip() == "none":
        return []
    return [_get_exporter_entry_point(_exporter.strip(), signal_type) for _exporter in names.split(",")]


class OtelLoader:
    def __init__(self, distro: BaseDistro):
        self.resource = self._create_otel_odoo_resource()
        self._distro = distro
        self._sampler: Sampler = None

    def _create_otel_odoo_resource(self) -> Resource:
        os.environ[OTEL_EXPERIMENTAL_RESOURCE_DETECTORS] = "odoo," + os.getenv(
            OTEL_EXPERIMENTAL_RESOURCE_DETECTORS, "otel"
        )
        if os.getenv(ODOO_OTEL_DISTRO_DEFAULT_RESOURCE_DETECTORS, "True").lower() == "true":
            os.environ[OTEL_EXPERIMENTAL_RESOURCE_DETECTORS] = "os,process,host," + os.getenv(
                OTEL_EXPERIMENTAL_RESOURCE_DETECTORS
            )
        resource = Resource.create({})
        _logger.info("resource %s", resource.to_json(indent=4))
        return resource

    def load_exporters(self):
        span_exporters, metric_exporters, log_exporters = _import_exporters(
            _get_exporter_names("traces"), _get_exporter_names("metrics"), _get_exporter_names("logs")
        )
        _logger.debug("span_exporters %s", span_exporters)
        _logger.debug("metric_exporters %s", metric_exporters)
        _logger.debug("log_exporters %s", log_exporters)
        _init_tracing(span_exporters, resource=self.resource, sampler=self._sampler)
        _init_metrics(metric_exporters, resource=self.resource)
        _init_logging(log_exporters, resource=self.resource, setup_logging_handler=False)

    def load_samplers(self):
        sampler = os.environ.get(OTEL_TRACES_SAMPLER)
        sampler_args = os.environ.get(OTEL_TRACES_SAMPLER_ARG)
        if sampler not in _KNOWN_SAMPLERS:
            _logger.debug("Custom sampler [%s] auto importing it", sampler)
        self._sampler = self._import_sampler(sampler, sampler_args)
        if not isinstance(self._sampler, CompositeSampler):
            return

        default_custom_sampler = os.environ.get(ODOO_OTEL_TRACE_CUSTOM_DEFAULT, "parentbased_traceidratio")
        default_custom_sampler_args = os.environ.get(ODOO_OTEL_TRACE_CUSTOM_DEFAULT_ARGS, "0.1")
        for custom_sampler in os.environ.get(ODOO_OTEL_TRACE_CUSTOM, "").split(","):
            parts = custom_sampler.strip().split(":")
            if len(parts) == 1:
                span_name, sampler_name, sampler_args = parts[0], default_custom_sampler, default_custom_sampler_args
            elif len(parts) == 2:
                span_name, sampler_name, sampler_args = parts[0], parts[1], default_custom_sampler_args
            elif len(parts) == 3:
                span_name, sampler_name, sampler_args = parts[0], parts[1], parts[2]
            else:
                raise ValueError(
                    "ODOO_OTEL_TRACE_CUSTOM must be a comma separated list in format : "
                    "span_name[:sampler_name[:sampler_args]]"
                )
            sub_sampler = self._import_sampler(sampler_name, sampler_args)
            self._sampler.add_sampler_for_name(span_name, sub_sampler)
        _logger.debug("Custom sampler [%s] imported : %s", sampler, self._sampler.get_description())

    def _import_sampler(sefl, sampler_name: str, sampler_args: str) -> Sampler | None:
        if not sampler_name:
            return None
        try:
            sampler_factory = _import_sampler_factory(sampler_name)
            if sampler_name.endswith("traceidratio"):
                try:
                    rate = float(sampler_args)
                except (ValueError, TypeError):
                    _logger.warning("Could not convert TRACES_SAMPLER_ARG to float. Using default value 1.0.")
                    rate = 1.0
                arg = rate
            else:
                arg = sampler_args

            sampler = sampler_factory(arg)
            if not isinstance(sampler, Sampler):
                message = f"Sampler factory, {sampler_factory}, produced output, {sampler}, which is not a Sampler."
                _logger.warning(message)
                raise ValueError(message)
            return sampler
        except Exception as exc:  # pylint: disable=broad-exception-caught
            _logger.warning(
                "Using default sampler. Failed to initialize sampler, %s: %s",
                sampler_name,
                exc,
            )
            return None

    def load_instrument(self):
        _load_instrumentors(self._distro)

    def setup_logging(self):
        handler = LoggingHandler(level=logging.DEBUG)
        handler.addFilter(OdooFilter())
        if Logfmter:
            handler.setFormatter(Logfmter())
        else:
            handler.setFormatter(logging.Formatter(os.getenv(ODOO_OTEL_LOG_FORMAT) or ODOO_OTEL_LOG_FORMAT_DEFAULT))
        logging.getLogger().addHandler(handler)
