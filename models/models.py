# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)


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

# #@api.multi
    def add_demo_5000_record(self):
        # (0, _ , {'field': value}) creates a new record and links it to this one.

        # data_1 = self.env.ref(
        #     'sh5000.demo_5000_data_1')

        tag_data_1 = self.env.ref('sh5000.demo_tag_001')
        tag_data_2 = self.env.ref('sh5000.demo_tag_002')

        for record in self:
            # creates a new record
            val = {
                'name': 'no super haha',
                # 'super_id': 2,
                # 'super_id': data_1.super_id,
                'tag_ids': [(6, 0, [tag_data_1.id, tag_data_2.id])]
            }

            self.sh5000_line_ids = [(0, 0, val)]

    # #@api.multi
    def link_demo_5000_record(self):
        # (4, id, _) links an already existing record.

        data_1 = self.env.ref(
            'sh5000.demo_5000_data_1')

        for record in self:
            # link already existing record
            self.sh5000_line_ids = [(4, data_1.id, 0)]

    # #@api.multi
    def replace_demo_5000_record(self):
        # (6, _, [ids]) replaces the list of linked records with the provided list.

        data_1 = self.env.ref(
            'sh5000.demo_5000_data_1')
        data_2 = self.env.ref(
            'sh5000.demo_5000_data_2')

        for record in self:
            # replace multi record
            self.sh5000_line_ids = [(6, 0, [data_1.id, data_2.id])]

    # #@api.multi

    def button_line_ids(self):
        return {
            'name': 'Demo SH5000 Line IDs',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'demo.sh5000.show',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('super_id', '=', self.id)],
        }

    # #@api.multi
    def name_get(self):
        names = []
        for record in self:
            name = '%s-%s' % (record.create_date.date(), record.name)
            names.append((record.id, name))
        return names

    # odoo12/odoo/odoo/addons/base/models/ir_model.py
    # @api.model
    # def _name_search(self, name='', args=None, operator='ilike', limit=100):
    #     if args is None:
    #         args = []
    #     #domain = args + ['|', ('id', operator, name), ('name', operator, name)]
    #     domain = args + [ ('name', operator, name)]
    #     # domain = args + [ ('id', operator, name)]
    #     return super(DemoSupervisor, self).search(domain, limit=limit).name_get()

    # overridden to allow searching both on model name (field 'model') and model
    # description (field 'name')
    # @api.model

    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('id', operator, name), ('name', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)


class sh5000(models.Model):
    _name = 'demo.sh5000.show'
    _description = 'sh5000 show - step by step'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # track_visibility

    name = fields.Char('the Name', required=True)
    mobile = fields.Char('Mobile No.')
    dzz = fields.Char('Company')
    biryear = fields.Char('Birth Year')
    education = fields.Char('Education')

    #image = fields.Binary('Picture')

    img = fields.Binary("Image", attachment=True)

    # track_visibility='always' 和 track_visibility='onchange'

    is_done_track_onchange = fields.Boolean(
        #string='Is Done?', default=False, track_visibility='onchange')
        string='Is Done?', default=False)

    name_track_always = fields.Char(
        #string="track_name", track_visibility='always')
        string="track_name")

    super_id = fields.Many2one(
        'demo.supervisor', string='the Supervisor', required='True')

    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    login = fields.Char('LOGIN', related='user_id.login')

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

    # #@api.multi
    def button_super_id(self):
        return {
            'view_mode': 'form',
            'res_model': 'demo.supervisor',
            'res_id': self.super_id.id,
            'type': 'ir.actions.act_window'
        }

    # #@api.multi
    def action_demo(self):
        self.ensure_one()
        _logger.warning('=== CALL ACTION 5000 Demo ===')

    def button_activity_schedule(self):
        self.activity_schedule(
            'sh5000.mail_act_approval',
            user_id = self.sudo().user_id.id,
            note = 'my note',
            summary = 'my summary')

    def button_activity_feedback(self):
        self.activity_feedback(
            ['sh5000.mail_act_approval'])

    def button_activity_unlink(self):
        self.activity_unlink(
            ['sh5000.mail_act_approval'])
