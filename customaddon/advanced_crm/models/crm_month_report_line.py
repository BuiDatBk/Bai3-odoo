from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'crm.month.report.line'

    sales_team_id = fields.Many2one('crm.team')
    actual_revenue = fields.Float(string="Actual Revenue")
    diff_actual_target = fields.Float()

