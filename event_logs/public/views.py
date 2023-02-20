# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user

from event_logs import app
from event_logs.extensions import login_manager
from event_logs.orm.event import EventLog
from event_logs.public.forms import LoginForm
from event_logs.services.importer.event_import import EventImporter
from event_logs.user.forms import RegisterForm
from event_logs.user.models import User
from event_logs.utils import flash_errors


blueprint = Blueprint("public", __name__, static_folder="../static")

@blueprint.route("/import_events")
def import_events():
    """Initial csv data load."""
    EventImporter().load_to_db()
    return "Imported data succeed"


@blueprint.route("/query/<customer_id>")
def query_events_by_customer_id(customer_id):
    """Display all events by customer_id."""
    query = """SELECT customer_id, transaction_id, timestamp
                FROM event_log 
                WHERE customer_id = "{}" 
                """.format(customer_id)
    
    results = []

    with app.get_engine().connect() as con:
        rs = con.execute(query)
        for row in rs:
            results.append(dict(row))
            print(row)

    return results

@blueprint.route("/query/<customer_id>/<start_time>/<end_time>")
def query_events_by_start_end_time(customer_id, start_time, end_time):
    """Query and return customer events by hour between start and end time. """
    query = """SELECT  
                strftime('%Y-%m-%d %H:00:00', timestamp) AS hour_bucket, 
                COUNT(transaction_id) AS total_transactions
                FROM event_log 
                WHERE customer_id = "{}" AND timestamp > "{}" AND timestamp < "{}"
                Group By hour_bucket
                ORDER By hour_bucket ASC""".format(customer_id, start_time, end_time) 
                
    
    results = []

    with app.get_engine().connect() as con:
        rs = con.execute(query)
        for row in rs:
            results.append(dict(row))
            print(row)

    return {"results":results,"customer_id":customer_id}

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
