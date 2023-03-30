from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField,DecimalField,SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError,NumberRange
from tccs.models import Customer, Employee


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
    branchID = IntegerField(label='Branch ID: ', validators=[DataRequired()])
    position = StringField(label='Position: ', validators=[DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginCustomerForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class LoginEmployeeForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

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
    dispatch_branch = SelectField("Dispatch Branch",coerce=int)
    receiver_branch = SelectField("Receiver Branch",coerce=int)
    submit = SubmitField("Proceed")    