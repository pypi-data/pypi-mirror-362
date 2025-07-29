from odoo import models, fields, _
from odoo.exceptions import UserError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    crm_lead_id = fields.Many2one(
        "crm.lead", string="Created CRM Lead", copy=False, ondelete="set null"
    )
    stage_id_closed = fields.Boolean(
        string="Stage Closed", related="stage_id.closed", readonly=True, store=False
    )

    def convert_to_lead(self):
        """Convert a ticket into a CRM Lead."""

        if len(self) > 1:
            raise UserError(
                _("You are only able to convert to CRM Lead ONE ticket at a time.")
            )
        if self.crm_lead_id:
            raise UserError(_("This ticket can not be reconverted!"))
        if self.stage_id_closed:
            raise UserError(_("This ticket is on a closed stage!"))

        return {
            "name": _("Convert to CRM Lead"),
            "view_mode": "form",
            "view_type": "form",
            "view_id": self.env.ref(
                "helpdesk_ticket_to_lead.crm_lead_conversion_form_wizard", False
            ).id,
            "res_model": "crm.lead",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_helpdesk_original_ticket_id": self.id},
        }
