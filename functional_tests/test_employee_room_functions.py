from functional_tests.base import FunctionalTest


class RoomFunctionTest(FunctionalTest):

    def test_adding_new_rooms(self):
        # ажилтан Болд нэвтрэх эрхээрээ нэвтэрч оров
        url = self.live_server_url + '/login'
        self.browser.get(url)
        self.browser.find_element_by_id('id_username').send_keys('bold')
        self.browser.find_element_by_id('id_password').send_keys('CocaCola')
        self.browser.find_element_by_id('submit').click()

        # Өрөө гэсэн товч дээр дарахад яг одоогоор сул өрөөнүүд болон
        # өнөөдөр хүмүүс буудаллах өрөөг харуулна
        self.browser.find_element_by_link_text('Rooms').click()


        # Мөн сүүлд хүмүүс орсноос хойш өрөөнд цэвэрлэгээ орсон үгүйг тэмдэглэсэн байна.

        # Түвшин цэвэрлэгээ ороогүй өрөөг сонгож дарахад тухайн өрөөн статус цэвэрлэгдэж байгаа хэлбэрт шилжив.

        # Цэвэрлэж дуусаад Түвшин цэвэрлэж байгаа өрөөг дахин сонгоход цэвэрлэгдсэн хэлбэрт шилжив

    def test_room_status(self):
        pass
