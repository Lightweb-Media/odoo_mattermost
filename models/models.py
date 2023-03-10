# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import mattermost
_logger = logging.getLogger(__name__)



class odoo_mattermost(models.Model):
    _name = 'odoo_mattermost.config'
    _description = 'odoo_mattermost.odoo_mattermost'

    def _get_mm_url(self):
        return 'https://chat.lightweb-media.de/api'
        return self.env['ir.config_parameter'].sudo().get_param('mattermost_url')
    

    def _get_mm_token(self):
        return 'axuk3kuqhjbh8qqwx9khph1gkr'
        return self.env['ir.config_parameter'].sudo().get_param('mattermost_token')
    
    def _get_mm_team_id(self):
        return 'kksq3nwy6tbztei781y73odf8o'
        return self.env['ir.config_parameter'].sudo().get_param('mattermost_team_id')  

    def _login(self):
        mm = mattermost.MMApi(self._get_mm_url())
        mm.login(bearer=self._get_mm_token())
        return mm

    def prepare_name(self, name):
        return name
       #
       #  return  "".join(ch for ch in name if ch.isalnum())
      #  return name.replace(' ', '_').replace('.', '_')
    
    def _create_user(self, email, name):
        mm = self._login()
        mm_user = mm.create_user(email, self.prepare_name(name))
        self.revoke_user_session()
        return mm_user

    def get_mm_user_by_email(self, email):
        pass

    def create_msg(self, msg, channel_id):
        mm = self._login()
        _logger.debug (channel_id)
        mm.create_post(channel_id, msg)
        mm.revoke_user_session()    

 #   @api.model
 #   def _get_user_id(self, user_name):
 #       return self.mm.get_user_id(user_name)

 
 #   def _create_channel(self, channel_name):
 #       self.mm.create_channel(channel_name)

 #   def _logout(self):
 #       self.mm.revoke_user_session()

class odoo_mattermost_partner(models.Model):
    #get_users (in_team=None, not_in_team=None, in_channel=None, not_in_channel=None, group_constrained=None, without_team=None, sort=None, **kwargs)
    _inherit = 'res.partner'
    mm_user_id = fields.Char(string='MM User ID', required=False)

    def mm_create_user(self):
        mm_obj = self.env['odoo_mattermost.config']._login()
       # mm_user = mm_obj.create_user(self.email, self.name)
        self.mm_user_id = mm_user['id']
        mm_obj.revoke_user_session()


class odoo_mattermost_project(models.Model):
   # _name = 'odoo_mattermost.project'
    _inherit = 'project.project'
    
    mm_channel_id = fields.Char(string='Channel ID', required=False)
    
    @api.onchange('allowed_internal_user_ids')
    def onchange_allowed_internal_user_ids(self):
        return self.allowed_internal_user_ids



    @api.onchange('user_id')
    def onchange_user_id(self):
        _logger.debug('onchange a %s with vals ', self.user_id)
      
        
        # Do something with the project or user
    """
    rename
    """
    def check_visibility(self):
       
        visibility = self.privacy_visibility


        if visibility == 'portal':
            """ potenziell ignorieren """
            #pass
            return []
        elif visibility == 'employers':
            """
            get all internal_user_ids and loop over it
            """
            #pass
            return []
        elif visibility == 'followers':
           user_ids = self.allowed_internal_user_ids
           return user_ids
           
          
    @api.model
    def mm_create_channel(self, ids):
        
        for id in ids:
            project = self.env['project.project'].browse(id)
           
        if project.mm_channel_id:
            return
        else:
       
            mm_obj = self.env['odoo_mattermost.config']._login()
            team_id = self.env['odoo_mattermost.config']._get_mm_team_id()
            channel = mm_obj.create_channel(team_id,str(hash(project.name)),project.name)
            project.mm_channel_id = channel['id']
 
            pm_user = project.user_id.mm_user_id
            
           
            mm_obj.add_user_to_channel(channel['id'], pm_user)
            for partner_id in self.check_visibility():
                if partner_id.mm_user_id:
                    mm_obj.add_user_to_channel(channel['id'], partner_id.mm_user_id)

            mm_obj.revoke_user_session()

   

        
        
class ProjectTask(models.Model):
  
    _inherit = ['project.task']
    _auto_subscribe = True


  
    @api.model
    def message_new(self, msg_dict, custom_values=None):
        print(f"New comment added to task {msg_dict.get('res_id')}: {msg_dict.get('body')}")
        if msg_dict.get('message_type') == 'comment':
            # Triggered when a new comment is added to the chatter log of a task

            # Access the message data using the `msg_dict` parameter
            print(f"New comment added to task {msg_dict.get('res_id')}: {msg_dict.get('body')}")

            # Do something with the message data
            # For example, you could create a new record or trigger a notification

        # Call super to continue the normal behavior of the method
        #return super().message_new(msg_dict, custom_values)

    
    @api.model_create_multi
    def create(self, vals_list):
        tasks = super(ProjectTask, self).create(vals_list)
        for task in tasks:
            if task.user_id and task.project_id.mm_channel_id and task.project_id.user_id.mm_user_id:
                msg = f"{task.user_id.name} created a new task: {task.name} for @{task.user_id.name}"
                self.env['odoo_mattermost.config'].create_msg(msg, task.project_id.mm_channel_id)
              #  self.env['odoo_mattermost.config'].create_msg(task.name, task.project_id.mm_channel_id)
                
        return tasks
    

    
    @api.onchange('stage_id')
    def _on_state_change(self):
        if self.user_id and self.project_id.mm_channel_id and self.project_id.user_id.mm_user_id:
            msg = f"{self.user_id.name} updated {self.name} stage to:  {self.stage_id.name}"
            self.env['odoo_mattermost.config'].create_msg(msg, self.project_id.mm_channel_id)
        pass

class MyModel(models.Model):
    _name = 'my.model'
    

    @api.model_create_single
    def message_new(self, msg_dict, custom_values=None):
        print('A new comment was added!')
        if msg_dict.get('message_type') == 'comment':
            # Your code here
            print('A new comment was added!')

        return super().message_new(msg_dict, custom_values)