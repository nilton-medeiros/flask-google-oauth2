from flask import session
from functools import wraps

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# https://firebase.google.com/docs/firestore/quickstart?hl=pt-br
cred = credentials.Certificate("config/key.json")
firebase_admin.initialize_app(cred)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        # Você adicionaria uma verificação aqui e usaria o ID do usuário ou algo para buscar
        # os outros dados desse usuário / verifique se existem
        print("User: --------------------------------------------------------------")
        print(user)  # Por algum motivo user está None
        print(type(user))
        print("Profile: -----------------------------------------------------------")
        profile = dict(session)['profile']['email']
        print(type(profile))
        if user:
            db = firestore.Client()
            if not db:
                return 'Falha na conexão com banco de dados!'
            users_ref = db.collection(u'users')
            # Cadastra usuário que acessa pela primeira vez no Firestore
            if not users_ref.where(u'user_gmail', u'==', profile['email']):
                db.collection(u'users').add({
                    u'user_name': profile['name'],
                    u'user_gmail': profile['email'],
                    u'user_photo': profile['picture']
                })
            return f(*args, **kwargs)
        return 'Você não está logado, nenhuma página para você!'
    return decorated_function
