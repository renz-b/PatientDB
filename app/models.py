# base models, need to import db from instantiated create_app class later
from flask import current_app 
import datetime
from os import remove

from . import db
from app.search import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page, min_score=0.1):
        ids, total, score = query_index(cls.__tablename__, expression, page, per_page, 
            min_score)
        if total == 0:
            return cls.query.filter_by(id=0), 0, 0 #last zero is a score of 0 if results return none
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total, score
    
    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }
    
    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj.__tablename__, obj):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
diagnosisTable = db.Table("diagnosis_patient",
    db.Column('diagnosis_id', db.Integer, db.ForeignKey('diagnosis.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'), primary_key=True))

class Patient(SearchableMixin, db.Model):
    __tablename__ = "patient"
    __searchable__=["first_name", "last_name", "middle_name", "age"]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    name_suffix = db.Column(db.String(4))
    address = db.Column(db.String(128), nullable=False)
    email_address = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.Integer(), nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #MISSING IN MODELS BIRTHDAY. Please remove age. Please add Male or female
    history = db.relationship(
        "History",
        backref="patient",
        lazy=True,
        uselist=False
    )
   
    final_diagnosis = db.relationship(
        "Diagnosis",
        secondary=diagnosisTable,
        lazy=True,
        backref=db.backref("patient", lazy=True)
    )

    # admissions = db.relationship(
    #     "Admission",
    #     backref="patient",
    #     lazy=True
    # ) 

    # admitted = db.Column(db.Boolean(default=False))

    # def is_admitted(self):
    #     if self.admitted == True:
    #         return True
    #     else:
    #         return False

    # def admit(self):
    #     self.admitted = True
    #     date_time_admitted = self.date_time_object()
    #     admitting_diagnosis = self.diagnosis # need to rethink this since diagnosis in the model does not always mean its admitting
    #     admission_object = Admission(date_time_admitted=date_time_admitted, admitting_diagnosis=admitting_diagnosis,
    #         patient_id=self.id)
    #     db.session.add(admission_object)
    #     db.session.commit()
    #     return "Added {}".format(admission_object)
        
        
    # def discharge(self):
    #     self.admitted = False
    #     date_time_discharged = self.date_time_object()
    #     final_diagnosis = self.diagnosis
    #     admission_object = Admission.query.filter_by(self.id).order_by(Admission.date_time_admitted) #not sure recheck in tester
    
    # @staticmethod
    # def date_time_object():
    #     date_time_object = datetime.datetime.now()
    #     date_time_format = "{0}/{1}/{2} -- {3}:{4}:{5}".format(
    #         date_time_object.month, date_time_object.day, date_time_object.year,
    #         date_time_object.hour, date_time_object.minute, date_time_object.second
    #     )
    #     return date_time_format

    def __repr__(self):
        return "<Patient {0} - {1}>".format(self.id, self.last_name)

    
class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hpi = db.Column(db.Text)
    pmh = db.Column(db.Text)
    fh = db.Column(db.Text)
    psh = db.Column(db.Text)
    obh = db.Column(db.Text)
    pe = db.Column(db.Text) # make a template i think
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), 
        nullable=False)
    def __repr__(self):
        return "<History Patient {}>".format(self.patient_id)

class Diagnosis(db.Model):
    __tablename__ = "diagnosis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    disease = db.Column(db.String(256), unique=True, nullable=False)

    def __repr__(self):
        return "<Disease: {}>".format(self.disease)

# class Admission(db.Model):
#     __tablename__ = "admission"
#     id = db.Column(db.Integer, primary_key=True)
#     date_time_admitted = db.Column(db.DateTime())
#     admitting_diagnosis = db.Column(db.Text, nullable=False)
#     date_time_discharged = db.Column(db.DateTime())
#     discharge_diagnosis = db.Column(db.Text)
#     patient_id = db.Column(db.Integer, foreign_keys="patient.id", nullable=False)

#     admitting_diagnosis = db.relationship(
#         "Diagnosis",
#         backref="admitting_diagnosis",
#         lazy=true
#     )
