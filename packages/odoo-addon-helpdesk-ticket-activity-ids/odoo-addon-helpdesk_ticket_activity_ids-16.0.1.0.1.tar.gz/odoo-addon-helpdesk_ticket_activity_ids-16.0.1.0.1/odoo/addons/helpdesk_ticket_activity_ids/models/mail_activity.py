from odoo import models, api, fields, _


class MailActivity(models.Model):
    _inherit = "mail.activity"

    date_subject = fields.Text("Date/Subject", compute="_compute_date_subject")

    @api.depends("create_date", "summary")
    def _compute_date_subject(self):
        for activity in self:
            activity.date_subject = (
                f" {activity.create_date.strftime('%Y-%m-%d %H:%M:%S')} \n"
                f" {activity.summary}"
            )

    def action_edit_activity(self):
        self.ensure_one()

        return {
            "name": _("Edit Activity"),
            "type": "ir.actions.act_window",
            "res_model": "mail.activity",
            "views": [[self.env.ref("mail.mail_activity_view_form_popup").id, "form"]],
            "res_id": self.id,
            "target": "new",
            "context": self.env.context,
        }
