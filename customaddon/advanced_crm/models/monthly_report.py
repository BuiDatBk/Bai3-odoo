import datetime

from odoo import fields, models, api


class MonthlyReport(models.Model):
    _name = 'monthly.report'

    crm_month_report = fields.Many2many('crm.month.report.line')
    purchase_month_report = fields.Many2many('purchase.month.report.line')

    def action_send_mail(self):

        for line in self.env.ref("advanced_purchase.accountant").users:
            email_values = {
                'email_cc': False,
                'auto_delete': True,
                'recipient_ids': [],
                'partner_ids': [],
                'scheduled_date': False,
                # 'email_from': 'nguyendanhbinhgiang@gmail.com',
                'email_to': line.email,
            }

        # email_values = {
        #     'email_cc': False,
        #     'auto_delete': True,
        #     'recipient_ids': [],
        #     'partner_ids': [],
        #     'scheduled_date': False,
        #     # 'email_from': 'nguyendanhbinhgiang@gmail.com',
        #     'email_to': 'buivandaty2k@gmail.com',
        # }

            self.search([]).unlink()
            self.env['crm.month.report.line'].search([]).unlink()
            self.env['purchase.month.report.line'].search([]).unlink()

            create_date = datetime.datetime.today().replace(day=1, month=2)
            date_from = create_date
            date_to = datetime.datetime.today().replace(day=1, month=3)
            opportunities = self.env['crm.lead'].search([
                ('create_date', '>=', date_from), ('create_date', '<', date_to)
            ])

            crm_list_line = []
            for team in self.env["crm.team"].search([]):
                team.cost = 0.0

            for team in self.env["crm.team"].search([]):
                for opportunity in opportunities:
                    if opportunity.team_id.id == team.id:
                        team.cost = team.cost + opportunity.sale_amount_total

            target = 0.0
            for team in self.env["crm.team"].search([]):
                target = team.month2
                # match self.month:
                #     case "1":
                #         target = self.env["crm.team"].browse(team).month1
                #     case "2":
                #         target = self.env["crm.team"].browse(team).month2
                #     case "3":
                #         target = self.env["crm.team"].browse(team).month3
                #     case "4":
                #         target = self.env["crm.team"].browse(team).month4
                #     case "5":
                #         target = self.env["crm.team"].browse(team).month5
                #     case "6":
                #         target = self.env["crm.team"].browse(team).month6
                #     case "7":
                #         target = self.env["crm.team"].browse(team).month7
                #     case "8":
                #         target = self.env["crm.team"].browse(team).month8
                #     case "9":
                #         target = self.env["crm.team"].browse(team).month9
                #     case "10":
                #         target = self.env["crm.team"].browse(team).month10
                #     case "11":
                #         target = self.env["crm.team"].browse(team).month11
                #     case "12":
                #         target = self.env["crm.team"].browse(team).month12
                #     case _:
                #         target = self.env["crm.team"].browse(team).month2
                crm_list_line.append({"team": team.id,
                                       "actual_revenue": team.cost,
                                       "diff_actual_target": team.cost - target})

            for rec in crm_list_line:
                self.env['crm.month.report.line'].create(
                    {"sales_team_id": rec['team'],
                     "actual_revenue": rec['actual_revenue'],
                     "diff_actual_target": rec['diff_actual_target']
                     })
            crm_report_list = []
            for rec in self.env['crm.month.report.line'].search([]):
                crm_report_list.append(rec.id)

            # purchase report line
            po = self.env['purchase.order'].sudo().search(
                [('state', '=', 'purchase'), ('create_date', '>=', date_from), ('create_date', '<', date_to)])
            dict_report = []
            list_dep = []
            for dep in self.env['hr.department'].search([]):
                dep.cost = 0.0

            for order in po:
                if order.department.id not in list_dep:
                    for dep in self.env['hr.department'].search([]):
                        if dep.id == order.department.id:
                            dep.cost = dep.cost + order.amount_total

            for dep in self.env['hr.department'].search([]):
                dict_report.append(
                    {"department_id": dep.id, "actual_spending": dep.cost, "diff_actual_limit": dep.cost- dep.spending_limit_a_month})

            for rec in dict_report:
                self.env['purchase.month.report.line'].create(
                    {"department_id": rec['department_id'],
                     "actual_spending": rec['actual_spending'],
                     "diff_actual_limit": rec['diff_actual_limit']
                     })
            purchase_report_list = []
            for rec in self.env['purchase.month.report.line'].search([]):
                purchase_report_list.append(rec.id)

            self.create({"crm_month_report": [(6, 0, crm_report_list)],
                         "purchase_month_report": [(6, 0, purchase_report_list)]})

            mail_template = self.env.ref('advanced_crm.mail_template_mobile_merge_request')
            if mail_template:
                mail_template.send_mail(self.env['monthly.report'].search([])[0].id, force_send=True,
                                        email_values=email_values)
