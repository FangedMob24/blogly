from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, TagPost

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

#
#
# USERS SECTION
#
#

# /users
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

    return redirect("/users")

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

    return redirect("/users")

#/users/[user-id]/delete, methods=["POST"]
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    return redirect("/users")

#
#
#POSTS SECTION
#
#

#/users/[user-id]/posts/new
@app.route('/users/<int:user_id>/posts/new')
def post_form(user_id):
    """Write out post info"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post_new.html',user=user,tags=tags)

#/user/[user-id]/posts/new, methods=["POST"]
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Create post"""
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    tags = request.form.getlist('tags')
    for tag in tags:
        new_tag = TagPost(post_id = new_post.id, tag_id = tag)
        db.session.add(new_tag)
        db.session.commit()

    return redirect(f"/users/{user_id}")

#/posts/[post-id]
@app.route('/posts/<int:post_id>')
def post_info(post_id):
    """Show the full post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',post=post)

#/posts/[post-id]/edit
@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    """Edit existing post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('post_edit.html', post=post, tags=tags)

#/posts/[post-id]/edit, methods=["POST"]
@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_change(post_id):
    """Edit existing post confirmation"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]

    tags = request.form.getlist('tags')
    post.tags = Tag.query.filter(Tag.id.in_(tags)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

#/posts/[post-id]/delete
@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.users.id

    Post.query.filter_by(id = post_id).delete()
    db.session.commit()
    return redirect(f"/users/{user}")

#
#
# TAGS SECTION
#
#

#/tags
@app.route('/tags')
def list_tags():
    """Full list of tags"""
    tags = Tag.query.all()
    return render_template('tag.html', tags=tags)

#/tags/[tag-id]
@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """details about the tag like the posts it is linked to"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)

#/tags/new
@app.route('/tags/new')
def tag_form():
    """New tag form"""
    return render_template('tag_new.html')

#/tags/new, methods=["POST"]
@app.route('/tags/new', methods=["POST"])
def new_tag():
    """Create a new tag"""
    tag_name = request.form["tag"]

    new_tag = Tag(tag_name=tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

#/tags/[tag-id]/edit
@app.route('/tags/<int:tag_id>/edit')
def tag_edit_form(tag_id):
    """Edit tag form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_edit.html', tag=tag)

#/tags/[tag-id]/edit, methods=["POST"]
@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edited_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    tag.tag_name = request.form["tag"]

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

#/tags/[tag-id]/delete
@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")