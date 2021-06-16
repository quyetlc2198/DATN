from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from datetime import date, datetime
from hotel.models import *
from customer.models import *

@login_required(login_url='/admin/')
def admin_site(request):
    if not request.user.is_staff:
        return redirect('/admin')
    booking = Booking.objects.all()
    room = Rooms.objects.all()
    comment = Comments.objects.all()
    context = {
        'booking': len(booking),
        'room':len(room),
        'comment': len(comment),
        'room_lst': room,
        'booking_lst': booking,
    }
    return render(request, 'adminsite/main.html/', context= context)


@login_required(login_url='/login_user/')
def admin_site_category(request):
    category_lst = Categories.objects.all()
    context = {
        'categories': category_lst
    }
    return render(request, 'adminsite/category.html', context=context)
@login_required(login_url='/login_user/')
def admin_site_room(request):
    room_lst = Rooms.objects.all()
    context = {
        'rooms': room_lst
    }
    return render(request, 'adminsite/room.html', context=context)
@login_required(login_url='/login_user/')
def admin_site_booking(request):
    # booking_lst = Booking.objects.all()
    # context = {
    #     'books': booking_lst
    # }
    # return render(request, 'adminsite/booking.html', context=context)
    return reverse('hotel/booking')


@login_required(login_url='/login_user/')
def admin_site_add_category(request):
    if request.method == 'GET':
        service_lst = service.objects.all()
        context = {
            'ser_lst': service_lst
        }
        return render(request, 'adminsite/add_category.html', context=context)
    else:
        name_category = request.POST['name']
        price = request.POST['price']
        des = (request.POST['description'])
        ser_lst = request.POST.getlist('service')
        cate = Categories.objects.create(name=name_category, description=des, price_randian=price)
        for ser in ser_lst:
            s = get_object_or_404(service, name=ser)
            cate.service_list.add(s)
        cate.save()
        return redirect('admin_site_category')
@login_required(login_url='/login_user/')
def admin_site_add_room(request):
    if request.method == 'GET':
        categories = Categories.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'adminsite/add_room.html', context=context)
    else:
        name = request.POST['name']
        price = request.POST['price']
        des = (request.POST['description'])
        cate_lst = request.POST.getlist('category')
        cate = get_object_or_404(Categories, name=cate_lst[0])
        room = Rooms.objects.create(name=name, price=price, description=des, status=0, category=cate)
        room.save()
        return redirect('admin_site_room')


# delete booking
def admin_booking_room_delete(request,id):
    if not request.user.is_staff:
        return redirect('/admin')
    try:
        room = Booking.objects.get(pk=id)
        room.room.status = 0
        room.room.save()
        room.delete()
    except:
        pass
    return redirect('admin_booking')

def admin_site_add_service(request):
    return redirect('hotel:Homepage')



