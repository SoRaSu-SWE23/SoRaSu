from tccs import app, db, login_manager,get
from tccs import bcrypt
from flask_login import UserMixin, current_user
from enum import Enum
from abc import ABC, abstractclassmethod
from datetime import datetime
import pytz
timezone = pytz.timezone("Asia/Kolkata")

@login_manager.user_loader
def load_user(customer_id):
    user = get()
    if(user=="customer"):
        return Customer.query.get(int(customer_id))
    if(user=="employee"):
        return Employee.query.get(int(customer_id))


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # orderHistory =db.Column(ARRAY(db.String), db.ForeignKey('Bill.id'))
    
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    branchID = db.Column(db.Integer(), nullable=False)
    position = db.Column(db.String(length=30), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)
    

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer(), primary_key=True)
    addr = db.Column(db.String(length=100), nullable=False)
    city = db.Column(db.String(length=30), nullable=False)
    pincode = db.Column(db.String(length=6), nullable=False)

    # def __init__(self, addr=None, city=None, pincode=None):
    #     self.addr = addr
    #     self.city = city
    #     self.pincode = pincode

    def __repr__(self):
        return f'<Address: {self.addr}' \
            f'City: {self.city} PIN: {self.pincode}>'

class ConsignmentStatus(Enum):
    PENDING = 0
    ENROUTE = 1
    ALLOTED = 2
    DELIVERED = 3

class Consignment(db.Model):
    __tablename__ = 'consignment'
    consignment_id = db.Column(db.Integer(), primary_key=True)
    volume = db.Column(db.Double(), nullable=False)
    sender_name = db.Column(db.String(length=30))
    receiver_name = db.Column(db.String(length=30))
    senderAddress_id = db.Column(db.Integer(), db.ForeignKey('address.id'))
    receiverAddress_id = db.Column(db.Integer(), db.ForeignKey('address.id'))
    senderAddress = db.relationship('Address', uselist=False, foreign_keys=senderAddress_id)
    receiverAddress = db.relationship('Address', uselist=False, foreign_keys=receiverAddress_id)
    sourceBranchID = db.Column(db.Integer(), nullable=False)
    destinationBranchID = db.Column(db.Integer(), nullable=False)
    customer_id = db.Column(db.Integer())
    order_date_time = db.Column(db.DateTime())
    dispatch_date_time = db.Column(db.DateTime())
    arrival_date_time = db.Column(db.DateTime())
    status = db.Column(db.Enum(ConsignmentStatus))
    charge = db.Column(db.Double())
    truck_id = db.Column(db.Integer(), db.ForeignKey('truck.id'))
    # Bill wala part bacha hai!

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.customer_id = current_user.id
        self.status = ConsignmentStatus.PENDING
        self.charge = 0.0
        self.order_date_time = timezone.localize(datetime.now())
        self.dispatch_date_time = timezone.localize(datetime.now())
        self.arrival_date_time = timezone.localize(datetime.now())
        self.truck_id = 1


    def getConsignmentId(self):
        return self.consignment_id

    def getVolume(self):
        return self.volume

    def getStatus(self):
        return self.status

    def getSourceBranch(self):
        return self.source_branch_id

    def getDestinationBranch(self):
        return self.dest_branch_id

    def getTruckId(self):
        return self.truck_id

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


class TruckStatus(Enum):
    AVAILABLE = 0
    ASSIGNED = 1
    ENROUTE = 2

class Truck(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    truckNumber = db.Column(db.String(length=10))
    branch_id = db.Column(db.Integer())
    # currentBranch = db.Column(db.Integer(), db.ForeignKey('Office.id'),default=0)
    status = db.Column(db.Enum(TruckStatus))
    volumeConsumed = db.Column(db.Double(), nullable=False, default=0) # Volume consumed is in metre cube
    usageTime = db.Column(db.Integer(),default=0) # Usage time is in hours
    idleTime = db.Column(db.Integer(),default=0) # Idle time is in hours

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.status = TruckStatus.AVAILABLE
        self.volumeConsumed = 0.00
        self.usageTime = 0.00
        self.idleTime = 0.00
    # consignments = db.relationship(
    #     "Consignment", secondary=join_table, back_populates="trucks")

    # @property
    # def branchid(self):
    #     return self.branchid
    # @branchid.setter
    # def branchid(self,brancid_):
    #     branch = Office.query.filter_by(id=brancid_)
    #     self.currentBranch=branch.id

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
