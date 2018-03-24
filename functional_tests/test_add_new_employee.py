from functional_tests.base import FunctionalTest


class EmployeeAdditionTest(FunctionalTest):
    def test_initial_web_test(self):
        # Ажилтан Болд ажилтдын нэвтрэх хуудсын хаягийг нээж нэвтрэх эрхээрээ нэвтэрч оров

        url = self.live_server_url + '/accounts/login'
        self.browser.get(url)

        self.assertIn('Hotel System', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Employee', header_text)

        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')

        self.browser.find_element_by_id('submit').click()

        header_text = self.browser.find_element_by_tag_name('p').text
        self.assertIn('bold', header_text)

        # Ажилтан нэмэх товч дээр дарав.
        self.browser.find_element_by_link_text('Add employee').click()
        # Ажилтан нэмэх хуудас дээр шинэ ажилтан Тулга-ийн хэрэгцээт мэдээллийг оруулав.

        self.browser.find_element_by_id('id_username').send_keys('Tulga')
        self.browser.find_element_by_id('id_password1').send_keys('SevenEight')
        self.browser.find_element_by_id('id_password2').send_keys('SevenEight')

        # Баталгаажуулах товчийг дарахад ажилтан Тулга-ийг бүртгэв.
        self.browser.find_element_by_id('submit').click()

        #Болд нэвтрэх эрхээрээ орсноо гаргаад Тулга өөрийн шинэ нэвтрэх эрхээрээ
        #ажилтдын нэвтрэх хуудсыг нээж нэвтрэх эрхээрээ амжилттай нэвтэрч орж болж байв.
        url = self.live_server_url + '/accounts/logout'
        self.browser.get(url)

        url = self.live_server_url + '/accounts/login'
        self.browser.get(url)

        self.browser.find_element_by_id('id_username').send_keys('Tulga')
        self.browser.find_element_by_id('id_password').send_keys('SevenEight')

        self.browser.find_element_by_id('submit').click()

        header_text = self.browser.find_element_by_tag_name('p').text
        self.assertIn('Tulga', header_text)




