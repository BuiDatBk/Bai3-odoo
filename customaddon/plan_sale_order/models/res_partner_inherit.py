from odoo import fields, models, api


class ResPartnerInderit(models.Model):
    _inherit = 'res.partner'

    approval_id = fields.Many2one('approval')
