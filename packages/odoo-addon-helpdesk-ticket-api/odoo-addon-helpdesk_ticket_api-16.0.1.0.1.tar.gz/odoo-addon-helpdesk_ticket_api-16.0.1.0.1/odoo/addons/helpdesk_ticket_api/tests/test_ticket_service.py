import base64
import json
import odoo
import requests
from pathlib import Path
from odoo.addons.api_common_base.tests.common_service import APICommonBaseRestCase
from odoo.tests.common import tagged


@tagged("post_install", "-at_install", "helpdesk_ticket_api")
class TestTicketService(APICommonBaseRestCase):
    def setUp(self):
        super().setUp()
        self.session = requests.Session()
        self.Ticket = self.env["helpdesk.ticket"]
        self.partner = self.env.ref("base.res_partner_2")
        self.partner.ref = "82828"
        self.team = self.env.ref("helpdesk_mgmt.helpdesk_team_1")
        self.category = self.env.ref("helpdesk_mgmt.helpdesk_category_1")
        self.tag_1 = self.env.ref("helpdesk_mgmt.helpdesk_tag_1")
        self.tag_2 = self.env.ref("helpdesk_mgmt.helpdesk_tag_2")
        self.contract = self.env["contract.contract"].create(
            {"name": "Contract TEST", "partner_id": self.partner.id, "code": "E728S8S"}
        )
        self.url = "/api/ticket"
        self.ticket_data = {
            "summary": "New Ticket",
            "description": "brand new one",
            "partner_ref": self.partner.ref,
            "team": self.team.code,
            "category": self.category.code,
            "priority": "0",  # Low
            "tags": "{},{}".format(self.tag_1.code, self.tag_2.code),
        }

    def test_create_ticket_ok(self):
        """
        Test Helpdesk Ticket creation by API and
        the parameters correspondance with the created ticket.
        """

        default_channel = self.env.ref("helpdesk_mgmt.helpdesk_ticket_channel_email")
        default_stage = self.env.ref("helpdesk_mgmt.helpdesk_ticket_stage_new")
        default_user = self.env.ref("base.user_admin")

        response = self.http_post(self.url, data=self.ticket_data)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        ticket = self.Ticket.browse(content["id"])

        self.assertTrue(ticket)
        self.assertEqual(ticket.name, self.ticket_data["summary"])
        self.assertIn(self.ticket_data["description"], ticket.description)
        self.assertEqual(ticket.partner_id, self.partner)
        self.assertEqual(ticket.team_id, self.team)
        self.assertEqual(ticket.category_id, self.category)
        self.assertEqual(ticket.priority, self.ticket_data["priority"])
        self.assertEqual(len(ticket.tag_ids), 2)
        self.assertIn(self.tag_1, ticket.tag_ids)
        self.assertIn(self.tag_2, ticket.tag_ids)
        self.assertEqual(ticket.channel_id, default_channel)
        self.assertEqual(ticket.stage_id, default_stage)
        self.assertEqual(ticket.user_id, default_user)

    def test_create_ticket_with_partner_email_single_match(self):
        """
        Test Helpdesk Ticket creation by API
        searching partner by email with single partner match.
        """
        ticket_data = self.ticket_data.copy()
        ticket_data.pop("partner_ref")
        ticket_data["partner_email"] = self.partner.email

        response = self.http_post(self.url, data=ticket_data)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        ticket = self.Ticket.browse(content["id"])

        self.assertEqual(ticket.partner_id, self.partner)

    def test_create_ticket_with_partner_email_match_also_with_child(self):
        """
        Test Helpdesk Ticket creation by API
        searching partner by email if match is a child partner.
        """
        ticket_data = self.ticket_data.copy()
        ticket_data.pop("partner_ref")
        ticket_data["partner_email"] = self.partner.email

        self.env["res.partner"].create(
            {
                "name": "Child Partner",
                "email": self.partner.email,
                "parent_id": self.partner.id,
            }
        )

        response = self.http_post(self.url, data=ticket_data)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        ticket = self.Ticket.browse(content["id"])

        self.assertEqual(ticket.partner_id, self.partner)

    def test_create_ticket_with_partner_email_match_only_with_child(self):
        """
        Test Helpdesk Ticket creation by API
        searching partner by email if one match is child
        and the other is a parent.
        """
        ticket_data = self.ticket_data.copy()
        ticket_data.pop("partner_ref")
        ticket_data["partner_email"] = self.partner.email

        self.env["res.partner"].create(
            {
                "name": "Child Partner",
                "email": self.partner.email,
                "parent_id": self.partner.id,
            }
        )

        response = self.http_post(self.url, data=ticket_data)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        ticket = self.Ticket.browse(content["id"])

        self.assertEqual(ticket.partner_id, self.partner)

    def test_create_ticket_with_partner_email_multiple_childs_found(self):
        """
        Test Helpdesk Ticket creation by API
        searching partner by email if no parent is found and
        multiple childs are found with diferent parents.
        """
        ticket_data = self.ticket_data.copy()
        ticket_data.pop("partner_ref")
        ticket_data["partner_email"] = "random@email.coop"

        self.env["res.partner"].create(
            {
                "name": "Child Partner",
                "email": ticket_data["partner_email"],
                "parent_id": self.partner.id,
            }
        )

        self.env["res.partner"].create(
            {
                "name": "Child Partner 2",
                "email": ticket_data["partner_email"],
                "parent_id": self.env.ref("base.res_partner_3").id,
            }
        )
        response = self.http_post(self.url, data=ticket_data)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        ticket = self.Ticket.browse(content["id"])

        self.assertFalse(ticket.partner_id)
        self.assertEqual(ticket.partner_email, ticket_data["partner_email"])

    def test_create_ticket_with_partner_email_multiple_found(self):
        """
        Test Helpdesk Ticket creation by API
        searching partner by email if no parent is found and
        multiple childs are found with diferent parents.
        """
        ticket_data = self.ticket_data.copy()
        ticket_data.pop("partner_ref")
        ticket_data["partner_email"] = self.partner.email

        self.env["res.partner"].create(
            {
                "name": "New Partner",
                "email": self.partner.email,
                "parent_id": "",
            }
        )

        response = self.http_post(self.url, data=ticket_data)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        ticket = self.Ticket.browse(content["id"])

        self.assertFalse(ticket.partner_id)
        self.assertEqual(ticket.partner_email, ticket_data["partner_email"])

    def test_create_ticket_with_partner_email_not_found(self):
        """
        Test Helpdesk Ticket creation by API
        searching partner by email.
        """
        ticket_data = self.ticket_data.copy()
        ticket_data.pop("partner_ref")
        ticket_data["partner_email"] = "random@email.coop"

        response = self.http_post(self.url, data=ticket_data)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        ticket = self.Ticket.browse(content["id"])

        self.assertFalse(ticket.partner_id)
        self.assertEqual(ticket.partner_email, ticket_data["partner_email"])

    def test_create_ticket_with_contract(self):
        """
        Test Helpdesk Ticket creation by API
        with a contract linked.
        """
        ticket_data = self.ticket_data.copy()
        ticket_data.pop("partner_ref")
        ticket_data["contract_code"] = self.contract.code

        response = self.http_post(self.url, data=ticket_data)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        ticket = self.Ticket.browse(content["id"])

        self.assertEqual(ticket.contract_id, self.contract)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_create_ticket_with_partner_not_found(self):
        """
        Test Helpdesk Ticket creation by API
        with an unknown VAT (non-existing partner).
        """
        ticket_data = self.ticket_data.copy()
        ticket_data.pop("partner_ref")
        ticket_data["partner_vat"] = "ESA820208S"

        response = self.http_post(self.url, data=ticket_data)
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 400)  # ValidationError
        error_msg = "Partner with {}: {} not found".format(
            "vat", ticket_data["partner_vat"]
        )
        self.assertIn(error_msg, content["description"])

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_create_ticket_bad_request(self):
        """
        Test Helpdesk Ticket creation by API
        with no partner no contract reference (required in its schema)
        """
        ticket_data = self.ticket_data.copy()
        ticket_data.pop("partner_ref")

        response = self.http_post(self.url, data=ticket_data)

        self.assertEqual(response.status_code, 400)  # BadRequest

    def test_create_ticket_with_attachments(self):
        """
        Test Helpdesk Ticket creation by API with files,
        that should be attached to ticket.
        """
        ticket_data = self.ticket_data.copy()

        module_path = Path(__file__).resolve().parents[1]
        file_name = "icon.png"
        file_relative_path = "static/description"
        file_path = module_path / file_relative_path / file_name
        file = open(file_path, "rb")
        file_content = base64.b64encode(file.read()).decode("utf-8")
        file_mimetype = "image/png"

        ticket_data["attachments"] = [
            {"filename": file_name, "content": file_content, "mimetype": file_mimetype}
        ]

        response = self.http_post(self.url, data=ticket_data)

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        ticket = self.Ticket.browse(content["id"])
        self.assertTrue(ticket)

        ticket_attachment = self.env["ir.attachment"].search(
            [
                ("res_model", "=", "helpdesk.ticket"),
                ("res_id", "=", ticket.id),
                ("name", "=", file_name),
                ("mimetype", "=", file_mimetype),
            ]
        )
        self.assertTrue(ticket_attachment)

    def test_getlist_ticket_ok(self):
        """
        Test Helpdesk Ticket API getlist by partner_ref.
        """
        url = self.url + "/getlist"
        stage_new = self.env.ref("helpdesk_mgmt.helpdesk_ticket_stage_new")
        params = {"partner_ref": self.partner.ref, "stage": stage_new.code}
        partner_tickets = self.Ticket.search(
            [("partner_id", "=", self.partner.id), ("stage_id", "=", stage_new.id)]
        )

        response = self.http_get(url, params=params)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content["tickets"]), len(partner_tickets))

        ticket_dct = content["tickets"][0]
        ticket = self.Ticket.browse(ticket_dct["id"])

        self.assertEqual(ticket_dct["name"], ticket.name)
        self.assertEqual(ticket_dct["description"], ticket.description)
        self.assertEqual(
            ticket_dct["date_open"],
            ticket.create_date.strftime("%Y-%m-%d %H:%M"),
        )
        self.assertEqual(
            ticket_dct["date_updated"],
            ticket.write_date.strftime("%Y-%m-%d %H:%M"),
        )
        self.assertEqual(ticket_dct["priority"], ticket.priority)
        self.assertEqual(ticket_dct["stage"], stage_new.name)
        self.assertEqual(ticket_dct["assigned_user"], ticket.user_id.name)
        self.assertEqual(ticket_dct["channel"], ticket.channel_id.name)
        self.assertEqual(ticket_dct["tags"], ticket.tag_ids.mapped("name"))

    def test_getlist_ticket_by_contract_code(self):
        """
        Test Helpdesk Ticket API getlist by partner_ref.
        """

        url = self.url + "/getlist"
        params = {"contract_code": self.contract.code}

        ticket = self.Ticket.create(
            {
                "name": "Ticket with contract",
                "description": "Ticket with contract",
                "contract_id": self.contract.id,
                "team_id": self.team.id,
                "category_id": self.category.id,
            }
        )

        response = self.http_get(url, params=params)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content["tickets"]), 1)
        ticket_dct = content["tickets"][0]
        self.assertEqual(ticket_dct["id"], ticket.id)
