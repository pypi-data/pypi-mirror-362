# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "SomItCoop ODOO helpdesk automove",
    "version": "16.0.1.0.2",
    "depends": [
        "helpdesk_mgmt",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Auth",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        ODOO helpdesk customizations for social cooperatives.
        In this module we want to move our desk cards between
        stages with timming conditions.
    """,
    "data": [
        "views/helpdesk_ticket_stage_automove.xml",
        "data/helpdesk_automove_cron.xml",
    ],
    "application": False,
    "installable": True,
}
