import time
import threading
import json
import os
from ch9329Comm import keyboard, mouse
import serial

# 用于通知 main.py 配置已更新的文件
CONFIG_UPDATE_FILE = 'config_update.txt'


class FPSAimbot:
    def __init__(self, port_name='/dev/ttyUSB0', baud_rate=115200):
        """
        初始化FPS压枪宏
        :param port_name: 串口名称
        :param baud_rate: 波特率
        """
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.serial_port = None
        self.is_active = False  # 压枪宏是否激活
        self.is_enabled = False  # 压枪宏是否启用
        self.current_config = 1  # 当前配置编号
        self.configs = {}  # 存储所有配置
        self.keyboard_comm = None
        self.mouse_comm = None
        self.load_configs()
        
    def connect_serial(self):
        """
        连接串口
        """
        try:
            self.serial_port = serial.Serial(self.port_name, self.baud_rate)
            self.keyboard_comm = keyboard.DataComm()
            self.mouse_comm = mouse.DataComm()
            return True
        except Exception as e:
            print("串口连接失败: {}".format(e))
            return False
            
    def load_configs(self):
        """
        加载配置文件
        """
        config_file = 'configs.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.configs = json.load(f)
        else:
            # 默认配置
            self.configs = {
                "1": {
                    "name": "AKM",
                    "icon": "akm.png",
                    "recoil_pattern": [
                        [0, 2],
                        [1, 3],
                        [-1, 2],
                        [2, 4],
                        [-2, 3]
                    ]
                },
                "2": {
                    "name": "M416",
                    "icon": "m416.png",
                    "recoil_pattern": [
                        [0, 1],
                        [1, 2],
                        [0, 2],
                        [-1, 2],
                        [1, 3]
                    ]
                }
            }
            self.save_configs()
            
        # 检查配置更新文件
        if os.path.exists(CONFIG_UPDATE_FILE):
            os.remove(CONFIG_UPDATE_FILE)
            
    def save_configs(self):
        """
        保存配置文件
        """
        with open('configs.json', 'w') as f:
            json.dump(self.configs, f, indent=4)
            
        # 检查配置更新文件
        if os.path.exists(CONFIG_UPDATE_FILE):
            os.remove(CONFIG_UPDATE_FILE)
            
    def switch_config(self, config_num):
        """
        切换配置
        :param config_num: 配置编号 (1-9)
        """
        if str(config_num) in self.configs:
            self.current_config = config_num
            print("已切换到配置 {}: {}".format(config_num, self.configs[str(config_num)]['name']))
            
    def toggle_aimbot(self):
        """
        开启/关闭压枪宏
        """
        self.is_enabled = not self.is_enabled
        status = "开启" if self.is_enabled else "关闭"
        print("压枪宏已{}".format(status))
        
    def activate_aimbot(self):
        """
        激活压枪宏（按下鼠标左键时调用）
        """
        if not self.is_enabled:
            return
            
        self.is_active = True
        config = self.configs[str(self.current_config)]
        pattern = config["recoil_pattern"]
        
        # 执行压枪模式
        for move in pattern:
            if not self.is_active:  # 如果提前释放鼠标左键则停止
                break
            x, y = move
            self.mouse_comm.send_data_relatively(x, y)
            time.sleep(0.05)  # 50ms间隔，模拟射击间隔
            
    def deactivate_aimbot(self):
        """
        释放鼠标左键时调用
        """
        self.is_active = False
        
    def send_normal_input(self, key):
        """
        发送正常的键鼠操作（压枪宏关闭时）
        :param key: 按键
        """
        if not self.is_enabled:
            self.keyboard_comm.send_data(key)
            self.keyboard_comm.release()
            
    def handle_key_event(self, key):
        """
        处理键盘事件
        :param key: 按键
        """
        # 处理ALT+数字键事件
        if key.startswith('ALT+'):
            sub_key = key[4:]  # 获取ALT后的键
            if sub_key.isdigit():
                num = int(sub_key)
                if num == 0:
                    # ALT+0 切换压枪宏开关
                    self.toggle_aimbot()
                elif 1 <= num <= 9:
                    # ALT+1-9 切换配置
                    self.switch_config(num)
        
    def run(self):
        """
        运行主程序
        """
        if not self.connect_serial():
            return
            
        print("FPS压枪宏已启动")
        print("使用 ALT+0 开启/关闭压枪宏")
        print("使用 ALT+1-9 切换配置")
        print("按下鼠标左键激活压枪")
        
        # 这里应该监听键盘事件，但为了简化示例，我们用循环模拟
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.serial_port.close()
            print("程序已退出")