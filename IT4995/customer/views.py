from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
from django.views.generic.base import View
from hotel.models import *
from .models import *
# Create your views here.
from django.utils.decorators import method_decorator
from django.http import HttpResponse

class Cus_Booking(View):
    def get(self, request, *args, **kwargs):
        my_booking = Booking.objects.filter(user=request.user)
        return render(request, 'customer/my_room_test.html', {'booking_list': my_booking})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        data = request.POST['data']
        check_in_date = request.POST['check_in']
        check_out_date = request.POST['check_out']
        adults = (request.POST['adults'])
        children = (request.POST['children'])
        voucher_code = request.POST['voucher_code']
        try:
            adults = 0 if (adults == '') else int(adults)
            children = 0 if (children == '') else int(children)
            i = format_date(check_in_date)
            o = format_date(check_out_date)
        except:
            return  redirect('hotel:Category_detail', name = data)
        if data is not None and adults != 0 and (adults + children) <= 10:
            room_lst = Rooms.objects.filter(category__in=Categories.objects.filter(name = data))
            avail_room = []
            for room in room_lst:
                avail_room.append(room)
            for room in room_lst:
                booking1 = Booking.objects.filter(room=room, status='PENDING')
                booking2 = Booking.objects.filter(room=room, status='CONFIRM')
                booking3 = Booking.objects.filter(room=room, status='OCCUPIED')
                if len(booking1) != 0:
                    for b in booking1:
                        if b.departure_date >= datetime.strptime(i,
                                                                '%Y-%m-%d').date() or b.arival_date <= datetime.strptime(
                                o, '%Y-%m-%d').date():
                            avail_room.remove(b.room)
                elif len(booking2) != 0:
                    for b in booking2:
                        if b.departure_date >= datetime.strptime(i,
                                                                '%Y-%m-%d').date() or b.arival_date <= datetime.strptime(
                                o, '%Y-%m-%d').date():
                            avail_room.remove(b.room)
                elif len(booking3) != 0:
                    for b in booking2:
                        if b.departure_date >= datetime.strptime(i,
                                                                '%Y-%m-%d').date() or b.arival_date <= datetime.strptime(
                                o, '%Y-%m-%d').date():
                            avail_room.remove(b.room)
            avail_room = list(set(avail_room))
            if len(avail_room) != 0:
                voucher = Voucher.objects.filter(code=voucher_code).first()
                print(voucher)
                if voucher is not None:
                    if voucher.qty > 0 and voucher.create_date < datetime.strptime(i,
                                                                                   '%Y-%m-%d').date() and voucher.end_date > datetime.strptime(
                            i, '%Y-%m-%d').date():
                        a = Booking.objects.create(room=avail_room[0], user=request.user, number_adults=adults,
                                                   number_children=children,
                                                   arival_date=i, departure_date=o, voucher=voucher)
                        voucher.qty -= 1
                        voucher.save()
                        a.save()
                        booking_id = a.id
                    else:
                        a = Booking.objects.create(room=avail_room[0], user=request.user, number_adults=adults,
                                                   number_children=children,
                                                   arival_date=i, departure_date=o)
                        a.save()
                        booking_id = a.id
                else:
                    a = Booking.objects.create(room=avail_room[0], user=request.user, number_adults=adults,
                                               number_children=children,
                                               arival_date=i, departure_date=o)
                    a.save()
                    booking_id = a.id
            else:
                return HttpResponse('<h1>No Room</h1>')
        else:
            return redirect('hotel:Category_detail', name = data)
        my_booking = Booking.objects.filter(user=request.user)
        print(booking_id)
        return render(request, 'customer/my_room_test.html', {'booking_list': my_booking})


def cancel_booking(request):
    if request.method == 'POST':
        book_id = request.POST['cancel_booking']
        b= Booking.objects.get(id = book_id)
        try:
            b.status = "CANCEL"
            b.save()
        except:
            pass
    return redirect('customer:booking_room')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('hotel:Homepage')
    error = ''
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['pwd']
        user = authenticate(username=email, password=pwd)
        try:
            if user:
                login(request, user)
                error = 'no'
            else:
                error = 'yes'
        except:
            error = 'yes'
    try:
        next_page = request.GET['next']
    except:
        next_page = ''
    return render(request, 'customer/login_user.html', {'error': error, 'next_page': next_page})

@login_required
def Comment(request):
    if request.method == 'POST':
        room_type_review = request.POST['room_type_review']
        position_review = request.POST['position_review']
        comfort_review = request.POST['comfort_review']
        price_review = request.POST['price_review']
        quality_review = request.POST['quality_review']
        review_text = request.POST['review_text']
        evals = "Position: " + position_review + ' Comfort: ' + comfort_review + ' Price: ' + price_review + ' Quality: ' + quality_review
        category = Categories.objects.filter(name=room_type_review).first()
        if category is None or category == '':
            return redirect('hotel:Category')
        if room_type_review != '':
            tmp = Comments.objects.create(category=category, user=request.user, evaluation=evals, comment=review_text)
            tmp.save()
            return redirect('hotel:Category_detail', name=category)
        else:
            return redirect('hotel:Category_detail', name=category)
    return redirect('hotel:Category_detail')

def format_date(datetime):
    datetime = datetime.split()
    day = datetime[1] if datetime[1] >= '10' else '0' + datetime[1]
    month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
             'Sep': '09', 'Oct': '10', 'Now': '11', 'Dec': '12'}
    year = date.today().year
    return '-'.join([str(year), month[datetime[0]], day])

#
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')
    error = ""
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contact = request.POST['contact']
        email = request.POST['email']
        password = request.POST['pwd']
        try:
            user = User.objects.create_user(username=email, password=password, first_name=first_name,
                                            last_name=last_name)
            Signup.objects.create(user=user, contact=contact)
            error = 'no'
        except:
            error = 'yes'
    d = {'error': error}
    return render(request, 'customer/sign_up.html', d)


@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('customer:Login')
    data = Signup.objects.get(user=request.user.username)
    print(data)
    return render(request, 'customer/profile.html', {'data': data})

# to change password user
@login_required
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = ""
    if request.method == 'POST':
        o_p = request.POST['o-pwd']
        n_p = request.POST['n-pwd']
        c_p = request.POST['c-pwd']
        u = User.objects.get(username__exact=request.user.username)
        if not check_password(o_p, u.password):
            error = "yes"
        elif c_p == n_p:
            u.password = make_password(n_p)
            u.save()
            error = "no"
        else:
            error = "yes"
    d = {"error": error}
    return render(request, 'customer/changepassword.html', d)


def Logout(request):
    logout(request)
    return redirect('hotel:Homepage')