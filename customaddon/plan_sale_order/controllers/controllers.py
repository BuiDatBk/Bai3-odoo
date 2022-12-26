# -*- coding: utf-8 -*-
# from odoo import http


# class Customaddon/planSaleOrder(http.Controller):
#     @http.route('/customaddon/plan_sale_order/customaddon/plan_sale_order', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customaddon/plan_sale_order/customaddon/plan_sale_order/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customaddon/plan_sale_order.listing', {
#             'root': '/customaddon/plan_sale_order/customaddon/plan_sale_order',
#             'objects': http.request.env['customaddon/plan_sale_order.customaddon/plan_sale_order'].search([]),
#         })

#     @http.route('/customaddon/plan_sale_order/customaddon/plan_sale_order/objects/<model("customaddon/plan_sale_order.customaddon/plan_sale_order"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customaddon/plan_sale_order.object', {
#             'object': obj
#         })
