import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from core.models import Room, Reservation
from django.contrib.auth.models import User
import datetime

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

        first_room = Room(room_id=1, room_name="Deluxe")
        first_room.save()
        second_room = Room(room_id=2, room_name="Combo")
        second_room.save()

        User.objects.create_user(username='bold',
                                 email='bold@bgmail.com',
                                 password='CocaCola', is_staff=True)

        reservation_date = datetime.date(2017, 10, 24)
        first_reservation = Reservation(first_name="Bat", last_name="Dorj", e_mail_address="1@this.com",
                                        country_name="MN", city_name="this_city", phone_number="C12345678",
                                        date=reservation_date, room=first_room
                                        )
        first_reservation.save()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()
