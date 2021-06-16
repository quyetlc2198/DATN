from datetime import date

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# model category room
from django.db.models import UniqueConstraint
from django.urls import reverse


class service(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/service')
    link_url = models.CharField(max_length=40)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1500, default='')
    description_home = models.CharField(max_length=500, default='')
    image = models.ImageField(upload_to='static/images/categories', default='')
    price_randian = models.FloatField(default=0)
    service_list = models.ManyToManyField(service)
    def __str__(self):
        return self.name
    # category detail
    def get_absolute_url(self):
        return reverse('hotel:Category_detail', args=[self.name])

    # list room of category
    def get_absolute_url1(self):
        return reverse('hotel:Category_Room', args=[self.name])
#     list comment of category
    def get_absolute_url2(self):
        return reverse('hotel:Category_detail', args=[self.name])



# model room
class Rooms(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Voucher(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    # %
    discount = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    description = models.CharField(max_length=100, null=True)
    create_date = models.DateField(default= date.today())
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.name
STATUS_BOOKING = [
        ('PENDING', 'Pending'),
        ('CONFIRM', 'Confirm'),
        ('OCCUPIED','Occupied'),
        ('RETURNED','Returned'),
        ('CANCEL','Cancel')
    ]
# model book a room

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    number_adults = models.IntegerField(default=0)
    number_children = models.IntegerField(default=0)
    arival_date = models.DateField()
    departure_date = models.DateField()
    UniqueConstraint(fields=['user', 'room'], name='unique_user_booking')
    status = models.CharField(max_length=10, choices= STATUS_BOOKING, default='PENDING')
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null= True)
    def __str__(self):
        return self.user.first_name

    def Fee(self):
        time = (self.departure_date - self.arival_date)
        fee = int(time.days)*self.room.category.price_randian
        if self.voucher is None:
            return int(fee)
        else:
            return int(fee*(1-self.voucher.discount/100))
    def Discount(self):
        if self.voucher is None:
            return 0
        else:
            time = (self.departure_date - self.arival_date)
            fee = (int(time.days) * self.room.category.price_randian)
            return int(fee*(self.voucher.discount/100))
    def get_display_fee(self):
        return self.Fee()*100
    def Name(self):
        return self.user.first_name + ' ' + self.user.last_name
    def Email(self):
        return self.user.username
