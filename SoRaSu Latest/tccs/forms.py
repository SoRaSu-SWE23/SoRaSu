from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField,DecimalField,SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError,NumberRange
from tccs.models import Customer, Employee

#---------------------------------------------------------------------------------------------------------------------------

class RegisterCustomerForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = Customer.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = Customer.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class RegisterEmployeeForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = Employee.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = Employee.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    branchID = SelectField(label="Choose an option",coerce=int)
    position = SelectField(label="Choose a Position",choices=[('None','Select Position'),('Manager','Manager'),('Employee','Employee'),('Driver','Driver')])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

#---------------------------------------------------------------------------------------------------------------------------

class LoginCustomerForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class LoginEmployeeForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class ForgotPasswordForm_email(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    submit = SubmitField(label='Change Password')
    
class ForgotPasswordForm_password(FlaskForm):
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Change Password')

#---------------------------------------------------------------------------------------------------------------------------

class ConsignmentForm(FlaskForm):
    sender_name = StringField(label='Sender Name',validators=[Length(min=2,max=30),DataRequired()])
    senderAddressLine = StringField(label='Address',validators=[DataRequired(),Length(max=100)])
    sender_city = StringField(label='Sender City',validators=[DataRequired(),Length(max=100)])
    senderPincode = StringField(label='Pincode',validators=[DataRequired(),Length(min=6,max=6)])
    receiver_name = StringField(label='Name',validators=[Length(min=2,max=30),DataRequired()])
    receiverAddressLine = StringField(label='Address',validators=[DataRequired(),Length(max=100)])
    receiver_city = StringField(label='Receiver City',validators=[DataRequired(),Length(max=100)])
    receiverPincode = StringField(label='Pincode',validators=[DataRequired(),Length(min=6,max=6)])
    volume = DecimalField(label="Volume",validators=[DataRequired(),NumberRange(min=1,max =1000)])
    dispatch_branch = SelectField('Choose an option',coerce=int)
    receiver_branch = SelectField('Choose an option',coerce=int)
    submit = SubmitField("Proceed") 

#---------------------------------------------------------------------------------------------------------------------------

class TruckForm(FlaskForm):
    truckNumber = StringField(label='Truck Number',validators=[Length(min=2,max=10),DataRequired()])
    branchID = SelectField('Choose an option',coerce=int)
    submit = SubmitField(label='Add truck')

class TruckStatusForm(FlaskForm):
    Latitude = DecimalField(label='Latitude')
    Longitude = DecimalField(label='Longitude')
    submit = SubmitField(label='Update Status')

#---------------------------------------------------------------------------------------------------------------------------

class ApproveTruckForm(FlaskForm):
    submit = SubmitField(label="Approve Truck")

class DispatchTruckForm(FlaskForm):
    submit = SubmitField(label="Truck Enroute")

class ReceiveTruckForm(FlaskForm):
    submit = SubmitField(label="Truck Reached")

class ApproveIncomingTruckForm(FlaskForm):
    submit = SubmitField(label="Approve Incoming Truck")

class TruckAvailableForm(FlaskForm):
    submit = SubmitField(label="Make Truck Available")

class TruckUsageForm(FlaskForm):
    distance = DecimalField()
    submit = SubmitField(label="Make Truck Available")
    

