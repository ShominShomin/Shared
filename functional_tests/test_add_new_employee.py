from functional_tests.base import FunctionalTest
from functional_tests.wait import wait_for_page_load

class EmployeeAdditionTest(FunctionalTest):

    def test_adding_new_employee(self):
        # Менежер Болд ажилтдын нэвтрэх хуудсын хаягийг нээж нэвтрэх эрхээрээ нэвтэрч оров
        url = self.live_server_url + '/accounts/login/'
        self.browser.get(url)
        self.assertIn('Hotel System', self.browser.title)
        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('submit').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/employee')

        # Ажилтан нэмэх товч дээр дарав.
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('Add employee').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/employee/add')
        # Ажилтан нэмэх хуудас дээр шинэ ажилтан Тулга-ийн хэрэгцээт мэдээллийг оруулав.
        self.browser.find_element_by_id('id_username').send_keys('Tulga')
        self.browser.find_element_by_id('id_password1').send_keys('SevenEight')
        self.browser.find_element_by_id('id_password2').send_keys('SevenEight')
        # Баталгаажуулах товчийг дарахад ажилтан Тулга-ийг бүртгэв.
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('id_confirmation_button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url+ '/employee')

        # Болд нэвтрэх эрхээрээ орсноо гаргаад Тулга өөрийн шинэ нэвтрэх эрхээрээ
        # ажилтдын нэвтрэх хуудсыг нээж нэвтрэх эрхээрээ амжилттай нэвтэрч орж болж байв.
        url = self.live_server_url + '/accounts/logout/'
        self.browser.get(url)
        url = self.live_server_url + '/accounts/login/'
        with wait_for_page_load(self.browser):
            self.browser.get(url)

        self.browser.find_element_by_id('id_username').send_keys('Tulga')
        self.browser.find_element_by_id('id_password').send_keys('SevenEight')
        self.browser.find_element_by_id('submit').click()
        self.assertEqual(self.browser.current_url, self.live_server_url+ '/employee')

