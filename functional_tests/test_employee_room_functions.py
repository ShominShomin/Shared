from functional_tests.base import FunctionalTest
import re
from datetime import datetime
from django.utils import timezone
import time


class RoomFunctionTest(FunctionalTest):

    def test_adding_new_rooms(self):
        # ажилтан Болд нэвтрэх эрхээрээ нэвтэрч оров
        url = self.live_server_url + '/login'
        self.browser.get(url)
        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')
        self.browser.find_element_by_id('submit').click()

        # Өрөө гэсэн товч дээр дарахад өрөөнүүдийнг жагсаалт дүрслэгдэв.
        self.browser.find_element_by_link_text('Rooms').click()
        text_found = re.search(r'Deluxe', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'Combo', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        #Тухайн жагсаалтаас өрөөнд хүн байгаа эсэхийг харж болж байв.

