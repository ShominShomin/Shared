from django.db import models
from django_countries.fields import CountryField
from datetime import datetime
from django.utils import timezone


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)

    room_number = models.PositiveIntegerField(default=0)
    last_cleaned = models.DateTimeField(default=timezone.now)
    is_occupied = models.BooleanField(default=False)

    room_name = models.CharField(max_length=40)
    room_description = models.TextField(max_length=800, default=' ')
    smoking = models.BooleanField(default=False)
    max_people = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.room_name


class Reservation(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    e_mail_address = models.CharField(max_length=50)
    country_name = CountryField()
    city_name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20)

    confirmation = models.BooleanField(default=False)

    def __str__(self):
        string = self.first_name + " " + str(self.last_name)
        return string


class ReservedRoom(models.Model):
    reserved_room_id = models.AutoField(primary_key=True)
    #below are the fields
    date = models.DateField()
    room_number = models.PositiveIntegerField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('date', 'room_number',)

    def __str__(self):
        string = str(self.room_number) + ", " + str(self.date)
        return string
