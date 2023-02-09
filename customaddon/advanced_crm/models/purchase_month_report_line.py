from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'purchase.month.report.line'

    department_id = fields.Many2one('hr.department')
    actual_spending = fields.Float(string="Actual Spending")
    diff_actual_limit = fields.Float()

