import os
import click
import sys
from app import create_app, db
from app.models import Patient, History, Diagnosis
from flask_migrate import Migrate

COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage
    COV = coverage.coverage(branch=True, include="app/*")
    COV.start()

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Patient=Patient, History=History, Diagnosis=Diagnosis) # add other models ie User=User from imports


@app.cli.command()
@click.option("--coverage/--no-coverage", default=False,
        help="Run tests under code coverage.")
def test(coverage):
    if coverage and not os.environ.get("FLASK_COVERAGE"):
        os.environ["FLASK_COVERAGE"] = "1"
        args = sys.argv
        args[0] = args[0] + ".exe"
        os.execvp(sys.executable, [sys.executable] + args)
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print("Coverage summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print("HTML Version: file://%s/index.html" % covdir)
        COV.erase()