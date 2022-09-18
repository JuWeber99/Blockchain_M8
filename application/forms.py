from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange

from application.models.blockchain.Wallet import get_user_wallet


class LoginForm(FlaskForm):
    """Form for logging into an account"""
    passphrase = StringField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class SendForm(FlaskForm):
    """Form for creating a transaction"""
    quantity = DecimalField(
        'Quantity',
        validators=[InputRequired(), NumberRange(min=1)],
        render_kw={"placeholder": "Quantity to Send"}
    )
    receiver = StringField(
        'Receiver',
        validators=[InputRequired(), Length(min=0, max=10000000000)],  # TODO
        render_kw={"placeholder": "Receiver Address"},
        default=get_user_wallet().public_key
    )
    submit = SubmitField('Send')
