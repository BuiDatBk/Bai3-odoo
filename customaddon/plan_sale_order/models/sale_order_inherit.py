from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    plan_sale = fields.One2many('plan.sale.order', 'quotation', string='Plan Sale Order')

    name_plan = fields.Many2one('plan.sale.order', compute='compute_name_plan')

    def action_plan_sale_order(self):
        self.ensure_one()
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
        for rec in self:
            if rec.plan_sale:
                if rec.plan_sale.state == 'refuse':
                    raise UserError(_('%s plan is refused') % (rec.plan_sale.name))
                elif rec.plan_sale.state == 'sent':
                    raise UserError(_('Not yet approved %s plan.') % (rec.plan_sale.name))
                elif rec.plan_sale.state == 'draft':
                    raise UserError(_('%s has not been sent.') % (rec.plan_sale.name))
                else:
                    super().action_confirm()
            else:
                raise UserError(_('No plan.'))
