from django import forms
from .models import Reservation, Room, Schedule, BigText

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('first_name', 'last_name', 'e_mail_address', 'country_name', 'address', 'phone_number')


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_number','room_name', 'room_description', 'smoking', 'max_people', 'image')

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('event', 'start_time', 'end_time')


class BigTextForm(forms.ModelForm):
    class Meta:
        model = BigText
        fields = ('title', 'text')
