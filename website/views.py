from flask import Blueprint, render_template, request, send_file
from flask_login import login_required
from flask_security import current_user
import sqlite3
import pandas as pd
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
    #time.sleep(0.5)
    return send_file("static/images/face.jpeg",mimetype="image/jpeg")

@login_required
@views.route('/latest_emotion')
def latest_emotion():
    return send_file("static/images/lastemotion.png",mimetype="image/png")

@login_required
@views.route('/emorec', methods=['GET', 'POST'])
def emorec():
    return render_template("Emorec.html", user=current_user,  patients=get_all_patients())

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
    return render_template("Evaluate.html", user=current_user,  patients=get_all_patients())

@login_required
@views.route('/activities', methods=['GET', 'POST'])
def activities():
    return render_template("Activities.html", user=current_user,  patients=get_all_patients())

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
    return render_template("Metrics.html", user=current_user,  patients=get_all_patients(),chart_data=chart_data)

@login_required
@views.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("Settings.html", user=current_user,  patients=get_all_patients())
