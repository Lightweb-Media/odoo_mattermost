import mattermost
import pprint
'''
Token Description: odoo_connector
Token ID: aks457thep8s5xd4oe1kwpracc
Access Token: axuk3kuqhjbh8qqwx9khph1gkr
'''
#axuk3kuqhjbh8qqwx9khph1gkr 


mm = mattermost.MMApi("https://chat.lightweb-media.de/api")
mm.login(bearer="axuk3kuqhjbh8qqwx9khph1gkr ")

pprint.pprint(mm.get_user())