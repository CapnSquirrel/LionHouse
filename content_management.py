from google.appengine.api import users
from google.appengine.ext import ndb
from LionHouse_models import Post, User
from datetime import datetime

logout_url = users.create_logout_url('/')
login_url = users.create_login_url('/')
class PPost():
    def __init__(self, author, content, time):
        self.author = author
        self.content = content
        self.time = time

def format_posts(posts):
    formatted_posts = []
    for post in posts:
        author = User.query().filter(User.key == post.author).get().username
        formatted_posts.append(PPost(author, post.content, post.time))
    return formatted_posts

def populate_feed(current_user):
    feed_fields = {
        "sign_out": logout_url,
        "username": current_user.username,
        "user_name": current_user.name,
        "post_count": len(Post.query().filter(Post.author == current_user.key).fetch()),
        "user_count": len(User.query().fetch()),
        "posts": format_posts(Post.query().order(-Post.time).fetch(limit=20)),
        "users": User.query().order(User.username).fetch(),
    }
    return feed_fields
