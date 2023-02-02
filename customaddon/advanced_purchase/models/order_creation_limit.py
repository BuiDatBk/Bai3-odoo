from odoo import fields, models, api


class OrderCreationLimit(models.Model):
    _name = 'order.creation.limit'

    order_creation_limit_ids = fields.Many2many('order.creation.limit.line', string="Order Creation Limit")
    purchase_id = fields.One2many("purchase.order", "order_creation_limit_id")

    @api.model
    def action_order_creation_limit(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'view_id': self.env.ref("advanced_purchase.order_creation_limit_form_view").id,
            'target': 'current',
            'res_id': self.search([])[0].id,
        }