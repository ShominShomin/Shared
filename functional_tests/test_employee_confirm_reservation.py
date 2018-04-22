from functional_tests.base import FunctionalTest
from functional_tests.wait import wait_for_page_load
import re


class EmployeeConfirmReservationTest(FunctionalTest):

    def test_confirming_reservation(self):
        # Ажилтан Болд ажилтдын нэвтрэх хуудсын хаягийг нээж нэвтрэх эрхээрээ нэвтэрч оров
        url = self.live_server_url + '/accounts/login'
        self.browser.get(url)
        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('submit').click()
        # Захиалга товч дээр дарахад баталгаажаагүй хэрэглэгчдийн жагсаалт харагдана
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('Confirm Reservations').click()
        text_found = re.search(r'Bat', self.browser.page_source)
        self.assertNotEqual(text_found, None)

        # Жагсаалтаас Бат-ийн захиалгийг хараад баталгаажуулахад тухайн захиалга
        # Баталгаажуулаагүй захиалгын жагсаалтаас хасагдав
        button = self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td[9]/a[1]')
        with wait_for_page_load(self.browser):
            button.click()
        text_found = re.search(r'Bat', self.browser.page_source)
        self.assertEqual(text_found, None)
        text_found = re.search(r'There are no unconfirmed reservations!', self.browser.page_source)
        self.assertNotEqual(text_found, None)

    def test_removing_reservation(self):
        url = self.live_server_url + '/accounts/login'
        self.browser.get(url)
        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('submit').click()
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('Confirm Reservations').click()
        text_found = re.search(r'Bat', self.browser.page_source)
        self.assertNotEqual(text_found, None)

        # Жагсаалтаас Бат-ийн захиалгийг хараад устгахад тухайн захиалга
        # Баталгаажуулаагүй захиалгын жагсаалтаас хасагдав
        button = self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td[9]/a[2]')
        with wait_for_page_load(self.browser):
            button.click()
        text_found = re.search(r'Bat', self.browser.page_source)
        self.assertEqual(text_found, None)

        #Устгагдсан захиалгын жагсаалтыг харахаар шийдэв
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('Deleted').click()
        #Жагаалтад саяхан устгасан Батын захиалга харагдаж байна
        text_found = re.search(r'Bat', self.browser.page_source)
        self.assertNotEqual(text_found, None)
