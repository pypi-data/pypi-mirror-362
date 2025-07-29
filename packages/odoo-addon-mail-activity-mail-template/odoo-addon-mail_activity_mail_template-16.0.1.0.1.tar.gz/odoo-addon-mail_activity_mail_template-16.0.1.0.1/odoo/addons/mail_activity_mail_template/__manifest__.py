# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Add default templates to mail activities",
    "version": "16.0.1.0.1",
    "depends": ["mail_activity_board"],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)",
    """,
    "category": "Customer Relationship Management",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Applies a mail template to the note field based on the mail activity type.
    """,
    "demo": [
        "demo/mail_template.xml",
        "demo/mail_activity_type.xml",
    ],
    "data": [
        "views/mail_activity_view.xml",
    ],
    "application": False,
    "installable": True,
}
