from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from core.models import Room, Reservation
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
import time

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

        first_room = Room(room_number=1, room_name="Deluxe", last_cleaned = timezone.datetime(2017, 11, 22, 21, 10, 9, 127325, tzinfo=pytz.UTC))
        first_room.save()
        second_room = Room(room_number=2, room_name="Combo")
        second_room.save()

        User.objects.create_user(username='bold',
                                 email='bold@bgmail.com',
                                 password='CocaCola', is_staff=True)

        first_reservation = Reservation(first_name="Bat", last_name="Dorj", e_mail_address="1@this.com",
                                        country_name="MN", address="this_address", phone_number="C12345678")
        first_reservation.save()

    def tearDown(self):
        time.sleep(2)
        self.browser.refresh()
        self.browser.quit()