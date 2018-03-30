from django.conf.urls import include, url
from django.contrib import admin
from core import views as core_views
from core import urls as core_urls
from django.contrib.auth import views

urlpatterns = [
    url(r'^$', core_views.home_page, name='home'),
    url(r'^', include(core_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
]