from django.test import TestCase

from datetime import datetime
from datetime import timedelta
from core.models import ReservedRoom, Room, Reservation
from core.views import daterange
from core.forms import ReservationForm

from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from datetime import date


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ReservationPageTest(TestCase):

    def test_reservation_page_uses_template(self):
        reservation_date = "/reservation"
        response = self.client.get(reservation_date)
        self.assertTemplateUsed(response, 'reservation.html')

    def test_redirects_to_reservation_room_page(self):
        start_date = datetime.today().strftime('%m/%d/%Y')
        end_date = datetime.today().strftime('%m/%d/%Y')
        response = self.client.post(
            f'/reservation', {'start_date': start_date, 'end_date': end_date}
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
        response = self.client.get(f'/reservation/{self.start_date}/{self.end_date}/1000')
        self.assertTemplateUsed(response, 'reservation_place_order.html')

    def test_invalid_room_fails(self):
        response = self.client.get(f'/reservation/{self.start_date}/{self.end_date}/999')
        self.assertRedirects(response, f'/')

    def test_existing_room_fails(self):
        Room.objects.create(room_number=1000, room_name="Deluxe")
        ReservedRoom.objects.create(room_number=1000, date=self.date_now)
        response = self.client.get(f'/reservation/{self.start_date}/{self.end_date}/1000')
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
            f'/reservation/{self.start_date}/{self.end_date}/1000',
            {'first_name': "Bat",
             'last_name': "Tuvshin",
             'e_mail_address': "bat@tuvshin.com",
             'country_name': "MN",
             'city_name': "Ulaanbaatar",
             'phone_number': "999999999"}
        )
        self.assertRedirects(response, f'/display/1')
        self.assertEqual(Reservation.objects.get(pk=1).confirmation, False)
        self.assertEqual(Reservation.objects.all().count(), 1)

    def test_authorized_user_post(self):
        user = User.objects.create_user('bat', 'bat@tuvshin.com', 'tuvshin')
        user.save()
        self.client = Client()
        self.client.login(username='bat', password='tuvshin')

        Room.objects.create(room_number=1000, room_name="Deluxe")
        response = self.client.post(
            f'/reservation/{self.start_date}/{self.end_date}/1000',
            {'first_name': "Bat",
             'last_name': "Tuvshin",
             'e_mail_address': "bat@tuvshin.com",
             'country_name': "MN",
             'city_name': "Ulaanbaatar",
             'phone_number': "999999999"}
        )
        self.assertRedirects(response, f'/display/1')
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
        response = self.client.get(f'/display/1')
        self.assertTemplateUsed(response, 'reservation_display_page.html')

    def test_employee_register_reservation(self):
        user = User.objects.create_user('bat', 'bat@tuvshin.com', 'tuvshin')
        user.save()
        self.client = Client()
        self.client.login(username='bat', password='tuvshin')
        self.client.post(
            f'/reservation/{self.start_date}/{self.end_date}/1000',
            {'first_name': "Bat",
             'last_name': "Tuvshin",
             'e_mail_address': "bat@tuvshin.com",
             'country_name': "MN",
             'city_name': "Ulaanbaatar",
             'phone_number': "999999999"}
        )
        response = self.client.get(f'/display/2')
        self.assertContains(response, 'True')


class EmployeeHomeTest(TestCase):

    def only_employees_can_access(self):
        response = self.client.get('/employee')
        self.assertRedirects(response, f'/login/')

    def test_uses_home_template(self):
        user = User.objects.create_user('bat', 'bat@tuvshin.com', 'tuvshin')
        user.save()
        self.client = Client()
        self.client.login(username='bat', password='tuvshin')
        response = self.client.get('/employee')
        self.assertTemplateUsed(response, 'employee/home.html')


class NewEmployeeAddTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('bat', 'bat@tuvshin.com', 'tuvshin')
        user.is_staff = True
        user.save()
        self.client.login(username='bat', password='tuvshin')

    def test_only_staff_can_access(self):
        self.client.logout()
        response = self.client.get(f'/employee/add')
        self.assertRedirects(response, f'/accounts/login/?next=/employee/add')
        user = User.objects.create_user('bold', 'bold@bayar.com', 'bayar')
        user.save()
        self.client.login(username='bold', password='bayar')
        response = self.client.get(f'/employee/add')
        self.assertRedirects(response, f'/admin/login/?next=/employee/add')

    def test_uses_employee_add_template(self):
        response = self.client.get(f'/employee/add')
        self.assertTemplateUsed(response, 'employee/add.html')

    def test_forms(self):
        form_data = {'username': "TestUser",
                     'password1': "newEmployee",
                     'password2': "newEmployee"}
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_employee_add(self):
        response = self.client.post(
            f'/employee/add',
            {'username': "TestUser",
             'password1': "newEmployee",
             'password2': "newEmployee"}
        )
        self.assertRedirects(response, f'/employee')
        self.assertEqual(User.objects.all().count(), 2)


