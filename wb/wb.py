import requests
from bs4 import BeautifulSoup
import csv

# 目标用户微博主页链接
user_weibo_url = "https://weibo.com/Your_UserID"

# 构造带有 Cookies 的请求头
headers = {
    "User-Agent": "Your_User_Agent",
    # 添加 Cookies
    "Cookie": "Your_Cookies"
}
# 获取总页数
total_pages = 100  # 假设总页数为100，实际情况需要根据页面解析获取

# 循环访问每一页的微博内容
for page in range(1, total_pages + 1):
  # 发送带有 Cookies 的请求访问目标用户的微博主页
  response = requests.get(user_weibo_url, headers=headers)
  if response.status_code == 200:
      # 解析 HTML 获取微博内容等信息
      soup = BeautifulSoup(response.text, "html.parser")
      # 提取微博内容、发布时间、点赞数、转发数等信息
      # 根据实际页面结构进行解析
      # 这里以提取微博文本内容为例
      weibo_contents = soup.select(".WB_text")
      for content in weibo_contents:
          print(content.text)
      # 将爬取的数据保存为 CSV 文件
      with open("weibo_data.csv", "w", encoding="utf-8", newline="") as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(["Content", "Time", "Likes", "Reposts"])  # 写入表头
          # 循环遍历爬取到的微博内容等信息，写入 CSV 文件
          for content in weibo_contents:
              writer.writerow([content.text, "Time", "Likes", "Reposts"])  # 写入数据，时间、点赞数、转发数待补充
  else:
      print("Failed to fetch user's weibo page")