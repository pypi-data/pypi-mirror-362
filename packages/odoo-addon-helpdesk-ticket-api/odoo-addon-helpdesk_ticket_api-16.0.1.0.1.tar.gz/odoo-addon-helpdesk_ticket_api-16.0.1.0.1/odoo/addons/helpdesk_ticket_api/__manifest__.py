{
    "version": "16.0.1.0.1",
    "name": "Helpdesk ticket API",
    "depends": [
        "api_common_base",
        "helpdesk_mgmt",
        "contacts",
        "helpdesk_ticket_contract_contract",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Customer Relationship Management",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Expose an API-Key authenticated API to get and create helpdesk tickets.
    """,
    "data": [
        "views/helpdesk_ticket_category.xml",
        "views/helpdesk_ticket_channel.xml",
        "views/helpdesk_ticket_stage.xml",
        "views/helpdesk_ticket_tag.xml",
        "views/helpdesk_ticket_team.xml",
    ],
    "demo": [
        "demo/helpdesk_ticket_category.xml",
        "demo/helpdesk_ticket_channel.xml",
        "demo/helpdesk_ticket_stage.xml",
        "demo/helpdesk_ticket_tag.xml",
        "demo/helpdesk_ticket_team.xml",
    ],
    "application": False,
    "installable": True,
}
