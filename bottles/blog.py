from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from bottles.db import get_db_session
from bottles.auth import login_required
from bottles.models import Post, Subscription, User


bp = Blueprint('blog', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def root():

    s = get_db_session()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title required'
        elif not body:
            error = 'Post has no content'
        
        if error is None:
            s.add(Post(author_id=g.user.id, title=title, body=body))
            s.commit()
            flash('Post added successfully')
        else:
            flash(error)

    posts = (
        s.query(Post, User)
        .join(Subscription, Post.author_id == Subscription.target_id)
        .join(User, Post.author_id == User.id)
        .filter(Subscription.subscriber_id == g.user.id)
        .all()
    )

    return render_template('blog/blog.html', posts=posts)

@bp.route('/new')
@login_required
def new():

    return render_template('blog/new.html')

# TODO moje posty + usuwanie
# if check_author and post['author_id'] != g.user['id']:
#         abort(403)

@bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():

    s = get_db_session()

    if request.method == 'POST':

        sub = (
            s.query(Subscription)
            .filter(Subscription.subscriber_id == g.user.id)
            .filter(Subscription.target_id == request.form['sub'])
        )

        if sub.first():
            sub.delete()
            s.commit()
        else:
            print('create')
            s.add(
                Subscription(subscriber_id=g.user.id, target_id=request.form['sub'])
            )
            s.commit()

    users = (
        s.query(User)
        .filter(User.id != g.user.id)
        .all()
    )
    
    subs = get_users_subs(g.user.id)

    users_dict = {}
    for u in users:
        users_dict[u.id] = {
            'id': u.id,
            'subscribed': u.id in subs,
            'nick': u.nick,
        }
    print(subs)
    print(users_dict)

    return render_template('blog/users.html', users=users_dict)

def get_users_subs(user_id):
    s = get_db_session()
    subs = (
        s.query(Subscription.target_id)
        .filter(Subscription.subscriber_id == user_id)
    )
    return [s.target_id for s in subs]
