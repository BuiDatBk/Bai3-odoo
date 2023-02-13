from odoo import fields, models, api


class ResultExportReport(models.TransientModel):
    _name = 'result.export.report'
    _rec_name = 'file_name'

    file = fields.Binary()
    file_name = fields.Text()