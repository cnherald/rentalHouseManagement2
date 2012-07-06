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
    #rentalContract = db.ReferenceProperty()
    roomNumber = db.StringProperty(required = False)    
    area = db.FloatProperty()
    rentSingle = db.FloatProperty()
    rentDouble = db.FloatProperty()
    
    def hasVacancy(self):
        rooms = Room.all()
        for room in rooms:
            if room.isNotOccupied():
                    return True
        return False
    
    def isUnoccupied(self):
        rc = RentalContract()
        contracts = rc.getAllRentalContracts()
        for con in contracts:
            if self.key()== con.room.key():
                return False
        return True
    
    def getVacantRooms(self):
        rooms = Room.all()
        vacant_rooms_list = []
        rc = RentalContract()
        contracts = rc.getAllRentalContracts()
        for room in rooms:
            for con in contracts:
                if room.key() == con.room.key():
                    vacant_rooms_list.append(room)
        return vacant_rooms_list
        
    def getRoomsProfile(self,rooms):
        rooms_data_list = []
        for room in rooms:
            rooms_data_list.append({'roomKey':str(room.key()),'roomNumber':room.roomNumber,'area':room.area,'rentSingle':room.rentSingle,'rentDouble':room.rentDouble})
        return rooms_data_list     
      
class Tenant(db.Model):
    #rentalContract = db.ReferenceProperty()
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
    def hasCheckedIn(self):
        rc = RentalContract()
        contracts = rc.getAllRentalContracts()
        for con in contracts:
            if self.key()== con.tenant.key():
                return True
        return False
class RentalContract(db.Model):
    tenant = db.ReferenceProperty(Tenant)
    room = db.ReferenceProperty(Room)
    
    startDate = db.DateProperty()
    expiryDate = db.DateProperty()
    endDate = db.DateProperty()
    rent = db.FloatProperty()
    checkedOutDate = db.DateProperty()
    
    def getAllRentalContracts(self):
        contracts = db.GqlQuery("SELECT * "
                      "FROM RentalContract")
#        allContracts = []
#        for contract in contracts:
#            allContracts.append(contract)
        return contracts
    
    def createRentalContract(self,data):
        self.tenant = Tenant.get(data['tenantKey'])    
        self.room = Room.get(data['room_key'])
        self.rent = float(data['actualRent'])                                  
        self.payPeriod = int(data['payPeriod'])       
        startDate = datetime.strptime(data['startDate'],"%Y-%m-%d")
        self.startDate = startDate.date()
        self.expiryDate = startDate.date()
        
        self.put()
    
class Payment(db.Model):
    contract = db.ReferenceProperty(RentalContract, required = True)
    rentActual = db.FloatProperty()
    payPeriod = db.IntegerProperty(default = 1)
    bond = db.FloatProperty()
    
class Transaction(db.Model):
    payment = db.ReferenceProperty(Payment, required = True)
    paidAmount = db.FloatProperty()
    transactionDate = db.DateProperty()
