# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "ODOO helpdesk tickets with document pages",
    "version": "16.0.1.1.1",
    "depends": [
        "helpdesk_mgmt",
        "document_page",
        "document_page_tag",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)",
    """,
    "category": "Auth",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        ODOO module to relate helpdesk tickets with knowledge document pages.
    """,
    "data": [
        "views/document_page.xml",
        "views/helpdesk_ticket.xml",
    ],
    "demo": [],
    "application": False,
    "installable": True,
}
