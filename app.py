"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'SECRET!'
debug = DebugToolbarExtension(app)

db.create_all()


@app.get('/')
def redirect_to_users():
    '''Redirects user at homepage to users list'''

    return redirect('/users')


@app.get('/users')
def list_users():
    '''List users and show home page with add button'''

    users = User.query.all()
    return render_template('list.html', users=users)



@app.get('/users/new')
def show_add_users():
    '''Shows create user form with add button'''

    return render_template('new_user_form.html')


@app.post('/users/new')
def handle_form_submission():
    '''Process the add form, adding a new user and going back to /users'''

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

