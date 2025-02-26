import requests
from bs4 import BeautifulSoup
import time

# 目标帖子 URL（你可以换成你要爬取的帖子）
BASE_URL = "https://tieba.baidu.com/p/971192275"

# 请求头（模拟浏览器访问）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# 爬取帖子回复
def fetch_replies(post_url):
    page = 1
    all_replies = []
    
    while True:
        url = f"{post_url}?pn={page}"
        print(f"正在爬取第 {page} 页: {url}")
        
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")

        # 提取所有回复
        replies = soup.find_all("div", class_="d_post_content j_d_post_content")  # 贴吧的回复内容
        
        if not replies:
            print("没有找到更多的回复，爬取结束。")
            break

        for reply in replies:
            text = reply.get_text(strip=True)
            all_replies.append(text)
        
        # 判断是否有下一页
        next_page = soup.find("a", text="下一页")
        if not next_page:
            print("已经到最后一页，爬取结束。")
            break

        page += 1
        time.sleep(2)  # 防止爬取太快被封

    return all_replies

if __name__ == "__main__":
    replies = fetch_replies(BASE_URL)
    
    # 保存到文件
    with open("replies.txt", "w", encoding="utf-8") as f:
        for idx, reply in enumerate(replies, 1):
            f.write(f"【{idx}】{reply}\n")
    
    print(f"共爬取 {len(replies)} 条回复，并保存到 replies.txt")
