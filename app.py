"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask.templating import render_template_string

from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.util.langhelpers import method_is_overridden
from models import db, connect_db, People
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "BLOGLY"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    """List all users and add form"""

    people = People.query.all()
    return render_template("home.html", people = people)
    
@app.route("/new_user")
def new_user():
    """form for new users"""
    return render_template("new_user.html")

@app.route("/new_user", methods=["POST"])
def add_user():
    """add user to db"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    user_name = request.form['user_name']
    image_url = request.form['image_url']

    people = People(first_name=first_name, last_name=last_name, user_name=user_name, img_url=image_url)
    db.session.add(people)
    db.session.commit()

    return redirect("/")

@app.route("/<int:people_id>/details")
def user_profile(people_id):
    """Show user profile"""

    person = People.query.get_or_404(people_id)
    return render_template("details.html", people = person)

@app.route("/<int:people_id>/delete")
def delete_profile(people_id):
    """Delete profile"""

    person = People.query.get_or_404(people_id)
    db.session.delete(person)
    db.session.commit()

    return redirect("/")



@app.route("/<int:people_id>/edit_user")
def edit_user_page(people_id):
    """Show user edit form - pull user id"""
    person = People.query.get_or_404(people_id)
    return render_template("edit_user.html", people = person)


@app.route("/<int:people_id>/edit_user", methods=["POST"])
def edit_user(people_id):
    """Make updates to user in database"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user_name = request.form['user_name']

    person = People.query.get(people_id)
    person.edit_user_info(first_name, last_name, user_name, image_url)
    db.session.add(person)
    db.session.commit()


    # How do I have this redirect to the details page for the user being updated?
    return redirect("/" + str(people_id) + "/details")
    # return redirect("/")