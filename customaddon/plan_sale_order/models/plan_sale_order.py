from odoo import fields, models, api


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Text(string='Plan Name', required=True)
    quotation = fields.Many2one('sale.order', string='Quotation', readonly=True)
    plan_information = fields.Text(string='Plan Information', required=True)
    approval_ids = fields.One2many('approval', 'plan_sale_id', string='Approval', auto_join=True)

    state = fields.Selection([
        ('draft', 'New'),
        ('sent', 'Waiting For Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft', compute='update_state')

    btn_visible_state = fields.Boolean(string='Visible', compute='visible')
    read_only = fields.Boolean(string='Add a Line', compute='is_readonly')

    def action_send_to_review(self):
        self.ensure_one()
        message_list = self.approval_ids.mapped("approver.partner_id.id")

        self.sudo().message_post(body='Business plan need approval',
                                 partner_ids=message_list,
                                 message_type='notification')
        for rec in self:
            rec.state = 'sent'
            for line in rec.approval_ids:
                line.status_approval = 'not_approve'

    @api.depends('approval_ids.status_approval')
    def update_state(self):
        for rec in self:
            draft = 0
            for line in rec.approval_ids:
                if line.status_approval == 'refused':
                    draft = 1
                    break
                elif line.status_approval == 'not_approve':
                    draft = 2
                elif line.status_approval == 'draft':
                    draft = 3
                    break
                else:
                    draft += 0
            if draft == 0:
                rec.state = 'approve'
            elif draft == 1:
                rec.state = 'refuse'
            elif draft == 3:
                rec.state = 'draft'
            else:
                rec.state = 'sent'

    @api.depends('state')
    def visible(self):
        for rec in self:
            if rec.state != 'draft' and rec.state != 'refuse' :
                rec.btn_visible_state = False
            else:
                rec.btn_visible_state = True

    @api.depends('state')
    def is_readonly(self):
        for rec in self:
            if rec.state != 'draft':
                rec.read_only = True
            else:
                rec.read_only = False