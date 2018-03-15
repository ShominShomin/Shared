from django.test import TestCase
import json

from datetime import datetime
from datetime import timedelta
from core.models import ReservedRoom, Room, Reservation
from core.views import daterange
from core.forms import ReservationForm

from django.test.client import Client


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ReservationPageTest(TestCase):

    def test_reservation_page_uses_template(self):
        year = datetime.today().year
        month = datetime.today().month
        reservation_date = "/reservation/" + str(year) + "/" + str(month) + "/"
        response = self.client.get(reservation_date)
        self.assertTemplateUsed(response, 'reservation.html')

    def test_redirects_to_reservation_room_page(self):
        year = datetime.today().year
        month = datetime.today().month
        start_date = datetime.today().strftime('%m/%d/%Y')
        end_date = datetime.today().strftime('%m/%d/%Y')
        response = self.client.post(
            f'/reservation/{year}/{month}/', {'start_date': start_date, 'end_date': end_date}
        )
        start_date = datetime.today().strftime('%Y-%m-%d')
        end_date = datetime.today().strftime('%Y-%m-%d')
        self.assertRedirects(response, f'/reservation/{start_date}/{end_date}/')


class ReservationRoomPageTest(TestCase):
    start_date = datetime.today().strftime('%Y-%m-%d')
    end_date = (datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d')

    def test_reservation_room_page_uses_template(self):
        response = self.client.get(f'/reservation/{self.start_date}/{self.end_date}/')
        self.assertTemplateUsed(response, 'reservation_room.html')

    def test_daterange_function(self):
        date = datetime.today()
        n = 0
        for single_date in daterange(date, date + timedelta(10)):
            self.assertEqual(date + timedelta(n), single_date)
            n = n + 1

    def test_displays_the_correct_rooms(self):
        Room.objects.create(room_number=1, room_name="Deluxe")
        Room.objects.create(room_number=2, room_name="Combo")
        Room.objects.create(room_number=3, room_name="Queen")

        ReservedRoom.objects.create(room_number=3, date=datetime.today())

        response = self.client.get(f'/reservation/{self.start_date}/{self.end_date}/')
        self.assertContains(response, 'Deluxe')
        self.assertContains(response, 'Combo')
        self.assertNotContains(response, 'Queen')


class ReservationPlaceOrderTest(TestCase):
    date_now = datetime.today()
    start_date = date_now.strftime('%Y-%m-%d')
    end_date = (date_now + timedelta(days=5)).strftime('%Y-%m-%d')

    def test_reservation_place_page_uses_template(self):
        Room.objects.create(room_number=1000, room_name="Deluxe")
        response = self.client.get(f'/reservation/{self.start_date}/{self.end_date}/1000/')
        self.assertTemplateUsed(response, 'reservation_place_order.html')

    def test_invalid_room_fails(self):
        response = self.client.get(f'/reservation/{self.start_date}/{self.end_date}/999/')
        self.assertRedirects(response, f'/')

    def test_existing_room_fails(self):
        Room.objects.create(room_number=1000, room_name="Deluxe")
        ReservedRoom.objects.create(room_number=1000, date=self.date_now)
        response = self.client.get(f'/reservation/{self.start_date}/{self.end_date}/1000/')
        self.assertRedirects(response, f'/')

    def test_forms(self):
        form_data = {'first_name': 'Bat',
                     'last_name': 'Tuvshin',
                     'e_mail_address': 'bat@tuvshin.com',
                     'country_name': 'MN',
                     'city_name': 'Ulaanbaatar',
                     'phone_number': '999999999'}
        form = ReservationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_reservation_post(self):
        Room.objects.create(room_number=1000, room_name="Deluxe")
        response = self.client.post(
            f'/reservation/{self.start_date}/{self.end_date}/1000/',
            {'first_name': "Bat",
             'last_name': "Tuvshin",
             'e_mail_address': "bat@tuvshin.com",
             'country_name': "MN",
             'city_name': "Ulaanbaatar",
             'phone_number': "999999999"}
        )
        self.assertRedirects(response, f'/display/1/')
        self.assertEqual(Reservation.objects.get(pk=1).confirmation, False)
        self.assertEqual(Reservation.objects.all().count(), 1)

    def test_authorized_user_post(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user('bat', 'bat@tuvshin.com', 'tuvshin')
        user.save()
        self.client = Client()
        self.client.login(username='bat', password='tuvshin')

        Room.objects.create(room_number=1000, room_name="Deluxe")
        response = self.client.post(
            f'/reservation/{self.start_date}/{self.end_date}/1000/',
            {'first_name': "Bat",
             'last_name': "Tuvshin",
             'e_mail_address': "bat@tuvshin.com",
             'country_name': "MN",
             'city_name': "Ulaanbaatar",
             'phone_number': "999999999"}
        )
        self.assertRedirects(response, f'/display/1/')
        self.assertEqual(Reservation.objects.get(pk=1).confirmation, True)
        self.assertEqual(Reservation.objects.all().count(), 1)


class ReservationDisplayTest(TestCase):
    date_now = datetime.today()
    start_date = date_now.strftime('%Y-%m-%d')
    end_date = (date_now + timedelta(days=5)).strftime('%Y-%m-%d')

    def setUp(self):
        Room.objects.create(room_number=1000, room_name="Deluxe")
        Reservation.objects.create(first_name="Bat", last_name="Dorj", e_mail_address="1@this.com",
                                   country_name="MN", city_name="this_city", phone_number="C12345678")

    def test_reservation_display_page_uses_template(self):
        response = self.client.get(f'/display/1/')
        self.assertTemplateUsed(response, 'reservation_display_page.html')

    def test_employee_register_reservation(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user('bat', 'bat@tuvshin.com', 'tuvshin')
        user.save()
        self.client = Client()
        self.client.login(username='bat', password='tuvshin')
        self.client.post(
            f'/reservation/{self.start_date}/{self.end_date}/1000/',
            {'first_name': "Bat",
             'last_name': "Tuvshin",
             'e_mail_address': "bat@tuvshin.com",
             'country_name': "MN",
             'city_name': "Ulaanbaatar",
             'phone_number': "999999999"}
        )
        response = self.client.get(f'/display/2/')
        self.assertContains(response, 'True')

