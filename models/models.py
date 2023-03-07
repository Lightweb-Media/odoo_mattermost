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
    


    def get_mm_user_by_email(self, email):
        pass

    def create_msg(self, msg, channel_id):
        mm = self._login()
        _logger.debug (channel_id)
        mm.create_post(channel_id, msg)
        self.revoke_user_session()    

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


class odoo_mattermost_project(models.Model):
   # _name = 'odoo_mattermost.project'
    _inherit = 'project.project'
    
    mm_channel_id = fields.Char(string='Channel ID', required=False)
    
    @api.onchange('allowed_internal_user_ids')
    def onchange_allowed_internal_user_ids(self):
        print (self.allowed_internal_user_ids)
        print (self.user_id.mm_user_id)

    @api.onchange('user_id')
    def onchange_user_id(self):
        _logger.debug('onchange a %s with vals ', self.user_id)
        print ('dsfudfsdafsdflasdjfklsdjfjasdkfhsdkfhasdfsdjflksdjl')
        print (self.user_id)
        print (self.user_id.mm_user_id)
        
        # Do something with the project or user
    """
    rename
    """
    def check_visibility(self):
        return ['rc6hexnjfbr48xewksszj3siao'] 
        visibility = self.privacy_visibility


        if visibility == 'portal':
            """ potenziell ignorieren """
            pass
        elif visibility == 'employers':
            """
            get all internal_user_ids and loop over it
            """
            pass
        elif visibility == 'followers':
           user_ids = self.allowed_internal_user_ids
           
           """
           toDo:
            loop over user_ids to get list of mm_user_id like 
        

           return [
               '63869injb3ny78yofbqkkijfsr',
               'c5bhujruu7n3jc1ohuzekfrw4r',
               '8bhysa3wu78jj8b3uw1quu7idy',
               'mo48tguyu3fn9pcqzkg64aibjo',
               '3g5m5h8oq3rjmeu38j85c7k5nc',
               '14hrfamn8ty3zjqk17np8uirga',
               'rc6hexnjfbr48xewksszj3siao',
               'nsteeshro38nxbgr9bc9k1csho',
               '63869injb3ny78yofbqkkijfsr'
               ]  
            """
          
    @api.model
    def create_channel(self, project_id):
        active_id = project_id
        project = self.browse(active_id)
        print (project_id)    
        if self.mm_channel_id:
            return
        else:
       
            mm_obj = self.env['odoo_mattermost.config']._login()
            team_id = self.env['odoo_mattermost.config']._get_mm_team_id()
            channel = mm_obj.create_channel(team_id,str(hash(project.name)),project.name)
            project.mm_channel_id = channel['id']
        # except:
        #     return
            pm_user = self.user_id.mm_user_id
            mm_obj.add_user_to_channel(channel['id'], pm_user)
            for user in self.check_visibility():
                mm_obj.add_user_to_channel(channel['id'], user)

            mm_obj.revoke_user_session()

   

        
        
class ProjectTask(models.Model):
    _inherit = 'project.task'

    
    def message_new(self, msg_dict, custom_values=None):
        """Triggered when a new message is added to a task."""
        task = self.browse(msg_dict.get('res_id'))
        print (task)
        _logger.warning(msg_dict.get('body'))
        self.env['odoo_mattermost.config'].create_msg('tests', 'ragdbxts5bd3fc54fidt3kojee')
        #task.project_id.mm_channel_id
        # Do something with the task or message
        return super(ProjectTask, self).message_new(msg_dict, custom_values)