"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# First, create a User model for SQLAlchemy. Put this in a models.py file.
# It should have the following columns:
#   id, an autoincrementing integer number that is the primary key
#   first_name and last_name
#   image_url for profile images
# Make good choices about whether things should be required, have defaults, and so on.
class People(db.Model):
    __tablename__ = 'peoples'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    user_name = db.Column(db.String(50),nullable=False, unique = True)
    img_url = db.Column(db.String(),nullable=True)

    psts = db.relationship('Post', backref='peoples')
   
    def edit_user_info(self, f_name, l_name, u_name, url, ):
        """Edit user information in database"""
        self.first_name = f_name
        self.last_name= l_name
        self.user_name= u_name
        self.img_url = url


# Next, add another model, for blog posts (call it Post).
# Post should have an:
# id, like for User
# title
# content
# created_at a date+time that should automatically default to the when the post is created
# a foreign key to the User table

class Post(db.Model):
    """Post Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime(),nullable=False, default=func.now())
    peoples_id = db.Column(db.Integer, db.ForeignKey('peoples.id'))

    posttag = db.relationship('PostTag', backref='post')
    # connectedtags = db.relationship('Tag', secondary = 'posttags', backref='posts')


    def edit_post_info(self, title, content, created_at, peoples_id):
        """Edit post information in database"""
        self.title = title
        self.content= content
        self.created_at= created_at
        self.poeples_id= peoples_id

class Tag(db.Model):
    """Tag Model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50),nullable=False, unique = True)

    posttag = db.relationship('PostTag', backref='tag')

    def edit_tag_info(self, name):
        """Edit tag information in database"""
        self.name = name

class PostTag(db.Model):
    """PostTag Model"""

    __tablename__ = "posttags"

    tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True, nullable=False)
    posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True, nullable=False)

    # def connect_tag(self, tags_id, posts_id)
    # """adds post + tag connection to table"""
    # self.tags_id = tags_id
    # self.posts_id = posts_id
    
