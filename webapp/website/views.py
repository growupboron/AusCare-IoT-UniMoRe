from flask import Blueprint, render_template, request
from flask_login import login_required
from flask_security import current_user

from .patient import Patient
from .patient import get_all_patients

views = Blueprint('views', __name__)

p = Patient()

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        pass

    return render_template("home.html", user=current_user)


@login_required
@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html", user=current_user,  patients=get_all_patients())

@login_required
@views.route('/dashboard/activities', methods=['GET', 'POST'])
def activities():
    return render_template("Activities.html", user=current_user,  patients=get_all_patients())