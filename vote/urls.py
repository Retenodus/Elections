# vim: fileencoding=utf-8 :

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
	url(r'^$', direct_to_template, {'template' : 'vote/index.html'}, name="vote-index"),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'vote/login.html'}, name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
	url(r'^bulletin/$', 'elections.vote.views.bulletin', name="vote-bulletin"),
	url(r'^bulletin/done/$', direct_to_template, {'template': 'vote/vote.html'}, name="vote-avote"),
	url(r'^bulletin/dejavote/$', direct_to_template, {'template': 'vote/dejavote.html'}, name="vote-dejavote"),
)
