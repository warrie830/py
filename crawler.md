### 内部库

操作 url
urllib

- 请求

```
import urllib.request
# 打开一个URL地址
file = urllib.request.urlopen('http://www.baidu.com')
# 读取内容
data=file.read()
dataline= file.readline()
datalines= file.readlines()
```

- 保存

```
# 读取网页并存到变量
# 以写入的方式打开一个文件，命名为test.html
# 讲变量写入该文件
# 关闭文件
fhandle=open("./1.html","wb")
fhandle.write(data)
fhandle.close()

# 读取网页并保存到本地
import urllib.request
urlib.request.urlretrieve("http://www.baidu.com",filename="./1.html")
# 清除缓存
urllib.request.urlcleanup()
```

- 查看信息

```
# 读取的网页可以查看信息
file.info()
file.getCode()
file.getUrl()
```

- url 编码

```
urllib.request.quote()
urllib.request.unquote()
```

- header

```
# urlopen是初级的方法，高级的方法是build_opener
url="https://blog.csdn.net/wolinxuebin/article/details/7615098"
headers=("user-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
opener=urllib.request.build_opener()
opener.addheaders=[headers]
data=opener.open(url).read()

# 或者创建一个Request对象
req=urllib.request.Request(url)
req.add_header(headers[0],headers[1])
data=urllib.request.urlopen(req).read()
```

- 错误处理

```
try:
  file=urllib.request.urlopen(url, timeout=1)
  data=file.read()
except Exception as e:
  print("异常" +str(e))
```

- http

```
postdata=urllib.parse.urlencode(values).encode('utf-8')
req=urllib.request.Request(url,postdata)
```

- 代理服务器
```
def use_proxy(url, proxy_addr):
  proxy=urllib.request.ProxyHandler({'http':proxy_addr})
  opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
  urllib.request.install_opener(opener)
  data=urllib.request.urlopen(url).read().decode('utf-8')
  # data=opener.open(url).read().decode('utf-8')
  return data
```

- debuglog
```
httphd=urllib.request.HTTPHandler(debuglevel=1)
```

- 异常处理
```
import urllib.error
import urllib.request
try:
  urllib.request.urlopen(url)
except urllib.error.URLError as e:
  if hasattr(e,"code"):
    print(e.code)
  if hasattr(e,"reason"):
    print(e.reason)
```
