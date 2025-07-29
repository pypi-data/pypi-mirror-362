from odoo import models, fields, api, _


class CRMLead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    helpdesk_original_ticket_id = fields.Many2one(
        "helpdesk.ticket", string="Original Ticket Converted", ondelete="set null"
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)

        # Getting the current active_id record from the context
        helpdesk_original_ticket_id = self._context.get(
            "default_helpdesk_original_ticket_id"
        )
        if helpdesk_original_ticket_id:
            active_ticket = self.env["helpdesk.ticket"].browse(
                helpdesk_original_ticket_id
            )
            # We copy some ticket data to this new lead
            defaults.update(
                {
                    "name": active_ticket.name,
                    "description": active_ticket.description,
                    "priority": active_ticket.priority,
                    "partner_id": active_ticket.partner_id.id
                    if active_ticket.partner_id
                    else None,
                    "partner_name": active_ticket.partner_name,
                    "email_from": active_ticket.partner_email,
                }
            )
        return defaults

    @api.model
    def create(self, values):
        result = super(CRMLead, self).create(values)
        if result and result.id and result.helpdesk_original_ticket_id:
            helpdesk_original_ticket_id = result.helpdesk_original_ticket_id
            if helpdesk_original_ticket_id:
                helpdesk_original_ticket_id.crm_lead_id = result.id

                # We have to close the original ticket
                closed_stage_id = self.env["helpdesk.ticket.stage"].search(
                    [("closed", "=", True)], order="sequence asc", limit=1
                )
                if closed_stage_id:
                    helpdesk_original_ticket_id.stage_id = closed_stage_id.id

                # setting the log message in chatter for itself ...
                chatter_messages = {
                    "default_message_original_ticket": _(
                        "This Ticket has been closed and converted into the CRM Lead: ##"
                    ),  # noqa
                    "default_message_crm_lead": _(
                        "This CRM Lead comes from the conversion of the following ticket: ##"
                    ),
                }
                link = (
                    "<a href=# data-oe-model=helpdesk.ticket data-oe-id=%d>%s</a>"
                    % (
                        result.helpdesk_original_ticket_id.id,
                        result.helpdesk_original_ticket_id.number,
                    )
                )
                message = chatter_messages.get("default_message_crm_lead").replace(
                    "##", link
                )
                result.sudo().message_post(body=message)
                # ... and now for the original helpdesk ticket
                link = "<a href=# data-oe-model=crm.lead data-oe-id=%d>%s</a>" % (
                    result.id,
                    result.name,
                )
                message = chatter_messages.get(
                    "default_message_original_ticket"
                ).replace("##", link)
                helpdesk_original_ticket_id.sudo().message_post(body=message)

        return result

    def action_redirect_to_lead(self):
        # Odoo will trigger the create method before this one by default
        self.ensure_one()

        view_id = self.env.ref("sale_crm.crm_case_form_view_oppor").id
        return {
            "type": "ir.actions.act_window",
            "res_model": "crm.lead",
            "res_id": self.id,
            "views": [[view_id, "form"]],
            "view_mode": "form",
            "target": "current",
        }
