# -*- encoding: utf-8 -*-
#
#Created on May 27, 2019
#
#@author: dogan
#
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_candidate = fields.Boolean('Is Candidate')


class ResUser(models.Model):
    _inherit = 'res.users'
    
    recruitment_departments = fields.Many2many('hr.department',compute='_compute_recruitment_departments')

    application_ids = fields.Many2many('hr.applicant', string='Applications', compute='_compute_applications')

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate',compute='_compute_candidate')

    @api.multi
    def _compute_candidate(self):
        candidate_obj = self.env['hr.recruitment.candidate']
        for user in self:
            self.candidate_id = candidate_obj.search([('partner_id', '=', user.partner_id.id)],limit=1)

    @api.multi
    def _compute_applications(self):
        applicant_obj = self.env['hr.applicant']
        for user in self:
            self.application_ids = applicant_obj.search([('candidate_id.partner_id','=',user.partner_id.id)])
    
    @api.one
    def _compute_recruitment_departments(self):
        employee = self.env['hr.employee'].search([('user_id','=',self.id)])
        self.recruitment_departments = employee.department_id

    @api.model
    def _signup_create_user(self, values):
        values.update({'is_candidate':True})
        res = super(ResUser, self)._signup_create_user(values)

        self.env['hr.recruitment.candidate'].create({'partner_id': res.partner_id.id})

        return res



class resState(models.Model):
    _inherit = 'res.country.state'


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        return super(resState,self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

