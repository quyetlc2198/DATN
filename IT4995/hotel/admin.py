from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.
from django.contrib.auth.models import Group


admin.site.unregister(Group)

class AdminBooking(admin.ModelAdmin):
    list_display = [ "user",'room']

admin.site.register(service)

admin.site.site_header = 'Sapa Hotel'

# admin site manage room
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_editable = ['category']
    list_filter = ['category']
    search_fields=['category','name']
    fields = ('name','category')
    change_list_template = 'admin/change_list_graph.html'

admin.site.register(Rooms,RoomAdmin)


# admin site manage category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','price_randian']
    list_editable = ['price_randian']

admin.site.register(Categories,CategoryAdmin)


# admin site manage booking
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id','user','Name','room','arival_date','departure_date','status','voucher','Fee','Discount']
    list_editable = ['status']
    search_fields = ['user','Name']
    list_per_page = 20
    change_list_template = 'admin/change_list_graph1.html'


admin.site.register(Booking,BookingAdmin)


class VoucherAdmin(admin.ModelAdmin):
    list_display = ['name', 'code','discount','qty','create_date','end_date']
    list_editable = ['discount']

admin.site.register(Voucher,VoucherAdmin)

# admin site manage user

