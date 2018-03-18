from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime


class InitialTest(FunctionalTest):

    def test_initial_web_test(self):
        current_date = datetime.datetime.now()

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

        # Өөрийн буудаллах боломжит сарын эхний өдрийг сонгоход өрөөний сонголтууд гарч ирэв.
        chosendatebox = self.browser.find_element_by_link_text('1')
        chosendatebox.click()
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Choose Room', header_text)

        # Өрөөгөө сонгоход баталгаажуулах хуудас гарч ирэв.
        chosenroombox = self.browser.find_element_by_id('id_room_box')
        chosenroombox.click()
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Enter credentials', header_text)

        # Бат  мэдээллээ хийгээд баталгаажуулалтын товчийг дарахад
        # тухайн захиалга бүртгэгдэж. Захиалга амжилттай болсноор
        # захиалгын дугаар болон нууц кодыг тухайн хуудаст дүрслэв
        credentialsbutton = self.browser.find_element_by_id('id_confirmation_button')
        credentialsbutton.click()
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your reservation has been placed', header_text)
        # more status displayed under.


        # Бат захиалгаа өгч дуусаад захиалгаа шалгах товчийг дарснаар өөрийн захиалгийн статусыг харахад
        # Захиалга бүртгэгдсэн боловч баталгаажаагүйг харуулж байв
        self.browser.refresh()
        self.browser.get(self.live_server_url)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Home', header_text)

        checkbutton = self.browser.find_element_by_id('id_check_reservation_button')
        checkbutton.click()

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Reservation Check', header_text)

        # Ажилтан Болд нэвтрэх эрхээрээ нэвтэрч оров

        # Захиалга товч дээр дарахад баталгаажаагүй хэрэглэгчдийн жагсаалт харагдана

        # Жагсаалтаас Бат-ийн захиалгийг хараад холбогдох утас-руу залгаж/смсдэв.

        # Батийн захиалгийг ажилтан Болд баталгаажуулав.

        # Мэдээллийн ажилтан/Систем Бат-тай утсаар/мэйл/СМС-ээр холбогдоод захиалгыг баталгаажуулсны
        # дараагаар Бат захиалгаа шалгахад батаалгажсан статустай болсон байна.
