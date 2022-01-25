"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask.templating import render_template_string

from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.util.langhelpers import method_is_overridden
from models import db, connect_db, People, Post
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

    post = Post.query.all()

    return render_template("details.html", people = person, post = post)

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

# Posts
@app.route("/<int:people_id>/details/new_post")
def new_post(people_id):
    """form for new posts based on user profile"""
    person = People.query.get(people_id)
    return render_template("new_post.html", people = person)

@app.route("/<int:people_id>/details/new_post", methods=["POST"])
def add_post(people_id):
    """add new post to db"""

    title = request.form['title']
    content = request.form['content']
    peoples_id = people_id

    post = Post(title=title, content=content, peoples_id=people_id)
    db.session.add(post)
    db.session.commit()

    return redirect("/" + str(people_id) + "/details")

@app.route("/<int:post_id>/post")
def post_detail(post_id):
    """Show user post"""

    posts = Post.query.get_or_404(post_id)
    person_id = posts.peoples_id
    person = People.query.get_or_404(person_id)

    return render_template("post.html", posts = posts, person = person, person_id = person_id)

@app.route("/<int:post_id>/edit_post")
def edit_post_page(post_id):
    """Show post edit form"""

    post = Post.query.get_or_404(post_id)
    person_id = post.peoples_id
    person = People.query.get_or_404(person_id)

    return render_template("edit_post.html", post = post, person=person)

@app.route("/<int:post_id>/edit_post", methods=["POST"])
def edit_post(post_id):
    """Make updates to the post in database"""
    title = request.form['title']
    content = request.form['content']
    created_at = request.form['created_at']

    post = Post.query.get(post_id)
    peoples_id = post.peoples_id
    post.edit_post_info(title, content, created_at, peoples_id)
    db.session.add(post)
    db.session.commit()
# Not updating the post in the database, directing properly
    return redirect("/" + str(post_id) + "/post")
    # return redirect("/")


@app.route("/<int:post_id>/deletepost")
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    person_id = post.peoples_id
    db.session.delete(post)
    db.session.commit()

    return redirect("/" + str(person_id) + "/details")
