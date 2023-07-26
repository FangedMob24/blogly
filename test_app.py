from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UerViewsTestCase(TestCase):
    """Test for views for Pets"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name="TestUser",last_name="UserLast",image_url="TestSite.com")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>First Name: TestUser</h2>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUser2", "last_name": "UserLast2", "image_url": "TestSite.com"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUserEdit", "last_name": "UserLastedit", "image_url": "TestSite.com"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUserEdit", html)