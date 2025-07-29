from odoo.addons.queue_job.controllers.main import RunJobController

from opentelemetry_distro_odoo.instrumentation.odoo import OdooInstrumentor


class OTelRunJobController(RunJobController):
    def _try_perform_job(self, env, job):
        def _post_callback(span):
            span.set_attribute("odoo.queue.job.uuid", job.uuid)
            span.set_attribute("odoo.queue.job.model_name", job.model_name)
            span.set_attribute("odoo.queue.job.method_name", job.method_name)
            span.set_attribute("odoo.queue.job.func_string", job.func_string)
            span.set_attribute("odoo.queue.job.state", job.state)

        with OdooInstrumentor().odoo_call_wrapper(
            "queue.job",
            "perform",
            span_attrs=job._store_values(),
            post_span_callback=_post_callback,
            common_attrs={"odoo.queue.job.channel": job.channel},
        ):
            return super()._try_perform_job(env, job)
