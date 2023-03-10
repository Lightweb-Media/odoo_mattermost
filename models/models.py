# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from datetime import datetime
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
        return '4cww6pn4ft8wurd6y1zbpfibth'
        return self.env['ir.config_parameter'].sudo().get_param('mattermost_team_id')  

    def _login(self):
        mm = mattermost.MMApi(self._get_mm_url())
        mm.login(bearer=self._get_mm_token())
        return mm

    def prepare_name(self, name):
        return  "".join(ch for ch in name if ch.isalnum())
    
  



class odoo_mattermost_partner(models.Model):
    #get_users (in_team=None, not_in_team=None, in_channel=None, not_in_channel=None, group_constrained=None, without_team=None, sort=None, **kwargs)
    _inherit = 'res.partner'
    mm_user_id = fields.Char(string='MM User ID', required=False)

    @api.model
    def mm_create_user(self, ids):
        print (ids)
        for id in ids:
            partner_id = self.env['res.partner'].browse(id)
        mm_obj = self.env['odoo_mattermost.config']._login()
        
        name = partner_id.name.replace(" ", "")
        
        data = {
            'email': partner_id.email,
            'username': name,
            "auth_data": "cn=test1234,ou=users,dc=ldap,dc=goauthentik,dc=io",
            "auth_service": "saml",
        }
        mm_user = mm_obj._post("/v4/users",data=data)
      
        self.mm_user_id = mm_user['id']
        mm_obj.revoke_user_session()


class odoo_mattermost_project(models.Model):
   # _name = 'odoo_mattermost.project'
    _inherit = 'project.project'
    
    mm_channel_id = fields.Char(string='Channel ID', required=False)

    def remove_all_channel_user(self, channel_id):
        mm_obj = self.env['odoo_mattermost.config']._login()
        users = mm_obj.get_channel_members(channel_id)
        for user in users:
            mm_obj.remove_user_from_channel(channel_id, user['user_id'])
        mm_obj.revoke_user_session()
        
    

    def write(self, vals):
        result = super().write(vals)
       
        if 'allowed_internal_user_ids' in vals and self.mm_channel_id:
                
                
                mm_obj = self.env['odoo_mattermost.config']._login()
                new_allowed_users = self.allowed_internal_user_ids
                self.remove_all_channel_user(self.mm_channel_id)
                
                for user in new_allowed_users:
                    if user.mm_user_id:
                        mm_obj.add_user_to_channel(self.mm_channel_id, user.mm_user_id)
                mm_obj.revoke_user_session()
        
        return result

    @api.onchange('stage_id')
    def _on_state_change(self):
        if self.mm_channel_id:
            if self.user_id  and self.user_id.mm_user_id:
    
                msg = f"{self.user_id.name} updated {self.name} stage to:  {self.stage_id.name}"
                self.env['odoo_mattermost.config'].create_msg(msg, self.project_id.mm_channel_id)
            pass

   # @api.model
   # def create(self, vals):
   #     project = super().create(vals)
        # Your code here
   #     return project

    @api.onchange('active')
    def _on_active_change(self):
       
        if self.name:
            if self.project_id.mm_channel_id:
                if not self.active:
                    msg = f"{self.user_id.name} archived {self.name}"
                    self.env['odoo_mattermost.config'].create_msg(msg, self.project_id.mm_channel_id)
                    
                    payload = {
                        
                        }
                    
                    mm_obj = self.env['odoo_mattermost.config']._login()
                    mm_obj._delete("/v4/channels/"+self.mm_channel_id, data=payload)
                    mm_obj.revoke_user_session()
        #   if self.active and self.project_id.mm_channel_id:


  #  def write(self, vals):
  #      result = super().write(vals)
  #      if 'active' in vals:
            # Check if the project is being archived
   #         if not vals['active'] and self.mm_channel_id:
   #             payload = {
                 
    #            }
    #            mm_obj = self.env['odoo_mattermost.config']._login()

    #            mm_obj._delete("/v4/channels/"+self.mm_channel_id, data=payload)
    #            mm_obj.revoke_user_session()
        
            
    #    return result

   # def write(self, vals):
   #     result = super().write(vals)
   #     if 'active' in vals:
            # Check if the project is being archived
   #         if  vals['active'] and self.mm_channel_id:
   #             payload = {
   #              
   #             }
   #             mm_obj = self.env['odoo_mattermost.config']._login()
   #             mm_obj._delete("/v4/channels/"+self.mm_channel_id, data=payload)
   #             mm_obj.revoke_user_session()

            
   #     return result        
    """
    rename
    """
    def check_visibility(self):
       
        visibility = self.privacy_visibility
        print (visibility)

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
           print(user_ids)
           return user_ids
        else:
           return []
          
    @api.model
    def mm_create_channel(self, ids):
        
        for id in ids:
            project = self.env['project.project'].browse(id)
           
        if project.mm_channel_id:
            return
        else:
            
            if project.name and project.user_id.mm_user_id:
                
                name = self.env['odoo_mattermost.config'].prepare_name(project.name)
                mm_obj = self.env['odoo_mattermost.config']._login()
             #   print (str(hash(project.name))+str(fields.datetime.now()))
                
                team_id = self.env['odoo_mattermost.config']._get_mm_team_id()
                org_channel = False
                try:
                    org_channel = mm_obj.get_channel_by_name(team_id,name)
                except:
                    pass
                if(org_channel):
                   
                    project.mm_channel_id = org_channel['id']
                if not org_channel:
                  
                    channel = mm_obj.create_channel(team_id,name,project.name)
                    project.mm_channel_id = channel['id']
    
                pm_user = project.user_id.mm_user_id
                
            
                mm_obj.add_user_to_channel(project.mm_channel_id, pm_user)
                mm_obj.revoke_user_session()

   

        
        
class ProjectTask(models.Model):
  
    _inherit = ['project.task']
    _auto_subscribe = True


    
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

