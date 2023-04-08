from tccs import app, change, get
from flask import render_template, redirect, url_for, flash, request
from tccs.models import Customer, Employee, Consignment, Address, Truck, ConsignmentStatus, Bill, Manager, Office, TruckStatus, EmployeeStatus, BranchOffice, HeadOffice
from tccs.forms import RegisterCustomerForm, RegisterEmployeeForm, LoginCustomerForm, LoginEmployeeForm, ConsignmentForm, TruckForm, BranchQueryForm, ApproveTruckForm, DispatchTruckForm, ReceiveTruckForm, ApproveIncomingTruckForm, TruckAvailableForm
from tccs import db
from flask_login import login_user, logout_user, current_user, login_required


# -------------------------------------------------------HOME PAGE-----------------------------------------------------------


@app.route('/')
@app.route('/home')
def home_page():
    if Office.query.count() == 0:
        address = Address(addr="IITKGP", city="Kharagpur", pincode="721302")
        db.session.add(address)
        db.session.commit()
        office = HeadOffice(
            rate=10, officeAddressID=address.id, officePhone="9090909")
        address1 = Address(addr="vs", city="kgp", pincode="123445")
        db.session.add(address1)
        db.session.commit()
        address2 = Address(addr="vs", city="pune", pincode="988989")
        db.session.add(address2)
        db.session.commit()
        b1 = BranchOffice(
            rate='10', officeAddressID=address1.id, officePhone="9843843")
        b2 = BranchOffice(
            rate='10 ', officeAddressID=address2.id, officePhone="9088978989")
        db.session.add(b1)
        db.session.add(b2)
        db.session.add(office)
        db.session.commit()
    if Customer.query.count() == 0:
        cus1 = Customer(username="cus1", name="cus1",
                        email_address="cus1@gmail.com", password="000000")
        db.session.add(cus1)
        db.session.commit()
    if Employee.query.count() == 0:
        manager = Manager(username="man1", name="manager1", email_address="man1@gmail.com",
                          branchID=3, position="Manager", password="000000")
        employee = Employee(username="emp1", name="employee1", email_address="emp1@gmail.com",
                            branchID=1, position="Employee", password="000000")
        driver = Employee(username="dri1", name="dri1", email_address="dri1@gmail.com",
                          branchID=1, position="Driver", password="000000")
        db.session.add(manager)
        db.session.add(employee)
        db.session.add(driver)
        db.session.commit()
    if Consignment.query.count() == 0:
        a = Address(addr="MS Hall", city="Kharagpur", pincode="721302")
        db.session.add(a)
        db.session.commit()
        b = Address(addr="Trillium", city="Pune", pincode="411034")
        db.session.add(b)
        db.session.commit()
        bill = Bill(amount=100, branch_id=1)
        db.session.add(bill)
        db.session.commit()
        c = Consignment(volume=100, sender_name="Sukhomay", receiver_name="Soukhin", bill_id=bill.id, customer_id=cus1.id,
                        senderAddress_id=a.id, receiverAddress_id=b.id, sourceBranchID=1,
                        destinationBranchID=2)
        db.session.add(c)
        db.session.commit()
    if Truck.query.count() == 0:
        truck = Truck(branch_id=1, truckNumber="MH047856")
        db.session.add(truck)
        db.session.commit()
        truck.setArrivalTime()
        return redirect(f'/allocate_truck/{truck.branch_id}')
    return render_template('home.html')

# -------------------------------------------------------CUSTOMER PAGE-----------------------------------------------------------


@app.route('/customer')
def customer_page():
    return render_template('customer.html')

# -------------------------------------------------------MANAGER PAGE-----------------------------------------------------------


@app.route('/manager')
def manager_page():
    return render_template('manager.html')

# -------------------------------------------------------EMPLOYEE PAGE-----------------------------------------------------------


@app.route('/employee')
def employee_page():
    return render_template('employee.html')

# -------------------------------------------------------DRIVER PAGE-----------------------------------------------------------


