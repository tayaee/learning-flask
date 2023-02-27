from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    sql = f'''
select p.id, title, body, created, author_id, username
from post p join user u on p.author_id = u.id
order by created desc
'''
    posts = db.execute(sql).fetchall()
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
            db = get_db()
            sql = f'insert into post (title, body, author_id) values (?, ?, ?)'
            args = (title, body, g.user['id'])
            db.execute(sql, args)
            db.commit()
            return redirect(url_for('blog.index'))

        if error is not None:
            flash(error)
    return render_template('blog/create.html')
