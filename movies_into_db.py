from flask_app import db
from flask_app.models import User, Movie, Category
import json




def movies_into_db():
	file = input('where is the json? ')
	category_in = input('is there a category? ')
	if category_in:
		if Category.query.filter_by(name=category_in).first():
			category_class = Category.query.filter_by(name=category_in).first()
		else:
			category_class = Category(name=category_in)

	with open(file) as f:
		movies_json = json.load(f)

	for movie in movies_json:
		if Movie.query.filter_by(title=movie['title']).first():
			print(movie['title'] + ' is already in database')
			if category_class not in Movie.query.filter_by(title=movie['title']).first().categories:
				Movie.query.filter_by(title=movie['title']).first().categories.append(category_class)
				print(category_class.name + ' has been added to it\'s categories')
			Movie.query.filter_by(title=movie['title']).first().image = movie['image']
			Movie.query.filter_by(title=movie['title']).first().synopsis = movie['synopsis']
			Print('Image and synopsis updated')
		else:
			movie_class = Movie(title=movie['title'], released=movie['released'], synopsis=movie['synopsis'], image=movie['image'], categories=[category_class])
			db.session.add(movie_class)
		db.session.commit()
