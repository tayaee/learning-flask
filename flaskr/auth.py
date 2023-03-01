import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            db = get_db()
            try:
                sql = 'insert into user (username, password) values (?, ?)'
                args = (username, generate_password_hash(password))
                db.execute(sql, args)
                db.commit()
                return redirect(url_for('auth.login'))
            except db.IntegrityError:
                error = f'User {username} is already registered.'
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            db = get_db()
            sql = 'select * from user where username = ?'
            args = (username,)
            row = db.execute(sql, args).fetchone()
            if row:
                user = {k: row[k] for k in row.keys()}
                if check_password_hash(user['password'], password):
                    session.clear()
                    session['user_id'] = user['id']
                    return redirect(url_for('index'))
                else:
                    error = 'Incorrect password.'
            else:
                error = 'Incorrect username.'
        flash(error)
    return render_template('auth/login.html')


# 모든 view 에 대해 호출
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        sql = 'select * from user where id = ?'
        args = (user_id,)
        row = get_db().execute(sql, args).fetchone()
        g.user = {k: row[k] for k in row.keys()}


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 다른 url에 대해 사용할 decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
