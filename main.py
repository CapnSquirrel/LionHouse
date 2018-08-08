import webapp2
import jinja2
import os
from user_info import user_information
from google.appengine.ext import ndb

jinja_current_directory = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

#the handler section
class LoginPageHandler(webapp2.RequestHandler):
    def get(self):
        login_page = jinja_current_directory.get_template(
            "templates/index.html")
        self.response.write(login_page.render())

    def post(self):
        feed_page = jinja_current_directory.get_template(
            "templates/feed.html")
        self.response.write(feed_page.render())

class FeedHandler(webapp2.RequestHandler):
    def get(self):
        feed_page = jinja_current_directory.get_template(
            "templates/feed.html")
        self.response.write(feed_page.render(user_information))

    def post(self):
        feed_page = jinja_current_directory.get_template(
            "templates/feed.html")
        self.response.write(feed_page.render(user_information))

#the app configuration section
app = webapp2.WSGIApplication([
    ('/', LoginPageHandler),
    ('/feed', FeedHandler),
], debug=True)
