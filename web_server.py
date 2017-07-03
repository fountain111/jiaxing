from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# 模拟登陆163邮箱
driver = webdriver.Firefox()
driver.get("http://mail.163.com/")

# 用户名 密码
elem_user = driver.find_element_by_name("username")
elem_user.send_keys("15201615157")
elem_pwd = driver.find_element_by_name("password")
elem_pwd.send_keys("********")
elem_pwd.send_keys(Keys.RETURN)
time.sleep(5)
assert "baidu" in driver.title
driver.close()
driver.quit()