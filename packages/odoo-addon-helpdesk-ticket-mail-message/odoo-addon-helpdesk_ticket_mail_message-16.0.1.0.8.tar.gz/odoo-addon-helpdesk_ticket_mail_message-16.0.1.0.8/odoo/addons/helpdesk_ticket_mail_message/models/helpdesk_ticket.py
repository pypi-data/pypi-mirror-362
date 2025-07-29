from markupsafe import Markup
from odoo import models, fields, api, tools, _


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    name = fields.Char(string="Title", required=True, size=100)
    message_emails_ids = fields.One2many(
        "mail.message", compute="_compute_emails", string="Messages"
    )
    color_row = fields.Char("Color Row", default="#000000")
    color_background_row = fields.Char("Color Background Row", default="#FFFFFF")
    partner_category_id = fields.Many2many(
        related="partner_id.category_id", string="Partner Category", readonly=True
    )

    partner_contact_phone = fields.Char(
        related="partner_id.phone",
        string="Partner Phone",
        readonly=True,
    )

    @api.depends("message_ids")
    def _compute_emails(self):
        for record in self:
            emails_ids = [
                msg_id.id
                for msg_id in record.message_ids
                if msg_id.message_type in ("email", "comment") and msg_id.body
            ]
            record.message_emails_ids = [(6, 0, emails_ids)]

    def mail_compose_message_action(self):
        """
        Open new communication sales according to requirements
        """
        action = self.env.ref(
            "helpdesk_ticket_mail_message." "action_mail_compose_message_wizard"
        ).read()[0]
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "mass_mail",
                "default_template_id": self.env.ref(
                    "helpdesk_ticket_mail_message.created_response_ticket_template"
                ).id
                or False,
                "default_email_to": self.partner_email,
                "default_subject": _("The Ticket %s", self.number),
                "default_body": self.description,
                "default_message_type_mail": "email_sent",
                "active_model": self._name,
                "active_id": self.id,
                "active_ids": [self.id],
                "skip_onchange_template_id": True,
            }
        )
        action["context"] = ctx
        return action

    def mail_compose_message_action_note(self):
        """
        Open new communication sales according to requirements
        """
        action = self.env.ref(
            "helpdesk_ticket_mail_message." "action_mail_compose_message_wizard"
        ).read()[0]
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "comment",
                "default_is_log": True,
                "active_model": self._name,
                "active_id": self.id,
                "active_ids": [self.id],
                "default_subject": self.name,
                "default_body": Markup(""),
            }
        )
        action["context"] = ctx
        action["name"] = _("Create note")
        return action

    def _message_get_default_recipients(self):
        """
        Override for helpdesk tickets (as in crm.lead) to avoid the email composer
        to suggest addresses based on ticket partners, since it was causing duplicates
        for gmail accounts.
        """
        return {
            r.id: {
                "partner_ids": [],
                "email_to": ",".join(tools.email_normalize_all(r.partner_email))
                or r.partner_email,
                "email_cc": False,
            }
            for r in self.sudo()
        }

    def chatter_note_action(self):
        """
        Client action to scroll to the top of the chatter and trigger
        the note creation.
        """
        self.ensure_one()

        return {
            "type": "ir.actions.client",
            "tag": "chatter_note_action",
            "params": {
                "model": self._name,
                "res_id": self.id,
                "res_ids": self.ids,
            },
        }
