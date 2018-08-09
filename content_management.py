from google.appengine.api import users

logout_url = users.create_logout_url('/')
login_url = users.create_login_url('/')

def populate_feed(current_user):
    feed_fields = {
        "sign_out": logout_url,
        "username": current_user.username,
        "user_name": current_user.name,
        "post_count": len(current_user.posts)
    }
    return feed_fields
