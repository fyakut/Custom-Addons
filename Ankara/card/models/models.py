# -*- coding: utf-8 -*-

from odoo import models, fields

class Movement(models.Model):
    _name = 'card.movement'

    trackDateTime = fields.Datetime(string="Track Time")

    device_id = fields.Many2one('card.device', string="Device")

class Device(models.Model):
    _name = 'card.device'

    ip_address = fields.Char(string="Ip Address")
    direction = fields.Char(string="3 Selection")

    device_id = fields.One2many('card.movement', 'device_id', string="Movement")
