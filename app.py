"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, DEFAULT_IMAGE_URL, Post
from sqlalchemy import delete

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
    image_url = request.form['image_url'] or None

    user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user(user_id):
    '''Show info on a single user'''

    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('user_info.html', user=user, posts = posts)

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
    image_url = request.form['image_url'] or DEFAULT_IMAGE_URL

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

    User.query.filter_by(id = user_id).delete()

    db.session.commit()

    flash("User deleted")

    return redirect('/users')

@app.get('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    '''Shows add post form for that user'''

    user = User.query.get_or_404(user_id)
    return render_template('new_post_form.html', user=user)

@app.post('/users/<int:user_id>/posts/new')
def add_post(user_id):
    '''Handle add form; add post and redirect to the user detail page'''

    title = request.form['title']
    content = request.form['content']

    post = Post(title = title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def show_post(post_id):
    '''Show a post. Show buttons to edit and delete that post'''

    post = Post.query.get_or_404(post_id)
    user = post.user

    render_template('post_detail.html', post=post, user=user)

@app.get('/posts/<int:post_id>/edit')
def show_edit_form(post_id):
    '''Show form to edit a post, and to cancel (back to user page)'''

    post = Post.query.get_or_404(post_id)
    user = post.user

    render_template('edit_post.html', post=post, user=user)

@app.post('/posts/<int:post_id>/edit')
def edit_post(post_id):
    '''Handle editing of a post. Redirect back to the post view'''

    title = request.form['title']
    content = request.form['content']

    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    '''Delete the post'''

    post = Post.query.filter_by(id = post_id)
    user_id = post.user.id
    post.delete()

    db.session.commit()

    flash("Post Deleted")

    return redirect(f'/users/{user_id}')