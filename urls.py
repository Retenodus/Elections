# vim: fileencoding=utf-8 :
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^vote/', include('elections.vote.urls')),
    (r'^admin/', include(admin.site.urls)),

	# Page par défaut
	(r'^$', redirect_to, {'url': '/vote/', 'permanent': True}),
)
