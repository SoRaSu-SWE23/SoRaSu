from tccs import app, change,get
from flask import render_template, redirect, url_for, flash
from tccs.models import Customer, Employee, Consignment, Address, Truck, ConsignmentStatus, Manager , Office
from tccs.forms import RegisterCustomerForm, RegisterEmployeeForm, LoginCustomerForm, LoginEmployeeForm, ConsignmentForm, TruckForm, BranchQueryForm
from tccs import db
from flask_login import login_user, logout_user,current_user,login_required

#-------------------------------------------------------HOME PAGE-----------------------------------------------------------
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

#-------------------------------------------------------CUSTOMER PAGE-----------------------------------------------------------

@app.route('/customer')
def customer_page():
    return render_template('customer.html')

#-------------------------------------------------------MANAGER PAGE-----------------------------------------------------------

@app.route('/manager')
def manager_page():
    return render_template('manager.html')

#***************************RAJ CHANGE******************************************  
#-------------------------------------------------------EMPLOYEE PAGE-----------------------------------------------------------
@app.route('/employee')
def employee_page():
    return render_template('employee.html')

#***************************RAJ CHANGE******************************************  
#-------------------------------------------------------DRIVER PAGE-----------------------------------------------------------
@app.route('/driver')
def driver_page():
    return render_template('driver.html')

#-------------------------------------------------------DASHBOARD PAGE-----------------------------------------------------------

@app.route('/dashboard')
def dashboard_page():
    if get()=="customer":
        return redirect(url_for('customer_page'))
    #***************************RAJ CHANGE******************************************         
    elif get()=="employee":
        if current_user.role == "manager":
            return redirect(url_for('manager_page'))
        elif current_user.position == "driver" or current_user.position == "Driver":
            return redirect(url_for('driver_page'))
        else:
            return redirect(url_for('employee_page'))
#-------------------------------------------------------REGISTER PAGES-----------------------------------------------------------

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
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('customer_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register_customer.html', form=form)

@app.route('/register_employee', methods=['GET', 'POST'])
def register_employee_page():
    form = RegisterEmployeeForm()
    if form.validate_on_submit():
    #***************************RAJ CHANGE****************************************** 
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
        #***************************RAJ CHANGE******************************************        
        if user_to_create.role == 'manager':
            flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
            return redirect(url_for('manager_page'))
        elif user_to_create.role == 'employee' and (user_to_create.position == 'driver' or user_to_create.position == 'Driver'): 
            flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
            return redirect(url_for('driver_page'))
        else:
            flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
            return redirect(url_for('employee_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register_employee.html', form=form)


#-------------------------------------------------------LOGIN/LOGOUT PAGES-----------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')

@app.route('/login_customer',methods=['GET','POST'])
def login_customer_page():
    form = LoginCustomerForm()
    if form.validate_on_submit():
        attempted_user = Customer.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            change("customer")
            login_user(attempted_user)
            flash(f"You are logged in as: {attempted_user.username}",category='success')
            return redirect(url_for('customer_page'))
        else:
            flash("Please try again",category='danger')
    return render_template('login_customer.html',form = form)

@app.route('/login_employee',methods=['GET','POST'])
def login_employee_page():
    form = LoginEmployeeForm()
    if form.validate_on_submit():
        attempted_user = Employee.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            change("employee")
            login_user(attempted_user)   
            #***************************RAJ CHANGE******************************************         
            if attempted_user.role == 'manager':
                flash(f"Account created successfully! You are now logged in as {attempted_user.username}", category='success')
                return redirect(url_for('manager_page'))
            elif attempted_user.role == 'employee' and (attempted_user.position == 'driver' or attempted_user.position == 'Driver'): 
                flash(f"Account created successfully! You are now logged in as {attempted_user.username}", category='success')
                return redirect(url_for('driver_page'))
            else:
                flash(f"Account created successfully! You are now logged in as {attempted_user.username}", category='success')
                return redirect(url_for('employee_page'))
        else:
            flash("Please try again",category='danger')
    return render_template('login_employee.html',form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out",category="info")
    return redirect(url_for("home_page"))


#-------------------------------------------------------PLACE_CONSIGNMENT PAGE-----------------------------------------------------------

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
        consignment_to_create = Consignment(volume=form.volume.data,
                                            sender_name = senderName,
                                            receiver_name = receiverName,
                                            senderAddress_id = senderAddress.id,
                                            receiverAddress_id = receiverAddress.id,
                                            sourceBranchID = form.dispatch_branch.data,
                                            destinationBranchID = form.receiver_branch.data)
        db.session.add(consignment_to_create)
        db.session.commit()
        
        flash(f"Consignment {consignment_to_create.id} created successfully by {current_user.username}",category="success")
        return redirect(url_for('customer_page'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'There is was error creating a consignment:{err_msg}',category='danger') 
    return render_template('place_consignment.html',form=form)

#-------------------------------------------------------ADD_NEW_TRUCK PAGE-----------------------------------------------------------

@app.route('/add_truck', methods=['GET', 'POST'])
def add_truck_page():
    form = TruckForm()
    if form.validate_on_submit():
        truck_to_create = Truck(branch_id = form.branchID.data,
                                truckNumber = form.truckNumber.data)
        db.session.add(truck_to_create)
        db.session.commit()
        flash(f"Truck added successfully!", category='success')
        return redirect(url_for('manager_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with adding a truck {err_msg}', category='danger')

    return render_template('add_new_truck.html', form=form)

#-------------------------------------------------------BRANCH_QUERY PAGE-----------------------------------------------------------

@app.route('/branch_query',methods=['GET','POST'])
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
    return render_template('branch_query.html',form = form)


#-------------------------------------------------------ORDER_HISTORY(CUSTOMER) PAGE-----------------------------------------------------------

@app.route('/order_history')
def order_history_page():
    consignments = current_user.consignments
    consignments.reverse()
    return render_template('order_history.html', consignments=consignments)

#-------------------------------------------------------VIEW ALL CONSIGNMENTS(EMPLOYEE) PAGE-----------------------------------------------------------
@app.route('/order_history/<token>')
def order_history_branch_page(token):
    consignments = list(Consignment.query.filter_by(sourceBranchID=token))
    consignments.reverse()
    return render_template('order_history.html', consignments=consignments)

#-------------------------------------------------------VIEW PENDING CONSIGNMENTS(EMPLOYEE) PAGE-----------------------------------------------------------
@app.route('/order_history/<token>/pending')
def branch_pending_consignments_page(token):
    consignments = list(Consignment.query.filter_by(sourceBranchID=token,status=ConsignmentStatus.PENDING))
    consignments.reverse()
    return render_template('order_history.html', consignments=consignments)


#-------------------------------------------------------TRACK_CONSIGNMENT(CUSTOMER) PAGE-----------------------------------------------------------

@app.route('/track_consignment/<token>')
@login_required
def track_consignment_page(token):
    consignment = Consignment.query.filter_by(id=token).first()
    return render_template('track_consignment.html',consignment=consignment, ConsignmentStatus=ConsignmentStatus)

#-------------------------------------------------------VIEW CONSIGNMENTS(MANAGER) PAGE-----------------------------------------------------------
@app.route('/view_consignment_status')
def view_consignment_status_page():
    consignments = list(Consignment.query.all())
    consignments.reverse()
    branches = Office.query.all()
    branch_city={}
    for branch in branches:
        branch_city[int(branch.id)]= branch.officeAddress.city

    return render_template('view_consignment_status.html', consignments=consignments , branch_city=branch_city)











