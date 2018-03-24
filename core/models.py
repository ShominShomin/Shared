from django.db import models
from django_countries.fields import CountryField


class Room(models.Model):
    room_id = models.PositiveIntegerField(primary_key=True)
    room_name = models.CharField(max_length=40)

    def __str__(self):
        return self.room_name


class Reservation(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    e_mail_address = models.CharField(max_length=50)
    country_name = CountryField()
    city_name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20)

    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)

    confirmation = models.BooleanField(default=False)

    def __str__(self):
        string = self.first_name + " " + str(self.date)
        return string


class ReservedRoom(models.Model):
    date = models.DateField()
    room_id = models.PositiveIntegerField(primary_key=True)

    class Meta:
        unique_together = ('date', 'room_id',)

    def __str__(self):
        string = str(self.room_id) + ", " + str(self.date)
        return string

