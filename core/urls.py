from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^reservation$', views.reservation_page, name='reservation'),
    url(r'^room$', views.room_page, name='room'),
    url(r'^reservation_auth$', views.reservation_auth_page, name='reservation_auth'),
    url(r'^confirm_order$', views.confirm_order_page, name='confirm_order'),
    url(r'^check_reservation$', views.check_reservation_page, name='check_reservation'),
    url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)/$', views.calendar),
]
