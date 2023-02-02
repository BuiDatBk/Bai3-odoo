import datetime

from odoo import fields, models, api


class DetaiedReport(models.Model):
    _name = 'detailed.report'

    month = fields.Selection([('1', 1), ('2', 2), ('3', 3), ('4', 4),
                              ('5', 5), ('6', 6), ('7', 7), ('8', 8),
                              ('9', 9), ('10', 10), ('11', 11),
                              ('12', 12), ], default=str(fields.datetime.now().month), required=True)
    team_sales = fields.Many2many("crm.team", string="Sales Team")

    @api.depends('team_sales')
    def action_export_data(self):
        self.ensure_one()
        month = int(self.month)
        create_date = datetime.datetime.today().replace(day=1, month=month)
        date_from = create_date
        date_to = datetime.datetime.today().replace(day=1, month=month + 1)

        if self.team_sales:
            opportunities = self.env['crm.lead'].search(
                [('team_id', 'in', self.team_sales.ids),
                 ('create_date', '>=', date_from), ('create_date', '<', date_to)])

            list_dict_data = []
            for opportunity in opportunities:
                list_dict_data.append({"opportunity": opportunity.name,
                                       "user_id": opportunity.user_id.id,
                                       "team_id": opportunity.team_id.id,
                                       "min_revenue": opportunity.min_revenue,
                                       "sale_amount_total": opportunity.sale_amount_total})

            self.env['report.one'].search([]).unlink()

            for x in list_dict_data:
                self.env["report.one"].create({
                    "opportunity": x["opportunity"],
                    "person": x["user_id"],
                    "team": x["team_id"],
                    "min": x["min_revenue"],
                    "sale_total": x["sale_amount_total"]
                })

            return {
                "name": "Opportunity",
                'res_model': 'report.one',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'view_id': self.env.ref("advanced_crm.report_tree_view").id,
                'target': 'current',
            }

        else:
            opportunities = self.env['crm.lead'].search([
                ('create_date', '>=', date_from), ('create_date', '<', date_to)])

            list_dict_data = []
            for opportunity in opportunities:
                if opportunity.team_id:
                    list_dict_data.append({"opportunity": opportunity.name,
                                           "user_id": opportunity.user_id.id,
                                           "team_id": opportunity.team_id.id,
                                           "min_revenue": opportunity.min_revenue,
                                           "sale_amount_total": opportunity.sale_amount_total})

            self.env['report.one'].search([]).unlink()

            for x in list_dict_data:
                self.env["report.one"].create({
                    "opportunity": x["opportunity"],
                    "person": x["user_id"],
                    "team": x["team_id"],
                    "min": x["min_revenue"],
                    "sale_total": x["sale_amount_total"]
                })

            return {
                "name": "Opportunity",
                'res_model': 'report.one',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'view_id': self.env.ref("advanced_crm.report_tree_view").id,
                'target': 'current',
            }
