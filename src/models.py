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
        contracts = rc.getValidRentalContracts()
        for con in contracts:
            if self.key()== con.room.key():
                return False
        return True
    
    def getVacantRooms(self):
        rooms = Room.all()
        vacant_rooms_list = []
        rc = RentalContract()
        validContracts = rc.getValidRentalContracts()  
        for room in rooms:
            for con in validContracts :
                if room.key() == con.room.key():
                    break
            else:
                #continue   
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
        tenant.email = data['email']
        tenant.contactName = data['contactName']
        tenant.contactPhoneNumber = data['contactPhoneNumber']
        #tenant.registerDate = data['registerDate']
        registerDate = datetime.strptime(data['registerDate'],"%Y-%m-%d")
        tenant.registerDate = registerDate.date()    
        tenant.put()
        return tenant
    
    def getTenantProfile(self):
#        tenants = db.GqlQuery("SELECT * "
#                      "FROM Tenant")
        data_list = []
        #for tenant in tenants:
            #if tenant.key()== self.key():
                #data_list.append({'firstName':tenant.firstName,'surname':tenant.surname,'gender':tenant.gender,'age':tenant.age,'phoneNumber':tenant.phoneNumber,'email':tenant.email,'contactName':tenant.contactName,'contactPhoneNumber':tenant.contactPhoneNumber,'registerDate': tenant.registerDate.isoformat()})
        data_list.append({'firstName':self.firstName,'surname':self.surname,'gender':self.gender,'age':self.age,'phoneNumber':self.phoneNumber,'email':self.email,'contactName':self.contactName,'contactPhoneNumber':self.contactPhoneNumber,'registerDate': self.registerDate.isoformat()})        
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
        contracts = rc.getValidRentalContracts()
        for con in contracts:
            if self.key()== con.tenant.key():
                return True
        return False
   
    def getRentalStatusInfo(self):
        rentalStatus_data_list = []
        paymentKey = self.getPayment().key()
        lastPayDate = self.getLastPayDate()
        if lastPayDate:
            lastPayDate = lastPayDate.isoformat()
        rentalStatus_data_list.append({'firstName':self.firstName,'surname':self.surname,'roomNumber':self.getTenantContract().room.roomNumber,'startDate':self.getTenantContract().startDate.isoformat(),'livingPeriod':self.getLivingPeriod(),'rent':self.getTenantContract().rent,'rentRate':self.getTenantContract().getRentRate(),'totalPaidRent':self.getPayment().totalPaidAmount,'lastPayDate':lastPayDate,'unpaidDays': self.getUnpaidDays(),'unpaidRent':self.getUnpaidRent(),'paymentKey':str(paymentKey)})          
        return rentalStatus_data_list   
   
    def getTenantContract(self):
        contracts = RentalContract().getValidRentalContracts()
        for contract in contracts:
            if contract.tenant.key() == self.key():
                return contract
            
    def getLivingPeriod(self):
        today = date.today()
        contract = self.getTenantContract()
        startDay = contract.startDate       
        return (today-startDay).days
    
    def getPayment(self):
        contract = self.getTenantContract()
        payment = contract.getTenantPayment()
        return payment
    
    def getUnpaidDays(self):
        #today = datetime.date.today()
        today = date.today()
        expiryDate = self.getPayment().rentExpiredDate
        return (today-expiryDate).days
         
    def getUnpaidRent(self):
        return round(self.getUnpaidDays()*self.getTenantContract().getRentRate(),1)
    
    def getLastPayDate(self):
        
#        transactions = db.GqlQuery("SELECT * "
#                    "FROM Transaction")
        tenantPayment = self.getPayment()
        transactions = db.GqlQuery("SELECT * FROM Transaction WHERE payment = :1" ,tenantPayment,)
        transactionDates = []
        if transactions:
            for transaction in transactions:    
                    #if transaction.payer.key().name() == self.key().name():
                transactionDates.append(transaction.transactionDate)
        if not transactionDates:
            return None
        else:
            return max(transactionDates)       
    
    
