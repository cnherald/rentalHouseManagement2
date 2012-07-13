from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from models import Tenant
from models import Room
from models import RentalContract
from models import Payment
from models import Transaction
from google.appengine.ext import db
import simplejson
import django.utils.simplejson as json
from datetime import datetime

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
        path = os.path.join(os.path.dirname(__file__), 'templates/mainPage.html')
        template_values = {'pendingTenants':pendingTenants, 'clearedTenants':clearedTenants}
        self.response.out.write(template.render(path, template_values))
        
class TenantHandler(webapp.RequestHandler):
    roomNotAvailable = False
    def get(self):
        tenants = Tenant().getCurrentTenants()
        rooms = Room.all().get()
        path = os.path.join(os.path.dirname(__file__), 'templates/tenants.html')
     
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

        path = os.path.join(os.path.dirname(__file__), 'templates/rooms.html')         
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
        vacantRooms=room.getVacantRooms()
        if vacantRooms:            
            tenant_data_list = tenant.getTenantProfile()
            rooms_data_list = room.getRoomsProfile(vacantRooms)
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
        contract = RentalContract()
        contract.createRentalContract(data)
        payment = Payment()
        payment.initializePayment(contract)
        #.createCheckinActivityRecord()          
        checkinResponse = {'checkinSuccessMessage':'Congratulations, you have checked in the room successfully!'}
        jsonCheckinResponse = simplejson.dumps(checkinResponse)
        return self.response.out.write(jsonCheckinResponse)
    
class RoomProfileDataHandler(webapp.RequestHandler):
    def get(self):
        room_key = self.request.get('room_key')
        room = Room.get(room_key)
        data_list = []
        #data_list = room.getRoomProfile()
        data_list.append({'roomNumber':room.roomNumber,'area':room.area,'rentSingle':room.rentSingle,'rentDouble':room.rentDouble})
        output_json = json.dumps(data_list)
        self.response.out.write(output_json) 

    def post(self):
        room_key = self.request.get('room_key')
        room = Room.get(room_key)
        room.roomNumber = self.request.get('room_number')    
        room.size = float(self.request.get('room_size'))
        room.rentSingle = float(self.request.get('room_rentSingle'))
        room.rentDouble = float(self.request.get('room_rentDouble'))
        room.put()
        roomProfile_url = '/rooms'
        self.redirect(roomProfile_url)

class TenantContractHandler(webapp.RequestHandler):
    def get(self):
        contracts = db.GqlQuery("SELECT * "
                            "FROM RentalContract")

        path = os.path.join(os.path.dirname(__file__), 'templates/contracts.html')         
        template_values = {'contracts':contracts}
        self.response.out.write(template.render(path, template_values)) 
    
class TenantPaymentHandler(webapp.RequestHandler):    
    def get(self):
        payments = db.GqlQuery("SELECT * "
                            "FROM Payment")
        path = os.path.join(os.path.dirname(__file__), 'templates/payments.html')         
        template_values = {'payments':payments}
        self.response.out.write(template.render(path, template_values)) 
        
class PayRentHandler(webapp.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        jsonString = self.request.body          
        data = simplejson.loads(jsonString) #Decoding JSON
#        payAmount = float(data['payAmount'])
#        payDate = datetime.strptime(data['payDate'],"%Y-%m-%d").date()
#        tenant_key = data['tenant_key']                   
#        tenant = Tenant.get(tenant_key)
#        payment_key = data['payment_key']
#        payment = Payment.get(payment_key)
        transaction = Transaction()
        #transaction.createTransaction(payment,payAmount,payDate)
        transaction.createTransaction(data)
        pass        
    #transactions go here
application = webapp.WSGIApplication([('/', MainPage),
                                      ('/tenantContracts',TenantContractHandler),
                                      ('/tenantPayment',TenantPaymentHandler),
                                      ('/payRent',PayRentHandler),
                                      ('/tenantRegister',TenantRegisterHandler),
                                      ('/roomRegister',RoomRegisterHandler),
                                      ('/tenantCheckin',TenantCheckinHandler),
                                      ('/rooms',RoomHandler),
                                      ('/roomProfileData',RoomProfileDataHandler),
                                      ('/tenants',TenantHandler)], debug=True)

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
