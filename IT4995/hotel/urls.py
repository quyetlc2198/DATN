from django.urls import  path
from django.views.generic import TemplateView

from . import views
from .views import *
app_name = 'hotel'

urlpatterns = [
    path('', HomePage.as_view(), name = 'Homepage'),
    path('about/', TemplateView.as_view(template_name='hotel/about.html')),
    path('contact/', TemplateView.as_view(template_name='hotel/contacts.html')),
    path('support/', TemplateView.as_view(template_name='hotel/support.html')),
    path('category/',Category,name = 'Category'),
    path('category/<str:name>/', Category_Detail ,name = 'Category_detail'),
    path('category/<str:name>/room/', Category_Room ,  name = 'Category_Room'),
    path('profile/', profile, name = 'profile'),
    path('room/', my_room, name = 'my_room'),
    path('available_room/',availble_list, name='avail_room'),
]