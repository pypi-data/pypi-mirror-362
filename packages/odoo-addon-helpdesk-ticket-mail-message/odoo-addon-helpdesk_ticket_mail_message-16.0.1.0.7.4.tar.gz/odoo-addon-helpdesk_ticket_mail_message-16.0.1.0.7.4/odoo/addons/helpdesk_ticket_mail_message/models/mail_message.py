from markupsafe import Markup
from odoo import api, models, fields, tools, _


class Message(models.Model):
    """Messages model: system notification (replacing res.log notifications),
    comments (OpenChatter discussion) and incoming emails."""

    _inherit = "mail.message"

    color_row = fields.Char("Color Row", default="#000000")
    color_background_row = fields.Char("Color Background Row", default="#FFFFFF")
    date_subject = fields.Text("Date/Subject", compute="_compute_date_subject")
    message_type_mail = fields.Selection(
        selection=[
            ("email_sent", _("Mail sent")),
            ("email_received", _("Email received")),
            ("note", _("Note")),
        ],
        string="Message type",
    )

    @api.depends("date", "subject")
    def _compute_date_subject(self):
        for mail in self:
            mail.date_subject = (
                f" {mail.date.strftime('%Y-%m-%d %H:%M:%S')} \n" f" {mail.subject}"
            )

    @api.model
    def create(self, values):
        """
        When creating a new message, color it depending of its type
        (sent, recieved, note) and update its ticket if it is related to one
        """
        if values.get("model") == "helpdesk.ticket" and values.get("res_id"):
            ticket = self.env["helpdesk.ticket"].browse(values.get("res_id"))
            if not ticket:
                return super(Message, self).create(values)

            if values.get("message_type") == "email":
                values["color_row"] = "#FFFFFF"
                if self._context.get(
                    "default_message_type_mail"
                ) == "email_sent" or self.env.user.company_id.email == values.get(
                    "email_from"
                ):
                    values["message_type_mail"] = "email_sent"
                    values["color_background_row"] = "#FF0000"
                else:
                    values["message_type_mail"] = "email_received"
                    values["color_background_row"] = "#000000"
            elif values.get("message_type") == "comment":
                values["message_type_mail"] = "note"
                values["color_background_row"] = "#23FF00"

        return super(Message, self).create(values)

    def mail_compose_action(self):
        if self.message_type == "email":
            return self.mail_compose_message_action()
        elif self.message_type == "comment":
            res_model = self._context.get("params", {}).get("model")
            if res_model == "helpdesk.ticket":
                res_id = self._context.get("params", {}).get("id")
                ticket = self.env["helpdesk.ticket"].browse(res_id)
                if ticket:
                    return ticket.chatter_note_action()
            return self.mail_compose_message_action_note()
        else:
            return False

    def _prepare_action_mail_compose_with_context(
        self, composition_mode, is_resend=False
    ):
        """
        Prepare action mail_compose_message for tickets with context,
        depending on the composition_mode and other parameters
        """
        if not self.res_id or not self.model == "helpdesk.ticket":
            return {}
        ticket = self.env["helpdesk.ticket"].browse(self.res_id)

        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": composition_mode,
                "default_email_from": self._get_message_email_from_for_reply(
                    ticket.team_id.alias_id if ticket.team_id else None
                ),
                "default_email_to": self.email_from,
                "default_no_atuto_thread": True,
                "default_reply_to": self.email_from,
                "default_parent_id": self.id,
                "default_body": self._get_message_body_for_reply(),
                "default_template_id": False,
                "active_model": self.model,
                "active_id": self.res_id,
                "active_ids": [self.res_id],
                "default_subject": self._get_message_subject_for_reply(
                    is_resend, ticket.number
                ),
                "default_message_type_mail": "email_sent",
                "default_is_log": (composition_mode == "comment"),
            }
        )

        action = self.env.ref(
            "helpdesk_ticket_mail_message.action_mail_compose_message_wizard"
        ).read()[0]
        action.update(
            {
                "src_model": "helpdesk.ticket",
                "context": ctx,
            }
        )

        return action

    def mail_compose_message_action(self):
        """
        Open new communication to send mail
        """
        return self._prepare_action_mail_compose_with_context("mass_mail")

    def mail_compose_message_action_all(self):
        """
        Open new communication to send mail with CC
        """
        action = self._prepare_action_mail_compose_with_context("mass_mail")
        self.email_cc = self._get_message_email_cc_for_reply_all(action)
        action["context"].update({"default_email_cc": self.email_cc})
        return action

    def mail_compose_message_action_resend(self):
        """
        Open new communication to reply
        """
        return self._prepare_action_mail_compose_with_context(
            "mass_mail", is_resend=True
        )

    def mail_compose_message_action_note(self):
        """
        Open new communication to create a note
        """
        res = self._prepare_action_mail_compose_with_context("comment")
        res["context"].update({"default_body": Markup("")})
        res["name"] = _("Create note")

        return res

    def _get_message_body_for_reply(self):
        email_from = tools.email_normalize(self.email_from) or self.email_from
        email_to = ", ".join(set(tools.email_normalize_all(self.email_to)))
        email_cc = ", ".join(set(tools.email_normalize_all(self.email_cc)))

        return Markup(
            _(
                "<hr><blockquote>"
                "<p><b>From:</b> {email_from}</p>"
                "<p><b>Sent at:</b> {date}</p>"
                "<p><b>To:</b> {email_to}</p>"
                "<p><b>CC:</b> {email_cc}</p>"
                "<p><b>Subject:</b> {subject}</p>"
                "{body}"
                "</blockquote>"
            ).format(
                email_from=email_from,
                date=self.date,
                email_to=email_to or (self.email_to or ""),
                email_cc=email_cc or (self.email_cc or ""),
                subject=self.subject,
                body=self.body,
            )
        ).unescape()

    def _get_message_subject_for_reply(self, is_resend, ticket_number=None):
        refwd_suffix = _("Fwd:") if is_resend else _("Re:")
        ticket_number = f"[{ticket_number}]" if ticket_number else ""
        return (
            self.subject
            if refwd_suffix in self.subject
            else f"{refwd_suffix}{ticket_number} {self.subject}"
        )

    def _get_message_email_from_for_reply(self, team_alias_id=None):
        """
        Get email_from for reply for ticket messages.
        If the ticket has a team assigned, use the team's email;
        otherwise, use the authenticated user's email or the company email.
        """
        if team_alias_id and team_alias_id.alias_domain and team_alias_id.alias_name:
            return f"{team_alias_id.alias_name}@{team_alias_id.alias_domain}"
        return self.env.user.email_formatted or self.env.user.company_id.email_formatted

    def _get_message_email_cc_for_reply_all(self, action={}):
        """
        Get the email CC for the reply all message
        """
        ignore_addresses = set({})
        for server in self.env["fetchmail.server"].sudo().search([]):
            if server.user and "@" in str(server.user):
                ignore_addresses.add(tools.email_normalize(server.user))

        if action.get("default_email_from"):
            ignore_addresses.add(
                tools.email_normalize(action.get("default_email_from"))
            )

        email_cc = set(
            tools.email_normalize_all(self.email_cc)
            + tools.email_normalize_all(self.email_to)
        )
        email_cc -= ignore_addresses
        return ",".join(sorted(email_cc)) if email_cc else ""
