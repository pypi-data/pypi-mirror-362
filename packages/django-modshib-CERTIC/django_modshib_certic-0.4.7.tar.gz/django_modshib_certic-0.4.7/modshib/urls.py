from django.urls import path
from . import views

urlpatterns = [
    path("sso/", views.sso, name="modshib_sso"),
]
