from flask import render_template, request, jsonify
from flask.helpers import url_for
from . import main
from .. import db

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', back_link = url_for('main.index'), e=e), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template('500.html', back_link = url_for('main.index'),e=e), 500