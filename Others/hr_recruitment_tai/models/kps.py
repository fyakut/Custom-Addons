
import suds.client
from odoo import models, api

# from suds.transport import TransportError
# from suds.transport.http import HttpAuthenticated
# raise ImportError('Install suds library!')
# from suds import WebFault
# from odoo.exceptions import ValidationError
# from datetime import datetime
# import json

# import os, ssl
#
# if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
#         getattr(ssl, '_create_unverified_context', None)):
#     ssl._create_default_https_context = ssl._create_unverified_context


class KPS(models.AbstractModel):
    _name = 'kps.service'

    @api.model
    def validate_tckn(self, tckn, name, birth_year):

        try:
            endpoint = 'https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL'
            client = suds.client.Client(endpoint)

            param = client.factory.create('tns:TCKimlikNoDogrula')

            parts = name.strip().split(" ")

            if len(parts) > 1:
                firstname = ''
                for i, part in enumerate(parts):
                    if( i != len(parts)-1) :
                        firstname = firstname + " " + part
                lastname  = parts[len(parts)-1]
            else :
                return False

            param.TCKimlikNo = tckn
            param.Ad = firstname.strip().upper()
            param.Soyad = lastname.upper()
            param.DogumYili = birth_year[0:4]

            res = client.service.TCKimlikNoDogrula(param)

        except :
            res = False

        return res




    # @api.model
    # def get_ilan(self):
    #     endpoint = 'https://taiextuygtest1.tai.com.tr/WATS/IseAlimService?wsdl'
    #
    #     client = Client(endpoint)
    #
    #     data = client.service.getIlan()
    #
    #     company_id = 1
    #     state = "recruit"
    #     user_id = 1
    #     create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     address_id = 1
    #     is_published = True
    #
    #     self.env['hr.job'].search([]).unlink()
    #
    #     jsondata = json.loads(data)
    #     for job in jsondata:
    #         parameters = {
    #             'name': job["adi"],
    #             'description': job["aciklama"],
    #             'department_id': job["birimkodu"],
    #             'company_id': company_id,
    #             'state': state,
    #             'create_uid': user_id,
    #             'create_date': create_date,
    #             'write_uid': user_id,
    #             'write_date': create_date,
    #             'address_id': address_id,
    #             'is_published': is_published
    #         }
    #         self.env['hr.job'].create(parameters)




