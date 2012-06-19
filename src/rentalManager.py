from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from models import Tenant
from models import Room

class MainPage(webapp.RequestHandler):
    def get(self):
        
        tenants = Tenant().getCurrentTenants()              
        clearedTenants = []
        pendingTenants = []      
        for tenant in tenants:
            if tenant.room: #displays only checked in tenant                 
                if tenant.paymentIsClear():
                    clearedTenants.append(tenant)                
                else:
                    pendingTenants.append(tenant)  
        path = os.path.join(os.path.dirname(__file__), 'htmls/mainPage.html')
        template_values = {'pendingTenants':pendingTenants, 'clearedTenants':clearedTenants}
        self.response.out.write(template.render(path, template_values))
        
class TenantHandler(webapp.RequestHandler):
    roomNotAvailable = False
    def get(self):
        tenants = Tenant().getCurrentTenants()
        rooms = Room.all().get()
        path = os.path.join(os.path.dirname(__file__), 'htmls/tenants.html')
     
        if rooms:
            template_values = {'tenants':tenants} 
        else:                 
            roomNotAvailable = True
            template_values = {'tenants':tenants, 'roomNotAvailable':roomNotAvailable}                       

        self.response.out.write(template.render(path, template_values))       

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/tenants',TenantHandler)], debug=True)

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
