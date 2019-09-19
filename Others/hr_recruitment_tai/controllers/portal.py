# -*- coding: utf-8 -*-
import base64

from odoo.http import Controller, request, route

from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment

from werkzeug.exceptions import NotFound
import logging
import werkzeug

from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import UserError
from odoo.http import request
import xmlrpc.client
from datetime import datetime
import requests
import json
import random

RESUME_TEMPLATES = {'step1':'hr_recruitment_tai.portal_my_resume_step1',
                    'step2':'hr_recruitment_tai.portal_my_resume_step2',
                    'step3':'hr_recruitment_tai.portal_my_resume_step3',
                    'step4':'hr_recruitment_tai.portal_my_resume_step4',
                    'step5':'hr_recruitment_tai.portal_my_resume_step5',
                    'step6':'hr_recruitment_tai.portal_my_resume_step6',
                    'step7':'hr_recruitment_tai.portal_my_resume_step7',
                    'step8':'hr_recruitment_tai.portal_my_resume_step8',
                    'step9':'hr_recruitment_tai.portal_my_resume_step9',
                    'step10':'hr_recruitment_tai.portal_my_resume_step10',
                    'step11':'hr_recruitment_tai.portal_my_resume_step11',
                    'step12':'hr_recruitment_tai.portal_my_resume_step12',
                    'step13':'hr_recruitment_tai.portal_my_resume_step13'

                    }


_logger = logging.getLogger(__name__)

class WebsiteHrRecruitmentInherit(WebsiteHrRecruitment):

    @route('''/jobs/apply/<model("hr.job", "[('website_id', 'in', (False, current_website_id))]"):job>''',
                type='http', auth="public", website=True)
    def jobs_apply(self, job, **kwargs):
        if not job.can_access_from_current_website():
            raise NotFound()

        error = {}
        default = {}
        if 'website_hr_recruitment_error' in request.session:
            error = request.session.pop('website_hr_recruitment_error')
            default = request.session.pop('website_hr_recruitment_default')

        if request.env.user._is_public():
            request.redirect('/web/login')

        candidate = request.env.user.candidate_id
        # create application
        can_apply, reasons = job.can_apply()

        # alternatif 1
        #if reason == 'missing_resume':
        #    return request.render('hr_recruitment_tai.missing_resume', {candidate: candidate})

        # alternatif 2
        if not can_apply:
            existing_app = None

            #if reason == APPLICATION_FAIL_INSUFFICIENT_CV:
            #    existing_app = request.env['hr.applicant'].sudo().search([('candidate_id','=', candidate.id),
            #                                                              ('job_id','=', job.id)])

            return request.render('hr_recruitment_tai.application_fail', {'candidate': candidate,
                                                                        'job':job,
                                                                        'reasons':reasons,
                                                                        'existing_app': existing_app})


        new_app = request.env['hr.applicant'].sudo().create({'candidate_id': candidate.id,
                                                   'name': job.name,
                                                   'job_id':job.id,
                                                   'partner_name':request.env.user.name})

        return request.render('hr_recruitment_tai.application_success', {'application': new_app})


    @route('''/jobs/withdraw/<model("hr.job", "[('website_id', 'in', (False, current_website_id))]"):job>''',
                type='http', auth="public", website=True)
    def jobs_withdraw(self, job, **kwargs):
        if not job.can_access_from_current_website():
            raise NotFound()

        if request.env.user._is_public():
            request.redirect('/web/login')

        candidate = request.env.user.candidate_id
        existing_app = request.env['hr.applicant'].sudo().search([('candidate_id','=', candidate.id),
                                                                    ('job_id','=', job.id)])
        existing_app.write({'active': False})

        return request.render('hr_recruitment_tai.application_withdraw', {'application': existing_app})



class AuthSignupHome(Home):

    @route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if request.httprequest.method == 'POST':
            tcknChbx  = qcontext.get('tckn_chbx')
            tckn      = qcontext.get('tckn')
            birthdate = qcontext.get('birthdate')
            name      = qcontext.get('name')

            if tcknChbx=='on' and len(tckn)>0:
                res = request.env['kps.service'].validate_tckn(tckn, name, birthdate)
                if not res:
                    qcontext["error"] = _("Turkish Public Identification Number Verification Error!")
            if tcknChbx == 'on' and len(tckn)==0:
                qcontext["error"] = _("Please fill out Tckn No")

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

