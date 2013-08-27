from flask import render_template, flash, redirect
from app import app, models, db, login_manager
from forms import TagForm, PostForm, SearchForm, LoginForm
from flask.ext.login import login_user, logout_user, login_required
from sqlalchemy_searchable import search
from admin import User
from config import RESULTS_PER_PAGE
from math import ceil

@app.route('/')
@app.route('/index')
@app.route('/blog')
@app.route('/index/<int:page>')
def index(page = 1):
	posts = models.Post.query.paginate(page, RESULTS_PER_PAGE, False)
	num = int(ceil(posts.total / RESULTS_PER_PAGE))
	return render_template('index.html', title="Home", posts=posts.items, number_of_pages=num)

@app.route('/blog/<id>')
def blog(id):
	post = db.session.query(models.Post).filter_by(id=id).one()
	return render_template('blog.html', title=post.title, post=post)

@app.route('/search', methods=['GET', 'POST'])
def search_post():
	form = SearchForm()
	if form.validate_on_submit():
		results = search(db.session.query(models.Post), form.query.data).limit(5).all()
		if results:
			return render_template('search.html', title="Search Results - ", form=form, results=results)
		flash('No results found! Try again')
		return redirect('/search')
	return render_template('search.html', title="Search", form=form)

@login_manager.user_loader
def load_user(userid):
	return User()

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.password.data == User.password:
			flash('Login Successful!')
			login_user(User())
			return redirect('/admin')
		else:
			flash('Bad password!')
			return redirect('/index')
	return render_template('login.html', title="Login - ", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout Successful!')
    return redirect('/index')

@app.route('/admin')
@login_required
def admin():
	tags = db.session.query(models.Tag).all()
	posts = db.session.query(models.Post).all()
	return render_template('admin.html', posts=posts, tags=tags, admin=True)

@app.route('/admin/new_tag', methods=['GET', 'POST'])
@login_required
def new_tag():
	form = TagForm()
	if form.validate_on_submit():
		flash('Tag with name %r created successfully!' % (form.name.data))
		new_tag = models.Tag(name=form.name.data)
		db.session.add(new_tag)
		db.session.commit()
		return redirect('/admin/new_tag')
	return render_template('new_tag.html', title="New Tag - Admin", form=form, admin=True)

@app.route('/admin/delete_tag/<name>')
@login_required
def delete_tag(name):
	tag = db.session.query(models.Tag).filter_by(name=name).one()
	db.session.delete(tag)
	db.session.commit()
	flash('Tag with name %r deleted successfully!' % (name))
	return redirect('/admin')

@app.route('/admin/edit_tag/<name>', methods=['GET', 'POST'])
@login_required
def edit_tag(name):
	form = TagForm()
	if form.validate_on_submit():
		tag = db.session.query(models.Tag).filter_by(name=name).one()
		tag.name = form.name.data
		db.session.commit()
		flash('Tag with name %r changed to %r successfully!' % (name, form.name.data))
		return redirect('/admin')
	form.name.data = name
	return render_template('new_tag.html', title="Edit Tag - Admin", form=form, admin=True)

@app.route('/admin/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		tags = [db.session.query(models.Tag).filter_by(id=int(id)).one()
				for id in form.tags.data]
		new_post = models.Post(title=form.title.data, body=form.body.data, tags=tags)
		db.session.add(new_post)
		db.session.commit()
		flash('Post with title %r created successfully!' % (new_post.title))
		return redirect('/index')
	return render_template('new_post.html', title="New Post - Admin", form=form, admin=True)

@app.route('/admin/edit_post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	form = PostForm()
	if form.validate_on_submit():
		post = db.session.query(models.Post).filter_by(id=id).one()
		post.title = form.title.data
		post.body = form.body.data
		tags = [db.session.query(models.Tag).filter_by(id=int(id)).one()
				for id in form.tags.data]
		post.tags = list(set(post.tags + tags))
		db.session.commit()
		flash('Post with title %r edited successfully!' % (post.title))
		return redirect('/admin')
	post = db.session.query(models.Post).filter_by(id=id).one()
	form.title.data = post.title
	form.body.data = post.body
	return render_template('new_post.html', title="Edit Post - Admin", form=form)

@app.route('/admin/delete_post/<id>')
@login_required
def delete_post(id):
	post = db.session.query(models.Post).filter_by(id=id).one()
	db.session.delete(post)
	db.session.commit()
	flash('Post with title %r deleted' % (post.title))
	return redirect('/admin')

@app.route('/admin/remove_tag/<id>/<name>')
@login_required
def remove_tag(id, name):
	post = db.session.query(models.Post).filter_by(id=id).one()
	tag = db.session.query(models.Tag).filter_by(name=name).one()
	post.tags = list(set(post.tags) - set([tag]))
	db.session.commit()
	return redirect('/admin')