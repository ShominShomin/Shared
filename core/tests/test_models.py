from django.test import TestCase
from core.models import Reservation, Room, ReservedRoom
import datetime


class ModelsTest(TestCase):

    def setUp(self):
        first_room = Room(room_id=1, room_name="Deluxe")
        first_room.save()
        second_room = Room(room_id=2, room_name="Combo")
        second_room.save()

        reservation_date = datetime.date(2017, 10, 24)
        first_reservation = Reservation(first_name="Bat", last_name="Dorj", e_mail_address="1@this.com",
                                        country_name="MN", city_name="this_city", phone_number="C12345678",
                                        date=reservation_date, room=first_room
                                        )
        first_reservation.save()

        second_reservation = Reservation(first_name="Bayar", last_name="Bold", e_mail_address="2@this.com",
                                         country_name="MN", city_name="this_city", phone_number="C9999999",
                                         date=reservation_date, room=second_room
                                         )
        second_reservation.save()

    def test_retrieving_reservations(self):
        reservation_date = datetime.date(2017, 10, 24)

        saved_rooms = Room.objects.all()
        first_saved_room = saved_rooms[0]
        second_saved_room = saved_rooms[1]

        saved_reservations = Reservation.objects.all()
        self.assertEqual(saved_reservations.count(), 2)

        first_saved_reservation = saved_reservations[0]
        self.assertEqual(first_saved_reservation.first_name, 'Bat')
        self.assertEqual(first_saved_reservation.last_name, 'Dorj')
        self.assertEqual(first_saved_reservation.e_mail_address, '1@this.com')
        self.assertEqual(first_saved_reservation.country_name, 'MN')
        self.assertEqual(first_saved_reservation.city_name, 'this_city')
        self.assertEqual(first_saved_reservation.phone_number, 'C12345678')
        self.assertEqual(first_saved_reservation.date, reservation_date)
        self.assertEqual(first_saved_reservation.room, first_saved_room)

        second_saved_reservation = saved_reservations[1]
        self.assertEqual(second_saved_reservation.first_name, 'Bayar')
        self.assertEqual(second_saved_reservation.last_name, 'Bold')
        self.assertEqual(second_saved_reservation.e_mail_address, '2@this.com')
        self.assertEqual(second_saved_reservation.country_name, 'MN')
        self.assertEqual(second_saved_reservation.city_name, 'this_city')
        self.assertEqual(second_saved_reservation.phone_number, 'C9999999')
        self.assertEqual(second_saved_reservation.date, reservation_date)
        self.assertEqual(second_saved_reservation.room, second_saved_room)

    def test_retrieving_rooms(self):
        saved_rooms = Room.objects.all()
        self.assertEqual(saved_rooms.count(), 2)

        first_saved_room = saved_rooms[0]
        second_saved_room = saved_rooms[1]
        self.assertEqual(first_saved_room.room_id, 1)
        self.assertEqual(first_saved_room.room_name, 'Deluxe')
        self.assertEqual(second_saved_room.room_id, 2)
        self.assertEqual(second_saved_room.room_name, 'Combo')

    def test_saving_and_retrieving_reserved_rooms(self):
        reservation_date = datetime.date(2017, 10, 24)
        first_reserved_room = ReservedRoom(room_id=1, date=reservation_date)
        first_reserved_room.save()
        second_reserved_room = ReservedRoom(room_id=2, date=reservation_date)
        second_reserved_room.save()
        double_booking_room = ReservedRoom(room_id=1, date=reservation_date)
        double_booking_room.save()

        saved_reserved_rooms = ReservedRoom.objects.all()
        self.assertEqual(saved_reserved_rooms.count(), 2)
        self.assertEqual(saved_reserved_rooms[0].room_id, 1)
        self.assertEqual(saved_reserved_rooms[0].date, reservation_date)
        self.assertEqual(saved_reserved_rooms[1].room_id, 2)
        self.assertEqual(saved_reserved_rooms[1].date, reservation_date)