@app.route('/driver')
def driver_page():
    return render_template('driver.html')

# -------------------------------------------------------DASHBOARD PAGE-----------------------------------------------------------


@app.route('/dashboard')
def dashboard_page():
    if get() == "customer":
        return redirect(url_for('customer_page'))
    elif get() == "employee":
        if current_user.role == "manager":
            return redirect(url_for('manager_page'))
        elif current_user.position == "driver" or current_user.position == "Driver":
            return redirect(url_for('driver_page'))
        else:
            return redirect(url_for('employee_page'))

# -------------------------------------------------------REGISTER PAGES-----------------------------------------------------------


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return render_template('register.html')


@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer_page():
    form = RegisterCustomerForm()
    if form.validate_on_submit():
        user_to_create = Customer(username=form.username.data,
                                  name=form.name.data,
                                  email_address=form.email_address.data,
                                  password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        change("customer")
        login_user(user_to_create)
        flash(
            f"successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('customer_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register_customer.html', form=form)


@app.route('/register_employee', methods=['GET', 'POST'])
def register_employee_page():
    offices = Office.query.all()
    office_ids = [(i.id, i.officeAddress.city) for i in offices]
    form = RegisterEmployeeForm()
    form.branchID.choices = office_ids
    if form.validate_on_submit():
        # ***************************RAJ CHANGE******************************************
        if form.position.data == "Manager" or form.position.data == "manager":
            user_to_create = Manager(username=form.username.data,
                                     name=form.name.data,
                                     email_address=form.email_address.data,
                                     branchID=form.branchID.data,
                                     position=form.position.data,
                                     password=form.password1.data)
        else:
            user_to_create = Employee(username=form.username.data,
                                      name=form.name.data,
                                      email_address=form.email_address.data,
                                      branchID=form.branchID.data,
                                      position=form.position.data,
                                      password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        change("employee")
        login_user(user_to_create)
        # ***************************RAJ CHANGE******************************************
        if user_to_create.role == 'manager':
            flash(
                f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
            return redirect(url_for('manager_page'))
        elif user_to_create.role == 'employee' and (user_to_create.position == 'driver' or user_to_create.position == 'Driver'):
            flash(
                f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
            return redirect(url_for('driver_page'))
        else:
            flash(
                f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
            return redirect(url_for('employee_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register_employee.html', form=form)

# -------------------------------------------------------LOGIN/LOGOUT PAGES-----------------------------------------------------------


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')


@app.route('/login_customer', methods=['GET', 'POST'])
def login_customer_page():
    form = LoginCustomerForm()
    if form.validate_on_submit():
        attempted_user = Customer.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            change("customer")
            login_user(attempted_user)
            flash(
                f"You are logged in as: {attempted_user.username}", category='success')
            return redirect(url_for('customer_page'))
        else:
            flash("Please try again", category='danger')
    return render_template('login_customer.html', form=form)


@app.route('/login_employee', methods=['GET', 'POST'])
def login_employee_page():
    form = LoginEmployeeForm()
    if form.validate_on_submit():
        attempted_user = Employee.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            change("employee")
            login_user(attempted_user)
            # ***************************RAJ CHANGE******************************************
            if attempted_user.role == 'manager':
                flash(
                    f"Account created successfully! You are now logged in as {attempted_user.username}", category='success')
                return redirect(url_for('manager_page'))
            elif attempted_user.role == 'employee' and (attempted_user.position == 'driver' or attempted_user.position == 'Driver'):
                flash(
                    f"Account created successfully! You are now logged in as {attempted_user.username}", category='success')
                return redirect(url_for('driver_page'))
            else:
                flash(
                    f"Account created successfully! You are now logged in as {attempted_user.username}", category='success')
                return redirect(url_for('employee_page'))
        else:
            flash("Please try again", category='danger')
    return render_template('login_employee.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for("home_page"))


# -------------------------------------------------------PLACE_CONSIGNMENT PAGE-----------------------------------------------------------

@app.route('/place_consignment', methods=['GET', 'POST'])
def place_consignment_page():
    offices = Office.query.filter_by(type="branch")
    office_ids = [(i.id, i.officeAddress.city) for i in offices]
    form = ConsignmentForm()
    form.dispatch_branch.choices = office_ids
    form.receiver_branch.choices = office_ids
    if form.validate_on_submit():

        senderName = form.sender_name.data
        senderAddress = Address(addr=form.senderAddressLine.data,
                                city=form.sender_city.data, pincode=form.senderPincode.data)
        db.session.add(senderAddress)
        db.session.commit()
        receiverName = form.receiver_name.data
        receiverAddress = Address(addr=form.receiverAddressLine.data,
                                  city=form.receiver_city.data, pincode=form.receiverPincode.data)
        db.session.add(receiverAddress)
        db.session.commit()
        bill = Bill(amount=100, branch_id=senderAddress.id)
        db.session.add(bill)
        db.session.commit()
        consignment_to_create = Consignment(volume=form.volume.data,
                                            bill_id=bill.id,
                                            customer_id=current_user.id,
                                            sender_name=senderName,
                                            receiver_name=receiverName,
                                            senderAddress_id=senderAddress.id,
                                            receiverAddress_id=receiverAddress.id,
                                            sourceBranchID=form.dispatch_branch.data,
                                            destinationBranchID=form.receiver_branch.data)
        db.session.add(consignment_to_create)
        db.session.commit()

        flash(
            f"Consignment {consignment_to_create.id} created successfully by {current_user.username}", category="success")
        return redirect(f'/allocate_truck/{consignment_to_create.sourceBranchID}')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There is was error creating a consignment:{err_msg}', category='danger')
    return render_template('place_consignment.html', form=form)

# -------------------------------------------------------ALLOCATE_TRUCK FUNCTION-----------------------------------------------------------


@app.route('/allocate_truck/<token>')
def allocate_truck_page(token):
    pending_consignemnts = list(Consignment.query.filter_by(
        sourceBranchID=token, status=ConsignmentStatus.PENDING))
    available_trucks = list(Truck.query.filter_by(
        branch_id=token, status=TruckStatus.AVAILABLE))
    assigned_trucks = list(Truck.query.filter_by(
        branch_id=token, status=TruckStatus.ASSIGNED))

    for consignment in pending_consignemnts:
        for truck in assigned_trucks:
            if truck.destinationBranch == consignment.destinationBranchID and (truck.volumeConsumed + consignment.volume) <= 500:
                truck.addVolumeConsumed(consignment.volume)
                consignment.setTruckId(truck.id)
                consignment.setStatus(ConsignmentStatus.APPROVED)
                consignment.setApprovalDateTime()
                print(consignment.approval_date_time)
                break
        if consignment.status == ConsignmentStatus.PENDING:
            for truck in available_trucks:
                truck.setStatus(TruckStatus.ASSIGNED)
                truck.setDestinationBranch(consignment.destinationBranchID)
                truck.addVolumeConsumed(consignment.volume)
                consignment.setTruckId(truck.id)
                consignment.setStatus(ConsignmentStatus.APPROVED)
                consignment.setApprovalDateTime()
                print(consignment.approval_date_time)
                available_trucks.remove(truck)
                assigned_trucks.append(truck)
                break

    return redirect(url_for("dashboard_page"))


# -------------------------------------------------------ADD_NEW_TRUCK PAGE-----------------------------------------------------------

@app.route('/add_truck', methods=['GET', 'POST'])
def add_truck_page():
    offices = Office.query.filter_by(type="branch")
    office_ids = [(i.id, i.officeAddress.city) for i in offices]
    form = TruckForm()
    form.branchID.choices = office_ids
    if form.validate_on_submit():
        truck_to_create = Truck(branch_id=form.branchID.data,
                                truckNumber=form.truckNumber.data)
        truck_to_create.setArrivalTime()
        db.session.add(truck_to_create)
        db.session.commit()
        flash(f"Truck added successfully!", category='success')
        return redirect(f'/allocate_truck/{truck_to_create.branch_id}')
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with adding a truck {err_msg}', category='danger')

    return render_template('add_new_truck.html', form=form)

# -------------------------------------------------------BRANCH_QUERY PAGE-----------------------------------------------------------


@app.route('/branch_query', methods=['GET', 'POST'])
def branch_query_page():
    form = BranchQueryForm()
    # if form.validate_on_submit():
    #     attempted_user = Customer.query.filter_by(username=form.username.data).first()
    #     if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
    #         change("customer")
    #         login_user(attempted_user)
    #         current_user = attempted_user
    #         flash(f"You are logged in as: {attempted_user.username}",category='success')
    #         return redirect(url_for('customer_page'))
    #     else:
    #         flash("Please try again",category='danger')
    return render_template('branch_query.html', form=form)


# -------------------------------------------------------ORDER_HISTORY(CUSTOMER) PAGE-----------------------------------------------------------

@app.route('/order_history')
def order_history_page():
    consignments = current_user.consignments
    consignments.reverse()
    return render_template('order_history.html', consignments=consignments)

# -------------------------------------------------------VIEW ALL CONSIGNMENTS(EMPLOYEE) PAGE-----------------------------------------------------------


@app.route('/view_consignment_status/<token>')
def view_consignment_page(token):
    consignments = list(Consignment.query.filter_by(sourceBranchID=token))
    consignments.reverse()
    branches = Office.query.all()
    branch_city = {}
    for branch in branches:
        branch_city[int(branch.id)] = branch.officeAddress.city
    return render_template('view_consignment_status.html', consignments=consignments, branch_city=branch_city)
# -------------------------------------------------------VIEW PENDING CONSIGNMENTS(EMPLOYEE) PAGE-----------------------------------------------------------


@app.route('/view_consignment_status/<token>/pending')
def branch_pending_consignments_page(token):
    consignments = list(Consignment.query.filter_by(
        sourceBranchID=token, status=ConsignmentStatus.PENDING))
    consignments.reverse()
    branches = Office.query.all()
    branch_city = {}
    for branch in branches:
        print(branch.officeAddress.city)
        branch_city[int(branch.id)] = branch.officeAddress.city
    return render_template('view_consignment_status.html', consignments=consignments, branch_city=branch_city)

# -------------------------------------------------------TRACK_CONSIGNMENT(CUSTOMER) PAGE-----------------------------------------------------------


@app.route('/track_consignment/<token>')
@login_required
def track_consignment_page(token):
    consignment = Consignment.query.filter_by(id=token).first()
    return render_template('track_consignment.html', consignment=consignment, ConsignmentStatus=ConsignmentStatus)


# -------------------------------------------------------INVOICE(CUSTOMER) PAGE-----------------------------------------------------------

@app.route('/invoice/<token>')
@login_required
def invoice_page(token):
    consignment = Consignment.query.filter_by(id=token).first()
    bill = Bill.query.filter_by(id=consignment.bill_id).first()
    # return render_template('track_consignment.html',consignment=consignment, ConsignmentStatus=ConsignmentStatus)
    return render_template('invoice.html', bill=bill, consignment=consignment)

# -------------------------------------------------------VIEW CONSIGNMENTS(MANAGER) PAGE-----------------------------------------------------------


@app.route('/view_consignment_status', methods=["GET", "POST"])
def view_consignment_status_page():
    consignments = list(Consignment.query.all())
    consignments.reverse()
    branches = Office.query.all()
    branch_city = {}
    for branch in branches:
        branch_city[int(branch.id)] = branch.officeAddress.city

    return render_template('view_consignment_status.html', consignments=consignments, branch_city=branch_city)


# -------------------------------------------------------VIEW TRUCK STATUS(MANAGER) PAGE-----------------------------------------------------------
@app.route('/view_truck_status', methods=["GET", "POST"])
def view_truck_status_page():
    approve_form = ApproveTruckForm()
    if request.method == "POST":
        approved_truck = request.form.get('approve_truck')
        approved_truck_object = Truck.query.filter_by(
            id=approved_truck).first()
        if approved_truck_object:
            approved_truck_object.allocate_driver(
                approved_truck_object.branch_id)
            flash(
                f"Truck {approved_truck_object.id} with truck number {approved_truck_object.truckNumber} is assigned", category="success")
        else:
            flash("Truck not approved", category="danger")
        return redirect(url_for('view_truck_status_page'))
    if request.method == "GET":
        trucks = list(Truck.query.all())
        trucks.reverse()
        branches = Office.query.all()
        branch_city = {}
        for branch in branches:
            branch_city[int(branch.id)] = branch.officeAddress.city
        return render_template('view_truck_status.html', trucks=trucks, branch_city=branch_city, approve_form=approve_form)


# -------------------------------------------------------VIEW TRUCK STATUS(EMPLOYEE) PAGE-----------------------------------------------------------
@app.route('/view_truck_status/<token>', methods=["GET", "POST"])
def view_branch_truck_status_page(token):
    approve_form = ApproveTruckForm()
    if request.method == "POST":
        approved_truck = request.form.get('approve_truck')
        approved_truck_object = Truck.query.filter_by(
            id=approved_truck).first()
        if approved_truck_object:
            approved_truck_object.allocate_driver(token)
            flash(
                f"Truck {approved_truck_object.id} with truck number {approved_truck_object.truckNumber} is assigned", category="success")
        else:
            flash("Truck not approved", category="danger")
        return redirect(f'/view_truck_status/{token}')

    if request.method == "GET":
        trucks = list(Truck.query.filter_by(branch_id=token))
        trucks.reverse()
        branches = Office.query.all()
        branch_city = {}
        for branch in branches:
            branch_city[int(branch.id)] = branch.officeAddress.city
        return render_template('view_truck_status.html', trucks=trucks, branch_city=branch_city, approve_form=approve_form)


# # -------------------------------------------------------ALLOCATE_Driver FUNCTION-----------------------------------------------------------
# @app.route('/allocate_driver/<token>', methods=["GET", "POST"])
# def allocate_driver_page(token):
#     # available_trucks = list(Truck.query.filter_by(branch_id = token, status = TruckStatus.AVAILABLE))
#     assigned_trucks = list(Truck.query.filter_by(
#         branch_id=token, status=TruckStatus.ASSIGNED))
#     drivers = list(Employee.query.filter_by(
#         branchID=token, status=EmployeeStatus.AVAILABLE, position="Driver"))
#     print("***************************")
#     print(assigned_trucks)
#     print(drivers)
#     for driver in drivers:
#         for truck in assigned_trucks:
#             truck.setDriverID(driver.id)
#             truck.setStatus(TruckStatus.DISPATCHED)
#             driver.setStatus(EmployeeStatus.BUSY)
#             consignments = list(Consignment.query.filter_by(truck_id=truck.id))
#             for consignment in consignments:
#                 consignment.setStatus(ConsignmentStatus.DISPATCHED)
#             assigned_trucks.remove(truck)
#             break

#     return redirect(url_for("dashboard_page"))

# -------------------------------------------------------AVG WAITING TIME(MANAGER)-----------------------------------------------------------
@app.route('/avg_wait_time_consignment', methods=["GET", "POST"])
def avg_wait_time_consignment_page():
    branches = Office.query.filter_by(type="branch")
    branch_city = {}
    for branch in branches:
        branch_city[int(branch.id)] = branch.officeAddress.city
        if branch.type == 'branch':
            print(
                "*************************************************************************************")
            branch.calAvgWaitTime()
    return render_template('avg_wait_time_consignment.html', branches=branches)

# -------------------------------------------------------DRIVER TRUCK PAGE-----------------------------------------------------------


@app.route('/view_assigned_truck/<token>', methods=["GET", "POST"])
def driver_truck_page(token):
    dispatch_form = DispatchTruckForm()
    if request.method == "POST":
        dispatched_truck = request.form.get('dispatch_truck')
        dispatched_truck_object = Truck.query.filter_by(
            id=dispatched_truck).first()
        if dispatched_truck_object:
            dispatched_truck_object.setStatus(TruckStatus.ENROUTE)
            dispatched_truck_object.setDispatchTime()
            dispatched_truck_object.updateIdleTime()
            consignments = list(Consignment.query.filter_by(
                truck_id=dispatched_truck_object.id))
            for consignment in consignments:
                consignment.setDispatchDateTime()
                consignment.setStatus(ConsignmentStatus.ENROUTE)
            flash(
                f"TRUCK {dispatched_truck_object.id} of volume {dispatched_truck_object.volumeConsumed} cubic meters is enroute", category="success")
        else:
            flash(
                f"Consignment {dispatched_truck_object.id} of volume {dispatched_truck_object.volumeConsumed} cubic meters is not enroute", category="danger")
        return redirect(url_for('dashboard_page'))

    if request.method == "GET":
        trucks = list(Truck.query.filter_by(driverID=token))
        branches = Office.query.all()
        branch_city = {}
        for branch in branches:
            branch_city[int(branch.id)] = branch.officeAddress.city
        return render_template('driver_truck_assigned.html', trucks=trucks, branch_city=branch_city, dispatch_form=dispatch_form)

# -------------------------------------------------------DRIVER TRUCK RECEIVE PAGE-----------------------------------------------------------


@app.route('/driver_truck_receive/<token>', methods=["GET", "POST"])
def driver_truck_receive_page(token):
    receive_truck_form = ReceiveTruckForm()
    if request.method == "POST":
        received_truck = request.form.get('receive_truck')
        received_truck_object = Truck.query.filter_by(
            id=received_truck).first()
        if received_truck_object:
            received_truck_object.setStatus(TruckStatus.AVAILABLE)
            current_user.setStatus(EmployeeStatus.AVAILABLE)
            flash(f"TRUCK {received_truck_object.id} of volume {received_truck_object.volumeConsumed} cubic meters has reached the destination", category="success")
        else:
            flash(
                f"Consignment {received_truck_object.id} of volume {received_truck_object.volumeConsumed} cubic meters has not reached the destination", category="danger")
        return redirect(url_for('dashboard_page'))

    if request.method == "GET":
        trucks = list(Truck.query.filter_by(driverID=token))
        branches = Office.query.all()
        branch_city = {}
        for branch in branches:
            branch_city[int(branch.id)] = branch.officeAddress.city
        return render_template('driver_truck_receive.html', trucks=trucks, branch_city=branch_city, receive_truck_form=receive_truck_form)

# -------------------------------------------------------VIEW INCOMING TRUCK STATUS(EMPLOYEE) PAGE-----------------------------------------------------------


@app.route('/view_incoming_truck_status/<token>', methods=["GET", "POST"])
def view_incoming_truck_status_page(token):
    approve_incoming_form = ApproveIncomingTruckForm()
    if request.method == "POST":
        approved_incoming = request.form.get('approve_incoming_truck')
        approved_incoming_object = Truck.query.filter_by(
            id=approved_incoming).first()
        if approved_incoming_object:
            approved_incoming_object.setStatus(TruckStatus.ENROUTE)
            temp = approved_incoming_object.branch_id
            # approved_incoming_object.setSourceBranch(
            #     approved_incoming_object.destinationBranch)
            approved_incoming_object.setDestinationBranch(temp)
            approved_incoming_object.setVolumeConsumed(0)
            consignments = list(Consignment.query.filter_by(
                truck_id=approved_incoming_object.id))
            for consignment in consignments:
                consignment.setStatus(ConsignmentStatus.DELIVERED)
                consignment.setArrivalDateTime()
            flash(
                f"Incoming Truck {approved_incoming_object.id} with truck number {approved_incoming_object.truckNumber} is approved", category="success")
        else:
            flash("Incoming Truck not approved", category="danger")
        return redirect(f'/view_incoming_truck_status/{token}')

    if request.method == "GET":
        trucks = list(Truck.query.filter_by(destinationBranch=token))
        trucks.reverse()
        branches = Office.query.all()
        branch_city = {}
        for branch in branches:
            branch_city[int(branch.id)] = branch.officeAddress.city
        return render_template('view_incoming_truck_status.html', trucks=trucks, branch_city=branch_city, approve_incoming_form=approve_incoming_form)

# -------------------------------------------------------VIEW AVG TRUCK IDLE TIME-----------------------------------------------------------


@app.route('/view_truck_idle_time', methods=['GET', 'POST'])
def view_truck_idle_time_page():
    trucks = Truck.query.all()
    branches = Office.query.all()
    branch_city = {}
    for branch in branches:
        branch_city[int(branch.id)] = branch.officeAddress.city
    return render_template('avg_truck_idle_time.html', trucks=trucks, branch_city=branch_city)

# -------------------------------------------------------MAKE TRUCK AVAILABLE(DRIVER) PAGE-----------------------------------------------------------


@app.route('/driver_truck_available/<token>', methods=['GET', 'POST'])
def driver_truck_available_page(token):
    truck_available_form = TruckAvailableForm()
    if request.method == "POST":
        truck_available = request.form.get('truck_available')
        truck_available_object = Truck.query.filter_by(
            id=truck_available).first()
        if truck_available_object:
            truck_available_object.setStatus(TruckStatus.AVAILABLE)
            current_user.setStatus(EmployeeStatus.AVAILABLE)
            truck_available_object.setArrivalTime()
            truck_available_object.setSourceBranch(truck_available_object.destinationBranch)
            truck_available_object.setDestinationBranch(None)
            truck_available_object.setDriverID(None)
            flash(f"Truck {truck_available_object.id} with truck number { truck_available_object.truckNumber } is now available", category="success")
        else:
            flash(
                f"Truck {truck_available_object.id} with truck number { truck_available_object.truckNumber } is not available", category="danger")
        return redirect(url_for('dashboard_page'))

    if request.method == "GET":
        trucks = list(Truck.query.filter_by(driverID=token,volumeConsumed=0))
        branches = Office.query.all()
        branch_city = {}
        for branch in branches:
            branch_city[int(branch.id)] = branch.officeAddress.city
        return render_template('driver_truck_available.html', trucks=trucks, branch_city=branch_city, truck_available_form=truck_available_form)
    
# -------------------------------------------------------BRANCH CONSIGNMENT HANDLING-----------------------------------------------------------
@app.route('/branch_consignment_handling')
def branch_consignment_handling_page():
    all_consignments = list(Consignment.query.all())
    all_branches = list(Office.query.filter_by(type="branch"))
    pending_list = {}
    enroute_list = {}
    delivered_list = {}
    all_branch_city = {}
    waiting_time_list = {}
    for consignment in all_consignments:
        branch_city = Office.query.filter_by(id=consignment.sourceBranchID).first().officeAddress.city
        all_branch_city[branch_city] = branch_city
        waiting_time_list[branch_city] = Office.query.filter_by(id=consignment.sourceBranchID).first().avg_waiting_time
        pending_list[branch_city] = 0
        enroute_list[branch_city] = 0   
        delivered_list[branch_city] = 0
    for consignment in all_consignments:
        branch_city = Office.query.filter_by(id=consignment.sourceBranchID).first().officeAddress.city
        if consignment.status == ConsignmentStatus.PENDING:
            pending_list[branch_city] += 1
        elif consignment.status != ConsignmentStatus.PENDING and consignment.status != ConsignmentStatus.DELIVERED:
            enroute_list[branch_city] += 1    
        else:
            delivered_list[branch_city] += 1

    return render_template('branch_consignment_handling.html', pending_list=pending_list, enroute_list=enroute_list, delivered_list=delivered_list, all_branch_city=all_branch_city, waiting_time_list=waiting_time_list)
