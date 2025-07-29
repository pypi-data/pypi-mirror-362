from odoo import fields, models


class HelpdeskTicketTag(models.Model):
    _inherit = "helpdesk.ticket.tag"

    code = fields.Char(string="code")
