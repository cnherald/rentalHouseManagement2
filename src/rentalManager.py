from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from models import Tenant
from models import Room
from models import RentalContract
from google.appengine.ext import db
import simplejson
import django.utils.simplejson as json

class MainPage(webapp.RequestHandler):
    def get(self):
        
        tenants = Tenant().getCurrentTenants()              
        clearedTenants = []
        pendingTenants = []      
#        for tenant in tenants:
#            if tenant.RentalContract.room: #displays only checked in tenant                 
#                if tenant.paymentIsClear():
#                    clearedTenants.append(tenant)                
#                else:
#                    pendingTenants.append(tenant)  
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
        
class TenantRegisterHandler(webapp.RequestHandler):
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
    
class RoomRegisterHandler(webapp.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        jsonString = self.request.body          
        data = simplejson.loads(jsonString) #Decoding JSON        
        room = Room(key_name = data['roomNumber'] )
        room.roomNumber = data['roomNumber']         
        room.area = float(data['roomArea'])
        room.rentSingle = float(data['rentSingle'])
        room.rentDouble = float(data['rentDouble'])
        room.put()    

        roomRegisterResponse = {'roomRegisterMsg':'Congratulations, you have registered a new room successfully!'}
        json = simplejson.dumps(roomRegisterResponse)
        return self.response.out.write(json)
                  
class TenantCheckinHandler(webapp.RequestHandler):
    def get(self):
        tenant_key = self.request.get('tenant_key')
        tenant = Tenant.get(tenant_key)
        room = Room()
        contract = RentalContract()
        contracts = contract.getAllRentalContracts()
        if room.notFull():            
            tenant_data_list = tenant.getTenantProfile()
            rooms_data_list = room.getAvailableRoomsProfile()
            data_list = []
            data_list.append({'tenantProfile': tenant_data_list, 'roomsProfile': rooms_data_list})
            output_json = json.dumps(data_list) 
            self.response.out.write(output_json)                              
        else:
            noVacancyResponse = {'noVacancyResponse':'Sorry, All rooms are occupied!'}
            noVacancyResponse_json = simplejson.dumps(noVacancyResponse)
            return self.response.out.write(noVacancyResponse_json) 
        
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        jsonString = self.request.body       
        data = simplejson.loads(jsonString)
        tenant_key = data['tenantKey']
        tenant = Tenant.get(tenant_key)
        tenant.registerRoom(data)
        tenant.createCheckinActivityRecord()          
        checkinResponse = {'checkinSuccessMessage':'Congratulations, you have checked in the room!'}
        jsonCheckinResponse = simplejson.dumps(checkinResponse)
        return self.response.out.write(jsonCheckinResponse)
application = webapp.WSGIApplication([('/', MainPage),
                                      ('/tenantRegister',TenantRegisterHandler),
                                      ('/roomRegister',RoomRegisterHandler),
                                      ('/tenantCheckin',TenantCheckinHandler),
                                      ('/rooms',RoomHandler),
                                      ('/tenants',TenantHandler)], debug=True)

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
