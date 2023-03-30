from tccs import app,db, login_manager,get
from tccs import bcrypt
from flask_login import UserMixin
from datetime import datetime
from enum import Enum
import pytz
from abc import ABC,abstractclassmethod
timezone = pytz.timezone("Asia/Kolkata")

@login_manager.user_loader
def load_user(customer_id):
    user = get()
    if(user=="customer"):
        return Customer.query.get(int(customer_id))
    if(user=="employee"):
        return Employee.query.get(int(customer_id))

join_table = db.Table(
    'truck and consignment', db.Model.metadata, db.Column(
        'consignmentID', db.Integer, db.ForeignKey('Consignment.id')),
    db.Column('truckID', db.Integer, db.ForeignKey('Truck.id')))

consignment_customer = db.Table(
    'consignment_customer', db.Model.metadata, db.Column(
        'consignmentID', db.Integer, db.ForeignKey('Consignment.id')),
    db.Column('customerID', db.Integer, db.ForeignKey('Customer.id')))



class Address(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    addr = db.Column(db.String(length=100), nullable=False)
    city = db.Column(db.String(length=30), nullable=False)
    pincode = db.Column(db.String(length=6), nullable=False)
    itemid = db.relationship('Consignment',backref='address',lazy=True)

    def __init__(self, addr=None, city=None, pincode=None):
        self.addr = addr
        self.city = city
        self.pincode = pincode

    def __repr__(self):
        return f'<Address: {self.addr}' \
            f'City: {self.city} PIN: {self.pincode}>'

class ConsignmentStatus(Enum):
    PENDING = 0
    ENROUTE = 1
    ALLOTED = 2
    DELIVERED = 3
class Bill(db.Model):
    id = db.Column(db.String(length=30), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Double())
    consignmentid = db.relationship('Consignment',backref='item_bill',lazy=True)

    def getAmount(senderAddress,receiverAddress):
        return 100
    def getDate(self):
        return self.date
    def getPaymentID(self):
        return self.paymentID
    def setDate(self,date):
        self.date = date
    def setAmount(self,amount):
        self.amount = amount

class Consignment(db.Model):
    id = db.Column(db.String(), primary_key=True)
    volume = db.Column(db.Double(), nullable=False)
    customerUsername = db.Column(db.String(length=30), nullable=False)
    order_date_time = db.Column(db.DateTime())
    dispatch_date_time = db.Column(db.DateTime())
    arrival_date_time = db.Column(db.DateTime())
    sender_name = db.Column(db.String(length=30))
    receiver_name = db.Column(db.String(length=30))
    senderAddress = db.relationship("Address",db.ForeignKey('Address.id'))
    receiverAddress = db.relationship("Address",db.ForeignKey('Address.id'))
    status = db.Column(db.Enum(ConsignmentStatus))
    charge = db.Column(db.Double())
    sourceBranchID = db.Column(db.String(), nullable=False)
    destinationBranchID = db.Column(db.String(), nullable=False)

    item_bill = db.Column(db.Integer(),db.ForeignKey('Bill.id'))

    trucks = db.relationship(
        "Truck", secondary=join_table, back_populates="consignments")
    customers = db.relationship(
        "Customer", secondary=consignment_customer, back_populates="consignments")

    def __init__(self, volume, username, order_time,sender_name,receiver_name,sender_Address,receiver_Address, customer_id, srcbrnid, destbrnid):
        self.status = ConsignmentStatus.PENDING
        self.charge = 0.0
        self.order_date_time = timezone.localize(datetime.now())

    def getConsignmentId(self):
        return self.id

    def getVolume(self):
        return self.volume

    def getStatus(self):
        return self.status

    def getSourceBranch(self):
        return self.source_branch_id

    def getDestinationBranch(self):
        return self.dest_branch_id

    def getTruckId(self):
        return self.truckID

    def getCharge(self):
        return self.charge

    def setVolume(self, vol):
        self.volume = vol
        return

    def setStatus(self, status):
        self.status = status
        return

    def setSourceBranch(self, source_branch):
        self.source_branch_id = source_branch
        return

    def setDestinationBranch(self, dest_branch):
        self.dest_branch_id = dest_branch
        return

    def __repr__(self):
        return f'<Consignment: {self.consignment_id},Source Branch:{self.source_branch_id} , Destination Branch: {self.dest_branch_id}, Volume:{self.volume}, status: {self.status}>'

# @login_manager.user_loader
# def load_user(employee_id):
#     return Employee.query.get(int(employee_id))


class Customer(db.Model, UserMixin):
    id = db.Column(db.String(length=30), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    consignments = db.relationship(
        "Consignment", secondary=join_table, back_populates="customers")

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password)->bool:
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def placeOrder(self,volume,senderAddress:Address,receiverAddress:Address):
        sourceBranch = Office.query.filter_by(zipCode=senderAddress.zipCode).first()
        destinationBranch = Office.query.filter_by(zipCode=receiverAddress.zipCode).first()
        custom_consignment = Consignment(
            volume = volume,
            customerUsername = self.username,
            sourceBranchID = sourceBranch.officeID,
            destinationBranchID = destinationBranch.officeID,
            charge = Bill.getAmount(senderAddress,receiverAddress),
        )
        db.session.add(custom_consignment)
        db.session.commit()
        self.consignments.append(custom_consignment)
        return custom_consignment.consignmentID

    def viewTruckRouteDetails(consignmentID):
        current_consignment = Consignment.query.filter_by(consignmentID)
        return current_consignment.getStatus()
    
    def viewOrderHistory(self):
        return self.orderHistory


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    branchID = db.Column(db.Integer(), nullable=False)
    position = db.Column(db.String(length=30), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    role = db.Column(db.String(64))

    __mapper_args__ = {

        'polymorphic_identity': 'employee',
        'polymorphic_on': role
    }

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)
    def getUsername(self):
        return self.username
    
    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def getBranchID(self):
        return self.branchID
    
    def setUsername(self,username):
        self.username = username

    def setPassword(self,password):
        self.password_hash=bcrypt.generate_password_hash(password).decode('utf-8')
    
class Manager(Employee):
    __tablename__ = "manager"

    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }
    def queryConsignment(consignmentID):
        consignment = Consignment.query.filter_by(consignmentID=consignmentID).first()
        return consignment
    def viewWaitingPeriod():
        pass
    def viewIdleTime(officeID):
        idle_time = 0 
        office = Office.query.filter_by(officeID = officeID).first()
        return office.idleTime

    def viewTruckStatus(truckID):
        pass
    def changeRate(officeID,rate):
        office = Office.query.filter_by(officeID = officeID).first()
        office.rate = rate
    
    def createEmployee(username,name,email_address,branchID,position,password):
        user_to_create = Employee(username=username,
                                  name=name,
                                email_address=email_address,
                              branchID=branchID,
                              position=position,
                              password=password)
        db.session.add(user_to_create)
        db.session.commit()

    def viewTruckUsage():
        pass
  

