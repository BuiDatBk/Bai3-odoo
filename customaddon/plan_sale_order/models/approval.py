from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'approval'

    approver = fields.Many2one('res.users', String="Approver", required=True)
    status_approval = fields.Selection([
        ('draft', 'Wait Send'),
        ('approved', 'Approved'),
        ('not_approve', 'Not Approved Yet'),
        ('refused', 'Refused'),
    ], default='draft')
    plan_sale_id = fields.Many2one('plan.sale.order')
    btn_visible = fields.Boolean(string='Visible', compute='visible')

    def visible(self):
        for rec in self:
            if rec.status_approval == 'not_approve':
                rec.btn_visible = rec.approver == self.env.user
            else:
                rec.btn_visible = False

    def action_approve(self):
        for rec in self:
            rec.status_approval = 'approved'

    def action_refuse(self):
        for rec in self:
            rec.status_approval = 'refused'


