from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    plan_sale = fields.One2many('plan.sale.order', 'quotation', string='Plan Sale Order')

    name_plan = fields.Many2one('plan.sale.order', compute='compute_name_plan')

    def action_plan_sale_order(self):

        self.ensure_one()
        if self.name_plan:
            return {
                'res_model': 'plan.sale.order',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'target': 'current',
                'domain': [('name', '=', self.name_plan.name)],
            }
        else:
            return {
                'res_model': 'plan.sale.order',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': self.env.ref("plan_sale_order.plan_sale_order_form_view").id,
                'target': 'new',
                'context': {
                    'default_quotation': self.id,
                }
            }

    @api.depends('plan_sale')
    def compute_name_plan(self):
        for rec in self:
            if rec.plan_sale:
                rec.name_plan = rec.plan_sale[0]
            else:
                rec.name_plan = False

    def action_confirm(self):
        # check dieu kien truoc khi xac nhan
        if not self.plan_sale:
            raise UserError(_('No plan.'))
        else:
            if self.plan_sale.state == 'refuse':
                raise UserError(_('%s plan is refused') % (self.plan_sale.name))
            elif self.plan_sale.state == 'sent':
                raise UserError(_('Not yet approved %s plan.') % (self.plan_sale.name))
            elif self.plan_sale.state == 'draft':
                raise UserError(_('%s has not been sent.') % (self.plan_sale.name))
            else:
                return super().action_confirm()
