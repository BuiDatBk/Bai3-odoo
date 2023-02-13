from odoo import fields, models, api
# from . import crm_stage
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from odoo.addons.crm.models import crm_stage


class ModelName(models.Model):
    _inherit = "crm.lead"

    min_revenue = fields.Float(string='Doanh thu tối thiểu\n(Trước VAT)')
    readonly_revenue = fields.Boolean(compute="compute_readonly_revenue")
    correct_sales_team = fields.Integer(compute="compute_correct_sales_team", store=True)
    is_sale_person = fields.Boolean(compute="compute_is_sale_person")
    is_team_lead = fields.Boolean(compute="compute_is_team_lead")
    report_id = fields.Many2one("target.assessment.report")


    @api.depends('team_id')
    def compute_correct_sales_team(self):
        self.correct_sales_team = self.team_id.id


    def compute_readonly_revenue(self):
        for rec in self:
            rec.readonly_revenue = rec.quotation_count > 0

    @api.constrains('min_revenue')
    def _check_positive_revenue(self):
        if any(rec.min_revenue <= 0 for rec in self):
            raise ValidationError(_('You can not enter negative money.'))

    def action_set_lost(self, **kwargs):
        for rec in self:
            if rec.priority == crm_stage.AVAILABLE_PRIORITIES[3][0]:
                # flag = self.pool.get('res.users').has_group(cr, uid, 'advanced_crm.group_sales_manager')
                flag = self.env['res.users'].has_group('advanced_crm.group_sales_manager')
                if flag:
                    super().action_set_lost()
                else:
                    raise UserError(_('Sales Manager?'))
            else:
                super().action_set_lost()

    def compute_is_sale_person(self):
        for rec in self:
            rec.is_sale_person = rec.user_id == self.env.user or rec.create_uid == self.env.user

    def compute_is_team_lead(self):
        for rec in self:
            if rec.user_id.crm_team_ids:
                rec.is_team_lead = self.env.user in rec.user_id.crm_team_ids.mapped("user_id")
            else:
                rec.is_team_lead = False

    @api.constrains('user_id')
    def _check_role(self):
        for rec in self:
            flag = self.env['res.users'].has_group('advanced_crm.group_sales_manager')
            match = self.env.user in rec.user_id.crm_team_ids.mapped("crm_team_member_ids.user_id")
            if rec.user_id != self.env.user and flag == False and match == False:
                # TODO
                raise ValidationError(_('You can only add yourself or your sales team members.'))
