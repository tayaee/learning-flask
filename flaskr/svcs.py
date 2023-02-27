from flask import abort
from flask import g

from flaskr.db import get_db


def svc_get_all_posts():
    db = get_db()
    sql = f'''
select p.id, title, body, created, author_id, username
from post p join user u on p.author_id = u.id
order by created desc
'''
    rows = db.execute(sql).fetchall()
    posts = [{k: item[k] for k in item.keys()} for item in rows]
    return posts


def svc_get_post(id, check_author=True):
    sql = f'''
select p.id, title, body, created, author_id, username
 from post p join user u on p.author_id = u.id
 where p.id = ?
'''
    args = (id,)
    row = get_db().execute(sql, args).fetchone()
    post = {k: row[k] for k in row.keys()}

    if post is None:
        abort(404, f'Post id {id} does not exist.')
    if check_author:
        post_author_id = post['author_id']
        g_user_id = g.user['id']
        if post_author_id != g_user_id:
            abort(403)
    return post


def svc_create_post(body, title):
    db = get_db()
    sql = f'insert into post (title, body, author_id) values (?, ?, ?)'
    args = (title, body, g.user['id'])
    db.execute(sql, args)
    db.commit()


def svc_update_post(body, id, title):
    db = get_db()
    sql = f'update post set title = ?, body = ? where id = ?'
    args = (title, body, id)
    db.execute(sql, args)
    db.commit()
