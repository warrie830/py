from google.cloud import speech
import io

client = speech.SpeechClient()

# 音频文件路径
file_name = "audio.m4a"

with io.open(file_name, "rb") as audio_file:
    content = audio_file.read()

# 设置音频识别参数
audio = speech.RecognitionAudio(content=content)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="zh-CN",  # 支持中文
)

# 调用 Google 语音识别 API
response = client.recognize(config=config, audio=audio)

for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))
