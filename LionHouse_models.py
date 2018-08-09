from google.appengine.ext import ndb

class Post(ndb.Model):
    author = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    posts = ndb.KeyProperty(Post, repeated=True)
