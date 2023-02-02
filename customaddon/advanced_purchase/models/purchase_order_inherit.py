from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
import datetime


class PurchaseOrderInherit(models.Model):
    _inherit = ['purchase.order']

    department = fields.Many2one('hr.department', string="Phòng ban")
    order_creation_limit_id = fields.Many2one("order.creation.limit")
    department_name = fields.Text(string="Department Name", compute="compute_department_name")
    department_limit = fields.Text(string="Hạn mức chi tiêu/ tháng", compute="compute_department_limit")

    def compute_department_name(self):
        for rec in self:
            rec.department_name = rec.department.name

    def compute_department_limit(self):
        for rec in self:
            rec.department_limit = rec.department.spending_limit_a_month

    def button_confirm(self):
        for rec in self:
            for line in self.env['order.creation.limit'].search([])[0].order_creation_limit_ids:
                if self.env.user == line.employee and rec.amount_total > line.limit:
                    todos = [{
                        'res_id': rec.id,
                        'res_model_id': rec.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
                        'user_id': kt.id,
                        'summary': 'can confirm',
                        'note': 'Can nhan vien ke toan confirm',
                        'activity_type_id': 4,
                        'date_deadline': datetime.date.today(),
                    } for kt in rec.env.ref('advanced_purchase.accountant').users]

                    for todo in todos:
                        rec.env['mail.activity'].sudo().create(todo)
                        rec.env.cr.commit()
                    raise UserError(
                        _('you have bought more than the allowed limit. Please wait for the accountant to confirm'))

                else:
                    super().button_confirm()

    # def create_activity(self):
    #     self.ensure_one()
    #     todos = [{
    #         'res_id': self.id,
    #         'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
    #         'user_id': kt.id,
    #         'summary': 'can confirm',
    #         'note': 'Can nhan vien ke toan confirm',
    #         'activity_type_id': 4,
    #         'date_deadline': datetime.date.today(),
    #     } for kt in self.env.ref('advanced_purchase.accountant').users]
    #
    #     for todo in todos:
    #         self.env['mail.activity'].sudo().create(todo)
    #         self.env.cr.commit()
