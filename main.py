## Logging
import logging as log
#import coloredlogs
import time
import webapp2
import jinja2
import os
from LionHouse_models import Post, User
from content_management import populate_feed, logout_url, login_url
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_current_directory = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

#the handler section
class LoginPageHandler(webapp2.RequestHandler):
    def get(self):
        new_user_template = jinja_current_directory.get_template("templates/new_user.html")
        prev_user_template = jinja_current_directory.get_template("templates/prev_user.html")
        google_login_template = jinja_current_directory.get_template("templates/google_login.html")

        # get Google user
        user = users.get_current_user()

        if user:
            # look for user in datastore
            existing_user = User.query().filter(User.email == user.email()).get()
            nickname = user.nickname()
            if not existing_user:
                # prompt new users to sign up
                fields = {
                  "nickname": nickname,
                  "logout_url": logout_url,
                }
                self.response.write(new_user_template.render(fields))
            else:
                # direct existing user to feed
                self.redirect('/feed')
        else:
            # Ask user to sign in to Google
            self.response.write(google_login_template.render({ "login_url": login_url }))

class FeedHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
        current_user = User.query().filter(User.email == user.email()).get()
        feed_fields = populate_feed(current_user)
        start_feed = jinja_current_directory.get_template("templates/feed.html")
        self.response.write(start_feed.render(feed_fields))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
        current_user = User.query().filter(User.email == user.email()).get()
        if not current_user:
            # upon new user form submission, create new user and store in datastore
            new_user_entry = User(
                name = self.request.get("name"),
                username = self.request.get("username"),
                email = user.email(),
            )
            new_user_entry.put()
            current_user = new_user_entry
        else:
            # if not a new user, existing user submitted a post from feed
            new_post = Post(author= current_user.key, content= self.request.get("user_post"))
            new_post.put()
        time.sleep(.2)
        self.redirect('/feed')


#the app configuration section
app = webapp2.WSGIApplication([
    ('/', LoginPageHandler),
    ('/feed', FeedHandler),
], debug=True)
