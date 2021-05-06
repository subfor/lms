from time import sleep

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from academy.models import Student, Group, Lecturer


class SeleniumTest(StaticLiveServerTestCase):
    NUMBER_OF_STUDENT = 10
    NUMBER_OF_GROUP = 10

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser('admin', 'adminl@test.com', 'admin')
        self.first_name = "Jhon"
        self.last_name = "Doe"
        self.email = "jdoe@fdsdf.com"
        self.photo = "photo/default.png"

        for number in range(self.NUMBER_OF_GROUP):
            self.group = Group.objects.create(course="Python",
                                              group_name=f"test_group{number}"
                                              )
            self.lecturer = Lecturer.objects.create(first_name=self.first_name,
                                                    last_name=self.last_name,
                                                    email=self.email,
                                                    photo=self.photo,
                                                    )
            self.group.teachers.add(self.lecturer)
            for _ in range(self.NUMBER_OF_STUDENT):
                self.student = Student.objects.create(first_name=self.first_name,
                                                      last_name=self.last_name,
                                                      email=self.email,
                                                      photo=self.photo
                                                      )
                self.group.students.add(self.student)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_unsuccessful_login(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_xpath('//*[local-name()="svg"][@style="fill: white"]')
        login_url.click()
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('test')

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('test')

        submit_btn = self.selenium.find_element_by_xpath('//input[@type="submit" and @value="login"]')
        submit_btn.submit()

        error = self.selenium.find_element_by_id('error')
        expected_error = "Your username and password didn't match. Please try again."
        self.assertEqual(error.text, expected_error)

    def test_check_students_pagination(self):
        self.selenium.get(self.live_server_url)

        students_menu_link = self.selenium.find_elements_by_tag_name('a')[1]
        students_menu_link.click()

        pagination = self.selenium.find_element_by_class_name('pagination')

        self.assertTrue(bool(pagination))

    def test_successful_login(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_xpath('//*[local-name()="svg"][@style="fill: white"]')
        login_url.click()
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('admin')

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('admin')

        submit_btn = self.selenium.find_element_by_xpath('//input[@type="submit" and @value="login"]')
        submit_btn.submit()
        sleep(1)
        name = self.selenium.find_element_by_id('login_name')
        expected_name = "admin"
        self.assertEqual(name.text, expected_name)

    def test_add_student_button_check_for_admins(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_xpath('//*[local-name()="svg"][@style="fill: white"]')
        login_url.click()
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('admin')

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('admin')

        submit_btn = self.selenium.find_element_by_xpath('//input[@type="submit" and @value="login"]')
        submit_btn.submit()
        sleep(1)
        menu_button_name = self.selenium.find_elements_by_tag_name('a')[4].text
        expected_menu_button_name = "Add Student"
        self.assertEqual(menu_button_name, expected_menu_button_name)

    def test_successful_logout(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_xpath('//*[local-name()="svg"][@style="fill: white"]')
        login_url.click()
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('admin')

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('admin')

        submit_btn = self.selenium.find_element_by_xpath('//input[@type="submit" and @value="login"]')
        submit_btn.submit()

        logout_url = self.selenium.find_element_by_xpath(
            '//*[local-name()="svg"][@style="fill: white; margin-left: 12px;"]')
        logout_url.click()

        lms_name = self.selenium.find_element_by_tag_name('h1').text
        expected_lms_name = 'LMS'
        self.assertEqual(lms_name, expected_lms_name)

    def test_successful_add_student(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_xpath('//*[local-name()="svg"][@style="fill: white"]')
        login_url.click()
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('admin')

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('admin')

        submit_btn = self.selenium.find_element_by_xpath('//input[@type="submit" and @value="login"]')
        submit_btn.submit()
        sleep(1)
        menu_button_add_student = self.selenium.find_elements_by_tag_name('a')[4]
        menu_button_add_student.click()

        first_name_input = self.selenium.find_element_by_name('first_name')
        first_name_input.send_keys('Bob')
        last_name_input = self.selenium.find_element_by_name('last_name')
        last_name_input.send_keys('Dylan')
        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys('bob.dylan@email.com')

        submit_btn = self.selenium.find_element_by_xpath('//input[@type="submit" and @value="Add student"]')
        submit_btn.submit()
        sleep(1)
        message = self.selenium.find_element_by_id('success_message')
        expected_message = "Student Bob Dylan successfully added to LMS"
        self.assertEqual(message.text, expected_message)
