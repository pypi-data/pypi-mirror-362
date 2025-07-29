# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Helpdesk Sub-Tags",
    "version": "16.0.1.0.2",
    "depends": [
        "web",
        "helpdesk_mgmt",
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
        ODOO helpdesk customizations for social cooperatives.
        In this module we want to add subtags to the helpdesk tickets.
    """,
    "data": [
        "views/helpdesk_tag_view.xml",
    ],
    "qweb": [
        "static/src/xml/widget_child_selector_tag.xml",
    ],
    "application": False,
    "installable": True,
}
