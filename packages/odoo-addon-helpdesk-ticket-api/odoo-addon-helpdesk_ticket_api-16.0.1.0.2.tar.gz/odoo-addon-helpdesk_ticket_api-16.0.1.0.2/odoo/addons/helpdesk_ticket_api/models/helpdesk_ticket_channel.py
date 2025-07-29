from odoo import fields, models


class HelpdeskTicketChannel(models.Model):
    _inherit = "helpdesk.ticket.channel"

    code = fields.Char(string="code")
