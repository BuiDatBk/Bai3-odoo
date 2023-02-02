from odoo import fields, models, api


class ModelName(models.TransientModel):
    _name = 'report.two'

    team = fields.Many2one("crm.team", string="Sales Team")
    actual_revenue = fields.Float(string="Actual Revenue")
    revenue_target = fields.Float(string="Revenue Target")