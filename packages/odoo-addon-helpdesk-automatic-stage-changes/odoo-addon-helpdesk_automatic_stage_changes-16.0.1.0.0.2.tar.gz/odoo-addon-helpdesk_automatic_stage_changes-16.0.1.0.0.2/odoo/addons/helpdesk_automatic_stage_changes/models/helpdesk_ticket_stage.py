# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, _


class HelpdeskTicketStage(models.Model):
    _inherit = "helpdesk.ticket.stage"

    action_user_odoo = fields.Selection(
        selection=[
            ("0", _("Open new ticket")),
            ("1", _("Change stage")),
        ],
        string="Action when a user responds",
    )

    change_stage_to_id = fields.Many2one(
        "helpdesk.ticket.stage", string="Change stage to"
    )

    when_odoo_responds_change_stage_to_id = fields.Many2one(
        "helpdesk.ticket.stage", string="Change stage to (When Odoo responds)"
    )

    color_row = fields.Char("Color Row", default="#000000")

    color_background_row = fields.Char("Color Background Row", default="#FFFFFF")

    def write(self, vals):
        """
        Load stage values to tickets when modifying stages
        """
        for stage in self:
            if vals.get("color_row") or vals.get("color_background_row"):
                tickets = self.env["helpdesk.ticket"].search(
                    [("stage_id", "=", stage.id)]
                )
                vals_tickets = {}
                if vals.get("color_row"):
                    vals_tickets["color_row"] = vals.get("color_row")
                if vals.get("color_background_row"):
                    vals_tickets["color_background_row"] = vals.get(
                        "color_background_row"
                    )
                tickets.write(vals_tickets)
        return super().write(vals)
