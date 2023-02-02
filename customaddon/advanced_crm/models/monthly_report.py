from odoo import fields, models, api


class MonthlyReport(models.Model):
    _name = 'monthly.report'


    def action_send_mail(self):

        # for line in self.env.ref("advanced_purchase.accountant").users:
        #     email_values = {
        #         'email_cc': False,
        #         'auto_delete': True,
        #         'recipient_ids': [],
        #         'partner_ids': [],
        #         'scheduled_date': False,
        #         # 'email_from': 'nguyendanhbinhgiang@gmail.com',
        #         'email_to': line.email,
        #     }
        #
        #     mail_template = self.env.ref('advanced_crm.mail_template_mobile_merge_request')
        #     if mail_template:
        #         mail_template.send_mail(self.id, force_send=True, email_values=email_values)

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

