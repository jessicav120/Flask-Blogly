from unittest import TestCase

from app import app
from models import db, connect_db, User, DEFAULT_IMAGE_URL

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyViewsTestCase(TestCase):
    """Tests view functions for users on Blogly."""

    def setUp(self):
        """Add sample User."""

        User.query.delete()

        usr = User(first_name='Test', last_name='Case', image_url=DEFAULT_IMAGE_URL)
        
        db.session.add(usr)
        db.session.commit()

        self.user_id = usr.id
        self.user = usr

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Case', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertIn('User Details', html)
            self.assertIn('<h2>Test Case</h2>', html)
            self.assertIn(self.user.image_url, html)

    def test_new_user(self):
        with app.test_client() as client:
            d = {"first_name": "Another", 
                 "last_name": "Test",
                 "image_url" : DEFAULT_IMAGE_URL}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Another Test", html)