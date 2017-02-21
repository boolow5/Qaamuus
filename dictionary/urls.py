from django.conf.urls import include, url
from . import views

urlpatterns = [
               url(r'^$', views.index, name='index'),
               url(r'^all/$', views.list, name='list'),
               url(r'^word/(?P<word_url>[A-Za-z0-9_\-]+)/$', views.detail, name='detail'),
               url(r'^login/$', views.login, name="login"),
               url(r'^register/$', views.register, name="register"),
               url(r'^signup/$', views.signup, name="signup"),
               url(r'^logout/$', views.logout, name="logout"),
               url(r'^new/word/$', views.add_word, name="add_word"),
               url(r'^new/comment/$', views.add_comment, name="add_comment"),
               url(r'^react/$', views.add_reaction, name="add_reaction"),
]
