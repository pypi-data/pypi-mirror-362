from django.conf import settings

_default_conf = {
    "MODSHIB_FORMS_TITLE": "Authentification",
    "MODSHIB_STYLESHEET_URL": None,
    "MODSHIB_SHOW_SSO_LOGIN": True,
    "MODSHIB_SHOW_LOCAL_LOGIN": True,
    "MODSHIB_SSO_SUBMIT_LABEL": "Connexion via SSO",
    "MODSHIB_LOCAL_SUBMIT_LABEL": "Connexion avec mot de passe",
    "APP_URL_BASE_PATH": "/",
}

for k in _default_conf.keys():
    try:
        val = getattr(settings, k)
        _default_conf[k] = val
    except AttributeError:
        continue


def modshib_context(request):
    return _default_conf
