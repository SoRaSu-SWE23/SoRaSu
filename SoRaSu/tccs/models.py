from tccs import app, db, login_manager,get
from tccs import bcrypt
from flask_login import UserMixin, current_user
from enum import Enum
# from abc import ABC, abstractclassmethod
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

class Bill(db.Model):
    id = db.Column(db.String(length=30), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Double())
    consignment_id = db.Column(db.Integer(),db.ForeignKey('consignment.id'))
    branch_id = db.Column(db.Integer(),db.ForeignKey('office.id'))
    # consignmentid = db.relationship('Consignment',backref='item_bill',lazy=True)

    def getAmount(senderAddress,receiverAddress):
        return 100
    def getDate(self):
        return self.date
    def getPaymentID(self):
        return self.id
    def setDate(self,date):
        self.date = date
    def setAmount(self,amount):
        self.amount = amount

class Address(db.Model):
    __tablename__ = 'address'
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

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    consignments = db.relationship(
        "Consignment",backref='customer',lazy=True)
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password)->bool:
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    # def placeOrder(self,consignment):
    #     db.session.add(custom_consignment)
    #     db.session.commit()
    #     self.consignments.append(custom_consignment)
    #     return custom_consignment.consignmentID

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
    branchID = db.Column(db.Integer(),db.ForeignKey("office.id"))
    position = db.Column(db.String(length=30), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    role = db.Column(db.String(64))

    __mapper_args__ = {

        'polymorphic_identity': 'employee',
        'polymorphic_on': role
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

class ConsignmentStatus(Enum):
    PENDING = 0
    APPROVED = 1
    DISPATCHED =2
    ENROUTE = 3
    DELIVERED = 4

class TruckStatus(Enum):
    AVAILABLE = 0
    ASSIGNED = 1
    ENROUTE = 2

class Truck(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    truckNumber = db.Column(db.String(length=10))
    branch_id = db.Column(db.Integer())
    currentBranch = db.Column(db.Integer(), db.ForeignKey('office.id'),default=0)
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


class Office(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    rate = db.Column(db.Double(), nullable=False)
    officeAddressID = db.Column(db.Integer, db.ForeignKey('address.id'))
    officeAddress = db.relationship(
        'Address', uselist=False, foreign_keys=officeAddressID)
    employees = db.relationship(
        "Employee", uselist=True, lazy=False)

    transactions = db.relationship(
        "Bill", foreign_keys='Bill.branch_id', uselist=True, lazy=False)

    officePhone = db.Column(db.String(length=10), nullable=False)

    type = db.Column(db.String(length=10), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'office',
        'polymorphic_on': type
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    manager = db.relationship("Manager",foreign_keys='Manager.branchID' ,uselist=False,lazy=True,)
    __mapper_args__ = {
        'polymorphic_identity': 'head',
    }

 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def isBranch(self):
        return False

    def setRate(self, rate):
        self.rate = rate

    def returnRate(self):
        return self.rate

class BranchOffice(Office):
    idleTime = db.Column(db.Double())
    truckIDs = db.relationship(
        "Truck", foreign_keys='Truck.currentBranch', uselist=True, lazy=False)

    consignmentIDs = db.relationship(
        "Consignment", foreign_keys='Consignment.sourceBranchID', uselist=True, lazy=False)

    __mapper_args__ = {
        'polymorphic_identity': 'branch',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def isBranch(self):
        return True

    def viewTruckIDs(self):
        for truckID in self.truckIDS:
            pass          


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


class Consignment(db.Model):
    __tablename__ = 'consignment'
    id = db.Column(db.Integer(), primary_key=True)
    volume = db.Column(db.Double(), nullable=False)
    sender_name = db.Column(db.String(length=30))
    receiver_name = db.Column(db.String(length=30))

    senderAddress_id = db.Column(db.Integer(), db.ForeignKey('address.id'))
    receiverAddress_id = db.Column(db.Integer(), db.ForeignKey('address.id'))
    senderAddress = db.relationship('Address', uselist=False, foreign_keys=senderAddress_id)
    receiverAddress = db.relationship('Address', uselist=False, foreign_keys=receiverAddress_id)
    #change 1
    sourceBranchID = db.Column(db.Integer(), db.ForeignKey('office.id'),nullable=False)
    destinationBranchID = db.Column(db.Integer(),db.ForeignKey('office.id'), nullable=False)

    customer_id = db.Column(db.Integer(),db.ForeignKey('customer.id'))
    order_date_time = db.Column(db.DateTime())
    approval_date_time = db.Column(db.DateTime())

    dispatch_date_time = db.Column(db.DateTime())
    arrival_date_time = db.Column(db.DateTime())
    status = db.Column(db.Enum(ConsignmentStatus))
    charge = db.Column(db.Double())
    truck_id = db.Column(db.Integer(), db.ForeignKey('truck.id'))
    # Bill wala part bacha hai!
    bill_id = db.Column(db.Integer(),db.ForeignKey('bill.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.customer_id = current_user.id
        self.status = ConsignmentStatus.PENDING
        self.charge = 0.0
        self.order_date_time = timezone.localize(datetime.now())
        self.approval_date_time = datetime(1, 1, 1, 0, 0, 0, 0)
        self.dispatch_date_time = datetime(1, 1, 1, 0, 0, 0, 0)
        self.arrival_date_time = datetime(1, 1, 1, 0, 0, 0, 0)
        self.truck_id = 1


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
        return f'<Consignment: {self.id},Source Branch:{self.source_branch_id} , Destination Branch: {self.dest_branch_id}, Volume:{self.volume}, status: {self.status}>'



with app.app_context():
    db.create_all()
    address = Address(addr="ms",city="kharagpur",pincode="721302")
    db.session.add(address)
    db.session.commit()
    office = HeadOffice(rate=10,officeAddressID=address.id,officePhone="9090909")
    address1 = Address(addr="vs",city="kgp",pincode="123445") 
    db.session.add(address1)
    db.session.commit()
    b1 = BranchOffice(rate='10',officeAddressID=address1.id,officePhone="9843843",idleTime=23)
    db.session.add(office)
    db.session.add(b1)
    db.session.commit()


