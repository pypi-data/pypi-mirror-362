# Copyright 2025 Som IT Cooperatiu SCCL - Nicolás Ramos <nicolas.ramos@somit.coop>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)

import json
from lxml import etree

from odoo import _, fields, models


class HelpdeskTicketStage(models.Model):
    _inherit = "helpdesk.ticket.stage"

    next_stage_ids = fields.Many2many(
        "helpdesk.ticket.stage",
        string="Next stages",
        relation="helpdesk_ticket_stage_next_stage_rel",
        column1="stage_id",
        column2="next_stage_id",
        help="Define the stages that can be reached from this stage.",
    )
    previous_stage_ids = fields.Many2many(
        "helpdesk.ticket.stage",
        string="Previous stages",
        relation="helpdesk_ticket_stage_next_stage_rel",
        column1="next_stage_id",
        column2="stage_id",
        help="Stages from which this stage can be reached. This is the inverse of next_stage_ids.",
        readonly=True,  # This field is typically read-only as it's the inverse of next_stage_ids
    )

    def _get_stage_node_attrs(self):
        """
        Returns the attributes for the button node in the form view.
        The button will be invisible if the current ticket's stage is not
        among the previous stages defined for this target stage.
        """
        return {"invisible": [("stage_id", "not in", self.previous_stage_ids.ids)]}

    def _get_stage_node_name(self):
        """Returns the string for the button node."""
        return _("To %s") % self.name

    def _get_stage_node(self):
        """
        Generates an lxml etree Element representing a button for this stage.
        This button, when clicked, will call the 'set_helpdesk_ticket_stage' method
        on the 'helpdesk.ticket' model, passing this stage's ID in the context.
        The button will be invisible if the current ticket's stage_id is not
        among the previous_stage_ids of this target stage.
        """
        attrs = self._get_stage_node_attrs()
        button_attributes = {
            "name": "action_set_helpdesk_ticket_stage",
            "id": str(self.id),
            "type": "object",
            "class": "oe_highlight btn-primary",  # Hardcoded to btn-primary
            "context": json.dumps({"next_stage_id": self.id}),
            "attrs": json.dumps(attrs),
            "string": self._get_stage_node_name(),
        }

        if not any(key for key in attrs if key != "invisible" and attrs[key]):
            button_attributes["invisible"] = json.dumps(attrs["invisible"])

        return etree.Element("button", attrib=button_attributes)
