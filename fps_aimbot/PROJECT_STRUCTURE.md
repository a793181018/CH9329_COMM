# FPS Aimbot 项目结构说明

## 目录结构

```
fps_aimbot/
├── README.md                  # 项目说明文档
├── main.py                    # 主程序入口
├── aimbot.py                  # 压枪宏核心逻辑
├── web_app.py                 # Web应用
├── run_web.py                 # Web服务器启动脚本
├── requirements.txt           # 项目依赖
├── configs.json               # 配置文件
├── PROJECT_STRUCTURE.md       # 项目结构说明
├── static/                    # 静态文件目录
│   └── icons/                 # 武器图标
│       ├── akm.png
│       ├── m416.png
│       └── scar.png
└── templates/                 # HTML模板目录
    └── index.html             # 主页面模板
```

## 文件说明

### 核心文件

1. **main.py**: 程序入口文件，负责初始化压枪宏控制器、连接串口设备、启动键盘鼠标监听器和Web服务器。

2. **aimbot.py**: 压枪宏核心逻辑实现，包括：
   - 串口通信连接
   - 配置文件加载与保存
   - 压枪宏开关控制
   - 配置切换
   - 压枪模式执行
   - 键鼠事件处理

3. **web_app.py**: Web应用实现，基于Flask框架，提供：
   - 状态信息API
   - 配置管理API
   - Web界面路由

4. **run_web.py**: 独立运行Web服务器的脚本。

### 配置文件

1. **configs.json**: 存储不同武器的压枪配置，包括武器名称、图标和压枪模式。

2. **requirements.txt**: 项目依赖库列表。

### 资源文件

1. **static/icons/**: 存放武器图标文件。

2. **templates/index.html**: Web界面模板。

### 文档

1. **README.md**: 项目说明文档。

2. **PROJECT_STRUCTURE.md**: 项目结构说明文档。