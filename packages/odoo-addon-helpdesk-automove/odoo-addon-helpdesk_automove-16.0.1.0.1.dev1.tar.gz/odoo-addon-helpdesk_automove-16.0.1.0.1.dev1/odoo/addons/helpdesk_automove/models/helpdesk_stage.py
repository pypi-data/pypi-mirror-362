from odoo import models, fields, api
import logging


class HelpdeskTicketStage(models.Model):
    _inherit = "helpdesk.ticket.stage"

    has_automove = fields.Boolean(string="Auto Move", default=False)
    timeout = fields.Integer(string="Timeout (days)", default=0)
    to_stage_id = fields.Many2one("helpdesk.ticket.stage", string="To Stage")

    # Use the field last_stage_update as reference for the timeout
    # (datetime.now() - last_stage_update > timeout)
    # We want to substract the present day from the last day the ticket was in the stage

    @api.model
    def cron_automove(self):
        _logger = logging.getLogger(__name__)
        _logger.info("Cron Auto move started")
        stages = self.env["helpdesk.ticket.stage"].search([("has_automove", "=", True)])
        for stage in stages:
            tickets = self.env["helpdesk.ticket"].search([("stage_id", "=", stage.id)])
            for ticket in tickets:
                if ticket.last_stage_update:
                    if (
                        fields.Datetime.now() - ticket.last_stage_update
                    ).days >= stage.timeout:
                        ticket.stage_id = stage.to_stage_id
                        _logger.info("Ticket %s automove" % ticket.id)
        _logger.info("Cron Automove ended")
