from odoo import http


class Show5000(http.Controller):

    @http.route('/demo/sh5000', auth='public')
    def list(self, **kwargs):
        obj = http.request.env['demo.sh5000.show']
        objs = obj.search([])
        return http.request.render(
            'sh5000.demo_sh5000_template',{'objs': objs})


# -*- coding: utf-8 -*-
# from odoo import http


# class Sh5000(http.Controller):
#     @http.route('/sh5000/sh5000/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sh5000/sh5000/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sh5000.listing', {
#             'root': '/sh5000/sh5000',
#             'objects': http.request.env['sh5000.sh5000'].search([]),
#         })

#     @http.route('/sh5000/sh5000/objects/<model("sh5000.sh5000"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sh5000.object', {
#             'object': obj
#         })
