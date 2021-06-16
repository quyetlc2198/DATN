from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *
app_name = 'adminsite'

urlpatterns = [
    path('', admin_site, name = 'admin site'),
    path('category', admin_site_category, name='admin_site_category'),
    path('room', admin_site_room, name='admin_site_room'),
    path('booking', admin_site_booking, name='admin_site_booking'),
    path('add_category', admin_site_add_category, name='admin_site_add_category'),
    path('add_room', admin_site_add_room, name='admin_site_add_room'),
    path('add_service/',admin_site_add_service, name= 'admin_site_add_service')

]