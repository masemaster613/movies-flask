from flask import render_template, url_for, flash, redirect, request
from flask_app import app, bcrypt, db
from flask_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, LikeForm, MatchForm
from flask_app.models import User, Movie, Category
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
import json
from PIL import Image


def get_my_movies(user, movies_list):
	my_movies = []
	for movie in movies_list:
		if movie not in user.likes + user.dislikes:
			my_movies.append(movie)
	return my_movies




@app.route("/", methods=['GET', 'POST'])
def base():
	return redirect(url_for('login'))

@app.route("/home/", methods=['GET', 'POST'])
@app.route("/home/<category>", methods=['GET', 'POST'])
@login_required
def home(category=''):
	if category:
		movies_list = Category.query.filter_by(name=category).first().movies
	else:
		movies_list = Movie.query.all()
	my_movies = get_my_movies(current_user, movies_list)
	form = LikeForm()
	if form.validate_on_submit():
		if form.like.data:
			current_user.likes.append(my_movies[0])
			db.session.commit()
		elif form.dislike.data:
			current_user.dislikes.append(my_movies[0])
			db.session.commit()
		return redirect(category)
	return render_template('home.html', movies=my_movies, form=form, categories=sorted(Category.query.all()))

@app.route("/matches", methods=['GET', 'POST'])
@login_required
def matches():
	form = MatchForm()
	matches = []
	if form.validate_on_submit():
		matcher = User.query.filter_by(username=form.username_to_match.data).first()
		if matcher:
			for movie in current_user.likes:
				if movie in matcher.likes:
					matches.append(movie)
		else:
			matches = [{'title':'no such user'}]
	return render_template('matches.html', form=form, matches=matches, categories=sorted(Category.query.all()))


@app.route("/about")
def about():
	return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form, categories=sorted(Category.query.all()))


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form, categories=sorted(Category.query.all()))

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


#function for saving pictures in the account route
def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

	output_size=(125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your account has been updated", "success")
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html', title='account', image_file=image_file, form=form, categories=sorted(Category.query.all()))
