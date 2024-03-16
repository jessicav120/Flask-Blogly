from unittest import TestCase

from app import app
from models import db, connect_db, User, DEFAULT_IMAGE_URL, Post   

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
        """Add sample User and Sample Post."""

        Post.query.delete()
        User.query.delete()

        usr = User(first_name='Test', last_name='Case', image_url=DEFAULT_IMAGE_URL)
        db.session.add(usr)
        db.session.commit()
        
        post = Post(title='Test Post', content='Testing Content', user_id=usr.id)
        db.session.add(post)
        db.session.commit()

        self.post = post
        self.post_id = post.id
        
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-2"> Test Post </h1>', html)
            self.assertIn('<p>Testing Content</p>', html)

    def test_new_post(self):
        with app.test_client() as client:
            d = {"title": "Test Post 2", 
                 "content": "More Test Content",
                 "user_id": self.post.user_id}
            resp = client.post(f"/users/{self.post.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post 2', html)