import datetime as dt
from flask import Blueprint, Flask, flash
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from flask import request, render_template, redirect, url_for
import pytz
from telegramBot import add_volunteer_to_group

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rescue.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'zaq12345'
db = SQLAlchemy(app)

teaming = Blueprint('team', __name__, url_prefix='/team')
volunteering = Blueprint('volunteer', __name__, url_prefix='/volunteer')


class TeamStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ONLEAVE = "On Leave"

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=True, default=lambda: dt.datetime.now())
    description = db.Column(db.Text, nullable=False)
    finishedTask = db.Column(db.Boolean, nullable=False, default=False)
    assignedTeam = db.Column(db.String(100), nullable=True)

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    telegram_contact = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    TeamID = db.Column(db.Integer, db.ForeignKey('team.TeamID'))
    description = db.Column(db.Text, nullable=True)
    

class Team(db.Model):
    TeamID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    job = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(TeamStatus), nullable=False, default=TeamStatus.INACTIVE)
    composition = db.Column(db.Text, nullable=True)  # stores team composition (e.g. list of volunteer roles)
    point_of_contact = db.Column(db.String(100), nullable=True)  # stores team point of contact (e.g. name, email, phone)
    volunteers = db.relationship('Volunteer', backref='team', lazy=True)



def catch_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return "Error: " + str(e)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route("/")
@catch_errors
def index():
    incidents = Incident.query.all()
    return render_template("admin.html", incidents=incidents)

@app.route("/newincident", methods=["GET", "POST"], endpoint = "newincident")
@catch_errors
def incident():
    if request.method == "POST":
        # Get the form data
        description = request.form["description"]
        finishedTask = request.form["finishedTask"] == "True"
        assignedTeam = request.form["assignedTeam"]

        # Create a new Incident object
        incident = Incident(
            description=description,
            finishedTask=finishedTask,
            assignedTeam=assignedTeam
        )

        # Add the incident to the database
        db.session.add(incident)
        db.session.commit()

        # Flash a success message
        flash("Incident reported successfully!")

        # Redirect to the incidents page
        return redirect(url_for("newincident"))

    # Render the incident.html template
    return render_template("incident.html")


@volunteering.route("/register", methods=["GET", "POST"])
@catch_errors
def volunteer_register():
    if request.method == "POST":
        print(str(request.form))
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        telegram_contact = request.form["telegram_contact"]
        skills = request.form["skills"]
        description = request.form["description"]
        volunteer = Volunteer(name=name, email=email, phone=phone, 
                        telegram_contact=telegram_contact, skills=skills, description=description)
        db.session.add(volunteer)
        db.session.commit()
        add_volunteer_to_group(telegram_contact)
        print(volunteer)
        flash("Volunteer registered successfully!")
        return redirect(url_for("volunteer_list"))
    return render_template("volunteer_register.html")

@app.route("/volunteer/list", methods=["GET"])
@catch_errors
def volunteer_list():
    volunteers = Volunteer.query.all()
    return render_template("volunteer_list.html", volunteers=volunteers)

@app.route("/volunteer/<int:volunteer_id>", methods=["GET"])
def volunteer_details(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    return render_template("volunteer_details.html", volunteer=volunteer)

@app.route("/volunteer/<int:volunteer_id>/update", methods=["GET","POST"])
def volunteer_status_update(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    if request.method == "POST":
        volunteer.name = request.form["name"]
        volunteer.email = request.form["email"]
        volunteer.phone = request.form["phone"]
        volunteer.TeamID = request.form["TeamID"]
        volunteer.skills = request.form["skills"]
        volunteer.description = request.form["description"]
        db.session.commit()
        flash("Volunteer status updated successfully!")
        return redirect(url_for("volunteer_status_update", volunteer_id=volunteer.id))
    return render_template("volunteer_update.html", volunteer=volunteer)

@app.route("/team/list")
def teams():
    teams = Team.query.all()
    return render_template("teams.html", teams=teams)

@app.route("/team/<int:team_id>/update", methods=["GET", "POST"])
def team(team_id):
    team = Team.query.get_or_404(team_id)
    if request.method == "POST":
        team.name = request.form["name"]
        team.description = request.form["description"]
        db.session.commit()
        flash("Team updated successfully!")
        return redirect(url_for("teams"))
    return render_template("team.html", team=team)


@app.route("/team/add", methods=["GET", "POST"])
def add_team():
    if request.method == "POST":
        team = Team(name=request.form["name"], description=request.form["description"])
        db.session.add(team)
        db.session.commit()
        flash("Team added successfully!")
        return redirect(url_for("teams"))
    return render_template("add_team.html")










app.register_blueprint(teaming)
app.register_blueprint(volunteering)



from app import app, db


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()