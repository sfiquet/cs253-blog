import webapp2
import cgi

form = """
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(text)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, text=""):
        self.response.out.write(form % {"text": text})
        
    def get(self):
        self.write_form()

    def post(self):
        text = self.request.get("text")
        text = text.encode("rot_13")
        self.write_form(cgi.escape(text, quote=True))

app = webapp2.WSGIApplication([('/unit2/rot13', MainPage)],
                              debug=True)