class RentalContract(db.Model):
    tenant = db.ReferenceProperty(Tenant)
    room = db.ReferenceProperty(Room)
    
    startDate = db.DateProperty()
    payPeriod = db.IntegerProperty(default = 1)
    
    #endDate = db.DateProperty()
    rent = db.FloatProperty()
    #bond = db.FloatProperty()
    checkOutDate = db.DateProperty()
    isValid = db.BooleanProperty()
    
    def getRentRate(self):
        return round(self.rent/7.0,1)
    
    def getBond(self):
        return round(self.rent * 2)
    
    def getValidRentalContracts(self):
        contracts = db.GqlQuery("SELECT * "
                      "FROM RentalContract "  #need space between the statement and the question mark
                      "WHERE isValid = :1 ORDER BY startDate",True )  
        return contracts
    
    def getInvalidRentalContracts(self):
        contracts = db.GqlQuery("SELECT * "
                      "FROM RentalContract "    #need space between the statement and the question mark
                      "WHERE isValid = :1 ORDER BY checkOutDate",False )
        return contracts
    
    def createRentalContract(self,data):
        self.tenant = Tenant.get(data['tenantKey'])    
        self.room = Room.get(data['room_key'])
        self.rent = float(data['actualRent'])                                  
        self.payPeriod = int(data['payPeriod'])       
        startDate = datetime.strptime(data['startDate'],"%Y-%m-%d")
        self.startDate = startDate.date()
        #self.rentExpiredDate = startDate.date()
        self.isValid = True
        self.put()
        
    def getTenantPayment(self):
        payments = Payment().getAllPayments()
        for payment in payments:
            if payment.contract.key() == self.key():
                return payment
    
        
        
    
class Payment(db.Model):
    contract = db.ReferenceProperty(RentalContract)
    #rentActual = db.FloatProperty()
    totalPaidAmount = db.FloatProperty()
    rentExpiredDate = db.DateProperty()
    
    def getAllPayments(self):
        payments = db.GqlQuery("SELECT * "
                      "FROM Payment ")
        return payments
    def initializePayment(self, contract):
        self.contract = contract
        self.rentExpiredDate = self.contract.startDate
        self.totalPaidAmount = 0.0
        self.put()
        
    def getLastPayDate(self):       
        transactions = db.GqlQuery("SELECT * "
                    "FROM Transaction")
        payDates = []
        if transactions:
            for transaction in transactions:    
                    if transaction.payment.key().name() == self.key().name():
                        payDates.append(transaction.transactionDate)
        if not payDates:
            return None
        else:
            return max(payDates)
    
    def updateExpiryDate(self,paidAmount):        
        rate = self.contract.getRentRate()
        days = int(paidAmount / rate)
        paid_days = timedelta(days = days)         
        self.rentExpiredDate = self.rentExpiredDate + paid_days
        
    def getTenantTransactions(self):
        transactions = Transaction().getAllTransactions()
        transactions_list = []
        i = 1
        for transaction in transactions:
            if transaction.payment.key() == self.key():
                tenant = self.contract.tenant
                transactions_list.append({'transactionNumber': tenant.firstName + "_" + tenant.surname + "_" + str(i),'transactionDate': transaction.transactionDate.isoformat(), 'paidAmount': transaction.paidAmount})
                i = i + 1
        transactions_list.append({'totalPaidAmount':self.totalPaidAmount}) 
        return transactions_list
        
    
class Transaction(db.Model):
    payment = db.ReferenceProperty(Payment)
    paidAmount = db.FloatProperty()
    transactionDate = db.DateProperty()
    
    def getAllTransactions(self):
        transactions = db.GqlQuery("SELECT * "
                      "FROM Transaction")
        return transactions
    
    def processTransaction(self,data):
        paidAmount = float(data['paidAmount'])
        payDate = datetime.strptime(data['payDate'],"%Y-%m-%d").date()
#        tenant_key = data['tenant_key']                   
#        tenant = Tenant.get(tenant_key)
        payment_key = data['payment_key']
        payment = Payment.get(payment_key)
        payment.totalPaidAmount = payment.totalPaidAmount + paidAmount
        self.payment = payment
        self.paidAmount = paidAmount
        self.transactionDate = payDate
        payment.updateExpiryDate(paidAmount)
        payment.put()
        self.put()
        
#    def getTenantTransactions(self,payment_key):
#        transactions = self.getAllTransactions()       
#        transactions_list = []
#        i = 1
#        for transaction in transactions:
#            if payment_key == transaction.payment.key():
#                tenant = transaction.payment.contract.tenant                
#                transactions_list.append({'transactionNumber': tenant.firstName + "_" + tenant.surname + "_" + str(i),'transactionDate': transaction.transactionDate.isoformat(), 'paidAmount': transaction.paidAmount})
#                i = i + 1
#        transactions_list.append({'totalPaidAmount':transaction.payment.totalPaidAmount}) 
#        return transactions_list
     