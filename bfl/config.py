# B站视频监控配置

# 要监控的视频URL列表
VIDEO_URLS = [
    "https://www.bilibili.com/video/BV1xx411c7mu",  # 示例视频1
    "https://www.bilibili.com/video/BV1xx411c7mv",  # 示例视频2
    # 添加更多视频URL
]

# 监控参数
CHECK_INTERVAL_MINUTES = 10  # 检查间隔（分钟）
MONITOR_DURATION_HOURS = 24  # 监控时长（小时）

# 数据文件配置
DATA_FILENAME = "bilibili_data.csv"
CHART_FOLDER = "charts"  # 图表保存文件夹 