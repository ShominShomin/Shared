from django import forms
from .models import Reservation, Room, Schedule, BigText
from datetime import datetime


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('first_name', 'last_name', 'e_mail_address', 'country_name', 'city_name', 'phone_number')


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_name', 'room_description', 'smoking', 'max_people', 'image',)


class DateInput(forms.DateInput):
    input_type = 'date'


class DateSelectionForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('event', 'start_time', 'end_time')


class BigTextForm(forms.ModelForm):
    class Meta:
        model = BigText
        fields = ('title', 'text')
