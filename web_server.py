from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# 模拟登陆163邮箱
driver = webdriver.Firefox()
driver.get("http://61.164.40.59:8888/")
time.sleep(2)

# 用户名 密码
elem_user = driver.find_element_by_id('userAccount')
elem_user.send_keys("2511")
elem_pwd = driver.find_element_by_id("userPassword")
elem_pwd.send_keys("Hcxt123321")
elem_pwd.send_keys(Keys.RETURN)
time.sleep(5)
driver.get( 'http://61.164.40.59:8888/hroa/com/travel/apply/frame.htm')
time.sleep(2)
driver.execute_script("document.getElementsByClassName('ui-button ui-button-sorange ')[0].click()")

time.sleep(5)

driver.close()
driver.quit()