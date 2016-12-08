from django.conf.urls import url

from . import views

app_name = 'deleteme_bot'

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^auth_thanks/', views.auth_thanks, name='auth_thanks')
]
