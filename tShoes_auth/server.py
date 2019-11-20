# /server.py

# Flask dependencies
from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

# Auth0 Libraries
from authlib.integrations.flask_client import OAuth

# Psycop2
import psycopg2

# Authtoken
from connection import Authtoken

# Utilities
from functools import wraps
import json
from urllib.parse import urlencode
import os

#-----------------------------
# Constants
#-----------------------------
API_BASE_URL=os.environ.get("API_BASE_URL")
ACCESS_TOKEN_URL=os.environ.get("ACCESS_TOKEN_URL")
AUTHORIZE_URL=os.environ.get("AUTHORIZE_URL")
CLIENT_SECRET=os.environ.get("CLIENT_SECRET")
CLIENT_ID=os.environ.get("CLIENT_ID")
REDIRECT_URI=os.environ.get("REDIRECT_URI")

app = Flask(__name__)
app.secret_key = CLIENT_SECRET
oauth = OAuth(app)
token_conn = Authtoken()

auth0 = oauth.register(
    'auth0',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    api_base_url=API_BASE_URL,
    access_token_url=ACCESS_TOKEN_URL,
    authorize_url=AUTHORIZE_URL,
    client_kwargs={
        'scope': 'openid profile email',
    },)

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    algo = auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'email': userinfo['email'],
        'picture': userinfo['picture'],
        'access_token': algo['access_token']
    }

    # Email and access_token from session
    email = session['profile']['email']
    access_token = session['profile']['access_token']

    try:
        # Retrieves user's id form email
        id = token_conn.fetch_user_by_email(email)
        session['profile']['id'] = id
        # Creates token authenticator in tShoes-db
        token_conn.insert_authtoken(user_id=id, token=access_token)
    except (Exception, psycopg2.Error) as error:
        print ("Error while fetching data from PostgreSQL", error)
    return redirect('/dashboard')

@app.route('/login/')
def login():
    """ Login processing """
    return auth0.authorize_redirect(redirect_uri=REDIRECT_URI)

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

@app.route('/dashboard/')
@requires_auth
def dashboard():
    """ Dash board with client  """
    return render_template('dashboard.html',
                           userinfo=json.dumps(session['profile']),
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

@app.route('/logout/')
def logout():
    """ Log out processing """
    id = session.get('profile').get('id')
    token_conn.delete_authtoken(id)
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/')
def home():
    """ Home template """
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)