# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Mail activities with chatter",
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
        Adds the chatter functionality in mail activities so notes can be left on them.
    """,
    "demo": [],
    "data": [
        "views/mail_activity_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mail_activity_chatter/static/src/xml/mail_chatter_buttons.xml",
        ],
    },
    "application": False,
    "installable": True,
}
