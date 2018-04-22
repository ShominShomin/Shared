from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    last_cleaned = models.DateTimeField(default=timezone.now)
    is_occupied = models.BooleanField(default=False)
    room_number = models.PositiveIntegerField(default=0)

    room_name = models.CharField(max_length=40)
    room_description = models.TextField(max_length=800, default=' ')
    smoking = models.BooleanField(default=False)
    max_people = models.PositiveIntegerField(default=1)
    image = models.FileField(upload_to='image/', default='image/room_default.png')

    def __str__(self):
        return self.room_name


class Reservation(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    e_mail_address = models.CharField(max_length=50)
    country_name = CountryField()
    address = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20)
    confirmation = models.BooleanField(default=False)

    @property
    def reserved_room(self):
        return ReservedRoom.objects.filter(reservation=self)

    @property
    def reserved_room_number(self):
        return ReservedRoom.objects.filter(reservation=self).values('room_number').distinct()

    def __str__(self):
        string = self.first_name + " " + str(self.last_name)
        return string

class ReservedRoom(models.Model):
    reserved_room_id = models.AutoField(primary_key=True)
    date = models.DateField()
    room_number = models.PositiveIntegerField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True)

    @property
    def is_past_due(self):
        return timezone.now().date() > self.date

    @property
    def my_reservation(self):
        return Reservation.objects.get(id = self.reservation.id)

    class Meta:
        unique_together = ('date', 'room_number',)

    def __str__(self):
        string = str(self.room_number) + ", " + str(self.date)
        return string


class DeletedReservation(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    e_mail_address = models.CharField(max_length=50)
    country_name = CountryField()
    address = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20)
    deleted_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        string = self.first_name + " " + str(self.last_name)
        return string


class Schedule(models.Model):
    event = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        string = self.event + " " + str(self.start_time) + " " + str(self.end_time)
        return string


class BigText(models.Model):
    title = models.CharField(max_length=40, default='No Title')
    text = models.TextField(max_length=1000, default=' ')

    def __str__(self):
        return self.title
