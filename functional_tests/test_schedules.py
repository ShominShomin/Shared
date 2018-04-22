from functional_tests.base import FunctionalTest
from functional_tests.wait import wait_for_page_load
import re
from core.models import Schedule
import datetime

class ScheduleTest(FunctionalTest):

    def test_schedules(self):
        Schedule.objects.create(event="Morning", start_time=datetime.time(8, 0), end_time=datetime.time(10, 0))
        Schedule.objects.create(event="Noon", start_time=datetime.time(11, 0), end_time=datetime.time(13, 0))

        # Ажилтан Болд нэвтрэх эрхээрээ нэвтэрч оров
        url = self.live_server_url + '/accounts/login'
        self.browser.get(url)
        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('submit').click()

        # Хувиар гэсэн товч дээр дарахад өдрийн хувиар дүрслэгдэв
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('Schedule').click()
        text_found = re.search(r'Morning', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'Noon', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'08:00', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'10:00', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'11:00', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'13:00', self.browser.page_source)
        self.assertNotEqual(text_found, None)

        # Өөрчлөх товч дээр дарахад хувиар өөрчлөх форм гарч ирэв
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[1]/td[4]/a[1]').click()
        # Мэдээллийг өөрчлөөд хадгалах товчийг дарав
        self.browser.find_element_by_id('id_event').clear()
        self.browser.find_element_by_id('id_event').send_keys('Event edit')
        self.browser.find_element_by_id('id_start_time').clear()
        self.browser.find_element_by_id('id_start_time').send_keys('09:53')
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('id_confirmation_button').click()

        # Нүүр хуудсаас хувиар өөрчлөгдсөн байгааг харав
        self.browser.get(self.live_server_url)
        text_found = re.search(r'Morning', self.browser.page_source)
        self.assertEqual(text_found, None)
        text_found = re.search(r'Noon', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'Event edit', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'08:00 - 10:00', self.browser.page_source)
        self.assertEqual(text_found, None)
        text_found = re.search(r'09:53 - 10:00', self.browser.page_source)
        self.assertNotEqual(text_found, None)

        # Хувиар өөрчлөгдсөн байгааг хараад ажилтны хэсэгт буцаж оров
        url = self.live_server_url + '/employee'
        self.browser.get(url)
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('Schedule').click()
        # Шинэ хувиар товч дээр дарахад шинэ өрөө нэмэх форм гарч ирэв
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('NEW SCHEDULE').click()
        self.browser.find_element_by_id('id_event').send_keys('Evening')
        self.browser.find_element_by_id('id_start_time').send_keys('17:30')
        self.browser.find_element_by_id('id_end_time').send_keys('19:30')
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_id('id_confirmation_button').click()

        # Шинэ өрөөг нэмэхэд өрөөний мэдээлэл жагсаалтад нэмэгдсэн байгааг харав
        text_found = re.search(r'Evening', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'17:30', self.browser.page_source)
        self.assertNotEqual(text_found, None)
        text_found = re.search(r'19:30', self.browser.page_source)
        self.assertNotEqual(text_found, None)

        #Өрөө устгах товч дээр дарахад өрөөний жагсаалтаас тухайн өрөө хасагдав
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[1]/td[4]/a[2]').click()
        text_found = re.search(r'Event edit', self.browser.page_source)
        self.assertEqual(text_found, None)
