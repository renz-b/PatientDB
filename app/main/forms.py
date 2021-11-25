from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, DateField, SelectField

from wtforms.validators import DataRequired, NumberRange, Email

class GeneralDataForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    middle_name = StringField("Middle Name", validators=[DataRequired()], render_kw={"placeholder": "Middle Name"})
    name_suffix = StringField("Name Suffix", default=None, render_kw={"placeholder": "Name Suffix (eg: Jr., Sr)"})
    birthday = DateField("Birthday", render_kw={"type": "date", "required": "true"})
    gender = SelectField("Gender", choices=[("m", "Male"), ("f", "Female")])   
    email_address = StringField("Email", validators=[Email()], render_kw={"placeholder": "Email"}) 
    phone_number = IntegerField("Contact No.", validators=[DataRequired()], render_kw={"placeholder": "Contact No."})
    address = StringField("Address", validators=[DataRequired()], render_kw={"placeholder": "Address"})

class HistoryForm(FlaskForm):
    hpi = TextAreaField("History of Present Illness", render_kw={"placeholder": "History of Present Illness"})
    pmh = TextAreaField("Past Medical History", render_kw={"placeholder": "Past Medical History"})
    fh = TextAreaField("Family History", render_kw={"placeholder": "Family History"})
    psh = TextAreaField("Past Medical History", render_kw={"placeholder": "Past Medical History"})
    obh = TextAreaField("OB History", render_kw={"placeholder": "OB History"})
    pe = TextAreaField("Physical Exam", render_kw={"placeholder": "Physical Exam"})

class FullPatientForm(GeneralDataForm, HistoryForm):
    submit = SubmitField("edit patient")
