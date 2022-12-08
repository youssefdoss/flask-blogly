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
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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
def add_user():
    '''Process the add form, adding a new user and going back to /users'''

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user(user_id):
    '''Show info on a single user'''

    user = User.query.get_or_404(user_id)
    return render_template('user_info.html', user=user)

@app.get('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    '''Shows the edit page for a user'''
    
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''Processes the edit form and returns the user to the /users page'''

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    '''Deletes the user'''

    user = User.query.get_or_404(user_id)
    
    user.delete()

    return redirect('/users')
