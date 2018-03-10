from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class InitialTest(FunctionalTest):

    def test_initial_web_test(self):
        #Бат зочид буудлын талаар сонсоод вебсайтыг нь зочилхоор шийдэв
        #Анх орж үзэхэд вебийн title болон header-т тухайн вебийн нэр бичээстэй байхыг харав
        self.browser.get(self.live_server_url)
        self.assertIn('Hotel System', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Home', header_text)

        #Зочид буудлын талаар дэлгэрэнгүй мэдээллийг авснаар
        #онлайнаар захиалга өгч болохыг мэдээд захиалга өгөхөөр шийдэв.
        reservationbutton = self.browser.find_element_by_id('id_reservation_button')
        reservationbutton.click()
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Reservation', header_text)


        #Өөрийн буудаллах өдрийг сонгоход өрөөний сонголтууд гарч ирэв.
        chosendatebox = self.browser.find_element_by_id('id_date_box')
        chosendatebox.click()
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Choose Room', header_text)

        #Өрөөгөө сонгоод захиалах товчийг дарахад шинээр бүртгүүлэх эсвэл
        #утасны дугаараар шууд баталгаажуулалт хийх хуудас гарч ирэв.
        chosenroombox = self.browser.find_element_by_id('id_room_box')
        chosenroombox.click()
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Enter credentials', header_text)

        #Бат утасны дугаараа хийгээд баталгаажуулалтын товчийг дарахад
        #тухайн захиалга бүртгэгдэж. Захиалга амжилттай болсноор
        #захиалгын дугаар болон нууц кодыг тухайн хуудаст дүрсэлж
        #Мэдээллийн ажилтан дахин холбогдоно гэдгийг Бат-д мэдэгдэв.
        credentialsbutton = self.browser.find_element_by_id('id_confirmation_button')
        credentialsbutton.click()
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your reservation has been placed', header_text)
        #more status displayed under.


        #Бат захиалгаа өгч дуусаад захиалгаа шалгах товчийг дарснаар өөрийн захиалгийн статусыг харахад
        #Захиалга бүртгэгдсэн боловч баталгаажаагүйг харуулж байв
        self.browser.refresh()
        self.browser.get(self.live_server_url)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Home', header_text)


        checkbutton = self.browser.find_element_by_id('id_check_reservation_button')
        checkbutton.click()

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Reservation Check', header_text)

        #Мэдээллийн ажилтан/Систем Бат-тай утсаар/мэйл/СМС-ээр холбогдоод захиалгыг баталгаажуулсны
        #дараагаар Бат захиалгаа шалгахад батаалгажсан статустай болсон байна.





    #Бат бодлоо өөрчлөн шинээр бүртгэл үүсгэхээр шийдэж шинээр бүртгэл үүсгэх товчийг дарав

    #Өөрийн мэдээллийг оруулаад бүртгүүлэх товчийг дарахад бүртгэл баталгаажуулалтыг мэйл
    #хаягт явуулсныг мэдэгдэв.

    #Бат мэйл хаягаа шалгаад бүртгэлээ баталгаажуулах линк дээр дарахад бүртгэл нь баталгаажав.

    #Бат өөрийн бүртгэлийн хуудсаа харж үзэхэд өмнө захиалгаа хадаж болохыг анзаараад
    #өмнө хийсэн захиалгаа өөрийн шинэ бүртгэлдээ хадахаар шийдэж захиалгын код болон
    #нууц кодыг хийхэд бүртгэлд нь тухайн захиалга хадагдав.

    #Мөн өөр өдөр захиалга өгөхөөр шийдээд захиалга өгөв.

    #Өгсөн захиалгууд нь бүртгэгдсэн эсэхийг шалгахаар өөрийн бүртгэлийн хуудас-руу хандаж
    #үзэхэд захиалгууд нь байна.
