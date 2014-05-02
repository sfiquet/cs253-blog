import webapp2

page = """
<!DOCTYPE html>

<html>
  <head>
    <title>CS253 Assignments</title>
  </head>

  <body>
    <h1>CS253 Assignments</h1>
    <h2>Unit 1</h2>
    <a href="/unit1/hello">Hello Udacity</a><br>
    <h2>Unit 2</h2>
    <a href="/unit2/rot13">ROT-13</a><br>
    <a href="/unit2/signup">Sign-up</a><br>
    <h2>Unit 3</h2>
    <a href="/unit3/basicblog">Basic Blog</a><br>
    <h2>Unit 4</h2>
    <h2>Unit 5</h2>
    <h2>Unit 6</h2>
    <h2>Unit 7</h2>
  </body>

</html>
"""

class MainPage(webapp2.RequestHandler):
  def get(self):
      #self.response.headers['Content-Type'] = 'text/plain'
      self.response.write(page)

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
