# -*- encoding: utf-8 -*-
#
# Created on May 28, 2019
#
# @author: ipek
#

from odoo import models, fields, api
import re
import requests
from odoo.http import request
import warnings
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import datetime



class Exam(models.Model):
    _name = "hr.recruitment.exam"
    _description = "Exam"

    name = fields.Char('Exam Name')


class HrCandidateInternship(models.Model):
    _name = "hr.recruitment.candidate.internship"

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', required=True)
    internship_company = fields.Char('Internship Company')
    date_from = fields.Date('Start Date', required=True)
    date_to = fields.Date('End Date', required=True)

class HrCandidateExam(models.Model):
    _name = 'hr.recruitment.candidate.exam'

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', required=True)

    eng_level = fields.Selection([('basic', 'Basic'),
                             ('inter', 'Intermediate'),
                             ('advanced', 'Advanced')],
                            string='Eng Level')

    eng_exam_name = fields.Many2one("hr.recruitment.exam", string='Exam')
    eng_exam_score  = fields.Char('Exam Score')
    eng_exam_date = fields.Char('Exam Date', required=True)

    #belge eklenecek

class HrCandidateOtherExams(models.Model):
    _name = 'hr.recruitment.candidate.other_exams'

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', required=True)

    other_lang_name = fields.Selection([('ger', 'German'),
                             ('fr', 'French'),
                             ('span', 'Spanish')],
                            string='Other Lang')

    other_exam_level = fields.Selection([('basic', 'Basic'),
                             ('inter', 'Intermediate'),
                             ('advanced', 'Advanced')],
                            string='Other Language Level')


    #belge eklenecek


class HrCandidateKnowledge(models.Model):
    _name = 'hr.recruitment.candidate.knowledge'

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', required=True)
    name = fields.Char('Knowledge Name')
    definition = fields.Char('Knowledge Definition')
    level = fields.Char('Knowledge Level')


class HrCandidateCourse(models.Model):
    _name = 'hr.recruitment.candidate.course'

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', required=True)
    name = fields.Char('Course')
    company = fields.Char('Course Company')
    date = fields.Date('Course Date', required=True)


class HrCandidateExperience(models.Model):
    _name = 'hr.recruitment.candidate.experience'

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', required=True)
    company_name = fields.Char('Company Name')
    position = fields.Char('Position')
    responsibilities = fields.Text('Responsibilities')
    type = fields.Selection([('full', 'Full Time'),
                             ('part', 'Part Time'),
                             ('internship', 'Internship')],
                            string='Working Type')
    reason_for_leaving= fields.Text('Reason for Leaving')
    date_from = fields.Char('Start Date', required=True)
    date_to = fields.Char('End Date', required=True)
    is_current = fields.Boolean(string='Is current?', default=False)
    employer = fields.Char('Employer')
    employer_company = fields.Char('Employer')
    employer_duty = fields.Char('Employer')
    employer_phone_number = fields.Char('Phone Number', size=11)

class HrCandidateEducation(models.Model):
    _name = 'hr.recruitment.candidate.education'

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', required=True)

    degree = fields.Many2one('hr.recruitment.candidate.degree', string='Degree')
    school_id = fields.Many2one('hr.recruitment.candidate.school', string='School', required=True)
    faculty_id = fields.Many2one('hr.recruitment.candidate.faculty', string='Faculty', required=True)
    school_department_id = fields.Many2one('hr.recruitment.candidate.department', string='Department')

    school_province = fields.Many2one('res.country.state', string='Province')

    date_from = fields.Char('Start Date', required=True)
    date_to = fields.Integer('End Date', required=True)
    graduation_score = fields.Float('Graduation Score', required=True)

    @api.onchange('degree')
    def _onchange_degree(self):
        self.school_id = False
        if self.degree:
            return {'domain': {'school_id': [('degree_id', '=', self.degree.id)]}}
        else:
            return {'domain': {'school_id': []}}

    @api.onchange('faculty_id')
    def _onchange_faculty(self):
        self.school_department_id = False
        if self.faculty_id:
            return {'domain': {'school_department_id': [('faculty_id', '=', self.faculty_id.id)]}}
        else:
            return {'domain': {'school_department_id': []}}

class HrCandidateReferance(models.Model):
    _name = 'hr.recruitment.candidate.referance'
uired=True)

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', req
    name = fields.Char('Referance Name', required=True)
    surname = fields.Char('Referance Surname', required=True)
    company = fields.Char('Company', required=True)
    duty = fields.Char('Duty', required=True)
    phone = fields.Char('Phone', required=True)
    is_relative = fields.Boolean(string='Is a Relative', default=False,
                                 help="Check this box if this person is a relative/familiar working in TUSAŞ or retired from TUSAŞ")
    relationship_degree = fields.Char('Relationship degree')

