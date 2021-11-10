from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextField, TextAreaField

from wtforms.validators import DataRequired, NumberRange, Email

class AddPatientValidatorForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("last_name", validators=[DataRequired()])
    middle_name = StringField("middle_name", validators=[DataRequired()])
    name_suffix = StringField("name_suffix", default=None)
    #add birthday instead of age and compute age whenever rendering from birthday
    age = IntegerField("age", validators=[DataRequired(message="Must be a number"), NumberRange(min=0, max=120, message=f"%(min)s - %(max)s")])
    submit = SubmitField("Submit")

class FullPatientForm(FlaskForm):
    address = StringField("Address", validators=[DataRequired()])
    email_address = StringField("Email", validators=[Email()]) 
    phone_number = IntegerField("Contact No.", validators=[DataRequired()])

    hpi = TextAreaField("History of Present Illness")
    pmh = TextAreaField("Past Medical History")
    fh = TextAreaField("Family History")
    psh = TextAreaField("Past Medical History")
    obh = TextAreaField("OB History")
    pe = TextAreaField("Physical Exam")

    final_diagnosis = TextField("Diagnosis") # Please use select field and use an __init__ to dynamically produce diagnosis 
    submit = SubmitField("SubmitForm")
    #think of a way to dynamically create a list of available diagnosis like what i did in the subjects category for quicktest
    #and also dynamically commit in same page a diagnosis if not found on list

class EditPatientForm(AddPatientValidatorForm, FullPatientForm):
    submit = SubmitField("edit patient")
