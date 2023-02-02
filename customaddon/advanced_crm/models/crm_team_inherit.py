from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class ModelName(models.Model):
    _inherit = "crm.team"

    month1  = fields.Float(string='Tháng 1' )
    month2  = fields.Float(string='Tháng 2' )
    month3  = fields.Float(string='Tháng 3' )
    month4  = fields.Float(string='Tháng 4' )
    month5  = fields.Float(string='Tháng 5' )
    month6  = fields.Float(string='Tháng 6' )
    month7  = fields.Float(string='Tháng 7' )
    month8  = fields.Float(string='Tháng 8' )
    month9  = fields.Float(string='Tháng 9' )
    month10 = fields.Float(string='Tháng 10')
    month11 = fields.Float(string='Tháng 11')
    month12 = fields.Float(string='Tháng 12')
    cost = fields.Float()

    #TODO statement
    # exec("a = 1") - thuc thi chuoi nhu lenh
    # i = eval("a[0]") - thuc thi chuoi nhu lenh va tra ve gia tri

    @api.constrains('month1','month2','month3','month4','month5','month6','month7','month8','month9','month10','month11','month12')
    def _check_positive_money(self):
        if any(rec.month1 <= 0 or rec.month2 <= 0 or rec.month3 <= 0 or rec.month4 <= 0
               or rec.month5 <= 0 or rec.month6 <= 0 or rec.month7 <= 0 or rec.month8 <= 0
               or rec.month9 <= 0 or rec.month10 <= 0 or rec.month11 <= 0 or rec.month12 <= 0
               for rec in self):
            raise ValidationError(_('You can not enter negative money.'))
