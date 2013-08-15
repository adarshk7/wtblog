from app import db

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    body = db.Column(db.String(500), index=True)
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return '<Post %r %r>' % (self.title, self.tags)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)

    def __repr__(self):
    	return '<Tag %r>' % (self.name)