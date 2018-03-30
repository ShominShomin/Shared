from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from core.models import Room, Reservation
from django.contrib.auth.models import User

import time

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

        first_room = Room(room_number=1, room_name="Deluxe")
        first_room.save()
        second_room = Room(room_number=2, room_name="Combo")
        second_room.save()

        User.objects.create_user(username='bold',
                                 email='bold@bgmail.com',
                                 password='CocaCola', is_staff=True)

        first_reservation = Reservation(first_name="Bat", last_name="Dorj", e_mail_address="1@this.com",
                                        country_name="MN", city_name="this_city", phone_number="C12345678")
        first_reservation.save()

    def tearDown(self):
        time.sleep(1)
        self.browser.refresh()
        time.sleep(1)
        self.browser.quit()
