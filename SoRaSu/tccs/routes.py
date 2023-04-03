from tccs import app, change, get
from flask import render_template, redirect, url_for, flash, request
from tccs.models import Customer, Employee, Consignment, Address, Truck, ConsignmentStatus, Bill, Manager, Office, TruckStatus, EmployeeStatus
from tccs.forms import RegisterCustomerForm, RegisterEmployeeForm, LoginCustomerForm, LoginEmployeeForm, ConsignmentForm, TruckForm, BranchQueryForm, ApproveTruckForm ,DispatchTruckForm , ReceiveTruckForm , ApproveIncomingTruckForm
from tccs import db
from flask_login import login_user, logout_user, current_user, login_required

# -------------------------------------------------------HOME PAGE-----------------------------------------------------------


@app.route('/')
@app.route('/home')
def home_page():
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
    form = RegisterEmployeeForm()
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
            current_user = attempted_user
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
    form = ConsignmentForm()
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
                break
        if consignment.status == ConsignmentStatus.PENDING:
            for truck in available_trucks:
                truck.setStatus(TruckStatus.ASSIGNED)
                truck.setDestinationBranch(consignment.destinationBranchID)
                truck.addVolumeConsumed(consignment.volume)
                consignment.setTruckId(truck.id)
                consignment.setStatus(ConsignmentStatus.APPROVED)
                consignment.setApprovalDateTime()
                available_trucks.remove(truck)
                assigned_trucks.append(truck)
                break

    return redirect(url_for("dashboard_page"))


# -------------------------------------------------------ADD_NEW_TRUCK PAGE-----------------------------------------------------------

@app.route('/add_truck', methods=['GET', 'POST'])
def add_truck_page():
    form = TruckForm()
    if form.validate_on_submit():
        truck_to_create = Truck(branch_id=form.branchID.data,
                                truckNumber=form.truckNumber.data)
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


@app.route('/view_consignment_status')
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
    trucks = list(Truck.query.all())
    trucks.reverse()
    branches = Office.query.all()
    branch_city = {}
    for branch in branches:
        branch_city[int(branch.id)] = branch.officeAddress.city
    return render_template('view_truck_status.html', trucks=trucks, branch_city=branch_city)


# -------------------------------------------------------VIEW TRUCK STATUS(EMPLOYEE) PAGE-----------------------------------------------------------
@app.route('/view_truck_status/<token>', methods=["GET", "POST"])
def view_branch_truck_status_page(token):
    approve_form = ApproveTruckForm()
    if request.method == "POST":
        approved_truck = request.form.get('approve_truck')
        approved_truck_object = Truck.query.filter_by(
            id=approved_truck).first()
        if approved_truck_object:
            redirect(f'allocate_driver/{ token }')
            flash(
                f"Truck {approved_truck_object.id} with truck number {approved_truck_object.truckNumber} is assigned", category="success")
        else:
            flash("Truck not approved", category="danger")
        return redirect(url_for('view_truck_status_page'))

    if request.method == "GET":
        trucks = list(Truck.filter_by(branch_id=token))
        trucks.reverse()
        branches = Office.query.all()
        branch_city = {}
        for branch in branches:
            branch_city[int(branch.id)] = branch.officeAddress.city
        return render_template('view_truck_status.html', trucks=trucks, branch_city=branch_city, approve_form=approve_form)


# -------------------------------------------------------ALLOCATE_TRUCK FUNCTION-----------------------------------------------------------
@app.route('/allocate_driver/<token>')
def allocate_driver_page(token):
    # available_trucks = list(Truck.query.filter_by(branch_id = token, status = TruckStatus.AVAILABLE))
    assigned_trucks = list(Truck.query.filter_by(
        branch_id=token, status=TruckStatus.ASSIGNED))
    drivers = list(Employee.query.filter_by(
        branchID=token, status=EmployeeStatus.AVAILABLE, position="Driver"))

    for driver in drivers:
        for truck in assigned_trucks:
            truck.setDriverID(driver.id)
            truck.setStatus(TruckStatus.DISPATCHED)
            driver.setStatus(EmployeeStatus.BUSY)
            consignments = list(Consignment.query.filter_by(truck_id=truck.id))
            for consignment in consignments:
                consignment.setStatus(ConsignmentStatus.DISPATCHED)
            assigned_trucks.remove(truck)
            break

    return redirect(url_for("dashboard_page"))

