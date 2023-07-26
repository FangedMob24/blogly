from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "HellWorld"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def redirect_users():
    """Redirects to the list of users"""
    return redirect('/users')

# users
@app.route('/users')
def list_users():
    """Shows the user accounts"""
    users = User.query.all()
    return render_template('user_list.html', users=users)

#/user/new
@app.route('/users/new')
def user_form():
    return render_template('user_new.html')

#/users/new, methods=["POST"]
@app.route('/users/new', methods=["POST"])
def create_user():
    """Create a user account"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users")

#/users/[user-id]
@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)

#/users/[user-id]/edit
@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    return render_template("user_edit.html", user_id=user_id)

#/users/[user-id]/edit, methods=["POST"]
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Create a user account"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users")

#/users/[user-id]/delete, methods=["POST"]
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    return redirect("/users")