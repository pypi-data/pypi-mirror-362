# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields
from odoo.tests import common, tagged


@tagged("post_install", "helpdesk_automove")
class TestHelpdeskAutoMove(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.ticket = self.env["helpdesk.ticket"].create(
            {"name": "Test Ticket", "description": "This is a test ticket."}
        )
        self.stage1 = self.env["helpdesk.ticket.stage"].create(
            {"name": "Stage 1", "sequence": 1}
        )
        self.stage2 = self.env["helpdesk.ticket.stage"].create(
            {"name": "Stage 2", "sequence": 2}
        )

    def test_automove(self):
        self.stage1.has_automove = True
        self.stage1.timeout = 0
        self.stage1.to_stage_id = self.stage2
        self.ticket.stage_id = self.stage1
        self.ticket.last_stage_update = fields.Datetime.now()
        self.env["helpdesk.ticket.stage"].cron_automove()
        self.assertEqual(
            self.ticket.stage_id,
            self.stage2,
            "Ticket should have been moved to stage 2",
        )

    def test_automove_not_activate(self):
        self.stage1.has_automove = False
        self.stage1.timeout = 0
        self.stage1.to_stage_id = self.stage2
        self.ticket.stage_id = self.stage1
        self.ticket.last_stage_update = fields.Datetime.now()
        self.env["helpdesk.ticket.stage"].cron_automove()
        self.assertEqual(
            self.ticket.stage_id,
            self.stage1,
            "Ticket should not have been moved",
        )
