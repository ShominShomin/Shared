from django.contrib import admin
from .models import Room, Reservation, ReservedRoom

admin.site.register(Reservation)
admin.site.register(Room)
admin.site.register(ReservedRoom)