class HREnterpriseQualificationExams(models.Model):
    _name = 'hr.recruitment.candidate.hrenterprisequalificationexams'

    tracking_number = fields.Char(string='Tracking Number')
    access_code = fields.Char(string='Access Code')
    access_link = fields.Char(string='Access Link')
    state = fields.Selection([('draft', 'Draft'),
                                    ('done', 'Done')],
                                    string='Draft')
    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', required=True)
    assessment_types = fields.Selection([('PiT', 'PiT - Kişilik Envanteri'),
                                   ('genel_yetenek', 'Genel Yetenek'),
                                   ('genel_kultur', 'Genel Kültür'),
                                   ('ingilizce', 'HRWin - İngilizce'),
                                   ('kriterleri_saglamayan', 'Kriterleri Sağlamayan'),
                                   ('kurum_yasakli', 'Kurum Yasaklı')],
                                  string='Assessment Type')
    assessment_result_link =fields.Char(string='Assessment Result Link')
    completion_date = fields.Date('Completion Date', required=False)

    @api.multi
    def post_candidate_assessment(self):
        try:
            url = "https://api.hrpeak.com/AssessmentCenter/CandidateInvite"

            data = {
                "Battery": "A56A3BE7-76A4-4132-BD7A-02FA6356A6D7",
                "FullName": self.candidate_id.partner_id.name,
                "EMailAddress": self.candidate_id.partner_id.email,
                "MobilePhoneNumber": self.candidate_id.partner_id.phone,
                "CandidateId": self.candidate_id.partner_id,
                "Position": "",
                "SendNotification": 'true',
                "CustomMessage": "sample string 7",
                "CustomLanguage": 0,
                "StartDate": "2018-06-16T14:42:49.4253199+03:00",
                "EndDate": "2020-09-16T14:42:49.4253199+03:00"
            }

            result = requests.post(url, data, auth=('wg2ujttuh', 'm6883ugpb')).json()


            tracking_number = result["TrackingNumber"]
            access_code = result["AccessCode"]
            access_link = result["AccessLink"]


            self.write({
                'assessment_types': 'PiT',
                'candidate_id': self.candidate_id.id,
                'tracking_number': tracking_number,
                'access_code': access_code,
                'access_link': access_link,
                'state': 'draft'
            })


        except Exception as e:
            raise UserError(e)


        return

    @api.multi
    def get_candidate_assessments_result(self):
        try:
            values = {}
            url = "https://api.hrpeak.com/AssessmentCenter/GetCandidateAssessments"


            params = {
                "candidateTrackingNumber": "279bb4ab-8a43-4aaa-8b65-fefea29ce65e"
            }
            headers = {"content-type": "application/json"}

            result = requests.get(url, params=params, headers=headers, auth=('wg2ujttuh', 'm6883ugpb')).json()
            candidate_assessment_results = result["Sets"][0]["Assessments"][0]["ReportLink"]

            self.write({
                'assessment_result_link': candidate_assessment_results,
                'state': 'done'
            })

        except Exception as e:
            raise UserError(e)

        return




