from flask_sqlalchemy import SQLAlchemy
from flask import url_for

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def image_url(self):
        if self.image:
            return url_for('static', filename=f"posts/{self.image}")
        return None

    @property
    def show_url(self):
        return url_for('posts.show', id=self.id)

    @property
    def delete_url(self):
        return url_for('posts.delete', id=self.id)

    @property
    def edit_url(self):
        return url_for('posts.edit', id=self.id)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    @property
    def show_url(self):
        return url_for('users.show', id=self.id)
