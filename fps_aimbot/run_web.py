#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
运行Web服务器
"""

import sys
import os

# 添加项目路径到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)