class ResumeController(Controller):

    @route(['/my/resume/deneme'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        print("deneme")


    @route(['/my/resume',
            '/my/resume/<string:step>'], type='http', auth='user', website=True)
    def account(self, redirect=None, step='step1', **post):
        values = {}

        # url = 'http://localhost:8069'
        # db = 'odoo'
        # username = 'admin'
        # password = 'admin'
        # common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        # uid = common.authenticate(db, username, password, {})
        # models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)

        partner = request.env.user.partner_id
        attachments = request.env['ir.attachment'].sudo().search([])
        candidate = request.env['hr.recruitment.candidate'].sudo().search([('partner_id','=',partner.id)], limit=1)
        referance = request.env['hr.recruitment.candidate.referance'].sudo().search([('candidate_id', '=', candidate.id)])
        experience = request.env['hr.recruitment.candidate.experience'].sudo().search([('candidate_id', '=', candidate.id)])
        internship = request.env['hr.recruitment.candidate.internship'].sudo().search([('candidate_id', '=', candidate.id)])
        contact_info = request.env['hr.recruitment.candidate.contact_info'].sudo().search([('candidate_id', '=', candidate.id)])
        education = request.env['hr.recruitment.candidate.education'].sudo().search([('candidate_id', '=', candidate.id)])
        eng_exam = request.env['hr.recruitment.candidate.exam'].sudo().search([('candidate_id', '=', candidate.id)])
        other_exam = request.env['hr.recruitment.candidate.other_exams'].sudo().search([('candidate_id', '=', candidate.id)])



        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        degrees = request.env['hr.recruitment.candidate.degree'].sudo().search([])
        schools = request.env['hr.recruitment.candidate.school'].sudo().search([])
        facultys = request.env['hr.recruitment.candidate.faculty'].sudo().search([])
        departments = request.env['hr.recruitment.candidate.department'].sudo().search([])
        sch_provinces = request.env['res.country.state'].sudo().search([('country_id', '=', 224)])
        exams = request.env['hr.recruitment.exam'].sudo().search([])

        values.update({
            'error': {},
            'error_message': [],
            'step': step,
            'page_name': 'my_resume',
            'candidate': candidate,
            'education': education,
            'degrees': degrees,
            'schools': schools,
            'facultys': facultys,
            'departments': departments,
            'sch_provinces': sch_provinces,
            'contact_info': contact_info,
            'countries': countries,
            'states': states,
            'referances':referance,
            'experience':experience,
            'internship':internship,
            'attachments':attachments,
            'eng_exam':eng_exam,
            'other_exam': other_exam,
            'exams':exams
        })

        #insert ve delete yapılacak
        if request.httprequest.method == 'POST':
            candidate.sudo().write(post)
            #candidate.write({'referance_ids': [(0, False, {'candidate_id': candidate.id,
            #                                               'name': post["referance.name"],
            #                                               'surname': post["referance.surname"],
            #                                                'company': post["referance.company"],
            #                                                'duty': post["referance.duty"],
            #                                                'phone': post["referance.phone"],
            #                                                'is_relative': post.get('referance.is_relative', False),
            #                                                'relationship_degree': post.get(
            #                                                 "referance.relationship_degree", False)})]})
            # parameters = {
            #     'candidate_id': candidate.id,
            #     'name': post["referance.name"],
            #     'surname': post["referance.surname"],
            #     'company': post["referance.company"],
            #     'duty': post["referance.duty"],
            #     'phone': post["referance.phone"],
            #     'is_relative': post["referance.is_relative"],
            #     'relationship_degree': post["referance.relationship_degree"]
            # }
            # models.execute_kw(db, uid, password, 'hr.recruitment.candidate.referance', 'create', [parameters])

            # return request.redirect('/my/home')



        if step == 'step1':
            values.update({

            })
            #hocanın mail ile gönderdiği kod
            # if 'file' in values:
            #
            #     for c_file in request.httprequest.files.getlist('file'):
            #         data = c_file.read()
            #
            #         if c_file.filename:
            #             request.env['ir.attachment'].sudo().create({
            #                 'name': c_file.filename,
            #                 'datas': base64.b64encode(data),
            #                 'datas_fname': c_file.filename,
            #                 'res_model': 'service.desk.ticket',
            #                 'res_id': new_ticket_id.id
            #             })

            # for i in attachments:

            # print(i["res_id"])
            # if request.httprequest.method == 'POST':
            #     if 'file' in post:
            #
            #         for c_file in request.httprequest.files.getlist('file'):
            #             data = c_file.read()
            #
            #             if c_file.filename:
            #                 request.env['ir.attachment'].sudo().create({
            #                     'name': c_file.filename,
            #                     'datas': base64.b64encode(data),
            #                     'datas_fname': c_file.filename,
            #                     'res_model': 'hr.recruitment.candidate',
            #                     'res_id': candidate.id
            #                 })

            if request.httprequest.method == 'POST':

                candidate.sudo().write(post)
                return request.redirect('/my/resume/step2')

        elif step == 'step2':
            values.update({

            })

            if request.httprequest.method == 'POST':
                candidate.sudo().write(post)
                return request.redirect('/my/resume/step3')

        elif step == 'step3':
            values.update({

            })

            if request.httprequest.method == 'POST':
                candidate.sudo().write(post)
                return request.redirect('/my/resume/step4')

        elif step == 'step4':
            values.update({


            })

            if request.httprequest.method == 'POST':
            #for insert
                if candidate.id != contact_info.candidate_id["id"]:

                    candidate.sudo().write({'contact_info_ids': [(0, False, {'candidate_id': candidate.id,
                                                                             'province': post["contact_info.province"],
                                                                             'town': post["contact_info.town"],
                                                                             'zip_code': post["contact_info.zip_code"],
                                                                             'email': post["contact_info.email"],
                                                                             'phone': post["contact_info.phone"],
                                                                             'emergancy_name': post.get(
                                                                                 'contact_info.emergancy_name', False),
                                                                             'emergancy_surname': post.get(
                                                                                 "contact_info.emergancy_surname", False),
                                                                             'emergancy_degree': post.get(
                                                                                 "contact_info.emergancy_degree", False),
                                                                             'emergancy_phone': post.get(
                                                                                 "contact_info.emergancy_phone", False)
                                                                             })]})
                    return request.redirect('/my/resume/step5')

                # for update
                else:
                    candidate.sudo().write({'contact_info_ids': [(1, contact_info["id"], {
                        'province': post["contact_info.province"],
                        'town': post["contact_info.town"],
                        'zip_code': post["contact_info.zip_code"],
                        'email': post["contact_info.email"],
                        'phone': post["contact_info.phone"],
                        'emergancy_name': post.get(
                            'contact_info.emergancy_name', False),
                        'emergancy_surname': post.get(
                            "contact_info.emergancy_surname",
                            False),
                        'emergancy_degree': post.get(
                            "contact_info.emergancy_degree",
                            False),
                        'emergancy_phone': post.get(
                            "contact_info.emergancy_phone", False)
                    })]})

                    return request.redirect('/my/resume/step5')


        elif step == 'step5':
            values.update({

            })

            if request.httprequest.method == 'POST':
                candidate.sudo().write(post)
                return request.redirect('/my/resume/step6')

        elif step == 'step6':
            values.update({

            })

            if request.httprequest.method == 'POST':

                if candidate.id != education.candidate_id["id"]:

                    candidate.sudo().write({'education_ids': [(0, False, {'candidate_id': candidate.id,
                                                                          'degree': post["education.degree"],
                                                                          'school_id': post["education.school_id"],
                                                                          'faculty_id': post["education.faculty_id"],
                                                                          'school_department_id': post["education.school_department_id"],
                                                                          'school_province': post["education.school_province"],
                                                                          'date_from': post["education.date_from"],
                                                                          'date_to': post["education.date_to"],
                                                                          'graduation_score': post["education.graduation_score"]

                                                                             })]})
                    return request.redirect('/my/resume/step7')

                else:
                    candidate.sudo().write({'education_ids': [(1, education["id"], {
                        'degree': post["education.degree"],
                        'school_id': post["education.school_id"],
                        'faculty_id': post["education.faculty_id"],
                        'school_department_id': post["education.school_department_id"],
                        'school_province': post["education.school_province"],
                        'date_from': post["education.date_from"],
                        'date_to': post["education.date_to"],
                        'graduation_score': post["education.graduation_score"]

                    })]})

                    return request.redirect('/my/resume/step7')


        elif step == 'step7':
            values.update({
            })

            if request.httprequest.method == 'POST':
                return request.redirect('/my/resume/step8')

        elif step == 'step8':
            values.update({
            })

            if request.httprequest.method == 'POST':

                if candidate.id != eng_exam.candidate_id["id"]:

                    candidate.sudo().write({'exam_ids': [(0, False, {'candidate_id': candidate.id,
                                                                     'eng_level': post["eng_exam.eng_level"],
                                                                     'eng_exam_name': post["eng_exam.eng_exam_name"],
                                                                     'eng_exam_score': post["eng_exam.eng_exam_score"],
                                                                     'eng_exam_date': post["eng_exam.eng_exam_date"],

                                                                             })]})

                else:
                    candidate.sudo().write({'exam_ids': [(1, eng_exam["id"], {
                                                                     'eng_level': post["eng_exam.eng_level"],
                                                                     'eng_exam_name': post["eng_exam.eng_exam_name"],
                                                                     'eng_exam_score': post["eng_exam.eng_exam_score"],
                                                                     'eng_exam_date': post["eng_exam.eng_exam_date"],

                                                                     })]})


                if candidate.id != other_exam.candidate_id["id"]:


                    candidate.sudo().write({'other_exam_ids': [(0, False, {'candidate_id': candidate.id,
                                                                           'other_lang_name': post["other_exam.other_lang_name"],
                                                                           'other_exam_level': post["other_exam.other_exam_level"]
                                                                           })]})

                else:

                    candidate.sudo().write({'other_exam_ids': [(1, other_exam["id"], {
                        'other_lang_name': post["other_exam.other_lang_name"],
                        'other_exam_level': post["other_exam.other_exam_level"]
                    })]})





                return request.redirect('/my/resume/step9')

        elif step == 'step9':
            values.update({
            })

            if request.httprequest.method == 'POST':

                if candidate.id != experience.candidate_id["id"]:

                    candidate.sudo().write({'experience_ids': [(0, False, {'candidate_id': candidate.id,
                                                                          'company_name': post["experience.company_name"],
                                                                          'position': post["experience.position"],
                                                                          'responsibilities': post["experience.responsibilities"],
                                                                          'type': post["experience.type"],
                                                                          'reason_for_leaving': post["experience.reason_for_leaving"],
                                                                          'date_from': post["experience.date_from"],
                                                                          'date_to': post["experience.date_to"],
                                                                          'is_current': post["experience.is_current"],
                                                                          'employer': post["experience.employer"],
                                                                          'employer_company': post["experience.employer_company"],
                                                                          'employer_duty': post["experience.employer_duty"],
                                                                          'employer_phone_number': post["experience.employer_phone_number"]
                                                                             })]})


                else:
                    candidate.sudo().write({'experience_ids': [(1, experience["id"], {
                          'company_name': post["experience.company_name"],
                          'position': post["experience.position"],
                          'responsibilities': post["experience.responsibilities"],
                          'type': post["experience.type"],
                          'reason_for_leaving': post["experience.reason_for_leaving"],
                          'date_from': post["experience.date_from"],
                          'date_to': post["experience.date_to"],
                          'is_current': post["experience.is_current"],
                          'employer': post["experience.employer"],
                          'employer_company': post["experience.employer_company"],
                          'employer_duty': post["experience.employer_duty"],
                          'employer_phone_number': post["experience.employer_phone_number"]

                    })]})

                return request.redirect('/my/resume/step13')

        elif step == 'step10':
            values.update({
            })

            if request.httprequest.method == 'POST':
                return request.redirect('/my/resume/step11')

        elif step == 'step11':
            values.update({
            })

            if request.httprequest.method == 'POST':

                candidate.sudo().write(post)
                return request.redirect('/my/resume/step12')

        elif step == 'step12':
            values.update({

            })

            if request.httprequest.method == 'POST':
                return request.redirect('/my/home')

            # TODO form onaylama kontrolleri yapılacak

        elif step == 'step13':
            values.update({
            })

            if request.httprequest.method == 'POST':

                if candidate.id != education.candidate_id["id"]:

                    candidate.sudo().write({'referance_ids': [(0, False, {'candidate_id': candidate.id,
                                                                          'name': post["referance.name"],
                                                                          'surname': post["referance.surname"],
                                                                          'duty': post["referance.duty"],
                                                                          'company': post["referance.company"],
                                                                          'phone': post["referance.phone"],
                                                                          'is_relative': post["referance.is_relative"],
                                                                          'relationship_degree': post["referance.relationship_degree"]
                                                                             })]})



                else:
                    for i in referance:
                        candidate.sudo().write({'referance_ids': [(1, i["id"], {
                            'name': post["referance.name"],
                            'surname': post["referance.surname"],
                            'duty': post["referance.duty"],
                            'company': post["referance.company"],
                            'phone': post["referance.phone"],
                            'is_relative': post["referance.is_relative"],
                            'relationship_degree': post["referance.relationship_degree"]

                        })]})

                return request.redirect('/my/resume/step10')


        template = RESUME_TEMPLATES.get(step, 'step1')
        response = request.render(template ,values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


    @route(['/my/resume/update_referance'], type='json', auth='user', website=True)
    def update_create_referance(self, ref_id=None, **args):
        data = args
