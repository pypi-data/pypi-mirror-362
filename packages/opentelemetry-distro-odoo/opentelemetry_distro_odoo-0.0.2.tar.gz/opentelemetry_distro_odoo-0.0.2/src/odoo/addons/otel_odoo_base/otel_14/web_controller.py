import timeit

from odoo import http

from odoo.addons.web.controllers.main import DataSet, ReportController

from opentelemetry_distro_odoo.instrumentation.odoo import OdooInstrumentor


class OTelDataSet14(DataSet):
    @http.route()
    def search_read(self, model, fields=False, offset=0, limit=False, domain=None, sort=None):
        with OdooInstrumentor().odoo_call_wrapper(model, "search_read"):
            return super().search_read(model, fields, offset, limit, domain, sort)

    @http.route()
    def load(self, model, id, fields):
        with OdooInstrumentor().odoo_call_wrapper(model, "load"):
            return super().search_read(model, id, fields)

    @http.route()
    def call(self, model, method, args, domain_id=None, context_id=None):
        with OdooInstrumentor().odoo_call_wrapper(model, method):
            return super().call(model, method, args, domain_id, context_id)

    @http.route()
    def call_kw(self, model, method, args, kwargs, path=None):
        with OdooInstrumentor().odoo_call_wrapper(model, method):
            return super().call_kw(model, method, args, kwargs, path)

    @http.route()
    def call_button(self, model, method, args, kwargs):
        with OdooInstrumentor().odoo_call_wrapper(model, method):
            return super().call_button(model, method, args, kwargs)

    @http.route()
    def resequence(self, model, ids, field="sequence", offset=0):
        with OdooInstrumentor().odoo_call_wrapper(model, "resequence"):
            return super().resequence(model, ids, field, offset)


class OTelReportController(ReportController):
    @http.route()
    def report_routes(self, reportname, docids=None, converter=None, **data):
        instrument = OdooInstrumentor()
        start = timeit.default_timer()
        try:
            return super().report_routes(reportname=reportname, docids=docids, converter=converter, **data)
        except Exception as e:
            raise e
        finally:
            duration_s = timeit.default_timer() - start
            instrument.odoo_report_duration.record(duration_s, {"report": reportname, "converter": converter})
