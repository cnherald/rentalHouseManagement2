from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from models import Tenant
from models import Room
from google.appengine.ext import db
import simplejson
import django.utils.simplejson as json

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
        
class RoomHandler(webapp.RequestHandler):
    def get(self):
        rooms = db.GqlQuery("SELECT *"
                            "FROM Room")

        path = os.path.join(os.path.dirname(__file__), 'htmls/rooms.html')         
        template_values = {'rooms':rooms}
        self.response.out.write(template.render(path, template_values)) 
    def post(self):
        room = Room()
        room.roomNumber = self.request.get('room_number')
        room.size = float(self.request.get('room_size'))
        room.rentSingle = float(self.request.get('room_rent_single'))
        room.rentDouble = float(self.request.get('room_rent_double'))
        #room.availability = self.request.get('room_availability')
        room.put()    
        room_url = '/rooms'
        self.redirect(room_url) 
        
class tenantRegisterHandler(webapp.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        jsonString = self.request.body          
        data = simplejson.loads(jsonString) #Decoding JSON 
        Tenant().registerTenant(data) 
        #tenant = Tenant().registerTenant(data)
        #tenant.createRegisterActivityRecord()
        tenantRegisterResponse = {'tenantRegisterMsg':'Congratulations, you have registered a new tenant successfully!'}
        jsonResponse = simplejson.dumps(tenantRegisterResponse)
        return self.response.out.write(jsonResponse)
                  

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/tenantRegister',tenantRegisterHandler),
                                      ('/rooms',RoomHandler),
                                      ('/tenants',TenantHandler)], debug=True)

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
