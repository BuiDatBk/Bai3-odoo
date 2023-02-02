from odoo import fields, models, api


class ModelName(models.TransientModel):
    _name = 'report'

    department = fields.Many2one("hr.department")
    cost = fields.Float(string="Cost")
    spending_limit = fields.Float(string="Spending Limit")


