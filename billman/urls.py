from django.urls import path
from django.contrib import admin
from .core.views import public_home, login, private_home, logout, profile_view, contacts_view

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile_view, name='profile-view'),
    path('private-home/', private_home, name='private-home'),
    path('', public_home, name='public_home'),
    path('admin/', admin.site.urls),
    path('contacts-view/', contacts_view, name='contacts-view'),
]
