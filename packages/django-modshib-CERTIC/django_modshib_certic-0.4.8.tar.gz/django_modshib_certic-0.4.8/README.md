# Django mod_shib

Application Django destinée à faciliter la gestion de l'authentification avec mod_shib.
Elle fournit une route (URL) devant être gérée par mod_shib, ainsi que des pages prêtes
à l'emploi pour l'authentification.

Distribué sous [Licence CeCILL-C](LICENSE.txt)

## Avertissement

Pour des raisons de sécurité, ne **jamais** installer cette application en production sans que la configuration du module
Apache `mod_shib` n'ait été correctement réalisée en amont, particulièrement lorsque 
les variables de configuration `MODSHIB_CREATE_ACCOUNT` et `MODSHIB_ACTIVATE_ACCOUNT` 
valent vrai.

## Pré-requis

Cette application Django dépend de l'application `django.contrib.auth`. Il est également attendu que la variable
`LOGIN_REDIRECT_URL` dans votre `settings.py` soit renseignée 
(voir [documentation Django à ce sujet](https://docs.djangoproject.com/fr/4.2/ref/settings/#std-setting-LOGIN_REDIRECT_URL)).

Un serveur Apache avec le module Shibboleth est requis. Voir à ce sujet [la documentation spécifique](https://git.unicaen.fr/certic/kics/-/blob/master/doc/INSTALL_shibboleth.md).

## installation

Installation via pip:

    pip install django-modshib-certic

Ou via poetry:

    poetry add django-modshib-certic

Puis ajouter `modshib.apps.ModshibConfig` dans le `settings.py` de votre projet Django:

    INSTALLED_APPS = [
        [...]
        "modshib.apps.ModshibConfig",
    ]

Ainsi que la configuration des routes dans votre `urls.py`:

    urlpatterns = [
        [...]
        path("modshib/", include("modshib.urls"))
    ]

L'URL pour modshib sera alors à `/modshib/sso`.

Ajoutez également le contexte dans la configuration de vos gabarits :

    TEMPLATES = [
        {
            [...]
            "OPTIONS": {
                "context_processors": [
                    [...]
                    "modshib.context_processors.modshib_context"
                ],
            },
        },
    ]

## Configuration pour `settings.py`

### `MODSHIB_CREATE_ACCOUNT`

Valeur par défaut : `False`

S'il n'existe pas déjà, crée un compte local (modèle `django.contrib.auth.models.User`)
dont le `username` est l'EPPN fournit par `mod_shib`. 
Le compte est créé sans mot de passe et est inactif par défaut.

### `MODSHIB_ACTIVATE_ACCOUNT`

Valeur par défaut : `False`

Active le compte local s'il est trouvé (`User.is_active=True`).

### `MODSHIB_EMAIL_IS_IDENTIFIER`

Valeur par défaut : `False`

L'email renvoyé par l'IDP est utilisé en remplacement de l'EPPN dans toutes les requêtes impliquant le `username` du
modèle `django.contrib.auth.models.User`, ce qui inclut le login est la création de compte.

### `MODSHIB_FORMS_TITLE`

Valeur par défaut: `Authentification`

Titre utilisé dans les formulaires de connexion/déconnexion.

### `MODSHIB_STYLESHEET_URL`

Valeur par défaut: `None`

URL utilisée pour ajouter des styles CSS aux pages d'authentification

### `MODSHIB_SHOW_SSO_LOGIN`

Valeur par défaut: `True`

Afficher ou non le formulaire de connexion via SSO

### `MODSHIB_SHOW_LOCAL_LOGIN`

Valeur par défaut: `True`

Afficher ou non le formulaire de connexion locale

### `MODSHIB_SSO_SUBMIT_LABEL`

Valeur par défaut: `Connexion via SSO`

Texte du bouton de connexion via SSO

### `MODSHIB_LOCAL_SUBMIT_LABEL`

Valeur par défaut: `Connexion avec mot de passe`

Texte du bouton de connexion locale

### `APP_URL_BASE_PATH`

Valeur par défaut: `/`

Préfixe utilisé pour déployer l'application

## Utilisation

Une fois installé, `modshib ` fournit des templates par défaut qui sont appelés selon le contexte (login, logout, échec de connexion sso, etc.).

Si vous voulez intégrer ou surcharger ces templates, vous devrez créer un répertoire `templates/registration` et les fichiers que vous souhaitez remplacer.

Exemple d'intégration du bloc de connexion pour la page de login (fichier `templates/registration/login.html`)`:
```html
{% extends "base.html" %}
{% block content %}
  <div class="d-flex justify-content-center align-items-center p-5">
    {% include "registration/_block_connection.html" %}
  </div>
{% endblock content %}
```