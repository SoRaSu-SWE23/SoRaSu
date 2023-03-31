from tccs import app, change
from flask import render_template, redirect, url_for, flash
from tccs.models import Customer, Employee, Consignment, Address, Truck
from tccs.forms import RegisterCustomerForm, RegisterEmployeeForm, LoginCustomerForm, LoginEmployeeForm, ConsignmentForm, TruckForm
from tccs import db
from flask_login import login_user, logout_user,current_user

#-------------------------------------------------------HOME PAGE-----------------------------------------------------------
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/customer')
def customer_page():
    return render_template('customer.html')

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
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register_customer.html', form=form)

@app.route('/register_employee', methods=['GET', 'POST'])
def register_employee_page():
    form = RegisterEmployeeForm()
    if form.validate_on_submit():
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
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
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
            current_user = attempted_user
            flash(f"You are logged in as: {attempted_user.username}",category='success')
            return redirect(url_for('home_page'))
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
            flash(f"You are logged in as: {attempted_user.username}",category='success')
            return redirect(url_for('home_page'))
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
        
        flash(f"Consignment {consignment_to_create.consignment_id} created successfully by {current_user.username}",category="success")
        return redirect(url_for('home_page'))
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
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with adding a truck {err_msg}', category='danger')

    return render_template('add_new_truck.html', form=form)










