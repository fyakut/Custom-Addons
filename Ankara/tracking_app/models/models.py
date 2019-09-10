# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools
from odoo.modules.module import get_module_resource


class Movement(models.Model):
    _name = 'tracking.movement'

    trackDateTime = fields.Datetime(string="Track Date Time", default=fields.Datetime.now)

    device_id = fields.Many2one('tracking.device', string="Device")
    object_id = fields.Many2one('tracking.deviceobject', string="Device Object")


class Device(models.Model):
    _name = 'tracking.device'

    device_type = fields.Char(string="Device Type")
    ip_address = fields.Char(string="Ip Address")
    fixed_asset_no = fields.Char(string="Fixed Asset No")
    direction_type = fields.Char(string="Device Direction")
    description = fields.Text(string="Description")

    movement_ids = fields.One2many('tracking.movement', 'device_id', string="Movement")
    location_id = fields.Many2one('tracking.location', string="Location")

    # the following code concatenates many2one fields on a single record
    @api.multi
    def name_get(self):
        result = []

        for record in self:
            name = record.ip_address + ', ' + record.direction_type
            result.append((record.id, name))
        return result


class Location(models.Model):
    _name = 'tracking.location'

    name = fields.Char(string="Location Name")

    device_ids = fields.One2many('tracking.device', 'location_id', string="Device")
    authorization_ids = fields.One2many('tracking.authorization', 'location_id', string="Authorization")


class DeviceObject(models.Model):
    _name = 'tracking.deviceobject'

    name = fields.Char(string="Device Object Name")
    iot_code = fields.Char(string="IOT Code")
    _sql_constraints = [
        ('tracking_deviceobject_uq',  # Constraint unique identifier
         'UNIQUE (iot_code)',  # Constraint SQL syntax
         'IOT Code must be unique'),  # Message
    ]
    movement_ids = fields.One2many('tracking.movement', 'object_id', string="Movement")
    authorization_ids = fields.One2many('tracking.authorization', 'object_id', string="Authorization")
    user_id = fields.Many2one('res.users', 'User', store=True, readonly=False)

    # partner_id = fields.Many2one(
    #     'res.partner',
    #     delegate=True,
    #     ondelete='cascade',
    #     required=True)


class Authorization(models.Model):
    _name = 'tracking.authorization'

    expire_date = fields.Datetime(string='Expiry Date')

    object_id = fields.Many2one('tracking.deviceobject', required=True, string="IOT Code")
    location_id = fields.Many2one('tracking.location', required=True, string="Location")
