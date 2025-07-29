from odoo import models, fields, _


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    ticket_activity_ids = fields.One2many(related="activity_ids")

    def action_new_activity(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update(
            {
                "default_res_id": self.id,
                "default_res_model": self._name,
                "default_res_model_id": self.env.ref(
                    "helpdesk_mgmt.model_helpdesk_ticket"
                ).id,
            }
        )
        # From Kanban view, a "default_team_id" is set as context refering to
        # `helpdesk.ticket.team` model. But in this method creating a `mail.activity`,
        # "default_team_id" would be taken as a reference to `mail.activity.team` model.
        ctx.pop("default_team_id", None)

        return {
            "name": _("New Activity"),
            "type": "ir.actions.act_window",
            "res_model": "mail.activity",
            "views": [[self.env.ref("mail.mail_activity_view_form_popup").id, "form"]],
            "view_type": "form",
            "res_id": False,
            "target": "new",
            "context": ctx,
        }
