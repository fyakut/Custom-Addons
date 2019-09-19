# -*- coding: utf-8 -*-
{
    'name' : 'TAI HR Recruitment Extensions',
    'version' : '1.0',
    'summary': '--',
    'sequence': 15,
    'description': """

    """,
    'category': 'Human Resources',
    'depends': ['hr_recruitment',
                'partner_firstname',
                'auth_signup',
                'contacts',
                'website',
                'website_hr_recruitment'],
    'data': [
        'security/res_groups.xml',
        'security/rules.xml',
        'security/ir.model.access.csv',
        'data/tai_hr_stages.xml',
        'data/tai_hr_demo_users.xml',
        'views/hr_job_views.xml',
        'views/hr_menu.xml',
        'views/hr_interview_views.xml',
        'views/hr_tai_menu.xml',
        'views/hr_candidate_views.xml',
        'views/hr_applicant_views.xml',
        'data/ir_cron_data.xml',
        'data/mail_templates.xml',
        'data/hr_recruitment_tai_data.xml',
        'report/candidate_report_templates.xml',
        'report/candidate_report.xml',
        'views/assets.xml',
        'views/portal_templates.xml',
        'views/website_templates.xml',
        'views/auth_templates.xml'

    ],
    'demo': [
        
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
