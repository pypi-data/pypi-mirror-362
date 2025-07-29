from odoo import fields, models


class HelpdeskTicketTeam(models.Model):
    _inherit = "helpdesk.ticket.team"

    code = fields.Char(string="code")
