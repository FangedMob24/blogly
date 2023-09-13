from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User account"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50))
    image_url = db.Column(db.String(500),
                          nullable=False,
                          unique=False)
    
    post = db.relationship('Post', backref='users')
    
class Post(db.Model):
    """Post from users"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False)
    content = db.Column(db.String(500),
                        nullable=False)
    user_id = db.Column(db.Integer,
                          db.ForeignKey('users.id'))
    
    poststags = db.relationship('TagPost', backref='posts')
    
    tags = db.relationship("Tag",
                           secondary="tags_posts",
                           backref="posts")
    
class TagPost(db.Model):
    "stores which tags go with which post"

    __tablename__ = "tags_posts"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey("tags.id"),
                        primary_key=True)

    
class Tag(db.Model):
    """Tags for post"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    tag_name = db.Column(db.Text,
                         nullable=False,
                         unique=True)
    
    tagsposts = db.relationship('TagPost', backref='tags')