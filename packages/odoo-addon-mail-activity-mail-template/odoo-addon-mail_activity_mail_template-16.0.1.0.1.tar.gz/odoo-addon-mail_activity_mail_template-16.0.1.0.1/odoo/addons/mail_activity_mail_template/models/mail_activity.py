from odoo import api, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    @api.onchange("activity_type_id")
    def _onchange_activity_type_id(self):
        if self.activity_type_id and len(self.activity_type_id.mail_template_ids) == 1:
            template = self.activity_type_id.mail_template_ids[0]
            self.note = template.body_html
