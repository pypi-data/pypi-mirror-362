# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "version": "16.0.1.0.1",
    "name": "Helpdesk ticket activity ids page view",
    "depends": [
        "mail",
        "mail_activity_team",
        "helpdesk_ticket_mail_message",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Helpdesk",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Adds a page to check and edit all the activities related to a helpdesk.ticket.
    """,
    "data": ["views/helpdesk_ticket.xml", "views/mail_activity.xml"],
    "assets": {
        "web.assets_backend": [
            "helpdesk_ticket_activity_ids/static/src/css/*.css",
            "helpdesk_ticket_activity_ids/static/src/js/*.js",
        ],
    },
    "demo": [],
    "application": False,
    "installable": True,
}
