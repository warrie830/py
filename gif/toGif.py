from moviepy.editor import VideoFileClip

def video_to_gif(video_path, gif_path, start_time=0, end_time=None):
    # 加载视频文件
    clip = VideoFileClip(video_path)
    
    # 如果指定了时间段，就裁剪视频
    if end_time:
        clip = clip.subclip(start_time, end_time)
    else:
        clip = clip.subclip(start_time)
    
    # 写入GIF文件
    clip.write_gif(gif_path)

# 示例调用
video_to_gif('lv_0_20250224101533.mp4', 'lv_0_20250213092538.gif')
