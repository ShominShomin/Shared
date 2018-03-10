from django.test import TestCase

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ReservationPageTest(TestCase):

    def test_uses_reservation_template(self):
        response = self.client.get('/core/reservation')
        self.assertTemplateUsed(response, 'reservation.html')


class RoomPageTest(TestCase):

    def test_uses_room_page_template(self):
        response = self.client.get('/core/room')
        self.assertTemplateUsed(response, 'room.html')


class ReservationAuthPageTest(TestCase):

    def test_uses_reservation_auth_template(self):
        response = self.client.get('/core/reservation_auth')
        self.assertTemplateUsed(response, 'reservation_auth.html')


class ConfirmOrderPageTest(TestCase):

    def test_uses_confirm_order_template(self):
        response = self.client.get('/core/confirm_order')
        self.assertTemplateUsed(response, 'confirm_order.html')


class CheckReservationPageTest(TestCase):

    def test_uses_check_reservation_template(self):
        response = self.client.get('/core/check_reservation')
        self.assertTemplateUsed(response, 'check_reservation.html')

