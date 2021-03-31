from datetime import datetime
from flask_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    )

dislikes = db.Table('dislikes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    )

categories = db.Table('categories',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    likes = db.relationship('Movie', secondary=likes, lazy='subquery', backref=db.backref('liked_by', lazy=True))
    dislikes = db.relationship('Movie', secondary=dislikes, lazy='subquery', backref=db.backref('disliked_by', lazy=True))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    released = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
    synopsis = db.Column(db.Text, default='')


    def __repr__(self):
        return f"Movie('{self.title}', '{self.released}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    movies = db.relationship('Movie', secondary=categories, lazy='subquery', backref=db.backref('categories', lazy=True))
    def __repr__(self):
        return f"Category('{self.name}')"

    def __lt__(self, other):
        return self.name < other.name

    

 