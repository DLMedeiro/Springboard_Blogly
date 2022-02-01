"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask.templating import render_template_string

from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.util.langhelpers import method_is_overridden
from models import db, connect_db, People, Post, Tag, PostTag
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
def main_home():
    """Landing page"""

    return render_template("main_home.html")

@app.route("/home")
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

    return redirect("/home")

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
    person.edit_user_info(str(first_name), str(last_name), str(user_name), str(image_url))
    db.session.add(person)
    db.session.commit()

    return redirect("/" + str(people_id) + "/details")
    # return redirect("/")

# Posts
@app.route("/<int:people_id>/details/new_post")
def new_post(people_id):
    """form for new posts based on user profile"""
    person = People.query.get(people_id)
    taglist = Tag.query.all()
    return render_template("new_post.html", people = person, taglist = taglist)

@app.route("/<int:people_id>/details/new_post", methods=["POST"])
def add_post(people_id):
    """add new post to db"""

    title = request.form['title']
    content = request.form['content']
    peoples_id = people_id

    post = Post(title=title, content=content, peoples_id=people_id)
    db.session.add(post)
    db.session.commit()
    newpost_id = post.id

    # How to connect new post id to tags, when the post id isn't created until after the form is submitted
    selectedtags = request.form.getlist('tagID')
    if selectedtags:
        for tag in selectedtags:
            tag = Tag.query.filter(Tag.name == tag)
            post_tag = PostTag(tags_id = tag.first().id, posts_id = newpost_id )
            db.session.add(post_tag)
            db.session.commit()

    return redirect("/" + str(people_id) + "/details")

@app.route("/<int:post_id>/post")
def post_detail(post_id):
    """Show user post"""

    posts = Post.query.get_or_404(post_id)
    person_id = posts.peoples_id
    person = People.query.get_or_404(person_id)

    taglist = PostTag.query.filter_by(posts_id = post_id).all()

    tagnames = Tag.query.all()

    return render_template("post.html", posts = posts, person = person, person_id = person_id, taglist = taglist, tagnames = tagnames)


@app.route("/<int:post_id>/edit_post")
def edit_post_page(post_id):
    """Show post edit form"""

    post = Post.query.get_or_404(post_id)
    person_id = post.peoples_id
    person = People.query.get_or_404(person_id)

    taglist = Tag.query.all()
    # How can i set this up where the already selected tags are checked off? (similar to having the values already showing on the text boxes)
    # posttags = PostTag.query.filter(PostTag.posts_id == post_id).all()

    return render_template("edit_post.html", post = post, person=person, taglist = taglist)

@app.route("/<int:post_id>/edit_post", methods=["POST"])
def edit_post(post_id):
    """Make updates to the post in database"""
    title = request.form['title']
    content = request.form['content']
    created_at = request.form['created_at']

    post = Post.query.get(post_id)
    peoples_id = post.peoples_id
    post.edit_post_info(title, content, created_at, peoples_id)

    PostTag.query.filter(PostTag.posts_id == post_id).delete()

    selectedtags = request.form.getlist('tagID')
    # https://stackoverflow.com/questions/67394290/flaskajax-how-to-send-and-get-multiple-checkbox-values

    if selectedtags:
        for tag in selectedtags:
            tag = Tag.query.filter(Tag.name == tag)
            post_tag = PostTag(tags_id = tag.first().id, posts_id = post_id )
            db.session.add(post_tag)
            db.session.commit()


    db.session.add(post)
    db.session.commit()



    return redirect("/" + str(post_id) + "/post")

@app.route("/<int:post_id>/deletepost")
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    person_id = post.peoples_id
    db.session.delete(post)
    db.session.commit()

    return redirect("/" + str(person_id) + "/details")

# Tags
@app.route("/tags_list")
def tags_list():
    """List of all tags"""
    tags = Tag.query.all()
    return render_template("/tags_list.html", tags=tags)

@app.route("/new_tag")
def new_tag():
    """Create a new tag name"""
    return render_template("new_tag.html")

@app.route("/new_tag", methods=["POST"])
def add_tag():
    """add tag to db"""

    name = request.form['name']

    tag = Tag(name= name)
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags_list")

@app.route("/tag_list/<int:tag_id>/details")
def tag_detail(tag_id):
    """Show tag details - edit / remove and list associated posts"""

    tag = Tag.query.get_or_404(tag_id)

    postlist = PostTag.query.filter_by(tags_id = tag_id).all()

    posttitles = Post.query.all()

    return render_template("tag_detail.html", tag = tag, postlist = postlist, posttitles = posttitles)

@app.route("/tag_list/<int:tag_id>/deletetag")
def delete_tag(tag_id):
    """Delete tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags_list")

@app.route("/tag_list/<int:tag_id>/edit_tag")
def edit_tag_page(tag_id):
    """Show tag edit form"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit_tag.html", tag = tag)

@app.route("/tag_list/<int:tag_id>/edit_tag", methods=["POST"])
def edit_tag(tag_id):
    """Make updates to a tag in database"""
    name = request.form['name']

    tag = Tag.query.get(tag_id)
    tag.edit_tag_info(name)
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags_list")
