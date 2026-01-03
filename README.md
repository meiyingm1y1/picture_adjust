# 图片大小调整工具

## 项目简介
这是一个基于 Python 和 Flask 的图片大小调整工具。该项目由“魅影m1y1”独立开发，用户可以通过网页上传图片，输入目标宽度和高度，调整图片大小并下载结果。

## 功能特点
- 支持单张图片大小调整。
- 支持批量调整目录中所有图片的大小。
- 提供现代化的网页界面，用户体验良好。
- 动态背景效果，提升视觉吸引力。

## 安装依赖
1. 创建虚拟环境（可选）：

```bash
python -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 运行项目
1. 启动 Flask 应用：

```bash
python app.py
```

2. 打开浏览器，访问 `http://127.0.0.1:5000`。

## 文件结构
```
.
├── app.py              # Flask 应用主文件
├── resize_image.py     # 图片大小调整脚本
├── requirements.txt    # 项目依赖文件
├── templates/          # HTML 模板文件夹
│   └── index.html      # 网页界面
├── uploads/            # 上传的图片存储目录
├── outputs/            # 调整后的图片存储目录
└── README.md           # 项目说明文件
```

## 后续计划
- 增加更多图片处理功能，例如裁剪、旋转等。
- 提供多语言支持，提升用户覆盖面。
- 优化代码结构，提升可维护性和扩展性。

---

© 2026 魅影m1y1