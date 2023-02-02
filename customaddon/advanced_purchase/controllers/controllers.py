# -*- coding: utf-8 -*-
# from odoo import http


# class Customaddon/advancedPurchase(http.Controller):
#     @http.route('/customaddon/advanced_purchase/customaddon/advanced_purchase', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customaddon/advanced_purchase/customaddon/advanced_purchase/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customaddon/advanced_purchase.listing', {
#             'root': '/customaddon/advanced_purchase/customaddon/advanced_purchase',
#             'objects': http.request.env['customaddon/advanced_purchase.customaddon/advanced_purchase'].search([]),
#         })

#     @http.route('/customaddon/advanced_purchase/customaddon/advanced_purchase/objects/<model("customaddon/advanced_purchase.customaddon/advanced_purchase"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customaddon/advanced_purchase.object', {
#             'object': obj
#         })
