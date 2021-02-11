# AS simeple as possbile flask google oAuth 2.0
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta

# decorador para rotas que devem ser acessíveis apenas por usuários conectados
from auth_decorator import login_required

# dotenv setup
from dotenv import load_dotenv
load_dotenv()


# App config
app = Flask(__name__)
# Session config
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.debug = True

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/')
@login_required
def hello_world():
    email = dict(session)['profile']['email']
    return f'Olá, você está logado como {email}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')  # cria o cliente google oauth
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # cria o cliente google oauth
    token = google.authorize_access_token()  # Token de acesso do google (necessário para obter informações do usuário)
    resp = google.get('userinfo')  # userinfo contém coisas que você especificou no scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # usa endpoint openid para buscar informações do usuário
    # Aqui você usa os dados de perfil/usuário que obteve e consulta seu banco de dados, localizar/registrar o usuário
    # e definir seus próprios dados na sessão, não o perfil do google session['profile'] = user_info
    session.permanent = True  # tornar a sessão permanente para que continue existindo depois que o navegador for fechado
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')
