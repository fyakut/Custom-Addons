# -*- encoding: utf-8 -*-
from . import models
from . import controllers

from odoo import api, SUPERUSER_ID

def _clear_default_data(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    default_application_stage_1 = env.ref('hr_recruitment.stage_job1', raise_if_not_found=False)
    if default_application_stage_1:
        default_application_stage_1.unlink()
    # remove all records - option 1    
    #env['hr.recruitment.stage'].search([]).unlink()
    
    #remove all records - option 2
    
    #cr.execute('delete from hr_requrietment_stage')