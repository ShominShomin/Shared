from django.shortcuts import get_object_or_404, render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_protect
from datetime import date, timedelta, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ReservationForm, RoomCreationForm, DateSelectionForm, ScheduleForm
from .models import Room, ReservedRoom, Reservation, Schedule, BigText, DeletedReservation


def home_page(request):
    current_date = str(date.year) + "/" + str(date.month)
    schedules = Schedule.objects.all()
    return render(request, 'home.html', {'current_date': mark_safe(current_date), 'schedules': schedules})


def reservation_room_page(request, start_date, end_date):
    rooms = Room.objects.all()
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    for single_date in daterange(start_date, end_date):
        reserved_rooms = ReservedRoom.objects.filter(date=single_date)

        for reserved_room in reserved_rooms:
            rooms = rooms.exclude(room_number=reserved_room.room_number)

    return render(request, 'reservation_room.html', {'rooms': rooms})


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def reservation_place_order_page(request, start_date, end_date, room):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    for single_date in daterange(start_date, end_date):
        if ReservedRoom.objects.filter(room_number=room, date=single_date).exists():
            return redirect(home_page)
    if not Room.objects.filter(room_number=room).exists():
        return redirect(home_page)

    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation = reservation_form.save()
            for single_date in daterange(start_date, end_date):
                if ReservedRoom.objects.filter(room_number=room, date=single_date).exists():
                    reservation.delete()
                    return render(request, 'home.html')
                reserved_room = ReservedRoom(date=single_date, room_number=room)
                reserved_room.reservation = reservation
                reserved_room.save()
            if request.user.is_authenticated():
                reservation.confirmation = True
            reservation.save()
            return redirect('reservation_display', pk=reservation.pk)
            # return render(request, 'reservation_display_page.html', {'pk': reservation.pk})
    else:
        reservation_form = ReservationForm(initial={'country_name': 'MN'})
    return render(request, 'reservation_place_order.html', {'reservation_form': reservation_form})


def reservation_display_page(request, pk):
    reservation = Reservation.objects.filter(pk=pk)
    reserved_rooms = ReservedRoom.objects.filter(reservation=reservation)
    return render(request, 'reservation_display_page.html',
                  {'reservation': reservation, 'reserved_rooms': reserved_rooms})


@login_required
def employee_home_page(request):
    from django.utils import timezone
    reserved_rooms = ReservedRoom.objects.filter(date=timezone.now().date())
    return render(request, 'employee/home.html', {'reserved_rooms': reserved_rooms})


@login_required
@staff_member_required
def employee_add_page(request):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            return redirect('employee_home')
    else:
        user_creation_form = UserCreationForm()
    return render(request, 'employee/add.html', {'user_creation_form': user_creation_form})


@login_required
def reservation_confirmation_page(request):
    reservations = Reservation.objects.filter(confirmation=False)
    reserved_rooms = ReservedRoom.objects.filter(reservation=reservations.values('pk'))
    return render(request, 'employee/reservations.html',
                  {'reservations': reservations, 'reserved_rooms': reserved_rooms})


@csrf_protect
@login_required
def reservation_confirmation_status(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    reservation.confirmation = not reservation.confirmation
    reservation.save()
    return redirect('confirm_reservations')


@csrf_protect
@login_required
def reservation_delete(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    deleted_reservation = DeletedReservation(first_name=reservation.first_name, last_name=reservation.last_name,
                                             e_mail_address=reservation.e_mail_address,
                                             country_name=reservation.country_name, address=reservation.address,
                                             phone_number=reservation.phone_number)
    deleted_reservation.save()
    reservation.delete()
    return redirect('confirm_reservations')


@login_required
def room_list_page(request):
    room_list = Room.objects.all()
    for room in room_list:
        if ReservedRoom.objects.filter(room_number=room.room_number, date=date.today()).exists():
            room.is_occupied = True
        else:
            room.is_occupied = False
    return render(request, 'employee/rooms.html', {'room_list': room_list})


@login_required
def room_clean_status(request, pk):
    from django.utils import timezone
    room = Room.objects.get(pk=pk)
    room.last_cleaned = timezone.now()
    room.save()
    return redirect('room_list')


@login_required
def room_remove(request, pk):
    room = Room.objects.get(pk=pk)
    room.delete()
    return redirect('room_list')


@login_required
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


@login_required
def all_reservations_page(request):
    reservation_list = Reservation.objects.filter(confirmation=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(reservation_list, 25)
    try:
        reservations = paginator.page(page)
    except PageNotAnInteger:
        reservations = paginator.page(1)
    except EmptyPage:
        reservations = paginator.page(paginator.num_pages)
    return render(request, 'employee/all.html', {'reservations': reservations})


@login_required
def deleted_reservations_page(request):
    reservation_list = DeletedReservation.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(reservation_list, 25)
    try:
        reservations = paginator.page(page)
    except PageNotAnInteger:
        reservations = paginator.page(1)
    except EmptyPage:
        reservations = paginator.page(paginator.num_pages)
    return render(request, 'employee/deleted.html', {'reservations': reservations})


@login_required
def schedule_page(request):
    schedule_list = Schedule.objects.all()
    return render(request, 'employee/schedules.html', {'schedule_list': schedule_list})


@login_required
def schedule_edit_page(request, pk=None):
    if pk:
        schedule = get_object_or_404(Schedule, pk=pk)
    else:
        schedule = Schedule()
    form = ScheduleForm(request.POST or None, instance=schedule)
    if request.POST and form.is_valid():
        form.save()
        return redirect(schedule_page)
    return render(request, 'employee/schedule_edit.html', {'form': form})


@login_required
def schedule_remove(request, pk):
    schedule = Schedule.objects.get(pk=pk)
    schedule.delete()
    return redirect('schedule_list')
