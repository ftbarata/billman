from django.conf.urls import url
from django.contrib import admin
from .core.views import public_home, login, private_home, logout, profile_view

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/$', profile_view, name='profile-view'),
    url(r'^private-home/$', private_home, name='private-home'),
    url(r'^$', public_home, name='public_home'),
    url(r'^admin/', admin.site.urls),
]
