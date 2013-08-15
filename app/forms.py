from flask.ext.wtf import Form, TextField, SelectMultipleField
from flask.ext.wtf import Required
from app import models, db

class TagForm(Form):
	name = TextField('name', validators=[Required()])

class PostForm(Form):
	title = TextField('title', validators=[Required()])
	body = TextField('body', validators=[Required()])
	tags = SelectMultipleField('tags', validators=[Required()], 
							   choices=[(str(tag.id), tag.name) for tag in db.session.query(models.Tag).all()])