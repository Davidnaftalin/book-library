from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from shelf.views import HomeView, CheckoutBookView, ReturnBookView, search

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^checkout/(?P<book_id>[\d-]+)/$', CheckoutBookView.as_view(), name='checkout'),
    url(r'^return/(?P<book_id>[\d-]+)/$', ReturnBookView.as_view(), name='return'),
    url(r'^search/$', search, name= 'search'),
    url(r'^$', HomeView.as_view(), name='home'),
)
