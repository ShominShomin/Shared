from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^reservation/(?P<year>\d+)/(?P<month>\d+)/$', views.reservation_page, name='reservation'),
    url(r'^reservation/(?P<start_date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/(?P<end_date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$',
        views.reservation_room_page,
        name='reservation_room'),
    url(r'^reservation/$', views.reservation_room_page, name='reservation_room'),

    url(
        r'^reservation/(?P<start_date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/(?P<end_date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/(?P<room>\d+)/$',
        views.reservation_place_order_page,
        name='reservation_auth'),

    url(r'^display/(?P<pk>\d+)/$', views.reservation_display_page, name='reservation_display'),

    url(r'^employee$', views.employee_home_page, name='employee_home'),
    url(r'^employee/add$', views.employee_add_page, name='employee_add'),
    url(r'^employee/reservations$', views.reservation_confirmation_page, name='confirm_reservations'),
    url(r'^status/(?P<pk>\d+)/$', views.reservation_confirmation_status, name='reservation_status'),
    url(r'^rooms$', views.room_list_page, name='room_list'),

    url(r'^room/status/(?P<pk>\d+)/$', views.room_clean_status, name='clean_status'),

    url(r'^room/new/$', views.room_edit_page, name='room_new'),
    url(r'^room/edit/(?P<pk>\d+)/$', views.room_edit_page, name='room_edit'),
]
