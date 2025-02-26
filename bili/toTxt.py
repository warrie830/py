
# 使用 Whisper 进行音频转文字

import whisper

model = whisper.load_model("base")  # 加载模型（可以选择不同大小的模型）
result = model.transcribe('audio.m4a')  # 输入音频文件路径
print(result['text'][:100])  # 只打印前 100 个字符



# # 保存为 .txt
# with open("output.txt", "w", encoding="utf-8") as f:
#     f.write(result['text'])


import opencc

# 初始化 OpenCC 转换器
converter = opencc.OpenCC('t2s')  # 't2s.json' 为简体转繁体（你也可以选择 's2t.json' 等）

# 将繁体字转为简体字
simplified_text = converter.convert(result['text'])

# 打印简体字结果
print(simplified_text[:100])

# 保存为简体字 txt 文件
with open("output_simplified.txt", "w", encoding="utf-8") as f:
    f.write(simplified_text)

