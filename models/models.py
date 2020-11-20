# -*- coding: utf-8 -*-

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
        'demo.sh5000.show',  # related model
        'super_id',  # field for "this" on related model
        string='Show 5000 by Supervisor')


class sh5000(models.Model):
    _name = 'demo.sh5000.show'
    _description = 'sh5000 show - step by step'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # track_visibility

    name = fields.Char('the Name', required=True)
    mobile = fields.Char('Mobile No.')
    dzz = fields.Char('Company')
    biryear = fields.Char('Birth Year')
    education = fields.Char('Education')

    # track_visibility='always' 和 track_visibility='onchange'

    is_done_track_onchange = fields.Boolean(
        string='Is Done?', default=False, track_visibility='onchange')

    name_track_always = fields.Char(
        string="track_name", track_visibility='always')

    super_id = fields.Many2one(
        'demo.supervisor', String='the Supervisor', required='True')

    tag_ids = fields.Many2many(
        'demo.tag', 'demo_5000_tag', 'demo_5000_id', 'tag_id', string='Tages')

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100

    start_datetime = fields.Datetime(
        'Start DateTime', default=fields.Datetime.now())
    stop_datetime = fields.Datetime(
        'End Datetime', default=fields.Datetime.now())

    field_onchange_demo = fields.Char('onchange_demo')
    field_onchange_demo_set = fields.Char('onchange_demo_set', readonly=True)

    # float digits
    # field tutorial
    input_number = fields.Float(string='input number', digits=(10, 3))
    field_compute_demo = fields.Integer(
        compute="_get_field_compute")  # readonly

    # _sql_constraints = [
    #     ('name_uniq', 'unique(name)', 'Description must be unique'),
    # ]

    @api.constrains('start_datetime', 'stop_datetime')
    def _check_date(self):
        for data in self:
            if ((not data.start_datetime) or (not data.stop_datetime)):
                raise ValidationError(
                    "(1)datetime must not be NULL"
                )
            elif (data.start_datetime > data.stop_datetime):
                raise ValidationError(
                    "(2)data.stop_datetime  > data.start_datetime"
                )

            # if data.start_datetime > data.stop_datetime:
            #     raise ValidationError(
            #         "data.stop_datetime  > data.start_datetime"
            #     )

    # @api.depends('input_number')
    @api.depends('biryear')
    def _get_field_compute(self):

        for data in self:
            data.field_compute_demo = 2021 - int(data.biryear)

        # for data in self:
        #     data.field_compute_demo = data.input_number * 1000

    @api.onchange('field_onchange_demo')
    def onchange_demo(self):
        if self.field_onchange_demo:
            self.field_onchange_demo_set = 'set {}'.format(
                self.field_onchange_demo)
