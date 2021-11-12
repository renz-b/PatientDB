from math import ceil
from flask import render_template, url_for, request, current_app, jsonify, redirect, session
from werkzeug.urls import url_parse
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
    try:
        q = f"{request.form['first_name']} {request.form['last_name']} {request.form['middle_name']} {request.form['age']}"
        page = request.args.get("page", 1, type=int)
        patients, total, score = Patient.search(
        q, page, current_app.config["POSTS_PER_PAGE"], min_score=0.8)
        total_pages = int(total/current_app.config["POSTS_PER_PAGE"])
        
        if total == 0:
            form = HistoryForm()
            #diagnosis = Diagnosis.query.all() add back to return testing diagnosis in patient_details.html
            return jsonify({ 'html' : render_template("main/section_second_form.html", form=form), 'message' : "No patient found with same name. Please complete form." }) #change this after making html form for diagnosis and history

        return render_template("main/section_table.html", patients=patients, total=total, 
            query=q, page=page, total_pages=total_pages, score=score)        
    except:
        elastic_check_for_emptydb = Patient.query.all()

        if elastic_check_for_emptydb == []:
            form = HistoryForm()
            return jsonify({ 'html' : render_template("main/section_second_form.html", form=form), 'message' : "Database empty." }) #change this after making html form for diagnosis and history
    

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

@main.route("/patient/<id>")
def patient(id):
    patient = Patient.query.filter_by(id=id).first_or_404()
    patient_id = patient.id
    referrer = url_parse(request.referrer)
    if referrer.path == url_for('main.all_patients'):
        session["prev_page"] = referrer.query[5:6]

    general_data = { 
        "Name": f"{patient.last_name}, {patient.first_name}",
        "Name Suffix" : "None" if patient.name_suffix == '' else patient.name_suffix,
        "Age" : patient.age,
        "Address" : patient.address,
        "Email" : patient.email_address,
        "Phone Number" : patient.phone_number,
        "Date Added" : patient.date_added,
    }
    history = {
        "History of Present Illness" : patient.history.hpi,
        "Past Medical History" : patient.history.pmh,
        "Family History" : patient.history.fh,
        "Personal Social History" : patient.history.psh,
        "OB History" : patient.history.obh,
        "Physical Examination" : patient.history.pe
        }
    final_diagnosis = {
        "final_diagnosis" : patient.final_diagnosis.all()
    }
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
    form2 = FullPatientForm(obj=history)
    return render_template("main/patient_update.html", patient=patient, form=form, form2=form2, referrer=referrer)

@main.route("/diagnosis_update", methods=["POST"])
def diagnosis_update():
    patient_id = request.form["patient_id"]
    diagnosis = request.form["diagnosis"]

    patient_query = Patient.query.filter_by(id=patient_id).first()
    diagnosis_query = Diagnosis.query.filter_by(disease=diagnosis).first()
    
    patient = patient_query.final_diagnosis.append(diagnosis_query)
    db.session.add(patient_query)
    db.session.commit()

    return jsonify({ 'html' : render_template("main/section_final_diagnosis.html", final_diagnosis = patient_query.final_diagnosis.all()), 'message' : 'Diagnosis Updated'})

@main.route("/diagnosis_delete_from_patient", methods=["POST"])
def diagnosis_delete_from_patient():
    patient_id = request.form["patient_id"]
    diagnosis = request.form["diagnosis"]

    patient_query = Patient.query.filter_by(id=patient_id).first()
    diagnosis_query = Diagnosis.query.filter_by(disease=diagnosis).first()

    patient = patient_query.final_diagnosis.remove(diagnosis_query)
    db.session.add(patient_query)
    db.session.commit()

    return jsonify({ 'html' : render_template("main/section_final_diagnosis.html", final_diagnosis = patient_query.final_diagnosis.all()), 'message' : 'Diagnosis Updated'})

@main.route("/diagnosis_add", methods=["POST"])
def diagnosis_add():
    if request.method == "POST":
        new_diagnosis = request.form["new_diagnosis"]
        diagnosis_model = Diagnosis(disease=new_diagnosis)
        db.session.add(diagnosis_model)
        db.session.commit()
        diagnosis_query = Diagnosis.query.all()
        return jsonify({ "html" : render_template("main/section_diagnosis.html", diagnosis_select = diagnosis_query),
            "message" : f"Added diagnosis {new_diagnosis}." })
    
@main.route("/diagnosis_delete", methods=["POST"])
def diagnosis_delete():
    if request.method == "POST":
        del_diagnosis = request.form["del_diagnosis"]
        diagnosis_query_del = Diagnosis.query.filter_by(disease=del_diagnosis).first()
        db.session.delete(diagnosis_query_del)
        db.session.commit()
        diagnosis_query = Diagnosis.query.all()
        return jsonify({ "html" : render_template("main/section_diagnosis.html", diagnosis_select = diagnosis_query),
            "message" : f"Deleted diagnosis {del_diagnosis}." })

