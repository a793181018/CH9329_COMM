#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FPS压枪宏主程序
"""

import sys
import os
import threading
import time
from flask import Flask
from aimbot import FPSAimbot
from pynput import keyboard, mouse
from web_app import app as web_app
import json

# 添加项目路径到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class FPSAimbotController:
    def __init__(self):
        self.aimbot = FPSAimbot()
        self.alt_pressed = False
        
    def on_key_press(self, key):
        """
        键盘按下事件处理
        """
        try:
            # 检查是否按下了ALT键
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = True
                return
            
            # 如果ALT键已按下，检查数字键
            if self.alt_pressed:
                if hasattr(key, 'char') and key.char and key.char.isdigit():
                    num = int(key.char)
                    if num == 0:
                        # ALT+0 切换压枪宏开关
                        self.aimbot.toggle_aimbot()
                    elif 1 <= num <= 9:
                        # ALT+1-9 切换配置
                        self.aimbot.switch_config(num)
        except Exception as e:
            print("处理键盘按下事件时出错: {}".format(e))
            
    def on_key_release(self, key):
        """
        键盘释放事件处理
        """
        try:
            # 检查是否释放了ALT键
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = False
        except Exception as e:
            print("处理键盘释放事件时出错: {}".format(e))
            
    def on_mouse_click(self, x, y, button, pressed):
        """
        鼠标点击事件处理
        """
        try:
            if button == mouse.Button.left:
                if pressed:
                    # 鼠标左键按下，激活压枪
                    self.aimbot.activate_aimbot()
                else:
                    # 鼠标左键释放
                    self.aimbot.deactivate_aimbot()
        except Exception as e:
            print("处理鼠标点击事件时出错: {}".format(e))


def main():
    # 创建压枪宏控制器实例
    controller = FPSAimbotController()
    
    # 连接串口
    if not controller.aimbot.connect_serial():
        print("无法连接到串口设备，请检查设备连接！")
        return
    
    print("FPS压枪宏已启动")
    print("使用 ALT+0 开启/关闭压枪宏")
    print("使用 ALT+1-9 切换配置")
    print("按下鼠标左键激活压枪")
    
    # 启动键盘监听
    key_listener = keyboard.Listener(
        on_press=controller.on_key_press,
        on_release=controller.on_key_release)
    key_listener.start()
    
    # 启动鼠标监听
    mouse_listener = mouse.Listener(on_click=controller.on_mouse_click)
    mouse_listener.start()
    
    # 启动Web服务器
    web_thread = threading.Thread(target=lambda: web_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False))
    web_thread.daemon = True
    web_thread.start()
    
    # 运行主程序
    try:
        while True:
            time.sleep(1)
            # 检查配置文件是否更新
            controller.aimbot.load_configs()
    except KeyboardInterrupt:
        controller.aimbot.serial_port.close()
        key_listener.stop()
        mouse_listener.stop()
        print("程序已退出")


if __name__ == "__main__":
    main()