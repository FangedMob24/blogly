"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it 
User.query.delete()

# Add pets
hunter = User(first_name="hunter",last_name="powell",
               image_url="https://pyxis.nymag.com/v1/imgs/57e/935/9be1deb435f6dac97089c43309bf9d99d3-12-white-guys.rhorizontal.w700.jpg")

# Add new objects to session, so they'll persist
db.session.add(hunter)

# Commit--otherwise, this never gets saved!
db.session.commit()