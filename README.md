# 图片大小调整工具

## 📋 项目简介

这是一个基于 Python 和 Flask 的图片大小调整工具。用户可以通过网页上传图片，输入目标宽度和高度，调整图片大小并下载结果。项目支持保持宽高比、图片预览、拖拽上传等功能。

> 作者：魅影m1y1 | 版本：2.0.0

## ✨ 功能特点

- **单张图片调整**：上传一张图片，自定义目标尺寸
- **保持宽高比**：自动锁定比例，防止图片变形
- **批量处理**：命令行支持目录级批量调整
- **拖拽上传**：支持拖拽图片到上传区域
- **实时预览**：上传后自动显示图片预览和尺寸信息
- **自动填充尺寸**：上传后自动填充原始图片尺寸
- **错误提示**：完善的表单验证和错误提示
- **文件安全**：文件类型验证、大小限制、安全文件名
- **自动清理**：支持清理过期临时文件
- **现代化界面**：渐变背景、粒子动画、响应式设计
- **打包exe**：可打包为独立可执行文件

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | Flask >= 2.0 |
| 图像处理 | Pillow >= 9.0 |
| 文件安全 | Werkzeug (secure_filename) |
| 打包工具 | PyInstaller |

## 📦 打包可执行文件

使用 PyInstaller 打包为独立的 `.exe` 文件：

```bash
pip install pyinstaller
pyinstaller --clean ImageResizer.spec
```

打包完成后，可执行文件位于 `dist/ImageResizer/` 目录。

## 📦 安装依赖

1. **创建虚拟环境（可选）**：

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

2. **安装依赖**：

```bash
pip install -r requirements.txt
```

## 🚀 运行项目

### 方式一：Web 应用

1. **启动 Flask 应用**：

```bash
python app.py
```

2. **打开浏览器**，访问 `http://127.0.0.1:5000`

### 方式二：命令行工具

```bash
python resize_image.py
```

按提示选择模式：
- 模式1：单张图片调整
- 模式2：批量调整
- 模式3：查看图片信息

### 方式三：使用可执行文件

直接运行 `dist/ImageResizer/ImageResizer.exe`（无需安装 Python 环境）

**如何关闭网站：**
- 运行 exe 后会弹出一个控制台窗口，显示 Flask 服务器的日志
- 在控制台窗口中按 `Ctrl + C` 即可停止服务器
- 或者直接关闭控制台窗口

## 📁 文件结构

```
.
├── app.py                      # Flask Web 应用主文件
├── resize_image.py             # 图像处理命令行模块
├── requirements.txt            # Python 依赖
├── ImageResizer.spec           # PyInstaller 打包配置
├── README.md                   # 项目说明
├── development_log.md          # 开发日志
├── build/                      # PyInstaller 构建临时目录（可删除）
├── dist/
│   └── ImageResizer/           # 打包后的可执行文件
│       ├── ImageResizer.exe
│       └── _internal/
├── templates/
│   └── index.html              # Web 界面模板
├── uploads/                    # 上传的临时文件目录
└── outputs/                    # 处理结果输出目录
```

## 📦 打包说明

```bash
# 打包命令
pyinstaller --clean ImageResizer.spec

# 打包结果位于 dist/ImageResizer/ 目录
# build/ 目录是临时文件，可以安全删除
```

## 📖 使用说明

### Web 界面

1. **上传图片**：点击上传区域或拖拽图片到页面
2. **设置尺寸**：输入目标宽度和高度（默认自动填充原始尺寸）
3. **保持比例**：默认锁定宽高比，可点击链条图标解锁
4. **调整大小**：点击按钮提交处理
5. **下载结果**：处理后点击下载链接保存

### 命令行

```python
from resize_image import resize_image, batch_resize_images

# 单张调整
resize_image('input.png', 'output.png', 800, 600, maintain_aspect=True)

# 批量处理
batch_resize_images('./input_dir', './output_dir', 800, 600)
```

## 🔧 API 接口

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET/POST | 主页面 |
| `/outputs/<filename>` | GET | 下载处理后的图片 |
| `/api/image_info` | POST | 获取图片信息 (JSON) |
| `/cleanup` | POST | 清理临时文件 |

## ⚙️ 配置项

在 `app.py` 中可修改以下配置：

```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}
MAX_FILE_SIZE = 16 * 1024 * 1024    # 16MB
IMAGE_QUALITY = 95                   # JPEG 质量
```

## 📝 支持的图片格式

- PNG
- JPG / JPEG
- GIF
- BMP
- WebP
- TIFF

## ⚠️ 注意事项

- 上传文件大小限制为 16MB
- JPEG 格式不支持透明度，会自动填充白色背景
- 建议保持宽高比以避免图片变形
- 临时文件会在 24 小时后自动清理

## 🔄 后续计划

- [ ] 增加裁剪、旋转等更多图片处理功能
- [ ] 提供多语言支持
- [ ] 添加图片压缩功能
- [ ] 支持更多输出格式转换
- [ ] 优化移动端体验

## 📄 许可证

MIT License

---

© 2026 魅影m1y1