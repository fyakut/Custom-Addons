# -*- encoding: utf-8 -*-
#
#Created on May 29, 2019
#
#@author: dogan
#
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError



class HrInterviewQuestions(models.Model):
    _name = 'hr.interview.questions'

    interview_type = fields.Selection([('hr', 'HR'),
                                        ('technical', 'Technical'),
                                        ('language', 'Language'),
                                        ('referance', 'Referance')], string='Interview Type')

    question_definition = fields.Text('Question Definition')





class HrInterviewQuestionAnswer(models.Model):
    _name = 'hr.interview.question.answer'

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done')], string='State')

    question_definition = fields.Text('Question Definition')

    question_answer = fields.Text('Question Answer')

    interviewer_id = fields.Many2one('hr.interview.interviewer', string='Interviewer', required=True)

    name = fields.Char('Question', default='Question')

    @api.onchange('question_definition')
    def _question_definition_change(self):
        self.name = self.question_definition

    @api.onchange('question_answer')
    def _question_answer_change(self):
        self.state = 'done'
        interviewer = self.interviewer_id.id

        questions = self.env['hr.interview.question.answer'].search(
            [('interviewer_id' , '=', interviewer),('state', '!=', 'done')])
        if len(questions) == 1:
            self.interviewer_id.write({'state': 'done'})


class HrInterviewInterviewer(models.Model):
    _name = 'hr.interview.interviewer'

    state = fields.Selection([('draft', 'Draft'),
                              ('planned', 'Planned'),
                              ('done', 'Done')], string='State', default='draft')

    final_evaluation = fields.Selection([('very_good', 'Very Good'),
                              ('good', 'Good'),
                              ('not_bad', 'Not Bad')], string='Final Evaluation')

    final_evaluation_comment = fields.Text('Comment')

    interview_id = fields.Many2one('hr.interview',string='Interview')

    user_id = fields.Many2one('res.users', string='Interviewer')
    # , search = 'interviewers_search'

    interview_questions_answer = fields.One2many('hr.interview.question.answer', 'interviewer_id', string='Questions')

    @api.onchange('user_id')
    def _user_id_change(self):
        self.state = 'draft'

    #
    #
    # def interviewers_search(self, operator, operand):
    #     current_user = self.user_id
    #     interviewers_search = self.env['hr.interview.interviewer'].search(
    #         [('user.id', '=', current_user)]).ids
    #     return [(interviewers_search, '=', id)]


    @api.multi
    def send_interview(self):
        try:
            questions = self.env['hr.interview.questions'].search(
                [('interview_type', '=', self.interview_id.interview_type)])

            interviewer_id = self.id

            for question in questions:
                self.env['hr.interview.question.answer'].create({
                    'state': 'draft',
                    'question_definition': question.question_definition,
                    'name': 'Question',
                    'interviewer_id' : interviewer_id })

            self.state = 'planned'

        except Exception as e:
            raise UserError(e)

    @api.multi
    def complete_evaluation(self):

        interviewer = self.id
        self_interviewer = self

        questions = self.env['hr.interview.question.answer'].search(
            [('interviewer_id', '=', interviewer), ('state', '!=', 'done')])
        if len(questions) == 0:
            if not self.final_evaluation:
                import warnings
                warnings.warn("Please complete final evaluation.",
                              PendingDeprecationWarning, stacklevel=2)
            else:
                self_interviewer.write({'state': 'done'})

        else:
            # import warnings
            # warnings.warn("Please complete questions first.",
            #               PendingDeprecationWarning, stacklevel=2)

            return {

                'warning': {

                    'title': 'Warning!',

                    'message': 'The warning text'}

            }
        return





class HrInterview(models.Model):
    _name = 'hr.interview'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    interview_type = fields.Selection([('hr', 'HR'),
                                        ('technical', 'Technical'),
                                        ('language', 'Language'),
                                        ('referance', 'Referance')], string='Type')


    applicant_id = fields.Many2one('hr.applicant', string='Application')

    interviewer_ids = fields.One2many('hr.interview.interviewer', 'interview_id', string='Interviewers')


    question_ids = fields.One2many('hr.interview.questions', 'interview_type', string='Questions')


    state = fields.Selection([('draft','Draft'),
                              ('planned','Planned'),
                              ('done','Done'),
                              ('cancel','Cancel')],string='State', default='draft')



    date_start = fields.Datetime('Starts at', required=True)

    responsible_id = fields.Many2one('res.users', string='HR Responsible', required=True)

    name = fields.Char("Interview")




    expected_salary = fields.Monetary('Expected Salary')
    currency_id = fields.Many2one('res.currency', string='Currency')


    # @api.onchange('date_start')
    # def _date_start_change(self):
    #
    #     date_start = self.date_start
    #     # Mail gönderimi
    #     interviewers = self.interviewer_ids
    #
    #     notification_template = self.env.ref('hr_recruitment_tai.email_template_interview_create_notification_applicant')
    #     if notification_template:
    #         for interviewer in interviewers:
    #             notification_template.sudo().send_mail(interviewer.id, force_send=False)
    #     return

    @api.multi
    def send_mail_to_interviewers(self):
        try:

            interviewers = self.interviewer_ids

            notification_template = self.env.ref(
                'hr_recruitment_tai.email_template_interview_create_notification_interviewers')
            if notification_template:
                for interviewer in interviewers:
                    notification_template.sudo().send_mail(interviewer.id, force_send=False)

        except Exception as e:
            raise UserError(e)

        return

    @api.multi
    def send_mail_to_candidate(self):
        try:

            interview = self
            notification_template = self.env.ref(
                'hr_recruitment_tai.email_template_interview_create_notification_candidate')
            if notification_template:
                notification_template.sudo().send_mail(interview.id, force_send=False)


        except Exception as e:
            raise UserError(e)

        return





    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.interview') or '/'
        scrap = super(HrInterview, self).create(vals)

        return scrap

    @api.multi
    def action_plan(self):
        self.write({'state':'planned'})

    @api.multi
    def action_done(self):
        self.write({'state': 'done'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def get_ilan(self):
        res = self.env['kps.service'].get_ilan()

