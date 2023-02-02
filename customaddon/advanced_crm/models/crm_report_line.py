from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'crm.report.line'

    sales_team = fields.Many2one('crm.team')
    opportunity_id = fields.Many2one('crm.lead')
    actual_revenue = fields.Float(string="Actual Revenue", compute="compute_actual_revenue")

