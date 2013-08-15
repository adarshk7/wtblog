from flask import render_template, flash, redirect
from app import app, models, db
from forms import TagForm, PostForm

@app.route('/')
@app.route('/index')
def index():
	posts = db.session.query(models.Post).order_by(models.Post.id.desc()).offset(0).limit(5).all()
	return render_template('index.html', title="Home", posts=posts)

@app.route('/blog/<id>')
def blog(id):
	post = db.session.query(models.Post).filter_by(id=id).one()
	return render_template('blog.html', title=post.title, post=post)

@app.route('/admin')
def admin():
	tags = db.session.query(models.Tag).all()
	posts = db.session.query(models.Post).all()
	return render_template('admin.html', posts=posts, tags=tags)

@app.route('/admin/new_tag', methods=['GET', 'POST'])
def new_tag():
	form = TagForm()
	if form.validate_on_submit():
		flash('Tag with name %r created successfully!' % (form.name.data))
		new_tag = models.Tag(name=form.name.data)
		db.session.add(new_tag)
		db.session.commit()
		return redirect('/admin/new_tag')
	return render_template('new_tag.html', title="New Tag - Admin", form=form)

@app.route('/admin/delete_tag/<name>')
def delete_tag(name):
	tag = db.session.query(models.Tag).filter_by(name=name).one()
	db.session.delete(tag)
	db.session.commit()
	flash('Tag with name %r deleted successfully!' % (name))
	return redirect('/admin')

@app.route('/admin/edit_tag/<name>', methods=['GET', 'POST'])
def edit_tag(name):
	form = TagForm()
	if form.validate_on_submit():
		tag = db.session.query(models.Tag).filter_by(name=name).one()
		tag.name = form.name.data
		db.session.commit()
		flash('Tag with name %r changed to %r successfully!' % (name, form.name.data))
		return redirect('/admin')
	return render_template('new_tag.html', title="Edit Tag - Admin", form=form)

@app.route('/admin/new_post', methods=['GET', 'POST'])
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
	return render_template('new_post.html', title="New Post - Admin", form=form)

@app.route('/admin/edit_post/<id>', methods=['GET', 'POST'])
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
	return render_template('new_post.html', title="Edit Post - Admin", form=form)

@app.route('/admin/delete_post/<id>')
def delete_post(id):
	post = db.session.query(models.Post).filter_by(id=id).one()
	db.session.delete(post)
	db.session.commit()
	flash('Post with title %r deleted' % (post.title))
	return redirect('/admin')

@app.route('/admin/remove_tag/<id>/<name>')
def remove_tag(id, name):
	post = db.session.query(models.Post).filter_by(id=id).one()
	tag = db.session.query(models.Tag).filter_by(name=name).one()
	post.tags = list(set(post.tags) - set([tag]))
	db.session.commit()
	return redirect('/admin')