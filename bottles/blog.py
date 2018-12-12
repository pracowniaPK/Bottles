from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from bottles.db import get_db
from bottles.auth import login_required


bp = Blueprint('blog', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
def root():

    db = get_db()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        # TODO sprawdzić czy nie puste
        db.execute(
            'INSERT INTO post \
            (author_id, title, body) VALUES (?, ?, ?)',
            (g.user['id'], title, body)
        )
        db.commit()

    posts = db.execute(
        'SELECT * FROM post \
        INNER JOIN subscription ON post.author_id = subscription.target_id \
        INNER JOIN user ON post.author_id = user.id \
        WHERE subscriber_id = ?', 
        (g.user['id'], )
    ).fetchall()

    print(posts)

    return render_template('blog/blog.html', posts=posts)

@bp.route('/new')
def new():

    return render_template('blog/new.html')

# TODO moje posty + usuwanie
# if check_author and post['author_id'] != g.user['id']:
#         abort(403)

@bp.route('/users', methods=['GET', 'POST'])
def users():

    db = get_db()

    if request.method == 'POST':

        sub = db.execute(
            'SELECT * FROM subscription \
            WHERE subscriber_id = ? AND target_id = ?',
            (g.user['id'], request.form['sub'])
        ).fetchone()

        if sub is None:
            db.execute(
                'INSERT INTO subscription \
                (subscriber_id, target_id) VALUES (?, ?)',
                (g.user['id'], request.form['sub'])
            )
            db.commit()
        else:
            db.execute(
                'DELETE FROM subscription \
                WHERE id = ?',
                (sub['id'], )
            )
            db.commit()

    users = db.execute(
        'SELECT id, nick FROM user \
        WHERE id != ?',
        (g.user['id'], ),
    ).fetchall()
    
    subs = get_users_subs(g.user['id'])

    users_dict = {}
    for u in users:
        users_dict[u[0]] = {
            'id': u[0],
            'subscribed': u[0] in subs,
            'nick': u[1],
        }

    return render_template('blog/users.html', users=users_dict)

def get_users_subs(user_id):
    subs = get_db().execute(
        'SELECT target_id FROM subscription \
        WHERE subscriber_id = ?',
        (user_id, ),
    ).fetchall()
    return [s['target_id'] for s in subs]
