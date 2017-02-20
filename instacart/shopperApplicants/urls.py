from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views import ShopperLandingPageView, ShopperApplicantsEditView, ShopperConfirmBackgroundCheckView, \
    ShopperApplicationView, ShopperLoginView, ShopperLogoutView


urlpatterns = patterns('',

                       url(r'^shoppers/$', ShopperLandingPageView.as_view(), name='shopperLand'),
                       url(r'^shoppers/apply/$', ShopperApplicationView.as_view(), name='shopperApply'),
                       url(r'^shoppers/edit/(?P<id>\w+)', ShopperApplicantsEditView.as_view(), name='shopperEdit'),
                       url(r'^shoppers/bgc', ShopperConfirmBackgroundCheckView.as_view(), name='shopperBckCheck'),
                       url(r'^shoppers/login', ShopperLoginView.as_view(), name='shopperLogin'),
                       url(r'shoppers/logout', ShopperLogoutView.as_view(), name='shopperLogout')
)
urlpatterns += staticfiles_urlpatterns()