from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
import os
import sys
import uuid
from PIL import Image
from werkzeug.utils import secure_filename


def get_base_path():
    """获取应用基础路径，支持 PyInstaller 打包后的环境"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后
        return os.path.dirname(sys.executable)
    else:
        # 开发环境
        return os.path.dirname(os.path.abspath(__file__))


def get_template_path():
    """获取模板目录路径"""
    base_path = get_base_path()
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后，模板在 _internal/templates 中
        return os.path.join(base_path, '_internal', 'templates')
    else:
        # 开发环境
        return os.path.join(base_path, 'templates')


app = Flask(__name__, template_folder=get_template_path())
app.secret_key = os.urandom(24)  # 用于 flash 消息

# 配置项 - 使用绝对路径
base_path = get_base_path()
UPLOAD_FOLDER = os.path.join(base_path, 'uploads')
OUTPUT_FOLDER = os.path.join(base_path, 'outputs')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB 最大文件大小
IMAGE_QUALITY = 95  # 输出 JPEG 质量

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def allowed_file(filename):
    """
    检查文件扩展名是否在允许的列表中。
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_unique_filename(filename):
    """
    生成唯一文件名，避免覆盖已有文件。
    """
    name, ext = os.path.splitext(filename)
    unique_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
    return unique_name


def resize_image(input_path, output_path, width, height, maintain_aspect=False, quality=IMAGE_QUALITY):
    """
    调整图片大小并保存到指定路径。

    参数：
        input_path (str): 输入图片的路径。
        output_path (str): 输出图片的路径。
        width (int): 调整后的宽度。
        height (int): 调整后的高度。
        maintain_aspect (bool): 是否保持宽高比。
        quality (int): 输出图片质量 (1-100)。
    """
    # 使用 LANCZOS 重采样滤波器，获得更好的图像质量
    resampling_filter = Image.Resampling.LANCZOS
    
    with Image.open(input_path) as img:
        # 处理特殊图片类型
        if img.mode in ('P', 'PA'):
            img = img.convert('RGBA')
        elif img.mode == 'CMYK':
            img = img.convert('RGB')
        
        if maintain_aspect:
            # 保持宽高比，自适应调整
            img.thumbnail((width, height), resampling_filter)
        else:
            # 强制调整到指定尺寸
            img = img.resize((width, height), resampling_filter)
        
        # 保存处理后的图片
        save_kwargs = {}
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            # JPEG 不支持透明度，转换为 RGB
            if img.mode in ('RGBA', 'LA', 'PA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img, mask=img.split()[-1])
                img = background
            save_kwargs['quality'] = quality
            save_kwargs['format'] = 'JPEG'
        elif output_path.lower().endswith('.png'):
            save_kwargs['format'] = 'PNG'
        
        img.save(output_path, **save_kwargs)


def cleanup_old_files(folder, max_age_hours=24):
    """
    清理指定目录中超过指定时间的文件。
    """
    import time
    current_time = time.time()
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            file_age = current_time - os.path.getmtime(filepath)
            if file_age > max_age_hours * 3600:
                try:
                    os.remove(filepath)
                except OSError:
                    pass


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'file' not in request.files:
            flash('没有文件被选择', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # 检查文件名是否为空
        if file.filename == '':
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        # 检查文件类型是否允许
        if not allowed_file(file.filename):
            flash(f'不支持的文件类型，仅支持: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
            return redirect(request.url)
        
        # 获取并验证尺寸参数
        try:
            width = int(request.form.get('width', 0))
            height = int(request.form.get('height', 0))
            maintain_aspect = request.form.get('maintain_aspect') == 'on'
        except (ValueError, TypeError):
            flash('请输入有效的尺寸数值', 'error')
            return redirect(request.url)
        
        if width <= 0 or height <= 0:
            flash('宽度和高度必须大于0', 'error')
            return redirect(request.url)
        
        if width > 100000 or height > 100000:
            flash('尺寸过大，最大支持 100000x100000 像素', 'error')
            return redirect(request.url)
        
        try:
            # 使用安全文件名并处理唯一性
            original_filename = secure_filename(file.filename)
            unique_filename = get_unique_filename(original_filename)
            
            # 保存上传的文件
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(input_path)
            
            # 生成输出文件名
            name, ext = os.path.splitext(unique_filename)
            output_filename = f"{name}_resized{ext}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            # 调整图片大小
            resize_image(input_path, output_path, width, height, maintain_aspect)
            
            flash('图片调整成功！', 'success')
            return redirect(url_for('download', filename=output_filename))
            
        except Exception as e:
            flash(f'处理图片时出错: {str(e)}', 'error')
            # 清理可能产生的临时文件
            if os.path.exists(input_path):
                os.remove(input_path)
            return redirect(request.url)
    
    return render_template('index.html')


@app.route('/outputs/<filename>')
def serve_file(filename):
    """
    提供输出目录中的文件下载。
    """
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


@app.route('/download/<filename>')
def download(filename):
    """
    提供下载页面。
    """
    return render_template('index.html', download_filename=filename)


@app.route('/api/image_info', methods=['POST'])
def get_image_info():
    """
    API: 获取上传图片的尺寸信息。
    """
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件类型'}), 400
    
    try:
        from io import BytesIO
        content = file.read()
        img = Image.open(BytesIO(content))
        return jsonify({
            'width': img.size[0],
            'height': img.size[1],
            'format': img.format or img.mode,
            'mode': img.mode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/cleanup', methods=['POST'])
def cleanup():
    """
    API: 清理临时文件。
    """
    try:
        cleanup_old_files(app.config['UPLOAD_FOLDER'], max_age_hours=1)
        cleanup_old_files(app.config['OUTPUT_FOLDER'], max_age_hours=24)
        return jsonify({'message': '清理完成'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # 打包后禁用 debug 模式，避免重启导致的问题
    import sys
    app.run(debug=False, host='0.0.0.0', port=5000)
