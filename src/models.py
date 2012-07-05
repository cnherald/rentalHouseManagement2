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
    rentalContract = db.ReferenceProperty()
    roomNumber = db.StringProperty(required = False)    
    area = db.FloatProperty()
    rentSingle = db.FloatProperty()
    rentDouble = db.FloatProperty()
    
    def notFull(self):
        rooms = Room.all()
        rc = RentalContract()
        for room in rooms:
            for con in rc.getAllRentalContracts():
                if room.key() == con.room.key():
                #if (not room.rentalContract.tenant):
                    return False
        return True
    
    def getAvailableRooms(self):
        rooms = Room.all()
        rooms_list = []
        for room in rooms:
            if (not room.rentalContract):
                rooms_list.append(room)
        return rooms_list
    
    def getRoomProfile(self):
        rooms = db.GqlQuery("SELECT * "
                      "FROM Room")
        data_list = []
        for room in rooms:
            if room.key()== self.key():
                data_list.append({'roomNumber':room.roomNumber,'area':room.area,'rentSingle':room.rentSingle,'rentDouble':room.rentDouble})          
        return data_list
        
    def getRoomsProfile(self,rooms):
        #rooms = Room.all()
        rooms_data_list = []
        for room in rooms:
            #if (not room.tenant):
                rooms_data_list.append({'roomKey':str(room.key()),'roomNumber':room.roomNumber,'area':room.area,'rentSingle':room.rentSingle,'rentDouble':room.rentDouble})
        return rooms_data_list
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
    
    def getAllTenants(self):
        tenants = db.GqlQuery("SELECT * "
                      "FROM Tenant")
        return tenants
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
    
    def getTenantProfile(self):
        tenants = db.GqlQuery("SELECT * "
                      "FROM Tenant")
        data_list = []
        for tenant in tenants:
            if tenant.key()== self.key():
                data_list.append({'firstName':tenant.firstName,'surname':tenant.surname,'gender':tenant.gender,'age':tenant.age,'phoneNumber':tenant.phoneNumber,'email':tenant.email,'contactName':tenant.contactName,'contactPhoneNumber':tenant.contactPhoneNumber,'registerDate': tenant.registerDate.isoformat()})          
        return data_list
    
    def getCurrentTenants(self):
        tenants = db.GqlQuery("SELECT * "
                              "FROM Tenant")
        currentTenants = []
        for tenant in tenants:
            currentTenants.append(tenant)              
        return currentTenants  

class RentalContract(db.Model):
    tenant = db.ReferenceProperty(Tenant)
    room = db.ReferenceProperty(Room)
    checkedIn = db.BooleanProperty()
    startDate = db.DateProperty()
    endDate = db.DateProperty()
    checkedOutDate = db.DateProperty()
    
    def getAllRentalContracts(self):
        contracts = db.GqlQuery("SELECT * "
                      "FROM RentalContract")
#        allContracts = []
#        for contract in contracts:
#            allContracts.append(contract)
        return contracts
    
class Payment(db.Model):
    contract = db.ReferenceProperty(RentalContract, required = True)
    rentActual = db.FloatProperty()
    payPeriod = db.IntegerProperty(default = 1)
    bond = db.FloatProperty()
    
class Transaction(db.Model):
    payment = db.ReferenceProperty(Payment, required = True)
    paidAmount = db.FloatProperty()
    transactionDate = db.DateProperty()
