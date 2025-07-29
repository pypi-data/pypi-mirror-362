from odoo import api, models


class IrCron(models.Model):
    _inherit = "ir.cron"

    @api.model
    def _callback(self, cron_name, server_action_id, *args, **kwargs):
        self.otel_instrumentor.odoo_run_cron.add(1, attributes={"odoo.cron.manual": False})
        with self.start_as_current_span(
            "ir.cron:auto " + cron_name,
            attributes={"odoo.cron.action_id": server_action_id, "odoo.cron.manual": False},
        ):
            return super()._callback(cron_name, server_action_id, *args, **kwargs)

    def method_direct_trigger(self):
        for rec in self:
            (self.otel_instrumentor.odoo_run_cron.add(1, attributes={"odoo.cron.manual": True}))
            with self.start_as_current_span(
                "ir.cron:manual " + rec.name,
                attributes={
                    "odoo.cron.action_id": rec.ir_actions_server_id.id,
                    "odoo.cron.job": rec.id,
                    "odoo.cron.manual": True,
                },
            ):
                super(IrCron, rec).method_direct_trigger()
        return True
