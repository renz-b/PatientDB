from math import ceil
from flask import render_template, url_for, request, current_app, jsonify, redirect, session
from datetime import date, datetime, time
from flask.helpers import flash
from werkzeug.urls import url_parse
from sqlalchemy.exc import IntegrityError
from . import main
from .forms import GeneralDataForm, HistoryForm, FullPatientForm
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
    form = GeneralDataForm()
    return render_template("main/patient_form.html", form=form)

@main.route("/all_patients", methods=["GET"])
def all_patients():
    page = request.args.get("page", 1, type=int)
    pagination = Patient.query.order_by(Patient.id.asc()).paginate(page, current_app.config["POSTS_PER_PAGE"])
    patients = pagination.items
    total = Patient.query.count()
    total_pages = ceil(total/current_app.config["POSTS_PER_PAGE"])
    return render_template("main/tables.html", patients=patients, total=total, total_pages=total_pages, next_url = pagination, prev_url = pagination, page=page)

@main.route("/similar_patient", methods=["POST"])
def similar_patient():
    if request.form["query"] == "true":
        try:
            q = f"{request.form['first_name']} {request.form['last_name']} {request.form['middle_name']} {request.form['address']} {request.form['gender']}"
            page = request.args.get("page", 1, type=int)
            patients, total, score = Patient.search(
            q, page, current_app.config["POSTS_PER_PAGE"], min_score=0.8, fields=["first_name", "last_name", "middle_name", "gender", "address"])
            total_pages = int(total/current_app.config["POSTS_PER_PAGE"])
            
            if total == 0:
                form = HistoryForm()
                return jsonify({ "html" : render_template("main/section_second_form.html", form=form), 'message' : "No patient found with same name. Please complete form." }) 
            else:
                return render_template("main/section_table.html", patients=patients, total=total, 
                    query=q, page=page, total_pages=total_pages, score=score)        
        except:
            elastic_check_for_emptydb = Patient.query.all()

            if elastic_check_for_emptydb == []:
                form = HistoryForm()
                return jsonify({ 'html' : render_template("main/section_second_form.html", form=form), 'message' : "Database empty." }) #change this after making html form for diagnosis and history
    else:
        form = HistoryForm()
        return jsonify({ "html" : render_template("main/section_second_form.html", form=form), 'message' : "&#10071; Please make sure patient is not duplicate. Complete form below." })

@main.route("/commit_patient", methods=["POST"])
def commit_patient():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        middle_name = request.form["middle_name"]
        name_suffix = request.form["name_suffix"] # be wary of None objects find a way to set a default value if none
        gender = request.form["gender"]
        birthday = request.form["birthday"]
        address = request.form["address"]
        email_address = request.form["email_address"]
        phone_number = request.form["phone_number"]

        hpi = request.form["hpi"]
        pmh = request.form["pmh"]
        fh = request.form["fh"]
        psh = request.form["psh"]
        obh = request.form["obh"]
        pe = request.form["pe"]

        patient = Patient(first_name=first_name, last_name=last_name, middle_name=middle_name, name_suffix=name_suffix,
            gender=gender, birthday=birthday, address=address, email_address=email_address, phone_number=phone_number)
        history = History(hpi=hpi, pmh=pmh, fh=fh, psh=psh, obh=obh, pe=pe, patient=patient)
        db.session.add(patient)
        db.session.add(history)
        db.session.commit()
        return jsonify({ 'message': "success! Committed!", "redirect" : url_for("main.patient", id=patient.id) })

@main.route("/patient/<id>")
def patient(id):
    patient = Patient.query.filter_by(id=id).first_or_404()
    patient_id = patient.id
    referrer = url_parse(request.referrer)
    if referrer.path == url_for('main.all_patients'):
        session["prev_page"] = referrer.query[5:6]
    date_added = patient.date_added.date().strftime("%Y/%b/%d")
    time_added = patient.date_added.time().strftime("%I:%M %p")

    general_data = { 
        "Name": f"{patient.last_name}, {patient.first_name}",
        "Name Suffix" : "" if patient.name_suffix == '' else patient.name_suffix,
        "Age" : patient.age(),
        "Gender" : "Male" if patient.gender == "m" else "Female",
        "Birthday" : patient.birthday.date(),
        "Address" : patient.address,
        "Email" : patient.email_address,
        "Phone Number" : patient.phone_number,
        "Date Added" : f"{date_added} - {time_added}",
    }
  
    history = {
        "History of Present Illness" : patient.history.hpi,
        "Past Medical History" : patient.history.pmh,
        "Family History" : patient.history.fh,
        "Personal Social History" : patient.history.psh,
        "OB History" : patient.history.obh,
        "Physical Examination" : patient.history.pe
        }
    final_diagnosis = patient.final_diagnosis.all()
    
    diagnosis_select = Diagnosis.query.all()
    return render_template("main/patient_details.html", patient=patient, general_data_keys = list(general_data.keys()), 
        general_data_values=list(general_data.values()),
        history_keys = list(history.keys()), 
        history_values = list(history.values()), final_diagnosis = final_diagnosis, diagnosis_select = diagnosis_select, patient_id = patient_id)

