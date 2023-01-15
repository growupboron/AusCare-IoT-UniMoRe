from datetime import datetime

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


def convert_timestamp(timestamp):
    # Convert the timestamp to a readable format
    dt_object = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    return dt_object.date()


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
    patients = get_all_patients()
    latest_update = patients[len(patients) - 1]
    return render_template("Emorec.html", user=current_user, latest_update=latest_update)


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
    conn = sqlite3.connect('instance/database.db')
    data = pd.read_sql_query("SELECT * from Patient", conn)
    conn.close()
    # list of unique dates in the database except None values --> the x axis of our line chart
    dates = data['timestamp'].unique()
    dates = pd.Series(dates).dropna().tolist()
    data['timestamp'].apply(convert_timestamp)
    data['timestamp'] = data['timestamp'].apply(convert_timestamp)
    # list of the number of people met for each day in the dates list --> the y axis of our line chart
    counters = data['people_counter'].groupby(data['timestamp']).count().tolist()
    print(counters)

    # pie chart data processing
    pie_data = {emotion: 0 for emotion in data['emotion'].unique().tolist() if emotion != None}

    for emotion in data['emotion']:
        if emotion != None:
            pie_data[emotion] += 1
    print(pie_data)

    # x_axis : days                            (14/01/2022)
    # y_axis : no of timestamps in that day    (14/01/2022 00:00 23:59)

    x_axis = data['timestamp'].tolist()
    y_axis = data['people_counter'].tolist()

    line_chart_data = {
        'labels': dates,
        'datasets': [{
            'label': 'No of People',
            'data': counters,
            'fill': False,
            'borderColor': 'rgba(75,192,192,1)',
            'lineTension': 0.1
        }]
    }
    pie_chart_data = {
        'labels': list(pie_data.keys()),
        'datasets': [{
            'data': list(pie_data.values()),
            'backgroundColor': ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)',
                                'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)',
                                'rgba(252, 201, 186, 0.2)'],
            'borderColor': ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)',
                            'rgba(252, 201, 186, 1)'],
            'borderWidth': 1
        }]
    }
    print(line_chart_data)
    print(current_user)
    # return render_template("Metrics.html", user=current_user, patients=get_all_patients(), chart_data=line_chart_data, pie_chart_data=pie_chart_data)
    return render_template("Metrics2.html", user=current_user, patients=get_all_patients(),
                           line_chart_data=line_chart_data, pie_chart_data=pie_chart_data)


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
    flash('Settings updated successfully!', category='success')
    return redirect('/settings')


def update_user_in_db(user_id, new_name, new_email):
    # Update the user's information in the database
    # with the new name and email
    db.session.query(User).filter_by(id=user_id).update({'first_name': new_name, 'email': new_email})
    db.session.commit()
