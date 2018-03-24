from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
import datetime


class InitialTest(FunctionalTest):

    def test_initial_web_test(self):
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
        # Тухайн хуудсыг шалгаж үзэхэд тухайн сарын календар харагдаж байв.
        month_text = self.browser.find_element_by_name('monthName').text
        mydate = datetime.datetime.now()
        test_date = mydate.strftime("%B").upper() + " " + str(mydate.year)
        self.assertIn(test_date, month_text)
        chosendatebox = self.browser.find_element_by_link_text(str(mydate.day))
        chosendatebox.click()

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

        # Бат захиалгаа өгч дууссаныг хараад browser-ийг хаав
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your reservation has been placed', header_text)
