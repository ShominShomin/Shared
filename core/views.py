from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')

def reservation_page(request):
    return render(request, 'reservation.html')

def room_page(request):
    return render(request, 'room.html')

def reservation_auth_page(request):
    return render(request, 'reservation_auth.html')

def confirm_order_page(request):
    return render(request, 'confirm_order.html')

def check_reservation_page(request):
    return render(request, 'check_reservation.html')