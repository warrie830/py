
import requests
import re
import csv
from datetime import datetime
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

def get_bvid(url):
    """提取视频的BV号"""
    pattern = r"video/(BV[0-9A-Za-z]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_data(bvid):
    """通过B站API获取视频数据"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.bilibili.com/"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        data = json_data["data"]
        
        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": data["title"],
            "view": data["stat"]["view"],      # 播放量
            "like": data["stat"]["like"],      # 点赞
            "favorite": data["stat"]["favorite"],  # 收藏
            "coin": data["stat"]["coin"],      # 投币
            "bvid": bvid
        }
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None

def save_to_csv(data_list, filename="bilibili_data.csv"):
    """保存数据到CSV文件"""
    file_exists = os.path.exists(filename)
    
    with open(filename, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["time", "title", "bvid", "view", "like", "favorite", "coin"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for data in data_list:
            if data:
                writer.writerow(data)
    
    print(f"数据已保存到 {filename}")

def generate_charts(filename="bilibili_data.csv"):
    """生成数据图表并保存"""
    df = pd.read_csv(filename, parse_dates=["time"])
    
    if df.empty:
        print("无可用数据生成图表")
        return
    
    # 为每个视频单独生成图表
    for bvid in df["bvid"].unique():
        video_df = df[df["bvid"] == bvid]
        video_title = video_df["title"].iloc[0][:20] + "..."  # 截取标题前20个字符
        
        plt.figure(figsize=(14, 8))
        
        # 播放量图表
        plt.subplot(2, 2, 1)
        plt.plot(video_df["time"], video_df["view"], "b-")
        plt.title(f"播放量趋势 - {video_title}")
        plt.xlabel("时间")
        plt.ylabel("播放量")
        plt.xticks(rotation=15)
        
        # 点赞/收藏/投币图表
        plt.subplot(2, 2, 2)
        plt.plot(video_df["time"], video_df["like"], "g-", label="点赞")
        plt.plot(video_df["time"], video_df["favorite"], "r-", label="收藏")
        plt.plot(video_df["time"], video_df["coin"], "y-", label="投币")
        plt.title(f"互动数据 - {video_title}")
        plt.xlabel("时间")
        plt.ylabel("数量")
        plt.xticks(rotation=15)
        plt.legend()
        
        # 各指标关系图表
        plt.subplot(2, 1, 2)
        metrics = ["view", "like", "favorite", "coin"]
        corr = video_df[metrics].corr()
        plt.imshow(corr, cmap="coolwarm", interpolation="nearest")
        plt.colorbar()
        plt.title(f"指标相关性 - {video_title}")
        plt.xticks(range(len(metrics)), metrics)
        plt.yticks(range(len(metrics)), metrics)
        
        plt.tight_layout()
        plt.savefig(f"chart_{bvid}.png")
        print(f"已生成图表: chart_{bvid}.png")

def monitor_videos(video_urls, interval_minutes=10, duration_hours=24):
    """定时监控视频数据"""
    end_time = time.time() + duration_hours * 3600
    
    print(f"开始监控{len(video_urls)}个视频，每{interval_minutes}分钟采集一次数据...")
    
    while time.time() < end_time:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(get_bvid, video_urls))
            bvids = [bvid for bvid in results if bvid]
        
        with ThreadPoolExecutor() as executor:
            data_list = list(executor.map(get_video_data, bvids))
        
        save_to_csv(data_list)
        
        # 每3次收集生成一次图表，避免过于频繁
        if int(time.time() - start_time) // (interval_minutes * 60) % 3 == 0:
            generate_charts()
        
        print(f"下次采集时间: {datetime.fromtimestamp(time.time() + interval_minutes * 60)}")
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    # 用户输入视频URL（逗号分隔）
    input_urls = input("请输入B站视频地址（多个地址用逗号分隔）: ")
    video_urls = [url.strip() for url in input_urls.split(",") if url.strip()]
    
    # 设置监控参数
    interval = int(input("采集间隔（分钟）: ") or 10)
    duration = int(input("监控时长（小时）: ") or 24)
    
    start_time = time.time()
    monitor_videos(video_urls, interval_minutes=interval, duration_hours=duration)