# -------------------------------------------------------AVG WAITING TIME(MANAGER)-----------------------------------------------------------
@app.route('/avg_wait_time_consignment',methods=["GET","POST"])
def avg_wait_time_consignment_page():
    branches = Office.query.all()
    branch_city={}
    for branch in branches:
        branch_city[int(branch.id)]= branch.officeAddress.city 
        branch.calAvgWaitTime()        

    return render_template('avg_wait_time_consignment.html',branches=branches)

# -------------------------------------------------------DRIVER TRUCK PAGE-----------------------------------------------------------
@app.route('/view_assigned_truck/<token>',methods=["GET","POST"])
def driver_truck_page(token):
    dispatch_form = DispatchTruckForm()
    if request.method == "POST":
        dispatched_truck = request.form.get('dispatch_truck')
        dispatched_truck_object = Truck.query.filter_by(id=dispatched_truck).first()
        if dispatched_truck_object:
            dispatched_truck_object.setStatus(TruckStatus.ENROUTE)
            consignments = list(Consignment.query.filter_by(truck_id=dispatched_truck_object.id))
            for consignment in consignments:
                consignment.setDispatchTime()
            flash(f"TRUCK {dispatched_truck_object.id} of volume {dispatched_truck_object.volume} cubic meters is enroute",category="success")
        else:
            flash(f"Consignment {dispatched_truck_object.id} of volume {dispatched_truck_object.volume} cubic meters is not enroute",category="danger")  
        return redirect(url_for('driver_truck_page'))         

    if request.method == "GET":
        trucks = list(Truck.filter_by(driverID=token))
        branches = Office.query.all()
        branch_city = {}
        for branch in branches:
            branch_city[int(branch.id)] = branch.officeAddress.city
        return render_template('driver_truck_assigned.html', trucks=trucks, branch_city=branch_city, dispatch_form=dispatch_form)

# -------------------------------------------------------DRIVER TRUCK PAGE-----------------------------------------------------------
@app.route('/driver_truck_receive/<token>',methods=["GET","POST"])
def driver_truck_receive_page(token):
    receive_truck_form = ReceiveTruckForm()
    if request.method == "POST":
        received_truck = request.form.get('receive_truck')
        received_truck_object = Truck.query.filter_by(id=received_truck).first()
        if received_truck_object:
            received_truck_object.setStatus(TruckStatus.AVAILABLE)
            current_user.setStatus(EmployeeStatus.AVAILABLE)
            flash(f"TRUCK {received_truck_object.id} of volume {received_truck_object.volume} cubic meters is enroute",category="success")
        else:
            flash(f"Consignment {received_truck_object.id} of volume {received_truck_object.volume} cubic meters is not enroute",category="danger")  
        return redirect(url_for('driver_truck_recieve_page'))         

    if request.method == "GET":
        trucks = list(Truck.filter_by(driverID=token))
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
            consignments = list(Consignment.query.filter_by(truck_id=approved_incoming_object.id))
            for consignment in consignments:
                consignment.setStatus(ConsignmentStatus.DELIVERED)
                consignment.setArrivalDateTime()
            flash(
                f"Incoming Truck {approved_incoming_object.id} with truck number {approved_incoming_object.truckNumber} is approved", category="success")
        else:
            flash("Incoming Truck not approved", category="danger")
        return redirect(url_for('view_incoming_truck_status_page'))

    if request.method == "GET":
        trucks = list(Truck.filter_by(destinationBranch=token))
        trucks.reverse()
        branches = Office.query.all()
        branch_city = {}
        for branch in branches:
            branch_city[int(branch.id)] = branch.officeAddress.city
        return render_template('view_incoming_truck_status.html', trucks=trucks, branch_city=branch_city, approve_incoming_form=approve_incoming_form)