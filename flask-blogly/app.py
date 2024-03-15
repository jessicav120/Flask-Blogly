"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_IMAGE_URL, Post

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'kikostinky'
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    '''Home page'''
    
    return redirect('/users')

@app.route('/users')
def show_list():
    '''Show list of users'''
    
    users = User.query.all()
    return render_template('listing.html', users=users)

##################### USER ROUTES #####################

@app.route('/users/new', methods=['GET', 'POST'])
def create_new_user():
    '''GET new user creation form or POST new user'''
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']
        
        new_user = User(first_name=first_name, 
                        last_name=last_name, 
                        image_url=image_url or None)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/users')
    else:
        return render_template('new_user.html')
    
@app.route('/users/<int:user_id>')
def  show_user_details(user_id):
    '''Show details of a single user'''
    
    user = User.query.get_or_404(user_id)
    #return post list by this user
    user_posts = Post.query.filter(Post.user_id == user.id)
    
    return render_template('details.html', user=user, user_posts=user_posts)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    '''Show User Edit form & process submission'''
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        # if pfp doesn't exist, return default image
        if request.form['image_url']:
            user.image_url = request.form['image_url']
        else:
            user.image_url = DEFAULT_IMAGE_URL
            
        db.session.add(user)
        db.session.commit()
        
        return redirect(f"/users/{user_id}")
    else:
        return render_template('edit_user.html', user=user)
    
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Delete the user from the database'''
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/')
    
################ POST ROUTES ############################
@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''Show a specific post'''
    
    post = Post.query.get_or_404(post_id)
    date = post.pretty_date()
    
    return render_template('post.html', post=post, date=date)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post_form(post_id):
    '''show edit form'''
    
    post = Post.query.get_or_404(post_id)
    date = post.pretty_date()
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
            
        db.session.add(post)
        db.session.commit()
        
        return render_template('post.html', post=post, date=date)
    else:
        return render_template('edit_post.html', post=post)

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    '''Create a new post for this user'''
    
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        new_post = Post(title=title, content=content, user_id=user_id)
        
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(f"/users/{user.id}")
    
    if request.method == 'GET':
        return render_template('add_post.html', user=user)
    
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Delete the selected post'''
    
    post = Post.query.get(post_id)
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{post.user_id}')
        