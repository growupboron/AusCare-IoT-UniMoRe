from flask import Blueprint, render_template, request, send_file, redirect, flash, url_for, g
from flask_login import login_required
from flask_security import current_user
import sqlite3
import pandas as pd

from . import db
from .models import User
from .patient import Patient
from .patient import get_all_patients

import subprocess
import time

views = Blueprint('views', __name__)

p = Patient()


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


'''
@login_required
@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html", user=current_user,  patients=get_all_patients())'''


@login_required
@views.route('/latest_face')
def latest_face():
    # time.sleep(0.5)
    return send_file("static/images/face.jpeg", mimetype="image/jpeg")


@login_required
@views.route('/latest_emotion')
def latest_emotion():
    return send_file("static/images/lastemotion.png", mimetype="image/png")


@login_required
@views.route('/emorec', methods=['GET', 'POST'])
def emorec():
    return render_template("Emorec.html", user=current_user, patients=get_all_patients())


process = None


@login_required
@views.route('/process', methods=['POST'])
def process_route():
    global process
    data = request.get_json()
    global process
    if data['state']:
        process = subprocess.Popen(["python", "website/emotion_detect.py"])
    else:
        process.terminate()
    return "", 204


@login_required
@views.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    return render_template("Evaluate.html", user=current_user, patients=get_all_patients())


@login_required
@views.route('/activities', methods=['GET', 'POST'])
def activities():
    return render_template("Activities.html", user=current_user, patients=get_all_patients())


@login_required
@views.route('/metrics', methods=['GET', 'POST'])
def metrics():
    conn = sqlite3.connect('../instance/database.db')
    data = pd.read_sql_query("SELECT * from Patient", conn)
    conn.close()
    x_axis = data['last_timestamp'].tolist()
    y_axis = data['people_counter'].tolist()
    chart_data = {
        'labels': x_axis,
        'datasets': [{
            'label': 'No of People',
            'data': y_axis,
            'fill': False,
            'borderColor': 'rgba(75,192,192,1)',
            'lineTension': 0.1
        }]
    }
    return render_template("Metrics2.html", user=current_user, patients=get_all_patients(), chart_data=chart_data)


@login_required
@views.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("Settings.html", user=current_user, patients=get_all_patients())


@login_required
@views.route('/update_settings', methods=['GET', 'POST'])
def update_settings():
    user = current_user
    new_name = request.form['name']
    new_email = request.form['email']
    # update user's information in the database
    update_user_in_db(user.id, new_name, new_email)
    flash('Settings updated successfully!')
    return redirect('/settings')


def update_user_in_db(user_id, new_name, new_email):
    # Update the user's information in the database
    # with the new name and email
    db.session.query(User).filter_by(id=user_id).update({'name': new_name, 'email': new_email})
