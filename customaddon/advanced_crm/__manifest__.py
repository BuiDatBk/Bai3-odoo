# -*- coding: utf-8 -*-
{
    'name': "customaddon/advanced_crm",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sales_team', 'crm', 'sale_crm', 'mail', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/crm_team_view_form_inherit.xml',
        'views/crm_lead_view_form_inherit.xml',
        'views/monthly_report_view.xml',
        'security/security_rules.xml',
        'wizard/detailed_report.xml',
        'wizard/content_detailed_report.xml',
        'wizard/target_assessment_report.xml',
        'wizard/content_target_report.xml',
        'data/cron.xml',
        'data/email_template.xml',
        # 'data/cron_plan_email.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
