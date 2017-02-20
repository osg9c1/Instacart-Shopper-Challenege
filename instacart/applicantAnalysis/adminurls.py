__author__ = 'sujata'
from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin



urlpatterns = patterns('',
    # Examples:

   url(r'^admin/', admin.site.urls),



)

urlpatterns += staticfiles_urlpatterns()