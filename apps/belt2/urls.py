from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^addquote$', views.addquote),
    url(r'^user/(?P<user_id>\d+)$', views.user),
    url(r'^join/(?P<user_id>\d+)$', views.join),
]
