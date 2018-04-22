from functional_tests.base import FunctionalTest
from functional_tests.wait import wait_for_page_load
import re



class RoomFunctionTest(FunctionalTest):

    def test_room_functions(self):
        # ажилтан Болд нэвтрэх эрхээрээ нэвтэрч оров
        url = self.live_server_url + '/accounts/login'
        self.browser.get(url)
        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('submit').click()

        # Өрөө гэсэн товч дээр дарахад өрөөнүүдийнг жагсаалт дүрслэгдэв
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('Rooms').click()
        text_found = re.search(r'Deluxe', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'Combo', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        # Тухайн жагсаалтаас өрөөнд хүн байгаа эсэхийг харж болж байв
        text = self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[1]/td[3]').text
        self.assertEqual(text, 'False')

        # Жагсаалтаас өрөөг сүүлд хэзээ цэвэрлэсэн гэдгийг харав
        text1 = self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[1]/td[4]').text
        self.assertEqual('Nov. 22, 2017, 9:10 p.m.', text1)
        # Жагсаалтын Цэвэрлэх товч дээр дарахад сүүлд цэвэрлэсэн огноо нь өөрчлөгдөв
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[1]/td[5]/a[1]').click()
        text2 = self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[1]/td[4]').text
        self.assertNotEqual(text1, text2)

        # Өөрчлөх товч дээр дарахад өрөөний мэдээллийг өөрчлөх форм гарч ирэв
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[1]/td[5]/a[2]').click()
        # Өрөөний мэдээллийг өөрчлөөд хадгалах товчийг дарав
        self.browser.find_element_by_id('id_room_name').clear()
        self.browser.find_element_by_id('id_room_name').send_keys('Room name new')
        self.browser.find_element_by_id('id_room_description').clear()
        self.browser.find_element_by_id('id_room_description').send_keys('Edited Text Edited Text Edited Text')
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('id_confirmation_button').click()
        # Өрөөний мэдээлэл амжилттай өөрчлөгдсөнийг шалгахын тулд захиалгын хуудсыг нээв
        self.browser.find_element_by_xpath('/html/body/div[1]/div/div/p').click()
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_xpath('/html/body/div[3]/div[3]/div/button[1]').click()
        # Өрөөний мэдээлэл өөрчлөгдсөн байгааг харав
        text_found = re.search(r'Deluxe', self.browser.page_source)
        self.assertEqual(text_found, None)
        text_found = re.search(r'Room name new', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'Edited Text Edited Text Edited Text', self.browser.page_source)
        self.assertNotEqual(text_found, None)

        # Өрөөг өөрчлөгдсөн байгааг хараад ажилтны хэсэгт буцаж оров
        url = self.live_server_url + '/employee'
        self.browser.get(url)
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('Rooms').click()
        # Шинээр өрөө нэмэхээр шийдээд шинэ өрөө товч дээр дарахад шинэ өрөө нэмэх форм гарч ирэв
        self.browser.find_element_by_link_text('NEW ROOM').click()
        self.browser.find_element_by_id('id_room_name').send_keys('Test Room')
        self.browser.find_element_by_id('id_room_description').send_keys('Test text')
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('id_confirmation_button').click()
        # Шинэ өрөө амжилттай нэмэгдсэнийг шалгахын тулд захиалгын хуудсыг нээв
        self.browser.find_element_by_xpath('/html/body/div[1]/div/div/p').click()
        self.browser.find_element_by_xpath('/html/body/div[3]/div[3]/div/button[1]').click()
        # Өрөөний мэдээлэл нэмэгдсэн байгааг харав
        text_found = re.search(r'Test Room', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'Test text', self.browser.page_source)
        self.assertNotEqual(text_found, None)

        url = self.live_server_url + '/employee'
        self.browser.get(url)
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('Rooms').click()
        #Өрөө устгах товч дээр дарахад өрөөний жагсаалтаас тухайн өрөө хасагдав
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[1]/td[5]/a[3]').click()
        text_found = re.search(r'Room name new', self.browser.page_source)
        self.assertEqual(text_found, None)
