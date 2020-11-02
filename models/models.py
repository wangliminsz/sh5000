#-*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class DemoTag(models.Model):
    _name = 'demo.tag'
    _description = 'Demo Tags'

    name = fields.Char(string='Tag Name', index=True, required=True)
    active = fields.Boolean(default=True, help="Set active.")

class DemoSupervisor(models.Model):
    _name = 'demo.supervisor'
    _description = 'Demo Supervisor'

    name = fields.Char(string='Supervisor Name', index=True, required=True)

    # One2many is a virtual relationship, there must be a Many2one field in the other_model,
    # and its name must be related_field

    sh5000_line_ids = fields.One2many(
        'demo.sh5000.show', # related model
        'super_id', # field for "this" on related model
        string='Show 5000 by Supervisor')

class sh5000(models.Model):
    _name = 'demo.sh5000.show'
    _description = 'sh5000 show - step by step'

    name = fields.Char('the Name', required=True)
    mobile = fields.Char('Mobile No.')
    dzz = fields.Char('Company')
    biryear = fields.Char('Birth Year')
    education = fields.Char('Education')

    super_id = fields.Many2one('demo.supervisor', String='the Supervisor',required='True')

    tag_ids = fields.Many2many('demo.tag', 'demo_5000_tag', 'demo_5000_id', 'tag_id', string='Tages')

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100



    
   

