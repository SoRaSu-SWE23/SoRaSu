from tccs import app,change
from flask import render_template, redirect, url_for, flash
from tccs.models import Customer, Employee , Truck , Bill
from tccs.forms import RegisterCustomerForm, RegisterEmployeeForm, LoginCustomerForm,LoginEmployeeForm,AddTruckForm
from tccs import db
from flask_login import login_user, logout_user, current_user, login_required
# from selenium import webdriver   # for webdriver
# driver = webdriver.Chrome()   
# # Get URL first to load page to run script


@app.route('/')
@app.route('/home')
def home_page():
    # driver.execute_script("window.localStorage.setItem('name', 'value');")
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
       
        # window.localStorage(user,2)
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register_employee.html', form=form)


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

@app.route('/add_truck', methods=['GET', 'POST'])
def add_truck_page():
    form = AddTruckForm()
    if form.validate_on_submit():
        truck_to_create =Truck(branchid=form.branchID.data,status=0,volumeConsumed=0,usageTime=0,idleTime=0)
        db.session.add(truck_to_create)
        db.session.commit()
        flash(f"truck added successfully!", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a truck {err_msg}', category='danger')

    return render_template('truck.html', form=form)

@app.route('/bill', methods=['Get','POST'])
def bill_page():
    bill = Bill(amount=100)
    db.session.add(bill)
    db.session.commit()
    print(bill)
    return render_template('bill.html')













