from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_restful import Resource
from app.posts import posts_blueprint
from app.models import Post, User, db
import os
from app.posts.forms import PostForm

def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)

@posts_blueprint.route('/create', endpoint='create', methods=['GET', 'POST'])
def create():
    users = User.query.all()
    if request.method == 'POST':
        name = request.form.get("name")
        description = request.form.get("description")
        image = request.files.get("image")
        user_id = request.form.get("user")

        if not name or not description or not user_id:
            return "Name, description, and user are required fields.", 400

        image_name = None
        if image and image.filename:
            image_name = secure_filename(image.filename)
            image.save(os.path.join('static/posts/', image_name))

        post = Post(
            name=name,
            description=description,
            image=image_name,
            user_id=user_id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.show', id=post.id))
    return render_template('posts/create.html', users=users)

@posts_blueprint.route('/<int:id>', endpoint='show')
def show(id):
    post = db.get_or_404(Post, id)
    user = db.get_or_404(User, post.user_id)
    return render_template("posts/show.html", post=post, user=user)

@posts_blueprint.route('/<int:id>/delete', endpoint='delete', methods=['POST'])
def delete(id):
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.index'))

@posts_blueprint.route('/<int:id>/edit', endpoint='edit', methods=['GET', 'POST'])
def edit(id):
    post = db.get_or_404(Post, id)
    if request.method == 'POST':
        post.name = request.form["name"]
        post.description = request.form["description"]

        if 'image' in request.files:
            image = request.files["image"]
            image_name = secure_filename(image.filename)
            image.save(os.path.join('static/posts/', image_name))
            post.image = image_name

        db.session.commit()
        return redirect(url_for('posts.show', id=post.id))
    return render_template('posts/edit.html', post=post)

@posts_blueprint.route('/form/create', endpoint='form_create', methods=['POST', 'GET'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        image_name = None
        if form.image.data:
            image = form.image.data
            image_name = secure_filename(image.filename)
            image.save(os.path.join('static/posts/', image_name))

        data = form.data
        data.pop('csrf_token', None)
        data.pop('submit', None)

        data["image"] = image_name

        post = Post(**data)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.show', id=post.id))
    return render_template('posts/forms/create.html', form=form)

class PostList(Resource):
    def get(self):
        posts = Post.query.all()
        return [{'id': post.id, 'name': post.name, 'description': post.description} for post in posts]