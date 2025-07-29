from __future__ import annotations

import contextlib
import logging
from typing import Iterator

from opentelemetry import trace
from opentelemetry import trace as trace_api
from opentelemetry.context import Context
from opentelemetry.trace import Span, SpanKind, _Links
from opentelemetry.util import types

from odoo import api, models

from opentelemetry_distro_odoo.instrumentation.odoo import OdooInstrumentor

_logger = logging.getLogger(__name__)


class OpenTelemetryBase(models.AbstractModel):
    _inherit = "base"

    @api.model
    def flush(self, fnames=None, records=None):
        if self._name != "base" and not fnames and not records:
            with self.start_as_current_span(f"full flush {self._name}"):
                return super().flush()
        return super().flush(fnames, records)

    def _compute_field_value(self, field):
        attr = {
            "odoo.compute.field": str(field),
            "odoo.compute.ids": self.ids,
            "odoo.compute.name": self._name,
        }
        with self.start_as_current_span(f"compute {field}", attributes=attr):
            return super()._compute_field_value(field)

    @api.model
    def _get_surrent_span(self) -> Span:
        return trace.get_current_span()

    @property
    def otel_instrumentor(self) -> OdooInstrumentor:
        return OdooInstrumentor()

    def start_span(
        self,
        name: str,
        context: Context | None = None,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: _Links = None,
        start_time: int | None = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
    ) -> Span:
        return trace_api.get_tracer("odoo").start_span(
            name,
            context=context,
            kind=kind,
            attributes=attributes,
            links=links,
            start_time=start_time,
            record_exception=record_exception,
            set_status_on_exception=set_status_on_exception,
        )

    @contextlib.contextmanager
    def start_as_current_span(
        self,
        name: str,
        context: Context | None = None,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: _Links = None,
        start_time: int | None = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
        end_on_exit: bool = True,
    ) -> Iterator[Span]:
        with trace_api.get_tracer("odoo").start_as_current_span(
            name,
            context=context,
            kind=kind,
            attributes=attributes,
            links=links,
            start_time=start_time,
            record_exception=record_exception,
            set_status_on_exception=set_status_on_exception,
            end_on_exit=end_on_exit,
        ) as span:
            yield span
