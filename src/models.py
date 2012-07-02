'''
Created on Jun 15, 2012

@author: qliu040
'''

from google.appengine.ext import db
from django.http import HttpResponse
from datetime import date
from datetime import timedelta
import math
from datetime import datetime
   

class Room(db.Model):
    #tenant = db.ReferenceProperty(required = False)
    #tenant = db.ReferenceProperty()#test
    roomNumber = db.StringProperty(required = False)    
    size = db.FloatProperty()
    rentSingle = db.FloatProperty()
    rentDouble = db.FloatProperty()
#    rentActual = db.FloatProperty()    

#    def notFull(self):
#        rooms = Room.all()
#        for room in rooms:
#            if (not room.tenant):
#                return True
#        return False
#            
#            
#    def getRoomProfile(self):
#        rooms = db.GqlQuery("SELECT * "
#                      "FROM Room")
#        data_list = []
#        for room in rooms:
#            if room.key()== self.key():
#                data_list.append({'roomNumber':room.roomNumber,'size':room.size,'rentSingle':room.rentSingle,'rentDouble':room.rentDouble,'rentActual':room.rentActual})          
#        return data_list
#    
#    def getAvailableRoomsProfile(self):
#        rooms = Room.all()
#        rooms_data_list = []
#        for room in rooms:
#            if (not room.tenant):
#                rooms_data_list.append({'roomKey':str(room.key()),'roomNumber':room.roomNumber,'size':room.size,'rentSingle':room.rentSingle,'rentDouble':room.rentDouble,'rentActual':room.rentActual})
#        return rooms_data_list
#        
#        
#    def updateRoomProfile(self,data):
#        rooms = db.GqlQuery("SELECT * "
#              "FROM Room")
#        for room in rooms:
#            if room.key() == self.key():
#                room.roomNumber = data['number']
#                room.size = float(data['size'])
#                room.rentSingle = float(data['rentSingle'])
#                room.rentDouble = float(data['rentDouble'])
#                room.rentActual = float(data['rentActual'])
#                room.put()
#        return True
      
class Tenant(db.Model):
    firstName = db.StringProperty()
    surname = db.StringProperty()
    gender = db.StringProperty()
    age = db.IntegerProperty(default = 20)
    phoneNumber = db.PhoneNumberProperty()
    contactName = db.StringProperty()
    contactPhoneNumber = db.PhoneNumberProperty()
    email = db.EmailProperty()  
    #payPeriod = db.IntegerProperty(default = 1)    
    #expiryDate = db.DateProperty()  
    #startDate = db.DateProperty(auto_now_add = True)
    registerDate = db.DateProperty(auto_now_add = True)  
    
    def registerTenant(self,data):
        tenant = Tenant(key_name = data['firstName'] + data['surname'] + data['registerDate'])         
        #tenant = Tenant(key_name = self.request.get('firstName')+'_' + self.request.get('surname'))      
        tenant.firstName = data['firstName']
        tenant.surname = data['surname']
        tenant.gender = data['gender']
        tenant.age = int(data['age'])
        tenant.phoneNumber = data['phoneNumber'] 
        tenant.contactName = data['contactName']
        tenant.contactPhoneNumber = data['contactPhoneNumber']
        #tenant.registerDate = data['registerDate']
        registerDate = datetime.strptime(data['registerDate'],"%Y-%m-%d")
        tenant.registerDate = registerDate.date()    
        tenant.put()
        return tenant
    
    def getCurrentTenants(self):
        tenants = db.GqlQuery("SELECT * "
                              "FROM Tenant")
        currentTenants = []
        for tenant in tenants:
            currentTenants.append(tenant)              
        return currentTenants  

class Contract(db.Model):
    tenant = db.ReferenceProperty(Tenant, required = True)
    room = db.ReferenceProperty(Room, required = True)
    checkedIn = db.BooleanProperty()
    startDate = db.DateProperty()
    endDate = db.DateProperty()
    checkedOutDate = db.DateProperty()
    
class Payments(db.Model):
    contract = db.ReferenceProperty(Contract, required = True)
    rentActual = db.FloatProperty()
    payPeriod = db.IntegerProperty(default = 1)
    bond = db.FloatProperty()
    
class Transaction(db.Model):
    payment = db.ReferenceProperty(Payments, required = True)
    paidAmount = db.FloatProperty()
    transactionDate = db.DateProperty()
