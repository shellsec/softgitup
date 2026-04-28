#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp 本地文件服务器
使用 Python 的 http.server 模块提供文件服务
"""

import http.server
import socketserver
import sys
import os
from pathlib import Path

# 默认端口
PORT = 8000

# 如果提供了端口参数，使用提供的端口
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print(f"错误: 无效的端口号: {sys.argv[1]}")
        sys.exit(1)

# 获取脚本所在目录作为服务器根目录
BASE_DIR = Path(__file__).parent.absolute()

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义 HTTP 请求处理器，添加 CORS 支持"""
    
    def end_headers(self):
        # 添加 CORS 头，允许跨域访问
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    """主函数"""
    print("=" * 60)
    print("SoftGitUp 本地文件服务器")
    print("=" * 60)
    print(f"服务器目录: {BASE_DIR}")
    print(f"服务器端口: {PORT}")
    print()
    print(f"访问地址: http://localhost:{PORT}/")
    print(f"软件列表: http://localhost:{PORT}/software/list.txt")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    print()
    
    # 切换到服务器根目录
    os.chdir(BASE_DIR)
    
    # 创建服务器
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"服务器已启动，监听端口 {PORT}...")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 10048:  # Windows: 端口已被占用
            print(f"错误: 端口 {PORT} 已被占用，请使用其他端口")
            print(f"用法: python {sys.argv[0]} [端口号]")
        else:
            print(f"错误: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)

if __name__ == "__main__":
    main()

