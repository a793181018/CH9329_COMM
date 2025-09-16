from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__, static_folder='static')

# 用于通知 main.py 配置已更新的文件
CONFIG_UPDATE_FILE = 'config_update.txt'

# 全局变量存储状态
aimbot_status = {
    "is_enabled": False,
    "current_config": 1,
    "configs": {}
}

# 加载配置
config_file = 'configs.json'
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        aimbot_status["configs"] = json.load(f)
else:
    # 默认配置
    aimbot_status["configs"] = {
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

@app.route('/')
def index():
    return render_template('index.html', status=aimbot_status)

@app.route('/api/status')
def get_status():
    return jsonify(aimbot_status)

@app.route('/api/toggle', methods=['POST'])
def toggle_aimbot():
    aimbot_status["is_enabled"] = not aimbot_status["is_enabled"]
    return jsonify(aimbot_status)

@app.route('/api/switch_config', methods=['POST'])
def switch_config():
    config_num = request.json.get('config')
    if str(config_num) in aimbot_status["configs"]:
        aimbot_status["current_config"] = config_num
    return jsonify(aimbot_status)

@app.route('/api/configs', methods=['GET'])
def get_configs():
    return jsonify(aimbot_status["configs"])

@app.route('/api/configs', methods=['POST'])
def update_configs():
    configs = request.json
    aimbot_status["configs"] = configs
    
    # 保存到文件
    with open('configs.json', 'w') as f:
        json.dump(configs, f, indent=4)
    
    # 通知 main.py 配置已更新
    notify_main_py()
    
    return jsonify({"status": "success"})

def notify_main_py():
    """
    通知 main.py 配置已更新
    """
    with open(CONFIG_UPDATE_FILE, 'w') as f:
        f.write('updated')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)