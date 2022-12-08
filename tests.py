from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, connect_db, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )


        second_user = User(
            first_name="test2_first",
            last_name="test2_last",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_post = Post(
            title='test_title',
            content='test_content',
            user_id = self.user_id
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        '''Tests if returns html containing a list of users'''
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_edit_user(self):
        '''Test when user clicks edit button, returns edit form html'''
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a user', html)

    def test_show_add_users(self):
        '''Tests if returns html to show add user form'''
        with self.client as c:
            resp = c.get('/users/new')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_add_user(self):
        '''Tests if returns list of users after new user added'''
        with self.client as c:
            test_additional_user = dict(first_name = 'Jeff', last_name = 'Doe', image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png')
            resp = c.post('/users/new', data=test_additional_user, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Add user</button>', html)

    def test_show_user(self):
        '''Tests if returns html of a specific user clicked on'''
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>test1_first', html)

    def test_show_add_post_form(self):
        '''Tests if it shows the correct add post form'''
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add Post for test1_first', html)

    def test_add_post(self):
        '''Tests if it adds the post correctly and brings back the user page'''
        with self.client as c:
            test_post = dict(title = 'test_title', content='test_content', user_id=self.user_id)
            resp = c.post(f'/users/{self.user_id}/posts/new', data=test_post, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<!--Testing add_post-->', html)

    def test_show_post(self):
        '''Tests if clicking on a post shows the post properly'''
        with self.client as c:
            resp = c.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<i>By test1_first', html)

    def test_show_edit_form(self):
        '''Tests if clicking on the edit button on a post shows the edit form properly'''
        with self.client as c:
            resp = c.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input type="text" name="title" value="test_title">', html)
    

