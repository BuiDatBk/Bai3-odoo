import datetime

from odoo import fields, models, api


class TargetAssessmentReport(models.Model):
    _name = 'target.assessment.report'

    month = fields.Selection([('1',1),('2',2),('3',3),('4',4),
                              ('5',5),('6',6),('7',7),('8',8),
                              ('9',9),('10',10),('11',11),
                              ('12',12),], default=str(fields.datetime.now().month), required=True)
    team_sales = fields.Many2many( "crm.team", string="Sales Team")
    def action_export_data(self):
        self.ensure_one()
        month = int(self.month)
        create_date = datetime.datetime.today().replace(day=1, month=month)
        date_from = create_date
        date_to = datetime.datetime.today().replace(day=1, month=month + 1)

        if self.team_sales:
            opportunities = self.env['crm.lead'].search([
                ('team_id', 'in', self.team_sales.ids),
                ('create_date', '>=', date_from), ('create_date', '<', date_to)])

            list_dict_data = []
            for team in self.env["crm.team"].search([]):
                team.cost = 0.0

            for team in self.env["crm.team"].search([]):
                for opportunity in opportunities:
                    if opportunity.team_id.id == team.id:
                        team.cost = team.cost + opportunity.sale_amount_total

            target = 0.0
            for team in self.team_sales.ids:
                match self.month:
                    case "1":
                        target = self.env["crm.team"].browse(team).month1
                    case "2":
                        target = self.env["crm.team"].browse(team).month2
                    case "3":
                        target = self.env["crm.team"].browse(team).month3
                    case "4":
                        target = self.env["crm.team"].browse(team).month4
                    case "5":
                        target = self.env["crm.team"].browse(team).month5
                    case "6":
                        target = self.env["crm.team"].browse(team).month6
                    case "7":
                        target = self.env["crm.team"].browse(team).month7
                    case "8":
                        target = self.env["crm.team"].browse(team).month8
                    case "9":
                        target = self.env["crm.team"].browse(team).month9
                    case "10":
                        target = self.env["crm.team"].browse(team).month10
                    case "11":
                        target = self.env["crm.team"].browse(team).month11
                    case "12":
                        target = self.env["crm.team"].browse(team).month12
                    case _:
                        target = self.env["crm.team"].browse(team).month2
                list_dict_data.append({"team": team,
                                       "actual_revenue": self.env["crm.team"].browse(team).cost,
                                       "revenue_target": target})

            self.env['report.two'].search([]).unlink()

            for x in list_dict_data:
                self.env["report.two"].create({
                    "team": x["team"],
                    "actual_revenue": x["actual_revenue"],
                    "revenue_target": x["revenue_target"]
                })

            return {
                "name": "Opportunity",
                'res_model': 'report.two',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'view_id': self.env.ref("advanced_crm.report_tree_view").id,
                'target': 'current',
           }

        else:
            opportunities = self.env['crm.lead'].search([
                ('create_date', '>=', date_from), ('create_date', '<', date_to)])

            list_dict_data = []
            for team in self.env["crm.team"].search([]):
                team.cost = 0.0

            for team in self.env["crm.team"].search([]):
                for opportunity in opportunities:
                    if opportunity.team_id.id == team.id:
                        team.cost = team.cost + opportunity.sale_amount_total

            target = 0.0
            for team in self.env["crm.team"].search([]):
                match self.month:
                    case "1":
                        target = team.month1
                    case "2":
                        target = team.month2
                    case "3":
                        target = team.month3
                    case "4":
                        target = team.month4
                    case "5":
                        target = team.month5
                    case "6":
                        target = team.month6
                    case "7":
                        target = team.month7
                    case "8":
                        target = team.month8
                    case "9":
                        target = team.month9
                    case "10":
                        target = team.month10
                    case "11":
                        target = team.month11
                    case "12":
                        target = team.month12
                    case _:
                        target = team.month2
                list_dict_data.append({"team": team.id,
                                       "actual_revenue": team.cost,
                                       "revenue_target": target})

            self.env['report.two'].search([]).unlink()

            for x in list_dict_data:
                self.env["report.two"].create({
                    "team": x["team"],
                    "actual_revenue": x["actual_revenue"],
                    "revenue_target": x["revenue_target"]
                })

            return {
                "name": "Opportunity",
                'res_model': 'report.two',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'view_id': self.env.ref("advanced_crm.report_tree_view").id,
                'target': 'current',
                # 'domain': [('month', '=', self.month), ('correct_year', '=', True)],
            }
