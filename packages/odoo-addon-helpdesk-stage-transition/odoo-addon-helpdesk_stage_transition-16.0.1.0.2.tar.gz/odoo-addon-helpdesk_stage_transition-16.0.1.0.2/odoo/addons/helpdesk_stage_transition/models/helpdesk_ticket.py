# Copyright 2025 Som IT Cooperatiu SCCL - Nicolás Ramos <nicolas.ramos@somit.coop>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)

from lxml import etree

from odoo import api, fields, models
from odoo.addons.base.models.ir_ui_view import (
    transfer_node_to_modifiers,
    transfer_modifiers_to_node,
)


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    stage_id = fields.Many2one(readonly=True, copy=False)

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """
        Dynamically modifies the form view to add stage transition buttons in the header.
        It also makes the kanban view non-draggable by setting group_draggable=False.
        """
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == "form":
            doc = etree.XML(res["arch"])
            header = doc.xpath("//form/header")
            if header:
                header = header[0]
                for button in header.xpath("//button[starts-with(@id, 'stage_btn_')]"):
                    header.remove(button)

                stages = self.env["helpdesk.ticket.stage"].search(
                    [], order="sequence desc"
                )
                for stage in stages:
                    node = stage._get_stage_node()
                    if "id" not in node.attrib or not node.attrib["id"]:
                        node.set("id", f"stage_btn_{stage.id}")
                    modifiers = {}
                    transfer_node_to_modifiers(node, modifiers)
                    transfer_modifiers_to_node(modifiers, node)
                    header.insert(0, node)
                res["arch"] = etree.tostring(doc, encoding="unicode")

        elif view_type == "kanban":
            doc = etree.XML(res["arch"])
            for node in doc.xpath("//kanban"):
                node.set("group_draggable", "false")
            res["arch"] = etree.tostring(doc, encoding="unicode")

        return res

    def action_set_helpdesk_ticket_stage(self):
        """
        Action method called by the dynamically generated buttons.
        It reads the target stage ID from the context and calls the internal method.
        """
        self.ensure_one()
        next_stage_id = self.env.context.get("next_stage_id")
        if next_stage_id:
            return self._set_helpdesk_ticket_stage(next_stage_id)
        return False

    def _set_helpdesk_ticket_stage(self, stage_id):
        """
        Internal method to write the new stage_id to the ticket.
        Potentially, more logic could be added here (e.g., logging, checks).
        """
        for ticket in self:
            if (
                ticket.stage_id
                and stage_id not in ticket.stage_id.next_stage_ids.ids
                and ticket.stage_id.next_stage_ids
            ):
                pass
            ticket.write({"stage_id": stage_id})
        return True

    def write(self, vals):
        if "stage_id" in vals and self.stage_id:
            new_stage_id = vals["stage_id"]
            current_stage = self.stage_id
            if (
                current_stage.next_stage_ids
                and new_stage_id not in current_stage.next_stage_ids.ids
            ):
                pass
        return super().write(vals)
