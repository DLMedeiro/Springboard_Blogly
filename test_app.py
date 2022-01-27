from unittest import TestCase
from app import app
from models import db, People, Post
from sqlalchemy.sql import func

# (venv) python -m unittest test_app.py


app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
# danielle@DESKTOP-AD3BEH2:~/Springboard/SQL/SQLAlchemy/flask-blogly$ createdb blogly_test
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()

# People Tests
class PeopleModelTestCase(TestCase):
    def setUp(self):
        """Clean up exisitng database"""

        People.query.delete()
        people = People(first_name = "FN_Test1", last_name = "LN_Test1", user_name = "UN_Test1")
        db.session.add(people)
        db.session.commit()

        self.people_id = people.id
        # Creates a reference to be used throughout the class

    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('FN_Test1', html)

    def test_user_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.people_id}/details")
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>FN_Test1 LN_Test1</h1>', html)

    def test_new_user(self):
        with app.test_client() as client:
            d = {"first_name":"FN_Test2", "last_name":"LN_Test2", "user_name":"UN_Test2", "image_url": "None"}
            resp = client.post("/new_user", data = d, follow_redirects=True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('FN_Test2 LN_Test2', html)

    def test_delete_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.people_id}/delete", follow_redirects  = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('', html)

# Post Tests
class PostModelTestCase(TestCase):
    def setUp(self):
        """Clean up exisitng database"""
        People.query.delete()
        Post.query.delete()
        people = People(first_name = "FN_Test1", last_name = "LN_Test1", user_name = "UN_Test1")
        db.session.add(people)
        db.session.commit()
        p1 = Post(title = "Post 1", content = "Post 1", created_at = func.now(), peoples_id = people.id)
        db.session.add(p1)
        db.session.commit()

        self.people_id = people.id
        self.post_id = p1.id
        # Creates a reference to be used throughout the class

    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()

    def test_user_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.people_id}/details")
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/1/post" class="list">Post 1</a>', html)

