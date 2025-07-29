import contextlib
import threading
import timeit
from typing import Any, Callable

from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.metrics import Counter, Histogram, UpDownCounter, get_meter
from opentelemetry.semconv.attributes.error_attributes import ERROR_TYPE
from opentelemetry.trace import Span, Status, StatusCode

from opentelemetry_distro_odoo.semconv.attributes import odoo as odoo_attributes
from opentelemetry_distro_odoo.semconv.metrics import odoo as odoo_metrics
from opentelemetry_distro_odoo.version import __version__


class OdooInstrumentor(BaseInstrumentor):
    odoo_call_sql_queries_count: Counter
    odoo_call_sql_queries_duration: Histogram
    odoo_call_error: Counter
    odoo_call_duration: Histogram
    odoo_report_duration: Histogram
    odoo_send_mail: Counter
    odoo_run_cron: Counter
    worker_count: UpDownCounter
    worker_max: UpDownCounter

    def _instrument(self, **kwargs: Any):
        super()._instrument(**kwargs)
        self._meter = get_meter(__name__, __version__)
        self.odoo_call_error = odoo_metrics.create_odoo_call_error(self._meter)
        self.odoo_call_duration = odoo_metrics.create_odoo_call_duration(self._meter)
        self.odoo_call_sql_queries_count = odoo_metrics.create_odoo_call_sql_queries_count(self._meter)
        self.odoo_call_sql_queries_duration = odoo_metrics.create_call_sql_queries_duration(self._meter)
        self.odoo_report_duration = odoo_metrics.create_odoo_report_duration(self._meter)
        self.odoo_send_mail = odoo_metrics.create_odoo_send_mail(self._meter)
        self.odoo_run_cron = odoo_metrics.create_odoo_run_cron(self._meter)
        self.worker_count = odoo_metrics.create_worker_count(self._meter)
        self.worker_max = odoo_metrics.create_worker_max(self._meter)

    def instrumentation_dependencies(self):
        return []

    def _uninstrument(self, **kwargs: Any):
        pass

    def get_attributes_metrics(self, odoo_record_name, method_name):
        current_thread = threading.current_thread()
        return {
            odoo_attributes.ODOO_MODEL_NAME: odoo_record_name,
            odoo_attributes.ODOO_MODEL_FUNCTION_NAME: method_name,
            odoo_attributes.ODOO_CURSOR_MODE: getattr(current_thread, "cursor_mode", "rw"),
        }

    @contextlib.contextmanager
    def odoo_call_wrapper(
        self,
        odoo_record_name,
        method_name,
        metrics_attrs=None,
        span_attrs=None,
        post_span_callback: Callable[[Span], None] = None,
        common_attrs=None,
    ):
        odoo_attr = self.get_attributes_metrics(odoo_record_name, method_name)

        metrics_attr = dict(odoo_attr)
        metrics_attr.update(common_attrs or {})
        metrics_attr.update(metrics_attrs or {})

        span_attr = dict(odoo_attr)
        span_attr.update(common_attrs or {})
        span_attr.update(span_attrs or {})

        start = timeit.default_timer()
        with trace.get_tracer("odoo.api").start_as_current_span(
            f"odoo: {odoo_record_name}#{method_name}", attributes=span_attr
        ) as span:
            try:
                yield
            except Exception as ex:
                metrics_attr[ERROR_TYPE] = type(ex).__qualname__
                self.odoo_call_error.add(1, metrics_attr)
                span.record_exception(ex)
                span.set_attribute(ERROR_TYPE, type(ex).__qualname__)
                span.set_status(Status(StatusCode.ERROR, str(ex)))
                raise ex
            finally:
                if post_span_callback:
                    post_span_callback(span)
                duration_s = timeit.default_timer() - start
                self.odoo_call_duration.record(duration_s, metrics_attr)
                current_thread = threading.current_thread()
                if hasattr(current_thread, "query_count"):
                    self.odoo_call_sql_queries_count.add(
                        current_thread.query_count,
                        metrics_attr,
                    )
                if hasattr(current_thread, "query_time"):
                    self.odoo_call_sql_queries_duration.record(current_thread.query_time, metrics_attr)
