from odoo import fields, models, api


class ModelName(models.TransientModel):
    _name = 'report.one'

    opportunity = fields.Char(string="Opportunity")
    person = fields.Many2one("res.partner", string="Salesperson")
    team = fields.Many2one("crm.team", string="Sales Team")
    min = fields.Float(string="Minimum Revenue")
    sale_total = fields.Float(string="Doanh thu thực tế")

