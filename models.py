from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash

db = SQLAlchemy(app)

class Post(db.Model):

    entry_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.Text)
    date = db.Column(db.DateTime)
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, title, entry, date, author):
        self.title = title
        self.entry = entry
        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.author = author

    def __repr__(self):
        return str(self.entry_id)
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    pw_hash = db.Column(db.String(100), nullable=False)
    blogs = db.relationship('Post', backref='author')

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.pw_hash = password
