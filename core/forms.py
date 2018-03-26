from django import forms
from .models import Reservation, Room

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('first_name', 'last_name', 'e_mail_address', 'country_name', 'city_name', 'phone_number')

class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_name', 'room_description', 'smoking', 'max_people')

class DateInput(forms.DateInput):
    input_type = 'date'

class DateSelectionForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
