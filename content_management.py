from google.appengine.api import users
from google.appengine.ext import ndb
from LionHouse_models import Post, User

logout_url = users.create_logout_url('/')
login_url = users.create_login_url('/')

def populate_feed(current_user):
    feed_fields = {
        "sign_out": logout_url,
        "username": current_user.username,
        "user_name": current_user.name,
        "post_count": len(Post.query().filter(Post.author == current_user.key).fetch()),
        "user_count": len(User.query().fetch()),
        "test_post": Post.query().order(-Post.time).fetch()
    }
    return feed_fields
