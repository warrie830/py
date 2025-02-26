import urllib.request
# 打开一个URL地址
file = urllib.request.urlopen('http://www.baidu.com')
# 读取内容
data=file.read()
dataline= file.readline()

# print(data)

# fhandle=open("./1.html","wb")
# fhandle.write(data)
# fhandle.close()

urllib.request.urlretrieve("http://www.baidu.com",filename="./1.html")