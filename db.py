import requests
from bs4 import BeautifulSoup
import time

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# 发送 HTTP 请求获取页面内容
def fetch_page(url):
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch page, status code: {response.status_code}")
        return None

# 解析页面内容，提取回复内容
def extract_replies(html):
    soup = BeautifulSoup(html, 'html.parser')
    replies = []
    # 以此处为例，使用 BeautifulSoup 提取回复内容
    # 根据实际情况修改提取规则
    reply_elements = soup.select('.reply-content')
    for reply_element in reply_elements:
        reply_text = reply_element.get_text().strip()
        replies.append(reply_text)
    return replies

# 将回复内容写入文件，并添加分隔线
def write_replies_to_file(replies, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for reply in replies:
            f.write(reply + '\n')
            f.write('-' * 30 + '\n')

# 解析页面内容，提取总页码
def extract_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 以此处为例，使用 BeautifulSoup 提取总页码
    # 根据实际情况修改提取规则
    pagination = soup.find('div', class_='paginator')
    if pagination:
        page_links = pagination.find_all('a', class_='paginator__page')
        if page_links:
            # 最后一个页码即为总页码
            total_pages = int(page_links[-1].get_text())
            return total_pages
    return None

# 获取豆瓣帖子的总页码
def get_total_pages(group_url):
    html = fetch_page(group_url)
    if html:
        total_pages = extract_total_pages(html)
        if total_pages:
            return total_pages
        else:
            print("Failed to extract total pages")
    else:
        print("Failed to fetch page")
    return None

# 获取页面标题
def get_page_title(url):
    html = fetch_page(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string
        return title
    else:
        print("Failed to fetch page")
        return None

# 给一个帖子id，返回这个帖子的所有回复
def get_all_replies(id,interval_seconds=60,filename='replies.txt'):
    group_url = f'https://www.douban.com/group/topic/{id}/'  # 替换成你要爬取的小组帖子链接
    interval_seconds = 60  # 定时爬取间隔，单位为秒
    # 获取标题名作为文件名

    filename = get_page_title(group_url) + '.txt'
    
    total_pages = get_total_pages(group_url)
    if total_pages:
        replies = []
        for page in range(1, total_pages + 1):
            page_url = f"{group_url}?start={page * 100}"
            html = fetch_page(page_url)
            if html:
                page_replies = extract_replies(html)
                replies.extend(page_replies)
            else:
                print(f"Failed to fetch page {page}")
        return replies
    else:
        return None

# 主程序，定时爬取回复内容
def main():
    group_url = 'https://www.douban.com/group/topic/304994211/?start=1700'  # 替换成你要爬取的小组帖子链接
    interval_seconds = 60  # 定时爬取间隔，单位为秒
    filename = 'replies.txt'

    # 读取已有的回复内容
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            existing_replies = f.read().split('-' * 30)
            # 去除末尾的空行
            existing_replies = [reply.strip() for reply in existing_replies if reply.strip()]
    except FileNotFoundError:
        existing_replies = []

    while True:
        # 发送 HTTP 请求获取页面内容
        html = fetch_page(group_url)
        if html:
            # 解析页面内容，提取回复内容
            replies = extract_replies(html)
            # 获取新增的回复内容
            new_replies = [reply for reply in replies if reply not in existing_replies]
            # print(replies)  # 输出回复内容
            # write_replies_to_file(replies, 'replies.txt')
            if new_replies:
                # 将新增的回复内容写入文件，并添加分隔线
                write_replies_to_file(new_replies, filename)
                # 更新已有的回复内容列表
                existing_replies.extend(new_replies)
        else:
            print("Failed to fetch page")

        # 间隔一段时间后再次爬取
        time.sleep(interval_seconds)

if __name__ == "__main__":
    main()