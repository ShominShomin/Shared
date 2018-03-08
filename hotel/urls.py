from django.conf.urls import include, url
from core import views as core_views
from core import urls as core_urls

urlpatterns = [
    url(r'^$', core_views.home_page, name='home'),
    url(r'^core/', include(core_urls)),
]