class HrCandidateDegree(models.Model):
    _name = 'hr.recruitment.candidate.degree'
    name = fields.Char(string='Degree', required=True, translate=True)
    priority = fields.Integer(string='Priority', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', required=True, translate=True)
    level = fields.Integer(string='Level', required=True, translate=True)


class HrCandidateSchool(models.Model):
    _name = 'hr.recruitment.candidate.school'
    degree_id = fields.Many2one('hr.recruitment.candidate.degree', string='Degree ID', required=True)
    name = fields.Char(string='School', required=True, translate=True)

class HrCandidateFaculty(models.Model):
    _name = 'hr.recruitment.candidate.faculty'
    name = fields.Char(string='Faculty', required=True, translate=True)

class HrCandidateDepartment(models.Model):
    _name = 'hr.recruitment.candidate.department'
    faculty_id = fields.Many2one('hr.recruitment.candidate.faculty', string='Faculty ID', required=True)
    name = fields.Char(string='Department', required=True, translate=True)

class HrCandidateContactInfo(models.Model):
    _name = 'hr.recruitment.candidate.contact_info'

    candidate_id = fields.Many2one('hr.recruitment.candidate', string='Candidate', required=True)
    province = fields.Many2one('res.country', string='Province')
    town = fields.Many2one('res.country.state', string='Town')
    zip_code = fields.Char('Zip Code')
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    emergancy_name = fields.Char('Emergancy Contact Name')
    emergancy_surname = fields.Char('Emergancy Contact Surname')
    emergancy_degree = fields.Char('Emergancy Contact Degree')
    emergancy_phone = fields.Char('Emergancy Contact Phone Number')



class HrCandidate(models.Model):
    _name = 'hr.recruitment.candidate'
    _description = "Candidate"

    # history için gerekli...
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {
        'res.partner': 'partner_id'
    }

    partner_id = fields.Many2one('res.partner', string='Related Partner')
    active = fields.Boolean('Active', default=True)
    display_name = fields.Char('Display Name', compute='_compute_display_name')
    candidate_image = fields.Binary('Image', attachment=True, required=False)

    tckn = fields.Char('Turkish Identity Number', required=True)
    date_birth = fields.Date('Birth Date', required=False)
    location_birth = fields.Char('Birth Location')
    home_address = fields.Text('Home Address ')  # home_address Candidate içindeydi. Form kısmında sorun olaiblir.

    summary_information = fields.Text('Summary Information ')
    last_apply_date = fields.Date('Last Apply Date', required=False)

    nationality_id = fields.Many2one('res.country', string='Nationality')
    other_nationality_id = fields.Many2one('res.country', string='Other Nationality')

    attachment_number = fields.Integer(compute='_get_attachment_number', string="Number of Attachments")

    status = fields.Selection([('ise_alindi', 'İşe Alındı'),
                               ('surecte', 'Süreçte'),
                               ('havuz', 'Havuz'),
                               ('gorsumesi_olumsuz', 'Görüşmesi Olumsuz'),
                               ('kriterleri_saglamayan', 'Kriterleri Sağlamayan'),
                               ('kurum_yasakli', 'Kurum Yasaklı')],
                              string='Candidate Status')

    # interview kısmında bu alandan var. birleştirmek gerekebilir
    expected_salary_application = fields.Float('Expected Salary', required=True, size=2, digits=0)

    # state_id = fields.Many2one("res.country.state", string='State'  )
    # nationality = fields.Char('Name')  #ülke tablosundan çekilmeli

    hide = fields.Boolean(string='Hide', compute="_compute_hide")

    classification = fields.Char('Classification')  # şehir tablosundan çekilmeli

    gender = fields.Selection([('man', 'Man'),
                               ('woman', 'Woman'),
                               ('not_applicable', 'Not Applicable')],
                              string='Gender')

    driving_license = fields.Selection([('not_have', 'Not Have'),
                                        ('b', 'B'),
                                        ('c', 'C')],
                                       string='Driving License')
    disability_status = fields.Selection([('full', 'Full Disable'),
                                          ('partly', 'Partly Disable'),
                                          ('non', 'Non Disable')],
                                         string='Disability Status')

    disability_information = fields.Text('Disability Information')

    disability_category = fields.Selection([('neuro', 'Neurological'),
                                            ('ortho', 'Orthopedic'),
                                            ('uro', 'Urology')],
                                           string='Disability Status')

    disability_percentage = fields.Integer('Disability Percentage')

    blocking_illness = fields.Selection([('non_illness', 'No '),
                                        ('yes_illness', 'Yes')],
                                       string='blocking_illness')

    judicial_status = fields.Selection([('non_judicial', 'No '),
                                        ('yes_judicial', 'Yes')],
                                       string='Judicial Status')


    # firstname = fields.Char('Name')
    # lastname = fields.Char('Family name')
    work_type = fields.Selection([('bluecollar', 'Blue Collar'),
                                  ('whitecollar', 'White Collar')],
                                 string='Type', default='bluecollar')

    military_status = fields.Selection([('not_completed', 'Not Completed'),
                                        ('completed', 'Completed'),
                                        ('not_applicable', 'Not Applicable')],
                                       string='Military Status')



    marriage_status = fields.Selection([('married', 'Married '),
                                        ('divorced', 'Divorced'),
                                        ('single', 'Single')],
                                       string='Marriage Status')

    candidate_status = fields.Selection([('married', 'Married '),
                                         ('divorced', 'Divorced'),
                                         ('single', 'Single')],
                                        string='Marriage Status')

    applicant_ids = fields.One2many('hr.applicant', 'candidate_id', string='Applicants')

    experience_ids = fields.One2many('hr.recruitment.candidate.experience', 'candidate_id', string='Experience')

    education_ids = fields.One2many('hr.recruitment.candidate.education', 'candidate_id', string='Education')

    referance_ids = fields.One2many('hr.recruitment.candidate.referance', 'candidate_id', string='Referance',
                                    delegate=True)

    contact_info_ids = fields.One2many('hr.recruitment.candidate.contact_info', 'candidate_id', string='Contact Info',
                                       delegate=True)

    exam_ids = fields.One2many('hr.recruitment.candidate.exam', 'candidate_id', string='Exam')

    other_exam_ids = fields.One2many('hr.recruitment.candidate.other_exams', 'candidate_id', string='Other Exams')

    internship_ids = fields.One2many('hr.recruitment.candidate.internship', 'candidate_id', string='Internship')

    knowledge_ids = fields.One2many('hr.recruitment.candidate.knowledge', 'candidate_id', string='Knowledge')

    cources_ids = fields.One2many('hr.recruitment.candidate.course', 'candidate_id', string='Course')

    visitor_system_record_ids = fields.One2many('hr.recruitment.candidate.referance', 'candidate_id', string='Visitor')

    #todo daha sonra düzeltilecek
    # last_experience_name = fields.Char('Last Experience Name', compute='_compute_last_exp_name')

    last_edu_name = fields.Char('Last Education Name', compute='_compute_last_edu_name')

    enterprise_qualification_exams = fields.One2many('hr.recruitment.candidate.hrenterprisequalificationexams',
                                                     'candidate_id', string='Enterprise Qualification Exams')



    @api.multi
    def _get_attachment_number(self):
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'hr.recruitment.candidate'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attach_data = dict((res['res_id'], res['res_id_count']) for res in read_group_res)
        for record in self:
            record.attachment_number = attach_data.get(record.id, 0)

    # @api.multi
    # def _compute_last_exp_name(self):
    #     for candidate in self:
    #         exp = self.env['hr.recruitment.candidate.experience'].search([('candidate_id', '=', candidate.id)],
    #                                                                      order='date_to desc')
    #         if len(exp) > 0:
    #             candidate.last_experience_name = exp[0].company_name + ' ' + str(exp[0].date_from.month) + '/' + str(
    #                 exp[0].date_from.year) + '-' + \
    #                                              str(exp[0].date_to.month) + '/' + str(exp[0].date_to.year)

    # education ekranı tamamlandıktan sonra school_id den degree ye göre max okul getirilmeli
    @api.multi
    def _compute_last_edu_name(self):
        for candidate in self:
            edu = self.env['hr.recruitment.candidate.education'].search([('candidate_id', '=', candidate.id)])

            max_edu_list = []
            if len(edu) > 0:
                candidate.last_edu_name = self._get_max_degree(edu)

    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        action['search_view_id'] = (self.env.ref('hr_recruitment.ir_attachment_view_search_inherit_hr_recruitment').id,)
        return action

    def _get_max_degree(self, education_list):
        highest_degree = 0
        for education in education_list:
            if education.degree.priority > highest_degree:
                highest_degree = education.degree.priority

        max_edu_list = []
        for education in education_list:
            if education.degree.priority == highest_degree:
                max_edu_list.append(education)

        return self._create_max_edu_string(max_edu_list)

    def _create_max_edu_string(self, max_edu_list):
        max_edu_string_list = []
        for edu in max_edu_list:
            max_edu_string_list.append(edu.school_id.name + '(' + edu.school_department_id.name + ')')
        return ', '.join(max_edu_string_list)

    # üstteki düzeltilecek, servis çağrılacak....

    @api.multi
    def _compute_display_name(self):
        for candidate in self:
            candidate.display_name = '%s %s' % (candidate.firstname or '', candidate.lastname or '')
            # candidate.display_name = candidate.firstname +'- '+ candidate.lastname

    # @api.onchange('tckn','firstname','lastname','date_birth')
    # def _onchange_tckn(self):
    #
    #     if self.tckn and self.date_birth and self.firstname and self.lastname:
    #
    #         res = self.env['kps.service'].validate_tckn(self.tckn, self.firstname, self.lastname, self.date_birth.year)
    #
    #         if not res:
    #             raise Warning(u'Kimlik bilgileriniz hatalı')

    @api.onchange('country_id')
    def _onchange_country_id(self):
        self.state_id = False
        if self.country_id:
            return {'domain': {'state_id': [('country_id', '=', self.country_id.id)]}}
        else:
            return {'domain': {'state_id': []}}

    # Show Hide State selection based on Country
    @api.depends('country_id')
    def _compute_hide(self):
        if self.country_id:
            self.hide = False
        else:
            self.hide = True

    # @api.onchange('phone')
    # def _onchange_phone_validation(self):
    #     if self.phone:
    #         match = re.match('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', self.phone)
    #         if match == None:
    #             raise ValidationError('Not a valid Phone Number')

    # @api.onchange('phone')
    # def _onchange_phone_validation(self):
    #     if self.phone:
    #         if not str(self.phone).isDigit(self.phone):
    #             raise ValidationError('Not a valid Phone Number')
    #
    # @api.onchange('email')
    # def validate_mail(self):
    #     if self.email:
    #         match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
    #         if match == None:
    #             raise ValidationError('Not a valid E-mail')

    @api.onchange('disability_status')
    def _onchange_disability_status(self):
        self.disability_percentage = False

    # #furkan
    # @api.onchange('date_birth')
    # def _onchange_date_check(self):
    #     if str(self.date_birth )> datetime.today().strftime('%Y-%m-%d'):
    #         raise ValidationError('Birth date can not be greater than current day')




