from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from odoo.addons.crm.models import crm_stage


class ModelName(models.TransientModel):
    _inherit = "crm.lead.lost"

    # def action_lost_reason_apply(self):
    #     for rec in self:
    #         if rec.priority == crm_stage.AVAILABLE_PRIORITIES[3][0]:
    #             # flag = self.pool.get('res.users').has_group(cr, uid, 'advanced_crm.group_sales_manager')
    #             flag = self.env['res.users'].has_group('advanced_crm.group_sales_manager')
    #             if flag:
    #                 super().action_lost_reason_apply()
    #             else:
    #                 raise UserError(_('Sales Manager?'))
    #         else:
    #             super().action_lost_reason_apply()
