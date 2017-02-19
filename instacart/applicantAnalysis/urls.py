__author__ = 'sujata'
from django.conf.urls.defaults import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from adminviews import ApplicantAnalysisView



urlpatterns = patterns('',

    url(r'^applicant_analysis', ApplicantAnalysisView.as_view(), name='appAnalysis'),


)

urlpatterns += staticfiles_urlpatterns()