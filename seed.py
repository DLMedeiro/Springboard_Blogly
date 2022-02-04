"""Seed file to make sample data for users db."""
""" (venv) python seed.py"""

from os import stat_result
from typing import ByteString
from models import People, db, Post, Tag, PostTag
from app import app



#Create tables
db.drop_all()
db.create_all()

#If table isn't empty, empty it
People.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()


#Create People
john_lennon = People(first_name="John", last_name="Lennon", user_name="JL_Guitar", img_url = "https://images.pexels.com/photos/6966/abstract-music-rock-bw.jpg")
paul_mccartney = People(first_name="Paul", last_name="McCartney", user_name="PM_BassGuitar", img_url = "https://images.pexels.com/photos/1389429/pexels-photo-1389429.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
george_harrison = People(first_name="George", last_name="Harrison", user_name="GH_Guitar", img_url = "https://images.pexels.com/photos/144429/pexels-photo-144429.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
ringo_star = People(first_name="Ringo", last_name="Star", user_name="RS_Drums", img_url="https://images.pexels.com/photos/542553/pexels-photo-542553.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")
pete_best = People(first_name="Pete", last_name="Best", user_name="Pete_B", img_url="https://images.pexels.com/photos/675960/mic-music-sound-singer-675960.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
tommy_moore = People(first_name="Tommy", last_name="Moore", user_name="TM_Drums", img_url="https://images.pexels.com/photos/9010102/pexels-photo-9010102.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")

#Create Posts
p1 = Post(title = "Post 1", content = "This is my first post", peoples_id = 1)
p2 = Post(title = "Post 2", content = "Sally sells sea shells down by the sea shore", peoples_id = 1)
p3 = Post(title = "Post 3", content = "Here There - Huey Daze", peoples_id = 4)

# Create Tags
tag1 = Tag(name = "Fun")
tag2 = Tag(name = "New")
tag3 = Tag(name = "Old")


# Create PostTag
PT1 = PostTag(posts_id = 1, tags_id = 1)
PT2 = PostTag(posts_id = 1, tags_id = 2)
PT3 = PostTag(posts_id = 2, tags_id = 3)
PT4 = PostTag(posts_id = 2, tags_id = 1)



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

# add tags to session
db.session.add_all([tag1, tag2, tag3])

# Commit tags
db.session.commit()

# add and commit PostTags
db.session.add_all([PT1, PT2, PT3, PT4])
db.session.commit()
