from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email
from flask_babel import _, lazy_gettext as _l
from app.models import User, Delivery_Address, Customer_Services


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    first_name = StringField(_l('First Name'), validators=[DataRequired()])
    last_name = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email Address'), validators=[DataRequired(), Email()])
    phone = IntegerField(_l('Phone Number'), validators=[DataRequired()])
    gender = StringField(_l('Gender'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, original_email, original_phone, original_first_name, original_last_name,
                 *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_first_name = original_first_name
        self.original_first_name = original_last_name
        self.original_email = original_email
        self.original_phone = original_phone

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different email address.'))

    def validate_phone(self, phone):
        if phone.data != self.original_phone:
            user = User.query.filter_by(phone=self.phone.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different phone number.'))


class EditDeliveryAddressForm(FlaskForm):
    delivery_address = StringField(_l('Delivery Address'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_delivery_address, *args, **kwargs):
        super(EditDeliveryAddressForm, self).__init__(*args, **kwargs)
        self.original_delivery_address = original_delivery_address

    def validate_delivery_address(self, delivery_address):
        if delivery_address.data != self.original_delivery_address:
            address = Delivery_Address.query.filter_by(address=self.delivery_address.data).first()
            if address is not None:
                raise ValidationError(_('Please use a different delivery address.'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class DeliveryAddressForm(FlaskForm):
    delivery_address = StringField(_l('Delivery Address'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class CsForm(FlaskForm):
    services = TextAreaField(_l('Send message to admin'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class EditMessage(FlaskForm):
    message = StringField(_l('Message'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class AddVoucher(FlaskForm):
    voucher = StringField(_l('Voucher Code'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class EditProduct(FlaskForm):
    pid = IntegerField(_l('ProductID'), validators=[DataRequired()])
    pname = StringField(_l('Product Name'), validators=[DataRequired()])
    qty = IntegerField(_l('QTY'), validators=[DataRequired()])
    price = FloatField(_l('Price'), validators=[DataRequired()])
    mid = IntegerField(_l('MID'))
    status = StringField(_l('Status'), validators=[DataRequired()])
    link = StringField(_l('Link'), validators=[DataRequired()])
    pc_id = IntegerField(_l('pc_id'))
    ps_id = IntegerField(_l('ps_id'))
    submit = SubmitField(_l('Submit'))





