from datetime import datetime
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from validate import FormValidator
from hashutils import check_pw_hash, make_pw_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:garbage@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'VF%^ghyjGRSfs4sdgfhdsgfdshgfdh^FUCK_________shhd6545&^FGS^5$%'

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
        self.pw_hash = make_pw_hash(password)

@app.before_request
def require_login():
    login_required_routes = ['newpost']
    if request.endpoint in login_required_routes and 'user_id' not in session: 
        return redirect('/login')
@app.route('/')
def index():
    authors = User.query.all()
    return render_template('authors.html', authors=authors)

@app.route('/blog')
def blog():
    entries = Post.query.join(User).order_by(Post.date.desc()).all()
    post_id = request.args.get('id')
    author_id = request.args.get('user')
    entry = Post.query.filter_by(entry_id=post_id).first()
    if not post_id:
        if author_id:
            the_author = Post.query.filter_by(author_id=author_id).all()
            return render_template('entries.html', entries=the_author)
        else:
            return render_template('entries.html', entries=entries)
    else:
        return render_template('entry.html', entry=entry)       

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    author = User.query.filter_by(user_id=session['user_id']).first()
    if request.method == 'POST':
        entry_title = request.form['title']
        entry_post = request.form['entry']
        if entry_post == "" or entry_title == "":
            error = 'Please do not leave any fields blank'
            return render_template('new-entry.html', title=entry_title, post=entry_post, error=error)

        new_entry = Post(entry_title, entry_post, None, author)
        db.session.add(new_entry)
        db.session.commit()
        new_post = Post.query.get(new_entry.entry_id)

        return redirect('/blog?id={0}'.format(new_post))
    return render_template('new-entry.html')

@app.route('/signup')
def signup():
        
    form = {"username": ["Username"],
    "email": ["Email Address"],
    "password": ["Password"],
    "verify": ["Verify Password"]}
    return render_template('signup.html', dictionary=form)

@app.route('/signup', methods=['POST'])
def validate():
        
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    verify = request.form['verify']

    username_error = FormValidator.is_bad_username(username)
    email_error = FormValidator.is_invalid_email(email)
    password_error = FormValidator.is_invalid_password(password)
    verif_error = FormValidator.does_not_match(password, verify)
    
    form = {"username": ["Username", username_error],
    "email": ["Email Address", email_error],
    "password": ["Password", password_error],
    "verify": ["Verify Password", verif_error]}

    if username_error == '' and email_error == '' and password_error == '' and verif_error == '':
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if not existing_user and not existing_email:
            new_user = User(email, username, password)
            db.session.add(new_user)
            db.session.flush()   #flush session to get id of inserted row
            db.session.commit()
            session['user_id'] = new_user.user_id
            flash("You have successfully registered")
            return redirect('/blog')
        if existing_user:
            error = "User already exists."
            return render_template('signup.html', dictionary=form, existing_user=error)
        if existing_email:
            error = "Email already in use."
            return render_template('signup.html', dictionary=form, existing_user=error)
    
    else:
        error = []
        for y in form.values():
            error += y[1]
        return render_template("signup.html",
    dictionary=form, username=username, email=email, error=error)


    return render_template('signup.html', dictionary=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['user_id'] = user.user_id
            flash('You have successfully logged in')
            return redirect('/blog')
        else:
            error = 'Username and/or password incorrect; or user does not exist.'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/blog')

@app.route('/delete-post', methods=['POST'])
def delete_post():

    post_id = int(request.form['post-id'])
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/blog')

if __name__ == '__main__':
    app.run()