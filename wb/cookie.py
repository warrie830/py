import time
from selenium import webdriver

# 启动浏览器
driver = webdriver.Chrome()

# 打开微博登录页面
driver.get("https://passport.weibo.cn/signin/login")

# 输入用户名和密码
driver.find_element_by_id("loginName").send_keys("Your_Username")
driver.find_element_by_id("loginPassword").send_keys("Your_Password")

# 点击登录按钮
driver.find_element_by_id("loginAction").click()

# 等待一段时间，确保登录成功并获取 Cookies
time.sleep(10)

# 获取 Cookies
cookies = driver.get_cookies()

# 关闭浏览器
driver.quit()

# 打印 Cookies
print(cookies)