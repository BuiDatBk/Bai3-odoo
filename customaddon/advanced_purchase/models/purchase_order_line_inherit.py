from odoo import fields, models, api
import random
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

class PurchaseOrderLineInherit(models.Model):
    _inherit = "purchase.order.line"

    propose_supplier = fields.Many2one("res.partner", string="Nhà cung cấp đề xuất", compute="compute_propose_supplier")

    # @api.depends('product_id.seller_ids.price', 'product_id.seller_ids.delay')
    @api.onchange('price_unit')
    def compute_propose_supplier(self):
        for rec in self:
            if rec.product_id.seller_ids:
                price = rec.product_id.seller_ids[0].price
                lead_time = rec.product_id.seller_ids[0].delay
                id = 0
                id_true = 0
                id_delay = 0
                list_seller_same_delay = []
                for line in rec.product_id.seller_ids:
                    if line.price < price:
                        price = line.price
                        id_true = id
                        id += 1
                    elif line.price == price and line.delay < lead_time:
                        lead_time = line.delay
                        id_true = id
                        id += 1
                    else:
                        id += 1

                # random a seller
                delay_min = rec.product_id.seller_ids[id_true].delay
                for line in rec.product_id.seller_ids:
                    if line.delay == delay_min and line.price == price:
                        list_seller_same_delay.append(id_delay)
                        id_delay += 1
                    else:
                        id_delay += 1

                if len(list_seller_same_delay) >= 2:
                    rec.propose_supplier = rec.product_id.seller_ids[random.choice(list_seller_same_delay)].name
                else:
                    rec.propose_supplier = rec.product_id.seller_ids[id_true].name
            else:
                raise UserError(_('list empty'))

        # sellers = rec.product_id.seller_ids.sort(key=rec.product_id.seller_ids.price)
        # price = sellers[0].price
        # lead_time = sellers[0].delay
        # id = 0
        # for seller in sellers:
        #     if seller.price == price and seller.delay < lead_time:
        #         lead_time = seller.delay
        #         id += 1
        # rec.propose_supplier = sellers[id].name
