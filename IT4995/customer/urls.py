from django.urls import  path
from . import views
from .views import *
app_name = 'customer'

urlpatterns = [
    path('booking/',Cus_Booking.as_view(), name = 'booking_room'),
    path('comment/', Comment,name = 'create_comment'),
    path('login_user/', login_user, name ='Login'),
    path('signup',sign_up, name = 'sign_up'),
    path('profile/',profile,name='profile'),
    path('change_password/', change_password, name='change_password'),
    path('logout/', Logout, name='logout'),
    path('cancel/', cancel_booking, name="cancel"),
]
