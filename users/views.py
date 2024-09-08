from flask import render_template, request, redirect, url_for
from app.models import db, User
from app.users import users_blueprint

@users_blueprint.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template("users/index.html", users=users)

@users_blueprint.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            email=request.form['email'],
            password_hash=request.form['password']
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.index'))
    return render_template("users/create.html")

@users_blueprint.route('/<int:id>', methods=['GET'])
def show(id):
    user = User.query.get_or_404(id)
    return render_template("users/show.html", user=user)

@users_blueprint.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.index'))

@users_blueprint.route('/list', methods=['GET'])
def list_users():
    users = User.query.all()
    return render_template('users/list.html', users=users)
