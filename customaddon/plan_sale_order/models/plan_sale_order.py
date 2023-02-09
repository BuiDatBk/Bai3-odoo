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

    btn_reset_invisible = fields.Boolean(compute='compute_btn_reset_invisible')
    btn_visible_state = fields.Boolean(string='Visible', compute='compute_visible')
    read_only = fields.Boolean(string='Add a Line', compute='is_readonly')

    def compute_btn_reset_invisible(self):
        for rec in self:
            if rec.state == 'refuse':
                rec.btn_reset_invisible = False
            else:
                rec.btn_reset_invisible = True

    def action_reset(self):
        self.state = 'sent'
        for line in self.approval_ids:
            line.status_approval = 'not_approve'

    def action_send_to_review(self):
        # self.ensure_one()
        # message_list = self.approval_ids.mapped("approver.partner_id.id")
        # self.sudo().message_post(body='Business plan need approval',
        #                          partner_ids=message_list,
        #                          message_type='notification')

        # send a activity
        self.ensure_one()
        todos = [{
            'res_id': self.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'plan.sale.order')]).id,
            'user_id': approval.approver.id,
            'summary': 'can confirm',
            'note': 'Plan can xac nhan',
            'activity_type_id': 4,  # trong database - psql/select * from mail_activity_type - choose activity type
            'date_deadline': fields.datetime.now(),
        } for approval in self.approval_ids]
        # for approval in self.env.ref('plan_sale_order.group_approval').users

        for todo in todos:
            self.env['mail.activity'].sudo().create(todo)
            self.env.cr.commit()

        for rec in self:
            rec.state = 'sent'
            for line in rec.approval_ids:
                line.status_approval = 'not_approve'

    def create_activity(self):
        self.ensure_one()
        todos = [{
            'res_id': self.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
            'user_id': kt.id,
            'summary': 'can confirm',
            'note': 'Can nhan vien ke toan confirm',
            'activity_type_id': 4,
            'date_deadline': fields.date.today(),
        } for kt in self.env.ref('purchase_inherit.invoice_employee').users]

        for todo in todos:
            self.env['mail.activity'].sudo().create(todo)
            self.env.cr.commit()

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
    def compute_visible(self):
        for rec in self:
            if rec.state != 'draft':
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

    def action_send_mail(self):
        email_values = {
            'email_cc': False,
            'auto_delete': True,
            'recipient_ids': [],
            'partner_ids': [],
            'scheduled_date': False,
            # 'email_from': 'nguyendanhbinhgiang@gmail.com',
            'email_to': 'buivandaty2k@gmail.com',
        }

        mail_template = self.env.ref('advanced_crm.mail_template_mobile_merge_request')
        if mail_template:
            mail_template.send_mail(self.id, force_send=True, email_values=email_values)
