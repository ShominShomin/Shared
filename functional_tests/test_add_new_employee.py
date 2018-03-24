from functional_tests.base import FunctionalTest


# Ажилтан нэмэх товч дээр дарав.
# Ажилтан нэмэх хуудас дээр шинэ ажилтан Тулга-ийн хэрэгцээт мэдээллийг оруулав.
# Баталгаажуулах товчийг дарахад ажилтан Тулга-ийг бүртгэв.

#Ажилтан Тулга ажилтдын нэвтрэх хуудсыг нээж нэвтрэх эрхээрээ амжилттай нэвтэрч орж болж байв.

class EmployeeAdditionTest(FunctionalTest):
    def test_initial_web_test(self):
        # Ажилтан Болд ажилтдын нэвтрэх хуудсын хаягийг нээж нэвтрэх эрхээрээ нэвтэрч оров

        url = self.live_server_url + '/accounts/login'
        self.browser.get(url)

        self.assertIn('Hotel System', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Employee', header_text)

        self.browser.find_element_by_id('id_username').send_keys('Bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')

        self.browser.find_element_by_id('submit').click()

        header_text = self.browser.find_element_by_id('username').text
        self.assertIn('Bold', header_text)



