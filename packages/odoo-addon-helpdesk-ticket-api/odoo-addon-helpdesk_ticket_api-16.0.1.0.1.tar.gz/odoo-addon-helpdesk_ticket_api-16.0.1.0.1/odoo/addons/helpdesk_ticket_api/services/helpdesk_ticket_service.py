from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from odoo.exceptions import ValidationError
from odoo import _

from . import schemas

import logging

_logger = logging.getLogger(__name__)


class TicketServiceAPI(Component):
    _name = "helpdesk.ticket.api"
    _inherit = "base.rest.service"
    _usage = "ticket"
    _collection = "api_common_base.services"
    _description = """
        Helpdesk Ticket API
        Access to search or create helpdesk tickets
    """

    @restapi.method(
        [(["/"], "POST")],
        input_param=restapi.CerberusValidator(schemas.S_TICKET_CREATE),
        output_param=restapi.CerberusValidator(schemas.S_TICKET_RETURN_CREATE),
    )
    def create_ticket(self, **params):
        attachments = params.pop("attachments", [])

        ticket_params = self._prepare_create(params)
        ticket = self.env["helpdesk.ticket"].create(ticket_params)
        for attachment in attachments:
            self._add_attachment(ticket, attachment)

        result = {"id": ticket.id}
        _logger.debug(result)

        return result

    @restapi.method(
        [(["/getlist"], "GET")],
        input_param=restapi.CerberusValidator(schemas.S_TICKET_LIST),
        output_param=restapi.CerberusValidator(schemas.S_TICKET_RETURN_LIST),
    )
    def get_ticket_list(self, **params):
        domain = []
        errors = []
        if params.get("partner_ref"):
            partner = self._search_partner(params)
            domain.append(("partner_id", "=", partner.id))
        elif params.get("contract_code"):
            contract = self.env["contract.contract"].search(
                [("code", "=", params["contract_code"])], limit=1
            )
            if contract:
                domain.append(("contract_id", "=", contract.id))
            else:
                errors.append(("contract", params["contract_code"]))

        if params.get("stage"):
            stage = self.env["helpdesk.ticket.stage"].search(
                [("code", "=", params["stage"])], limit=1
            )
            if stage:
                domain.append(("stage_id", "=", stage.id))
            else:
                errors.append(("stage", params["stage"]))

        if errors:
            self._process_errors(errors)

        tickets = self.env["helpdesk.ticket"].search(domain)
        result = {
            "tickets": [self._to_dict(ticket) for ticket in tickets],
        }
        _logger.debug(result)

        return result

    def _prepare_create(self, params):
        contract = None
        partner = None
        category = None
        tag_ids = None
        team = None

        if params.get("contract_code"):
            contract = self.env["contract.contract"].search(
                [("code", "=", params["contract_code"])]
            )
        else:
            partner = self._search_partner(params)

        errors = []
        if params.get("category"):
            category = self.env["helpdesk.ticket.category"].search(
                [("code", "=", params["category"])]
            )
            if not category:
                errors.append(("category", params["category"]))

        if params.get("channel"):
            channel = self.env["helpdesk.ticket.channel"].search(
                [("code", "=", params["channel"])]
            )
            if not channel:
                errors.append(("channel", params["channel"]))
        else:
            channel = self.env.ref("helpdesk_mgmt.helpdesk_ticket_channel_email")

        if params.get("stage"):
            stage = self.env["helpdesk.ticket.stage"].search(
                [("code", "=", params["stage"])]
            )
            if not stage:
                errors.append(("stage", params["stage"]))
        else:
            stage = self.env.ref("helpdesk_mgmt.helpdesk_ticket_stage_new")

        if params.get("tags"):
            tag_code_list = params["tags"].split(",")
            tag_ids = self.env["helpdesk.ticket.tag"].search(
                [("code", "in", tag_code_list)]
            )
            if not tag_ids:
                errors.append(("tag_ids", params["tags"]))

        if params.get("team"):
            team = self.env["helpdesk.ticket.team"].search(
                [("code", "=", params["team"])]
            )
            if not team:
                errors.append(("team", params["team"]))

        if errors:
            self._process_errors(errors)

        ticket_params = {
            "name": params["summary"],
            "description": params["description"],
            "category_id": category.id if category else None,
            "channel_id": channel.id,
            "partner_id": partner.id if partner else None,
            "partner_email": partner.email if partner else params.get("partner_email"),
            "priority": params.get("priority"),
            "stage_id": stage.id,
            "tag_ids": [(6, 0, tag_ids.ids)] if tag_ids else None,
            "team_id": team.id if team else None,
            "user_id": self.env.user.id,
            "contract_id": contract.id if contract else None,
        }
        return ticket_params

    def _search_partner(self, params):
        """
        Search partner in DB by incoming API call partner fields
        Returns: res.partner instance
        Email match either returns a partner without parent_id or no partner
        """
        partner_domain = []

        if params.get("partner_email"):
            partner_domain.append(("email", "=", params["partner_email"]))
            partners_result = self.env["res.partner"].search(partner_domain)
            partner = partners_result.filtered(lambda p: not p.parent_id)

            if partner and len(partner) == 1:
                return partner
            elif (
                len(partners_result) == 1
                or len(set(partners_result.mapped("parent_id"))) == 1
            ):
                return partners_result[0].parent_id
            return False

        if params.get("partner_ref"):
            partner_domain.append(("ref", "=", params["partner_ref"]))
            search_param = ("ref", params["partner_ref"])
        elif params.get("partner_vat"):
            partner_domain.append(("vat", "=", params["partner_vat"]))
            search_param = ("vat", params["partner_vat"])

        partner = self.env["res.partner"].search(partner_domain)
        if not partner:
            raise ValidationError(
                _("Partner with {}: {} not found").format(
                    search_param[0], search_param[1]
                )
            )

        return partner

    def _add_attachment(self, new_ticket, attachment):
        attachment_data = {
            "name": attachment["filename"],
            "type": "binary",
            "datas": attachment["content"],
            "res_model": "helpdesk.ticket",
            "res_id": new_ticket.id,
            "mimetype": attachment["mimetype"],
        }
        self.env["ir.attachment"].create(attachment_data)
        return

    def _process_errors(self, errors):
        error_message = _("Some params could not be found in our system:\n")
        for field, value in errors:
            error_message += f"{field}: {value}, "
        error_message = error_message[:-2]  # Delete last ',' and space
        raise ValidationError(error_message)

    def _to_dict(self, ticket):
        ticket.ensure_one()
        return {
            "id": ticket.id,
            "name": ticket.name,
            "description": ticket.description,
            "date_open": ticket.create_date.strftime("%Y-%m-%d %H:%M"),
            "date_updated": ticket.write_date.strftime("%Y-%m-%d %H:%M"),
            "priority": ticket.priority or "",
            "stage": ticket.stage_id.name if ticket.stage_id else "",
            "assigned_user": ticket.user_id.name if ticket.user_id else "",
            "channel": ticket.channel_id.name if ticket.channel_id else "",
            "tags": ticket.tag_ids.mapped("name") if ticket.tag_ids else [],
        }
