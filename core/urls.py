from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^reservation/(?P<year>\d+)/(?P<month>\d+)/$', views.reservation_page, name='reservation'),
    url(r'^reservation/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.reservation_room_page,
        name='reservation_room'),
    url(r'^reservation/$', views.reservation_room_page, name='reservation_room'),
    url(r'^reservation/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<room>\d+)/$', views.reservation_place_order_page,
        name='reservation_auth'),
    url(r'^confirm_order$', views.confirm_order_page, name='confirm_order'),
    url(r'^check_reservation$', views.check_reservation_page, name='check_reservation'),
    url(r'^employee$', views.employee_home_page, name='employee_home'),
    url(r'^employee/add$', views.employee_add_page, name='employee_add'),
    url(r'^employee/reservations$', views.reservation_confirmation_page, name='confirm_reservations'),
    url(r'^status/(?P<pk>\d+)/$', views.reservation_confirmation_status, name='reservation_status'),
    url(r'^rooms$', views.room_list_page, name='room_list'),
]
