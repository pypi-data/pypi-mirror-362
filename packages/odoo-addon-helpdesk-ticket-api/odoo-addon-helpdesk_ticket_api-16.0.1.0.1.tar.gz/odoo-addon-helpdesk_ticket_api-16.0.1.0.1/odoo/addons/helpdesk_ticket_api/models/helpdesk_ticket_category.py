from odoo import fields, models


class HelpdeskTicketCategory(models.Model):
    _inherit = "helpdesk.ticket.category"

    code = fields.Char(string="code")
