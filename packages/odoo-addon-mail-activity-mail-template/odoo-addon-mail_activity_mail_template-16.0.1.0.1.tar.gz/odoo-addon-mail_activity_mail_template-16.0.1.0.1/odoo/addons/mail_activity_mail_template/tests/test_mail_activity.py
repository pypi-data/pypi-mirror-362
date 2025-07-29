from odoo.tests.common import TransactionCase


class TestMailActivity(TransactionCase):
    def test_onchange_activity_type_id(self):
        """Test that the note field is updated
        based on the activity type's mail template"""

        mail_activity_type_call = self.env.ref("mail.mail_activity_data_call")
        mail_activity_type_meeting = self.env.ref("mail.mail_activity_data_meeting")

        partner = self.env["res.partner"].create({"name": "Test Partner"})
        mail_activity = self.env["mail.activity"].create(
            {
                "activity_type_id": mail_activity_type_call.id,
                "res_id": partner.id,
                "res_model_id": self.env.ref("base.model_res_partner").id,
            }
        )

        mail_activity._onchange_activity_type_id()

        assert mail_activity.note in mail_activity_type_call.mail_template_ids.body_html

        mail_activity.activity_type_id = mail_activity_type_meeting
        mail_activity._onchange_activity_type_id()

        assert (
            mail_activity.note in mail_activity_type_meeting.mail_template_ids.body_html
        )
