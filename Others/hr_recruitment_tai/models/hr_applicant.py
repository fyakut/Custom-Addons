# -*- encoding: utf-8 -*-
#
#Created on May 27, 2019
#
#@author: dogan
#

from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import Warning
from odoo.tools.translate import _
from odoo.exceptions import UserError

import math
from datetime import datetime, timedelta


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    interview_ids = fields.One2many('hr.interview', 'applicant_id', string='Applicant')

    candidate_id = fields.Many2one('hr.recruitment.candidate',string='Candidate')
    candidate_image = fields.Binary('Image', related='candidate_id.candidate_image', readonly=True)

    work_type = fields.Selection(related='candidate_id.work_type', store=False)

    state = fields.Selection([('new','New'),
                              ('accepted','Accepted'),
                              ('rejected','Rejected'),
                              ('withdrawn','Withdrawn'),
                              ('waiting','Waiting')], string='State', default='new')

    next_action_enabled = fields.Boolean('Next Enabled', compute='_compute_next_action_enabled')
    next_stage = fields.Many2one('hr.recruitment.stage',compute='_compute_next_stage')

    work_type = fields.Selection([('bluecollar', 'Blue Collar'),
                                  ('whitecollar', 'White Collar')],
                                 string='Type', default='bluecollar')

    # -----------------------------

    joining_type = fields.Selection([('first_join_to_company', 'First Join'),
                                       ('not_first_join_to_company', 'Not First Join')],
                                      string='İşe Gİriş Tipi')

    job_title_advised_by_department = fields.Selection([('engineer', 'Engineer'),
                                     ('other', 'Others')],
                                    string='Job Title')

    job_title_level_advised_by_department = fields.Selection([('1', '1'),
                                       ('2', '2')],
                                      string='Job Title Level')

    guide_person = fields.Many2many('hr.employee', string='Guide Person', required=True)


    job_definition = fields.Text('Job Definition')
    employee_needed_date =fields.Date('Need Date', required=False)

    project = fields.Selection([('tfx', 'TFX'),
                                ('others', 'others')],
                               string='Project')

    working_place = fields.Selection([('headquarters', 'Headquarters'),
                                ('others', 'others')],
                               string='working_place')

    work_environment_is_danger = fields.Selection([('danger', 'Danger'),
                                      ('not danger', 'Not Danger')],
                                     string='Work Environment Danger')

    lunch_time = fields.Selection([('12:00 - 13:00', '12:00 - 13:00'),
                                ('13:00 - 14:00', '13:00 - 14:00')],
                                string='Lunch Time')

    # -----------------------------

    join_to_company_date =fields.Date('Join Date', required=False)

    job_title_advised_by_hr = fields.Selection([('engineer', 'Engineer'),
                                                     ('other', 'Others')],
                                                       string='Job Title')

    job_title_level_advised_by_hr = fields.Selection([('1', '1'),
                                                        ('2', '2')],
                                                        string='Job Title Level')

    job_title_level_comments = fields.Text('Comments ')

    salary_degree = fields.Char(string='Salary Degree')

    salary_level = fields.Char(string='Salary Level')

    salary = fields.Char(string='Gross Salary ')

    salary_raise = fields.Selection([('yes', 'Raise'),
                               ('no', 'No Raise')],
                               string='Salary Raise')

    salary_definition_date = fields.Date('Salary Definition Date', required=False)

    # -----------------------------



    @api.model
    def default_get(self, fields):
        res = super(HrApplicant, self).default_get(fields)

        if 'stage_id' in fields:
            ise_alim = self.env['ir.model.data'].xmlid_to_object('hr_recruitment_tai.ise_alim_grubu')
            res['stage_id'] = ise_alim.id

        if 'name' in fields:
            res['name'] = '/'

        return res

    @api.one
    def _compute_next_stage(self):
        self.next_stage = self.env['hr.recruitment.stage'] \
            .search([('sequence', '>', self.stage_id.sequence)], limit=1)



    @api.multi
    def _compute_next_action_enabled(self):
        self.ensure_one()

        reject_stage_id = self.env['ir.model.data'].xmlid_to_res_id('hr_recruitment_tai.stage_rejected')
        if self.next_stage.id == reject_stage_id:
            self.next_action_enabled = False
        else:
            self.next_action_enabled = True


    @api.multi
    def write(self, vals):
        if 'stage_id' in vals:#and self.env.user.has_group():
            if self.env.user.has_group('hr_recruitment_tai.group_hr_birim_yoneticisi') and \
                not self.env.user.has_group('hr_recruitment_tai.group_hr_birim_baskani'):
                # birim yoneticisi sadece teknik degerlendirme ve form girisinde bir adim ilerletebilecek
                for applicant in self:
                    next_stage = self.env['hr.recruitment.stage'].browse([vals['stage_id']])
                    if applicant.stage_id.sequence == 7 and next_stage.sequence not in [6,7,8]:
                        raise Warning(_('%s asamasina ilerletemezsiniz' % next_stage.name))
                    elif applicant.stage_id.sequence != 7:
                        raise Warning(_('Bu asamada yetkiniz yok'))
                    
                    
                 
        return super(HrApplicant, self).write(vals)

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.applicant') or '/'
        scrap = super(HrApplicant, self).create(vals)

        return scrap
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # retrieve job_id from the context and write the domain: ids + contextual columns (job or default)
        stages = super(HrApplicant, self)._read_group_stage_ids(stages, domain, order)
        
        if self.env.user.has_group('hr_recruitment_tai.group_hr_birim_yoneticisi') and \
            not self.env.user.has_group('hr_recruitment.group_hr_recruitment_user'):
            stages = stages.filtered(lambda s: s.sequence > 4)

        return stages
    
    
    @api.model
    def check_need_action(self):
        
        date_before = datetime.utcnow() #+ timedelta(days=-10)
        
        applicants_to_notify = self.search([('date_last_stage_update','<', date_before)])
        
        apps = {}
        
        for app in applicants_to_notify:
            if app.user_id not in apps.keys():
                apps[app.user_id] = self.env['hr.applicant']
                
            apps[app.user_id] |= app


        notification_template = self.env.ref('hr_recruitment_tai.email_template_notify_applicant')
        if notification_template:
            for user, applications in apps.items():
                body_html = '<table><tbody>'
                for app in applications:
                    notification_template.sudo().send_mail(app.id, force_send=False, 
                                                       email_values={'email_to':user.email} )

                    body_html = '%a<tr>%s</tr>' % (body_html, app.name)

                body_html = '%a</tbody></table>' % (body_html)
                
                notification_template.sudo().send_mail(applications[0].id, force_send=False, 
                                                       email_values={'email_to':user.email, 'body_html':body_html} )
            
            
        return

    @api.multi
    def archive_applicant(self):

        reject_stage_id = self.env['ir.model.data'].xmlid_to_res_id('hr_recruitment_tai.stage_rejected')
        self.write({'stage_id':reject_stage_id,
                    'state':'rejected'})

    @api.multi
    def terminate_applicant(self):
        self.write({'active': False})

    @api.multi
    def reset_applicant(self):
        """ Reinsert the applicant into the recruitment pipe in the first stage"""
        default_stage_id = self._initial_stage_id()
        self.write({'active': True,
                    'stage_id': default_stage_id,
                    'state':'new'})

    @api.multi
    def _initial_stage_id(self):
        return (self.env['ir.model.data'].xmlid_to_res_id('hr_recruitment_tai.ise_alim_grubu'))

    @api.multi
    def action_next_stage(self):
        self.ensure_one()
        if self.next_action_enabled:
            self.stage_id = self.next_stage


    @api.multi
    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.candidate_id.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                # contact_name = applicant.partner_id.name_get()[0][1]
                job_title = applicant.candidate_id.work_type

            else:
                raise UserError(_('You must define an Candidate and Partner!'))
            if applicant.job_id and (applicant.candidate_id.partner_id.name):
                applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                employee = self.env['hr.employee'].create({
                    'name': applicant.candidate_id.partner_id.name,
                    'job_id': applicant.job_id.id,
                    'address_home_id': address_id,
                    'emergency_contact': job_title,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                                  and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                                  and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id
                                  and applicant.department_id.company_id.phone or False})
                applicant.write({'emp_id': employee.id})
                applicant.job_id.message_post(
                    body=_(
                        'New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                    subtype="hr_recruitment.mt_job_applicant_hired")
            else:
                raise UserError(_('You must define an Applied Job and a Contact Name for this applicant.'))

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        dict_act_window['context'] = {'form_view_initial_mode': 'edit'}
        dict_act_window['res_id'] = employee.id
        return dict_act_window


class RecruitmentStage(models.Model):
    _inherit = "hr.recruitment.stage"
