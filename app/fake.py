from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import Patient, History

def patients(count=10):
    fake = Faker()
    i = 0
    while i < count:
        p = Patient(first_name=fake.first_name_nonbinary(),
                    last_name=fake.last_name_nonbinary(),
                    middle_name=fake.last_name_nonbinary(),
                    birthday=fake.date(),
                    gender='m',
                    address=fake.address(),
                    email_address=fake.ascii_email(),
                    phone_number=fake.msisdn())
        h = History(hpi=fake.paragraph(nb_sentences=3),
                    pmh=fake.paragraph(nb_sentences=3),
                    fh=fake.paragraph(nb_sentences=3),
                    psh=fake.paragraph(nb_sentences=3),
                    obh=fake.paragraph(nb_sentences=3),
                    pe=fake.paragraph(nb_sentences=3),
                    patient=p)
        db.session.add(p)
        db.session.add(h)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
