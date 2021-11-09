from operator import add
from flask import render_template, url_for, request, current_app, jsonify, redirect
from . import main
from .forms import AddPatientValidator, FullPatientForm
from ..models import Patient, History, Diagnosis
from .. import db

@main.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")

@main.route("/search")
def search():
    if request.method == "GET":
        page = request.args.get("page", 1, type=int)
        q = request.args.get("query")
        patients, total, score = Patient.search(q, page,
            current_app.config["POSTS_PER_PAGE"])
        total_pages = int(total/current_app.config["POSTS_PER_PAGE"])
        next_url = url_for("main.search", query=q, page=page+1) \
            if total > page * current_app.config["POSTS_PER_PAGE"] else None
        prev_url = url_for("main.search", query=q, page=page-1) \
            if page > 1 else None
    return render_template("main/tables.html", patients=patients, total=total,
        next_url=next_url, prev_url=prev_url, query=q, page=page, total_pages=total_pages, score=score)

@main.route("/about", methods=["GET"])
def about():
    return "hello"

@main.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    form = AddPatientValidator()
    return render_template("main/patient_form.html", form=form)

@main.route("/all_patients", methods=["GET"])
def all_patients():
    patients = Patient.query.all()
    total = Patient.query.count()
    total_pages = int(total/current_app.config["POSTS_PER_PAGE"])
    return render_template("main/tables.html", patients=patients, total=total, total_pages=total_pages)


@main.route("/similar_patient", methods=["POST"])
def similar_patient():
    elastic_check_for_emptydb = Patient.query.all()

    if elastic_check_for_emptydb == []:
        form = FullPatientForm()
        return jsonify({ 'html' : render_template("main/section_second_form.html", form=form), 'message' : "No patient found with same name. Please complete form." }) #change this after making html form for diagnosis and history
    
    q = f"{request.form['first_name']} {request.form['last_name']} {request.form['middle_name']} {request.form['age']}"
    page = request.args.get("page", 1, type=int)
    patients, total, score = Patient.search(
    q, page, current_app.config["POSTS_PER_PAGE"], min_score=0.8)
    total_pages = int(total/current_app.config["POSTS_PER_PAGE"])
    
    if total == 0:
        form = FullPatientForm()
        return jsonify({ 'html' : render_template("main/section_second_form.html", form=form), 'message' : "No patient found with same name. Please complete form." }) #change this after making html form for diagnosis and history

    return render_template("main/section_table.html", patients=patients, total=total, 
        query=q, page=page, total_pages=total_pages, score=score)


@main.route("/commit_patient", methods=["POST"])
def commit_patient():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        middle_name = request.form["middle_name"]
        name_suffix = request.form["name_suffix"] # be wary of None objects find a way to set a default value if none
        age = request.form["age"]
        address = request.form["address"]
        email_address = request.form["email_address"]
        phone_number = request.form["phone_number"]

        hpi = request.form["hpi"]
        pmh = request.form["pmh"]
        fh = request.form["fh"]
        psh = request.form["psh"]
        obh = request.form["obh"]
        pe = request.form["pe"]

        final_diagnosis = request.form["final_diagnosis"]
        # still trying first commit diagnosis still not included
        patient = Patient(first_name=first_name, last_name=last_name, middle_name=middle_name, name_suffix=name_suffix,
            age=age, address=address, email_address=email_address, phone_number=phone_number)
        history = History(hpi=hpi, pmh=pmh, fh=fh, psh=psh, obh=obh, pe=pe, patient=patient)
        db.session.add(patient)
        db.session.add(history)
        db.session.commit()
        return jsonify({ 'message': "success! Committed!", "redirect" : url_for('main.index') })
    
#update patient watch red eyed coder video number 8 for update patient use that