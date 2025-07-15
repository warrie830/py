from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://www.wjx.cn/wjx/activitystat/viewstatsummary.aspx?activity=314729177&sat=1")  # 登录后答卷页面 URL
# 登录部分要手动或用 cookies 注入，略

# 找到包含“共 112 条”的元素
text = driver.find_element("xpath", "//div[contains(text(),'共')]").text
print(text)  # 解析出数字

driver.quit()