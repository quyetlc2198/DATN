from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic.base import View
from datetime import datetime
from customer.models import Comments
from customer.views import *
from .models import *

class HomePage(View):
    def get(self, request, *args,**kwargs):
        # lấy toàn bộ danh sách các loại phòng
        categories_lst = Categories.objects.all()
        comment_lst = Comments.objects.all()
        context = {
            'categories_lst' : categories_lst,
            'comment_lst': comment_lst,
        }
        return render(request, 'hotel/index.html', context=context)

def Category(request):
    categories_lst = Categories.objects.all()
    comment_lst = Comments.objects.all()
    context = {
        'categories_lst': categories_lst,
        'comment_lst': comment_lst,
    }
    return render(request, 'hotel/categories.html',context=context)

def Category_Detail(request, name = None):
    category = get_object_or_404(Categories, name = name)
    cmt_lst = Comments.objects.filter(category=category)
    context = {
        'category':category,
        'comments':cmt_lst,
    }
    return render(request, 'hotel/room_category.html',  context= context)

def Category_Room(request, name = None):
    category = get_object_or_404(Categories, name = name)
    cate_lst = Categories.objects.all()
    room_lst = Rooms.objects.filter(category=category)
    comments = Comments.objects.filter(category=category)
    ser = service.objects.all()
    context = {
        'cate_lst': cate_lst,
        'category': category,
        'room_lst': room_lst,
        'comments':comments,
        'ser':ser,

    }
    return render(request,'hotel/room_list.html', context= context)

def profile(request):
    return render(request, 'hotel/index.html', )

def my_room(request):
    return render(request, 'hotel/index.html', )


# list availble room
def availble_list(request):
    if request.method == 'POST':
        check_in_date = request.POST['check_in']
        check_out_date = request.POST['check_out']
        adults = request.POST['adults']
        children = request.POST['children']
        print(check_in_date)
        print(check_out_date)
        try:
            i = format_date(check_in_date)
            o = format_date(check_out_date)
        except:
            return redirect('hotel:Homepage')
        room_lst = Rooms.objects.all()
        avail_room = []
        for room in room_lst:
            avail_room.append(room)
        for room in room_lst:
            booking1 = Booking.objects.filter(room=room, status='PENDING')
            booking2 = Booking.objects.filter(room=room, status='CONFIRM')
            booking3 = Booking.objects.filter(room=room, status='OCCUPIED')
            if len(booking1) != 0:
                for b in booking1:
                    if b.departure_date >= datetime.strptime(i, '%Y-%m-%d').date() and b.arival_date <= datetime.strptime(o,'%Y-%m-%d').date():
                        avail_room.remove(b.room)
            elif len(booking2)!= 0:
                for b in booking2:
                    if b.departure_date >= datetime.strptime(i, '%Y-%m-%d').date() and b.arival_date <= datetime.strptime(
                            o, '%Y-%m-%d').date():
                        avail_room.remove(b.room)
            elif len(booking3)!= 0:
                for b in booking2:
                    if b.departure_date >= datetime.strptime(i, '%Y-%m-%d').date() and b.arival_date <= datetime.strptime(
                            o, '%Y-%m-%d').date():
                        avail_room.remove(b.room)
        print(avail_room)
        avail_room = list(set(avail_room))
        context = {
            'categories_lst': Categories.objects.all(),
            'room_lst' : avail_room,
            'check_in':check_in_date,
            "check_out":check_out_date,
            'adults' : adults,
            'children': children,
        }

        return render(request, 'hotel/avail_room.html',context=context)