class ReservationConfirmationTest(TestCase):

    def setUp(self):
        Reservation.objects.create(first_name="Bat", last_name="Dorj", e_mail_address="1@this.com",
                                   country_name="MN", city_name="this_city", phone_number="C12345678")
        Reservation.objects.create(first_name="Bayar", last_name="Bold", e_mail_address="2@this.com",
                                   country_name="MN", city_name="this_city", phone_number="211111111",
                                   confirmation=True)
        user = User.objects.create_user('bat', 'bat@tuvshin.com', 'tuvshin')
        user.is_staff = True
        user.save()
        self.client.login(username='bat', password='tuvshin')

    def test_reservation_confirmation_uses_template(self):
        response = self.client.get(f'/employee/reservations')
        self.assertTemplateUsed(response, 'employee/reservations.html')

    def test_only_employees_can_access(self):
        self.client.logout()
        response = self.client.get(f'/employee/reservations')
        self.assertRedirects(response, f'/accounts/login/?next=/employee/reservations')

    def test_only_unconfirmed_reservations_showed(self):
        response = self.client.get(f'/employee/reservations')
        self.assertContains(response, 'Bat')
        self.assertNotContains(response, 'Bayar')

    def test_reservation_status_change(self):
        reservation = Reservation.objects.create(first_name="Third", last_name="Test", e_mail_address="3@this.com",
                                                 country_name="MN", city_name="this_city", phone_number="46558982")
        response = self.client.get(f'/employee/reservations')
        self.assertContains(response, 'Bat')
        self.assertNotContains(response, 'Bayar')
        self.assertContains(response, 'Third')
        self.client.get(f'/status/{reservation.id}')
        self.assertEqual(Reservation.objects.get(id=reservation.pk).confirmation, True)
        response = self.client.get(f'/employee/reservations')
        self.assertContains(response, 'Bat')
        self.assertNotContains(response, 'Bayar')
        self.assertNotContains(response, 'Third')


class RoomListTest(TestCase):

    def setUp(self):
        Room.objects.create(room_number=1, room_name="Deluxe")
        Room.objects.create(room_number=2, room_name="Combo")
        Room.objects.create(room_number=3, room_name="Set")
        user = User.objects.create_user('bat', 'bat@tuvshin.com', 'tuvshin')
        user.save()
        self.client.login(username='bat', password='tuvshin')

    def test_only_employees_can_access(self):
        self.client.logout()
        response = self.client.get(f'/rooms')
        self.assertRedirects(response, f'/accounts/login/?next=/rooms')

    def test_room_list_uses_template(self):
        response = self.client.get(f'/rooms')
        self.assertTemplateUsed(response, 'employee/rooms.html')

    def test_room_list_display_right_room_data(self):
        response = self.client.get(f'/rooms')
        self.assertContains(response, 'Deluxe')
        self.assertContains(response, 'Combo')
        self.assertContains(response, 'Set')
        self.assertNotContains(response, True)
        ReservedRoom.objects.create(room_number=1, date=date.today())
        response = self.client.get(f'/rooms')
        self.assertContains(response, True)

    def test_room_list_room_change_status(self):
        room = Room.objects.create(room_number=4, room_name="Test", last_cleaned=timezone.now() - timedelta(days=5))
        last_cleaned = room.last_cleaned
        self.client.get(f'/room/status/{room.pk}')
        self.assertGreater(Room.objects.get(pk=room.pk).last_cleaned, last_cleaned)


class RoomEditTest(TestCase):

    def setUp(self):
        Room.objects.create(room_number=1, room_name="Deluxe")
        Room.objects.create(room_number=2, room_name="Combo")
        Room.objects.create(room_number=3, room_name="Set")

        user = User.objects.create_user('bat', 'bat@tuvshin.com', 'tuvshin')
        user.is_staff = True
        user.save()
        self.client.login(username='bat', password='tuvshin')

    def test_only_staff_can_access(self):
        self.client.logout()
        response = self.client.get(f'/room/new')
        self.assertRedirects(response, f'/accounts/login/?next=/room/new')
        response = self.client.get(f'/room/edit/1')
        self.assertRedirects(response, f'/accounts/login/?next=/room/edit/1')

        user = User.objects.create_user('bold', 'bold@bayar.com', 'bayar')
        user.save()
        self.client.login(username='bold', password='bayar')
        response = self.client.get(f'/room/new')
        self.assertRedirects(response, f'/admin/login/?next=/room/new')
        response = self.client.get(f'/room/edit/1')
        self.assertRedirects(response, f'/admin/login/?next=/room/edit/1')

    def test_room_edit_uses_template(self):
        response = self.client.get(f'/room/new')
        self.assertTemplateUsed(response, 'employee/edit.html')
        response = self.client.get(f'/room/edit/1')
        self.assertTemplateUsed(response, 'employee/edit.html')

    def test_new_room(self):
        response = self.client.post(
            f'/room/new',
            {'room_name': "testRoom",
             'room_description': "description",
             'smoking': True,
             'max_people': 9}
        )
        self.assertRedirects(response, f'/rooms')
        self.assertEqual(Room.objects.all().count(), 4)

    def test_room_edit(self):
        room_before = Room.objects.get(pk=1)
        response = self.client.post(
            f'/room/edit/1',
            {'room_name': "testRoom",
             'room_description': "description",
             'smoking': True,
             'max_people': 9}
        )
        self.assertRedirects(response, f'/rooms')
        self.assertEqual(Room.objects.all().count(), 3)
        room_after = Room.objects.get(pk=1)
        self.assertNotEqual(room_before.room_name, room_after.room_name)
        self.assertNotEqual(room_before.room_description, room_after.room_description)
        self.assertNotEqual(room_before.smoking, room_after.smoking)
        self.assertNotEqual(room_before.max_people, room_after.max_people)
