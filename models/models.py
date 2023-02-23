# -*- coding: utf-8 -*-

from odoo import models, fields, api
import mattermost

class odoo_mattermost(models.Model):
    _name = 'odoo_mattermost.config'
    _description = 'odoo_mattermost.odoo_mattermost'
    
    def __init__(self):
        self.mm = ''
        self.mm = self._login()

    def _login(self):
        mattermost_url = self.env['ir.config_parameter'].sudo().get_param('mattermost_url')
        bearer_token = self.env['ir.config_parameter'].sudo().get_param('mattermost_bearer_token')
        self.mm = mattermost.MMApi(mattermost_url)
        self.mm.login(bearer=bearer_token)
  
    def _get_user_id(self, user_name):
        return self.mm.get_user_id(user_name)

    def _create_channel(self, channel_name):
        self.mm.create_channel(channel_name)

    def _logout(self):
        self.mm.revoke_user_session()

class odoo_mattermost(models.Model):
    _name = 'odoo_mattermost.partner'
    _description = 'odoo_mattermost.odoo_mattermost'
    _inherit = 'res.partner'
    mattermost_user_id = fields.Char(string='Mattermost ID', required=False)



class odoo_mattermost(models.Model):
    _name = 'odoo_mattermost.chatter'
    _description = 'odoo_mattermost.odoo_mattermost'
    _inherit = 'mail.message'



class odoo_mattermost(models.Model):
    _name = 'odoo_mattermost.project'
    _description = 'odoo_mattermost.odoo_mattermost'
  
