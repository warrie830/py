#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页自动保存工具
支持保存任意网页和豆瓣帖子的HTML文档
"""

import os
import re
import time
import requests
from urllib.parse import urlparse, urljoin
from datetime import datetime
from pathlib import Path
import json
from typing import Optional, Dict, Any
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('web_saver.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WebSaver:
    """网页保存器"""
    
    def __init__(self, output_dir: str = "saved_pages"):
        """
        初始化网页保存器
        
        Args:
            output_dir: 保存目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 请求头，模拟浏览器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # 豆瓣特定的请求头
        self.douban_headers = self.headers.copy()
        self.douban_headers.update({
            'Referer': 'https://www.douban.com/',
            'Cookie': 'bid=' + ''.join([chr(random.randint(65, 90)) for _ in range(11)])
        })
        
        # 会话对象，保持连接
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_page_content(self, url: str, is_douban: bool = False) -> Optional[str]:
        """
        获取网页内容
        
        Args:
            url: 网页URL
            is_douban: 是否为豆瓣页面
            
        Returns:
            网页HTML内容
        """
        try:
            headers = self.douban_headers if is_douban else self.headers
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 设置正确的编码
            response.encoding = response.apparent_encoding or 'utf-8'
            
            logger.info(f"成功获取页面: {url}")
            return response.text
            
        except requests.RequestException as e:
            logger.error(f"获取页面失败 {url}: {e}")
            return None
    
    def is_douban_url(self, url: str) -> bool:
        """
        判断是否为豆瓣URL
        
        Args:
            url: 网页URL
            
        Returns:
            是否为豆瓣页面
        """
        domain = urlparse(url).netloc.lower()
        return 'douban.com' in domain
    
    def generate_filename(self, url: str, title: str = None) -> str:
        """
        生成文件名
        
        Args:
            url: 网页URL
            title: 页面标题
            
        Returns:
            文件名
        """
        # 从URL中提取域名和路径
        parsed = urlparse(url)
        domain = parsed.netloc.replace('.', '_')
        path = parsed.path.strip('/').replace('/', '_')
        
        # 如果没有路径，使用域名
        if not path:
            path = domain
        
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 如果有标题，使用标题（清理特殊字符）
        if title:
            # 清理标题中的特殊字符
            title = re.sub(r'[<>:"/\\|?*]', '_', title)
            title = title[:50]  # 限制长度
            filename = f"{title}_{timestamp}.html"
        else:
            filename = f"{domain}_{path}_{timestamp}.html"
        
        return filename
    
    def extract_title(self, html_content: str) -> str:
        """
        从HTML中提取标题
        
        Args:
            html_content: HTML内容
            
        Returns:
            页面标题
        """
        # 尝试从title标签提取
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()
            if title:
                return title
        
        # 尝试从h1标签提取
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            title = h1_match.group(1).strip()
            if title:
                return title
        
        return ""
    
    def save_page(self, url: str, custom_title: str = None) -> bool:
        """
        保存网页
        
        Args:
            url: 网页URL
            custom_title: 自定义标题
            
        Returns:
            是否保存成功
        """
        try:
            # 判断是否为豆瓣页面
            is_douban = self.is_douban_url(url)
            
            # 获取页面内容
            html_content = self.get_page_content(url, is_douban)
            if not html_content:
                return False
            
            # 提取标题
            title = custom_title or self.extract_title(html_content)
            
            # 生成文件名
            filename = self.generate_filename(url, title)
            filepath = self.output_dir / filename
            
            # 保存HTML文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 保存元数据
            metadata = {
                'url': url,
                'title': title,
                'saved_at': datetime.now().isoformat(),
                'is_douban': is_douban,
                'file_size': len(html_content)
            }
            
            metadata_file = filepath.with_suffix('.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"页面已保存: {filepath}")
            logger.info(f"元数据已保存: {metadata_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"保存页面失败 {url}: {e}")
            return False
    
    def save_douban_post(self, url: str) -> bool:
        """
        专门保存豆瓣帖子
        
        Args:
            url: 豆瓣帖子URL
            
        Returns:
            是否保存成功
        """
        logger.info(f"正在保存豆瓣帖子: {url}")
        return self.save_page(url, custom_title="豆瓣帖子")
    
    def batch_save(self, urls: list, delay: float = 1.0) -> Dict[str, bool]:
        """
        批量保存网页
        
        Args:
            urls: URL列表
            delay: 请求间隔（秒）
            
        Returns:
            保存结果字典
        """
        results = {}
        
        for i, url in enumerate(urls, 1):
            logger.info(f"正在处理第 {i}/{len(urls)} 个URL: {url}")
            
            success = self.save_page(url)
            results[url] = success
            
            # 添加延迟，避免请求过于频繁
            if i < len(urls):
                time.sleep(delay)
        
        return results


def main():
    """主函数"""
    print("=" * 50)
    print("网页自动保存工具")
    print("=" * 50)
    
    # 创建保存器
    saver = WebSaver()
    
    while True:
        print("\n请选择操作:")
        print("1. 保存单个网页")
        print("2. 保存豆瓣帖子")
        print("3. 批量保存网页")
        print("4. 查看已保存的文件")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            url = input("请输入网页URL: ").strip()
            if url:
                success = saver.save_page(url)
                if success:
                    print("✅ 页面保存成功!")
                else:
                    print("❌ 页面保存失败!")
        
        elif choice == '2':
            url = input("请输入豆瓣帖子URL: ").strip()
            if url:
                success = saver.save_douban_post(url)
                if success:
                    print("✅ 豆瓣帖子保存成功!")
                else:
                    print("❌ 豆瓣帖子保存失败!")
        
        elif choice == '3':
            print("请输入URL列表（每行一个，输入空行结束）:")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                delay = float(input("请输入请求间隔（秒，默认1.0）: ") or "1.0")
                results = saver.batch_save(urls, delay)
                
                print("\n批量保存结果:")
                for url, success in results.items():
                    status = "✅ 成功" if success else "❌ 失败"
                    print(f"{url}: {status}")
        
        elif choice == '4':
            print(f"\n已保存的文件（保存在 {saver.output_dir}）:")
            for file in saver.output_dir.glob("*.html"):
                size = file.stat().st_size
                print(f"📄 {file.name} ({size} bytes)")
        
        elif choice == '5':
            print("感谢使用！")
            break
        
        else:
            print("无效选择，请重新输入！")


if __name__ == "__main__":
    import random
    main() 