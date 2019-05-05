import unittest
from selenium import webdriver
import time

class rateMyCourseCase(unittest.TestCase):
    # initialize
    def setUp(self):
        self.driver = webdriver.Edge()

    # testcase methods (must begin with 'test')
    def test_rank(self):
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(3)
        body = self.driver.find_element_by_tag_name('body')
        bar = body.find_element_by_class_name('navbar navbar-expand-md navbar-dark bg-primary fixed-top')
        print(bar)
        con = bar.find_element_by_class_name('container')
        print(con)
        bts = con.find_elements_by_class_name('navbar-brand')
        bts[1].click()
        time.sleep(3)

    def test_searchCourse_res(self):
        strdev = "http://127.0.0.1:8000/"
        append = "search/?school=北京航空航天大学&department=计算机学院&keywords="
        self.driver.get(strdev + append)
        time.sleep(3)
        ein = self.driver.find_element_by_id("searchCourse")
        ein.clear()
        ein.send_keys("大数据")
        time.sleep(3)

    # run after all testcases
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
