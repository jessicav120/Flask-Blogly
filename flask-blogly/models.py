"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text 
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
DEFAULT_IMAGE_URL = 'https://static.vecteezy.com/system/resources/thumbnails/005/544/718/small/profile-icon-design-free-vector.jpg'

#MODELS
class User(db.Model):
    '''Create user'''
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)
    
class Post(db.Model):
    '''Make a post'''
    
    __tablename__='posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime,  nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.Relationship('User')
    
    def pretty_date(self):
        '''return a prettier format of date'''
        date = self.created_at
        pretty_date = date.strftime('%b/%d/%Y %-I:%M %p')
            
        return pretty_date