@main.route("/patient/<id>/edit", methods=["POST", "GET"])
def patient_update(id):
    patient = Patient.query.filter_by(id=id).first()
    history = patient.history
    referrer = request.referrer

    if request.method == "POST":
        form = GeneralDataForm(formdata=request.form, obj=patient)
        form2 = HistoryForm(formdata=request.form, obj=history)
        form.populate_obj(patient)
        form2.populate_obj(history)
        db.session.commit()
        return redirect(url_for("main.patient", id=patient.id))
    form = GeneralDataForm(obj=patient)
    form2 = HistoryForm(obj=history)
    return render_template("main/patient_update.html", patient=patient, form=form, form2=form2, referrer=referrer)

@main.route("/diagnosis_list_update", methods=["POST"])
def diagnosis_list_update():
    if request.method == "POST":
        action = request.form["action"]
        diagnosis = request.form["diagnosis"]
        message = action.capitalize()

        if diagnosis == '':
            return jsonify({ 'message' : 'no input'})
        else: 
            try:
                if action == "add":
                    diagnosis_model = Diagnosis(disease=diagnosis)
                    
                    db.session.add(diagnosis_model)
                else:
                    diagnosis_model = Diagnosis.query.filter_by(disease=diagnosis).first()
                    db.session.delete(diagnosis_model)
                
                db.session.commit()
                diagnosis_query = Diagnosis.query.all()
            except:
                if action == "add":
                    return jsonify({ 'message' : '&#10004;&#65039; Diagnosis already in database!<br>Can not delete if it does not exist.'})
                else:
                    return jsonify({ 'message' : '&#10060; Diagnosis not in database!'})
            return jsonify({ "html" : render_template("main/section_diagnosis.html", diagnosis_select = diagnosis_query, diagnosis = diagnosis),
                "message" : f"&#128203; {message}: {diagnosis}." })

@main.route("/update_patient_diagnosis", methods=["POST"])
def update_patient_diagnosis():
    patient_id = request.form["patient_id"]
    diagnosis = request.form["diagnosis"]
    action = request.form["action"]

    if diagnosis == '':
        return jsonify({ 'message' : 'no input'})
    else:
        patient_query = Patient.query.filter_by(id=patient_id).first()
        diagnosis_query = Diagnosis.query.filter_by(disease=diagnosis).first()
        try:
            if action == 'add':
                    patient = patient_query.final_diagnosis.append(diagnosis_query)
            else:
                patient = patient_query.final_diagnosis.remove(diagnosis_query)
            db.session.add(patient_query)
            db.session.commit()
        except IntegrityError:
            return jsonify({ 'message' : '&#10004;&#65039; Duplicate: Diagnosis already present in patient!'})
        except AttributeError:
            return jsonify({ 'message' : '&#128680; Diagnosis not in database.<br>Please "Add" Diagnosis on the right &#128073;'})
        return jsonify({ 'html' : render_template("main/section_final_diagnosis.html", 
            final_diagnosis = patient_query.final_diagnosis.all()), 'message' : '&#10004;&#65039; Diagnosis Updated'})

@main.route("/patient/<id>/delete_patient")
def delete_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    message = f"Deleted: {patient.last_name}, {patient.first_name}: {patient.age()} y.o., {patient.gender.upper()}"
    session["message"] = message
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for("main.search_page"))

@main.route("/search_page")
def search_page():
    try:
        message = session["message"] 
        session.pop("message", None)
        flash(message)
        return render_template("main/search_page.html")
    except:
        return render_template("main/search_page.html")