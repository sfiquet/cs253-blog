import webapp2

class MainPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('Hello, Udacity!')

app = webapp2.WSGIApplication([('/unit1/hello', MainPage)],
                              debug=True)
