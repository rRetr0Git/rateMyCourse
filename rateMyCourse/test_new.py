import unittest
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import random
import string
import time


# 继承至TestCase，表示这是一个测试用例类
class rateMyCourseCase(unittest.TestCase):
    # 初始化的一部分
    def setUp(self):
        self.driver = Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    # 测试用例方法，名称可以自定义，方法名称始终以test开头
    # 随机账户密码注册登陆
    def regist(self):
        self.driver.get("http://localhost:8000/")
        assert "主页 - 公课网" in self.driver.title
        time.sleep(1)
        Email = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1, 16))) + '@' + ''.join(
            random.sample(string.ascii_letters + string.digits, random.randint(2, 8))) + '.com'
        UserName = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(5, 16)))
        Password = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(5, 16)))
        self.driver.find_element_by_id("navLogin").click()
        time.sleep(1)
        self.driver.find_element_by_id("btnNewUser").click()
        RegistEmail = self.driver.find_element_by_id("inputEmail")
        RegistUsername = self.driver.find_element_by_id("inputUsername")
        RegistPassword = self.driver.find_element_by_id("inputPassword")
        RegistVerify = self.driver.find_element_by_id("inputVerify")
        RegistEmail.clear()
        RegistEmail.send_keys(Email)
        RegistUsername.send_keys(UserName)
        RegistPassword.send_keys(Password)
        RegistVerify.send_keys(Password)
        RegistEmail.send_keys(Keys.RETURN)
        time.sleep(1)
        assert UserName in self.driver.page_source

    def test_comment(self):
        self.regist()
        self.driver.find_element_by_id("buttonSelectSchool").click()
        assert "北京航空航天大学" in self.driver.page_source
        self.driver.find_element_by_xpath("//a[text()='北京航空航天大学']").click()
        self.driver.find_element_by_id("buttonSelectDepartment").click()
        self.driver.find_element_by_xpath("//a[text()='计算机学院']").click()
        self.driver.find_element_by_xpath("//a[text()='搜索课程']").click()
        self.driver.find_element_by_id("searchboxCourse").send_keys('数据')
        self.driver.find_element_by_id("searchboxCourse").send_keys(Keys.RETURN)
        time.sleep(1)
        assert "大数据与人工智能实训" in self.driver.page_source
        assert "大数据科学导论" in self.driver.page_source
        assert "大数据分析" in self.driver.page_source
        assert "数据挖据导论" in self.driver.page_source
        assert "数据库原理课程设计" in self.driver.page_source
        self.driver.find_element_by_xpath("//a[text()='大数据科学导论']").click()
        self.driver.find_element_by_xpath("//a[text()='撰写评价']").click()
        self.driver.find_element_by_id("B14").click()
        self.driver.find_element_by_id("B21").click()
        self.driver.find_element_by_id("B32").click()
        self.driver.find_element_by_id("B45").click()
        commentText = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(16, 128)))
        self.driver.find_element_by_id("writeCommentText").send_keys(commentText)
        time.sleep(1)


    # 在执行完各种测试用例方法之后会执行，为一个清理操作
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
