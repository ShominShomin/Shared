from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
import datetime
from core.models import Reservation


class InitialTest(FunctionalTest):

    def test_reservation(self):
        # Бат зочид буудлын талаар сонсоод вебсайтыг нь зочилхоор шийдэв
        # Анх орж үзэхэд вебийн title болон header-т тухайн вебийн нэр бичээстэй байхыг харав
        self.browser.get(self.live_server_url)
        self.assertIn('Hotel System', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Home', header_text)

        # Зочид буудлын талаар дэлгэрэнгүй мэдээллийг авснаар
        # онлайнаар захиалга өгч болохыг мэдээд захиалга өгөхөөр шийдэв.
        reservationbutton = self.browser.find_element_by_id('id_reservation_button')
        reservationbutton.click()
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Reservation', header_text)
        # Тухайн хуудсыг шалгаж үзэхэд буудаллах өдрөө сонгох хэсэг байв.
        self.browser.find_element_by_name('start_date').send_keys('2018-03-22')
        self.browser.find_element_by_name('end_date').send_keys('2018-03-31')
        self.browser.find_element_by_id('submit').click()

        # Өөрийн буудаллах боломжит сарын эхний өдрийг сонгоход өрөөний сонголтууд гарч ирэв.
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Choose Room', header_text)
        chosenroombox = self.browser.find_element_by_link_text('Deluxe')
        chosenroombox.click()

        # Өрөөгөө сонгоход баталгаажуулах хуудас гарч ирэв
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Enter credentials', header_text)

        # Бат  мэдээллээ хийгээд баталгаажуулалтын товчийг дарахад
        # тухайн захиалга бүртгэгдэж. Захиалга амжилттай болсноор
        # захиалгын дугаар болон нууц кодыг тухайн хуудаст дүрслэв
        self.browser.find_element_by_name('first_name').send_keys('Bat')
        self.browser.find_element_by_name('last_name').send_keys('Bayar')
        self.browser.find_element_by_name('e_mail_address').send_keys('Bat@gmail.com')
        ##if need to test dropdown selector uncomment
        ##Select(self.browser.find_element_by_name('country_name')).select_by_visible_text('Mongolia')
        self.browser.find_element_by_name('city_name').send_keys('Ulaanbaatar')
        self.browser.find_element_by_name('phone_number').send_keys('99999999')
        credentialsbutton = self.browser.find_element_by_id('id_confirmation_button')
        credentialsbutton.click()

        # Бат захиалгаа өгч дууссаныг харав
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your reservation has been placed', header_text)

    def test_employee_reservation(self):
        # Зочид буудал дээр Баяр өрөө авахаар шийдэж хүрэлцэн ирэв.
        # Ажилтан Болд ажилтдын нэвтрэх хуудсын хаягийг нээж нэвтрэх эрхээрээ нэвтэрч оров
        url = self.live_server_url + '/login'
        self.browser.get(url)
        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')
        self.browser.find_element_by_id('submit').click()


        #Шинэ захиалга үүсгэх товч дээр дарж Баярын захиалгыг үүсгэв.
        self.browser.find_element_by_link_text('New Reservation').click()
        self.browser.find_element_by_name('start_date').send_keys('2018-03-22')
        self.browser.find_element_by_name('end_date').send_keys('2018-03-31')
        self.browser.find_element_by_id('submit').click()

        self.browser.find_element_by_link_text('Deluxe').click()
        self.browser.find_element_by_name('first_name').send_keys('Bayar')
        self.browser.find_element_by_name('last_name').send_keys('Bold')
        self.browser.find_element_by_name('e_mail_address').send_keys('Bayar@gmail.com')
        self.browser.find_element_by_name('city_name').send_keys('Ulaanbaatar')
        self.browser.find_element_by_name('phone_number').send_keys('99999999')
        self.browser.find_element_by_id('id_confirmation_button').click()

        # Болд захиалгыг бүртгэж дуусаныг харав
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your reservation has been placed', header_text)
