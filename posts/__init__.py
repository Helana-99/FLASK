from flask import Blueprint

posts_blueprint = Blueprint('posts', __name__)

from app.posts import views
