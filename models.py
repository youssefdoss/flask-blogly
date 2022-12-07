"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    '''Connect to database'''

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    '''User class'''

    __tablename__ = 'users'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(db.Text,
        nullable=False)
    last_name = db.Column(db.Text,
        nullable=False)
    image_url = db.Column(db.Text) # maybe add a default image url and make it not null


