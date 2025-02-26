import yt_dlp

# 使用 youtube-dl 或者 yt-dlp（yt-dlp 是 youtube-dl 的一个分支，功能更强大）来下载视频的音频部分
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
download_audio('https://www.bilibili.com/video/BV1GJffY3Eu1')  # 替换为B站的视频链接

