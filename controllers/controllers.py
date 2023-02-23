# -*- coding: utf-8 -*-
# from odoo import http


# class OdooMattermost(http.Controller):
#     @http.route('/odoo_mattermost/odoo_mattermost/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_mattermost/odoo_mattermost/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_mattermost.listing', {
#             'root': '/odoo_mattermost/odoo_mattermost',
#             'objects': http.request.env['odoo_mattermost.odoo_mattermost'].search([]),
#         })

#     @http.route('/odoo_mattermost/odoo_mattermost/objects/<model("odoo_mattermost.odoo_mattermost"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_mattermost.object', {
#             'object': obj
#         })
