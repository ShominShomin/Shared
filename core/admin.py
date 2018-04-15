from django.contrib import admin
from .models import Room, Reservation, ReservedRoom, BigText, Schedule

admin.site.register(Reservation)
admin.site.register(Room)
admin.site.register(ReservedRoom)
admin.site.register(Schedule)
admin.site.register(BigText)