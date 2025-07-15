# 问卷星监控与微信推送

这个程序可以监控问卷星的问卷，当有新回答时，会通过微信推送通知给您。

## 安装

1. 安装依赖包：

```
pip install -r requirements.txt
```

2. 配置 `.env` 文件：

```
WJX_URL=https://www.wjx.cn/vm/您的问卷ID.aspx
WXPUSHER_TOKEN=您的WxPusher的APP_TOKEN
WXPUSHER_UID=您的WxPusher的UID
```

## 使用方法

1. 前往 https://wxpusher.zjiecode.com/ 注册账号并创建应用，获取 APP_TOKEN 和 UID
2. 配置 `.env` 文件
3. 运行程序：

```
python main.py
```

## 注意事项

- 问卷星可能会定期更新其网站结构，如果程序不再正常工作，可能需要更新代码
- 确保您有权限访问和查看问卷的回答
