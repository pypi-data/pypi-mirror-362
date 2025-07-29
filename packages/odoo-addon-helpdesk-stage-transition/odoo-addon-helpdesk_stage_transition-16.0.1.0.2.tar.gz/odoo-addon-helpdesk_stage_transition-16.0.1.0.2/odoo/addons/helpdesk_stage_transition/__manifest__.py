# Copyright 2025 Som IT Cooperatiu SCCL - Nicolás Ramos <nicolas.ramos@somit.coop>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)
{
    "name": "Helpdesk Stage Transition",
    "summary": """
        Allows to define transitions between helpdesk ticket stages
        and adds buttons to the helpdesk ticket form to trigger them.
        This module also disables drag and drop in the kanban view.
    """,
    "version": "16.0.1.0.2",
    "category": "Services/Helpdesk",
    "author": "Som IT Cooperatiu SCCL",
    "website": "https://somit.coop",
    "license": "AGPL-3",
    "depends": [
        "helpdesk_mgmt",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/helpdesk_ticket_stage_views.xml",
        "views/helpdesk_ticket_views.xml",
    ],
    "maintainers": ["nicolasramos"],
    "installable": True,
    "application": False,
}
