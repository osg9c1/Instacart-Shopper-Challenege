from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from applicantAnalysis.adminviews import ApplicantAnalysisView



admin.autodiscover()

urlpatterns = patterns('',

    url(r'^instacart/', include('instacart.applicantAnalysis.urls')),
    url(r'^admin/', include(admin.site.urls)),


   
    
)

urlpatterns += staticfiles_urlpatterns()
