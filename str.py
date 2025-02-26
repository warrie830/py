with open("replies.txt", "r", encoding="utf-8") as f:
    content = f.readlines()

# 重新格式化，让每个回复单独换行
with open("replies_fixed.txt", "w", encoding="utf-8") as f:
    for line in content:
        f.write(line.strip() + "\n\n")  # 处理空格并加换行


import re

# 读取原始文件
with open("replies_fixed.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 1. 让 "。"、"？"、"！" 后换行，但 "。”"、"？”"、"！”" 不换行
formatted_content = re.sub(r'([。！？])(?![”’])', r'\1\n\n', content)

# 2. 在 "“"（左引号）前换行，避免影响 `。”` 这样的情况
formatted_content = re.sub(r'(?<!\n)(?=[“])', r'\n\n', formatted_content)

# 写入新文件
with open("replies_fixed_2.txt", "w", encoding="utf-8") as f:
    f.write(formatted_content)

print("处理完成，结果保存在 replies_fixed.txt")
