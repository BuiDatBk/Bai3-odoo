import datetime

import odoo
import logging
import json

from odoo.http import request, Response

_logger = logging.getLogger(__name__)


class MonthlyReportAPI(odoo.http.Controller):
    @odoo.http.route('/foo', auth='public')
    def foo_handler(self):
        return "Welcome to 'foo' API!"

    @odoo.http.route('/bar', auth='public')
    def bar_handler(self):
        return json.dumps({
            "content": "Welcome to 'bar' API!"
        })

    @odoo.http.route(['/pet'], methods=['POST'], type='json', auth="none", csrf=True)
    def pet_handler(self, **kw):
        # body
        if request.httprequest.json.get("token") != "odooneverdie":
            return {"error": "Invalid Token"}

        model_name = "monthly.report"
        try:
            response = {}
            records = request.env[model_name].sudo().search([])
            for rec in records:
                if rec.create_date.month != request.httprequest.json.get("month"):
                    return response
                crm_report = []
                purchase_report = []
                for crm in rec.crm_month_report:
                    crm_report.append({
                        "sale_team_name": crm.sales_team_id.name,
                        "real_revenue": crm.actual_revenue,
                        "diff": crm.diff_actual_target
                    })
                response["sales"] = crm_report

                for purchase in rec.purchase_month_report:
                    purchase_report.append({
                        "department_name": purchase.department_id.name,
                        "real_cost": purchase.actual_spending,
                        "diff": purchase.diff_actual_limit
                    })
                response["purchase"] = purchase_report

        except Exception as e:
            response = {
                "status": "error",
                "content": "not found"
            }
            raise e
        return response

        # return request.make_response(json.dumps(response), headers=[('Content-Type', 'application/json')])
