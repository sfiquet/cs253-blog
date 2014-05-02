import os
import webapp2
import cgi
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

# Database model for blogposts
class BlogPost(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

# Utility handler class
# handles the rendering though Jinja
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# Handler for main page
# shows the last 10 entries
class MainPage(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 10")
        self.render("basicblog.html", blogposts=posts)

# Handler for New Post entry page
# Makes sure both subject and content are filled in before adding to DB
class NewPostHandler(Handler):
    def write_form(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)
    
    def get(self):
        self.write_form()
    
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            # store in database
            blog = BlogPost(subject = subject, content = content)
            blog.put()
            # redirect to new page
            self.redirect("/unit3/basicblog/%s" % blog.key().id())
        else:
            error = "Subject and content, please!"
            self.write_form(subject, content, error)

# Handler for single entry page identified by its database ID
# e.g. /unit3/basicblog/2343654235
class EntryHandler(Handler):
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        self.render("basicblog.html", blogposts=[post])

app = webapp2.WSGIApplication([(r'/unit3/basicblog', MainPage),
                               (r'/unit3/basicblog/newpost', NewPostHandler),
                               (r'/unit3/basicblog/(\d+)', EntryHandler)],
                              debug=True)
