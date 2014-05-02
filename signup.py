import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    if not email: # email is optional
        return True
    return EMAIL_RE.match(email)

def valid_verify(password, verify):
    return password == verify

form = """
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(err_username)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(err_password)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(err_verify)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(err_email)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, username="", email="",
                   err_username="", err_password="", err_verify="", err_email="" ):
        self.response.out.write(form % {"username": cgi.escape(username, quote=True),
                                        "email": cgi.escape(email, quote=True),
                                        "err_username": err_username,
                                        "err_password": err_password,
                                        "err_verify": err_verify,
                                        "err_email": err_email})
        
    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get("username")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")

        username = valid_username(user_username)
        password = valid_password(user_password)
        verify = valid_verify(user_password, user_verify)
        email = valid_email(user_email)
        if username and password and verify and email:
            # everything valid: redirect to welcome page
            self.redirect("/unit2/signup/welcome?username=%s" % cgi.escape(user_username, quote=True))
        else:
            # something is invalid: reload the page with error messages
            err_username = ''
            err_password = ''
            err_verify = ''
            err_email = ''
            if not username:
                err_username = "That's not a valid username."
            if not password:
                err_password = "That wasn't a valid password."
            elif not verify:
                err_verify = "Your passwords didn't match."
            if not email:
                err_email = "That's not a valid email."
            self.write_form(user_username,
                            user_email,
                            err_username,
                            err_password,
                            err_verify,
                            err_email)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("Welcome, %s!" %username)
    
app = webapp2.WSGIApplication([('/unit2/signup', MainPage),
                               ('/unit2/signup/welcome', WelcomeHandler)],
                              debug=True)
