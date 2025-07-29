import logging
import os
from typing import Optional, Sequence

from opentelemetry.context import Context
from opentelemetry.sdk.trace.sampling import (
    ALWAYS_OFF,
    DEFAULT_ON,
    ParentBasedTraceIdRatio,
    Sampler,
    SamplingResult,
    TraceIdRatioBased,
)
from opentelemetry.semconv.attributes import url_attributes
from opentelemetry.trace import Link, SpanKind, TraceState
from opentelemetry.util.types import Attributes

from ..utils import CompositeSampler

_logger = logging.getLogger("opentelemetry.distro.odoo")


class OdooTraceSampler(CompositeSampler, ParentBasedTraceIdRatio):
    def __init__(self, rate=1.0):
        super().__init__(rate)
        self._sampler_by_name.update(
            {
                "SELECT": ParentBasedTraceIdRatio(0.001),
                "WITH": ParentBasedTraceIdRatio(0.01),
                "ALTER": DEFAULT_ON,
            }
        )
        self.add_sampler_for_name(
            "queue.job#perform", TraceIdRatioBased(os.environ.get("ODOO_OTEL_TRACE_QUEUE_JOB", 0.1))
        )

    def get_description(self) -> str:
        return "Odoo Trace Sampler"

    def add_sampler_for_name(self, span_name: str, sampler: Sampler):
        super().add_sampler_for_name("odoo: " + span_name, sampler)

    def should_sample(
        self,
        parent_context: Optional["Context"],
        trace_id: int,
        name: str,
        kind: Optional[SpanKind] = None,
        attributes: Attributes = None,
        links: Optional[Sequence["Link"]] = None,
        trace_state: Optional["TraceState"] = None,
    ) -> "SamplingResult":
        attr = attributes or {}
        if attr.get(url_attributes.URL_PATH, "").startswith("/longpolling/"):
            return ALWAYS_OFF.should_sample(parent_context, trace_id, name, kind, attributes, links, trace_state)
        return super().should_sample(parent_context, trace_id, name, kind, attributes, links, trace_state)


def odoo_sampler_factory(arg: str) -> Sampler:
    try:
        rate = float(arg)
    except (ValueError, TypeError):
        _logger.warning("Could not convert TRACES_SAMPLER_ARG to float.")
        rate = 1.0
    return OdooTraceSampler(rate)
