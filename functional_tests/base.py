import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from core.models import Room
from django.contrib.auth.models import User
import time

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

        first_room = Room(room_id=1, room_name="Deluxe")
        first_room.save()
        second_room = Room(room_id=2, room_name="Combo")
        second_room.save()


        first_employee = User.objects.create_user(username='bold',
                                              email='bold@bgmail.com',
                                              password='CocaCola')


    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()
