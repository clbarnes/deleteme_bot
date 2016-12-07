from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^auth_thanks$', views.auth_thanks, name='deleteme_bot:auth_thanks'),
    url(r'^landing', views.landing, name='deleteme_bot:landing')
]
