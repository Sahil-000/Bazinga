from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email

# form used in basket
class CheckoutForm(FlaskForm):
    firstname = StringField("First Name", validators=[InputRequired()])
    lastname = StringField("Last name", validators=[InputRequired()])
    email = StringField("Email-ID", validators=[InputRequired(), email()])
    phone = StringField("Phone No.", validators=[InputRequired()])
    address = StringField("Delivery Address", validators=[InputRequired()])
    submit = SubmitField("Place Order")

