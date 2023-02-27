from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.svcs import svc_create_post
from flaskr.svcs import svc_get_all_posts
from flaskr.svcs import svc_get_post
from flaskr.svcs import svc_update_post

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = svc_get_all_posts()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None
        if not title:
            error = 'Title is required.'

        if error is None:
            svc_create_post(body, title)
            return redirect(url_for('blog.index'))

        if error is not None:
            flash(error)
    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = svc_get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None
        if not title:
            error = 'Title is required.'

        if error is None:
            svc_update_post(body, id, title)
            return redirect(url_for('blog.index'))

        if error is not None:
            flash(error)
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST', ))
@login_required
def delete(id):
    post = svc_get_post(id)
    if post is not None:
        db = get_db()
        sql = 'delete from post where id = ?'
        args = (id,)
        db.execute(sql, args)
        db.commit()
    return redirect(url_for('blog.index'))
