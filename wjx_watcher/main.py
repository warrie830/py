#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import logging
import schedule
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("wjx_watcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 配置
WJX_URL = os.getenv("WJX_URL", "https://www.wjx.cn/vm/xxx.aspx")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 10))
WXPUSHER_TOKEN = os.getenv("WXPUSHER_TOKEN", "")
WXPUSHER_UID = os.getenv("WXPUSHER_UID", "")

# WxPusher API 地址
WXPUSHER_API = "https://wxpusher.zjiecode.com/api/send/message"

# 存储上次检查时的答案数量
DATA_FILE = "last_count.json"


def save_data(data):
    """保存数据到文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def load_data():
    """从文件加载数据"""
    if not os.path.exists(DATA_FILE):
        return {"last_count": 0, "last_check": None}
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载数据文件失败: {e}")
        return {"last_count": 0, "last_check": None}


def get_response_count(url):
    """获取问卷星的回答数量"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 寻找包含回答数量的元素
        # 注意：问卷星可能会更新其页面结构，此处可能需要根据实际情况调整
        count_element = soup.select_one(".answerCount") or soup.select_one(".surveyCnt")
        
        if count_element:
            # 通常格式为"已收集x份答卷"
            text = count_element.text
            count = int(''.join(filter(str.isdigit, text)))
            return count
        else:
            logger.warning("未能找到回答数量元素，请检查问卷星页面结构是否有变化")
            return None
            
    except Exception as e:
        logger.error(f"获取问卷回答数量失败: {e}")
        return None


def send_wx_notification(title, content):
    """发送微信通知"""
    if not WXPUSHER_TOKEN or not WXPUSHER_UID:
        logger.warning("微信推送配置不完整，请检查环境变量")
        return False
    
    try:
        # 使用 requests 直接调用 WxPusher API
        data = {
            "appToken": WXPUSHER_TOKEN,
            "content": content,
            "summary": title,
            "contentType": 1,  # 1 表示文本
            "uids": [WXPUSHER_UID]
        }
        
        response = requests.post(WXPUSHER_API, json=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get("success"):
            logger.info("微信推送成功")
            return True
        else:
            logger.error(f"微信推送失败: {result.get('msg')}")
            return False
    except Exception as e:
        logger.error(f"微信推送失败: {e}")
        return False


def check_wjx():
    """检查问卷星是否有新回答"""
    logger.info(f"开始检查问卷: {WJX_URL}")
    
    # 加载上次检查的数据
    data = load_data()
    last_count = data["last_count"]
    
    # 获取当前回答数量
    current_count = get_response_count(WJX_URL)
    
    if current_count is None:
        logger.error("获取回答数量失败，跳过本次检查")
        return
    
    # 更新检查时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["last_check"] = now
    
    # 检查是否有新回答
    if current_count > last_count:
        new_answers = current_count - last_count
        logger.info(f"检测到 {new_answers} 份新回答！总计: {current_count}")
        
        # 发送微信通知
        title = "问卷星有新回答！"
        content = f"您的问卷有 {new_answers} 份新回答！\n当前总计回答数: {current_count}\n检查时间: {now}\n问卷链接: {WJX_URL}"
        send_wx_notification(title, content)
        
        # 更新最后的回答数量
        data["last_count"] = current_count
    else:
        logger.info(f"没有新回答。当前回答数: {current_count}")
    
    # 保存数据
    save_data(data)


def main():
    """主函数"""
    logger.info("问卷星监控程序启动")
    logger.info(f"问卷URL: {WJX_URL}")
    logger.info(f"检查间隔: {CHECK_INTERVAL}分钟")
    
    # 首次运行立即检查
    check_wjx()
    
    # 定时检查
    schedule.every(CHECK_INTERVAL).minutes.do(check_wjx)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
    finally:
        logger.info("问卷星监控程序已停止")


if __name__ == "__main__":
    main() 