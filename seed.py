"""Seed file to make sample data for users db."""

from os import stat_result
from typing import ByteString
from models import People, db, Post
from app import app

#Create tables
db.drop_all()
db.create_all()

#If table isn't empty, empty it
People.query.delete()

#Create People
john_lennon = People(first_name="John", last_name="Lennon", user_name="JL_Guitar")
paul_mccartney = People(first_name="Paul", last_name="McCartney", user_name="PM_BassGuitar")
george_harrison = People(first_name="George", last_name="Harrison", user_name="GH_Guitar")
ringo_star = People(first_name="Ringo", last_name="Star", user_name="RS_Drums")
pete_best = People(first_name="Pete", last_name="Best", user_name="Pete_B")
tommy_moore = People(first_name="Tommy", last_name="Moore", user_name="TM_Drums")

#Create Posts
p1 = Post(title = "Post 1", content = "This is my first post", peoples_id = 1)
p2 = Post(title = "Post 2", content = "Sally sells sea shells down by the sea shore", peoples_id = 1)
p3 = Post(title = "Post 3", content = "Here There - Huey Daze", peoples_id = 4)

# Add new people objects to session, so they'll persist
db.session.add(john_lennon)
db.session.add(paul_mccartney)
db.session.add(george_harrison)
db.session.add(ringo_star)
db.session.add(pete_best)
db.session.add(tommy_moore)

#Commit people
db.session.commit()

#add post objects to session
db.session.add_all([p1, p2, p3])

#commit posts
db.session.commit()