class Office(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    officeAddress = db.relationship("Address",db.ForeignKey('Address.id'))
    officePhone = db.Column(db.String(length=10),nullable=False)
    employees = db.relationship("Employee")
    transactions = db.relationship("Bill")

    # @abstractclassmethod
    def getOfficeID(self):
        return self.id
    
    # @abstractclassmethod
    def getOfficeAddress(self):
        return self.officeAddress

    # @abstractclassmethod
    def getOfficePhone(self):
        return self.officePhone
    
    # @abstractclassmethod
    def setOfficeAddress(self,addr):
        self.officeAddress = addr

    def setOfficePhone(self,phone):
        self.officePhone = phone

    def addEmployee(self,e):
        pass

    def removeEmployee(self,id):
        pass

    # @abstractclassmethod
    def isBranch(self):
        pass  

    def addTransaction(self,b):
        pass

class TruckStatus(Enum):
    Available = 0
    Assigned = 1
    Enroute = 2

class Truck(db.Model):
    id = db.Column(db.String(length=30), primary_key=True)
    currentBranch = db.Column(db.Integer(), db.ForeignKey('Office.id'),default=0)
    status = db.Column(db.Enum(TruckStatus),default=TruckStatus.Available)
    volumeConsumed = db.Column(db.Double(), nullable=False, default=0)
    usageTime = db.Column(db.Integer(),default=0)
    idleTime = db.Column(db.Integer(),default=0)

    consignments = db.relationship(
        "Consignment", secondary=join_table, back_populates="trucks")

    @property
    def branchid(self):
        return self.branchid
    @branchid.setter
    def branchid(self,brancid_):
        branch = Office.query.filter_by(id=brancid_)
        self.currentBranch=branch.id

    def getTruckID(self):
        return self.id
    def getCurrentBranch(self):
        return self.currentBranch
    def getStatus(self):
        return self.status
    def getVolumeConsumed(self):
        return self.volumeConsumed
    def getUsageTime(self):
        return self.usageTime
    def getIdleTime(self):
        return self.idleTime
    def viewConsignment(self):
        return self.consignments
    def setCurrentBranch(self,e):
        self.currentBranch = e

    # def setStatus(self,e):
    #     self.status = TruckStatus.e

    def addVolumeConsumed(self,a):
        self.volumeConsumed +=a

    def updateUsageTime(self,t):
        self.usageTime = t
    def updateIdleTime(self,t):
        self.idleTime = t

    def addConsignment(self,consignment):
        if self.status == TruckStatus.Available:
            self.status = TruckStatus.Assigned
            self.consignments.append(consignment)
            consignment.trucks.append(self)
            self.volumeConsumed += consignment.volume
            consignment.status = ConsignmentStatus.ALLOTED

        elif self.status == TruckStatus.Assigned:
            self.consignments.append(consignment)
            consignment.trucks.append(self)
            self.volumeConsumed += consignment.volume
            consignment.status = ConsignmentStatus.ALLOTED

    def emptyTruck(self):
        consignments = self.consignments
        self.volumeConsumed = 0
        self.consignments =[]
        self.status = TruckStatus.Available
        for consignment in consignments :
            if self in consignment.trucks :
                consignment.trucks.remove(self)

with app.app_context():
    db.create_all()


