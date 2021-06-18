from sqlalchemy.orm import backref
from app import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime







class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    photo = db.Column(db.String(150), nullable=False,)

    

    def __init__(self, username, email, password,photo):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.photo = photo

    def __repr__(self):
        return f'<User | {self.username}>'


    def to_dict(self):
        return {
            'id':self.id,
            'username':self.username,
            'email': self.email,
            'password':self.password,
            'photo':self.photo
        }










#model for recipies################

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, default="")
    preparation = db.Column(db.String(500),  nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), nullable=False)
    username = db.Column(db.String(30), nullable=False,  default="")
    likes = db.Column(db.Integer(), nullable=False)
    photo = db.Column(db.String(150), nullable=False,)
    likes_status = db.Column(db.Integer(), nullable=False)
    favourite_status = db.Column(db.Integer(), nullable=False)

    def __init__(self, name, preparation,user_id,username,photo,likes,likes_status,favourite_status):
        self.name = name
        self.preparation = preparation
        self.user_id = user_id
        self.username=username
        self.photo=photo
        self.likes=likes
        self.likes_status=likes_status
        self.favourite_status=favourite_status



    def to_dict(self):
        return {
            'id':self.id,
            'user_id':self.user_id,
            'name':self.name,
            'preparation': self.preparation,
            'likes':self.likes,
            'date_created':self.date_created,
            'username':self.username,
            'photo':self.photo,
            'likes_status':self.likes_status,
            'favourite_status':self.favourite_status
            
        } 





class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(30), nullable=False)
    recipe_id = db.Column(db.Integer(), nullable=False)


    def __init__(self, username, recipe_id):
        self.username = username
        self.recipe_id = recipe_id
        








class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recipe_id = db.Column(db.Integer(), nullable=False)
    user_name = db.Column(db.String(30))
    photo = db.Column(db.String(150), nullable=False,)



    def __init__(self, message, recipe_id,user_name,photo):
        self.message = message
        self.recipe_id=recipe_id
        self.user_name=user_name
        self.photo=photo
        


    def to_dict(self):
        return {
            'id':self.id,
            'message':self.message,
            'date_created':self.date_created,
            'recipe_id':self.recipe_id,
            'user_name':self.user_name,
            'photo':self.photo,
            
            
            
            
        }     


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    contact_id = db.Column(db.Integer(), nullable=False)




    def __init__(self, username, contact_id):
        self.username = username
        self.contact_id=contact_id







class Favourites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    recipe_id = db.Column(db.Integer(), nullable=False)


    def __init__(self, username, recipe_id):
        self.username = username
        self.recipe_id=recipe_id





