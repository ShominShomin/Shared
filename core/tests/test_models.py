from django.test import TestCase
from core.models import Reservation, Room, ReservedRoom, DeletedReservation, Schedule, BigText
import datetime
from django.db import transaction


class ModelsTest(TestCase):

    def setUp(self):
        first_room = Room(room_number=1, room_name="Deluxe")
        first_room.save()
        second_room = Room(room_number=2, room_name="Combo")
        second_room.save()
        first_reservation = Reservation(first_name="Bat", last_name="Dorj", e_mail_address="1@this.com",
                                        country_name="MN", address="this_address", phone_number="C12345678"
                                        )
        first_reservation.save()

        second_reservation = Reservation(first_name="Bayar", last_name="Bold", e_mail_address="2@this.com",
                                         country_name="MN", address="this_address", phone_number="C9999999"
                                         )
        second_reservation.save()

    def test_retrieving_rooms(self):
        saved_rooms = Room.objects.all()
        self.assertEqual(saved_rooms.count(), 2)
        first_saved_room = saved_rooms[0]
        second_saved_room = saved_rooms[1]
        self.assertEqual(first_saved_room.room_number, 1)
        self.assertEqual(first_saved_room.room_name, 'Deluxe')
        self.assertEqual(first_saved_room.room_description, ' ')
        self.assertEqual(first_saved_room.smoking, False)
        self.assertEqual(first_saved_room.max_people, 1)
        self.assertEqual(first_saved_room.image, 'image/room_default.png')
        self.assertEqual(second_saved_room.room_number, 2)
        self.assertEqual(second_saved_room.room_name, 'Combo')

    def test_retrieving_reservations(self):
        saved_reservations = Reservation.objects.all()
        self.assertEqual(saved_reservations.count(), 2)
        first_saved_reservation = saved_reservations[0]
        self.assertEqual(first_saved_reservation.first_name, 'Bat')
        self.assertEqual(first_saved_reservation.last_name, 'Dorj')
        self.assertEqual(first_saved_reservation.e_mail_address, '1@this.com')
        self.assertEqual(first_saved_reservation.country_name, 'MN')
        self.assertEqual(first_saved_reservation.address, 'this_address')
        self.assertEqual(first_saved_reservation.phone_number, 'C12345678')
        second_saved_reservation = saved_reservations[1]
        self.assertEqual(second_saved_reservation.first_name, 'Bayar')
        self.assertEqual(second_saved_reservation.last_name, 'Bold')
        self.assertEqual(second_saved_reservation.e_mail_address, '2@this.com')
        self.assertEqual(second_saved_reservation.country_name, 'MN')
        self.assertEqual(second_saved_reservation.address, 'this_address')
        self.assertEqual(second_saved_reservation.phone_number, 'C9999999')

    def test_saving_and_retrieving_reserved_rooms(self):
        reservation_date = datetime.date(2017, 10, 24)
        first_reserved_room = ReservedRoom(room_number=1, date=reservation_date)
        first_reserved_room.save()
        second_reserved_room = ReservedRoom(room_number=2, date=reservation_date)
        second_reserved_room.save()
        try:
            with transaction.atomic():
                double_booking_room = ReservedRoom(room_number=1, date=reservation_date)
                double_booking_room.save()
        except:
            pass

        saved_reserved_rooms = ReservedRoom.objects.all()
        self.assertEqual(saved_reserved_rooms.count(), 2)
        self.assertEqual(saved_reserved_rooms[0].room_number, 1)
        self.assertEqual(saved_reserved_rooms[0].date, reservation_date)
        self.assertEqual(saved_reserved_rooms[1].room_number, 2)
        self.assertEqual(saved_reserved_rooms[1].date, reservation_date)

    def test_saving_and_retrieving_deleted_reservation(self):
        deleted_reservation = DeletedReservation(first_name="Bat", last_name="Dorj", e_mail_address="1@this.com",
                                                 country_name="MN", address="this_address", phone_number="C12345678"
                                                 )
        deleted_reservation.save()
        deleted_reservation = DeletedReservation(first_name="Bat1", last_name="Dorj1", e_mail_address="11@this.com",
                                                 country_name="MN", address="this_address1", phone_number="C112345678"
                                                 )
        deleted_reservation.save()
        saved_deleted_reservation = DeletedReservation.objects.all()
        self.assertEqual(saved_deleted_reservation.count(), 2)
        self.assertEqual(saved_deleted_reservation[0].first_name, 'Bat')
        self.assertEqual(saved_deleted_reservation[0].last_name, 'Dorj')
        self.assertEqual(saved_deleted_reservation[0].e_mail_address, '1@this.com')
        self.assertEqual(saved_deleted_reservation[0].country_name, 'MN')
        self.assertEqual(saved_deleted_reservation[0].address, 'this_address')
        self.assertEqual(saved_deleted_reservation[0].phone_number, 'C12345678')
        self.assertEqual(saved_deleted_reservation[1], deleted_reservation)


    def test_saving_and_retrieving_schedule(self):
        schedule1 = Schedule(event="New", start_time=datetime.time(11, 23, 44), end_time=datetime.time(11, 25, 44))
        schedule1.save()
        schedule2 = Schedule(event="Next", start_time=datetime.time(8, 11, 10), end_time=datetime.time(8, 25, 12))
        schedule2.save()
        saved_schedule = Schedule.objects.all()
        self.assertEqual(saved_schedule.count(), 2)
        self.assertEqual(saved_schedule[0], schedule1)
        self.assertEqual(saved_schedule[1], schedule2)


    def test_saving_and_retrieving_big_text(self):
        bigtext1 = BigText(title="New", text="Lorem ipsum")
        bigtext1.save()
        bigtext2 = BigText(title="Next", text="Lorem ipsum")
        bigtext2.save()
        saved_bigtext = BigText.objects.all()
        self.assertEqual(saved_bigtext.count(), 2)
        self.assertEqual(saved_bigtext[0], bigtext1)
        self.assertEqual(saved_bigtext[1], bigtext2)