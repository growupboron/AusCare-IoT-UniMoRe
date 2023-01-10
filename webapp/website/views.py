from flask import Blueprint, render_template, request
from flask_login import login_required
from flask_security import current_user

from .patient import Patient
from .patient import get_all_patients

import subprocess

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
@views.route('/emorec', methods=['GET', 'POST'])
def emorec():
    return render_template("Emorec.html", user=current_user,  patients=get_all_patients())

process = None
@app.route('/process', methods=['POST'])
def process_route():
    global process
    data = request.get_json()
    if data['state']:
        process = subprocess.Popen(["python", "your_script.py"])
    else:
        process.terminate()
    return "", 204

# @login_required
# @views.route('/evaluate', methods=['GET', 'POST'])
# def evaluate():
#     return render_template("Evaluate.html", user=current_user,  patients=get_all_patients())

@login_required
@views.route('/activities', methods=['GET', 'POST'])
def activities():
    return render_template("Activities.html", user=current_user,  patients=get_all_patients())

@login_required
@views.route('/metrics', methods=['GET', 'POST'])
def metrics():
    return render_template("Metrics.html", user=current_user,  patients=get_all_patients())

@login_required
@views.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("Settings.html", user=current_user,  patients=get_all_patients())