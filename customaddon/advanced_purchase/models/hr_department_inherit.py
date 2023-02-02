from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

class HrDepartmentInherit(models.Model):
    _inherit = "hr.department"

    spending_limit_a_month = fields.Float(string="Hạn mức chi tiêu / tháng")
    purchase_ids = fields.One2many('purchase.order', 'department', string="Purchase Orders")
    actual_spending = fields.Float(string="Chi tiêu thực tế", compute="compute_actual_spending")
    report_id = fields.Many2one('report.spending')

    cost = fields.Float(string="Cost", default=0.0)

    def compute_actual_spending(self):
        for rec in self:
            total = 0.0
            for line in rec.purchase_ids:
                total += line.amount_total
            rec.actual_spending = total

    @api.constrains('spending_limit_a_month')
    def constrains_spending_limit_a_month(self):
        if any(self.spending_limit_a_month <= 0 for rec in self):
            raise ValidationError(_('You can not enter negative money.'))