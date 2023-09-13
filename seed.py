"""Seed file to make sample data for users db."""

from models import User, db, Post, Tag, TagPost
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it 
User.query.delete()

# Add user
hunter = User(first_name="hunter",last_name="powell",
               image_url="https://pyxis.nymag.com/v1/imgs/57e/935/9be1deb435f6dac97089c43309bf9d99d3-12-white-guys.rhorizontal.w700.jpg")

# Add new objects to session, so they'll persist
db.session.add(hunter)

# Commit--otherwise, this never gets saved!
db.session.commit()

# Add post
user_post = Post(title="First Post",content="This is the first post.",user_id=1)
db.session.add(user_post)
db.session.commit()

# Add tag
tag = Tag(tag_name="DemoTag")
db.session.add(tag)
db.session.commit()

# Connect the tag to post
tag_post = TagPost(post_id=1,tag_id=1)
db.session.add(tag_post)
db.session.commit()