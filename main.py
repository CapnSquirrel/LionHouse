import webapp2
import jinja2
import os
from welcome_display import previous_user, new_user, google_login
from LionHouse_models import Post, User
from google.appengine.ext import ndb
from google.appengine.api import users


jinja_current_directory = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)
logout_url = users.create_logout_url('/')
login_url = users.create_login_url('/')

#the handler section
class LoginPageHandler(webapp2.RequestHandler):
    def get(self):
        welcome_page = jinja_current_directory.get_template(
            "templates/welcome.html")
        user = users.get_current_user()

        if user:
            existing_user = User.query().filter(
            User.email == user.email()).get()
            nickname = user.nickname()
            if not existing_user:
                display = new_user.format(nickname, login_url)
            else:
                display = previous_user.format(
                existing_user.name, logout_url)
                self.redirect('/feed')
            self.response.write(display)
        else:
            display = google_login.format(login_url)
            self.response.write(display)

    def post(self):
        user = users.get_current_user()
        feed_page = jinja_current_directory.get_template(
            "templates/feed.html")
        new_user_entry = User(
            name= self.request.get("name"),
            email= user.email(),
            posts=[]
        )
        new_user_entry.put()
        self.response.write(feed_page.render())

class FeedHandler(webapp2.RequestHandler):
    def get(self):
        feed_page = jinja_current_directory.get_template(
            "templates/feed.html")
        self.response.write(feed_page.render({"sign_out":logout_url}))

    def post(self):
        feed_page = jinja_current_directory.get_template(
            "templates/feed.html")
        self.response.write(feed_page.render())

#the app configuration section
app = webapp2.WSGIApplication([
    ('/', LoginPageHandler),
    ('/feed', FeedHandler),
], debug=True)
