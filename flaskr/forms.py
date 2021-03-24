from wtforms import Form, BooleanField, StringField, IntegerField, SubmitField
from flask_wtf import FlaskForm


class SearchMapForm(FlaskForm):
    address = StringField('Address', description='Adress', render_kw={'placeholder': 'Adress'})
    radius = IntegerField('Radius', description='Radius', render_kw={'placeholder': 'Radius'})
    submit = SubmitField("Search")
