from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from datetime import date
from .customcalendar import CustomCalendar


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
    return render(request, 'reservation_room.html')


def reservation_choose_method_page(request, year, month, day, room):
    return render(request, 'reservation_choose_method.html')


def confirm_order_page(request):
    return render(request, 'confirm_order.html')


def check_reservation_page(request):
    return render(request, 'check_reservation.html')
