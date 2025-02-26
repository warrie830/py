import requests
from bs4 import BeautifulSoup
import time

# 设置请求头，模拟正常浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

# 使用你的cookie
cookies = {
    'bid': 'rVcZAlYN-wM',
    'douban-fav-remind': '1',
    '_pk_id.100001.8cb4': 'cf5863a26a4ceec0.1736238884.',
    '__yadk_uid': 'UgFSUZjOiGVPwRnxHIoByRoGcTYYdJDx',
    'dbcl2': '65371004:iGGN7h5vE6Y',
    'ck': 'nW6w',
    '_pk_ref.100001.8cb4': '[%22%22,%22%22,1740041874,%22https%3A%2F%2Faccounts.douban.com%2F%22]',
    '_pk_ses.100001.8cb4': '1',
    'SL_G_WPT_TO': 'en',
    'push_noty_num': '0',
    'push_doumail_num': '0',
    '__utma': '30149280.1394625244.1720776007.1736238885.1740041875.3',
    '__utmc': '30149280',
    '__utmz': '30149280.1740041875.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
    '__utmt': '1',
    '__utmv': '30149280.6537',
    'SL_GWPT_Show_Hide_tmp': '1',
    'SL_wptGlobTipTmp': '1',
    'RT': 'nu=https%3A%2F%2Fwww.douban.com%2Fgroup%2Ftopic%2F319428740%2F%3F_spm_id%3DMjUyNjc3NDcw&cl=1740041886804&r=https%3A%2F%2Fwww.douban.com%2Fgroup%2F718202%2F&ul=1740041886806&hd=1740041887499',
    '__utmb': '30149280.16.5.1740041888139'
}



# 每页评论数量
comments_per_page = 100

# 翻页的起始位置
start = 0

# 爬取某个豆瓣小组帖子的所有回复
def crawl_douban_post(post_url: str, output_filename: str, start=0):
    
    # 创建 Session 对象
    session = requests.Session()
    session.headers.update(headers)

    # 发送请求获取页面内容
    response = session.get(post_url, cookies=cookies)
    if response.status_code != 200:
        print("请求失败！")
        print(response.status_code)  # 打印 HTTP 状态码
        return False
    


    # 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到所有回复
    replies = soup.find_all('div', class_='reply-content')

    if not replies:
      print("没有找到评论，可能已经是最后一页了。")
      return False

    # 打开文件并写入内容
    with open(output_filename, 'a', encoding='utf-8') as file:
        for idx, reply in enumerate(replies, start=1):
            # 获取每个回复的文本内容
            reply_text = reply.get_text(strip=True)
            
            # 如果回复不为空，则写入文件
            if reply_text:
                file.write(f"回复 {start+idx}:\n")
                file.write(f"{reply_text}\n\n")  # 每个回复之间空一行
                # time.sleep(1)  # 为了避免过于频繁的请求，可以加个延迟

    print(f"已将所有回复保存到 {output_filename} 中！")
    return True

# 输入豆瓣小组帖子的 URL 和输出的文件名
post_url = 'https://www.douban.com/group/topic/319428740'  # 替换为你需要抓取的帖子 URL
output_filename = 'db.txt'

while True:
  # 构建翻页 URL
  url = f'{post_url}?start={start}'
  # 开始爬取
  res = crawl_douban_post(url, output_filename ,start)
  if not res:
    break
  # 更新起始位置，获取下一页
  start += comments_per_page
