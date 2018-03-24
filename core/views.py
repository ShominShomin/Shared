from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.safestring import mark_safe
from datetime import date
from .customcalendar import CustomCalendar
from .forms import ReservationForm
from .models import Room, ReservedRoom
from django.contrib.auth.forms import UserCreationForm
import datetime


def home_page():
    current_date = str(date.year) + "/" + str(date.month)
    return render_to_response('home.html', {'current_date': mark_safe(current_date), })


def home_page(request):
    return render(request, 'home.html')


def reservation_page(request, year, month):
    year = int(year)
    month = int(month)
    cal = CustomCalendar().formatmonth(year, month)
    return render(request, 'reservation.html', {'calendar': mark_safe(cal), })


def reservation_get(year, month):
    year = int(year)
    month = int(month)
    cal = CustomCalendar().formatmonth(year, month)
    return render_to_response('reservation.html', {'calendar': mark_safe(cal), })


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
            reservation.save()

            return render(request, 'reservation_confirm_order.html', {'reservation': mark_safe(reservation), })

    else:
        reservation_form = ReservationForm(initial={'country_name': 'MN'})

    return render(request, 'reservation_place_order.html', {'reservation_form': reservation_form})


def confirm_order_page(request, reservation):
    return render(request, 'reservation_confirm_order.html')


def check_reservation_page(request):
    return render(request, 'check_reservation.html')


def employee_home_page(request):
    return render(request, 'employee/home.html')


def employee_add_page(request):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()

    else:
        user_creation_form = UserCreationForm()

    return render(request, 'employee/add.html.', {'user_creation_form': user_creation_form})
