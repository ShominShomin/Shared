from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_protect
import datetime
from datetime import date

from .customcalendar import CustomCalendar
from .forms import ReservationForm
from .models import Room, ReservedRoom, Reservation


def home_page(request):
    current_date = str(date.year) + "/" + str(date.month)
    return render(request, 'home.html', {'current_date': mark_safe(current_date), })


def reservation_page(request, year, month):
    year = int(year)
    month = int(month)
    cal = CustomCalendar().formatmonth(year, month)
    return render(request, 'reservation.html', {'calendar': mark_safe(cal), })


def reservation_room_page(request, year, month, day):
    reservation_date = datetime.datetime(int(year), int(month), int(day))
    reserved_rooms = ReservedRoom.objects.filter(date=reservation_date)
    rooms = Room.objects.all()
    for reserved_room in reserved_rooms:
        rooms = rooms.exclude(room_id=reserved_room.room_id)
    return render(request, 'reservation_room.html', {'rooms': rooms})


def reservation_place_order_page(request, year, month, day, room):
    reservation_date = datetime.datetime(int(year), int(month), int(day))
    if ReservedRoom.objects.filter(room_id=room, date=reservation_date).exists():
        return render(request, 'home.html')
    if not Room.objects.filter(room_id=room).exists():
        return render(request, 'home.html')
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            if ReservedRoom.objects.filter(room_id=room, date=reservation_date).exists():
                return render(request, 'home.html')
            reserved_room = ReservedRoom(reservation_date, room)
            reserved_room.save()
            reservation = reservation_form.save()
            reservation.room = Room.objects.get(pk=room)
            reservation.date = reservation_date
            if request.user.is_authenticated():
                reservation.confirmation = True
            reservation.save()
            return render(request, 'reservation_confirm_order.html', {'reservation': mark_safe(reservation), })
    else:
        reservation_form = ReservationForm(initial={'country_name': 'MN'})
    return render(request, 'reservation_place_order.html', {'reservation_form': reservation_form})


def confirm_order_page(request, reservation):
    return render(request, 'reservation_confirm_order.html')


def check_reservation_page(request):
    return render(request, 'check_reservation.html')


@login_required
def employee_home_page(request):
    return render(request, 'employee/home.html')


@staff_member_required
def employee_add_page(request):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
    else:
        user_creation_form = UserCreationForm()
    return render(request, 'employee/add.html.', {'user_creation_form': user_creation_form})


@login_required
def reservation_confirmation_page(request):
    reservations = Reservation.objects.filter(confirmation=False)
    return render(request, 'employee/reservations.html', {'reservations': reservations})


@csrf_protect
@login_required
def reservation_confirmation_status(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    reservation.confirmation = not reservation.confirmation
    reservation.save()
    return redirect(request.META['HTTP_REFERER'])

@staff_member_required
def room_list_page(request):
    room_list = Room.objects.all()
    return render(request, 'employee/rooms.html', {'room_list': room_list})