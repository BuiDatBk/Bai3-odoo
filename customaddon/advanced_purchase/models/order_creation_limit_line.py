from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

class OrderCreationLimitLine(models.Model):
    _name = 'order.creation.limit.line'

    employee = fields.Many2one("res.users", string="Nhân viên", required=True)
    limit = fields.Float(string="Hạn mức/ đơn")
    limit_id = fields.Many2many("order.creation.limit")

    @api.constrains('limit')
    def constrains_limit(self):
        if any(self.limit <= 0 for rec in self):
            raise ValidationError(_('You can not enter negative money.'))