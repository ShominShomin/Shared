from functional_tests.base import FunctionalTest
from functional_tests.wait import wait_for_page_load
import re

class InitialTest(FunctionalTest):

    def test_reservation(self):
        # Бат зочид буудлын талаар сонсоод вебсайтыг нь зочилхоор шийдэв
        # Веб хуудсын гарчигт тухайн вебийн нэр бичээстэй байв
        self.browser.get(self.live_server_url)
        self.assertIn('Hotel System', self.browser.title)

        # Онлайнаар захиалга өгч болохыг мэдээд захиалга өгөхөөр шийдэв
        # Тухайн хуудсыг шалгаж үзэхэд буудаллах өдрөө сонгох хэсэг байв
        self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div').click()
        # Бат буудаллах өдрөө сонгоход өрөөгөө сонгох хуудас дүрслэгдэв
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/button[1]').click()


        # Өрөөгөө сонгоход баталгаажуулах хуудас гарч ирэв
        chosenroombox = self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/a[1]/div')
        with wait_for_page_load(self.browser):
            chosenroombox.click()
        text_found = re.search(r'Booking Form', self.browser.page_source)
        self.assertNotEqual(text_found, None)

        # Бат  мэдээллээ хийгээд баталгаажуулалтын товчийг дарав
        self.browser.find_element_by_name('first_name').send_keys('Bat')
        self.browser.find_element_by_name('last_name').send_keys('Bayar')
        self.browser.find_element_by_name('e_mail_address').send_keys('Bat@gmail.com')
        ##if need to test dropdown selector uncomment
        ##self.browser.find_element_by_name('country_name').select_by_visible_text('Mongolia')

        self.browser.find_element_by_name('address').send_keys('This address')
        self.browser.find_element_by_name('phone_number').send_keys('99999999')
        self.browser.find_element_by_id('id_confirmation_button').click()


        # Бат захиалгаа амжилттай бүртгэгдсэн боловч баталгаажаагүй байгааг харав
        text_found = re.search(r'Reservation is not confirmed. Wait until an employee contacts you.', self.browser.page_source)
        self.assertNotEqual(text_found, None)

