# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common, tagged
from odoo.exceptions import UserError


@tagged("post_install", "helpdesk_ticket_subtags")
class TestHelpdeskSubtags(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.ticket = self.env["helpdesk.ticket"].create(
            {"name": "Test Ticket", "description": "This is a test ticket."}
        )
        self.tag1 = self.env["helpdesk.ticket.tag"].create({"name": "Tag 1"})
        self.tag2 = self.env["helpdesk.ticket.tag"].create(
            {"name": "Tag 2", "parent_id": self.tag1.id}
        )

    def test_subtags(self):
        self.ticket.tag_ids = [(6, False, [self.tag2.id])]
        self.assertEqual(
            self.ticket.tag_ids,
            self.tag2,
            "Ticket should have tag 2 as subtag",
        )
        self.assertEqual(
            self.tag2.parent_id,
            self.tag1,
            "Tag 2 should have tag 1 as main tag",
        )

    def test_circular_reference(self):
        with self.assertRaises(UserError):
            self.tag1.write({"parent_id": self.tag2.id})
