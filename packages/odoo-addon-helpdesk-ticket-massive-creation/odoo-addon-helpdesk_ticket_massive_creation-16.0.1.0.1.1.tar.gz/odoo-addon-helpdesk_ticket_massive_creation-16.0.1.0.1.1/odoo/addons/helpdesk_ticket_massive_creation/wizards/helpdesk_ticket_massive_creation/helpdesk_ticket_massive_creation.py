from odoo import api, fields, models


class HelpdeskTicketMassiveCreation(models.TransientModel):
    _name = "helpdesk.ticket.massive.creation.wizard"
    _description = "Helpdesk Ticket Massive Creation Wizard"

    res_partner_ids = fields.Many2many("res.partner")
    contract_ids = fields.Many2many("contract.contract")

    name = fields.Char(string="Subject", required=True)
    category_id = fields.Many2one(
        comodel_name="helpdesk.ticket.category",
        string="Category",
    )
    team_id = fields.Many2one(
        comodel_name="helpdesk.ticket.team",
        string="Team",
        index=True,
    )
    user_ids = fields.Many2many(
        comodel_name="res.users", related="team_id.user_ids", string="Users"
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned user",
        index=True,
        domain="[('id', 'in', user_ids)]",
    )
    tag_ids = fields.Many2many(comodel_name="helpdesk.ticket.tag", string="Tags")
    priority = fields.Selection(
        selection=[
            ("0", "Low"),
            ("1", "Medium"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        default="1",
    )
    description = fields.Html(required=True, sanitize_style=True)

    def button_create(self):
        ticket_params = {
            "name": self.name,
            "category_id": self.category_id.id,
            "team_id": self.team_id.id,
            "user_id": self.user_id.id,
            "tag_ids": [(6, 0, self.tag_ids.ids)],
            "priority": self.priority,
            "description": self.description,
        }

        if self.contract_ids:
            for contract in self.contract_ids:
                params = ticket_params.copy()
                partner = contract.partner_id
                params.update(
                    {
                        "contract_id": contract.id,
                        "partner_id": partner.id,
                        "partner_name": partner.name,
                        "partner_email": partner.email,
                    }
                )
                self.env["helpdesk.ticket"].create(params)
        else:
            for partner in self.res_partner_ids:
                params = ticket_params.copy()
                params.update(
                    {
                        "partner_id": partner.id,
                        "partner_name": partner.name,
                        "partner_email": partner.email,
                    }
                )
                self.env["helpdesk.ticket"].create(params)

        return True

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_model = self.env.context["active_model"]
        if active_model == "res.partner":
            defaults["res_partner_ids"] = self.env.context["active_ids"]
        elif active_model == "contract.contract":
            defaults["contract_ids"] = self.env.context["active_ids"]
        return defaults
