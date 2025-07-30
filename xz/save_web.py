#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的网页保存工具
使用方法: python save_web.py <URL>
"""

import sys
import requests
from pathlib import Path
from datetime import datetime
import re
import json
from urllib.parse import urlparse

def save_webpage(url):
    """保存网页"""
    try:
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        # 获取页面
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or 'utf-8'
        
        # 创建保存目录
        output_dir = Path("saved_pages")
        output_dir.mkdir(exist_ok=True)
        
        # 提取标题
        title_match = re.search(r'<title[^>]*>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if title:
            # 清理标题中的特殊字符
            title = re.sub(r'[<>:"/\\|?*]', '_', title)
            title = title[:50]  # 限制长度
            filename = f"{title}_{timestamp}.html"
        else:
            # 使用URL生成文件名
            parsed = urlparse(url)
            domain = parsed.netloc.replace('.', '_')
            path = parsed.path.strip('/').replace('/', '_') or domain
            filename = f"{domain}_{path}_{timestamp}.html"
        
        # 保存文件
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # 保存元数据
        metadata = {
            'url': url,
            'title': title,
            'saved_at': datetime.now().isoformat(),
            'file_size': len(response.text)
        }
        
        metadata_file = filepath.with_suffix('.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 页面已保存: {filepath}")
        print(f"📄 文件大小: {len(response.text)} bytes")
        print(f"📋 标题: {title}")
        
        return True
        
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("使用方法: python save_web.py <URL>")
        print("示例: python save_web.py https://www.douban.com/group/topic/123456/")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"正在保存: {url}")
    save_webpage(url)

if __name__ == "__main__":
    main() 