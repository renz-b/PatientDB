from flask import render_template, url_for, request, redirect, g
from . import main
from .forms import SearchForm
from ..models import Patient, History, Diagnosis

# @main.before_app_request
# def before_request():
#     g.search_form = SearchForm()
# SEARCH BAR PRESENT IN ALL ROUTES FUNCTION

@main.route("/", methods=["GET"])
def index():
    search_form = SearchForm()
    return render_template("main/index.html")

@main.route('/search')
def search():
    # if not search_form.validate():
    #     return redirect(url_for("main.index"))
    # page = request.args.get('page', 1, type=int)
    # posts, total = Patient.search(search_form.q.data, page, 5)

    if request.method == "GET":
        page = request.args.get('page', 1, type=int)
        patients, total = Patient.search(request.args.get("query"), page, 5)
    return render_template('main/tables.html', patients=patients, total=total)

@main.route("/about", methods=["GET"])
def about():
    return "hello"

@main.route("/results", methods=["GET"])
def results():
    p = Patient.query.first()
    return render_template("main/tables.html", p=p)
