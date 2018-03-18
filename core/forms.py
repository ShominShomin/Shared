from django import forms
from .models import Reservation, Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_id', 'room_name')

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('first_name', 'last_name', 'e_mail_address', 'country_name', 'city_name', 'phone_number')
