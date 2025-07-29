import string
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.models import Group
import ftfy

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

User = get_user_model()
logger = logging.getLogger(__name__)

try:
    CREATE_ACCOUNT = bool(settings.MODSHIB_CREATE_ACCOUNT)
except AttributeError:
    CREATE_ACCOUNT = False

try:
    ACTIVATE_ACCOUNT = bool(settings.MODSHIB_ACTIVATE_ACCOUNT)
except AttributeError:
    ACTIVATE_ACCOUNT = False

try:
    EMAIL_IS_IDENTIFIER = bool(settings.MODSHIB_EMAIL_IS_IDENTIFIER)
except AttributeError:
    EMAIL_IS_IDENTIFIER = False

context = {"login_url": settings.LOGIN_URL}


def _updateUser(user: User, mail: string, first_name: string, last_name: string):
    if mail:
        user.email = mail
    if last_name:
        user.last_name = ftfy.fix_text(last_name)
    if first_name:
        user.first_name = ftfy.fix_text(first_name)
    user.save()


def sso(request: HttpRequest) -> HttpResponse:
    redirection = request.GET.get("next", settings.LOGIN_REDIRECT_URL)
    # nothing to do here...
    if request.user.is_authenticated:
        logger.info(f"User already authenticated, redirecting to {redirection}")
        return HttpResponseRedirect(redirection)
    # logger.warning(request.META)
    # fetch EPPN from headers, injected by mod_shib
    eppn = request.META.get("HTTP_EPPN", None)
    supann_etablissement = request.META.get("HTTP_SUPANNETABLISSEMENT", None)
    display_name = request.META.get("HTTP_DISPLAYNAME", None)
    mail = request.META.get("HTTP_MAIL", None)
    last_name = request.META.get("HTTP_SN", None)
    if last_name is not None:
        last_name = last_name.split(";")[-1]
    first_name = request.META.get("HTTP_GIVENNAME", None)
    if (EMAIL_IS_IDENTIFIER and not mail) or not eppn:
        return render(request, "registration/sso_lack_of_attributes.html", context)
    if last_name == '' and first_name == '' and display_name is not None:
        if ' ' in display_name:
            first_name, last_name = display_name.split(" ", 1)
        else:
            last_name = display_name

    # find account
    user_name = eppn.strip()
    if EMAIL_IS_IDENTIFIER:
        user_name = mail.strip()
    user = User.objects.filter(username=user_name).first()
    if not user and CREATE_ACCOUNT:
        logger.info(f"user {user_name} not found, creating account")
        user = User.objects.create_user(user_name)
        user.is_active = False
        _updateUser(user, mail, first_name, last_name)
        if supann_etablissement:
            group, created = Group.objects.get_or_create(
                name=f"supann_{supann_etablissement}"
            )
            user.groups.add(group)
    if not user:
        logger.info(f"user {user_name} not found, rejecting auth")
        return render(request, "registration/sso_no_account.html", context)
    if user and user.has_usable_password():
        logger.info(f"user {user_name} has a local password defined, rejecting auth")
        return render(request, "registration/sso_no_account.html", context)
    if not user.is_active and ACTIVATE_ACCOUNT:
        logger.info(f"user {user_name} not active, activating")
        user.is_active = True
    if not user.is_active:
        logger.info(f"user {user_name} inactive, rejecting auth")
        return render(request, "registration/sso_no_account.html", context)
    if user and user.is_active:
        logger.info(f"active user {user_name} found, login")
        request.session["auth_is_from_modshib"] = True
        _updateUser(user, mail, first_name, last_name)
        login(request, user)
        return HttpResponseRedirect(redirection)
    ## return default page but should not be used
    return render(request, "registration/sso_fail.html", context)