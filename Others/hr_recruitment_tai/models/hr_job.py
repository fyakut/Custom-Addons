# -*- encoding: utf-8 -*-
#
#Created on May 27, 2019
#
#@author: dogan
#

from odoo import models, fields, api
from odoo.exceptions import Warning
from odoo.tools.translate import _


APPLICATION_FAIL_INSUFFICIENT_CV = 1
APPLICATION_FAIL_COUNTRY_MISSING = 2
APPLICATION_FAIL_NO_RESUME = 3

class HrJob(models.Model):
    _inherit = 'hr.job'
    
    date_start = fields.Datetime('Start date',help='Date the job posting starts')
    date_end = fields.Datetime('End date')

    work_type = fields.Selection([('bluecollar', 'Blue Collar'),
                                  ('whitecollar', 'White Collar')],
                                 string='Type', default='bluecollar')

    domain_ids = fields.One2many('hr.job.domains', 'job_id', string='Domains')
    
    @api.constrains('date_start','date_end')
    def _check_dates(self):
        if self.date_start > self.date_end:
            raise Warning(_('Date validation error'))
    

    @api.model
    def default_get(self,default_fields):
        res = super(HrJob, self).default_get(default_fields)
        employee = self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
        res['department_id'] = employee.department_id.id
        return res

    @api.multi
    def can_apply(self):
        self.ensure_one()
        candidate = self.env.user.candidate_id
        reasons = []

        if not candidate.tckn:
            reasons.append(APPLICATION_FAIL_NO_RESUME)
            return not len(reasons), reasons

        #if len(candidate.education_ids) == 0:
        #    reasons.append(APPLICATION_FAIL_COUNTRY_MISSING)

        if not candidate.country_id:
            reasons.append(APPLICATION_FAIL_INSUFFICIENT_CV)


        return not len(reasons), reasons

    @api.multi
    def allready_applied(self):
        self.ensure_one()
        candidate = self.env.user.candidate_id

        if candidate.tckn:
            num_applications = self.env['hr.applicant'].sudo().search_count([('job_id','=',self.id),('candidate_id','=',candidate.id)])
        else:
            num_applications = -1

        return num_applications



    class HrJobDomains(models.Model):
        _name = 'hr.job.domains'
        _description = "Job Domains"

        domain_name = fields.Char('Domain name')
        job_id = fields.Many2one('hr.job', string='Job', required=True)
