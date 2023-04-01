from tccs import app, change_user
from flask import render_template, redirect, url_for, flash
from tccs.models import Customer, Employee, Consignment,Address
from tccs.forms import RegisterCustomerForm, RegisterEmployeeForm, LoginCustomerForm, LoginEmployeeForm, ConsignmentForm
from tccs import db
from flask_login import login_user, logout_user,current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/services')
def services():
    return render_template('services.html')


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
        change_user("Customer")
        login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

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
        change_user("Employee")
        login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register_employee.html', form=form)


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
            change_user("Customer")
            login_user(attempted_user)
            flash(
                f"You are logged in as: {attempted_user.username}", category='success')
            return redirect(url_for('home_page'))
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
            change_user("Employee")
            login_user(attempted_user)
            flash(
                f"You are logged in as: {attempted_user.username}", category='success')
            return redirect(url_for('home_page'))
        else:
            flash("Please try again", category='danger')
    return render_template('login_employee.html', form=form)


@app.route('/register_consignment', methods=['GET', 'POST'])
def register_consignment_page():
    form = ConsignmentForm()
    if form.validate_on_submit():
        sender_addr = Address(form.senderAddressLine.data,form.sender_city.data,form.senderPincode.data)
        receiver_addr = Address(form.receiverAddressLine.data,form.receiver_city.data,form.receiverPincode.data)
        consignment_to_create = Consignment(volume=form.volume.data,
                                            sender_name = form.sender_name.data,
                                            receiver_name = form.receiver_name.data,
                                            senderAddress= sender_addr,
                                            receiverAddress=receiver_addr,
                                            sourceBranchID = form.dispatch_branch.data,
                                            destinationBranchID = form.receiver_branch.data)
        db.session.add(consignment_to_create)
        db.session.commit()
        
        flash(f"Consignment {consignment_to_create.consignment_id} created successfully by {current_user.username}",category="success")
        return redirect(url_for('home_page'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'There is was error creating a consignment:{err_msg}',category='danger') 
    return render_template('consignment.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for("home_page"))
