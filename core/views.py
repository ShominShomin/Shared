from django.shortcuts import get_object_or_404, render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_protect
from datetime import date, timedelta, datetime

from .customcalendar import CustomCalendar
from .forms import ReservationForm, RoomCreationForm, DateSelectionForm
from .models import Room, ReservedRoom, Reservation


def home_page(request):
    current_date = str(date.year) + "/" + str(date.month)
    return render(request, 'home.html', {'current_date': mark_safe(current_date), })


def reservation_page(request, year, month):
    year = int(year)
    month = int(month)

    if request.method == 'POST':
        date_selection_form = DateSelectionForm(request.POST)
        if date_selection_form.is_valid():
            return redirect(reservation_room_page, start_date=date_selection_form.cleaned_data['start_date'],
                            end_date=date_selection_form.cleaned_data['end_date'])
    else:
        date_selection_form = DateSelectionForm()

    return render(request, 'reservation.html', {'date_selection_form': date_selection_form})


def reservation_room_page(request, start_date, end_date):
    rooms = Room.objects.all()
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    for single_date in daterange(start_date, end_date):
        reserved_rooms = ReservedRoom.objects.filter(date=single_date)
        for reserved_room in reserved_rooms:
            rooms = rooms.exclude(room_id=reserved_room.room_id)

    return render(request, 'reservation_room.html', {'rooms': rooms})


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def reservation_place_order_page(request, start_date, end_date, room):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    for single_date in daterange(start_date, end_date):
        if ReservedRoom.objects.filter(room_id=room, date=single_date).exists():
            return render(request, 'home.html')
    if not Room.objects.filter(room_id=room).exists():
        return render(request, 'home.html')

    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation = reservation_form.save()
            for single_date in daterange(start_date, end_date):
                if ReservedRoom.objects.filter(room_id=room, date=single_date).exists():
                    reservation.delete()
                    return render(request, 'home.html')
                reserved_room = ReservedRoom(date=single_date, room_id=room)
                reserved_room.reservation = reservation
                reserved_room.save()
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


@login_required
def room_list_page(request):
    room_list = Room.objects.all()
    for room in room_list:
        if ReservedRoom.objects.filter(room_id=room.room_id, date=date.today()).exists():
            room.is_occupied = True
        else:
            room.is_occupied = False
    return render(request, 'employee/rooms.html', {'room_list': room_list})


@login_required
def room_page(request, pk):
    room = Room.objects.get(pk=pk)
    return render(request, 'employee/rooms.html', {'room': room})


@login_required
def room_clean_status(request, pk):
    room = Room.objects.get(pk=pk)
    room.last_cleaned = datetime.now()
    room.save()
    return redirect(request.META['HTTP_REFERER'])


@staff_member_required
def room_edit_page(request, pk=None):
    if pk:
        room = get_object_or_404(Room, pk=pk)
    else:
        room = Room()

    form = RoomCreationForm(request.POST or None, instance=room)
    if request.POST and form.is_valid():
        form.save()
        return redirect(room_list_page)

    return render(request, 'employee/edit.html', {'form': form})
