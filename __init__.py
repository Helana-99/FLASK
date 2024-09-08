from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_restful import Api
from app.config import config_options

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap5()
api = Api()

def create_app(config_name='prd'):
    app = Flask(__name__)
    current_config = config_options[config_name]
    app.config.from_object(current_config)
    app.config['SQLALCHEMY_DATABASE_URI'] = current_config.SQLALCHEMY_DATABASE_URI

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    api.init_app(app)

    # Import blueprints after routes are defined
    from app.posts import posts_blueprint
    from app.users import users_blueprint

    app.register_blueprint(posts_blueprint, url_prefix='/posts')
    app.register_blueprint(users_blueprint, url_prefix='/users')

    # Register API resources after blueprints
    from app.posts.api.views import PostList
    api.add_resource(PostList, '/api/posts')

    return app
