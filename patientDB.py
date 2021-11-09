import os
import click
from app import create_app, db
from app.models import Patient, History, Diagnosis
# from app.models import models here
# from flask_migrate import Migrate (install flask migrate later)

app = create_app(os.getenv("FLASK_CONFIG") or "default")
# migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Patient=Patient, History=History, Diagnosis=Diagnosis) # add other models ie User=User from imports

# tests cli command goes here
# @app.cli.command()
