from odoo.tests import common, tagged
from odoo import exceptions
from odoo.tools.translate import _


@tagged("post_install", "helpdesk_ticket_to_lead")
class TestHelpdeskConversion(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.helpdesk_stage_closed = self.env["helpdesk.ticket.stage"].search(
            [("closed", "=", True)], limit=1
        )
        self.helpdesk_any_stage = self.env["helpdesk.ticket.stage"].search(
            [("closed", "!=", True)], limit=1
        )
        self.ticket = self.env["helpdesk.ticket"].create(
            {
                "name": _("Test Ticket"),
                "description": _("This is a test ticket."),
                "priority": "3",
                "partner_id": self.env["res.partner"].search([], limit=1)[0].id,
                "partner_name": _("Test Client"),
                "partner_email": "test@example.com",
                "stage_id": self.helpdesk_any_stage.id,
            }
        )

    def test_convert_ticket_to_lead_returned_action(self):
        """
        Test the the view returned by the new action in ticket.
        """
        view_dict = self.ticket.convert_to_lead()

        # We simply proceed to test the view dictionary returned
        self.assertEqual(view_dict.get("view_mode"), "form")
        self.assertEqual(
            view_dict.get("view_id"),
            self.env.ref(
                "helpdesk_ticket_to_lead.crm_lead_conversion_form_wizard", False
            ).id,
            "The ir.ui.view is not the proper one.",
        )
        self.assertEqual(view_dict.get("res_model"), "crm.lead", "View model is wrong.")
        self.assertEqual(
            view_dict.get("type"),
            "ir.actions.act_window",
            "Wrong action type for the view.",
        )
        self.assertEqual(
            view_dict.get("target"),
            "new",
            "The target of the view has to always be 'new'.",
        )
        self.assertTrue(view_dict.get("context"), "Context is now present in the view.")
        self.assertEqual(
            view_dict.get("context").get("default_helpdesk_original_ticket_id"),
            self.ticket.id,
            "Context default_helpdesk_original_ticket_id is non existant or not the right one.",
        )

    def test_convert_ticket_to_lead_conditionals(self):
        """
        Test the the inner conditionals in the action of the ticket.
        """
        another_ticket = self.ticket.copy()

        # when the action is called upon more than one tickets selected
        with self.assertRaises(exceptions.UserError):
            recordset = self.env["helpdesk.ticket"].search(
                [("id", "in", [self.ticket.id, another_ticket.id])]
            )
            recordset.convert_to_lead()

        ctx = {
            "default_message_original_ticket": "This Ticket has been closed and converted into the CRM Lead: ##",
            "default_message_crm_lead": "This CRM Lead comes from the conversion of the following ticket: ##",
        }
        self.env["crm.lead"].with_context(ctx).create(
            {
                "name": _("Test Lead"),
                "description": _("This is a test lead."),
                "priority": "3",
                "partner_id": self.env["res.partner"].search([], limit=1)[0].id,
                "partner_name": _("Test Client"),
                "email_from": "test@example.com",
                "helpdesk_original_ticket_id": another_ticket.id,
            }
        )

        # when the ticket has been already converted before
        with self.assertRaises(exceptions.UserError):
            another_ticket.convert_to_lead()

        # the ticket is in the wrong stage_id
        with self.assertRaises(exceptions.UserError):
            self.ticket.stage_id = self.helpdesk_stage_closed.id
            self.ticket.convert_to_lead()

    def test_lead_default_get(self):
        """
        Test the crm.lead default_get method returning the right
        list of fields given a ticket id in the context.
        """
        ctx = {
            "default_helpdesk_original_ticket_id": self.ticket.id,
            "default_message_original_ticket": "This Ticket has been closed and converted into the CRM Lead: ##",
            "default_message_crm_lead": "This CRM Lead comes from the conversion of the following ticket: ##",
        }
        true_fields = {
            "name": self.ticket.name,
            "description": self.ticket.description,
            "priority": self.ticket.priority,
            "partner_id": self.ticket.partner_id.id if self.ticket.partner_id else None,
            "partner_name": self.ticket.partner_name,
            "email_from": self.ticket.partner_email,
        }
        default_fields = (
            self.env["crm.lead"].with_context(ctx).default_get(true_fields.keys())
        )

        for field in true_fields.keys():
            self.assertEqual(
                default_fields.get(field),
                true_fields[field],
                "The default value of the field {} of crm.lead is not the expected".format(
                    field
                ),
            )

    def test_lead_create(self):
        """
        Test the crm.lead create method given a ticket id in the context.
        """
        ctx = {
            "default_helpdesk_original_ticket_id": self.ticket.id,
            "default_message_original_ticket": "This Ticket has been closed and converted into the CRM Lead: ##",
            "default_message_crm_lead": "This CRM Lead comes from the conversion of the following ticket: ##",
        }
        crm_lead = self.env["crm.lead"].with_context(ctx).create({})

        # Checking the stage of the ticket
        self.assertTrue(
            crm_lead.helpdesk_original_ticket_id.stage_id.closed,
            "The ticket that generated the lead is not in a closed stage",
        )

        # Now checking the messages for both

        self.assertTrue(
            crm_lead.message_ids.filtered(
                lambda x: '<a href="#" data-oe-model="helpdesk.ticket" data-oe-id="'
                in x.body
            ),
            "No mail.message found on crm.lead pointing to origin ticket.",
        )
        self.assertTrue(
            self.ticket.message_ids.filtered(
                lambda x: '<a href="#" data-oe-model="crm.lead" data-oe-id="' in x.body
            ),
            "No mail.message found on helpdesk.ticket pointing to converted lead.",
        )

    def test_lead_redirect(self):
        """
        Test the action_redirect_to_lead method in the ticket.
        """
        test_ticket_redirect = self.ticket.copy()

        ctx = {
            "default_helpdesk_original_ticket_id": test_ticket_redirect.id,
        }

        created_lead = (
            self.env["crm.lead"]
            .with_context(ctx)
            .create(
                {
                    "name": _("Test Lead Readirect"),
                    "description": _(
                        "Test redirection after lead creation from ticket."
                    ),
                    "priority": "3",
                    "partner_id": self.env["res.partner"].search([], limit=1)[0].id,
                    "partner_name": _("Test Client"),
                    "email_from": "test@example.com",
                    "helpdesk_original_ticket_id": test_ticket_redirect.id,
                }
            )
        )

        view_dict = created_lead.action_redirect_to_lead()

        # We simply proceed to test the view dictionary returned
        self.assertEqual(view_dict.get("view_mode"), "form")
        self.assertEqual(
            view_dict.get("view_id") or view_dict.get("views")[0][0],
            self.env.ref("sale_crm.crm_case_form_view_oppor", False).id,
            "The ir.ui.view is not the proper one.",
        )
        self.assertEqual(view_dict.get("res_model"), "crm.lead", "View model is wrong.")
        self.assertEqual(
            view_dict.get("type"),
            "ir.actions.act_window",
            "Wrong action type for the view.",
        )
        self.assertEqual(
            view_dict.get("target"),
            "current",
            "The target of the view has to always be 'current'.",
        )
        self.assertTrue(
            view_dict.get("res_id"), "The res_id is not present in the view."
        )
        self.assertEqual(
            view_dict.get("res_id"),
            test_ticket_redirect.crm_lead_id.id,
            "The res_id is not the right one.",
        )
