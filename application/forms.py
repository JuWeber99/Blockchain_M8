from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange

from application.models.blockchain.Wallet import get_user_wallet, Wallet, get_main_wallet


class SendForm(FlaskForm):
    """Form for creating a transaction"""
    quantity = DecimalField(
        'Quantity',
        validators=[InputRequired(), NumberRange(min=1)],
        render_kw={"placeholder": "Quantity to Send"},
        default=1
    )
    receiver = SelectField(
        'Receiver',
        coerce=str,
        choices=[get_user_wallet().public_key.encode("utf-8"), get_main_wallet().public_key.encode("utf-8")],
    )
    # choose from the 2 users
    submit = SubmitField('Send')
