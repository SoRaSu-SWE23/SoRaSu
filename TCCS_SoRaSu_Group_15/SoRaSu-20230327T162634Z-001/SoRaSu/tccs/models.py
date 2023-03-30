from tccs import app, db, login_manager,get
from tccs import bcrypt
from flask_login import UserMixin
from enum import Enum
from abc import ABC,abstractclassmethod
from datetime import datetime
import pytz
timezone = pytz.timezone("Asia/Kolkata")


@login_manager.user_loader
def load_user(id):
    user = get()
    if user == "Customer":
        return Customer.query.get(int(id))
    elif user == "Employee":
        return Employee.query.get(int(id))


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50),
                              nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # orderHistory =db.Column(ARRAY(db.String), db.ForeignKey('Bill.id'))
    role = "Customer"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50),
                              nullable=False, unique=True)
    branchID = db.Column(db.Integer(), nullable=False)
    position = db.Column(db.String(length=30), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    

class Address(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    addr = db.Column(db.String(length=100), nullable=False)
    city = db.Column(db.String(length=30), nullable=False)
    pincode = db.Column(db.String(length=6), nullable=False)

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


class Consignment(db.Model):
    consignment_id = db.Column(db.String(), primary_key=True)
    volume = db.Column(db.Double(), nullable=False)
    customerUsername = db.Column(db.String(length=30), nullable=False)
    order_date_time = db.Column(db.DateTime())
    dispatch_date_time = db.Column(db.DateTime())
    arrival_date_time = db.Column(db.DateTime())
    sender_name = db.Column(db.String(length=30))
    receiver_name = db.Column(db.String(length=30))
    senderAddress = db.relationship("Address",db.ForeignKey('address.id'))
    receiverAddress = db.relationship("Address",db.ForeignKey('address.id'))
    status = db.Column(db.Enum(ConsignmentStatus))
    charge = db.Column(db.Double())
    customer_id = db.Column(db.String)
    sourceBranchID = db.Column(db.String(), nullable=False)
    destinationBranchID = db.Column(db.String(), nullable=False)
    truckID = db.Column(db.String())

    def __init__(self):
        self.status = ConsignmentStatus.PENDING
        self.charge = 0.0
        self.order_date_time = timezone.localize(datetime.now())

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


class Office(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    officeAddressID = db.Column(db.Integer, db.ForeignKey('address.id'))
    officeAddress = db.relationship('Address', uselist=False, foreign_keys=officeAddressID)
    employees = db.relationship("Employee", uselist=True, lazy=False)

    transactions = db.relationship(
        "Bill", foreign_keys='Bill.branchID', uselist=True, lazy=False)
    
    officePhone = db.Column(db.String(length=10), nullable=False)
    type = db.Column(db.String(length=10), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'office',
        'polymorphic_on': type
    }

    def getOfficeID(self):
        return self.officeID

    def getOfficeAddress(self):
        return self.officeAddress

    def getOfficePhone(self):
        return self.officePhone

    def setOfficeAddress(self, addr):
        self.officeAddress = addr

    def setOfficePhone(self, phone):
        self.officePhone = phone

    def addEmployee(self, e):
        pass

    def removeEmployee(self, id):
        pass

    def isBranch(self):
        pass

    def addTransaction(self, b):
        pass


class HeadOffice(Office):

    manager = db.relationship("Manager", db.ForeignKey('manager.id'))
    __mapper_args__ = {
        'polymorphic_identity': 'head',
    }
    rate = db.Column(db.Double(), nullable=False)

    def isBranch(self):
        return False

    def setRate(self, rate):
        self.rate = rate

    def returnRate(self):
        return self.rate


class BranchOffice(Office):
    # idleTime = db.Column(db.Double())

    truckIDs = db.relationship(
        "Truck", foreign_keys='Truck.branchID', uselist=True, lazy=False)

    consignmentIDs = db.relationship(
        "Consignment", foreign_keys='Consignment.sourceBranchID', uselist=True, lazy=False)

    __mapper_args__ = {
        'polymorphic_identity': 'branch',
    }

    def isBranch(self):
        return True

    def viewTruckIDs(self):
        return self.truckIDs

    def viewTransactions(self):
        return self.transactions

    def addTransaction(self, b):
        pass

    def addTruckID(self, id):
        pass

    def removeTruckID(self, id):
        pass

    def getIdleTime(self):
        return self.idleTime

    def updateIdleTime(self, t):
        self.idleTime = t

    def addConsignment(self, id):
        pass

    def getCurrentConsignments(self, id):
        return self.consignmentsID


with app.app_context():
    db.create_all()
