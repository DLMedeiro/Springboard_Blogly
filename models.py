"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

    @classmethod
    def edit_user_info(self, f_name, l_name, u_name, url):
        """Edit user information in database"""
        self.first_name = f_name
        self.last_name= l_name
        self.user_name= u_name
        self.img_url = url

