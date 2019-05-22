import unittest
from selenium import webdriver
import time

class rateMyCourseCase(unittest.TestCase):
    # initialize
    def setUp(self):
        self.driver = webdriver.Edge()
        #self.host = "http://127.0.0.1:8000/" # for develop version
        self.host = "http://114.116.51.151/" # for release version

    # testcase methods
    def return2home(self):
        body = self.driver.find_element_by_tag_name('body')
        bar = body.find_element_by_class_name('navbar navbar-expand-md navbar-dark bg-primary fixed-top')
        print(bar)
        con = bar.find_element_by_class_name('container')
        print(con)
        bts = con.find_elements_by_class_name('navbar-brand')
        bts[0].click()
        time.sleep(3)
        print("# Return to homepage")    

    def test_rank(self):
        self.driver.get(self.host)
        time.sleep(3)
        body = self.driver.find_element_by_tag_name('body')
        bar = body.find_element_by_class_name('navbar navbar-expand-md navbar-dark bg-primary fixed-top')
        print(bar)
        con = bar.find_element_by_class_name('container')
        print(con)
        bts = con.find_elements_by_class_name('navbar-brand')
        bts[1].click()
        time.sleep(3)


    def test_searchCourse_home(self):
        self.driver.get(self.host)
        time.sleep(3)
        e10 = self.driver.find_element_by_id("buttonSelectSchool")
        print(e10)
        e10.click()
        e11 = self.driver.find_element_by_id("schoolList")
        print(e11)
        e11.click()
        time.sleep(3)

        e20 = self.driver.find_element_by_id("buttonSelectDepartment")
        e20.click()
        e21 = self.driver.find_element_by_id("departmentList")
        e21s = e21.find_elements_by_tag_name('a')
        print(len(e21s))
        e21s[0].click() # change department by changing the index
        # if raise exception, try adjusting the zoom level
        time.sleep(3)

        e30 = self.driver.find_element_by_id("buttonSearchCourse")
        e30.click()
        e31 = self.driver.find_element_by_id("searchboxCourse")
        e31.send_keys('\n') # you can modify the keywords
        time.sleep(6)

    def test_searchCourse_res(self):
        # append represents a query, feel free to modify it
        append = "search/?school=北京航空航天大学&department=计算机学院&keywords="
        
        self.driver.get(self.host + append)
        time.sleep(3)
        ein = self.driver.find_element_by_id("searchCourse")
        ein.clear()
        ein.send_keys("大数据\n")
        time.sleep(3)
        self.return2home()
        
    def test_rank2course(self):
        append = "rank/"
        self.driver.get(self.host + append)
        time.sleep(3)
        ein = self.driver.find_elements_by_id('radio')
        print(len(ein)) # 2 modes
        ein[1].click()
        time.sleep(3)
    
    # run after all testcases
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
