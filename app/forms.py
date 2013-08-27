"""
from flask.ext.wtf import Form, TextField, SelectMultipleField, PasswordField
from flask.ext.wtf import Required
from app import models, db

class LoginForm(Form):
	password = PasswordField('password', validators=[Required()])

class TagForm(Form):
	name = TextField('name', validators=[Required()])

class SearchForm(Form):
	query = TextField('query', validators=[Required()])

class PostForm(Form):
	title = TextField('title', validators=[Required()])
	body = TextField('body', validators=[Required()])
	tags = SelectMultipleField('tags', validators=[Required()], 
							   choices=[(str(tag.id), tag.name) for tag in db.session.query(models.Tag).all()])
"""