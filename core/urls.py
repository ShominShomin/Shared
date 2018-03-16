from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^confirm_order$', views.confirm_order_page, name='confirm_order'),
    url(r'^check_reservation$', views.check_reservation_page, name='check_reservation'),
    url(r'^reservation/(?P<year>\d+)/(?P<month>\d+)/$', views.reservation, name='reservation'),
    url(r'^reservation/(?P<year>\d+)/(?P<month>\d+)/$', views.reservation_get),
    url(r'^reservation/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.room_page, name='reservation_room'),
    url(r'^reservation/$', views.room_page, name='reservation_room'),
    url(r'^reservation/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<room>\d+)/$', views.reservation_auth_page, name='reservation_auth'),
]
