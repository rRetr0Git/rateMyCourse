import unittest
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
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
    def test_regist(self):
        self.driver.get("http://localhost:8000/")
        assert "主页 - 公课网" in self.driver.title
        Email = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1, 16))) + '@' + ''.join(
            random.sample(string.ascii_letters + string.digits, random.randint(2, 8))) + '.com'
        UserName = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(5, 16)))
        Password = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(5, 16)))
        print(Email, UserName, Password)
        self.driver.find_element_by_id("navLogin").click()
        self.driver.find_element_by_id("btnNewUser").click()
        RegistEmail = self.driver.find_element_by_id("inputEmail")
        RegistUsername = self.driver.find_element_by_id("inputUsername")
        RegistPassword = self.driver.find_element_by_id("inputPassword")
        RegistVerify = self.driver.find_element_by_id("inputVerify")
        time.sleep(1)
        RegistEmail.clear()
        RegistEmail.send_keys(Email)
        RegistUsername.send_keys(UserName)
        RegistPassword.send_keys(Password)
        RegistVerify.send_keys(Password)
        RegistEmail.send_keys(Keys.RETURN)

    # 在执行完各种测试用例方法之后会执行，为一个清理操作
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
