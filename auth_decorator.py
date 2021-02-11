from flask import session
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        # Você adicionaria uma verificação aqui e usaria o ID do usuário ou algo para buscar
        # os outros dados desse usuário / verifique se existem
        if user:
            return f(*args, **kwargs)
        return 'Você não está logado, nenhuma página para você!'
    return decorated_function
