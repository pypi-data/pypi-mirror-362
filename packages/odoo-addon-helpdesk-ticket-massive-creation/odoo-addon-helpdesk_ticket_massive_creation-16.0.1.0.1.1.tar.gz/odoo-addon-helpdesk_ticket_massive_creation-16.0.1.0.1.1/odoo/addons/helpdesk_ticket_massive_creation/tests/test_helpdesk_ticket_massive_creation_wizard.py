from odoo.tests import common, tagged


@tagged("post_install", "-at_install", "helpdesk_ticket_massive_creation")
class TestHelpdeskTicketMassiveCreationWizard(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.Ticket = self.env["helpdesk.ticket"]
        self.Contract = self.env["contract.contract"]
        self.partner_1 = self.env.ref("base.res_partner_1")
        self.partner_2 = self.env.ref("base.res_partner_2")

    def test_massive_helpdesk_ticket_create_partner(self):
        partner_ids = [self.partner_1.id, self.partner_2.id]
        ticket_domain = [
            ("partner_id", "in", partner_ids),
            ("name", "=", "Massive incident"),
        ]
        partners_tickets = self.Ticket.search(ticket_domain)

        self.assertFalse(partners_tickets)

        wizard = (
            self.env["helpdesk.ticket.massive.creation.wizard"]
            .with_context(active_ids=partner_ids, active_model="res.partner")
            .create(
                {
                    "name": "Massive incident",
                    "category_id": self.env.ref("helpdesk_mgmt.helpdesk_category_3").id,
                    "team_id": self.env.ref("helpdesk_mgmt.helpdesk_team_1").id,
                    "user_id": self.env.ref("base.user_demo").id,
                    "tag_ids": [(4, self.env.ref("helpdesk_mgmt.helpdesk_tag_1").id)],
                    "priority": "2",
                    "description": "Massive issue going on",
                }
            )
        )
        wizard.button_create()

        partners_tickets = self.Ticket.search(ticket_domain)

        self.assertTrue(partners_tickets)
        self.assertEqual(len(partners_tickets), 2)

        ticket = partners_tickets.filtered(lambda t: t.partner_id == self.partner_1)
        self.assertEqual(ticket.name, wizard.name)
        self.assertEqual(ticket.category_id, wizard.category_id)
        self.assertEqual(ticket.team_id, wizard.team_id)
        self.assertEqual(ticket.tag_ids, wizard.tag_ids)
        self.assertEqual(ticket.priority, wizard.priority)
        self.assertEqual(ticket.description, wizard.description)
        self.assertEqual(ticket.partner_name, self.partner_1.name)
        self.assertEqual(ticket.partner_email, self.partner_1.email)

    def test_massive_helpdesk_ticket_create_contract(self):
        contract_1 = self.Contract.create(
            {"name": "Contract TEST 1", "partner_id": self.partner_1.id}
        )
        contract_2 = self.Contract.create(
            {"name": "Contract TEST 2", "partner_id": self.partner_2.id}
        )

        contract_ids = [contract_1.id, contract_2.id]
        ticket_domain = [
            ("contract_id", "in", contract_ids),
            ("name", "=", "Massive incident"),
        ]
        contract_tickets = self.Ticket.search(ticket_domain)

        self.assertFalse(contract_tickets)

        wizard = (
            self.env["helpdesk.ticket.massive.creation.wizard"]
            .with_context(active_ids=contract_ids, active_model="contract.contract")
            .create(
                {
                    "name": "Massive incident",
                    "category_id": self.env.ref("helpdesk_mgmt.helpdesk_category_3").id,
                    "user_id": self.env.ref("base.user_demo").id,
                    "description": "Massive contract issue going on",
                }
            )
        )
        wizard.button_create()

        contract_tickets = self.Ticket.search(ticket_domain)

        self.assertTrue(contract_tickets)
        self.assertEqual(len(contract_tickets), 2)
        self.assertIn(contract_1, contract_tickets.mapped("contract_id"))
        self.assertIn(contract_2, contract_tickets.mapped("contract_id"))

        ticket_1 = contract_tickets[0]
        contract = ticket_1.contract_id
        self.assertEqual(ticket_1.partner_name, contract.partner_id.name)
        self.assertEqual(ticket_1.partner_email, contract.partner_id.email)

        ticket_2 = contract_tickets[1]
        contract = ticket_2.contract_id
        self.assertEqual(ticket_2.contract_id, contract)
        self.assertEqual(ticket_2.partner_name, contract.partner_id.name)
        self.assertEqual(ticket_2.partner_email, contract.partner_id.email)
