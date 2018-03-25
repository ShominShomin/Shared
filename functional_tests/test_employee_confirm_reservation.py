from functional_tests.base import FunctionalTest
import re


class EmployeeConfirmReservationTest(FunctionalTest):

    def test_confirming_reservation(self):
        # Ажилтан Болд ажилтдын нэвтрэх хуудсын хаягийг нээж нэвтрэх эрхээрээ нэвтэрч оров
        url = self.live_server_url + '/login'
        self.browser.get(url)
        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')
        self.browser.find_element_by_id('submit').click()

        # Захиалга товч дээр дарахад баталгаажаагүй хэрэглэгчдийн жагсаалт харагдана
        self.browser.find_element_by_link_text('Confirm Reservations').click()
        text_found = re.search(r'Bat', self.browser.page_source)
        self.assertNotEqual(text_found, None)

        # Жагсаалтаас Бат-ийн захиалгийг хараад баталгаажуулахад тухайн захиалга
        # Баталгаажуулаагүй захиалгын жагсаалтаас хасагдав
        self.browser.find_element_by_id('Bat').click()
        text_found = re.search(r'Bat', self.browser.page_source)
        self.assertEqual(text_found, None)
